"""The role write guard - who may write where under `novels/`.

`CLAUDE.md` §10 gives each role one thing it writes, and until this hook existed every one of
those was a sentence held by goodwill. The case that matters most is the quietest: a coordinator
that repairs a chapter during a benchmark produces a run that looks like a pass and measures the
coordinator. Nothing downstream can tell the difference afterwards, so it is caught here.

The other half of the contract is that the guard **fails open**. A guard that blocks work it was
never meant to judge gets switched off, and then it guards nothing - so every payload it cannot
understand is tested to allow.
"""

import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest

from fixtures import REPO

GUARD = os.path.join(REPO, "scripts", "hooks", "write_scope.py")


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


def write(agent, path, **extra):
    """A write-shaped tool call from `agent`, or from the coordinator when `agent` is None."""
    payload = {"tool_name": "Write", "tool_input": {"file_path": path}}
    if agent is not None:
        payload["agent_id"] = "agent_%s_01" % agent
        payload["agent_type"] = agent
    payload.update(extra)
    return run(payload)


class TestTheArchitect(unittest.TestCase):
    """Writes what the story is: `bible/`, `plan/`, `novel.md`, and the state seeds."""

    def test_the_bible_is_its_own(self):
        self.assertEqual(write("architect", "novels/a-book/bible/world.md")[0], 0)

    def test_the_cast_is_its_own(self):
        self.assertEqual(write("architect", "novels/a-book/bible/cast/_voices.md")[0], 0)

    def test_the_plan_is_its_own(self):
        self.assertEqual(write("architect", "novels/a-book/plan/chapters.md")[0], 0)

    def test_the_config_is_its_own(self):
        self.assertEqual(write("architect", "novels/a-book/novel.md")[0], 0)

    def test_it_may_not_write_a_chapter(self):
        code, err = write("architect", "novels/a-book/chapters/0001-x.md")
        self.assertEqual(code, 2)
        self.assertIn("drafter", err)

    def test_it_seeds_the_state_its_procedures_name(self):
        """`novel-init` step 9 seeds the ledger and the state files before chapter 1 exists,
        `chapter-plan` sets `power.md` §6, and the arc rollup writes digests. Refused until
        2026-09-24, which left `/novel-new` unable to finish its own scaffold."""
        for name in ("continuity.md", "threads.md", "power.md", "body.md", "growth.md"):
            self.assertEqual(write("architect", "novels/a-book/state/%s" % name)[0], 0, name)

    def test_the_brief_stays_the_drafter_s(self):
        code, err = write("architect", "novels/a-book/state/brief.md")
        self.assertEqual(code, 2)
        self.assertIn("brief", err)


class TestTheDrafter(unittest.TestCase):
    """Writes the chapter and the state, and nothing that the chapter is checked against."""

    def test_the_chapter_is_its_own(self):
        self.assertEqual(write("drafter", "novels/a-book/chapters/0004-x.md")[0], 0)

    def test_state_is_its_own(self):
        self.assertEqual(write("drafter", "novels/a-book/state/continuity.md")[0], 0)

    def test_the_brief_is_its_own(self):
        self.assertEqual(write("drafter", "novels/a-book/state/brief.md")[0], 0)

    def test_it_may_not_edit_the_bible_mid_draft(self):
        code, err = write("drafter", "novels/a-book/bible/world.md")
        self.assertEqual(code, 2)
        self.assertIn("report", err.lower())

    def test_it_may_not_rewrite_the_plan_to_match_what_it_wrote(self):
        self.assertEqual(write("drafter", "novels/a-book/plan/chapters.md")[0], 2)


class TestTheGate(unittest.TestCase):
    """Repairs the chapter it was handed. Narrower than the drafter on purpose."""

    def test_the_chapter_is_its_own(self):
        self.assertEqual(write("gate", "novels/a-book/chapters/0004-x.md",
                               tool_name="Edit")[0], 0)

    def test_it_repairs_a_chapter_and_never_rewrites_it_whole(self):
        # It gained `Write` for its hand-back on 2026-09-26; the chapter stays Edit-only.
        code, err = write("gate", "novels/a-book/chapters/0004-x.md")
        self.assertEqual(code, 2)
        self.assertIn("Edit", err)

    def test_it_may_not_move_the_state_it_checks_against(self):
        code, err = write("gate", "novels/a-book/state/continuity.md")
        self.assertEqual(code, 2)
        self.assertIn("state", err)

    def test_it_may_not_edit_the_bible_to_make_the_chapter_consistent(self):
        self.assertEqual(write("gate", "novels/a-book/bible/world.md")[0], 2)

    def test_its_hand_back_is_its_own(self):
        # Run #6, I4: the hand-back was the one hand-off with no file, and a dead drafter took
        # the gate's design item with it. The gate writes it to state/gate.md, and only there.
        self.assertEqual(write("gate", "novels/a-book/state/gate.md")[0], 0)
        self.assertEqual(write("gate", "novels/a-book/state/threads.md")[0], 2)

    def test_nobody_else_writes_the_hand_back(self):
        # A drafter that could edit it could rewrite what the gate said about its own chapter.
        code, err = write("drafter", "novels/a-book/state/gate.md")
        self.assertEqual(code, 2)
        self.assertIn("hand-back", err)
        self.assertEqual(write("architect", "novels/a-book/state/gate.md")[0], 2)
        self.assertEqual(write("drafter", "novels/a-book/state/threads.md")[0], 0)
        self.assertEqual(write("drafter", "novels/a-book/state/brief.md")[0], 0)


class TestTheCoordinator(unittest.TestCase):
    """No `agent_id` means the main session. The marker decides, because the protocol does.

    `docs/test-run-protocol.md` binds the coordinator; `CLAUDE.md` says in as many words that it
    "does not apply to a normal run, where editing a chapter on request is the job". So the
    guard may not simply refuse the main session - it refuses it while a run is being measured.
    """

    def setUp(self):
        self.dir = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, self.dir, True)

    def marker(self):
        open(os.path.join(self.dir, ".test-run"), "w").close()

    def test_an_ordinary_run_may_edit_a_chapter_on_request(self):
        self.assertEqual(write(None, "novels/a-book/chapters/0001-x.md", cwd=self.dir)[0], 0)

    def test_a_test_run_refuses_the_chapter(self):
        self.marker()
        code, err = write(None, "novels/a-book/chapters/0001-x.md", cwd=self.dir)
        self.assertEqual(code, 2)
        self.assertIn("coordinator", err)

    def test_a_test_run_refuses_the_bible_too(self):
        self.marker()
        self.assertEqual(write(None, "novels/a-book/bible/world.md", cwd=self.dir)[0], 2)

    def test_a_test_run_leaves_the_toolkit_alone(self):
        """The protocol stops the coordinator repairing the novel, not repairing the toolkit."""
        self.marker()
        self.assertEqual(write(None, "scripts/swlib/cmd_health.py", cwd=self.dir)[0], 0)


class TestOutsideTheNovelTree(unittest.TestCase):
    """Not this guard's business, whoever is asking."""

    def test_every_role_may_write_the_toolkit(self):
        for agent in (None, "architect", "drafter", "gate"):
            self.assertEqual(write(agent, ".claude/skills/write-chapter/SKILL.md")[0], 0, agent)

    def test_the_scratchpad_is_free(self):
        self.assertEqual(write("drafter", "/tmp/claude-1000/x/scratchpad/notes.md")[0], 0)

    def test_a_path_merely_containing_the_word_is_not_the_tree(self):
        self.assertEqual(write("gate", "docs/novels-and-how-to-plan-them.md")[0], 0)


class TestItFailsOpen(unittest.TestCase):
    """Every one of these allows. A guard that blocks on its own bug stops the session."""

    def test_an_unparseable_payload_allows(self):
        self.assertEqual(feed(b"{not json")[0], 0)

    def test_empty_stdin_allows(self):
        self.assertEqual(feed(b"")[0], 0)

    def test_a_payload_with_no_tool_input_allows(self):
        self.assertEqual(run({"tool_name": "Write"})[0], 0)

    def test_a_tool_input_that_is_not_an_object_allows(self):
        self.assertEqual(run({"tool_input": "novels/a/bible/world.md"})[0], 0)

    def test_an_agent_this_guard_does_not_know_allows(self):
        """A new agent is not a violation. Add it to SCOPE deliberately, not by being refused."""
        self.assertEqual(write("reader", "novels/a-book/bible/world.md")[0], 0)
        self.assertEqual(write("general-purpose", "novels/a-book/chapters/0001-x.md")[0], 0)

    def test_a_coordinator_with_no_cwd_allows(self):
        self.assertEqual(run({"tool_input": {"file_path": "novels/a/chapters/0001-x.md"}})[0], 0)


class TestHowThePathArrives(unittest.TestCase):

    def test_absolute_paths_are_classified(self):
        path = os.path.join(REPO, "novels/a-book/bible/world.md")
        self.assertEqual(write("drafter", path)[0], 2)
        self.assertEqual(write("architect", path)[0], 0)

    def test_an_allowed_prefix_does_not_license_what_it_escapes_into(self):
        """The dangerous shape is a path that *reads* in-scope and lands somewhere else.

        Un-normalised, `novels/a/bible/../chapters/x` matches the architect's `bible/` pattern
        and is allowed, while the write it performs is a chapter. Refusing it is the whole
        reason the path is normalised before it is classified.
        """
        self.assertEqual(write("architect", "novels/a-book/bible/../chapters/0001-x.md")[0], 2)
        self.assertEqual(write("drafter", "novels/a-book/chapters/../bible/world.md")[0], 2)
        self.assertEqual(write("gate", "novels/a-book/chapters/../state/growth.md")[0], 2)

    def test_a_notebook_edit_is_a_write(self):
        payload = {"tool_name": "NotebookEdit", "agent_id": "a1", "agent_type": "gate",
                   "tool_input": {"notebook_path": "novels/a-book/bible/world.md"}}
        self.assertEqual(run(payload)[0], 2)


if __name__ == "__main__":
    unittest.main()
