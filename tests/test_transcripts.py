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

    def test_the_skill_tool_counts(self):
        with Root() as root:
            root.write("projects/-work-repo/s1.jsonl", [row(message={"content": [
                {"type": "tool_use", "name": "Skill", "input": {"skill": "mtl-detox"}}]})])
            sess = transcripts.sessions_for("/work/repo", root.dir)
        self.assertIn("mtl-detox", sess[0].skills)

    def test_a_path_that_merely_mentions_skills_is_not_a_skill_load(self):
        self.assertEqual(self._skills("/r/docs/skills-notes.md"), {})


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
