"""Ledger, threads and plan integrity — the checks that keep the CCS honest.

The benchmark's one recorded state-corruption event was a wrong `wordcount:` that had already
propagated into `state/continuity.md`. These are the checks that catch that class.
"""

import io
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


FUTURE_LEDGER = """# Thread ledger

| id | thread | opened | type | tension | due | carried | status | payoff |
|---|---|---|---|---|---|---|---|---|
| T01 | the permit refusal | 1 | mystery | hot | 10 |  | open |  |
| T02 | the second audit | 6 | threat | cold | 20 |  | open |  |
"""

ODD_ID_LEDGER = """# Thread ledger

| id | thread | opened | type | tension | due | carried | status | payoff |
|---|---|---|---|---|---|---|---|---|
| TH01 | the permit refusal | 1 | mystery | hot | 10 |  | open |  |
"""


class TestThreadOpenedInTheFuture(unittest.TestCase):
    """Benchmark run #5, O8. Threads were pre-registered as opened at ch 6 and ch 9 before
    ch 1 existed, and every check passed - the "never operated on" warn was itself gated on
    `opened <= last_ch`, so the one thread that could not possibly have been operated on was
    the one case exempted from being asked about."""

    def _msgs(self, ledger, chapters=4):
        with NovelFixture() as fx:
            for i in range(1, chapters + 1):
                fx.add_chapter(i, BODY)
            fx.add_ledger(list(range(1, chapters + 1)))
            fx.write("state/threads.md", ledger)
            return [f.message for f in cmd_state.run(fx.novel()).findings]

    def test_a_thread_opened_past_the_last_chapter_is_named(self):
        msgs = self._msgs(FUTURE_LEDGER)
        self.assertTrue(any("T02" in m and "not an open promise" in m for m in msgs))

    def test_a_thread_opened_in_the_past_is_not_named(self):
        msgs = self._msgs(FUTURE_LEDGER)
        self.assertFalse(any(m.startswith("T01 is declared open") for m in msgs))

    def test_a_future_thread_does_not_also_get_the_never_operated_warn(self):
        """One finding per problem. It cannot have been operated on; saying so twice is noise."""
        msgs = [m for m in self._msgs(FUTURE_LEDGER) if "T02" in m]
        self.assertEqual(len(msgs), 1)

    def test_no_thread_ages_backwards(self):
        """The age came out negative, and a negative age sorted to the top of the oldest-first
        list - putting the newest promise where the oldest belongs."""
        with NovelFixture() as fx:
            for i in range(1, 5):
                fx.add_chapter(i, BODY)
            fx.add_ledger([1, 2, 3, 4])
            fx.write("state/threads.md", FUTURE_LEDGER)
            rep = cmd_state.run(fx.novel())
            lines = [ln for _, block in rep.sections for ln in block]
            oldest = [ln for ln in lines if "oldest open" in ln]
            self.assertEqual(len(oldest), 1)
            self.assertNotIn("-", oldest[0].split("oldest open")[1])


class TestThreadIdDrift(unittest.TestCase):
    """The id pattern was `^T\\d+`, copied into five commands. Run #5's novel numbered its
    threads `TH01`, so `sw state` matched nothing and skipped every thread check in silence
    while `sw status` went on counting nine open threads from the same file. A check that
    falls quiet reads exactly like a check that passed."""

    def _rep(self, ledger):
        with NovelFixture() as fx:
            for i in range(1, 5):
                fx.add_chapter(i, BODY)
            fx.add_ledger([1, 2, 3, 4])
            fx.write("state/threads.md", ledger)
            return cmd_state.run(fx.novel())

    def test_an_off_format_id_is_still_read(self):
        msgs = [f.message for f in self._rep(ODD_ID_LEDGER).findings]
        self.assertTrue(any("TH01" in m and "no ledger block has ever operated" in m
                            for m in msgs))

    def test_the_drift_itself_is_reported(self):
        msgs = [f.message for f in self._rep(ODD_ID_LEDGER).findings]
        self.assertTrue(any("TH01" in m and "`T01` form" in m for m in msgs))

    def test_the_documented_form_is_not_reported(self):
        msgs = [f.message for f in self._rep(LEDGER % ("10", "", "open")).findings]
        self.assertFalse(any("`T01` form" in m for m in msgs))

    def test_two_commands_do_not_disagree_about_the_same_ledger(self):
        """The shape of the original defect: `sw status` counted nine open threads out of the
        file that `sw state` read as containing none. Five modules, five copies of the pattern,
        and the drift reached one of them."""
        from swlib import cmd_status
        with NovelFixture() as fx:
            for i in range(1, 5):
                fx.add_chapter(i, BODY)
            fx.add_ledger([1, 2, 3, 4])
            fx.write("state/threads.md", ODD_ID_LEDGER)
            novel = fx.novel()
            state_saw = any("TH01" in f.message for f in cmd_state.run(novel).findings)
            status_text = " ".join(ln for _, b in cmd_status.run(novel).sections for ln in b)
            self.assertTrue(state_saw)
            self.assertIn("TH01", status_text)


class TestEmptyNovel(unittest.TestCase):

    def test_state_survives_a_novel_with_no_chapters(self):
        with NovelFixture() as fx:
            rep = cmd_state.run(fx.novel())
            self.assertIsNotNone(rep)


if __name__ == "__main__":
    unittest.main()
