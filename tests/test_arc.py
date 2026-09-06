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
            msgs = messages(cmd_arc.run(fx.novel(), 1))
            self.assertTrue(any("under 10% spoken" in m for m in msgs))

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


if __name__ == "__main__":
    unittest.main()
