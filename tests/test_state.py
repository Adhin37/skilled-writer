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


class TestEmptyNovel(unittest.TestCase):

    def test_state_survives_a_novel_with_no_chapters(self):
        with NovelFixture() as fx:
            rep = cmd_state.run(fx.novel())
            self.assertIsNotNone(rep)


if __name__ == "__main__":
    unittest.main()
