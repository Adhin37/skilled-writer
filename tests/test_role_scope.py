"""The role read guard - who may open what.

The write guard holds the role table's `writes` column; this holds the other one, and it is the
half the physical split was bought for. After the move there is no body inside a role tree to
open by accident, but `.claude/skills/` still holds 44 of them and `roles/gate/` still holds 36
files the drafter has no business in. Until this hook existed, the only thing between a drafter
and an audit card was a sentence in `CLAUDE.md` §3.

Two properties matter as much as the table itself. The guard **fails open** on anything it does
not understand, because a guard that blocks work it was never meant to judge gets switched off
and then guards nothing. And **ALLOW is consulted before DENIED**: `roles/draft/` matches the
"belongs to another role" pattern, so reversing the two loops refuses a drafter its own bucket
with a message that reads like a correct block.
"""

import json
import os
import subprocess
import sys
import unittest

from fixtures import REPO

GUARD = os.path.join(REPO, "scripts", "hooks", "role_scope.py")


def run(payload):
    """Run the guard with `payload` on stdin and return (exit code, stderr)."""
    proc = subprocess.Popen([sys.executable, GUARD],
                            stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE)
    try:
        _out, err = proc.communicate(json.dumps(payload).encode("utf-8"))
    finally:
        for pipe in (proc.stdin, proc.stdout, proc.stderr):
            if pipe is not None and not pipe.closed:
                pipe.close()
    return proc.returncode, err.decode("utf-8")


def read(agent, path, tool="Read", key="file_path", **extra):
    """A read-shaped tool call from `agent`, or from the coordinator when `agent` is None."""
    payload = {"tool_name": tool, "tool_input": {key: path}}
    payload["tool_input"].update(extra)
    if agent is not None:
        payload["agent_id"] = "agent_%s_01" % agent
        payload["agent_type"] = agent
    return run(payload)


class Mixin(object):

    def allowed(self, agent, path, **kw):
        code, err = read(agent, path, **kw)
        self.assertEqual(code, 0, "%s should open %s\n%s" % (agent, path, err))

    def refused(self, agent, path, needle=None, **kw):
        code, err = read(agent, path, **kw)
        self.assertEqual(code, 2, "%s should be refused %s" % (agent, path))
        if needle:
            self.assertIn(needle, err)
        return err


class TestTheDrafter(unittest.TestCase, Mixin):
    """Its own bucket, `shared/`, its two dispatcher bodies, and the novel."""

    def test_it_reads_its_own_bucket(self):
        self.allowed("drafter", "roles/draft/story-craft.draft-card.md")

    def test_it_reads_shared(self):
        self.allowed("drafter", "roles/shared/voice-separation.mirror-clause.md")

    def test_it_reads_the_novel(self):
        self.allowed("drafter", "novels/a-book/state/continuity.md")
        self.allowed("drafter", "novels/a-book/bible/cast/_voices.md")

    def test_it_reads_its_dispatcher_bodies_and_no_other(self):
        """Granting nothing new: both are preloaded through `skills:` already.

        Naming them is what preserves the documented no-Python fallback - `AGENTS.md` says to
        read the body and follow its step list by hand when a command is unavailable.
        """
        self.allowed("drafter", ".claude/skills/write-chapter/SKILL.md")
        self.allowed("drafter", ".claude/skills/continuity-summary/SKILL.md")
        self.refused("drafter", ".claude/skills/revision-pass/SKILL.md")

    def test_the_gate_s_bucket_is_refused(self):
        self.refused("drafter", "roles/gate/prose-quality.audit-card.md",
                     "belongs to another role")

    def test_a_module_body_is_refused(self):
        """The rule that used to be §3 of a document a cooperating agent chose to obey."""
        self.refused("drafter", ".claude/skills/prose-quality/SKILL.md",
                     "opened through its card, never its body")

    def test_the_design_bucket_is_refused(self):
        self.refused("drafter", "roles/design/combat-choreography.duel-geography.md")

    def test_docs_is_refused_and_says_the_card_is_the_defect(self):
        """`AGENTS.md` has said this since before the split; here it is mechanical.

        The message names the right fix, which is not "go and read it another way": a card that
        points a drafter at `docs/` is the defect, and `sw health`'s partition assertion 5 now
        stops one being written.
        """
        self.refused("drafter", "docs/creative-latitude.md", "the card is the defect")

    def test_something_nobody_named_falls_to_the_catch_all(self):
        self.refused("drafter", ".claude/settings.json", "somebody else in the pipeline")


class TestTheGate(unittest.TestCase, Mixin):

    def test_it_reads_its_own_bucket_and_shared(self):
        self.allowed("gate", "roles/gate/prose-quality.audit-card.md")
        self.allowed("gate", "roles/shared/plot-threads.foreshadowing.md")

    def test_it_reads_its_dispatcher_body(self):
        self.allowed("gate", ".claude/skills/revision-pass/SKILL.md")

    def test_the_drafter_s_bucket_is_refused(self):
        """A gate holding the draft card is a gate marking its own homework."""
        self.refused("gate", "roles/draft/story-craft.draft-card.md",
                     "belongs to another role")

    def test_the_chapter_it_was_handed_is_its_own(self):
        self.allowed("gate", "novels/a-book/chapters/0006-the-turn.md")


class TestTheArchitect(unittest.TestCase, Mixin):
    """No allowlist, and that is deliberate: `design` reads every bucket and every body.

    Enumerating what an architect may open would produce a list that rots in the direction that
    gets guards switched off - refusing work the guard was never meant to judge. One thing is out
    of its reach, so one thing is written down.
    """

    def test_it_reads_a_module_body(self):
        self.allowed("architect", ".claude/skills/prose-quality/SKILL.md")

    def test_it_reads_every_bucket(self):
        for bucket in ("draft", "gate", "shared", "design"):
            self.allowed("architect", "roles/%s/story-craft.draft-card.md" % bucket)

    def test_it_reads_the_rationale(self):
        self.allowed("architect", "docs/design-notes.md")


class TestTheColdReadRubric(unittest.TestCase, Mixin):
    """`roles/review/` is denied to everybody but the reader, the architect included.

    A rubric the *novel* gets designed toward is no better than one the drafter writes toward,
    and the file says so in its own second paragraph. This is the one denial that binds a role
    with no other restriction at all.
    """

    def test_no_writing_role_reaches_it(self):
        for agent in ("drafter", "gate", "architect"):
            self.refused(agent, "roles/review/reader-review.md", "the reader has not read it")

    def test_nor_the_worked_example(self):
        self.refused("drafter", "roles/review/reader-review-example.md")


class TestTheReaderHasOneOwner(unittest.TestCase, Mixin):
    """Delegated to `reader_guard.py` rather than restated here.

    Two copies of the reader's table would be two things to maintain and a silent contradiction
    waiting for whichever one gets edited. What the delegation buys is that the reader is now
    guarded by the **settings** hook as well as its own frontmatter one - and a settings hook
    does not depend on workspace trust.
    """

    def test_the_chapters_are_allowed(self):
        self.allowed("reader", "novels/a-book/chapters/0001-open.md")

    def test_its_own_brief_is_allowed_and_the_procedure_is_not(self):
        """The delegation carries the split too, which is the point of delegating.

        `reader-brief.md` is what a reader opens; `reader-review.md` is the maintainer procedure
        around it and names what the exercise is for. Had this guard restated the reader's table
        instead of calling into it, this boundary would have moved in one file and not the other.
        """
        self.allowed("reader", "roles/review/reader-brief.md")
        self.refused("reader", "roles/review/reader-review.md")

    def test_the_bible_is_refused_with_the_reader_s_own_reason(self):
        err = self.refused("reader", "novels/a-book/bible/world.md")
        self.assertIn("that is what the novel intended", err)

    def test_the_verdict_comes_from_the_other_module(self):
        """Pinned as an identity, not as a behaviour: a copied table would pass a behaviour
        test on the day it was copied and drift afterwards."""
        sys.path.insert(0, os.path.join(REPO, "scripts", "hooks"))
        import reader_guard
        import role_scope
        self.assertIs(role_scope.reader_guard, reader_guard)


class TestTheCoordinatorAndTheUnknown(unittest.TestCase, Mixin):

    def test_the_main_session_reads_everything(self):
        """No `agent_id` means the main thread. The coordinator routes roles and writes up runs;
        it needs the whole repo, and `docs/` is six maintainer files addressed to it."""
        for path in ("roles/gate/prose-quality.audit-card.md", "docs/benchmark.md",
                     "roles/review/reader-review.md", ".claude/skills/mc-design/SKILL.md"):
            self.allowed(None, path)

    def test_agent_type_without_agent_id_is_still_the_main_session(self):
        """`agent_id` is the discriminator; `agent_type` alone is not evidence of a subagent.

        This is the branch that says so. Without it the coordinator is allowed only by falling
        through the unknown-agent check below - correct today by accident, and wrong the moment
        anything changes about who is in ALLOW.
        """
        self.assertEqual(run({"tool_name": "Read",
                              "tool_input": {"file_path": "roles/gate/x.audit-card.md"},
                              "agent_type": "drafter"})[0], 0)

    def test_an_agent_this_guard_does_not_know_is_allowed(self):
        """Fails open by design. A guard that refuses an agent it was never written for is a
        guard somebody removes, and then the four it *was* written for run unguarded."""
        self.allowed("general-purpose", "roles/gate/prose-quality.audit-card.md")


class TestEveryRoleKeepsTheToolkit(unittest.TestCase, Mixin):
    """`scripts/` and `tests/` are allowed explicitly, not by omission, and the reason is that
    denial here would break something documented.

    Every skill that names an `sw` command keeps a manual checklist underneath it, and the
    fallback when a command misbehaves is to read what it does. A checker's source is the
    rubric's *enforcement*, not the rubric: useless to game rather than dangerous to see.
    """

    def test_the_scripts_are_open_to_the_writing_roles(self):
        for agent in ("drafter", "gate"):
            self.allowed(agent, "scripts/swlib/cmd_lint.py")
            self.allowed(agent, "tests/test_lint.py")

    def test_so_is_the_contract_the_harness_already_gave_them(self):
        for agent in ("drafter", "gate"):
            self.allowed(agent, "CLAUDE.md")
            self.allowed(agent, "AGENTS.md")


class TestUnscopedSearch(unittest.TestCase, Mixin):
    """A `Grep` with no `path` starts at the repo root and reads every tree there is.

    An allowlist keyed on a path cannot see it, which makes it the one accidental route left
    open by the table itself - so it is refused with the fix in the message rather than silently
    permitted.
    """

    def test_a_rootless_grep_is_refused(self):
        code, err = run({"tool_name": "Grep", "tool_input": {"pattern": "Pass Z"},
                         "agent_id": "a1", "agent_type": "drafter"})
        self.assertEqual(code, 2)
        self.assertIn("starts at the repo root", err)

    def test_a_rooted_grep_is_judged_on_its_root(self):
        self.allowed("drafter", "roles/draft", tool="Grep", key="path", pattern="event")
        self.refused("drafter", "roles/gate", tool="Grep", key="path", pattern="event")

    def test_a_glob_pattern_is_a_path_and_is_judged(self):
        """Glob's `pattern` names files; Grep's is a regex over contents and says nothing about
        what gets read, so only one of the two is treated as a target.

        Asserted on the *reason*, not the exit code. A Glob whose pattern is ignored has no path
        in it at all, so the unrooted rule refuses it too - same code, different rule, and a test
        that reads only the code cannot tell which one it is watching.
        """
        self.refused("drafter", "roles/gate/*.md", "belongs to another role",
                     tool="Glob", key="pattern")

    def test_the_architect_may_search_the_repo(self):
        code, _err = run({"tool_name": "Grep", "tool_input": {"pattern": "anything"},
                          "agent_id": "a1", "agent_type": "architect"})
        self.assertEqual(code, 0)

    def test_the_coordinator_may_search_the_repo(self):
        self.assertEqual(run({"tool_name": "Grep", "tool_input": {"pattern": "x"}})[0], 0)


class TestItFailsOpen(unittest.TestCase, Mixin):
    """Every payload the guard cannot understand is allowed, and each of these is tested rather
    than assumed. The alternative is a guard that blocks on its own bug."""

    def feed(self, raw):
        proc = subprocess.Popen([sys.executable, GUARD], stdin=subprocess.PIPE,
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        try:
            proc.communicate(raw)
        finally:
            for pipe in (proc.stdin, proc.stdout, proc.stderr):
                if pipe is not None and not pipe.closed:
                    pipe.close()
        return proc.returncode

    def test_unparseable_json(self):
        self.assertEqual(self.feed(b"{not json"), 0)

    def test_empty_stdin(self):
        self.assertEqual(self.feed(b""), 0)

    def test_a_tool_input_that_is_not_a_dict(self):
        self.assertEqual(run({"tool_name": "Read", "tool_input": "roles/gate/x.md",
                              "agent_id": "a1", "agent_type": "drafter"})[0], 0)

    def test_a_call_with_no_path_in_it(self):
        self.assertEqual(run({"tool_name": "Read", "tool_input": {},
                              "agent_id": "a1", "agent_type": "drafter"})[0], 0)

    def test_an_agent_type_that_is_missing(self):
        self.assertEqual(run({"tool_name": "Read",
                              "tool_input": {"file_path": "roles/gate/x.md"},
                              "agent_id": "a1"})[0], 0)


class TestHowThePathArrives(unittest.TestCase, Mixin):
    """The same file, spelled the four ways a tool call spells it."""

    def test_an_absolute_path(self):
        self.refused("drafter", os.path.join(REPO, "roles", "gate", "x.audit-card.md"))

    def test_a_dot_slash_prefix(self):
        self.refused("drafter", "./roles/gate/x.audit-card.md")

    def test_a_traversal_that_normalises_back_in(self):
        self.refused("drafter", "roles/draft/../gate/x.audit-card.md")

    def test_the_same_traversal_into_its_own_tree_is_allowed(self):
        self.allowed("drafter", "roles/gate/../draft/story-craft.draft-card.md")


class TestItIsWiredWhereItCanReachTheCoordinator(unittest.TestCase):
    """Registered once in `.claude/settings.json`, not per agent.

    A settings-file hook runs inside subagents too, and it is the only kind that also runs for
    the main session - which has no agent file to carry one. `sw health` checks the path
    resolves; this checks the matcher covers the three tools that read.
    """

    def test_the_hook_is_registered_for_the_reading_tools(self):
        with open(os.path.join(REPO, ".claude", "settings.json"), encoding="utf-8") as fh:
            settings = json.load(fh)
        wired = [h for entry in settings["hooks"]["PreToolUse"]
                 for h in entry.get("hooks", [])
                 if "role_scope.py" in h.get("command", "")]
        self.assertEqual(len(wired), 1)
        matcher = [entry["matcher"] for entry in settings["hooks"]["PreToolUse"]
                   if any("role_scope.py" in h.get("command", "")
                          for h in entry.get("hooks", []))][0]
        for tool in ("Read", "Grep", "Glob"):
            self.assertIn(tool, matcher)

    def test_it_is_wired_through_the_project_dir_placeholder(self):
        """Hooks run in the *current* directory, which follows a worktree or a `cd`. A relative
        path would be skipped silently and the role would run unguarded - the exact trap Phase 1
        fell into."""
        with open(os.path.join(REPO, ".claude", "settings.json"), encoding="utf-8") as fh:
            settings = json.load(fh)
        command = [h["command"] for entry in settings["hooks"]["PreToolUse"]
                   for h in entry.get("hooks", [])
                   if "role_scope.py" in h.get("command", "")][0]
        self.assertIn('"${CLAUDE_PROJECT_DIR}"/scripts/hooks/role_scope.py', command)


if __name__ == "__main__":
    unittest.main()
