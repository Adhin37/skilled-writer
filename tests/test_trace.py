"""`sw trace` - the report layer over the transcript reader.

`transcripts.py` has its own regressions; this covers what `cmd_trace` does on top, which is
where the judgement lives: which skills count as in play, what the finding-9 denominator is,
and the standing rule that this command measures a run and scores no chapter.

Run #4's T1 is why these exist. A defect in the measuring code made the headline number wrong
for three earlier benchmark runs, and nothing failed - a broken measurement does not look
broken, it looks like a result.
"""

import os
import sys
import unittest

from fixtures import REPO, NovelFixture

sys.path.insert(0, os.path.join(REPO, "scripts"))

from swlib import cmd_trace  # noqa: E402


class TestDuration(unittest.TestCase):

    def test_seconds_minutes_and_hours_are_all_legible(self):
        self.assertEqual(cmd_trace._hms(9), "9s")
        self.assertEqual(cmd_trace._hms(66), "1m 06s")
        self.assertEqual(cmd_trace._hms(3671), "1h 01m")

    def test_none_and_zero_do_not_raise(self):
        self.assertEqual(cmd_trace._hms(None), "0s")
        self.assertEqual(cmd_trace._hms(0), "0s")


class TestSkillRoster(unittest.TestCase):

    def test_the_roster_is_this_repo_s_skills(self):
        roster = cmd_trace._skill_roster(REPO)
        self.assertIn("write-chapter", roster)
        self.assertIn("revision-pass", roster)
        self.assertEqual(roster, sorted(roster))

    def test_a_repo_with_no_skills_directory_is_empty_not_an_error(self):
        self.assertEqual(cmd_trace._skill_roster(os.path.join(REPO, "scripts")), [])


class TestClassify(unittest.TestCase):
    """Off-for-this-novel and never-opened are different findings.

    Reporting a module that this novel's config switched off as a skill the run failed to open
    is a false positive on correct behaviour, and finding 9 is the number the benchmark runs
    are scored on.
    """

    def test_without_a_novel_nothing_is_off(self):
        roster = cmd_trace._skill_roster(REPO)
        in_play, off = cmd_trace._classify(roster, None, REPO)
        self.assertEqual(off, [])
        self.assertEqual(in_play, roster)

    def test_a_config_gated_module_is_off_rather_than_missed(self):
        roster = cmd_trace._skill_roster(REPO)
        with NovelFixture() as fx:
            in_play, off = cmd_trace._classify(roster, fx.novel(), REPO)
            self.assertTrue(off, "no skill was classified off for a default novel")
            self.assertEqual(set(in_play) & set(off), set())
            self.assertEqual(sorted(set(in_play) | set(off)), sorted(roster))

    def test_always_in_play_skills_are_never_classified_off(self):
        """`CLAUDE.md` section 3 lists these as always in play, for every novel."""
        roster = cmd_trace._skill_roster(REPO)
        with NovelFixture() as fx:
            _in_play, off = cmd_trace._classify(roster, fx.novel(), REPO)
        for core in ("write-chapter", "revision-pass", "bias-guard", "continuity-summary",
                     "voice-separation", "competence-map", "prose-quality"):
            self.assertNotIn(core, off, "%s must never be off for any novel" % core)


class TestSkillSection(unittest.TestCase):

    def _report(self, opened, novel=None):
        from swlib.report import Report
        rep, data = Report("t"), {}
        cmd_trace._skill_section(rep, REPO, novel, {"skills": dict(opened)}, data)
        return rep, data

    def test_a_skill_from_another_repo_does_not_inflate_the_denominator(self):
        """Bundled skills and slash commands arrive through the same `Skill` tool."""
        _rep, data = self._report({"write-chapter": 1, "pdf": 3, "mermaid": 2})
        self.assertIn("write-chapter", data["skills"]["opened_here"])
        self.assertEqual(sorted(data["skills"]["opened_elsewhere"]), ["mermaid", "pdf"])

    def test_a_run_that_opened_nothing_raises_no_finding_9(self):
        """Only a run that opened skills at all is evidence about which it skipped.

        Otherwise a trace over sessions that never wrote a chapter reports every skill as
        missing, which is how an unscoped trace produces a number that looks alarming and
        means nothing.
        """
        rep, _data = self._report({})
        self.assertEqual([f for f in rep.findings if f.level == "warn"], [])

    def test_a_run_that_skipped_an_always_in_play_skill_is_a_finding(self):
        rep, data = self._report({"write-chapter": 1})
        self.assertIn("bias-guard", data["skills"]["in_play_never_opened"])
        self.assertTrue([f for f in rep.findings
                         if f.level == "warn" and "never" in f.message])

    def test_a_missing_skills_directory_warns_rather_than_raising(self):
        from swlib.report import Report
        rep, data = Report("t"), {}
        cmd_trace._skill_section(rep, os.path.join(REPO, "scripts"), None,
                                 {"skills": {}}, data)
        self.assertTrue([f for f in rep.findings if f.level == "warn"])


class TestTraceScoresNoChapter(unittest.TestCase):
    """`trace` measures a run. It says nothing about whether any chapter is any good."""

    def test_no_finding_names_a_chapter_quality_check(self):
        rep, _data = TestSkillSection()._report({"write-chapter": 1})
        text = " ".join(str(f.message) for f in rep.findings)
        for word in ("speech-share", "house-style", "delivers", "wordcount"):
            self.assertNotIn(word, text)

    def test_it_raises_nothing_above_a_warn(self):
        rep, _data = TestSkillSection()._report({"write-chapter": 1})
        self.assertEqual([f for f in rep.findings if f.level == "defect"], [])


if __name__ == "__main__":
    unittest.main()
