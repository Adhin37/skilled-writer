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

from fixtures import REPO, TEMPLATE

from swlib import cmd_health, mdio
from swlib.novelio import Novel


TEMPLATE_NOVEL = Novel(TEMPLATE)

# The two tables live in `swlib.cmd_health`, which is what `sw health` reports from. Importing
# them rather than restating them is the point: a check that exists twice drifts, and the copy
# nobody runs is the one that goes stale.
TABLE_ACCESSORS = cmd_health.TABLE_ACCESSORS
SECTION_LOOKUPS = cmd_health.SECTION_LOOKUPS


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


class TestTemplateAxes(unittest.TestCase):
    """An axis the corpus mandates must have a slot in the template.

    A new novel is scaffolded from `novels/_template`, so a missing slot is a field no book will
    ever carry. `cadence` reached `voice-separation` §3 and `CLAUDE.md` §4 and neither template
    file; `eq` reached the matrix but not the profile the matrix calls its source of truth. Both
    were invisible because nothing checked owner -> template, only config-key -> owner.
    """

    def test_every_mandated_axis_has_a_template_slot(self):
        missing = []
        for axis, owner, targets in cmd_health.TEMPLATE_AXES:
            word = re.compile(r"\b%s\b" % re.escape(axis), re.I)
            for parts in targets:
                if not word.search(TEMPLATE_NOVEL._text(*parts)):
                    missing.append("%s (%s) in %s" % (axis, owner, "/".join(parts)))
        self.assertEqual([], missing, "axes with no template slot: %s" % "; ".join(missing))

    def test_the_axis_table_is_not_empty(self):
        self.assertTrue(cmd_health.TEMPLATE_AXES, "the guard would pass vacuously")


class TestCardScope(unittest.TestCase):
    """A card may be narrower than the skill that owns it, never broader.

    `pov-switch`'s draft card carried `when: always` while its skill and its own audit card were
    gated on `pov.mode != single`, so every single-POV novel opened a card for a decision it does
    not have — and spent one of twelve unconditional draft-card budget slots on it.
    """

    def test_no_card_is_broader_than_its_skill(self):
        from swlib import kb

        idx = kb.index(REPO, refresh=True)
        broader = []
        for kind in ("draft-card", "audit-card"):
            for f in idx.by_type(kind):
                skill = idx.skills.get(f.owner)
                if skill is None:
                    continue
                if (cmd_health._norm_when(skill.when) != "always"
                        and cmd_health._norm_when(f.when) == "always"):
                    broader.append("%s (skill is `when: %s`)" % (f.rel, skill.when))
        self.assertEqual([], broader, "cards broader than their skill: %s" % "; ".join(broader))


class TestDanglingCardPointers(unittest.TestCase):
    """No file points at a card that does not exist.

    Benchmark run #2's D4 in its recurring form: the `timeline-engine` audit card merged into
    `plot-threads`' and both Pass 4 texts went on naming it.
    """

    def test_health_reports_no_dangling_card(self):
        from swlib.report import Report

        rep = Report("probe")
        cmd_health._dangling_cards(REPO, cmd_health.skill_names(REPO), rep)
        found = [f for f in rep.findings if f.check == "card-dangling"]
        self.assertEqual([], [f.message for f in found])
