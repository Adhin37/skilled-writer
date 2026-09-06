"""Ledger, threads and plan integrity — the checks that keep the CCS honest.

The benchmark's one recorded state-corruption event was a wrong `wordcount:` that had already
propagated into `state/continuity.md`. These are the checks that catch that class.
"""

import unittest

from fixtures import NovelFixture
from swlib import cmd_state, cmd_write

BODY = "The room was cold.\n\n\"Shut it,\" she said.\n\nHe shut it.\n"


def checks(rep):
    return {f.check for f in rep.findings}


class TestLedger(unittest.TestCase):

    def test_wc_disagreement_is_caught(self):
        with NovelFixture() as fx:
            fx.add_chapter(1, BODY)
            fx.add_ledger([1], {1: 999})
            rep = cmd_state.run(fx.novel())
            self.assertIn("ccs", checks(rep))
            self.assertTrue(any("wc:999" in f.message for f in rep.findings))

    def test_stamp_ledger_repairs_the_disagreement(self):
        with NovelFixture() as fx:
            fx.add_chapter(1, BODY)
            fx.add_ledger([1], {1: 999})
            cmd_write.stamp(fx.novel(), 1, sync_ledger=True)
            rep = cmd_state.run(fx.novel())
            self.assertNotIn("ccs", checks(rep))

    def test_ledger_repair_keeps_the_rest_of_the_file(self):
        with NovelFixture() as fx:
            fx.add_chapter(1, BODY)
            fx.add_ledger([1], {1: 999})
            before = fx.read_bytes("state/continuity.md")
            cmd_write.stamp(fx.novel(), 1, sync_ledger=True)
            after = fx.read_bytes("state/continuity.md")
            self.assertEqual(len(before.splitlines()), len(after.splitlines()))
            self.assertIn(b"hook> the clerk locks the door behind her", after)

    def test_a_chapter_with_no_block_is_reported(self):
        with NovelFixture() as fx:
            fx.add_chapter(1, BODY)
            rep = cmd_state.run(fx.novel())
            self.assertTrue(rep.findings)

    def test_thread_operated_on_without_a_row(self):
        with NovelFixture() as fx:
            fx.add_chapter(1, BODY)
            fx.add_ledger([1])
            rep = cmd_state.run(fx.novel())
            self.assertIn("threads", checks(rep))


LEDGER = """# Thread ledger

| id | thread | opened | type | tension | due | carried | status | payoff |
|---|---|---|---|---|---|---|---|---|
| T01 | the permit refusal | 1 | mystery | hot | %s | %s | %s |  |
"""


def novel_with_threads(fx, chapters, due="10", carried="", status="open"):
    for i in range(1, chapters + 1):
        fx.add_chapter(i, BODY)
    fx.add_ledger(list(range(1, chapters + 1)))
    fx.write("state/threads.md", LEDGER % (due, carried, status))


class TestThreadAgeing(unittest.TestCase):
    """plot-threads section Ageing — the mechanism behind perpetual deferral."""

    def test_overdue_thread_without_a_reason_is_a_defect(self):
        with NovelFixture() as fx:
            novel_with_threads(fx, 25, due="10")
            msgs = [f.message for f in cmd_state.run(fx.novel()).findings]
            self.assertTrue(any("past its due chapter" in m and "no deferral reason" in m
                                for m in msgs))

    def test_a_recorded_reason_downgrades_it_to_a_warning(self):
        with NovelFixture() as fx:
            novel_with_threads(fx, 25, due="10", carried="to 40: the informant's price rose")
            findings = [f for f in cmd_state.run(fx.novel()).findings
                        if "past its due" in f.message]
            self.assertEqual(len(findings), 1)
            self.assertEqual(findings[0].level, "warn")

    def test_an_arc_that_pays_nothing_is_a_defect(self):
        with NovelFixture() as fx:
            novel_with_threads(fx, 25, due="99")
            msgs = [f.message for f in cmd_state.run(fx.novel()).findings]
            self.assertTrue(any("closed without paying a single thread" in m for m in msgs))

    def test_an_arc_that_pays_one_is_clean(self):
        with NovelFixture() as fx:
            novel_with_threads(fx, 25, due="99")
            with open(fx.path("state", "continuity.md"), encoding="utf-8") as fh:
                text = fh.read()
            fx.write("state/continuity.md", text.replace("thr> ~T01(permit-refused)",
                                                         "thr> vT01(permit-refused)", 1))
            msgs = [f.message for f in cmd_state.run(fx.novel()).findings]
            self.assertFalse(any("without paying a single thread" in m for m in msgs))

    def test_no_arc_check_before_the_first_arc_closes(self):
        with NovelFixture() as fx:
            novel_with_threads(fx, 5, due="99")
            msgs = [f.message for f in cmd_state.run(fx.novel()).findings]
            self.assertFalse(any("without paying a single thread" in m for m in msgs))


class TestEmptyNovel(unittest.TestCase):

    def test_state_survives_a_novel_with_no_chapters(self):
        with NovelFixture() as fx:
            rep = cmd_state.run(fx.novel())
            self.assertIsNotNone(rep)


if __name__ == "__main__":
    unittest.main()
