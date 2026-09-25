"""The transcript reader, written as regressions.

Each case names the wrong behaviour it pins down. These measurements are trusted by a report
that nobody cross-checks by hand, and the headline defect - one API response counted as seven -
is invisible in the output: it does not look like a broken parser, it looks like an expensive
run.
"""

import json
import os
import shutil
import tempfile
import unittest

from fixtures import REPO  # noqa: F401  (puts scripts/ on sys.path)

from swlib import transcripts
from swlib.rates import Rates


def row(**kw):
    base = {"type": "assistant", "timestamp": "2026-09-05T17:00:00.000Z",
            "cwd": "/work/repo", "requestId": "req_1", "uuid": "u1",
            "message": {"id": "msg_1", "model": "claude-sonnet-5", "content": [],
                        "usage": {"input_tokens": 0, "cache_creation_input_tokens": 0,
                                  "cache_read_input_tokens": 0, "output_tokens": 0}}}
    msg = kw.pop("message", None)
    base.update(kw)
    if msg:
        base["message"].update(msg)
    return base


def usage(inp=0, read=0, w5=0, w1=0, out=0):
    return {"input_tokens": inp, "cache_read_input_tokens": read,
            "cache_creation_input_tokens": w5 + w1, "output_tokens": out,
            "cache_creation": {"ephemeral_5m_input_tokens": w5,
                               "ephemeral_1h_input_tokens": w1}}


class Root(object):
    """A throwaway Claude Code config root."""

    def __enter__(self):
        self.dir = tempfile.mkdtemp(prefix="sw-tx-")
        return self

    def __exit__(self, *exc):
        shutil.rmtree(self.dir, ignore_errors=True)
        return False

    def write(self, relpath, rows):
        full = os.path.join(self.dir, *relpath.split("/"))
        parent = os.path.dirname(full)
        if not os.path.isdir(parent):
            os.makedirs(parent)
        with open(full, "w", encoding="utf-8", newline="\n") as fh:
            for r in rows:
                fh.write(json.dumps(r) + "\n")
        return full


class TestResponseGrouping(unittest.TestCase):

    def test_one_response_written_as_seven_rows_is_one_response(self):
        """The defect that put $28.39 in docs/benchmark.md.

        Claude Code writes one row per content block and repeats `usage` verbatim on each, so
        summing rows billed a single request up to seven times over.
        """
        u = usage(inp=2, read=28289, w5=24740, out=3688)
        rows = [row(apiBlockIndex=i, message={"usage": u}) for i in range(7)]
        with Root() as root:
            root.write("projects/-work-repo/s1.jsonl", rows)
            sess = transcripts.sessions_for("/work/repo", root.dir)
        self.assertEqual(len(sess), 1)
        self.assertEqual(len(sess[0].responses), 1, "seven rows are one API request")
        t = sess[0].totals()
        self.assertEqual(t["cache_read_input_tokens"], 28289)
        self.assertEqual(t["cache_creation_input_tokens"], 24740)
        self.assertEqual(sess[0].naive_totals["cache_read_input_tokens"], 28289 * 7,
                         "the naive row-sum is kept, so the overcount stays visible")

    def test_output_tokens_are_a_streaming_counter_not_a_running_total(self):
        """Rows carrying 5, 5, 289 mean 289 - not 299, and not 5.

        Taking the first row's value under-reports output by more than an order of magnitude;
        adding them up over-reports it.
        """
        rows = [row(apiBlockIndex=0, message={"usage": usage(out=5)}),
                row(apiBlockIndex=1, message={"usage": usage(out=5)}),
                row(apiBlockIndex=2, message={"usage": usage(out=289)})]
        with Root() as root:
            root.write("projects/-work-repo/s1.jsonl", rows)
            sess = transcripts.sessions_for("/work/repo", root.dir)
        self.assertEqual(sess[0].totals()["output_tokens"], 289)

    def test_separate_requests_are_separate_responses(self):
        rows = [row(requestId="req_1", message={"id": "msg_1", "usage": usage(read=10)}),
                row(requestId="req_2", message={"id": "msg_2", "usage": usage(read=20)})]
        with Root() as root:
            root.write("projects/-work-repo/s1.jsonl", rows)
            sess = transcripts.sessions_for("/work/repo", root.dir)
        self.assertEqual(len(sess[0].responses), 2)
        self.assertEqual(sess[0].totals()["cache_read_input_tokens"], 30)

    def test_synthetic_rows_contribute_nothing(self):
        """`<synthetic>` messages are generated locally and were never billed."""
        rows = [row(message={"model": "<synthetic>", "usage": usage(read=999999)})]
        with Root() as root:
            root.write("projects/-work-repo/s1.jsonl", rows)
            sess = transcripts.sessions_for("/work/repo", root.dir)
        self.assertEqual(sess[0].totals()["cache_read_input_tokens"], 0)

    def test_cache_write_ttls_are_split_and_a_missing_split_falls_back_to_5m(self):
        """The two TTLs are priced 1.25x and 2x; blending them misprices the write."""
        with Root() as root:
            root.write("projects/-work-repo/s1.jsonl", [
                row(requestId="a", message={"id": "a", "usage": usage(w5=100, w1=200)})])
            sess = transcripts.sessions_for("/work/repo", root.dir)
        t = sess[0].totals()
        self.assertEqual((t["cache_write_5m"], t["cache_write_1h"]), (100, 200))

        old = {"input_tokens": 0, "cache_creation_input_tokens": 500,
               "cache_read_input_tokens": 0, "output_tokens": 0}
        with Root() as root:
            root.write("projects/-work-repo/s1.jsonl",
                       [row(requestId="b", message={"id": "b", "usage": old})])
            sess = transcripts.sessions_for("/work/repo", root.dir)
        t = sess[0].totals()
        self.assertEqual((t["cache_write_5m"], t["cache_write_1h"]), (500, 0),
                         "a transcript with no TTL split is priced at the 5-minute rate")


class TestDiscovery(unittest.TestCase):

    def test_a_session_is_matched_by_its_cwd_not_by_the_directory_name(self):
        """The escaped project-directory name differs by platform and is never reconstructed."""
        with Root() as root:
            root.write("projects/completely-unrelated-name/s1.jsonl",
                       [row(cwd="/work/repo/novels/book")])
            sess = transcripts.sessions_for("/work/repo", root.dir)
        self.assertEqual(len(sess), 1, "a cwd *under* the repo counts; run #1 had four of them")

    def test_a_session_outside_the_repo_is_not_matched(self):
        with Root() as root:
            root.write("projects/-other/s1.jsonl", [row(cwd="/somewhere/else")])
            self.assertEqual(transcripts.sessions_for("/work/repo", root.dir), [])

    def test_subagent_files_are_found_and_labelled(self):
        with Root() as root:
            root.write("projects/-work-repo/s1.jsonl", [row()])
            root.write("projects/-work-repo/s1/subagents/agent-abc.jsonl", [row()])
            sess = transcripts.sessions_for("/work/repo", root.dir)
        kinds = sorted(s.is_subagent for s in sess)
        self.assertEqual(kinds, [False, True],
                         "subagent usage is not in the parent transcript; missing these "
                         "reports a multi-agent run as costing nothing")

    def test_subagent_usage_reaches_the_totals(self):
        """Finding the file is not the measurement; the tokens have to land in the sum.

        The parent writes its sidechain rows with empty usage, so a multi-agent run's whole cost
        sits in the per-agent files. Discovery without aggregation prices a split pipeline at
        whatever the coordinator alone spent, which is the one reading that would make moving
        work into subagents look free.
        """
        with Root() as root:
            root.write("projects/-work-repo/s1.jsonl", [
                row(requestId="p", message={"id": "p", "usage": usage(read=100, out=10)}),
                row(requestId="side", isSidechain=True,
                    message={"id": "side", "usage": usage()})])
            root.write("projects/-work-repo/s1/subagents/agent-abc.jsonl",
                       [row(requestId="a", message={"id": "a", "usage": usage(read=900, out=90)})])
            agg = transcripts.aggregate(transcripts.sessions_for("/work/repo", root.dir))
        self.assertEqual(agg["sessions"], 2)
        self.assertEqual((agg["cache_read_input_tokens"], agg["output_tokens"]), (1000, 100),
                         "the subagent's 900/90 is nine tenths of this run and is only in its "
                         "own file")

    def test_a_missing_root_is_not_an_error(self):
        self.assertEqual(transcripts.sessions_for("/work/repo", "/nope/not/here"), [])

    def test_a_half_written_last_line_is_skipped_not_fatal(self):
        """A live session's final line is routinely truncated mid-write."""
        with Root() as root:
            path = root.write("projects/-work-repo/s1.jsonl",
                              [row(requestId="a", message={"id": "a", "usage": usage(read=7)})])
            with open(path, "a", encoding="utf-8") as fh:
                fh.write('{"type": "assistant", "message": {"usa')
            sess = transcripts.sessions_for("/work/repo", root.dir)
        self.assertEqual(sess[0].totals()["cache_read_input_tokens"], 7)


class TestToolAndSkillDetection(unittest.TestCase):

    def _skills(self, path):
        with Root() as root:
            root.write("projects/-work-repo/s1.jsonl", [row(message={"content": [
                {"type": "tool_use", "name": "Read", "input": {"file_path": path}}]})])
            return transcripts.sessions_for("/work/repo", root.dir)[0].skills

    def test_a_windows_path_is_still_a_skill_load(self):
        """Transcripts store absolute paths from whatever machine wrote them."""
        # json.loads turns the file's escaped "C:\\Users\\..." back into single backslashes,
        # so this is the string the reader actually receives.
        self.assertIn("bias-guard",
                      self._skills(r"C:\Users\x\repo\.claude\skills\bias-guard\SKILL.md"))

    def test_a_posix_path_under_a_different_root_is_still_a_skill_load(self):
        self.assertIn("voice-separation",
                      self._skills("/elsewhere/x/.claude/skills/voice-separation/SKILL.md"))

    def test_a_reference_counts_as_opening_its_skill(self):
        skills = self._skills("/r/.claude/skills/power-scaling/references/draft-card.md")
        self.assertIn("power-scaling", skills)

    def test_a_role_tree_file_counts_as_opening_its_owner(self):
        """In `.claude/roles/` the owner is the filename prefix, not a directory."""
        self.assertIn("power-scaling",
                      self._skills("/r/.claude/roles/draft/power-scaling.draft-card.md"))
        self.assertIn("voice-separation",
                      self._skills("/r/.claude/roles/shared/voice-separation.mirror-clause.md"))

    def test_the_old_layout_still_counts_after_the_split(self):
        """These regexes read transcripts, and a transcript outlives the layout it recorded.

        A scanner taught only the current tree would report a drop in skill opens on the day of
        a refactor - a measurement artifact indistinguishable from a model that stopped reading.
        """
        self.assertIn("power-scaling",
                      self._skills("/r/.claude/skills/power-scaling/references/draft-card.md"))
        self.assertIn("power-scaling",
                      self._skills("/r/.claude/roles/draft/power-scaling.draft-card.md"))

    def test_the_root_layout_counts(self):
        """The tree at the repo root, which is where the role folders live now."""
        self.assertIn("power-scaling",
                      self._skills("/r/roles/draft/power-scaling.draft-card.md"))
        self.assertIn("voice-separation",
                      self._skills("/r/roles/shared/voice-separation.mirror-clause.md"))

    def test_a_word_ending_in_roles_is_not_a_role_file(self):
        """`ROLE_IN_TEXT` lost its `.claude/` anchor when the tree moved to the root, so the
        thing that stops it matching inside a longer word is now a lookbehind rather than a
        literal prefix. Without it `controles/draft/x.y.md` reads as an open.
        """
        self.assertEqual(self._skills("/r/controles/draft/power-scaling.draft-card.md"), {})

    def test_the_scanner_knows_every_layout_kb_does(self):
        """This module is standard-library-only and imports nothing from `swlib`, because it
        reads transcripts from outside the repo. That independence is why the two copies of the
        layout list can drift, and why the join between them has to be a test.
        """
        from swlib import kb
        self.assertEqual(set(transcripts.ROLE_DIRS), set(kb.ROLES_DIRS))

    def test_the_skill_tool_counts(self):
        with Root() as root:
            root.write("projects/-work-repo/s1.jsonl", [row(message={"content": [
                {"type": "tool_use", "name": "Skill", "input": {"skill": "mtl-detox"}}]})])
            sess = transcripts.sessions_for("/work/repo", root.dir)
        self.assertIn("mtl-detox", sess[0].skills)

    def test_a_path_that_merely_mentions_skills_is_not_a_skill_load(self):
        self.assertEqual(self._skills("/r/docs/skills-notes.md"), {})

    def _bash(self, command):
        with Root() as root:
            root.write("projects/-work-repo/s1.jsonl", [row(message={"content": [
                {"type": "tool_use", "name": "Bash", "input": {"command": command}}]})])
            return transcripts.sessions_for("/work/repo", root.dir)[0].skills

    def test_a_skill_read_with_bash_is_a_skill_load(self):
        """Benchmark run #4, T1.

        A model told to prefer shell reads opens a skill with `cat`, and the path never reaches
        `file_path`. `trace` reported "0 of 44 skills opened" for a run that opened thirteen, so
        the finding-9 measurement was silently a measurement of which tool the model happened to
        read with.
        """
        self.assertIn("story-craft",
                      self._bash("cat .claude/skills/story-craft/references/draft-card.md"))

    def test_several_skills_in_one_command_all_count(self):
        skills = self._bash("sed -n 1,40p .claude/skills/bias-guard/SKILL.md "
                            ".claude/skills/prose-quality/references/audit-card.md")
        self.assertIn("bias-guard", skills)
        self.assertIn("prose-quality", skills)

    def test_the_same_file_twice_in_one_command_counts_once(self):
        skills = self._bash("cat .claude/skills/mtl-detox/SKILL.md "
                            ".claude/skills/mtl-detox/SKILL.md")
        self.assertEqual(1, skills["mtl-detox"])

    def test_both_trees_in_one_command_count(self):
        skills = self._bash("cat .claude/skills/write-chapter/SKILL.md "
                            ".claude/roles/draft/conflict-engine.draft-card.md")
        self.assertIn("write-chapter", skills)
        self.assertIn("conflict-engine", skills)

    def test_a_command_naming_no_skill_is_not_a_skill_load(self):
        self.assertEqual(self._bash("ls docs/ && grep -r skills README.md"), {})


class TestChapterAttribution(unittest.TestCase):

    def test_a_chapter_is_anchored_on_its_last_write_not_its_first(self):
        """A revision rewrites the file; anchoring on the first write pushes that cost into
        the next chapter's bucket."""
        def write_row(ts, ch):
            return row(timestamp=ts, requestId="r" + ts, message={
                "id": "m" + ts, "usage": usage(out=1), "content": [
                    {"type": "tool_use", "name": "Write",
                     "input": {"file_path": "/work/repo/novels/b/chapters/%04d-x.md" % ch}}]})
        rows = [
            row(timestamp="2026-09-05T10:00:00.000Z", requestId="a", message={"id": "a", "usage": usage(read=100)}),
            write_row("2026-09-05T10:01:00.000Z", 1),
            row(timestamp="2026-09-05T10:02:00.000Z", requestId="b", message={"id": "b", "usage": usage(read=200)}),
            write_row("2026-09-05T10:03:00.000Z", 1),      # the revision
            row(timestamp="2026-09-05T10:04:00.000Z", requestId="c", message={"id": "c", "usage": usage(read=400)}),
            write_row("2026-09-05T10:05:00.000Z", 2),
        ]
        with Root() as root:
            root.write("projects/-work-repo/s1.jsonl", rows)
            sess = transcripts.sessions_for("/work/repo", root.dir)
        buckets = transcripts.by_chapter(sess)
        self.assertEqual([b["chapter"] for b in buckets], [1, 2])
        self.assertEqual(buckets[0]["cache_read_input_tokens"], 300,
                         "both pre-revision requests belong to chapter 1")
        self.assertEqual(buckets[1]["cache_read_input_tokens"], 400)
        self.assertEqual(buckets[0]["slug"], "b")

    def test_buckets_keep_their_models_so_a_mixed_run_can_be_priced(self):
        rows = [
            row(timestamp="2026-09-05T10:00:00.000Z", requestId="a",
                message={"id": "a", "model": "claude-opus-5", "usage": usage(out=100)}),
            row(timestamp="2026-09-05T10:01:00.000Z", requestId="w", message={
                "id": "w", "usage": usage(), "content": [
                    {"type": "tool_use", "name": "Write",
                     "input": {"file_path": "/work/repo/novels/b/chapters/0001-x.md"}}]}),
        ]
        with Root() as root:
            root.write("projects/-work-repo/s1.jsonl", rows)
            sess = transcripts.sessions_for("/work/repo", root.dir)
        b = transcripts.by_chapter(sess)[0]
        self.assertIn("claude-opus-5", b["by_model"])


class TestRates(unittest.TestCase):

    def test_the_published_table_reproduces_benchmark_run_one(self):
        """The corrected figures for the run docs/benchmark.md reports as $28.39."""
        cost = Rates().cost("claude-sonnet-5", input_tokens=154, cache_write_5m=807552,
                            cache_read=25450030, output_tokens=85464)
        self.assertAlmostEqual(cost, 7.96, places=2)

    def test_an_unpriced_model_costs_zero_and_is_recorded(self):
        r = Rates()
        self.assertEqual(r.cost("claude-from-the-future", output_tokens=10 ** 9), 0.0)
        self.assertIn("claude-from-the-future", r.unpriced)

    def test_a_rates_file_overrides_the_table(self):
        fd, path = tempfile.mkstemp(suffix=".json")
        os.close(fd)
        try:
            with open(path, "w", encoding="utf-8") as fh:
                json.dump({"claude-sonnet-5": {"input": 1.0, "output": 1.0, "cache_read": 1.0}}, fh)
            r = Rates.load(path)
            self.assertAlmostEqual(r.cost("claude-sonnet-5", output_tokens=1000000), 1.0)
        finally:
            os.unlink(path)


if __name__ == "__main__":
    unittest.main()


class TestRunScoping(unittest.TestCase):
    """Benchmark run #2, F5. Two ways the same measurement went wrong.

    `sessions_for` matched every session that ever ran in the repo — on the machine that produced
    run #2 that was 22 sessions and $225 of toolkit development. And `by_chapter` guarded the
    tail (`if idx >= len(buckets): break`) but not the head, so every response earlier than
    chapter 1's last write fell into chapter 1's bucket unconditionally.
    """

    def _write(self, root, name, entries):
        rows = []
        for stamp, req, chapter in entries:
            rows.append(row(timestamp=stamp, requestId=req,
                            message={"id": "m_" + req, "usage": usage(read=1000, out=10)}))
            if chapter:
                rows.append(row(timestamp=stamp, requestId=req, type="assistant",
                                message={"id": "m_" + req,
                                         "content": [{"type": "tool_use", "name": "Write",
                                                      "input": {"file_path":
                                                                "/work/repo/novels/b/chapters/"
                                                                "%04d-x.md" % chapter}}],
                                         "usage": usage()}))
        return root.write("projects/p/%s.jsonl" % name, rows)

    def test_since_excludes_an_earlier_session(self):
        with Root() as rt:
            self._write(rt, "old", [("2026-09-01T10:00:00.000Z", "a", None)])
            self._write(rt, "new", [("2026-09-09T10:00:00.000Z", "b", 1)])
            all_s = transcripts.sessions_for("/work/repo", rt.dir)
            scoped = transcripts.sessions_for("/work/repo", rt.dir, since="2026-09-09")
            self.assertEqual(len(all_s), 2)
            self.assertEqual(len(scoped), 1)

    def test_responses_before_since_are_not_billed_to_chapter_one(self):
        """Was: chapter 1's bucket absorbed every response that preceded it, from any run."""
        with Root() as rt:
            self._write(rt, "s", [("2026-09-09T09:00:00.000Z", "old", None),
                                  ("2026-09-09T12:00:00.000Z", "new", 1)])
            sessions = transcripts.sessions_for("/work/repo", rt.dir)
            buckets = transcripts.by_chapter(sessions, since="2026-09-09T11:00")
            pre = [b for b in buckets if b["chapter"] == 0]
            ch1 = [b for b in buckets if b["chapter"] == 1]
            self.assertEqual(len(pre), 1)
            self.assertEqual(pre[0]["responses"], 1)
            self.assertEqual(ch1[0]["responses"], 1)

    def test_without_since_the_first_chapter_still_absorbs_its_own_setup(self):
        """The head guard must not strip a chapter of the setup it is documented to absorb."""
        with Root() as rt:
            self._write(rt, "s", [("2026-09-09T09:00:00.000Z", "setup", None),
                                  ("2026-09-09T12:00:00.000Z", "new", 1)])
            sessions = transcripts.sessions_for("/work/repo", rt.dir)
            buckets = transcripts.by_chapter(sessions)
            self.assertEqual([b["chapter"] for b in buckets], [1])
            self.assertEqual(buckets[0]["responses"], 2)


class TestCardCounting(unittest.TestCase):
    """Runs #4 and #5 both made cards-opened the headline and both counted them by hand.

    A hand-count is a measurement that gets done once and estimated forever after, and the number
    it produces is the one the benchmark argues from. It is counted here instead, and - the whole
    point of the separation - it is counted per *phase*: Phase A spends draft cards and Phase C
    audit cards, so a run with one and not the other is a phase that did not happen.
    """

    def _cards(self, path):
        with Root() as root:
            root.write("projects/-work-repo/s1.jsonl", [row(message={"content": [
                {"type": "tool_use", "name": "Read", "input": {"file_path": path}}]})])
            return transcripts.sessions_for("/work/repo", root.dir)[0].card_opens

    def test_a_draft_card_is_recorded_with_its_phase(self):
        cards = self._cards("/r/.claude/skills/story-craft/references/draft-card.md")
        self.assertEqual([(c[1], c[2]) for c in cards], [("story-craft", "draft")])

    def test_an_audit_card_is_recorded_with_its_phase(self):
        cards = self._cards("/r/.claude/skills/bias-guard/references/audit-card.md")
        self.assertEqual([(c[1], c[2]) for c in cards], [("bias-guard", "audit")])

    def test_a_reference_that_is_not_a_card_is_not_counted(self):
        self.assertEqual(self._cards("/r/.claude/skills/prose-quality/references/"
                                     "ai-default-tells.md"), [])
        self.assertEqual(self._cards("/r/.claude/skills/revision-pass/SKILL.md"), [])

    def test_a_role_tree_card_is_recorded_with_its_phase(self):
        """The stem after the first dot is the card, and it carries no `references/` to key on."""
        self.assertEqual(
            [(c[1], c[2]) for c in self._cards("/r/.claude/roles/gate/bias-guard.audit-card.md")],
            [("bias-guard", "audit")])
        self.assertEqual(
            [(c[1], c[2]) for c in
             self._cards("/r/.claude/roles/draft/story-craft.draft-card.md")],
            [("story-craft", "draft")])
        self.assertEqual(
            self._cards("/r/.claude/roles/shared/prose-quality.ai-default-tells.md"), [])

    def test_a_card_opened_with_bash_counts(self):
        """The same hole run #4's T1 found for skills: a shell read never reaches `file_path`."""
        with Root() as root:
            root.write("projects/-work-repo/s1.jsonl", [row(message={"content": [
                {"type": "tool_use", "name": "Bash", "input": {
                    "command": "cat .claude/skills/conflict-engine/references/draft-card.md"}}]})])
            cards = transcripts.sessions_for("/work/repo", root.dir)[0].card_opens
        self.assertEqual([(c[1], c[2]) for c in cards], [("conflict-engine", "draft")])

    def test_aggregate_totals_and_names_them(self):
        with Root() as root:
            root.write("projects/-work-repo/s1.jsonl", [row(message={"content": [
                {"type": "tool_use", "name": "Read", "input": {"file_path": p}}
                for p in (".claude/skills/scene-craft/references/draft-card.md",
                          ".claude/skills/scene-craft/references/audit-card.md",
                          ".claude/skills/bias-guard/references/audit-card.md")]})])
            agg = transcripts.aggregate(transcripts.sessions_for("/work/repo", root.dir))
        self.assertEqual(agg["cards"], {"draft": 1, "audit": 2})
        self.assertEqual(agg["card_files"]["scene-craft (draft)"], 1)
        self.assertEqual(agg["card_files"]["bias-guard (audit)"], 1)

    def test_cards_bucket_against_the_chapter_they_preceded(self):
        def card_row(ts, skill, kind):
            return row(timestamp=ts, requestId="c" + ts, message={
                "id": "c" + ts, "usage": usage(), "content": [
                    {"type": "tool_use", "name": "Read", "input": {
                        "file_path": "/r/.claude/skills/%s/references/%s-card.md"
                                     % (skill, kind)}}]})

        def write_row(ts, ch):
            return row(timestamp=ts, requestId="w" + ts, message={
                "id": "w" + ts, "usage": usage(), "content": [
                    {"type": "tool_use", "name": "Write",
                     "input": {"file_path": "/work/repo/novels/b/chapters/%04d-x.md" % ch}}]})

        rows = [card_row("2026-09-05T10:00:00.000Z", "story-craft", "draft"),
                card_row("2026-09-05T10:01:00.000Z", "bias-guard", "audit"),
                write_row("2026-09-05T10:02:00.000Z", 1),
                card_row("2026-09-05T10:03:00.000Z", "scene-craft", "draft"),
                write_row("2026-09-05T10:04:00.000Z", 2)]
        with Root() as root:
            root.write("projects/-work-repo/s1.jsonl", rows)
            buckets = transcripts.by_chapter(transcripts.sessions_for("/work/repo", root.dir))
        self.assertEqual([(b["chapter"], b["draft_cards"], b["audit_cards"]) for b in buckets],
                         [(1, 1, 1), (2, 1, 0)])

    def test_cards_before_since_land_in_the_pre_bucket_not_in_chapter_one(self):
        """The same head guard responses got in run #2's F5, for the same reason."""
        rows = [row(timestamp="2026-09-05T09:00:00.000Z", requestId="old", message={
                    "id": "old", "usage": usage(), "content": [
                        {"type": "tool_use", "name": "Read", "input": {
                            "file_path": "/r/.claude/skills/mtl-detox/references/"
                                         "audit-card.md"}}]}),
                row(timestamp="2026-09-05T12:00:00.000Z", requestId="w", message={
                    "id": "w", "usage": usage(), "content": [
                        {"type": "tool_use", "name": "Write", "input": {
                            "file_path": "/work/repo/novels/b/chapters/0001-x.md"}}]})]
        with Root() as root:
            root.write("projects/-work-repo/s1.jsonl", rows)
            sess = transcripts.sessions_for("/work/repo", root.dir)
            buckets = transcripts.by_chapter(sess, since="2026-09-05T11:00")
        pre = [b for b in buckets if b["chapter"] == 0]
        self.assertEqual(len(pre), 1, "a card opened before the window is still reported")
        self.assertEqual(pre[0]["audit_cards"], 1)
        self.assertEqual([b["audit_cards"] for b in buckets if b["chapter"] == 1], [0])


class TestRolePipeline(unittest.TestCase):
    """A run that is several agents, measured as several agents.

    Until 2026-09-24 `trace` pooled a drafter, its gate and the coordinator into one set of
    totals and billed each response by chapter-file write times. Once the work split, the
    drafter's state write came after the gate and was billed to the NEXT chapter, and a gate
    that edited nothing left no anchor at all. The harness writes a label beside every subagent
    transcript; these pin reading it - and reading nothing else, because the module reads no
    prompt text.
    """

    def _meta(self, root, relpath, **meta):
        full = os.path.join(root.dir, *relpath.split("/"))
        with open(full[:-len(".jsonl")] + ".meta.json", "w", encoding="utf-8") as fh:
            json.dump(meta, fh)

    def _resp(self, ts, rid, read=0, content=None):
        return row(timestamp=ts, requestId=rid, message={
            "id": rid, "usage": usage(read=read), "content": content or []})

    def _write(self, ts, rid, ch):
        return self._resp(ts, rid, content=[{"type": "tool_use", "name": "Write", "input": {
            "file_path": "/work/repo/novels/b/chapters/%04d-x.md" % ch}}])

    def test_the_label_names_the_role_and_the_chapter(self):
        with Root() as root:
            root.write("projects/-work-repo/s1.jsonl", [row()])
            rel = "projects/-work-repo/s1/subagents/agent-g1.jsonl"
            root.write(rel, [row()])
            self._meta(root, rel, agentType="gate", description="gate ch 3", spawnDepth=1)
            sess = transcripts.sessions_for("/work/repo", root.dir)
        by = dict((s.is_subagent, s) for s in sess)
        self.assertEqual(by[False].role, "main")
        self.assertEqual(by[True].role, "gate")
        self.assertEqual(by[True].chapter_hint, 3)
        self.assertEqual(by[True].spawn_depth, 1)

    def test_a_subagent_with_no_label_is_still_a_subagent(self):
        """Transcripts written before the harness wrote meta files look like this."""
        with Root() as root:
            root.write("projects/-work-repo/s1/subagents/agent-x.jsonl", [row()])
            sess = transcripts.sessions_for("/work/repo", root.dir)
        self.assertEqual((sess[0].role, sess[0].chapter_hint), ("subagent", None))

    def test_a_grandchild_is_found(self):
        """A gate spawned by a drafter sits a level deeper; a fixed-depth glob dropped its cost."""
        with Root() as root:
            root.write("projects/-work-repo/s1/subagents/agent-a/subagents/agent-b.jsonl",
                       [self._resp("2026-09-05T10:00:00.000Z", "b", read=70)])
            agg = transcripts.aggregate(transcripts.sessions_for("/work/repo", root.dir))
        self.assertEqual(agg["cache_read_input_tokens"], 70)

    def test_a_labelled_agent_is_billed_to_its_chapter_whole(self):
        """The gate edits nothing and runs after the chapter's last write: under the anchor rule
        its whole cost left the chapter it gated."""
        with Root() as root:
            root.write("projects/-work-repo/s1.jsonl", [])
            d = "projects/-work-repo/s1/subagents/"
            root.write(d + "agent-d.jsonl", [
                self._resp("2026-09-05T10:00:00.000Z", "d1", read=100),
                self._write("2026-09-05T10:01:00.000Z", "d2", 1),
                self._resp("2026-09-05T10:05:00.000Z", "d3", read=300)])   # the state write
            self._meta(root, d + "agent-d.jsonl", agentType="drafter", description="draft ch 1")
            root.write(d + "agent-g.jsonl", [
                self._resp("2026-09-05T10:03:00.000Z", "g1", read=500)])
            self._meta(root, d + "agent-g.jsonl", agentType="gate", description="gate ch 1")
            buckets = transcripts.by_chapter(transcripts.sessions_for("/work/repo", root.dir))
        self.assertEqual([b["chapter"] for b in buckets], [1], "no tail: everything is ch 1's")
        b = buckets[0]
        self.assertEqual(b["cache_read_input_tokens"], 900)
        self.assertEqual(b["by_role"]["drafter"]["cache_read_input_tokens"], 400)
        self.assertEqual(b["by_role"]["gate"]["cache_read_input_tokens"], 500)

    def test_a_warm_drafter_across_chapters_falls_back_to_the_anchor_rule(self):
        """Continued by `SendMessage`, it keeps its first label; its writes say otherwise."""
        with Root() as root:
            rel = "projects/-work-repo/s1/subagents/agent-w.jsonl"
            root.write(rel, [self._write("2026-09-05T10:01:00.000Z", "w1", 1),
                             self._resp("2026-09-05T10:02:00.000Z", "w2", read=40),
                             self._write("2026-09-05T10:03:00.000Z", "w3", 2)])
            self._meta(root, rel, agentType="drafter", description="draft ch 1")
            sess = transcripts.sessions_for("/work/repo", root.dir)
            self.assertIsNone(sess[0].chapter_hint)
            buckets = transcripts.by_chapter(sess)
        self.assertEqual([(b["chapter"], b["cache_read_input_tokens"]) for b in buckets],
                         [(1, 0), (2, 40)])

    def test_work_after_the_last_write_is_kept_in_a_tail_row(self):
        """It was dropped, so the per-chapter rows never summed to the run total."""
        with Root() as root:
            root.write("projects/-work-repo/s1.jsonl", [
                self._write("2026-09-05T10:01:00.000Z", "a", 1),
                self._resp("2026-09-05T10:09:00.000Z", "b", read=250)])
            buckets = transcripts.by_chapter(transcripts.sessions_for("/work/repo", root.dir))
        self.assertEqual([b["chapter"] for b in buckets], [1, -1])
        self.assertEqual(buckets[-1]["cache_read_input_tokens"], 250)

    def test_aggregate_splits_by_role(self):
        with Root() as root:
            root.write("projects/-work-repo/s1.jsonl",
                       [self._resp("2026-09-05T10:00:00.000Z", "m", read=1)])
            rel = "projects/-work-repo/s1/subagents/agent-g.jsonl"
            root.write(rel, [self._resp("2026-09-05T10:01:00.000Z", "g", read=9)])
            self._meta(root, rel, agentType="gate", description="gate ch 2")
            agg = transcripts.aggregate(transcripts.sessions_for("/work/repo", root.dir))
        self.assertEqual(sorted(agg["by_role"]), ["gate", "main"])
        self.assertEqual(agg["by_role"]["gate"]["cache_read_input_tokens"], 9)

    def test_a_path_named_in_a_shell_command_is_recorded_as_opened(self):
        """What the routing check judges; the read guard never sees a `cat`."""
        with Root() as root:
            root.write("projects/-work-repo/s1.jsonl", [self._resp(
                "2026-09-05T10:00:00.000Z", "c", content=[{"type": "tool_use", "name": "Bash",
                "input": {"command": "cat roles/gate/prose-quality.audit-card.md docs/benchmark.md"}}])])
            sess = transcripts.sessions_for("/work/repo", root.dir)
        opened = [p for _ts, tool, p in sess[0].opened if tool == "Bash"]
        self.assertIn("roles/gate/prose-quality.audit-card.md", opened)
        self.assertIn("docs/benchmark.md", opened)
