"""The chapter loop as a pipeline of agents, and the seams between them.

Benchmark run #6 was going to be the first run through the role pipeline - drafter, gate,
architect as separate agents - and no chapter had ever gone drafter -> gate -> state end to end.
An audit on 2026-09-24 found the seams were where it would break, not the stages: a read-set too
long for the harness to show inline, a gate handed the brief it must not see, a module list that
sent the drafter to files its own guard refuses, a ledger check that failed every chapter the
gate was gating, and three step-proof lines nothing asked for. Each class below pins one seam.
"""

import os
import re
import sys
import unittest
from unittest import mock

from fixtures import NOVEL_MD, REPO, NovelFixture

from swlib import cmd_arc, cmd_health, cmd_history, cmd_lint, cmd_readset, cmd_state
from swlib.report import Report

BODY = "The room was cold.\n\n\"Shut it,\" she said.\n\nHe shut it.\n"

BRIEF = '''# Brief

```
Ch 2 — "The Second Quarter"
event    Wren files the counter-claim and is put out of the house
cand     1:she pays the levy 2:she talks Maro into paying -> took 3, the other two keep the house
gives    Noor walks her home the long way
next     the quarter answers in nine days
```
'''


def _status(fx, number, status):
    """Rewrite a fixture chapter's `status:`; the fixture writes `drafted`."""
    path = fx.path("chapters", "%04d-chapter.md" % number)
    with open(path, encoding="utf-8") as fh:
        text = fh.read()
    fx.write("chapters/%04d-chapter.md" % number, text.replace("status: drafted",
                                                               "status: %s" % status))


def _without(fx, key):
    """Drop every `<key>>` line from the ledger - a block written before the line existed."""
    with open(fx.path("state", "continuity.md"), encoding="utf-8") as fh:
        text = fh.read()
    fx.write("state/continuity.md", re.sub(r"(?m)^%s> .*\n" % key, "", text))


def _section(text, heading):
    if heading not in text:
        return ""
    return text.split(heading, 1)[1].split("\n## ", 1)[0]


class TestTheGateIsNotHandedTheBrief(unittest.TestCase):
    """`write-chapter` step 4 keeps the brief from the gate - a gate told what the chapter was
    reaching for grades it on the reach. The gate's own step 1 was `readset -c N`, which printed
    `state/brief.md` whenever it matched N: at Phase C, always."""

    def test_the_draft_role_gets_the_brief_and_the_gate_role_does_not(self):
        with NovelFixture() as fx:
            fx.write("state/brief.md", BRIEF)
            novel = fx.novel()
            drafted = cmd_readset.build(novel, 2)
            gated = cmd_readset.build(novel, 2, role="gate")
        self.assertIn("Wren files the counter-claim", drafted)
        self.assertNotIn("BRIEF ON FILE", gated)
        self.assertNotIn("Wren files the counter-claim", gated)
        self.assertNotIn("took 3", gated, "the rejected candidates are the brief's too")

    def test_the_gate_gets_no_phase_a_cards_and_no_module_list(self):
        """Its cards are `sw kb passes`; the phase A list is the drafter's decision set."""
        with NovelFixture() as fx:
            fx.add_chapter(1, BODY)
            gated = cmd_readset.build(fx.novel(), 1, role="gate")
        self.assertNotIn("### CARDS -", gated)
        self.assertNotIn("### active modules", gated)
        self.assertIn("sw kb passes", gated)

    def test_an_unknown_role_is_refused_rather_than_read_as_draft(self):
        with NovelFixture() as fx:
            with self.assertRaises(ValueError):
                cmd_readset.build(fx.novel(), 1, role="reader")


class TestTheReadSetSaysWhereItEnds(unittest.TestCase):
    """Past ~30 KB the harness hands an agent a 2 KB preview and a saved file. A chapter-6
    read-set is 46 KB, and a drafter paged it back with `cat` with nothing telling it the set
    was partial. Rule 1 says a short field is re-fetched - which needs the agent to be able to
    tell."""

    def test_the_last_line_is_the_end_mark(self):
        with NovelFixture() as fx:
            fx.add_chapter(1, BODY)
            text = cmd_readset.build(fx.novel(), 2)
        self.assertEqual(text.rstrip("\n").splitlines()[-1], cmd_readset.END_MARK % 2)

    def test_the_header_names_the_end_mark_and_the_size(self):
        """In the header, because the header is what a truncated delivery still shows."""
        with NovelFixture() as fx:
            text = cmd_readset.build(fx.novel(), 1)
        head = "\n".join(text.splitlines()[:3])
        self.assertIn(cmd_readset.END_MARK % 1, head)
        m = re.search(r"# (\d+) lines, ([\d.]+) KB", head)
        self.assertTrue(m, head)
        self.assertLessEqual(abs(int(m.group(1)) - len(text.splitlines())), 3)

    def test_the_gate_slice_ends_the_same_way(self):
        with NovelFixture() as fx:
            text = cmd_readset.build(fx.novel(), 1, role="gate")
        self.assertTrue(text.rstrip("\n").endswith(cmd_readset.END_MARK % 1))


class TestResumeIsReadOffTheDisk(unittest.TestCase):
    """A resumed chapter was told to "start again at step 0", which for a drafted chapter is
    ambiguous - redraft it? Every boundary now leaves a mark on disk, so the phase to resume at
    is a fact about files, not a memory of a conversation that may be gone."""

    def _resume(self, fx, number=2):
        return _section(cmd_readset.build(fx.novel(), number), "## RESUME")

    def test_a_fresh_chapter_has_no_resume_section(self):
        with NovelFixture() as fx:
            fx.add_chapter(1, BODY)
            self.assertEqual(self._resume(fx), "")

    def test_a_proposed_brief_is_presented_again_not_rewritten(self):
        with NovelFixture() as fx:
            fx.write("state/brief.md", "status: proposed\n\n" + BRIEF)
            text = cmd_readset.build(fx.novel(), 2)
        self.assertIn("RESUME at the phase A stop", _section(text, "## RESUME"))
        brief = _section(text, "## BRIEF ON FILE")
        self.assertIn("status: proposed", brief)
        self.assertIn("Not yet approved", brief)

    def test_an_approved_brief_resumes_at_phase_b(self):
        with NovelFixture() as fx:
            fx.write("state/brief.md", "status: approved\n\n" + BRIEF)
            self.assertIn("RESUME at phase B", self._resume(fx))

    def test_a_drafted_chapter_goes_back_to_the_coordinator_for_the_gate(self):
        with NovelFixture() as fx:
            fx.add_chapter(2, BODY)
            resume = self._resume(fx)
        self.assertIn("RESUME at phase C", resume)
        self.assertIn("READY FOR GATE", resume)

    def test_a_gated_chapter_resumes_at_the_state_write(self):
        with NovelFixture() as fx:
            fx.add_chapter(2, BODY)
            _status(fx, 2, "gated")
            resume = self._resume(fx)
        self.assertIn("RESUME at step 5", resume)
        self.assertIn("Do not re-gate", resume)

    def test_a_revised_chapter_with_its_block_is_finished(self):
        with NovelFixture() as fx:
            fx.add_chapter(2, BODY)
            _status(fx, 2, "revised")
            fx.add_ledger([2])
            self.assertIn("It is finished", self._resume(fx))

    def test_a_revised_chapter_without_its_block_resumes_at_the_state_write(self):
        with NovelFixture() as fx:
            fx.add_chapter(2, BODY)
            _status(fx, 2, "revised")
            self.assertIn("RESUME at step 5", self._resume(fx))

    def test_a_gated_chapter_below_is_named_as_unfinished_not_ungated(self):
        """`gated` counts as unfinished - the gate passed it, the state never landed - and the
        message has to say which of the two happened, or the fix sent is the wrong one."""
        with NovelFixture() as fx:
            fx.add_chapter(1, BODY)
            _status(fx, 1, "gated")
            gate = _section(cmd_readset.build(fx.novel(), 2), "## GATE")
        self.assertIn("step 5 never wrote its state", gate)
        self.assertNotIn("never ran on it", gate)


class TestTheBriefFileSaysWhatItIs(unittest.TestCase):
    """The same species as the `TH01` thread ids: a format drift that makes a check go quiet."""

    def test_a_brief_with_no_status_line_reads_as_approved(self):
        """It predates the line, and was written on approval under the old procedure."""
        with NovelFixture() as fx:
            fx.write("state/brief.md", BRIEF)
            self.assertEqual(fx.novel().brief_status(), "approved")

    def test_a_proposed_brief_says_so(self):
        with NovelFixture() as fx:
            fx.write("state/brief.md", "status: proposed\n\n" + BRIEF)
            self.assertEqual(fx.novel().brief_status(), "proposed")

    def test_a_chapter_spelled_out_is_still_a_brief(self):
        with NovelFixture() as fx:
            fx.write("state/brief.md", BRIEF.replace("Ch 2 —", "Chapter 2 —"))
            self.assertEqual(fx.novel().brief()[0], 2)

    def test_an_unfenced_brief_is_reported_not_ignored(self):
        with NovelFixture() as fx:
            fx.write("state/brief.md", "Ch 2 — \"The Second Quarter\"\nevent    she files it\n")
            novel = fx.novel()
            self.assertEqual(novel.brief(), (None, ""))
            self.assertTrue(novel.brief_unreadable())
            self.assertIn("no brief this tool can read", cmd_readset.build(novel, 2))

    def test_the_shipped_placeholder_is_not_an_unreadable_brief(self):
        with NovelFixture() as fx:
            self.assertFalse(fx.novel().brief_unreadable())


class TestTheWatchRowDropsNothingSilently(unittest.TestCase):
    """Run #5's row filled its four slots by chapter 4 and a fifth recurring check vanished
    without a word (O23). The cap keeps it a pointer; the overflow keeps it honest."""

    FIVE = {"checks": ["house-style"], "notes": ["texture", "weasel", "filter-verb", "pacing"]}

    def test_past_the_cap_is_returned_not_dropped(self):
        with NovelFixture() as fx:
            for n in range(1, 4):
                fx.add_chapter(n, BODY)
            novel = fx.novel()
            overflow = []
            with mock.patch.object(cmd_readset.cmd_lint, "check_counts",
                                   return_value=self.FIVE):
                row, _notes = cmd_readset.watch_row(novel, 4, overflow)
        self.assertEqual(len(row), cmd_readset.WATCH_CAP)
        self.assertEqual(len(overflow), 1)
        self.assertTrue(row[0].startswith("house-style"), "a warn ranks first")
        self.assertIn("; warn", row[0])

    def test_each_item_names_the_last_chapter_it_fired_in(self):
        """A habit the last two chapters shed must not read like one they kept."""
        with NovelFixture() as fx:
            for n in range(1, 5):
                fx.add_chapter(n, BODY)
            novel = fx.novel()

            def counts(_novel, chapter):
                early = chapter.number <= 2
                return {"checks": [], "notes": ["weasel"] if early else []}

            with mock.patch.object(cmd_readset.cmd_lint, "check_counts", side_effect=counts):
                row, _notes = cmd_readset.watch_row(novel, 5)
        self.assertEqual(row, ["weasel (2 of last 4; last c2)"])

    def test_the_read_set_prints_the_overflow(self):
        with NovelFixture() as fx:
            for n in range(1, 4):
                fx.add_chapter(n, BODY)
            with mock.patch.object(cmd_readset.cmd_lint, "check_counts",
                                   return_value=self.FIVE):
                text = cmd_readset.build(fx.novel(), 4)
        self.assertIn("+1 past the cap of %d" % cmd_readset.WATCH_CAP, text)


class TestTheModuleListOnlyNamesOpenableFiles(unittest.TestCase):
    """`no-harem` is on by default and has no draft card, so the read-set named its `SKILL.md` -
    which the drafter's read guard refuses. Every default novel's Phase A hit a refusal."""

    def _novel_md(self):
        md = NOVEL_MD.replace("status: drafting",
                              "status: drafting\n\noptional:\n  no-harem: on")
        if re.search(r"(?m)^\s*romance:", md):
            return re.sub(r"(?m)^(\s*)romance:.*$", r"\1romance: subplot", md)
        return md.replace("\ngenre: fantasy", "\ngenre: fantasy\ncontent:\n  romance: subplot")

    def test_a_card_less_module_prints_a_note_not_a_body(self):
        with NovelFixture(novel_md=self._novel_md()) as fx:
            fx.add_chapter(1, BODY)
            block = _section(cmd_readset.build(fx.novel(), 1), "### active modules")
        lines = dict((ln.split()[0], ln) for ln in block.strip().splitlines() if ln.strip())
        self.assertIn("no-harem", lines)
        self.assertIn("audited at the gate", lines["no-harem"])
        self.assertIn("lead-interest", lines)
        self.assertIn("design-time only", lines["lead-interest"])
        self.assertNotIn("SKILL.md", block)

    def test_every_listed_path_is_one_the_drafter_may_open(self):
        """Judged by the guard itself, so the list and the guard cannot drift apart."""
        sys.path.insert(0, os.path.join(REPO, "scripts", "hooks"))
        import role_scope
        payload = {"agent_id": "t", "agent_type": "drafter"}
        with NovelFixture(novel_md=self._novel_md()) as fx:
            fx.add_chapter(1, BODY)
            text = cmd_readset.build(fx.novel(), 1)
        paths = re.findall(r"-> (\S+\.md)", text)
        self.assertTrue(paths)
        for rel in paths:
            self.assertIsNone(role_scope.verdict(payload, rel), rel)


class TestHealthAsksTheGuard(unittest.TestCase):

    def test_the_real_corpus_sends_the_drafter_nowhere_it_is_refused(self):
        rep = Report("t")
        cmd_health._drafter_reach(REPO, rep)
        self.assertEqual([f.message for f in rep.findings], [])

    def test_routing_a_module_to_its_body_is_a_defect(self):
        """The mutation that restores the 2026-09-24 bug must be caught by name."""
        rep = Report("t")
        with mock.patch.object(cmd_readset, "_drafter_entry", side_effect=lambda s, e: e):
            cmd_health._drafter_reach(REPO, rep)
        found = [f for f in rep.findings if f.check == "drafter-reach"]
        self.assertTrue(found)
        self.assertTrue(any("no-harem" in f.message for f in found))


class TestTheLedgerIsNotDueMidLoop(unittest.TestCase):
    """The block is written at step 5, after the gate. Pass 0 used to raise a defect for the
    chapter being gated, every chapter - one the gate could not fix and learned to ignore."""

    def _ledger(self, status):
        with NovelFixture() as fx:
            fx.add_chapter(1, BODY)
            if status != "drafted":
                _status(fx, 1, status)
            rep = cmd_lint.run(fx.novel(), [1])
        return [f for f in rep.findings if f.check == "ledger" and f.level == "defect"]

    def test_a_drafted_chapter_owes_no_block_yet(self):
        self.assertEqual(self._ledger("drafted"), [])

    def test_a_gated_chapter_owes_no_block_yet(self):
        self.assertEqual(self._ledger("gated"), [])

    def test_a_revised_chapter_without_its_block_is_still_a_defect(self):
        self.assertTrue(self._ledger("revised"))


class TestTheStepLinesAreAskedFor(unittest.TestCase):
    """`cand>`, `z4>` and `gav>` each prove a step ran, and each may say `none`. Run #5 shipped
    `cand>` on three blocks of five and `gav>` on none, and nothing asked."""

    def _steps(self, novel_md=NOVEL_MD, drop=()):
        with NovelFixture(novel_md=novel_md) as fx:
            fx.add_chapter(1, BODY)
            fx.add_ledger([1])
            for key in drop:
                _without(fx, key)
            rep = cmd_state.run(fx.novel())
        return [f for f in rep.findings if f.check == "ccs-steps"]

    def test_a_block_with_all_three_is_clean(self):
        self.assertEqual(self._steps(), [])

    def test_a_missing_line_is_named(self):
        found = self._steps(drop=("cand", "gav"))
        self.assertEqual(len(found), 1)
        self.assertEqual(found[0].level, "warn")
        self.assertIn("`cand>`", found[0].message)
        self.assertIn("`gav>`", found[0].message)
        self.assertNotIn("`z4>`", found[0].message)

    def test_cold_warmth_stands_the_giving_line_down(self):
        cold = NOVEL_MD.replace("warmth: measured", "warmth: cold")
        self.assertEqual(self._steps(novel_md=cold, drop=("gav",)), [])


class TestThreadCells(unittest.TestCase):

    def test_a_range_is_read_as_its_first_chapter(self):
        """`due: ch 20-25` had every digit joined into 2025 - a thread that never falls due."""
        from swlib import rules
        self.assertEqual(rules.first_int("ch 20-25"), "20")
        self.assertEqual(rules.first_int(""), "")

    def _arc_close(self, thr=None):
        md = NOVEL_MD.replace("arc_length: 25", "arc_length: 2")
        with NovelFixture(novel_md=md) as fx:
            for n in (1, 2):
                fx.add_chapter(n, BODY)
            fx.add_ledger([1, 2])
            if thr:
                with open(fx.path("state", "continuity.md"), encoding="utf-8") as fh:
                    text = fh.read()
                fx.write("state/continuity.md",
                         text.replace("thr> ~T01(permit-refused)", "thr> " + thr, 1))
            rep = cmd_state.run(fx.novel())
        return [f for f in rep.findings if "without paying" in f.message]

    def test_an_arc_that_paid_nothing_is_still_caught(self):
        """The control: without it the next test passes on a check that never ran."""
        self.assertTrue(self._arc_close())

    def test_a_th_numbered_payment_counts_at_the_arc_boundary(self):
        """The local `v(T\\d+)` survived O28's fix and read `vTH06` as no payment at all."""
        self.assertEqual(self._arc_close("vTH06(the debt)"), [])


class TestGivingIsNotSatisfiedBySilence(unittest.TestCase):

    def _gives(self, novel_md=NOVEL_MD):
        with NovelFixture(novel_md=novel_md) as fx:
            for n in (1, 2, 3):
                fx.add_chapter(n, BODY)
            fx.add_ledger([1, 2, 3])
            _without(fx, "gav")
            rep, _data = cmd_history.run(fx.novel())
        return [f for f in rep.findings if f.check == "history-gives"]

    def test_a_book_with_no_gav_line_anywhere_is_asked_about_it(self):
        found = self._gives()
        self.assertEqual(len(found), 1)
        self.assertIn("none of 3", found[0].message)

    def test_a_cold_book_is_not(self):
        self.assertEqual(self._gives(NOVEL_MD.replace("warmth: measured", "warmth: cold")), [])


class TestArcCastMatchesShortNames(unittest.TestCase):
    """`chg>` lines use the name a chapter uses, the matrix the full one. Equality called run
    #5's arc a one-hander with four other matrix characters on the page."""

    VOICES = ("# Cast voice matrix\n\n| character | intel | eq | artic | wit |\n"
              "|---|---|---|---|---|\n| Rin Ashe | 3 | 2 | 3 | dry |\n"
              "| Maro Venn | 2 | 4 | 2 | none |\n")

    def test_a_short_name_puts_its_row_on_the_page(self):
        with NovelFixture() as fx:
            fx.write("bible/cast/_voices.md", self.VOICES)
            fx.add_chapter(1, BODY)
            fx.add_ledger([1])
            rep = cmd_arc.run(fx.novel(), 1)
        lines = dict(rep.sections).get("cast rotation", [])
        self.assertTrue(any("on the page" in ln and "Rin Ashe" in ln for ln in lines), lines)


if __name__ == "__main__":
    unittest.main()
