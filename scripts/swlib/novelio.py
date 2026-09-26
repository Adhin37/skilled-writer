"""The novel workspace: config, ledger, plan, cast tables, lexicon.

One object so the commands never re-parse or re-guess paths. Everything is lazy: a command
that only wants threads never reads the bible.
"""

import os
import re

from . import mdio
from .textstats import Channels, Chapter, load_chapters

# A chapter is finished once phase C has passed it AND step 5 has written its state - which is
# when the drafter stamps `revised`. `published` counts because a chapter cannot reach it without
# having been revised first. `gated` - the gate's own mark, set as its last act on a pass - is
# deliberately NOT here: a chapter the gate passed whose state was never written is unfinished.
GATED_STATUS = ("revised", "published")

# A walk-on's roster line in `bible/cast/_extras.md`:
# `<Name> — <what> — ch <appearances> — <status>`.
ROSTER_LINE = re.compile(r"^([^—\n|#<]{2,60}?)\s+—.*?—\s*ch\s+([0-9,\s~–\-()a-z]+?)\s*—")

# The Phase A brief in `state/brief.md`: a fenced block whose first line names the chapter.
BRIEF_FENCE = re.compile(r"^```[^\n]*\n(.*?)^```", re.M | re.S)
BRIEF_HEAD = re.compile(r"^(?:Ch|Chapter)\.?\s+(\d+)", re.M)


class CCSBlock(object):
    """One `=CNNNN=` chapter block from state/continuity.md."""

    def __init__(self, number, header, lines, line_no):
        self.number = number
        self.header = header
        self.lines = lines          # body lines after the header, blanks dropped
        self.line_no = line_no      # 1-based line of the header in continuity.md

    @property
    def text(self):
        return "\n".join([self.header] + self.lines)

    @property
    def line_count(self):
        return 1 + len(self.lines)

    def keys(self):
        # `[a-z][a-z0-9]*`, not `[a-z]+`: `z4>` names the gate pass it records, and under the
        # old pattern it parsed as nothing at all - the line was written, stored, and invisible
        # to every reader. Digits are allowed after the first letter for that reason only.
        out = {}
        for line in self.lines:
            m = re.match(r"^([a-z][a-z0-9]*)>\s*(.*)$", line)
            if m:
                out.setdefault(m.group(1), []).append(m.group(2))
        return out

    def has(self, key):
        return key in self.keys()

    def get(self, key, default=""):
        vals = self.keys().get(key)
        return vals[0] if vals else default

    def header_field(self, name):
        m = re.search(r"\b%s:\s*([^|]+)" % re.escape(name), self.header)
        return m.group(1).strip() if m else ""

    @property
    def wc(self):
        v = self.header_field("wc")
        return int(v) if v.isdigit() else None

    @property
    def arc(self):
        v = self.header_field("arc")
        return int(v) if v.isdigit() else None

    @property
    def pov(self):
        return self.header_field("pov")


def _memo(fn):
    """Cache a no-argument accessor on the instance.

    The text was already cached; the *parse* was not, so every caller rebuilt every Row. One
    `readset` re-parsed the plan table five times and the thread table three, and `sw state`
    re-parsed the plan table once per chapter — the only genuinely quadratic path in the
    toolkit.
    """
    key = "memo:" + fn.__name__

    def wrapper(self):
        if key not in self._cache:
            self._cache[key] = fn(self)
        return self._cache[key]

    wrapper.__name__ = fn.__name__
    wrapper.__doc__ = fn.__doc__
    return wrapper


class Novel(object):
    def __init__(self, root):
        self.root = os.path.normpath(root)
        self.slug = os.path.basename(self.root)
        self._cache = {}

    # ------------------------------------------------------------------ paths

    def path(self, *parts):
        return os.path.join(self.root, *parts)

    def exists(self):
        return os.path.isfile(self.path("novel.md"))

    def _text(self, *parts):
        key = parts
        if key not in self._cache:
            self._cache[key] = mdio.read_text(self.path(*parts))
        return self._cache[key]

    # ----------------------------------------------------------------- config

    @property
    def cfg(self):
        if "cfg" not in self._cache:
            fm, _ = mdio.split_frontmatter(self._text("novel.md"))
            self._cache["cfg"] = mdio.parse_yaml(fm)
        return self._cache["cfg"]

    def get(self, dotted, default=None):
        return mdio.dig(self.cfg, dotted, default)

    @property
    def title(self):
        return self.get("title") or self.slug

    @property
    def blurb(self):
        """The platform blurb, from the body of novel.md rather than a frontmatter field.

        It is multi-line prose and belongs where a human edits it; duplicating it into the
        frontmatter would give the book two blurbs that drift apart.
        """
        body = mdio.split_frontmatter(self._text("novel.md"))[1]
        sec = mdio.section(body, "Hook")
        return "\n".join(l for l in sec.split("\n")[1:]
                         if l.strip() and not l.strip().startswith("<!--")).strip()

    @property
    def has_foreknowledge(self):
        return bool(self.get("mc.foreknowledge"))

    @property
    def form_locked(self):
        return bool(self.get("mc.form_locked"))

    @property
    def scaling_shape(self):
        """climb | inverted | regression | plateau-late | none. Default climb."""
        s = str(self.get("scaling.shape", "climb") or "climb").strip().lower()
        return s if s in ("climb", "inverted", "regression", "plateau-late", "none") else "climb"

    @property
    def has_scaling(self):
        return self.scaling_shape != "none"

    @property
    def means_shape(self):
        """fades | flat | inverts | none. Default fades - the shape the genre actually has.

        Absent means fades rather than none, so a novel scaffolded before `means:` existed still
        gets its prices in the read-set. Turning it off is a decision somebody writes down.
        """
        s = str(self.get("means.shape", "fades") or "fades").strip().lower()
        return s if s in ("fades", "flat", "inverts", "none") else "fades"

    @property
    def has_means(self):
        return self.means_shape != "none"

    def scaling_int(self, key, default):
        n = self.get("scaling.%s" % key, default)
        return n if isinstance(n, int) else default

    @property
    def arc_length(self):
        n = self.get("chapters.arc_length", 25)
        return n if isinstance(n, int) and n > 0 else 25

    @property
    def opening_last_ch(self):
        """Last chapter story-opening owns: opening.contract_by_ch + 2."""
        n = self.get("opening.contract_by_ch", 3)
        return (n if isinstance(n, int) else 3) + 2

    def optional_on(self, name):
        return str(self.get("optional.%s" % name, "off")).lower() in ("on", "true")

    # --------------------------------------------------------------- chapters

    @property
    def channels(self):
        """The four marks this novel declares. `channels:` in novel.md, not a literal here."""
        if "channels" not in self._cache:
            self._cache["channels"] = Channels.from_novel(self)
        return self._cache["channels"]

    def chapters(self):
        if "chapters" not in self._cache:
            self._cache["chapters"] = load_chapters(self.path("chapters"),
                                                    channels=self.channels)
        return self._cache["chapters"]

    def chapter(self, number):
        if "chapter_index" not in self._cache:
            self._cache["chapter_index"] = {c.number: c for c in reversed(self.chapters())}
        return self._cache["chapter_index"].get(number)

    def ungated_chapters(self, below=None):
        """Chapters the write-chapter phase C gate never passed, newest first.

        Reads `status:` out of frontmatter and reports what it says: a chapter at `drafted` is
        one the gate has not run on, which is a fact about the file rather than an opinion
        about the prose. `below` bounds it to chapters before that number.
        """
        out = [c for c in self.chapters()
               if c.number is not None and (below is None or c.number < below)
               and str(c.meta.get("status", "")).strip().lower() not in GATED_STATUS]
        return sorted(out, key=lambda c: c.number, reverse=True)

    # ----------------------------------------------------------------- ledger

    def brief(self):
        """The Phase A brief on file, as `(chapter number, text)`, or `(None, "")`.

        The brief is the only thing the loop decides that lived solely in the conversation, so a
        compaction or a dead session took it outright - run #5's chapter 4 shipped with
        `cand> unrecorded` for exactly that reason. `write-chapter` writes it here on approval and
        the read-set hands it back, which makes a resume cost the draft rather than the decisions.

        It is a scratch file: the number is read from the brief's own first line and nothing here
        checks, scores or repairs it. A brief for another chapter is simply not this chapter's.
        """
        text = self._text("state", "brief.md")
        if not text:
            return None, ""
        body = None
        for block in BRIEF_FENCE.findall(text):
            if BRIEF_HEAD.search(block):
                body = block
                break
        if body is None:
            return None, ""
        m = BRIEF_HEAD.search(body)
        return int(m.group(1)), body.strip("\n")

    def handback(self):
        """The gate's hand-back on file, as `(chapter number, text)`, or `(None, "")`.

        The one hand-off in the loop that used to leave no file. Benchmark run #6's chapter 5
        drafter died mid-state-write; its successor rebuilt the block from the ledger and lost the
        gate's `For design:` item, because the hand-back had only ever lived in two conversations.
        The gate now writes it to `state/gate.md` in the brief's shape - a fenced block opening on
        `Ch <n> — gate hand-back` - and step 5 copies `z4>` and `For design:` from the file.
        """
        text = self._text("state", "gate.md")
        if not text:
            return None, ""
        for block in BRIEF_FENCE.findall(text):
            m = BRIEF_HEAD.search(block)
            if m:
                return int(m.group(1)), block.strip("\n")
        return None, ""

    def brief_status(self):
        """`proposed` or `approved` - where the brief on file is in the Phase A stop.

        The drafter writes the brief when it stops for approval, not after: a brief that exists
        only in the conversation while the user reads it is exactly what a dead session takes. So
        the file has to say whether it has been approved yet, or a resume would draft from a
        brief nobody agreed to. A file with no `status:` line predates the line and was written
        on approval, so it reads as approved.
        """
        m = re.search(r"^status:\s*(proposed|approved)\b", self._text("state", "brief.md"),
                      re.M | re.I)
        return m.group(1).lower() if m else "approved"

    def brief_unreadable(self):
        """True when `state/brief.md` holds a brief `brief()` cannot find.

        The same species as the `TH01` thread ids: a format drift that makes a check go quiet,
        which reads exactly like a check that passed. An unfenced brief, or a fence that does not
        open on `Ch <n>`, used to be indistinguishable from no brief at all - and a resume then
        re-ran Phase A and step 5 had no `cand` line to copy.
        """
        text = self._text("state", "brief.md")
        if not text.strip() or self.brief()[0] is not None:
            return False
        blocks = [b.strip() for b in BRIEF_FENCE.findall(text)]
        if any(b and not b.startswith("(no brief on file") for b in blocks):
            return True
        return bool(BRIEF_HEAD.search(BRIEF_FENCE.sub("", text)))

    @property
    def ledger_text(self):
        return self._text("state", "continuity.md")

    def blocks(self):
        """Every CCS chapter block, in file order."""
        if "blocks" in self._cache:
            return self._cache["blocks"]
        out, cur = [], None
        for i, line in enumerate(self.ledger_text.split("\n"), 1):
            m = re.match(r"^=C(\d+)=(.*)$", line)
            if m:
                cur = CCSBlock(int(m.group(1)), line, [], i)
                out.append(cur)
                continue
            if re.match(r"^=(?:ARC|BOOK)", line):
                cur = None
                continue
            if cur is not None:
                if line.strip() in ("", "```"):
                    if line.strip() == "```":
                        cur = None
                    continue
                if line.startswith("#"):
                    cur = None
                    continue
                cur.lines.append(line.rstrip())
        self._cache["blocks"] = out
        return out

    def block(self, number):
        if "block_index" not in self._cache:
            self._cache["block_index"] = {b.number: b for b in reversed(self.blocks())}
        return self._cache["block_index"].get(number)

    def book_digest(self):
        sec = mdio.section(self.ledger_text, "BOOK DIGEST")
        m = re.search(r"```\n(.*?)```", sec, re.S)
        if m:
            return m.group(1).rstrip()
        return "\n".join(l for l in sec.split("\n")[1:] if l.strip()).rstrip()

    def arc_digests(self):
        """{arc_number: text} from the ARC DIGESTS section."""
        sec = mdio.section(self.ledger_text, "ARC DIGEST")
        out, cur, num = {}, [], None
        for line in sec.split("\n"):
            m = re.match(r"^=ARC(\d+)=", line)
            if m:
                if num is not None:
                    out[num] = "\n".join(cur).rstrip()
                num, cur = int(m.group(1)), [line]
                continue
            if num is not None:
                if line.strip().startswith("=") or line.startswith("#"):
                    out[num] = "\n".join(cur).rstrip()
                    num, cur = None, []
                    continue
                if line.strip() and line.strip() != "```":
                    cur.append(line.rstrip())
        if num is not None:
            out[num] = "\n".join(cur).rstrip()
        return out

    # ------------------------------------------------------------ state tables

    @staticmethod
    def _table_by_headers(text, *required):
        """Pick a table by the columns it has, not by the prose heading above it.

        Heading text gets edited; column names are load-bearing and do not.
        """
        want = [mdio._norm_header(r) for r in required]
        for table in mdio.parse_tables(text):
            heads = [mdio._norm_header(h) for h in table.headers]
            if all(any(w == h for h in heads) for w in want):
                return table
        return None

    @_memo
    def threads(self):
        t = self._table_by_headers(self._text("state", "threads.md"), "id", "thread", "status")
        return t.rows if t else []

    @_memo
    def growth_rows(self):
        t = self._table_by_headers(self._text("state", "growth.md"), "character", "rung")
        return t.rows if t else []

    @_memo
    def skill_rows(self):
        t = self._table_by_headers(self._text("state", "growth.md"), "character", "skill", "stage")
        return t.rows if t else []

    @_memo
    def standing_rows(self):
        t = self._table_by_headers(self._text("state", "power.md"), "character", "tier", "the edge")
        return t.rows if t else []

    @_memo
    def ladder_rows(self):
        t = self._table_by_headers(self._text("state", "power.md"), "tier", "how many alive")
        return t.rows if t else []

    @_memo
    def pressure_rows(self):
        t = self._table_by_headers(self._text("state", "power.md"), "ch", "opposition", "p")
        return t.rows if t else []

    @_memo
    def gain_rows(self):
        t = self._table_by_headers(self._text("state", "power.md"), "ch", "source", "new problem")
        return t.rows if t else []

    @_memo
    def boost_rows(self):
        t = self._table_by_headers(self._text("state", "power.md"), "ch", "boost", "the debt")
        return t.rows if t else []

    @_memo
    def curve_plan_rows(self):
        t = self._table_by_headers(self._text("state", "power.md"), "arc", "pressure band")
        return t.rows if t else []

    @_memo
    def divergence_rows(self):
        t = self._table_by_headers(
            self._text("state", "timeline.md"), "ch", "mc action", "effect")
        return t.rows if t else []

    @_memo
    def plan_rows(self):
        t = self._table_by_headers(self._text("plan", "chapters.md"), "#", "title", "delivers")
        return t.rows if t else []

    @_memo
    def _plan_index(self):
        out = {}
        for r in self.plan_rows():
            digits = re.sub(r"\D", "", r.first())
            if digits:
                out.setdefault(int(digits), r)
        return out

    def plan_row(self, number):
        return self._plan_index().get(number)

    def roster(self):
        """The tier-C walk-on roster in `bible/cast/_extras.md`, as a list of dicts.

        Each entry: `name`, `appearances` (chapter numbers, the first number of each comma part),
        `line` (the file line number), `text` (the entry line plus its indented strokes line).
        Lines inside an HTML comment are the template's example and are skipped.

        One parser for two readers: `sw state`'s promotion check, and `sw readset`, which since
        2026-09-26 hands the drafter the roster line of every walk-on its chapter names. Before
        that the line reached nobody - run #6 had three designed walk-ons written from scratch on
        the page, and each design was then overwritten to match what the page invented.
        """
        text = self._text("bible", "cast", "_extras.md")
        if not text:
            return []
        lines = text.split("\n")
        out = []
        in_comment = False
        for i, line in enumerate(lines):
            if "<!--" in line and "-->" not in line.split("<!--", 1)[1]:
                in_comment = True
                continue
            if in_comment:
                if "-->" in line:
                    in_comment = False
                continue
            m = ROSTER_LINE.match(line)
            if not m:
                continue
            appearances = []
            for part in m.group(2).split(","):
                nums = re.findall(r"\d+", part)
                if nums:
                    appearances.append(int(nums[0]))
            entry = [line.rstrip()]
            if i + 1 < len(lines) and re.match(r"^\s+\S", lines[i + 1]):
                entry.append(lines[i + 1].rstrip())
            out.append({"name": m.group(1).strip(), "appearances": appearances,
                        "line": i + 1, "text": "\n".join(entry)})
        return out

    @_memo
    def voice_rows(self):
        t = self._table_by_headers(
            self._text("bible", "cast", "_voices.md"), "character", "intel", "artic", "wit")
        return t.rows if t else []

    @_memo
    def competence_rows(self):
        t = self._table_by_headers(
            self._text("bible", "cast", "_competence.md"), "character", "domain", "level")
        return t.rows if t else []

    @_memo
    def referral_rows(self):
        text = self._text("bible", "cast", "_competence.md")
        for table in mdio.parse_tables(text):
            heads = [mdio._norm_header(h) for h in table.headers]
            if heads and heads[0] == "character" and any("goto" in h or "outside" in h for h in heads):
                return table.rows
        return []

    @_memo
    def extras_rows(self):
        rows = []
        for t in mdio.parse_tables(self._text("bible", "cast", "_extras.md")):
            rows.extend(t.rows)
        return rows

    @_memo
    def fingerprints(self):
        """`{character name: {field: value}}` from each cast file's §Speech fingerprint table.

        Keyed by the `name:` the character's own file declares, so it joins to `_voices.md` by the
        same string `voice_rows` returns. Eight fields are declared per character and nothing read
        one until benchmark run #5, where a character whose file says `contractions: never` spoke
        ten of them in a single chapter: `sw lint` pools every speaker into one chapter-wide rate
        and only ever flags the low side, so the only thing that noticed was the drafter's own
        Pass 10. A declared field that no tool reads is a field that drifts.
        """
        out = {}
        for name in self.cast_files():
            text = self._text("bible", "cast", name + ".md")
            if not text:
                continue
            fm, _ = mdio.split_frontmatter(text)
            who = str((mdio.parse_yaml(fm) or {}).get("name", "")).strip()
            table = self._table_by_headers(text, "field", "value")
            if not who or not table:
                continue
            fields = {}
            for row in table.rows:
                if len(row.cells) >= 2 and row.cells[0].strip():
                    fields[row.cells[0].strip().lower()] = row.cells[1].strip()
            if fields:
                out[who] = fields
        return out

    @_memo
    def cast_frontmatter(self):
        """`{character name: frontmatter dict}` for every cast profile.

        `first_appears:` has been in both cast templates since the scaffold was written and was
        read by nothing at all, which is how it came to be wrong in two of run #5's seven files.
        It is also exactly the field a tool needs to check CLAUDE.md rule 8's clause that every
        named character is placed before they carry a scene.
        """
        out = {}
        for name in self.cast_files():
            text = self._text("bible", "cast", name + ".md")
            if not text:
                continue
            fm, _ = mdio.split_frontmatter(text)
            data = mdio.parse_yaml(fm) or {}
            who = str(data.get("name", "")).strip()
            if who:
                out[who] = data
        return out

    def cast_files(self):
        d = self.path("bible", "cast")
        if not os.path.isdir(d):
            return {}
        out = {}
        for name in sorted(os.listdir(d)):
            if name.endswith(".md") and not name.startswith("_"):
                out[name[:-3]] = os.path.join(d, name)
        return out

    # --------------------------------------------------------------- lexicon

    @_memo
    def anchor_terms(self):
        """Terms flagged `anchor? = yes` in bible/lexicon.md, aliases split out.

        Each entry is (display, regex). A term written with a capital letter is matched
        case-sensitively on that capital, so `the Leaf` cannot be satisfied by `a leaf fell`
        - which is what the shell version counted.
        """
        out = []
        for table in mdio.parse_tables(self._text("bible", "lexicon.md")):
            if not any(mdio._norm_header(h) == "anchor" for h in table.headers):
                continue
            for row in table.rows:
                if "yes" not in row.get("anchor?").lower():
                    continue
                term = re.sub(r"\(.*?\)", "", row.first()).strip()
                for alias in term.split("/"):
                    alias = alias.strip().strip("*").strip()
                    if not alias or alias.lower() == "term":
                        continue
                    bare = re.sub(r"^(?:the|a|an)\s+", "", alias, flags=re.I).strip()
                    if not bare:
                        continue
                    flags = 0 if bare[0].isupper() else re.I
                    rx = re.compile(r"\b%s\b" % re.escape(bare), flags)
                    out.append((alias, rx))
        return out

    @_memo
    def lexicon_names(self):
        out = []
        for table in mdio.parse_tables(self._text("bible", "lexicon.md")):
            if mdio._norm_header(table.headers[0]) in ("canonical", "term"):
                for row in table.rows:
                    name = re.sub(r"\(.*?\)", "", row.first()).strip().strip("*")
                    for part in name.split("/"):
                        part = part.strip()
                        if part:
                            out.append(part)
        return out

    # ----------------------------------------------------------------- world

    @_memo
    def location_rows(self):
        rows = []
        for t in mdio.parse_tables(self._text("bible", "world.md")):
            heads = [mdio._norm_header(h) for h in t.headers]
            if "location" in heads or "place" in heads:
                rows.extend(t.rows)
        return rows


def resolve(arg, repo_root="."):
    """Resolve a novel from a path, a slug, or (when unambiguous) the only one present."""
    candidates = []
    if arg:
        for p in (arg, os.path.join(repo_root, arg), os.path.join(repo_root, "novels", arg)):
            if os.path.isfile(os.path.join(p, "novel.md")):
                return Novel(p)
        return None
    nd = os.path.join(repo_root, "novels")
    if os.path.isdir(nd):
        for name in sorted(os.listdir(nd)):
            if name.startswith("_") or name == "README.md":
                continue
            if os.path.isfile(os.path.join(nd, name, "novel.md")):
                candidates.append(Novel(os.path.join(nd, name)))
    return candidates[0] if len(candidates) == 1 else None
