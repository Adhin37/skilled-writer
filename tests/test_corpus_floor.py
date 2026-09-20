"""`rules.CORPUS_FLOOR` - the one number in this toolkit that fails downward.

Every other budget here is a ceiling, and the failure this file exists for is the one a ceiling
cannot see: `kb.Index._build()` skips any directory without a `SKILL.md`, so a half-finished
move returns an EMPTY index. `sw health` then reports 0/0/0, `sw load` prints a row of zeros,
and both card budgets pass - against a corpus no agent can reach. A clean run is what the worst
failure looks like, which is why the floor lands before anything moves.

The load-bearing test here is `test_an_empty_corpus_passes_every_ceiling`: it asserts the hole
rather than the patch, so it keeps meaning something after the patch is edited.
"""

import os
import shutil
import sys
import tempfile
import unittest

from fixtures import REPO

sys.path.insert(0, os.path.join(REPO, "scripts"))

from swlib import cmd_health, cmd_load, kb, rules  # noqa: E402
from swlib.report import Report  # noqa: E402


class Scratch(object):
    """A directory that looks like the toolkit to `corpus_floor_applies`, with a corpus I choose.

    Only the marker file is real - `rules.corpus_floor_applies` is anchored on
    `scripts/swlib/rules.py`, and nothing under test executes it.
    """

    def __init__(self, marker=True):
        self.marker = marker

    def __enter__(self):
        self.dir = tempfile.mkdtemp(prefix="sw-floor-")
        os.makedirs(os.path.join(self.dir, ".claude", "skills"))
        if self.marker:
            os.makedirs(os.path.join(self.dir, "scripts", "swlib"))
            open(os.path.join(self.dir, "scripts", "swlib", "rules.py"), "w").close()
        return self

    def __exit__(self, *exc):
        shutil.rmtree(self.dir, ignore_errors=True)
        return False

    def skill(self, name):
        d = os.path.join(self.dir, ".claude", "skills", name)
        os.makedirs(d)
        with open(os.path.join(d, "SKILL.md"), "w", encoding="utf-8", newline="\n") as fh:
            fh.write("---\nname: %s\ndescription: does a thing.\n---\n\nbody\n" % name)

    def index(self):
        return kb.index(self.dir, refresh=True)


class TestTheFloorHolds(unittest.TestCase):

    def test_the_real_corpus_clears_every_floor(self):
        """If this fails, read it as the corpus shrinking - not as the floor being too high."""
        self.assertEqual(kb.index(REPO, refresh=True).shortfalls, [])

    def test_every_floor_sits_under_the_figure_it_guards(self):
        """A floor at today's count is a ratchet, and a ratchet on a corpus blocks every edit."""
        idx = kb.index(REPO, refresh=True)
        have = {"skill": len(idx.skills)}
        for kind in ("draft-card", "audit-card", "reference"):
            have[kind] = len(idx.by_type(kind))
        for kind, floor in rules.CORPUS_FLOOR.items():
            self.assertLess(floor, have[kind],
                            "the %s floor is at or above the live count - it would fire on an "
                            "ordinary merge, which is what `CARD_BUDGET` is for" % kind)


class TestTheFailureItCatches(unittest.TestCase):

    def test_an_empty_corpus_passes_every_ceiling(self):
        """The hole, asserted directly. This is the reason the floor exists.

        Deliberately written against the ceilings rather than the floor: it keeps failing for
        the right reason if someone later rewrites `_floor`.
        """
        with Scratch() as sc:
            counts = cmd_load._always_counts(sc.index())
            for kind, cap in rules.CARD_BUDGET.items():
                self.assertEqual(counts[kind][0], 0)
                self.assertLessEqual(counts[kind][0], cap)
            for kind, cap in rules.CARD_WORD_BUDGET.items():
                self.assertLessEqual(counts[kind][1], cap)

    def test_and_the_floor_catches_it(self):
        with Scratch() as sc:
            sc.skill("only-one")
            kinds = [s.split()[1] for s in sc.index().shortfalls]
            self.assertEqual(sorted(kinds), sorted(rules.CORPUS_FLOOR))

    def test_health_reports_a_shortfall_as_a_defect(self):
        original = rules.CORPUS_FLOOR
        rules.CORPUS_FLOOR = dict((k, v * 100) for k, v in original.items())
        try:
            rep = Report("t")
            cmd_health._corpus_floor(REPO, rep)
            self.assertTrue([f for f in rep.findings if f.level == "defect"])
            self.assertEqual({f.check for f in rep.findings}, {"corpus-floor"})
        finally:
            rules.CORPUS_FLOOR = original
            kb.index(REPO, refresh=True)

    def test_load_defects_rather_than_printing_a_row_of_zeros(self):
        """`sw load` is where an unreachable corpus would read as a light chapter."""
        original = cmd_load._always_counts
        cmd_load._always_counts = lambda idx: {"draft-card": (0, 0), "audit-card": (0, 0)}
        try:
            from fixtures import NovelFixture
            with NovelFixture() as fx:
                fx.add_chapter(1, "Prose.\n")
                rep = cmd_load.run(fx.novel(), 1, repo_root=REPO)
            checks = [f.check for f in rep.findings if f.level == "defect"]
            self.assertEqual(checks, ["corpus-floor", "corpus-floor"])
        finally:
            cmd_load._always_counts = original


class TestItDoesNotFireOnSomebodyElse(unittest.TestCase):
    """A floor that fires on every fixture is a floor somebody switches off inside a week."""

    def test_a_directory_that_is_not_this_toolkit_is_not_measured(self):
        with Scratch(marker=False) as sc:
            sc.skill("only-one")
            self.assertEqual(sc.index().shortfalls, [])

    def test_the_marker_is_the_file_that_declares_the_floor(self):
        self.assertTrue(rules.corpus_floor_applies(REPO))
        self.assertFalse(rules.corpus_floor_applies(os.path.dirname(REPO)))


if __name__ == "__main__":
    unittest.main()
