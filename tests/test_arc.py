"""`sw arc` — the distributional pass.

Every high-severity finding in benchmark run #1 was invisible in the chapter it appeared in and
obvious across five. These tests plant that kind of defect and assert the pass finds it.
"""

import unittest

from fixtures import MULTI_PARAGRAPH_SPEECH, NovelFixture
from swlib import cmd_arc

QUIET = "The room was cold. He shut the door and sat down to wait.\n"


def messages(rep):
    return [f.message for f in rep.findings]


def build(fx, n=25, body=None, delivers=None, pay=False):
    for i in range(1, n + 1):
        text = body(i) if callable(body) else (MULTI_PARAGRAPH_SPEECH if body is None else body)
        says = delivers(i) if callable(delivers) else (
            "ch %d changes something" % i if delivers is None else delivers)
        fx.add_chapter(i, text, delivers=says)
    fx.add_ledger(list(range(1, n + 1)))
    if pay:
        with open(fx.path("state", "continuity.md"), encoding="utf-8") as fh:
            text = fh.read()
        fx.write("state/continuity.md",
                 text.replace("thr> ~T01(permit-refused)", "thr> vT01(permit-refused)", 1))


class TestArcPass(unittest.TestCase):

    def test_dialogue_starvation_across_the_arc(self):
        """Run #1 shipped five chapters at 2-5% spoken. No single chapter looked wrong."""
        with NovelFixture() as fx:
            build(fx, 6, body=QUIET, pay=True)
            rep = cmd_arc.run(fx.novel(), 1)
            msgs = messages(rep)
            self.assertTrue(any("under 10% spoken" in m for m in msgs))
            # A silent arc is still the defect run #1 shipped; one quiet chapter is not.
            self.assertIn(("arc-dialogue", "defect"), {(f.check, f.level) for f in rep.findings})

    def test_a_healthy_arc_raises_no_dialogue_finding(self):
        with NovelFixture() as fx:
            build(fx, 6, pay=True)
            msgs = messages(cmd_arc.run(fx.novel(), 1))
            self.assertFalse(any("spoken" in m for m in msgs))

    def test_repeated_delivery_is_reported_as_one_group(self):
        with NovelFixture() as fx:
            build(fx, 6, delivers="Rin cannot get the permit", pay=True)
            found = [m for m in messages(cmd_arc.run(fx.novel(), 1))
                     if "nearly the same thing" in m]
            self.assertEqual(len(found), 1)
            self.assertIn("1, 2, 3", found[0])

    def test_missing_delivers_is_a_defect(self):
        with NovelFixture() as fx:
            build(fx, 6, delivers="", pay=True)
            self.assertTrue(any("no `delivers:`" in m for m in messages(cmd_arc.run(fx.novel(), 1))))

    def test_an_arc_that_closes_nothing_is_a_defect(self):
        with NovelFixture() as fx:
            build(fx, 6)
            msgs = messages(cmd_arc.run(fx.novel(), 1))
            self.assertTrue(any("closed none" in m for m in msgs))

    def test_identical_hooks_are_one_finding(self):
        with NovelFixture() as fx:
            build(fx, 6, pay=True)
            found = [m for m in messages(cmd_arc.run(fx.novel(), 1))
                     if "near-identical" in m]
            self.assertEqual(len(found), 1)

    def test_a_missing_ledger_block_is_caught(self):
        with NovelFixture() as fx:
            build(fx, 6, pay=True)
            fx.add_chapter(7, MULTI_PARAGRAPH_SPEECH)
            self.assertTrue(any("no CCS block for chapter" in m
                                for m in messages(cmd_arc.run(fx.novel(), 1))))

    def test_it_never_scores(self):
        """The pass reports and hands over. A scored arc is one the next arc is written toward."""
        with NovelFixture() as fx:
            build(fx, 6, pay=True)
            rendered = cmd_arc.run(fx.novel(), 1).render(show="note")
            self.assertIn("the judged half", rendered)
            self.assertIn("Do not score the arc", rendered)

    def test_empty_range_is_reported_not_crashed(self):
        with NovelFixture() as fx:
            rep = cmd_arc.run(fx.novel(), 3)
            self.assertTrue(any("no chapters in range" in m for m in messages(rep)))


def add_divergence(fx, ch, effect):
    """Put one row into `state/timeline.md`'s divergence ledger."""
    with open(fx.path("state", "timeline.md"), encoding="utf-8") as fh:
        text = fh.read()
    head = "| ch | MC action | track id | effect | order | who noticed | reciprocity opened |"
    sep = "|---|---|---|---|---|---|---|"
    row = "| %d | she leaned on the clerk | W01 | %s | 1st | nobody | a favour owed |" % (ch, effect)
    fx.write("state/timeline.md", text.replace(head + "\n" + sep,
                                               head + "\n" + sep + "\n" + row, 1))


class TestArcDivergence(unittest.TestCase):
    """`state/timeline.md` states the arc rule; until now nothing read the table.

    The one-sided shape at its purest: a divergence row is only ever wrong by saying something,
    so an empty ledger cleared every check in the repo.
    """

    def find(self, fx):
        return [m for m in messages(cmd_arc.run(fx.novel(), 1)) if "divergence row" in m]

    def test_an_empty_divergence_ledger_is_found(self):
        with NovelFixture() as fx:
            build(fx, 6, pay=True)
            self.assertEqual(len(self.find(fx)), 1)

    def test_unchanged_rows_alone_do_not_satisfy_the_arc_rule(self):
        with NovelFixture() as fx:
            build(fx, 6, pay=True)
            add_divergence(fx, 3, "`unchanged` (she was confined all arc)")
            self.assertEqual(len(self.find(fx)), 1)

    def test_one_real_divergence_row_clears_it(self):
        with NovelFixture() as fx:
            build(fx, 6, pay=True)
            add_divergence(fx, 3, "created")
            self.assertEqual(self.find(fx), [])

    def test_a_row_outside_the_arc_does_not_count(self):
        with NovelFixture() as fx:
            build(fx, 6, pay=True)
            add_divergence(fx, 99, "created")
            self.assertEqual(len(self.find(fx)), 1)

    def test_it_is_never_a_defect(self):
        """An MC who genuinely changed nothing is a legitimate arc, not a blocked ship."""
        with NovelFixture() as fx:
            build(fx, 6, pay=True)
            levels = {f.level for f in cmd_arc.run(fx.novel(), 1).findings
                      if f.check == "arc-divergence"}
            self.assertTrue(levels)
            self.assertNotIn("defect", levels)

    def test_effect_reads_only_the_leading_word(self):
        self.assertEqual(cmd_arc._effect("`unchanged` (she was confined)"), "unchanged")
        self.assertEqual(cmd_arc._effect("**created**"), "created")
        self.assertEqual(cmd_arc._effect("   "), "")


if __name__ == "__main__":
    unittest.main()


class TestTheOppositionHasAFace(unittest.TestCase):
    """Run #6's cold read, ranked first: five chapters, three hostile documents, no person."""

    ARCS = ("# Arcs\n\n**Antagonistic force.** Veyra Stall, acting on the Board's authority. "
            "Her case: the levy keeps the bridges up.\n")

    def _checks(self, early_mentions):
        with NovelFixture() as fx:
            fx.write("plan/arcs.md", self.ARCS)
            build(fx, 5, body=lambda i: QUIET + ("Veyra Stall signed it herself.\n"
                                                 if i in early_mentions else ""))
            return {(f.check, f.level) for f in cmd_arc.run(fx.novel(), 1).findings}

    def test_an_antagonist_absent_by_the_contract_chapter_is_named(self):
        self.assertIn(("arc-antagonist", "warn"), self._checks(early_mentions=(4, 5)))

    def test_one_on_the_page_in_time_is_not(self):
        self.assertNotIn(("arc-antagonist", "warn"), self._checks(early_mentions=(2,)))

    def test_the_template_placeholder_names_nobody(self):
        with NovelFixture() as fx:
            build(fx, 5, body=QUIET)
            self.assertEqual(cmd_arc.antagonist_names(fx.novel()), [])
