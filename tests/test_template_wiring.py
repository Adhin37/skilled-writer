"""The template and the parsers must not drift apart.

`plan_rows()` selects its table by the columns `("#", "title", "delivers")`, and the shipped
`plan/chapters.md` header did not carry `delivers`. Against the real template it therefore
returned `[]` forever: every plan check in `sw state` was dead, and the read-set's plan section
always reported "no plan rows in range" no matter what the author had written. Nothing caught it,
because every test that exercised plan rows supplied its own table.

These are the checks that catch that class. They run against `novels/_template` itself, so a
column renamed on one side and not the other fails here rather than silently in a novel.
"""

import os
import re
import unittest

from fixtures import TEMPLATE

from swlib import mdio
from swlib.novelio import Novel


TEMPLATE_NOVEL = Novel(TEMPLATE)

# Every table a parser selects by column name, and the columns it selects on.
TABLE_ACCESSORS = [
    ("threads",         ("state", "threads.md"),            ("id", "thread", "status")),
    ("growth_rows",     ("state", "growth.md"),              ("character", "rung")),
    ("skill_rows",      ("state", "growth.md"),              ("character", "skill", "stage")),
    ("standing_rows",   ("state", "power.md"),               ("character", "tier", "the edge")),
    ("ladder_rows",     ("state", "power.md"),               ("tier", "how many alive")),
    ("pressure_rows",   ("state", "power.md"),               ("ch", "opposition", "p")),
    ("gain_rows",       ("state", "power.md"),               ("ch", "source", "new problem")),
    ("boost_rows",      ("state", "power.md"),               ("ch", "boost", "the debt")),
    ("curve_plan_rows", ("state", "power.md"),               ("arc", "pressure band")),
    ("plan_rows",       ("plan", "chapters.md"),             ("#", "title", "delivers")),
    ("voice_rows",      ("bible", "cast", "_voices.md"),     ("character", "intel", "artic",
                                                              "wit")),
    ("competence_rows", ("bible", "cast", "_competence.md"), ("character", "domain", "level")),
]

# Every section a parser slices out by heading text.
SECTION_LOOKUPS = [
    (("bible", "cast", "_voices.md"),    "POV THOUGHT"),
    (("bible", "cast", "_voices.md"),    "MIRROR"),
    (("plan", "timeline.md"),            "SCHEDULED FOR THIS ARC"),
    (("state", "body.md"),               "CURRENT FORM"),
    (("state", "body.md"),               "ABSOLUTE LIMITS"),
    (("state", "foreknowledge.md"),      "THE GRAIN"),
    (("state", "foreknowledge.md"),      "THE INVENTORY"),
    (("state", "foreknowledge.md"),      "THE SPEND LOG"),
    (("state", "power.md"),              "CURRENT STANDING"),
    (("state", "power.md"),              "THE LADDER"),
    (("state", "power.md"),              "ACTIVE BOOSTS"),
    (("state", "continuity.md"),         "BOOK DIGEST"),
    (("state", "continuity.md"),         "ARC DIGEST"),
]


class TestTableAccessors(unittest.TestCase):
    """Every `_table_by_headers` selector resolves against the shipped template."""

    def test_every_selector_finds_its_table(self):
        broken = []
        for name, parts, cols in TABLE_ACCESSORS:
            text = TEMPLATE_NOVEL._text(*parts)
            if TEMPLATE_NOVEL._table_by_headers(text, *cols) is None:
                have = [t.headers for t in mdio.parse_tables(text)]
                broken.append("%s: %s wants %s; template has %s"
                              % (name, "/".join(parts), list(cols), have))
        self.assertEqual(broken, [],
                         "a parser selects on columns the template does not have, so it returns "
                         "[] against every real novel")

    def test_the_two_accessors_with_their_own_selection_logic_still_match(self):
        """`location_rows` accepts `location` or `place`; `extras_rows` takes every table."""
        self.assertTrue(TEMPLATE_NOVEL.location_rows() is not None)
        heads = [[mdio._norm_header(h) for h in t.headers]
                 for t in mdio.parse_tables(TEMPLATE_NOVEL._text("bible", "world.md"))]
        self.assertTrue(any("location" in h or "place" in h for h in heads),
                        "bible/world.md has no location table under either accepted name")
        self.assertTrue(mdio.parse_tables(TEMPLATE_NOVEL._text("bible", "cast", "_extras.md")),
                        "bible/cast/_extras.md has no tables, so the roster is unreadable")

    def test_a_filled_plan_row_is_actually_read(self):
        """The regression itself: rows written by the author must reach `plan_rows()`."""
        text = TEMPLATE_NOVEL._text("plan", "chapters.md")
        table = TEMPLATE_NOVEL._table_by_headers(text, "#", "title", "delivers")
        self.assertIsNotNone(table)
        for col in ("goal", "obstacle", "turn", "delivers", "cost", "hook"):
            self.assertIn(col, [mdio._norm_header(h) for h in table.headers],
                          "cmd_state.PLAN_REQUIRED checks `%s`, which the template omits" % col)


class TestSectionLookups(unittest.TestCase):
    """Every `mdio.section` heading resolves against the shipped template."""

    def test_every_heading_exists_and_is_not_empty(self):
        broken = []
        for parts, heading in SECTION_LOOKUPS:
            got = mdio.section(TEMPLATE_NOVEL._text(*parts), heading)
            if not (got and got.strip()):
                broken.append("%s -> %s" % ("/".join(parts), heading))
        self.assertEqual(broken, [],
                         "the read-set slices these by heading; a renamed heading silently "
                         "drops the section")


class TestConfigKeysHaveOwners(unittest.TestCase):
    """Every key in novel.md is named, by that exact key, somewhere that fills or reads it.

    `mc.starting_power` sat in the template for the life of the repo as a write-once field with
    no reader and no updater: no skill mentioned it and no script parsed it. A key nothing names
    is a question asked at init whose answer goes nowhere.
    """

    # `docs/` is excluded on purpose: it carries rationale and history, and a key named only
    # in a post-mortem ("mc.starting_power had no reader") is not a key with an owner.
    SEARCH_ROOTS = [".claude", "scripts"]
    SEARCH_FILES = ["CLAUDE.md"]

    @staticmethod
    def _flatten(d, prefix=""):
        out = []
        for k, v in (d or {}).items():
            key = "%s.%s" % (prefix, k) if prefix else k
            out += (TestConfigKeysHaveOwners._flatten(v, key)
                    if isinstance(v, dict) else [key])
        return out

    def _corpus(self):
        repo = os.path.dirname(TEMPLATE.rstrip(os.sep))
        repo = os.path.dirname(repo)
        chunks = []
        paths = [os.path.join(repo, f) for f in self.SEARCH_FILES]
        for root_name in self.SEARCH_ROOTS:
            for root, dirs, files in os.walk(os.path.join(repo, root_name)):
                dirs[:] = [d for d in dirs if d != "__pycache__"]
                paths += [os.path.join(root, f) for f in files
                          if f.endswith((".md", ".py"))]
        for p in paths:
            if os.path.isfile(p):
                with open(p, encoding="utf-8", errors="ignore") as fh:
                    chunks.append(fh.read())
        return "\n".join(chunks)

    def test_no_key_is_an_orphan(self):
        text = self._corpus()
        orphans = []
        for key in sorted(self._flatten(TEMPLATE_NOVEL.cfg)):
            leaf = key.split(".")[-1]
            if key in text or re.search(r"\b%s\b" % re.escape(leaf), text):
                continue
            orphans.append(key)
        self.assertEqual(orphans, [],
                         "novel.md declares these but no skill names them and no script reads "
                         "them - either wire them to an owner or drop them from the template")


class TestOptionalToggles(unittest.TestCase):
    """CLAUDE.md section 3: each `optional:` key maps to `.claude/skills/<key>/`."""

    def test_every_toggle_has_a_skill_directory(self):
        repo = os.path.dirname(os.path.dirname(TEMPLATE.rstrip(os.sep)))
        missing = [k for k in (TEMPLATE_NOVEL.cfg.get("optional") or {})
                   if not os.path.isdir(os.path.join(repo, ".claude", "skills", k))]
        self.assertEqual(missing, [], "an `optional:` key with no skill behind it never no-ops; "
                                      "it is simply never read")


if __name__ == "__main__":
    unittest.main()
