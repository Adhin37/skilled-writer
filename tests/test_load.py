"""`sw load` - the command that measures the instructions rather than the novel.

Untested until now, which is the wrong way round: `load` and `trace` are the two commands that
score the *toolkit*, and run #4's T1 was a `trace` bug that made the headline number wrong for
three earlier runs. Measurement code with no tests is the worst place in a repo to have none.

Nothing here asserts a corpus size. The counts move every time somebody edits a card, and a
test that pins them would be a test somebody deletes. These assert the *properties*: that the
measurement is honest, that the budget is enforced where it is claimed to be, and above all
that nothing in `load` can reach a chapter.
"""

import os
import sys
import unittest

from fixtures import REPO, NovelFixture

sys.path.insert(0, os.path.join(REPO, "scripts"))

from swlib import cmd_load, kb, rules  # noqa: E402


class TestMeasure(unittest.TestCase):

    def _write(self, fx, text):
        return fx.write("_card.md", text)

    def test_frontmatter_is_excluded(self):
        """Frontmatter is wiring, not instruction, and counting it inflates every card."""
        with NovelFixture() as fx:
            bare = self._write(fx, "one two three\n")
            w_bare, _b, _n = cmd_load.measure(bare)
            withfm = self._write(fx, "---\nname: x\ntype: draft-card\n---\none two three\n")
            w_fm, _b, _n = cmd_load.measure(withfm)
            self.assertEqual(w_bare, w_fm)

    def test_checkboxes_and_negations_are_counted(self):
        with NovelFixture() as fx:
            p = self._write(fx, "- [ ] never do this\n- [ ] no, not that\n- [x] done\n")
            _w, boxes, negs = cmd_load.measure(p)
            self.assertEqual(boxes, 2, "a ticked box is not a live compliance item")
            self.assertEqual(negs, 3)

    def test_a_missing_file_measures_as_zero_rather_than_raising(self):
        """A card named in frontmatter and absent on disk must not kill the report."""
        self.assertEqual(cmd_load.measure(os.path.join(REPO, "does", "not", "exist")),
                         (0, 0, 0))

    def test_the_negation_vocabulary_is_fixed(self):
        """A list that grows whenever somebody thinks of another negative word measures the
        list, not the corpus. This is a trend line, so the vocabulary is pinned."""
        for word in ("never", "no", "not", "cannot", "avoid", "banned"):
            self.assertRegex(word, cmd_load.NEGATION)
        for word in ("should", "prefer", "rarely", "seldom"):
            self.assertNotRegex(word, cmd_load.NEGATION)


class TestBudget(unittest.TestCase):

    def test_the_unconditional_set_is_within_its_card_budget(self):
        """`rules.CARD_BUDGET` binds the corpus, and `sw health` is where it is enforced.

        Asserted here too because this is the function that computes the number health reads.
        """
        counts = cmd_load._always_counts(kb.index(REPO))
        for kind, cap in rules.CARD_BUDGET.items():
            self.assertLessEqual(counts[kind][0], cap,
                                 "%s is past its budget - a new card must merge with the one "
                                 "that already owns its neighbourhood" % kind)

    def test_the_unconditional_word_figure_is_reported(self):
        counts = cmd_load._always_counts(kb.index(REPO))
        for kind in rules.CARD_BUDGET:
            self.assertGreater(counts[kind][1], 0,
                               "%s reports zero words - the measurement is broken, not the "
                               "corpus empty" % kind)


class TestLoadScoresNoChapter(unittest.TestCase):
    """The standing contract: `load` measures instructions and never a novel.

    It is the one command whose output a drafter could plausibly mistake for a target, so the
    contract is asserted rather than trusted.
    """

    def test_the_report_never_reads_a_chapter_file(self):
        with NovelFixture() as fx:
            fx.add_chapter(1, "Some prose.\n" * 50)
            rep = cmd_load.run(fx.novel(), 1, repo_root=REPO)
            text = "\n".join(str(f.message) for f in rep.findings)
            self.assertNotIn("wordcount", text)
            self.assertNotIn("0001", text)

    def test_the_same_chapter_measures_the_same_whatever_the_prose(self):
        """The number is a property of the instructions, so prose must not move it."""
        with NovelFixture() as fx:
            fx.add_chapter(1, "Short.\n")
            a = cmd_load.run(fx.novel(), 1, repo_root=REPO)
            fx.add_chapter(1, "Much longer prose. " * 400)
            b = cmd_load.run(fx.novel(), 1, repo_root=REPO)
            self.assertEqual([f.message for f in a.findings],
                             [f.message for f in b.findings])

    def test_it_raises_nothing_above_a_warn(self):
        """Nothing in `load` may fail a run: the budget is a maintainer signal."""
        with NovelFixture() as fx:
            fx.add_chapter(1, "Prose.\n")
            rep = cmd_load.run(fx.novel(), 1, repo_root=REPO)
            self.assertEqual([f for f in rep.findings if f.level == "defect"], [])


if __name__ == "__main__":
    unittest.main()


class TestWordBudget(unittest.TestCase):
    """`CARD_WORD_BUDGET` - the ratchet on the number that actually costs a drafter.

    `CARD_BUDGET` bounds the card COUNT, and the merges it forced moved four draft cards and
    three audit cards into the card that already owned their neighbourhood. The count fell
    42 -> 35 and the instruction load went 16,359 -> 16,550 words, because a merged card costs
    a drafter exactly what its two halves cost separately - and nothing, anywhere, objected.
    """

    def _words(self, kind):
        idx = kb.index(REPO, refresh=True)
        cards = [f for f in idx.by_type(kind)
                 if not f.when or f.when.strip() == "always"]
        return sum(cmd_load.measure(f.path)[0] for f in cards)

    def test_the_unconditional_set_is_within_its_word_budget(self):
        for kind, cap in rules.CARD_WORD_BUDGET.items():
            self.assertLessEqual(
                self._words(kind), cap,
                "%s is past its word budget - a merge does not pay for itself, so an "
                "addition has to be paid for with a cut (docs/creative-latitude.md item 6)"
                % kind)

    def test_every_kind_with_a_card_budget_also_has_a_word_budget(self):
        """The count alone was the hole. A new kind must not reopen it."""
        self.assertEqual(sorted(rules.CARD_BUDGET), sorted(rules.CARD_WORD_BUDGET))

    def test_health_reports_it_when_the_budget_is_exceeded(self):
        """A budget nothing enforces is a comment (`sw selftest`'s own argument)."""
        from swlib import cmd_health
        from swlib.report import Report
        original = rules.CARD_WORD_BUDGET
        rules.CARD_WORD_BUDGET = dict((k, 1) for k in original)
        try:
            rep = Report("t")
            cmd_health._card_budget(REPO, rep)
            checks = [f.check for f in rep.findings]
            self.assertIn("card-words", checks)
            self.assertTrue([f for f in rep.findings if f.level == "defect"])
        finally:
            rules.CARD_WORD_BUDGET = original
