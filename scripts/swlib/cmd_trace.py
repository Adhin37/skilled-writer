"""`sw trace` - what the run cost, and which skills and cards it actually opened.

The rest of the toolkit reviews the novel. This reviews the run: tokens, dollars, wall clock,
and the finding that motivated the command - `docs/benchmark.md` found that 21 of 37 skills were
never loaded, including four the contract calls non-optional, and had no way to check whether the
fix worked. This is that check, run against the transcripts Claude Code already writes.

It measures and does not score. There is no "good" number of skill loads and no target cost; the
one judgement it makes is that a skill `CLAUDE.md` section 3 lists as always in play, in a run
that opened skills at all, should have been opened.
"""

import os
import re

from . import kb, transcripts
from .rates import Rates, total_cost
from .report import Report


def _skill_roster(repo_root):
    d = kb.skills_dir(repo_root)
    if not os.path.isdir(d):
        return []
    return sorted(name for name in os.listdir(d)
                  if os.path.isfile(os.path.join(d, name, "SKILL.md")))


def _classify(roster, novel, repo_root):
    """Split the roster into (always-in-play, off-for-this-novel).

    Without a novel every module counts as in play: a module cannot be called switched off when
    nothing says which novel's switches to read.
    """
    # Switch-gated, genre-gated and config-gated all answer one question - is this skill live for
    # this novel - and each skill's frontmatter answers it. `content.romance: none` turns
    # lead-interest off as surely as an `optional:` key would, and reporting either as a missed
    # skill is a false positive on correct behaviour.
    off = set()
    if novel is not None:
        off = set(kb.index(repo_root).off_for(novel))
    return [s for s in roster if s not in off], sorted(off & set(roster))


def _short(sess):
    """A transcript name that identifies it: the id, not the left-truncated path to it."""
    name = os.path.basename(sess.path)
    if name.endswith(".jsonl"):
        name = name[:-6]
    if sess.is_subagent:
        parent = os.path.basename(os.path.dirname(os.path.dirname(sess.path)))
        return "%s/%s" % (parent[:8], name)
    return name


def _hms(seconds):
    seconds = int(seconds or 0)
    if seconds < 60:
        return "%ds" % seconds
    if seconds < 3600:
        return "%dm %02ds" % (seconds // 60, seconds % 60)
    return "%dh %02dm" % (seconds // 3600, (seconds % 3600) // 60)


def _per_model(sessions):
    """{model: usage} so cost can be priced per model rather than blended."""
    out = {}
    for sess in sessions:
        for r in sess.responses:
            u = out.setdefault(r.model or "(unknown)", {
                "responses": 0, "input_tokens": 0, "cache_write_5m": 0,
                "cache_write_1h": 0, "cache_read_input_tokens": 0, "output_tokens": 0})
            u["responses"] += 1
            u["input_tokens"] += r.input_tokens
            u["cache_write_5m"] += r.cache_write_5m
            u["cache_write_1h"] += r.cache_write_1h
            u["cache_read_input_tokens"] += r.cache_read
            u["output_tokens"] += r.output_tokens
    return out


def run(repo_root, novel=None, rates=None, transcript_root=None, include_all=False,
        since=None, until=None, session=None, roles=None):
    """Returns (Report, data). `data` is the same content, shaped for --json.

    `roles` keeps only the transcripts whose `Session.role` is in it - a comma-separated string
    or a list. Scope a run with `--session <the coordinator's session id>`: its subagents carry
    the same session id, so that one value takes in the drafter, the gate, the architect and
    the reader, and `--role` then narrows it.
    """
    rates = rates or Rates()
    root = transcript_root or transcripts.default_root()
    rep = Report("trace - %s" % (novel.title if novel is not None else
                                 os.path.basename(os.path.abspath(repo_root))))
    data = {"transcript_root": root, "repo_root": os.path.abspath(repo_root)}

    if not os.path.isdir(root):
        rep.info("transcripts", [
            "   no transcript directory at %s" % root.replace(os.sep, "/"),
            "   nothing to measure - this is not a finding about the novel",
            "   set CLAUDE_CONFIG_DIR, or pass --transcripts <dir>",
        ])
        data["sessions"] = []
        return rep, data

    sessions = transcripts.sessions_for(repo_root, root, include_all=include_all,
                                        since=since, until=until, session=session)
    if roles:
        want = set(r.strip() for r in (roles.split(",") if isinstance(roles, str) else roles)
                   if r.strip())
        sessions = [s for s in sessions if s.role in want]
        data["roles"] = sorted(want)
    if not sessions:
        rep.info("transcripts", [
            "   searched %s" % root.replace(os.sep, "/"),
            "   no session reports a cwd inside %s" % os.path.abspath(repo_root).replace(os.sep, "/"),
            "   nothing to measure - this is not a finding about the novel",
        ])
        data["sessions"] = []
        return rep, data

    agg = transcripts.aggregate(sessions)
    per_model = _per_model(sessions)
    cost = total_cost(rates, per_model)
    data["totals"] = agg
    data["cost_usd"] = round(cost, 4)
    data["per_model"] = per_model

    _run_section(rep, sessions, agg)
    _token_section(rep, agg)
    _cost_section(rep, rates, per_model, cost, agg)
    _role_section(rep, rates, agg, data)
    _chapter_section(rep, sessions, rates, data, since)
    _skill_section(rep, repo_root, novel, agg, data, narrowed=bool(roles))
    _card_section(rep, agg, data)
    _routing_section(rep, repo_root, sessions, data)
    _tool_section(rep, agg)

    data["sessions"] = [{
        "file": s.rel, "kind": "subagent" if s.is_subagent else "session",
        "role": s.role, "spawn_depth": s.spawn_depth, "description": s.description,
        "responses": len(s.responses), "rows": s.rows,
        "duration_s": s.duration_s, "first_ts": s.first_ts, "last_ts": s.last_ts,
        "totals": s.totals(), "naive": s.naive_totals,
        "skills": s.skills, "tools": s.tools,
    } for s in sessions]
    return rep, data


def _run_section(rep, sessions, agg):
    lines = ["   %-38s %-10s %6s %8s %9s  %s"
             % ("transcript", "role", "resp", "rows", "wall", "label")]
    for s in sessions:
        lines.append("   %-38s %-10s %6d %8d %9s  %s"
                     % (_short(s), s.role[:10], len(s.responses), s.rows, _hms(s.duration_s),
                        (s.description or "")[:40]))
    lines.append("   %d session(s), %d API responses from %d transcript rows"
                 % (agg["sessions"], agg["responses"], agg["rows"]))
    worked = sum(s.duration_s for s in sessions)
    lines.append("   %s summed across sessions; %s from first row to last (they overlap, and "
                 "idle time between" % (_hms(worked), _hms(agg["duration_s"])))
    lines.append("   sessions counts in the second figure and not the first)")
    lines.append("   span %s -> %s" % (agg["first_ts"] or "?", agg["last_ts"] or "?"))
    lines.append("   models: %s" % (", ".join("%s x%d" % kv for kv in sorted(agg["models"].items()))
                                    or "none"))
    rep.info("run", lines)


def _token_section(rep, agg):
    naive = agg["naive"]
    rows = [
        ("input", agg["input_tokens"], naive["input_tokens"]),
        ("cache write", agg["cache_creation_input_tokens"], naive["cache_creation_input_tokens"]),
        ("  - 5m ttl", agg["cache_write_5m"], None),
        ("  - 1h ttl", agg["cache_write_1h"], None),
        ("cache read", agg["cache_read_input_tokens"], naive["cache_read_input_tokens"]),
        ("output", agg["output_tokens"], naive["output_tokens"]),
    ]
    lines = ["   %-14s %14s %14s %8s" % ("class", "tokens", "naive row-sum", "inflation")]
    for label, real, naive_v in rows:
        if naive_v is None:
            lines.append("   %-14s %14s" % (label, "{:,}".format(real)))
            continue
        ratio = ("%.2fx" % (naive_v / float(real))) if real else "-"
        lines.append("   %-14s %14s %14s %8s"
                     % (label, "{:,}".format(real), "{:,}".format(naive_v), ratio))
    lines.append("   Claude Code writes one row per content block and repeats `usage` on each,")
    lines.append("   so the naive column is what summing rows would have reported. It is shown")
    lines.append("   because benchmark run #1 was counted that way.")
    rep.info("tokens (one entry per API response)", lines)

    if agg["responses"] and agg["rows"]:
        inflate = naive["cache_read_input_tokens"] / float(agg["cache_read_input_tokens"] or 1)
        if inflate > 1.05:
            rep.note("accounting", "summing transcript rows would overstate cache reads by "
                                   "%.2fx here - %d rows carry %d responses"
                     % (inflate, agg["rows"], agg["responses"]))


def _cost_section(rep, rates, per_model, cost, agg):
    lines = []
    for model in sorted(per_model):
        u = per_model[model]
        lines.append("   %-20s %6d resp  $%8.2f"
                     % (model[:20], u["responses"], rates.cost(
                         model, input_tokens=u["input_tokens"],
                         cache_write_5m=u["cache_write_5m"],
                         cache_write_1h=u["cache_write_1h"],
                         cache_read=u["cache_read_input_tokens"],
                         output_tokens=u["output_tokens"])))
    lines.append("   %-20s %6s   $%8.2f total" % ("", "", cost))
    lines.append("")
    lines.extend(rates.describe(per_model.keys()))
    rep.info("cost (computed from tokens - the transcripts carry no cost field)", lines)
    for model in sorted(rates.unpriced):
        rep.warn("rates", "no published rate for model `%s` - it contributes $0.00 above; "
                          "add it with --rates" % model)


def _role_section(rep, rates, agg, data):
    """Who spent what. A multi-agent run pooled into one total cannot say whether Phase C
    happened, let alone what it cost - and until 2026-09-24 that is all `trace` could print."""
    roles = agg.get("by_role") or {}
    data["by_role"] = {}
    if not roles:
        return
    lines = ["   %-12s %4s %6s %9s %9s %7s" % ("role", "sess", "resp", "wall", "cost", "cards")]
    for name in sorted(roles, key=lambda n: (n == "main", n)):
        r = roles[name]
        cost = total_cost(rates, r["by_model"])
        data["by_role"][name] = {"sessions": r["sessions"], "responses": r["responses"],
                                 "duration_s": r["duration_s"], "cost_usd": round(cost, 4),
                                 "draft_cards": r["draft_cards"],
                                 "audit_cards": r["audit_cards"]}
        lines.append("   %-12s %4d %6d %9s %9s %7s"
                     % (name[:12], r["sessions"], r["responses"], _hms(r["duration_s"]),
                        "$%.2f" % cost, "%d/%d" % (r["draft_cards"], r["audit_cards"])))
    lines.append("   `main` is a top-level session - the coordinator in a run, or a maintainer.")
    lines.append("   A role's wall time is summed across its agents, which may have overlapped.")
    rep.info("by role", lines)


def _chapter_section(rep, sessions, rates, data, since=None):
    buckets = transcripts.by_chapter(sessions, since=since)
    data["by_chapter"] = buckets
    if not buckets:
        return
    lines = ["   %-20s %4s %6s %9s %13s %10s %9s %7s  %s"
             % ("novel", "ch", "resp", "wall", "cache read", "output", "cost", "cards",
                "last write")]
    quick = []
    split = []
    for b in buckets:
        b["cost_usd"] = round(total_cost(rates, b["by_model"]), 4)
        pre = b["chapter"] <= 0
        lines.append("   %-20s %4s %6d %9s %13s %10s %9s %7s  %s"
                     % (b["slug"][:20], "-" if pre else b["chapter"], b["responses"],
                        _hms(b["duration_s"]),
                        "{:,}".format(b["cache_read_input_tokens"]),
                        "{:,}".format(b["output_tokens"]),
                        "$%.2f" % b["cost_usd"],
                        "%d/%d" % (b["draft_cards"], b["audit_cards"]),
                        (b["until"] or "-")[:19]))
        roles = b.get("by_role") or {}
        if not pre and b["responses"] and b["duration_s"] < 30:
            quick.append(b["chapter"])
        if len(roles) > 1 or (roles and "main" not in roles):
            parts = []
            for name in sorted(roles, key=lambda n: (n == "main", n)):
                r = roles[name]
                parts.append("%s %dr $%.2f %d/%d"
                             % (name, r["responses"], total_cost(rates, r["by_model"]),
                                r["draft_cards"], r["audit_cards"]))
            split.append("   %4s  %s" % ("-" if pre else b["chapter"], " | ".join(parts)))
    if split:
        lines.append("   by role (responses, cost, draft/audit cards):")
        lines.extend(split)
    lines.append("   `cards` is draft/audit opened in that bucket.")
    lines.append("   A subagent whose spawn label names one chapter (\"draft ch 6\", \"gate ch 6\")")
    lines.append("   is billed to that chapter whole. Everything else is attributed by the LAST")
    lines.append("   write of each chapter file: a revision rewrites it, and anchoring on the")
    lines.append("   first would push revision cost into the next bucket - so under that rule the")
    lines.append("   first chapter's row absorbs the setup before it, and a Phase A card opened")
    lines.append("   for the next chapter before this one's file is finished lands here.")
    lines.append("   Rows are in order of last write, which is not chapter order when a later")
    lines.append("   session revised an earlier chapter. `(after the last write)` is work no")
    lines.append("   chapter file follows - kept, so the rows sum to the totals.")
    if buckets and buckets[0]["chapter"] == 0:
        lines.append("   `(before --since)` is everything the window excludes, kept visible "
                     "rather than folded into chapter 1.")
    elif not since and len(sessions) > 1:
        lines.append("   No --since: every session ever run in this repo is in these numbers, "
                     "and the first chapter's bucket absorbs all of them.")
    rep.info("per chapter", lines)
    if quick and not any(s.chapter_hint is not None for s in sessions):
        rep.warn("trace-attribution",
                 "chapter(s) %s hold under 30 seconds of work - attribution anchors on each "
                 "file's LAST write, so an end-of-run cleanup sweep across several chapters "
                 "moves their real cost into whichever chapter was touched before it"
                 % ", ".join(str(c) for c in quick),
                 detail="benchmark run #2, F5: five chapters resolved to $11.76/$6.30/$1.28/"
                        "$0.23/$0.11 this way. Only the run total was trustworthy.")


def _skill_section(rep, repo_root, novel, agg, data, narrowed=False):
    roster = _skill_roster(repo_root)
    if not roster:
        rep.warn("skills", "no .claude/skills/ under %s - cannot tell which skills loaded"
                 % os.path.abspath(repo_root).replace(os.sep, "/"))
        return
    opened = agg["skills"]
    in_play, off = _classify(roster, novel, repo_root)
    # Two kinds of skill are never opened by a correct role run, and reporting them as missed
    # teaches the reader of this section to stop reading it. A body an agent file preloads
    # through `skills:` arrives as metadata, not a tool call - `write-chapter` in the drafter,
    # `revision-pass` in the gate - so the scanner never sees it opened. And a skill with no
    # file in the role trees has nothing a drafter or gate may open at all: `role_scope` refuses
    # every other body, so its advice reaches the run only through the cards that cite it.
    preloaded = _preloaded(repo_root)
    carded = _carded(repo_root)
    quiet = set(s for s in in_play if s in preloaded or s not in carded)
    never = [s for s in in_play if s not in opened and s not in quiet]
    data["skills"] = {"roster": roster, "opened": opened, "in_play": in_play,
                      "off_for_this_novel": off, "in_play_never_opened": never,
                      "preloaded": sorted(preloaded & set(roster)),
                      "no_role_file": sorted(set(roster) - carded)}

    known = set(roster)
    mine = dict((k, v) for k, v in opened.items() if k in known)
    foreign = dict((k, v) for k, v in opened.items() if k not in known)
    data["skills"]["opened_here"] = mine
    data["skills"]["opened_elsewhere"] = foreign

    lines = ["   %d of %d of this repo's skills opened" % (len(mine), len(roster))]
    if mine:
        hits = sorted(mine.items(), key=lambda kv: (-kv[1], kv[0]))
        lines.append("   opened: " + "  ".join("%s x%d" % (k, v) for k, v in hits))
    if foreign:
        # Bundled skills and slash commands come through the same `Skill` tool. They are not
        # this repo's and must not inflate the denominator.
        hits = sorted(foreign.items(), key=lambda kv: (-kv[1], kv[0]))
        lines.append("   not this repo's skills: "
                     + "  ".join("%s x%d" % (k, v) for k, v in hits))
    if off:
        lines.append("   off for this novel: " + "  ".join(off))
    if never:
        lines.append("   in play, never opened: " + "  ".join(never))
    unseen = sorted(q for q in quiet if q not in opened)
    if unseen:
        lines.append("   not counted as missed (preloaded by an agent, or no role file to "
                     "open): " + "  ".join(unseen))
    rep.info("skills", lines)

    # Only a run that opened skills at all is evidence about which ones it skipped. A trace over
    # sessions that never wrote a chapter would otherwise report every skill as missing. Nor is
    # a trace narrowed by `--role`: a gate never opens a design skill, correctly.
    if mine and never and not narrowed:
        rep.warn("skills", "%d skill(s) CLAUDE.md section 3 lists as always in play were never "
                           "opened in this run: %s" % (len(never), ", ".join(never[:8])),
                 detail="benchmark finding 9. A skill whose file never enters context contributes "
                        "only whatever another skill paraphrases of it.")


def _card_section(rep, agg, data):
    """Cards opened, which `trace` could not report until 2026-09-19.

    A skill file says the drafter reached for the advice; a card says it reached for the
    decision. Benchmark runs #4 and #5 both made the card count their headline and both had to
    assemble it by hand out of the agent transcript, which is the kind of measurement that gets
    done once and then estimated. It scores nothing: there is no correct number of cards, and the
    card budgets in `rules.py` bind the corpus rather than any run.
    """
    cards = agg["cards"]
    total = cards["draft"] + cards["audit"]
    data["cards"] = {"draft": cards["draft"], "audit": cards["audit"],
                     "by_card": agg["card_files"]}
    if not total:
        return
    lines = ["   %d card open(s): %d draft, %d audit"
             % (total, cards["draft"], cards["audit"])]
    hits = sorted(agg["card_files"].items(), key=lambda kv: (-kv[1], kv[0]))
    row = []
    for k, v in hits:
        row.append("%s x%d" % (k, v))
        if len(row) == 3:
            lines.append("   " + "  ".join(row))
            row = []
    if row:
        lines.append("   " + "  ".join(row))
    lines.append("   Counted, never scored. Phase A spends draft cards and Phase C audit cards,")
    lines.append("   so a run with one and not the other is a phase that did not happen.")
    rep.info("cards", lines)


def _preloaded(repo_root):
    """Skills an agent file preloads through `skills:` - they arrive without a tool call."""
    out = set()
    agents = os.path.join(repo_root, ".claude", "agents")
    if not os.path.isdir(agents):
        return out
    for name in sorted(os.listdir(agents)):
        if not name.endswith(".md"):
            continue
        try:
            with open(os.path.join(agents, name), encoding="utf-8") as fh:
                text = fh.read()
        except (IOError, OSError):
            continue
        m = re.match(r"---\n(.*?)\n---", text, re.S)
        if not m:
            continue
        block = re.search(r"^skills:\s*\n((?:\s+-\s*\S+\s*\n)+)", m.group(1) + "\n", re.M)
        if block:
            out.update(re.findall(r"-\s*(\S+)", block.group(1)))
    return out


def _carded(repo_root):
    """Skills that own at least one file in the role trees - something a role can open."""
    try:
        idx = kb.index(repo_root)
    except Exception:                                  # measurement must not fail on the corpus
        return set()
    return set(f.owner for f in idx.files if f.type != "skill")


# Which roles `role_scope.py` judges. The reader is guarded by its own hook, and the architect's
# denials are narrow; both are judged here too, because the guard's own `verdict` is what does it.
ROUTED = ("drafter", "gate", "architect", "reader")


def _routing_section(rep, repo_root, sessions, data):
    """What each agent opened that its read guard would refuse - by `Read`, and by `Bash`.

    The guard is a `PreToolUse` hook on `Read`, and a harness in auto mode tells every agent to
    prefer `cat` - so the one road the guard cannot see is the one agents are told to take
    (`CLAUDE.md` section 10). This is the after-the-fact view of that road, judged by the guard's
    own `verdict` so the two cannot disagree. A denied `Read` was refused as it happened and
    means a card sent the agent somewhere it should not go; a denied path in a shell command
    was opened, unguarded, and is the worse of the two.
    """
    guard = _load_guard(repo_root)
    data["routing"] = []
    if guard is None:
        return
    refused, unguarded = {}, {}
    for s in sessions:
        if not s.is_subagent or s.agent_type not in ROUTED:
            continue
        payload = {"agent_id": s.agent_id or "trace", "agent_type": s.agent_type}
        for _stamp, tool, path in s.opened:
            if guard.verdict(payload, path) is None:
                continue
            bucket = unguarded if tool == "Bash" else refused
            key = (s.agent_type, _rel(path, repo_root))
            bucket[key] = bucket.get(key, 0) + 1
            data["routing"].append({"role": s.agent_type, "tool": tool,
                                    "path": _rel(path, repo_root)})
    if unguarded or refused:
        rep.info("routing", [
            "   Judged against TODAY's read guard. A transcript from before the corpus moved",
            "   (roles/ replaced .claude/skills/*/references/ on 2026-09-20) reads as misrouted",
            "   for paths that were the right ones at the time."])
    for what, bucket, level in (("opened through Bash, where the guard cannot see",
                                 unguarded, rep.warn),
                                ("refused by the read guard - a card sent it there",
                                 refused, rep.note)):
        if not bucket:
            continue
        roles = sorted(set(r for r, _p in bucket))
        for role in roles:
            paths = sorted((p, n) for (r, p), n in bucket.items() if r == role)
            level("trace-routing", "%s: %d path(s) %s: %s"
                  % (role, len(paths), what,
                     ", ".join("%s%s" % (p, " x%d" % n if n > 1 else "") for p, n in paths[:6])
                     + (" ..." if len(paths) > 6 else "")))


def _load_guard(repo_root):
    path = os.path.join(repo_root, "scripts", "hooks", "role_scope.py")
    if not os.path.isfile(path):
        return None
    import importlib.util
    spec = importlib.util.spec_from_file_location("_sw_trace_role_scope", path)
    mod = importlib.util.module_from_spec(spec)
    try:
        spec.loader.exec_module(mod)
    except Exception:
        return None
    return mod


def _rel(path, repo_root):
    """A repo-relative spelling of a path the transcript recorded, when it is under the repo."""
    unix = path.replace(os.sep, "/")
    root = os.path.abspath(repo_root).replace(os.sep, "/").rstrip("/") + "/"
    return unix[len(root):] if unix.startswith(root) else unix


def _tool_section(rep, agg):
    tools = agg["tools"]
    if not tools:
        return
    rep.info("tools", ["   " + "  ".join("%s x%d" % kv for kv in
                                         sorted(tools.items(), key=lambda kv: (-kv[1], kv[0])))])
