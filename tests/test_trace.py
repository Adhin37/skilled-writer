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


def _agent(agent_type, opened):
    """A subagent transcript as `trace` sees it, without a file behind it."""
    from swlib import transcripts
    s = transcripts.Session("/cfg/projects/-r/s1/subagents/agent-%s.jsonl" % agent_type, "/cfg")
    s.agent_type = agent_type
    s.opened = [("2026-09-05T10:00:00.000Z", tool, path) for tool, path in opened]
    return s


class TestRouting(unittest.TestCase):
    """What each agent opened that its read guard refuses, judged by the guard's own `verdict`.

    The guard sees `Read`; the harness tells agents to prefer `cat`. So a denied path in a shell
    command is the road nothing else watches - a warn - and a denied `Read` was refused as it
    happened, which means a card misrouted the agent - a note.
    """

    def _routing(self, sessions):
        from swlib.report import Report
        rep, data = Report("t"), {}
        cmd_trace._routing_section(rep, REPO, sessions, data)
        return rep, data

    def test_a_bash_read_of_another_role_s_card_is_a_warn(self):
        rep, data = self._routing([_agent("drafter", [
            ("Bash", "roles/gate/prose-quality.audit-card.md")])])
        warns = [f for f in rep.findings if f.check == "trace-routing" and f.level == "warn"]
        self.assertEqual(len(warns), 1)
        self.assertIn("drafter", warns[0].message)
        self.assertEqual(data["routing"][0]["tool"], "Bash")

    def test_a_refused_read_is_a_note(self):
        rep, _data = self._routing([_agent("gate", [
            ("Read", "/work/repo/roles/draft/story-craft.draft-card.md")])])
        levels = [f.level for f in rep.findings if f.check == "trace-routing"]
        self.assertEqual(levels, ["note"])

    def test_an_agent_in_its_own_lane_raises_nothing(self):
        rep, data = self._routing([_agent("gate", [
            ("Read", "roles/gate/prose-quality.audit-card.md"),
            ("Bash", "roles/shared/voice-separation.mirror-clause.md")])])
        self.assertEqual([f for f in rep.findings if f.check == "trace-routing"], [])
        self.assertEqual(data["routing"], [])

    def test_the_main_session_is_never_judged(self):
        """The coordinator reads everything, by design."""
        from swlib import transcripts
        main = transcripts.Session("/cfg/projects/-r/s1.jsonl", "/cfg")
        main.opened = [("t", "Bash", "roles/gate/prose-quality.audit-card.md")]
        rep, _data = self._routing([main])
        self.assertEqual([f for f in rep.findings if f.check == "trace-routing"], [])


class TestSkillsARoleRunCannotOpen(unittest.TestCase):
    """A preloaded body arrives without a tool call, and a skill with no role file has nothing
    a drafter or gate may open. Reporting either as missed teaches the reader to skip the
    section."""

    def test_preloaded_and_card_less_skills_are_not_counted_as_missed(self):
        _rep, data = TestSkillSection()._report({"bias-guard": 1})
        never = data["skills"]["in_play_never_opened"]
        for quiet in ("write-chapter", "revision-pass", "continuity-summary"):
            self.assertIn(quiet, data["skills"]["preloaded"])
            self.assertNotIn(quiet, never)

    def test_a_narrowed_run_raises_no_never_opened_warn(self):
        from swlib.report import Report
        rep, data = Report("t"), {}
        cmd_trace._skill_section(rep, REPO, None, {"skills": {"bias-guard": 1}}, data,
                                 narrowed=True)
        self.assertEqual([f for f in rep.findings if f.level == "warn"], [])
