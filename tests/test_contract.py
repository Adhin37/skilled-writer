"""`sw contract <role>` - one source, N rendered artifacts, and a check that re-derives them.

A rendered contract is a **copy**, which is the thing this repo exists to remove - so the copy is
only tolerable while something re-derives it and fails when it drifts. These tests are that
claim: the render is deterministic, the health check sees a stale block, and it stays quiet about
a repo that never adopted one.

The binding table is asserted from the other side too. `CONTRACT_EXCLUDES` lists what a role does
**not** get, so a section nobody has ruled on reaches everybody - and a test that only checked
the exclusions would pass just as well if the default had been inverted.
"""

import os
import shutil
import tempfile
import unittest

from fixtures import REPO

from swlib import cmd_contract, cmd_health, kb, rules
from swlib.report import Report


def write(path, text):
    d = os.path.dirname(path)
    if d and not os.path.isdir(d):
        os.makedirs(d)
    with open(path, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(text)


CLAUDE = """# a toolkit

Preamble prose, addressed to whoever opened the repo. Read docs/test-run-protocol.md first.

---

## 1. Kept

A rule that binds everybody.

## 7. Dropped

The slash commands, which are the user's interface.

## 9. Also kept

Another rule.
"""

AGENT = ("---\nname: drafter\ndescription: writes a chapter.\ntools: Read\n"
         "omitClaudeMd: true\n---\n\n# drafter\n\nbody\n")


class Fake(object):
    """A repo with one CLAUDE.md and one agent file."""

    def __enter__(self):
        self.dir = tempfile.mkdtemp(prefix="sw-contract-")
        write(os.path.join(self.dir, "CLAUDE.md"), CLAUDE)
        write(os.path.join(self.dir, ".claude", "agents", "drafter.md"), AGENT)
        self._saved = dict(rules.CONTRACT_EXCLUDES)
        rules.CONTRACT_EXCLUDES = {"draft": ("7",), "gate": ("7",), "design": ("7",)}
        return self

    def __exit__(self, *exc):
        rules.CONTRACT_EXCLUDES = self._saved
        shutil.rmtree(self.dir, ignore_errors=True)
        return False

    def agent(self):
        with open(os.path.join(self.dir, ".claude", "agents", "drafter.md"),
                  encoding="utf-8") as fh:
            return fh.read()

    def health(self):
        rep = Report()
        cmd_health._contract(self.dir, rep)
        return [f for f in rep.findings if f.check == "contract"]


class TestWhatIsRendered(unittest.TestCase):

    def test_a_kept_section_is_in_and_an_excluded_one_is_not(self):
        with Fake() as f:
            out = cmd_contract.render(f.dir, "draft")
            self.assertIn("## 1. Kept", out)
            self.assertIn("## 9. Also kept", out)
            self.assertNotIn("## 7. Dropped", out)
            self.assertNotIn("the user's interface", out)

    def test_the_excluded_sections_are_named_rather_than_silently_missing(self):
        """An agent that does not know §7 exists cannot tell you the contract was cut.

        Naming them costs one line and turns a silent omission into a pointer, which matters
        most for the role that is *wrong* about its own scope - it now has somewhere to look.
        """
        with Fake() as f:
            self.assertIn("§7", cmd_contract.render(f.dir, "draft"))

    def test_the_preamble_is_never_rendered(self):
        """It names `docs/test-run-protocol.md`, which two of the three roles may not open.

        The preamble binds the coordinator - it is the instruction to read the protocol before a
        benchmark - so rendering it would put a pointer into a tree the reader is refused.
        """
        with Fake() as f:
            for role in cmd_contract.roles_with_contracts():
                out = cmd_contract.render(f.dir, role)
                self.assertNotIn("Preamble prose", out)
                self.assertNotIn("test-run-protocol", out)

    def test_a_section_nobody_ruled_on_reaches_every_role(self):
        """The default is *include*, and this is the test that would fail if it were inverted.

        A rule wrongly carried costs a few hundred words of a role's attention; one wrongly
        dropped costs a chapter. So a section added next month is in every contract until
        somebody writes it into the table on purpose.
        """
        with Fake() as f:
            rules.CONTRACT_EXCLUDES = {"draft": (), "gate": (), "design": ()}
            self.assertIn("## 7. Dropped", cmd_contract.render(f.dir, "draft"))


class TestTheReaderHasNoContract(unittest.TestCase):
    """`review` is absent from `ROLE_AGENT`, and that absence is the same enforcement the role
    is built on: a reader that has read the rubric is not a reader."""

    def test_review_has_no_agent_mapping(self):
        self.assertNotIn("review", cmd_contract.ROLE_AGENT)
        self.assertIn("review", kb.ROLES)

    def test_rendering_it_raises_rather_than_inventing_a_slice(self):
        with Fake() as f:
            self.assertRaises(KeyError, cmd_contract.render, f.dir, "review")

    def test_every_role_with_a_contract_is_a_role_the_index_knows(self):
        self.assertTrue(set(cmd_contract.ROLE_AGENT) <= set(kb.ROLES))


class TestWriting(unittest.TestCase):

    def test_it_appends_a_block_and_keeps_the_hand_written_body(self):
        with Fake() as f:
            cmd_contract.write(f.dir, "draft")
            body = f.agent()
            self.assertIn("name: drafter", body)
            self.assertIn("# drafter", body)
            self.assertIn(cmd_contract.BEGIN % "draft", body)
            self.assertIn(cmd_contract.END, body)

    def test_a_second_write_changes_nothing(self):
        with Fake() as f:
            cmd_contract.write(f.dir, "draft")
            first = f.agent()
            _path, changed = cmd_contract.write(f.dir, "draft")
            self.assertFalse(changed)
            self.assertEqual(f.agent(), first)

    def test_it_replaces_the_block_rather_than_appending_a_second(self):
        """Two blocks is the state where an agent reads one contract and `health` checks the
        other, which is worse than no generator at all."""
        with Fake() as f:
            cmd_contract.write(f.dir, "draft")
            path = os.path.join(f.dir, "CLAUDE.md")
            with open(path, encoding="utf-8") as fh:
                src = fh.read()
            write(path, src.replace("A rule that binds everybody.", "A rule, reworded."))
            cmd_contract.write(f.dir, "draft")
            body = f.agent()
            self.assertEqual(body.count(cmd_contract.BEGIN % "draft"), 1)
            self.assertEqual(body.count(cmd_contract.END), 1)
            self.assertIn("A rule, reworded.", body)
            self.assertNotIn("A rule that binds everybody.", body)

    def test_current_round_trips_with_render(self):
        with Fake() as f:
            cmd_contract.write(f.dir, "draft")
            self.assertEqual(cmd_contract.current(f.dir, "draft").strip(),
                             cmd_contract.render(f.dir, "draft").strip())


class TestTheHealthCheck(unittest.TestCase):

    def test_a_repo_that_never_adopted_a_contract_is_silent(self):
        """Rendering is opt-in per role. A repo without a block is not broken, and a check that
        demanded one would fire on every fixture in the suite."""
        with Fake() as f:
            self.assertEqual(f.health(), [])

    def test_a_fresh_block_is_clean(self):
        with Fake() as f:
            cmd_contract.write(f.dir, "draft")
            self.assertEqual(f.health(), [])

    def test_a_block_that_no_longer_matches_claude_md_is_a_defect(self):
        """The one state a copy must not be allowed to reach: two live contracts, and nothing
        saying which one the agent read."""
        with Fake() as f:
            cmd_contract.write(f.dir, "draft")
            path = os.path.join(f.dir, "CLAUDE.md")
            with open(path, encoding="utf-8") as fh:
                src = fh.read()
            write(path, src.replace("A rule that binds everybody.", "A rule that changed."))
            found = f.health()
            self.assertEqual(len(found), 1, found)
            self.assertIn("no longer matches", found[0].message)
            self.assertIn("contract draft --write", found[0].message)

    def test_a_hand_edit_inside_the_markers_is_a_defect(self):
        """Same check, the other direction - and the direction somebody will actually take."""
        with Fake() as f:
            cmd_contract.write(f.dir, "draft")
            p = os.path.join(f.dir, ".claude", "agents", "drafter.md")
            write(p, f.agent().replace("A rule that binds everybody.", "A rule I tweaked here."))
            self.assertEqual(len(f.health()), 1)


class TestASliceDoesNotPointAtWhatWasCut(unittest.TestCase):
    """A `§N` cross-reference is fine in the source and dangles the moment a slice is taken.

    Found 2026-09-22 by asking a live drafter what it held: three sentences in its own contract
    pointed at §8 and §10 as though they were in front of it, and `role_scope.py` refuses it
    `CLAUDE.md`, so it could not have followed them even in principle. Nothing else could have
    seen this - the render is correct, the diff is clean, and only a reader of the *result*
    notices that a pointer leads nowhere.
    """

    def test_a_pointer_at_an_excluded_section_is_found(self):
        with Fake() as f:
            path = os.path.join(f.dir, "CLAUDE.md")
            with open(path, encoding="utf-8") as fh:
                src = fh.read()
            write(path, src.replace("A rule that binds everybody.",
                                    "A rule that binds everybody. See §7."))
            found = cmd_contract.dangling(f.dir, "draft")
            self.assertEqual(len(found), 1, found)
            self.assertEqual(found[0][0], "§7")

    def test_a_pointer_at_a_kept_section_is_not(self):
        with Fake() as f:
            path = os.path.join(f.dir, "CLAUDE.md")
            with open(path, encoding="utf-8") as fh:
                src = fh.read()
            write(path, src.replace("A rule that binds everybody.",
                                    "A rule that binds everybody. See §9."))
            self.assertEqual(cmd_contract.dangling(f.dir, "draft"), [])

    def test_the_omissions_line_is_not_itself_a_dangling_pointer(self):
        """It names §7, §8 and §10 by number, which is the one place they belong.

        Telling a role what it does not have is the opposite of pointing it at something it
        cannot read - so the scan starts at the first section heading, and a check that forgot
        that would fire on every contract in the repo and be switched off within the week.
        """
        with Fake() as f:
            self.assertIn("§7", cmd_contract.render(f.dir, "draft"))
            self.assertEqual(cmd_contract.dangling(f.dir, "draft"), [])

    def test_it_is_a_defect_and_names_the_line(self):
        with Fake() as f:
            cmd_contract.write(f.dir, "draft")
            path = os.path.join(f.dir, "CLAUDE.md")
            with open(path, encoding="utf-8") as fh:
                src = fh.read()
            write(path, src.replace("A rule that binds everybody.",
                                    "A rule that binds everybody. See §7."))
            msgs = [x.message for x in f.health()]
            self.assertTrue(any("cites §7" in m for m in msgs), msgs)
            self.assertTrue(any("See §7." in m for m in msgs), msgs)

    def test_this_repo_has_none(self):
        for role in cmd_contract.roles_with_contracts():
            self.assertEqual(cmd_contract.dangling(REPO, role), [], role)


class TestTheFlagAndTheContractAreAPair(unittest.TestCase):
    """`omitClaudeMd: true` and a rendered contract only make sense together.

    The flag without the contract leaves an agent with no rules at all. The contract without the
    flag hands it the same rules twice. And for `reader`, which carries no contract, the flag is
    the only thing that keeps the auto-memory index out of a cold read - measured, because the
    documentation lists auto memory nowhere in the subagent startup set.
    """

    def test_every_named_agent_sets_it_in_this_repo(self):
        for agent in cmd_contract.OMIT_CLAUDE_MD:
            path = os.path.join(REPO, ".claude", "agents", agent + ".md")
            self.assertTrue(os.path.isfile(path), agent)
            with open(path, encoding="utf-8") as fh:
                self.assertIn("omitClaudeMd: true", fh.read(), agent)

    def test_the_reader_is_named_although_it_has_no_contract(self):
        """The two halves are separate claims, and the reader is the one that proves it.

        A check that only covered contract-carrying agents would leave the role whose isolation
        is load-bearing as the one role nothing verifies.
        """
        self.assertIn("reader", cmd_contract.OMIT_CLAUDE_MD)
        self.assertNotIn("reader", cmd_contract.ROLE_AGENT.values())

    def test_a_missing_flag_is_a_defect(self):
        with Fake() as f:
            cmd_contract.write(f.dir, "draft")
            self.assertEqual(f.health(), [])
            p = os.path.join(f.dir, ".claude", "agents", "drafter.md")
            with open(p, encoding="utf-8") as fh:
                body = fh.read()
            write(p, body.replace("omitClaudeMd: true\n", ""))
            found = f.health()
            self.assertEqual(len(found), 1, found)
            self.assertIn("omitClaudeMd", found[0].message)
            self.assertIn("twice", found[0].message)


class TestAgainstTheRealRepo(unittest.TestCase):
    """The fixtures prove the mechanism; this proves the repo is actually using it."""

    def test_every_role_with_a_contract_has_its_agent_file(self):
        for role in cmd_contract.roles_with_contracts():
            self.assertTrue(os.path.isfile(cmd_contract.agent_path(REPO, role)), role)

    def test_every_rendered_contract_is_current(self):
        for role in cmd_contract.roles_with_contracts():
            have = cmd_contract.current(REPO, role)
            self.assertIsNotNone(have, "%s carries no contract block" % role)
            self.assertEqual(have.strip(), cmd_contract.render(REPO, role).strip(), role)

    def test_the_excluded_sections_are_the_ones_that_describe_other_work(self):
        """Pinned by number, because dropping a section is the change worth noticing in review.

        §7 is the user's slash commands, §8 is how to author a skill file, §10 is the role table
        and the guards - each agent's own scope is stated in its own agent file.
        """
        for role in cmd_contract.roles_with_contracts():
            self.assertEqual(tuple(rules.CONTRACT_EXCLUDES[role]), ("7", "8", "10"), role)

    def test_the_hard_rules_reach_every_role_that_has_a_contract(self):
        """The failure this whole item had to avoid. Section 4 and section 5 are the contract -
        a role that lost them would draft against nothing and every check would stay green."""
        for role in cmd_contract.roles_with_contracts():
            out = cmd_contract.render(REPO, role)
            self.assertIn("## 4. Hard rules", out)
            self.assertIn("## 5. What good looks like", out)
            self.assertIn("State before prose", out)
            self.assertIn("No bias inheritance", out)


if __name__ == "__main__":
    unittest.main()
