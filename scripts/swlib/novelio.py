"""The novel workspace: config, ledger, plan, cast tables, lexicon.

One object so the commands never re-parse or re-guess paths. Everything is lazy: a command
that only wants threads never reads the bible.
"""

import os
import re

from . import mdio
from .textstats import Channels, Chapter, load_chapters


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
        out = {}
        for line in self.lines:
            m = re.match(r"^([a-z]+)>\s*(.*)$", line)
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
    def has_foreknowledge(self):
        return bool(self.get("mc.foreknowledge"))

    @property
    def form_locked(self):
        return bool(self.get("mc.form_locked"))

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
        for c in self.chapters():
            if c.number == number:
                return c
        return None

    # ----------------------------------------------------------------- ledger

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
        for b in self.blocks():
            if b.number == number:
                return b
        return None

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

    def threads(self):
        t = self._table_by_headers(self._text("state", "threads.md"), "id", "thread", "status")
        return t.rows if t else []

    def growth_rows(self):
        t = self._table_by_headers(self._text("state", "growth.md"), "character", "rung")
        return t.rows if t else []

    def skill_rows(self):
        t = self._table_by_headers(self._text("state", "growth.md"), "character", "skill", "stage")
        return t.rows if t else []

    def plan_rows(self):
        t = self._table_by_headers(self._text("plan", "chapters.md"), "#", "title", "delivers")
        return t.rows if t else []

    def plan_row(self, number):
        for r in self.plan_rows():
            if re.sub(r"\D", "", r.first()) == str(number):
                return r
        return None

    def voice_rows(self):
        t = self._table_by_headers(
            self._text("bible", "cast", "_voices.md"), "character", "intel", "artic", "wit")
        return t.rows if t else []

    def competence_rows(self):
        t = self._table_by_headers(
            self._text("bible", "cast", "_competence.md"), "character", "domain", "level")
        return t.rows if t else []

    def referral_rows(self):
        text = self._text("bible", "cast", "_competence.md")
        for table in mdio.parse_tables(text):
            heads = [mdio._norm_header(h) for h in table.headers]
            if heads and heads[0] == "character" and any("goto" in h or "outside" in h for h in heads):
                return table.rows
        return []

    def extras_rows(self):
        rows = []
        for t in mdio.parse_tables(self._text("bible", "cast", "_extras.md")):
            rows.extend(t.rows)
        return rows

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
