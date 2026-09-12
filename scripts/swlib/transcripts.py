"""Claude Code's own transcripts, read as measurements.

The toolkit's other modules review the novel. This one reviews the *run that produced it*:
what it cost, how long it took, and - the question `docs/benchmark.md` could not answer without
it - which skill files the model actually opened.

**The accounting rule that makes this module necessary.** Claude Code writes one JSONL row per
*content block* of an API response, and every row of that response repeats the same `usage`
object verbatim. Summing rows therefore bills one request as many as seven. Benchmark run #1 was
counted that way and overstated cache reads by 1.9x, cache writes by 8.7x and the total by 3.6x.
So: rows are grouped into a `Response` by `(requestId, message.id)`, the input-side fields are
taken **once** per group, and `output_tokens` - which is a running counter during streaming, with
early rows holding partials - is taken as the group's maximum.

**Privacy.** Nothing here reads prompt text, tool results, or assistant prose. The extracted
fields are exactly: type, timestamp, cwd, requestId, message.id, message.model, message.usage,
and the *names* and `file_path`s of tool calls. A reader pointed at somebody's own transcripts
should be able to say precisely that, so it does.

**Portability.** Claude Code escapes a project's path into its own directory name, and the
escaping differs between platforms. That name is never reconstructed here. Every `*.jsonl` under
the config root is opened and kept only if one of its rows reports a `cwd` inside the repo, which
works the same on Windows, macOS and Linux.
"""

import calendar
import glob
import json
import os
import re

# A skill load, matched on the *suffix* of whatever absolute path the transcript recorded: the
# repo sat somewhere else on the machine that wrote it, and will sit somewhere else again.
SKILL_PATH = re.compile(r"(?:^|/)\.claude/skills/([a-z0-9][a-z0-9._-]*)/(.+)$")
# The same path seen inside a shell command rather than in a `file_path` argument. A model told
# to prefer Bash reads `cat .claude/skills/x/SKILL.md`, and the path never reaches an argument
# this scanner used to look at - so benchmark run #4 reported "0 of 44 skills opened" for a run
# that opened thirteen. The finding-9 measurement is only as good as the tool the model happens
# to read with, so it has to see both.
SKILL_IN_TEXT = re.compile(r"\.claude/skills/([a-z0-9][a-z0-9._-]*)/([A-Za-z0-9._/-]+)")
CHAPTER_PATH = re.compile(r"(?:^|/)novels/([^/]+)/chapters/(\d+)[^/]*$")

# Rows carrying no real usage. `<synthetic>` is Claude Code's own placeholder for a message it
# generated locally (an interrupt notice, a hook result) and never sent to an API.
SYNTHETIC_MODELS = ("<synthetic>",)

USAGE_FIELDS = ("input_tokens", "cache_creation_input_tokens",
                "cache_read_input_tokens", "output_tokens")


def default_root():
    """Where Claude Code keeps its transcripts. `$CLAUDE_CONFIG_DIR` wins, else `~/.claude`."""
    env = os.environ.get("CLAUDE_CONFIG_DIR")
    if env:
        return os.path.abspath(os.path.expanduser(env))
    return os.path.join(os.path.expanduser("~"), ".claude")


def _norm(path):
    return os.path.normcase(os.path.abspath(path))


def _under(path, root):
    """True if `path` is `root` or inside it. Both are normalised first."""
    if not path:
        return False
    p, r = _norm(path), _norm(root)
    return p == r or p.startswith(r + os.sep)


def iter_rows(path):
    """Yield each JSON object in a JSONL file, skipping anything that will not parse.

    A live session's last line is routinely half-written, and a transcript is somebody else's
    file: a measurement tool that raises on it is a measurement tool nobody runs twice.
    """
    try:
        fh = open(path, encoding="utf-8", errors="replace")
    except (IOError, OSError):
        return
    with fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            try:
                row = json.loads(line)
            except ValueError:
                continue
            if isinstance(row, dict):
                yield row


class Response(object):
    """One billable API request, assembled from every row that shares its id."""

    __slots__ = ("key", "model", "timestamp", "rows", "input_tokens",
                 "cache_write_5m", "cache_write_1h", "cache_read", "output_tokens")

    def __init__(self, key):
        self.key = key
        self.model = ""
        self.timestamp = ""
        self.rows = 0
        self.input_tokens = 0
        self.cache_write_5m = 0
        self.cache_write_1h = 0
        self.cache_read = 0
        self.output_tokens = 0

    @property
    def cache_write(self):
        return self.cache_write_5m + self.cache_write_1h

    def absorb(self, row, usage):
        """Fold one row in. Input-side fields are set, not added; output takes the maximum."""
        self.rows += 1
        if not self.timestamp:
            self.timestamp = row.get("timestamp") or ""
        if not self.model:
            self.model = ((row.get("message") or {}).get("model")) or ""
        # Identical on every row of the response, so assignment - not `+=` - is the whole fix.
        self.input_tokens = usage.get("input_tokens") or 0
        self.cache_read = usage.get("cache_read_input_tokens") or 0
        created = usage.get("cache_creation") or {}
        w5 = created.get("ephemeral_5m_input_tokens")
        w1 = created.get("ephemeral_1h_input_tokens")
        if w5 is None and w1 is None:
            # Older transcripts carry only the total. Price it at the 5-minute rate, which is
            # what a run without an explicit 1-hour cache actually gets.
            self.cache_write_5m = usage.get("cache_creation_input_tokens") or 0
            self.cache_write_1h = 0
        else:
            self.cache_write_5m = w5 or 0
            self.cache_write_1h = w1 or 0
        # A streaming counter: the final row holds the total. Taken as a maximum so that rows
        # arriving out of order cannot truncate the count.
        self.output_tokens = max(self.output_tokens, usage.get("output_tokens") or 0)


class Session(object):
    """One transcript file: a main session, or one subagent of it."""

    def __init__(self, path, root):
        self.path = path
        self.rel = os.path.relpath(path, root).replace(os.sep, "/")
        self.responses = []
        self.naive_totals = dict((f, 0) for f in USAGE_FIELDS)
        self.rows = 0
        self.tools = {}
        self.skills = {}            # skill name -> times opened
        self.skill_files = {}       # "name/file.md" -> times opened
        self.artifacts = []         # (timestamp, novel slug, chapter number)
        self.first_ts = ""
        self.last_ts = ""
        self.models = {}
        self.agent_id = ""
        self.session_id = ""
        self.cwds = set()

    @property
    def is_subagent(self):
        return "/subagents/" in self.path.replace(os.sep, "/")

    @property
    def label(self):
        if self.is_subagent:
            return "agent %s" % (self.agent_id or os.path.basename(self.path))[:20]
        return "session %s" % (self.session_id or os.path.basename(self.path))[:20]

    @property
    def duration_s(self):
        return _span_seconds(self.first_ts, self.last_ts)

    def totals(self):
        t = dict((f, 0) for f in USAGE_FIELDS)
        t["cache_write_5m"] = 0
        t["cache_write_1h"] = 0
        for r in self.responses:
            t["input_tokens"] += r.input_tokens
            t["cache_creation_input_tokens"] += r.cache_write
            t["cache_read_input_tokens"] += r.cache_read
            t["output_tokens"] += r.output_tokens
            t["cache_write_5m"] += r.cache_write_5m
            t["cache_write_1h"] += r.cache_write_1h
        return t


_TS = re.compile(r"^(\d{4})-(\d\d)-(\d\d)T(\d\d):(\d\d):(\d\d)")


def _ts_seconds(stamp):
    """Seconds since epoch-ish, from an ISO timestamp. None when unparseable.

    Deliberately not `datetime.fromisoformat`: it rejects the trailing `Z` before Python 3.11,
    and this file has to run on 3.8.
    """
    m = _TS.match(str(stamp or ""))
    if not m:
        return None
    y, mo, d, h, mi, s = (int(x) for x in m.groups())
    try:
        return calendar.timegm((y, mo, d, h, mi, s, 0, 0, 0))
    except (ValueError, OverflowError):
        return None


def _span_seconds(first, last):
    a, b = _ts_seconds(first), _ts_seconds(last)
    if a is None or b is None or b < a:
        return 0
    return b - a


def _bump(counter, key, n=1):
    counter[key] = counter.get(key, 0) + n


def read_session(path, root):
    """Parse one transcript into a Session. Reads only the fields named in the module docstring."""
    sess = Session(path, root)
    groups = {}
    order = []
    for row in iter_rows(path):
        sess.rows += 1
        stamp = row.get("timestamp") or ""
        if stamp:
            if not sess.first_ts or stamp < sess.first_ts:
                sess.first_ts = stamp
            if stamp > sess.last_ts:
                sess.last_ts = stamp
        if row.get("cwd"):
            sess.cwds.add(row["cwd"])
        sess.agent_id = sess.agent_id or (row.get("agentId") or "")
        sess.session_id = sess.session_id or (row.get("sessionId") or "")

        message = row.get("message") or {}
        _scan_tools(sess, message, stamp)

        if row.get("type") != "assistant":
            continue
        model = message.get("model") or ""
        if model in SYNTHETIC_MODELS:
            continue
        usage = message.get("usage") or {}
        if not usage:
            continue
        _bump(sess.models, model or "(unknown)")
        for field in USAGE_FIELDS:
            sess.naive_totals[field] += usage.get(field) or 0

        key = (row.get("requestId") or "", message.get("id") or "", row.get("uuid") or "")
        # Only the first two identify a request; the uuid is the fallback for a transcript old
        # enough to carry neither, where every row is its own response.
        key = key[:2] if (key[0] or key[1]) else key
        if key not in groups:
            groups[key] = Response(key)
            order.append(key)
        groups[key].absorb(row, usage)

    sess.responses = [groups[k] for k in order]
    return sess


def _scan_tools(sess, message, stamp):
    """Count tool calls, and note skill opens and chapter writes. Names and paths only."""
    for block in (message.get("content") or []):
        if not isinstance(block, dict) or block.get("type") != "tool_use":
            continue
        name = block.get("name") or "(unnamed)"
        _bump(sess.tools, name)
        args = block.get("input")
        if not isinstance(args, dict):
            continue

        if name == "Skill":
            skill = args.get("skill")
            if isinstance(skill, str) and skill:
                _bump(sess.skills, skill)
                _bump(sess.skill_files, "%s (Skill tool)" % skill)
            continue

        path = args.get("file_path") or args.get("path") or args.get("notebook_path")
        if not isinstance(path, str) or not path:
            # A shell command carries its paths in the command string. Scan it for skill files
            # so a Bash-driven read is not invisible; chapter writes stay argument-anchored,
            # because `sed -i` and a heredoc are not reliably a write to the file named first.
            for field in ("command", "cmd"):
                text = args.get(field)
                if isinstance(text, str) and text:
                    seen = set()
                    for skill, rest in SKILL_IN_TEXT.findall(text.replace("\\", "/")):
                        if (skill, rest) in seen:
                            continue
                        seen.add((skill, rest))
                        _bump(sess.skills, skill)
                        _bump(sess.skill_files, "%s/%s" % (skill, rest))
            continue
        unix = path.replace("\\", "/")
        m = SKILL_PATH.search(unix)
        if m:
            _bump(sess.skills, m.group(1))
            _bump(sess.skill_files, "%s/%s" % (m.group(1), m.group(2)))
        if name in ("Write", "Edit", "NotebookEdit"):
            c = CHAPTER_PATH.search(unix)
            if c:
                sess.artifacts.append((stamp, c.group(1), int(c.group(2))))


def transcript_files(root):
    """Every transcript under a config root: main sessions first, then subagent files."""
    projects = os.path.join(root, "projects")
    found = sorted(glob.glob(os.path.join(projects, "*", "*.jsonl")))
    found += sorted(glob.glob(os.path.join(projects, "*", "*", "subagents", "*.jsonl")))
    return found


def sessions_for(repo_root, root=None, include_all=False, since=None, until=None,
                 session=None):
    """Every session whose rows report a cwd inside `repo_root`.

    `include_all` keeps sessions that report no cwd at all, which is what a hand-made fixture
    and a very old transcript look like.

    `session` selects one transcript by session id, agent id, or path fragment. A time window
    alone is **not** enough to measure what a writing agent did: the session driving that agent
    is running at the same time, in the same repo, and its own file reads land in the same
    window - which is how a driving session's exploration got counted as the agent's skill loads.

    `since`/`until` are ISO 8601 prefixes bounding a single run. Without them every session ever
    run in this repo is aggregated together - on the machine that produced benchmark run #2 that
    was 22 sessions and $225 of toolkit development, none of it the run being measured.
    """
    root = root or default_root()
    out = []
    if not os.path.isdir(root):
        return out
    for path in transcript_files(root):
        sess = read_session(path, root)
        if not sess.rows:
            continue
        if session and session not in (sess.session_id or "") \
                and session not in (sess.agent_id or "") and session not in sess.rel:
            continue
        if since and sess.last_ts and sess.last_ts < since:
            continue
        if until and sess.first_ts and sess.first_ts > until:
            continue
        matched = any(_under(c, repo_root) for c in sess.cwds)
        if matched or (include_all and not sess.cwds):
            out.append(sess)
    out.sort(key=lambda s: (s.first_ts, s.rel))
    return out


def aggregate(sessions):
    """Totals across sessions, plus the naive row-sum so the overcount stays visible."""
    agg = {
        "sessions": len(sessions),
        "responses": 0,
        "rows": 0,
        "input_tokens": 0,
        "cache_write_5m": 0,
        "cache_write_1h": 0,
        "cache_creation_input_tokens": 0,
        "cache_read_input_tokens": 0,
        "output_tokens": 0,
        "naive": dict((f, 0) for f in USAGE_FIELDS),
        "tools": {},
        "skills": {},
        "skill_files": {},
        "models": {},
        "first_ts": "",
        "last_ts": "",
    }
    for s in sessions:
        t = s.totals()
        agg["responses"] += len(s.responses)
        agg["rows"] += s.rows
        for field in ("input_tokens", "cache_creation_input_tokens",
                      "cache_read_input_tokens", "output_tokens",
                      "cache_write_5m", "cache_write_1h"):
            agg[field] += t[field]
        for field in USAGE_FIELDS:
            agg["naive"][field] += s.naive_totals[field]
        for src, dst in ((s.tools, "tools"), (s.skills, "skills"),
                         (s.skill_files, "skill_files"), (s.models, "models")):
            for k, v in src.items():
                _bump(agg[dst], k, v)
        if s.first_ts and (not agg["first_ts"] or s.first_ts < agg["first_ts"]):
            agg["first_ts"] = s.first_ts
        if s.last_ts > agg["last_ts"]:
            agg["last_ts"] = s.last_ts
    agg["duration_s"] = _span_seconds(agg["first_ts"], agg["last_ts"])
    return agg


def by_chapter(sessions, since=None):
    """Attribute each response to the chapter whose last write follows it.

    Anchored on the **last** write of a chapter file rather than the first: a revision step
    rewrites the same file, and anchoring on the first pushes revision cost into the next
    chapter's bucket. The first chapter's bucket therefore absorbs all preceding setup, which is
    a property of the measurement and is printed as such.
    """
    marks = {}
    for sess in sessions:
        for stamp, slug, number in sess.artifacts:
            if not stamp:
                continue
            key = (slug, number)
            if stamp > marks.get(key, ""):
                marks[key] = stamp
    if not marks:
        return []

    ordered = sorted(marks.items(), key=lambda kv: kv[1])
    buckets = [{"slug": k[0], "chapter": k[1], "until": ts, "responses": 0,
                "input_tokens": 0, "cache_write_5m": 0, "cache_write_1h": 0,
                "cache_read_input_tokens": 0, "output_tokens": 0, "first_ts": "", "last_ts": "",
                "by_model": {}}
               for k, ts in ordered]

    responses = []
    for sess in sessions:
        responses.extend(sess.responses)
    responses.sort(key=lambda r: r.timestamp or "")

    # There was a guard for responses after the last chapter write and none for those before the
    # first, so on an unscoped root every prior session in the repo landed in chapter 1's bucket.
    # Benchmark run #2, F5.
    #
    # The head boundary is `since` and nothing else. Guessing one from the first bucket would
    # strip that chapter of the setup it is documented to absorb - the cure being worse than the
    # disease. With no `since`, cmd_trace reports the unscoped span instead of moving cost.
    head = since or ""
    pre = {"responses": 0, "input_tokens": 0, "cache_write_5m": 0, "cache_write_1h": 0,
           "cache_read_input_tokens": 0, "output_tokens": 0, "by_model": {}}

    idx = 0
    for r in responses:
        stamp = r.timestamp or ""
        if head and stamp and stamp < head:
            _tally(pre, r)
            continue
        while idx < len(buckets) and stamp > buckets[idx]["until"]:
            idx += 1
        if idx >= len(buckets):
            break                      # after the last chapter write: unattributed
        b = buckets[idx]
        b["responses"] += 1
        b["input_tokens"] += r.input_tokens
        b["cache_write_5m"] += r.cache_write_5m
        b["cache_write_1h"] += r.cache_write_1h
        b["cache_read_input_tokens"] += r.cache_read
        b["output_tokens"] += r.output_tokens
        # Kept per model so the bucket can be priced rather than blended: a run that switched
        # models mid-chapter is exactly the case a single blended rate gets wrong.
        m = b["by_model"].setdefault(r.model or "(unknown)", {
            "responses": 0, "input_tokens": 0, "cache_write_5m": 0, "cache_write_1h": 0,
            "cache_read_input_tokens": 0, "output_tokens": 0})
        m["responses"] += 1
        m["input_tokens"] += r.input_tokens
        m["cache_write_5m"] += r.cache_write_5m
        m["cache_write_1h"] += r.cache_write_1h
        m["cache_read_input_tokens"] += r.cache_read
        m["output_tokens"] += r.output_tokens
        if stamp and (not b["first_ts"] or stamp < b["first_ts"]):
            b["first_ts"] = stamp
        if stamp > b["last_ts"]:
            b["last_ts"] = stamp
    for b in buckets:
        b["duration_s"] = _span_seconds(b["first_ts"], b["last_ts"])
        b["cache_creation_input_tokens"] = b["cache_write_5m"] + b["cache_write_1h"]
    if pre["responses"]:
        pre["cache_creation_input_tokens"] = pre["cache_write_5m"] + pre["cache_write_1h"]
        buckets.insert(0, dict(pre, slug="(before --since)", chapter=0, until=head,
                               first_ts="", last_ts="", duration_s=0))
    return buckets


def _tally(acc, r):
    acc["responses"] += 1
    acc["input_tokens"] += r.input_tokens
    acc["cache_write_5m"] += r.cache_write_5m
    acc["cache_write_1h"] += r.cache_write_1h
    acc["cache_read_input_tokens"] += r.cache_read
    acc["output_tokens"] += r.output_tokens
    m = acc["by_model"].setdefault(r.model or "(unknown)", {
        "responses": 0, "input_tokens": 0, "cache_write_5m": 0, "cache_write_1h": 0,
        "cache_read_input_tokens": 0, "output_tokens": 0})
    m["responses"] += 1
    m["input_tokens"] += r.input_tokens
    m["cache_write_5m"] += r.cache_write_5m
    m["cache_write_1h"] += r.cache_write_1h
    m["cache_read_input_tokens"] += r.cache_read
    m["output_tokens"] += r.output_tokens
