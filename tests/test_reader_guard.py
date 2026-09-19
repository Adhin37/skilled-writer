"""The `reader` agent's path guard.

`docs/reader-review.md` rests on one claim: a reader who has not seen what the novel *intended*
can see what no instrument can, because every instrument here reads the novel with the bible
open. The claim is worth exactly as much as the blindness, so the blindness is tested.

These are the cases that would quietly destroy the instrument rather than break it - a reader
that can reach `bible/` still produces a review, just a contaminated one, and nothing downstream
would notice.
"""

import json
import os
import subprocess
import sys
import unittest

from fixtures import REPO

GUARD = os.path.join(REPO, "scripts", "hooks", "reader_guard.py")


def feed(stdin_bytes):
    """Run the guard with `stdin_bytes` and return (exit code, stderr)."""
    proc = subprocess.Popen([sys.executable, GUARD],
                            stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE)
    try:
        _out, err = proc.communicate(stdin_bytes)
    finally:
        for pipe in (proc.stdin, proc.stdout, proc.stderr):
            if pipe is not None and not pipe.closed:
                pipe.close()
    return proc.returncode, err.decode("utf-8")


def run(payload):
    return feed(json.dumps(payload).encode("utf-8"))


def read(path):
    return run({"tool_input": {"file_path": path}})


class TestWhatTheReaderMayOpen(unittest.TestCase):

    def test_chapters_are_allowed(self):
        self.assertEqual(read("novels/a-book/chapters/0001-x.md")[0], 0)

    def test_chapters_are_allowed_by_absolute_path(self):
        self.assertEqual(read(os.path.join(REPO, "novels/a/chapters/0001-x.md"))[0], 0)

    def test_the_procedure_is_allowed(self):
        self.assertEqual(read("docs/reader-review.md")[0], 0)


class TestWhatItMayNot(unittest.TestCase):

    def test_the_bible_is_blocked(self):
        code, err = read("novels/a-book/bible/world.md")
        self.assertEqual(code, 2)
        self.assertIn("intended", err)

    def test_state_is_blocked(self):
        self.assertEqual(read("novels/a-book/state/continuity.md")[0], 2)

    def test_the_plan_is_blocked(self):
        self.assertEqual(read("novels/a-book/plan/chapters.md")[0], 2)

    def test_novel_config_is_blocked(self):
        self.assertEqual(read("novels/a-book/novel.md")[0], 2)

    def test_the_worked_example_is_blocked(self):
        # It carries a verdict. A reader who sees it will find its findings again.
        code, err = read("docs/reader-review-example.md")
        self.assertEqual(code, 2)
        self.assertIn("verdict", err)

    def test_the_benchmark_log_is_blocked(self):
        self.assertEqual(read("docs/benchmark.md")[0], 2)

    def test_the_protocol_is_blocked(self):
        self.assertEqual(read("docs/test-run-protocol.md")[0], 2)

    def test_the_corpus_is_blocked(self):
        code, err = read(".claude/skills/prose-quality/references/audit-card.md")
        self.assertEqual(code, 2)
        self.assertIn("rules the chapters were written against", err)

    def test_a_grep_path_is_checked_not_only_file_path(self):
        self.assertEqual(run({"tool_input": {"path": "novels/a-book/bible"}})[0], 2)

    def test_an_unlisted_path_is_blocked_by_default(self):
        # An allowlist, not a blocklist: a blocklist has to predict every route into `bible/`.
        self.assertEqual(read("README.md")[0], 2)


class TestItFailsOpen(unittest.TestCase):
    """A guard that crashes the reader teaches you to remove the guard. The prompt list stays."""

    def test_malformed_json_does_not_block(self):
        self.assertEqual(feed(b"not json at all")[0], 0)

    def test_a_payload_with_no_paths_does_not_block(self):
        self.assertEqual(run({"tool_input": {"command": "ls"}})[0], 0)

    def test_an_empty_payload_does_not_block(self):
        self.assertEqual(run({})[0], 0)


class TestTheAgentIsWiredToIt(unittest.TestCase):

    def test_the_agent_declares_the_hook_and_the_isolation(self):
        path = os.path.join(REPO, ".claude", "agents", "reader.md")
        self.assertTrue(os.path.isfile(path), "the reader agent is missing")
        text = open(path, encoding="utf-8").read()
        self.assertIn("scripts/hooks/reader_guard.py", text)
        self.assertIn("omitClaudeMd: true", text)
        # No `Skill` tool: Claude Code has no per-skill allowlist, so the only way to keep the
        # corpus away from the reader is to deny the tool entirely.
        self.assertNotIn("Skill", text.split("---")[1])


if __name__ == "__main__":
    unittest.main()
