"""`sw health` finds the wiring defects it claims to, and finds none in this repo.

The second half is the load-bearing one: these checks exist so that somebody who edits a skill
learns they broke a pointer. If they were only ever run against synthetic fixtures, the repo
could drift out from under them exactly the way `plan_rows()` did.
"""

import json
import os
import shutil
import tempfile
import unittest

from fixtures import REPO  # noqa: F401  (puts scripts/ on sys.path)

from swlib import cmd_health, kb
from swlib.report import Report


def checks(rep, level="defect"):
    return {f.check for f in rep.findings if f.level == level}


class Fake(object):
    """A minimal repo: .claude/skills plus whatever the test writes."""

    def __enter__(self):
        self.dir = tempfile.mkdtemp(prefix="sw-health-")
        self.skills = os.path.join(self.dir, ".claude", "skills")
        self.roles = os.path.join(self.dir, "roles")
        os.makedirs(self.skills)
        return self

    def __exit__(self, *exc):
        shutil.rmtree(self.dir, ignore_errors=True)
        return False

    def skill(self, name, body="", frontmatter=None, references=None):
        d = os.path.join(self.skills, name)
        os.makedirs(d)
        fm = frontmatter if frontmatter is not None else (
            "name: %s\ndescription: does a thing." % name)
        with open(os.path.join(d, "SKILL.md"), "w", encoding="utf-8", newline="\n") as fh:
            fh.write("---\n%s\n---\n\n# %s\n\n%s\n" % (fm, name, body))
        for fname, text in (references or {}).items():
            self.role_file(name, fname, text)
        return d

    def role_file(self, owner, stem, text, bucket=None):
        """A corpus file in the tree the real repo keeps it in: `roles/<bucket>/owner.stem.md`.

        It used to write `<skill>/references/<stem>.md`, which `kb` still resolves - the old
        layout stays recognised so a citation written before the move can be found and rewritten.
        But `_partition()` asks where a file **sits**, not whether it resolves, so a fixture repo
        shaped the old way defects on a layout no real repo has any more. The bucket is inferred
        from the stem for the same reason `kb.CARD_KINDS` does: a card's kind names the role that
        opens it, and everything else is shared until a closure says otherwise.
        """
        if bucket is None:
            bucket = kb.CARD_ROLES.get(kb.CARD_KINDS.get(stem, (None,))[0], "shared")
        d = os.path.join(self.roles, bucket)
        if not os.path.isdir(d):
            os.makedirs(d)
        path = os.path.join(d, "%s.%s" % (owner, stem))
        with open(path, "w", encoding="utf-8", newline="\n") as fh:
            fh.write(text)
        return path

    def command(self, name):
        d = os.path.join(self.dir, ".claude", "commands")
        if not os.path.isdir(d):
            os.makedirs(d)
        with open(os.path.join(d, name + ".md"), "w", encoding="utf-8", newline="\n") as fh:
            fh.write("---\ndescription: does a thing\n---\n\nbody\n")

    def claude_md(self, text):
        with open(os.path.join(self.dir, "CLAUDE.md"), "w", encoding="utf-8", newline="\n") as fh:
            fh.write(text)

    def run(self, commands=None):
        return cmd_health.run(self.dir, commands=commands)


class TestSkillWiring(unittest.TestCase):

    def test_a_missing_skill_md_is_a_defect(self):
        with Fake() as f:
            os.makedirs(os.path.join(f.skills, "ghost"))
            self.assertIn("skill-frontmatter", checks(f.run()))

    def test_a_name_that_does_not_match_the_directory_is_a_defect(self):
        with Fake() as f:
            f.skill("alpha", frontmatter="name: beta\ndescription: x.")
            self.assertIn("skill-frontmatter", checks(f.run()))

    def test_a_missing_description_is_a_defect(self):
        """The dispatcher picks skills by description alone."""
        with Fake() as f:
            f.skill("alpha", frontmatter="name: alpha")
            self.assertIn("skill-frontmatter", checks(f.run()))

    def test_a_reference_nobody_cites_is_a_defect(self):
        """A pointer without a trigger is not read - CLAUDE.md section 8."""
        with Fake() as f:
            f.skill("alpha", body="no pointers here",
                    references={"notes.md": "# notes"})
            self.assertIn("skill-reference", checks(f.run()))

    def test_a_citation_with_no_file_behind_it_is_a_defect(self):
        with Fake() as f:
            f.skill("alpha", body="open `references/gone.md` when stuck")
            self.assertIn("skill-reference", checks(f.run()))

    def test_a_cross_skill_citation_resolves_against_the_other_skill(self):
        """`competence-map/references/x.md` is not a claim about the citing skill's own dir."""
        with Fake() as f:
            f.skill("alpha", body="see `beta/references/ladder.md` when the edge moves")
            f.skill("beta", body="see `references/ladder.md` when the edge moves",
                    references={"ladder.md": "# ladder"})
            self.assertNotIn("skill-reference", checks(f.run()))

    def test_a_card_must_be_named_by_its_dispatcher(self):
        """A draft card the dispatcher never opens is a file nobody reads."""
        with Fake() as f:
            f.skill("write-chapter", body="the procedure")
            f.skill("alpha", body="body", references={"draft-card.md": "# card"})
            self.assertIn("skill-card", checks(f.run()))

    def test_a_card_that_declares_its_dispatcher_is_accepted(self):
        """The edge is declared by the card, not copied into the dispatcher's prose."""
        card = ("---\ntype: draft-card\nowner: alpha\ndispatcher: write-chapter\n"
                "phase: A\ndescription: what alpha decides\nwhen: always\n---\n# card")
        with Fake() as f:
            f.skill("write-chapter", body="open the CARDS block the read-set resolved")
            f.skill("alpha", body="body", references={"draft-card.md": card})
            self.assertNotIn("skill-card", checks(f.run()))

    def test_a_card_with_no_phase_is_a_defect(self):
        """The dispatcher places a card by its `phase:`; without one it cannot be resolved.

        This is the replacement for the old string-presence check. That one asked whether the
        card's path appeared in the dispatcher's prose, which the resolver made meaningless -
        what matters now is whether the card carries enough to be placed.
        """
        card = ("---\ntype: draft-card\nowner: alpha\ndispatcher: write-chapter\n"
                "description: what alpha decides\nwhen: always\n---\n# card")
        with Fake() as f:
            f.skill("write-chapter", body="open the CARDS block the read-set resolved")
            f.skill("alpha", body="body", references={"draft-card.md": card})
            self.assertIn("skill-card", checks(f.run()))

    def test_a_card_naming_a_dispatcher_that_does_not_exist_is_a_defect(self):
        card = ("---\ntype: draft-card\nowner: alpha\ndispatcher: ghost-writer\n"
                "phase: A\ndescription: what alpha decides\nwhen: always\n---\n# card")
        with Fake() as f:
            f.skill("write-chapter", body="open the CARDS block the read-set resolved")
            f.skill("alpha", body="body", references={"draft-card.md": card})
            self.assertIn("kb-dispatch", checks(f.run()))

    def test_an_unreadable_trigger_is_a_defect(self):
        """A `when:` that does not parse leaves the card permanently unresolvable."""
        card = ("---\ntype: draft-card\nowner: alpha\ndispatcher: write-chapter\n"
                "phase: A\ndescription: d\nwhen: chapter <=\n---\n# card")
        with Fake() as f:
            f.skill("write-chapter", body="open the CARDS block the read-set resolved")
            f.skill("alpha", body="body", references={"draft-card.md": card})
            self.assertIn("kb-trigger", checks(f.run()))

    def test_a_line_number_citation_is_a_defect(self):
        """`hook-and-pacing:38-39` rots silently the moment a paragraph is added above it."""
        with Fake() as f:
            f.skill("alpha", body="see hook-and-pacing:38-39 for the rule")
            self.assertIn("line-citation", checks(f.run()))

    def test_an_ordinary_section_citation_is_not_flagged(self):
        with Fake() as f:
            f.skill("alpha", body="see `hook-and-pacing` section Openings for the rule")
            self.assertNotIn("line-citation", checks(f.run()))


class TestRoleWiring(unittest.TestCase):
    """The role axis is only worth having if a broken one is noisy.

    A missing role is a skill no agent's view reaches; a misspelled one is worse, because it
    presents as a skill quietly absent from a view rather than as an error.
    """

    FM = ("name: %s\ndescription: does a thing.\nmetadata:\n"
          "  type: skill\n  tier: craft\n  force: structural\n  when: always\n"
          "  role: [%s]\n  owns: [%s]")

    def test_a_skill_with_no_role_is_a_defect(self):
        with Fake() as f:
            f.skill("alpha", frontmatter=(
                "name: alpha\ndescription: does a thing.\nmetadata:\n"
                "  type: skill\n  tier: craft\n  force: structural\n  when: always\n"
                "  owns: [alpha-thing]"))
            self.assertIn("skill-role", checks(f.run()))

    def test_a_misspelled_role_is_a_defect(self):
        with Fake() as f:
            f.skill("alpha", frontmatter=self.FM % ("alpha", "drafy", "alpha-thing"))
            self.assertIn("skill-role", checks(f.run()))

    def test_a_well_formed_role_is_accepted(self):
        with Fake() as f:
            f.skill("alpha", frontmatter=self.FM % ("alpha", "draft, gate", "alpha-thing"))
            roles = [d for d in f.run().findings if d.check == "skill-role"
                     and d.level == "defect"]
            self.assertEqual(roles, [])


class TestAgentWiring(unittest.TestCase):
    """Role agents. A hook whose script has moved is logged and skipped, not raised - so the
    isolation stops existing while every other check stays green. Same shape as a card whose
    dispatcher was renamed, checked for the same reason."""

    def agent(self, fake, name, text):
        d = os.path.join(fake.dir, ".claude", "agents")
        if not os.path.isdir(d):
            os.makedirs(d)
        with open(os.path.join(d, name + ".md"), "w", encoding="utf-8", newline="\n") as fh:
            fh.write(text)

    def test_a_hook_pointing_at_a_missing_script_is_a_defect(self):
        with Fake() as f:
            f.skill("alpha", frontmatter=TestRoleWiring.FM % ("alpha", "draft", "a-thing"))
            self.agent(f, "reader", "---\nname: reader\ndescription: reads.\nhooks:\n"
                                    "  PreToolUse:\n    - matcher: \"Read\"\n      hooks:\n"
                                    "        - type: command\n"
                                    "          command: \"python3 scripts/hooks/gone.py\"\n"
                                    "---\n\nbody\n")
            self.assertIn("agent-hook", checks(f.run()))

    def test_a_name_that_does_not_match_the_filename_is_a_defect(self):
        with Fake() as f:
            f.skill("alpha", frontmatter=TestRoleWiring.FM % ("alpha", "draft", "a-thing"))
            self.agent(f, "reader", "---\nname: raeder\ndescription: reads.\n---\n\nbody\n")
            self.assertIn("agent-frontmatter", checks(f.run()))

    def test_a_missing_description_is_a_defect(self):
        with Fake() as f:
            f.skill("alpha", frontmatter=TestRoleWiring.FM % ("alpha", "draft", "a-thing"))
            self.agent(f, "reader", "---\nname: reader\n---\n\nbody\n")
            self.assertIn("agent-frontmatter", checks(f.run()))

    def test_no_agents_directory_is_not_a_defect(self):
        with Fake() as f:
            f.skill("alpha", frontmatter=TestRoleWiring.FM % ("alpha", "draft", "a-thing"))
            found = [d for d in f.run().findings if d.check.startswith("agent-")]
            self.assertEqual(found, [])

    AGENT = ("---\nname: reader\ndescription: reads.\nhooks:\n"
             "  PreToolUse:\n    - matcher: \"Read\"\n      hooks:\n"
             "        - type: command\n          command: %s\n---\n\nbody\n")

    def guard(self, fake, rel):
        d = os.path.join(fake.dir, os.path.dirname(rel))
        if not os.path.isdir(d):
            os.makedirs(d)
        with open(os.path.join(fake.dir, rel), "w", encoding="utf-8", newline="\n") as fh:
            fh.write("#\n")

    def test_a_project_dir_placeholder_is_resolved_not_skipped(self):
        """The documented form must still be *checked*, or adopting it retires the check.

        A pattern that only reads bare relative paths matches nothing in
        `"${CLAUDE_PROJECT_DIR}"/scripts/...`, so the missing script goes unreported and the
        wiring looks sound precisely because it was written the recommended way.
        """
        with Fake() as f:
            f.skill("alpha", frontmatter=TestRoleWiring.FM % ("alpha", "draft", "a-thing"))
            self.agent(f, "reader", self.AGENT
                       % '\'python3 "${CLAUDE_PROJECT_DIR}"/scripts/hooks/gone.py\'')
            self.assertIn("agent-hook", checks(f.run()))

    def test_a_relative_hook_path_is_a_warning_even_when_the_script_is_there(self):
        """Hooks run in the current directory, which follows a worktree or a cd. A relative
        path resolves when the cwd happens to be right and is skipped silently when it is
        not - the same unguarded agent as a missing script, with nothing on disk to show it."""
        with Fake() as f:
            f.skill("alpha", frontmatter=TestRoleWiring.FM % ("alpha", "draft", "a-thing"))
            self.guard(f, "scripts/hooks/guard.py")
            self.agent(f, "reader", self.AGENT % '"python3 scripts/hooks/guard.py"')
            rep = f.run()
            self.assertNotIn("agent-hook", checks(rep),
                             "the script is there; nothing is broken yet")
            self.assertIn("agent-hook", checks(rep, "warn"))

    def test_the_placeholder_form_draws_no_warning(self):
        with Fake() as f:
            f.skill("alpha", frontmatter=TestRoleWiring.FM % ("alpha", "draft", "a-thing"))
            self.guard(f, "scripts/hooks/guard.py")
            self.agent(f, "reader", self.AGENT
                       % '\'python3 "${CLAUDE_PROJECT_DIR}"/scripts/hooks/guard.py\'')
            rep = f.run()
            self.assertNotIn("agent-hook", checks(rep))
            self.assertNotIn("agent-hook", checks(rep, "warn"))


class TestSettingsHooks(unittest.TestCase):
    """The one hook `TestAgentWiring` structurally cannot see.

    A guard that dispatches on *which* agent is calling has to be registered project-wide,
    because the coordinator is the main session and has no agent file to carry frontmatter. So
    the hook whose entire job is catching the role nothing else can catch lives in a file the
    agent check never opens, and its path rots exactly as silently.
    """

    def settings(self, fake, payload):
        d = os.path.join(fake.dir, ".claude")
        if not os.path.isdir(d):
            os.makedirs(d)
        with open(os.path.join(d, "settings.json"), "w", encoding="utf-8", newline="\n") as fh:
            fh.write(payload)

    def hooks(self, command):
        return json.dumps({"hooks": {"PreToolUse": [
            {"matcher": "Write|Edit", "hooks": [{"type": "command", "command": command}]}]}})

    def fake(self):
        f = Fake()
        f.__enter__()
        self.addCleanup(f.__exit__, None, None, None)
        f.skill("alpha", frontmatter=TestRoleWiring.FM % ("alpha", "draft", "a-thing"))
        return f

    def guard(self, fake, rel):
        d = os.path.join(fake.dir, os.path.dirname(rel))
        if not os.path.isdir(d):
            os.makedirs(d)
        with open(os.path.join(fake.dir, rel), "w", encoding="utf-8", newline="\n") as fh:
            fh.write("#\n")

    def test_a_missing_script_is_a_defect(self):
        f = self.fake()
        self.settings(f, self.hooks('python3 "${CLAUDE_PROJECT_DIR}"/scripts/hooks/gone.py'))
        self.assertIn("settings-hook", checks(f.run()))

    def test_a_relative_path_is_a_warning_even_when_the_script_is_there(self):
        f = self.fake()
        self.guard(f, "scripts/hooks/guard.py")
        self.settings(f, self.hooks("python3 scripts/hooks/guard.py"))
        rep = f.run()
        self.assertNotIn("settings-hook", checks(rep))
        self.assertIn("settings-hook", checks(rep, "warn"))

    def test_the_placeholder_form_is_clean(self):
        f = self.fake()
        self.guard(f, "scripts/hooks/guard.py")
        self.settings(f, self.hooks('python3 "${CLAUDE_PROJECT_DIR}"/scripts/hooks/guard.py'))
        rep = f.run()
        self.assertNotIn("settings-hook", checks(rep))
        self.assertNotIn("settings-hook", checks(rep, "warn"))

    def test_settings_that_do_not_parse_are_a_defect(self):
        """Every permission and every hook in the file is being ignored, silently."""
        f = self.fake()
        self.settings(f, '{"hooks": {"PreToolUse": [},}')
        self.assertIn("settings-hook", checks(f.run()))

    def test_settings_with_no_hooks_key_is_not_a_defect(self):
        f = self.fake()
        self.settings(f, json.dumps({"permissions": {"allow": ["Read(**)"]}}))
        self.assertNotIn("settings-hook", checks(f.run()))

    def test_no_settings_file_is_not_a_defect(self):
        f = self.fake()
        found = [d for d in f.run().findings if d.check == "settings-hook"]
        self.assertEqual(found, [])


class TestCommandDocs(unittest.TestCase):

    def test_a_documented_command_that_does_not_exist_is_a_defect(self):
        with Fake() as f:
            f.skill("alpha", body="x")
            with open(os.path.join(f.dir, "CLAUDE.md"), "w", encoding="utf-8") as fh:
                fh.write("# x\n\n## 9. The mechanical toolkit\n\n"
                         "| command | use it in |\n|---|---|\n"
                         "| `imaginary <novel>` | nowhere |\n")
            self.assertIn("command-doc", checks(f.run(commands=["lint"])))


class TestTheRealRepo(unittest.TestCase):
    """The point of the command. If this fails, the repo is what is broken."""

    def test_this_repo_is_clean(self):
        rep = cmd_health.run(REPO, commands=None)
        bad = sorted("%s: %s" % (f.check, f.message) for f in rep.findings
                     if f.level == "defect")
        self.assertEqual(bad, [], "sw health reports defects against skilled-writer itself")

    def test_the_template_accessor_table_is_not_empty(self):
        """`test_template_wiring` imports these; an emptied list would pass everything."""
        self.assertGreaterEqual(len(cmd_health.TABLE_ACCESSORS), 12)
        self.assertGreaterEqual(len(cmd_health.SECTION_LOOKUPS), 13)


class TestSkillNamesMeansLoadable(unittest.TestCase):
    """`skill_names` used to return any directory, `SKILL.md` or not.

    That is the shape a half-finished move leaves behind, and every check downstream then ran
    against a body that was not there - looking for frontmatter in a file it could not open and
    reporting the absence as the skill's fault, once per check.
    """

    def test_a_directory_with_no_body_is_not_a_skill(self):
        with Fake() as f:
            f.skill("real-one")
            os.makedirs(os.path.join(f.skills, "left-behind"))
            self.assertEqual(cmd_health.skill_names(f.dir), ["real-one"])
            self.assertEqual(cmd_health.skill_dirs(f.dir), ["left-behind", "real-one"])

    def test_but_it_is_still_a_defect(self):
        """Excluding it from the roster must not excuse it."""
        with Fake() as f:
            f.skill("real-one")
            os.makedirs(os.path.join(f.skills, "left-behind"))
            rep = f.run()
            messages = [str(x.message) for x in rep.findings if x.level == "defect"]
            self.assertTrue([m for m in messages if "left-behind" in m and "SKILL.md" in m],
                            messages)

    def test_an_empty_tree_reads_as_empty_rather_than_absent(self):
        """Present-but-empty and absent-entirely arrive by different routes."""
        with Fake() as f:
            rep = f.run()
            self.assertIn("is empty", str(rep.findings[0].message))

    def test_health_and_kb_agree_on_where_the_skills_are(self):
        """Two private copies of a path is two things to move."""
        from swlib import kb
        self.assertEqual(cmd_health.skills_dir(REPO), kb.skills_dir(REPO))


if __name__ == "__main__":
    unittest.main()


class TestDispatcherWiring(unittest.TestCase):
    """Benchmark run #2, F4. `mtl-detox` loaded zero times in a real 5-chapter run.

    Not laziness: CLAUDE.md section 3 said it runs "Inside `revision-pass`", and
    `revision-pass/SKILL.md` never named it, so a model following `revision-pass` correctly never
    opened it. `health` reported 0 defects throughout, because its card check is card-anchored —
    it asks whether every card that exists is opened, which cannot see a skill with no card.
    """

    REGISTRY = ("# x\n\n## 3. Skill registry\n\n"
                "| skill | use when |\n|---|---|\n"
                "| `alpha` | Cleaning up. Inside `revision-pass`. |\n"
                "| `revision-pass` | The gate. |\n")

    def _repo(self, f, dispatcher_body):
        f.skill("alpha", body="x")
        f.skill("revision-pass", body=dispatcher_body)
        with open(os.path.join(f.dir, "CLAUDE.md"), "w", encoding="utf-8") as fh:
            fh.write(self.REGISTRY)
        return f.run()

    def test_a_dispatcher_that_never_names_its_skill_is_a_defect(self):
        """Was: silent. The skill simply never entered context on any run."""
        with Fake() as f:
            self.assertIn("skill-dispatch", checks(self._repo(f, "Pass 1. Pass 2. Pass 3.")))

    def test_naming_the_skill_clears_it(self):
        with Fake() as f:
            self.assertNotIn("skill-dispatch",
                             checks(self._repo(f, "Pass 7 - open `alpha` and work it there.")))


class TestOwnership(unittest.TestCase):
    """`owns:` is the scope declaration: one concept, one owner."""

    def test_a_skill_with_no_owns_is_a_defect(self):
        with Fake() as f:
            f.skill("alpha")
            self.assertIn("skill-scope", checks(f.run()))

    def test_two_skills_claiming_one_concept_is_a_defect(self):
        with Fake() as f:
            f.skill("alpha", frontmatter="name: alpha\ndescription: d.\nowns: [voice-matrix]")
            f.skill("beta", frontmatter="name: beta\ndescription: d.\nowns: [voice-matrix]")
            self.assertIn("skill-scope", checks(f.run()))

    def test_distinct_claims_are_clean(self):
        with Fake() as f:
            f.skill("alpha", frontmatter="name: alpha\ndescription: d.\nowns: [voice-matrix]")
            f.skill("beta", frontmatter="name: beta\ndescription: d.\nowns: [stake-ladder]")
            self.assertNotIn("skill-scope", checks(f.run()))

    def test_a_slug_that_is_not_kebab_case_is_a_defect(self):
        with Fake() as f:
            f.skill("alpha", frontmatter="name: alpha\ndescription: d.\nowns: [Voice Matrix]")
            self.assertIn("skill-scope", checks(f.run()))


class TestOverlapDetector(unittest.TestCase):
    """Two skills carrying the same passage is what drifts. Citing one costs nothing."""

    PASSAGE = ("A permanent loss takes a person, a capability, a belief, or a place the "
               "protagonist can never return to, and the reader can state which. ")

    def test_a_shared_passage_between_two_skills_is_reported(self):
        with Fake() as f:
            f.skill("alpha", frontmatter="name: alpha\ndescription: d.\nowns: [a-thing]",
                    body=self.PASSAGE * 3)
            f.skill("beta", frontmatter="name: beta\ndescription: d.\nowns: [b-thing]",
                    body=self.PASSAGE * 3)
            self.assertIn("skill-overlap", checks(f.run(), "warn"))

    def test_a_citation_is_not_an_overlap(self):
        """Code spans are stripped before comparison, so pointing at an owner is free."""
        with Fake() as f:
            f.skill("alpha", frontmatter="name: alpha\ndescription: d.\nowns: [a-thing]",
                    body=self.PASSAGE * 3)
            f.skill("beta", frontmatter="name: beta\ndescription: d.\nowns: [b-thing]",
                    body="The stake ladder is `alpha`'s. " * 6)
            self.assertNotIn("skill-overlap", checks(f.run(), "warn"))

    def test_uniform_frontmatter_is_not_an_overlap(self):
        """The knowledge-base layer gives every card the same frontmatter keys.

        Without stripping it, the shared `type:`/`owner:`/`dispatcher:` block is a 10-word
        passage every pair of cards has in common and `skill-overlap` fires on all of them -
        which would destroy the warning channel permanently. Frontmatter is structure.
        """
        fm = ("---\ntype: draft-card\ndispatcher: write-chapter\nphase: A\n"
              "status: stable\ngenerated: {by: process:sw-migrate}\nwhen: always\n---\n")
        with Fake() as f:
            f.skill("alpha", frontmatter="name: alpha\ndescription: d.\nowns: [a-thing]",
                    references={"draft-card.md": fm + "Alpha decides how wide the gap is."})
            f.skill("beta", frontmatter="name: beta\ndescription: d.\nowns: [b-thing]",
                    references={"draft-card.md": fm + "Beta decides which beat gets played."})
            self.assertNotIn("skill-overlap", checks(f.run(), "warn"))

    def test_boilerplate_is_not_an_overlap(self):
        """The card template is structure every skill shares, not duplicated craft advice."""
        boiler = "Written here rather than summarised there. "
        with Fake() as f:
            f.skill("alpha", frontmatter="name: alpha\ndescription: d.\nowns: [a-thing]",
                    body="Alpha decides how wide the gap is. " + boiler)
            f.skill("beta", frontmatter="name: beta\ndescription: d.\nowns: [b-thing]",
                    body="Beta decides which beat gets played. " + boiler)
            self.assertNotIn("skill-overlap", checks(f.run(), "warn"))


class TestUncitedConcept(unittest.TestCase):
    """The paraphrase case: a skill states someone else's rule in its own words."""

    OWNER = "name: alpha\ndescription: d.\nowns: [stake-ladder]"
    OTHER = "name: beta\ndescription: d.\nowns: [b-thing]"

    def test_discussing_another_skills_concept_without_naming_it_is_reported(self):
        with Fake() as f:
            f.skill("alpha", frontmatter=self.OWNER)
            f.skill("beta", frontmatter=self.OTHER,
                    body="The stake ladder decides it. Climb the stake ladder every arc.")
            self.assertIn("skill-scope", checks(f.run(), "warn"))

    def test_naming_the_owner_clears_it(self):
        with Fake() as f:
            f.skill("alpha", frontmatter=self.OWNER)
            f.skill("beta", frontmatter=self.OTHER,
                    body="The stake ladder is `alpha`'s. Read the stake ladder there.")
            self.assertNotIn("skill-scope", checks(f.run(), "warn"))

    def test_one_passing_mention_is_not_a_finding(self):
        with Fake() as f:
            f.skill("alpha", frontmatter=self.OWNER)
            f.skill("beta", frontmatter=self.OTHER, body="Something about a stake ladder.")
            self.assertNotIn("skill-scope", checks(f.run(), "warn"))

    def test_a_single_word_concept_is_never_checked(self):
        """`title` and `pressure` are ordinary vocabulary, not evidence of a copy."""
        with Fake() as f:
            f.skill("alpha", frontmatter="name: alpha\ndescription: d.\nowns: [title]")
            f.skill("beta", frontmatter=self.OTHER,
                    body="The title matters. A title earns the click. Title again.")
            self.assertNotIn("skill-scope", checks(f.run(), "warn"))


class TestSlashCommandWiring(unittest.TestCase):
    """CLAUDE.md section 7 is the only place a user learns a slash command exists."""

    SECTION = "## 7. Slash commands\n\n%s\n"

    def test_a_listed_command_with_no_file_is_a_defect(self):
        with Fake() as f:
            f.skill('anything')
            f.claude_md(self.SECTION % "`/novel-write` `/novel-ghost`")
            f.command("novel-write")
            self.assertIn("slash-command", checks(f.run()))

    def test_a_command_file_nobody_lists_is_a_warning(self):
        """It works when typed; it is simply invisible. That is a decision, not a break."""
        with Fake() as f:
            f.skill('anything')
            f.claude_md(self.SECTION % "`/novel-write`")
            f.command("novel-write")
            f.command("novel-orphan")
            rep = f.run()
            self.assertIn("slash-command", checks(rep, "warn"))
            self.assertNotIn("slash-command", checks(rep))

    def test_a_matched_pair_is_clean(self):
        with Fake() as f:
            f.skill('anything')
            f.claude_md(self.SECTION % "`/novel-write` `/novel-plan`")
            f.command("novel-write")
            f.command("novel-plan")
            self.assertNotIn("slash-command", checks(f.run()))


class TestPartition(unittest.TestCase):
    """The role trees are a partition, and every way of breaking one has been watched to fire.

    These five assertions are what replaced a prose rule. *A drafting agent never opens a
    `SKILL.md`* used to be a sentence somebody obeyed; here it is a defect with a path in it.
    A check nobody has seen fire is a check nobody knows works, so each assertion gets its own
    mutation and each test asserts on the message rather than on the check name - several of
    these mutations trip more than one assertion, and a bare `assertIn("partition", ...)` could
    not tell which one did the work.
    """

    SKILL = ("name: %s\ndescription: does a thing.\nmetadata:\n"
             "  type: skill\n  tier: craft\n  force: structural\n  when: always\n"
             "  role: [%s]\n  owns: [%s]")
    CARD = "---\ntype: %s\nowner: %s\ndispatcher: %s\n---\n\n# card\n\n%s\n"
    NOTE = "---\ntype: reference\nowner: %s\n---\n\n# note\n\nOpen this when %s.\n"

    def base(self, f):
        """A repo whose partition is already clean, so a test's mutation is the only finding.

        `alpha` carries a draft card that cites one note. Both are reached by `draft` and by
        nothing else - `gate` has no cards here and no dispatcher body to seed from - so both
        belong exactly where they sit, and the fixture starts at zero partition findings.
        """
        f.skill("alpha", frontmatter=self.SKILL % ("alpha", "draft", "alpha-thing"))
        f.role_file("alpha", "draft-card.md",
                    self.CARD % ("draft-card", "alpha", "write-chapter",
                                 "Decide it. See roles/draft/alpha.notes.md"))
        f.role_file("alpha", "notes.md", self.NOTE % ("alpha", "the call is close"),
                    bucket="draft")

    def messages(self, rep, level="defect"):
        return [x.message for x in rep.findings
                if x.check == "partition" and x.level == level]

    def only(self, rep, needle, level="defect"):
        """Exactly one partition finding, and it is the one the mutation was aimed at."""
        got = self.messages(rep, level)
        self.assertEqual(len(got), 1, got)
        self.assertIn(needle, got[0])
        return got[0]

    # -- the baseline, without which every test below proves nothing ----------

    def test_a_clean_partition_reports_nothing(self):
        with Fake() as f:
            self.base(f)
            self.assertEqual(self.messages(f.run()), [])
            self.assertEqual(self.messages(f.run(), "warn"), [])

    def test_a_repo_with_no_role_trees_is_silent(self):
        """`_corpus_floor` owns 'the corpus vanished' and is anchored to the real repo.

        A two-skill fixture that never writes a role file has no partition to have, and asking
        it for one would make every other fixture in this file noisy for no reason.
        """
        with Fake() as f:
            f.skill("alpha")
            self.assertEqual(self.messages(f.run()), [])

    # -- 1: no body in a role tree -------------------------------------------

    def test_a_skill_body_inside_a_role_tree_is_a_defect(self):
        """The whole point of the move. It is the one assertion that needs no index.

        Exactly one finding, and the body cites `docs/` to prove it: assertion 5 would otherwise
        add "move the rationale to `provenance:`", which is what you do to a note that belongs in
        the tree rather than to a file that belongs outside it. A real body does cite `docs/` -
        `revision-pass/SKILL.md` does - so this fired the first time it was tried for real.
        """
        with Fake() as f:
            self.base(f)
            with open(os.path.join(f.roles, "draft", "SKILL.md"),
                      "w", encoding="utf-8", newline="\n") as fh:
                fh.write("---\nname: smuggled\n---\n\n# body\n\nSee docs/design-notes.md.\n")
            self.only(f.run(), "is a skill body inside a role tree")

    # -- 2: one bucket deep, `.md` only, `<owner>.<stem>.md` -----------------

    def test_a_file_at_the_root_of_the_trees_is_a_defect(self):
        with Fake() as f:
            self.base(f)
            with open(os.path.join(f.roles, "loose.md"),
                      "w", encoding="utf-8", newline="\n") as fh:
                fh.write("# loose\n")
            self.only(f.run(), "is a file at the root of the role trees")

    def test_a_directory_that_is_not_a_bucket_is_a_defect(self):
        with Fake() as f:
            self.base(f)
            os.makedirs(os.path.join(f.roles, "drift"))
            self.only(f.run(), "is not a bucket")

    def test_a_subdirectory_inside_a_bucket_is_a_defect(self):
        """A bucket is flat so a citation can go straight to `Read` with no resolution step."""
        with Fake() as f:
            self.base(f)
            os.makedirs(os.path.join(f.roles, "draft", "deeper"))
            self.only(f.run(), "is a subdirectory")

    def test_a_file_that_is_not_markdown_is_a_defect(self):
        with Fake() as f:
            self.base(f)
            with open(os.path.join(f.roles, "draft", "alpha.notes.txt"),
                      "w", encoding="utf-8", newline="\n") as fh:
                fh.write("notes\n")
            self.only(f.run(), "is not a `.md` file")

    def test_a_name_that_is_not_owner_dot_stem_is_a_defect(self):
        """The prefix is the checksum on the declared owner, so an unprefixed name is a defect.

        The file is cited from the card and declares `owner: alpha`, so it is reachable and
        correctly bucketed - the *only* thing wrong with it is its name, which is what makes
        this a test of the name rule rather than of the closure.
        """
        with Fake() as f:
            self.base(f)
            with open(os.path.join(f.roles, "draft", "Alpha.extra.md"),
                      "w", encoding="utf-8", newline="\n") as fh:
                fh.write(self.NOTE % ("alpha", "the call is closer"))
            f.role_file("alpha", "draft-card.md",
                        self.CARD % ("draft-card", "alpha", "write-chapter",
                                     "Decide it. See roles/draft/alpha.notes.md and "
                                     "roles/draft/Alpha.extra.md"))
            self.only(f.run(), "is not `<owner>.<stem>.md`")

    def test_the_reader_s_tree_is_exempt_from_the_name_rule(self):
        """`review` carries no corpus: its files are documents, not owned notes.

        They declare no `owner:` to prefix and sit deliberately outside `kb.BUCKETS`, so the
        rule that makes the prefix a checksum has nothing to check them against.
        """
        with Fake() as f:
            self.base(f)
            os.makedirs(os.path.join(f.roles, "review"))
            with open(os.path.join(f.roles, "review", "reader-review.md"),
                      "w", encoding="utf-8", newline="\n") as fh:
                fh.write("# Reader review\n\nRead the chapters and nothing else.\n")
            self.assertEqual(self.messages(f.run()), [])

    # -- 3: the closure agrees with the shelf --------------------------------

    def test_a_note_both_roles_reach_belongs_in_shared(self):
        """The assertion with teeth: it names `shared/` before either role is refused the file.

        This is also where Part 7's sixth assertion went - *no `draft/` file is reachable from
        an audit card*. That is the special case of this one where the disagreement is a card's,
        so a separate check would have been a second copy under a different name.
        """
        with Fake() as f:
            self.base(f)
            f.skill("beta", frontmatter=self.SKILL % ("beta", "gate", "beta-thing"))
            f.role_file("beta", "audit-card.md",
                        self.CARD % ("audit-card", "beta", "revision-pass",
                                     "Check it. See roles/draft/alpha.notes.md"))
            msg = self.only(f.run(), "it belongs in roles/shared/")
            self.assertIn("reached by draft, gate", msg)

    def test_a_note_no_role_reaches_belongs_in_design(self):
        """`design` is the residue, not a claim about where the architect stops looking.

        The note is cited by `alpha`'s body, which keeps the anti-orphan check quiet - and a
        body is not a seed unless it is a dispatcher, so nothing reaches the file.
        """
        with Fake() as f:
            f.skill("alpha", body="Background: roles/draft/alpha.orphan.md",
                    frontmatter=self.SKILL % ("alpha", "draft", "alpha-thing"))
            f.role_file("alpha", "draft-card.md",
                        self.CARD % ("draft-card", "alpha", "write-chapter", "Decide it."))
            f.role_file("alpha", "orphan.md", self.NOTE % ("alpha", "designing the thing"),
                        bucket="draft")
            self.only(f.run(), "it belongs in roles/design/")

    def test_a_corpus_file_left_outside_the_trees_is_a_defect(self):
        """The half-done move, from the other side: the old layout still resolves, and that is
        exactly why it needs saying. `kb` finds the file; the partition says it is in the wrong
        place, which is the difference between a citation that opens and a tree that is true."""
        with Fake() as f:
            self.base(f)
            refs = os.path.join(f.skills, "alpha", "references")
            os.makedirs(refs)
            with open(os.path.join(refs, "stranded.md"),
                      "w", encoding="utf-8", newline="\n") as fh:
                fh.write(self.NOTE % ("alpha", "the move is half done"))
            self.only(f.run(), "is a corpus file outside the role trees")

    # -- 4: the skill declares the role that opens its card ------------------

    def test_a_card_whose_owner_does_not_declare_the_role_is_a_warn(self):
        """A warn, because the card is evidence and `metadata.role:` is a declaration: a
        disagreement is a stale declaration far more often than it is a misfiled card."""
        with Fake() as f:
            f.skill("alpha", frontmatter=self.SKILL % ("alpha", "design", "alpha-thing"))
            f.role_file("alpha", "draft-card.md",
                        self.CARD % ("draft-card", "alpha", "write-chapter", "Decide it."))
            rep = f.run()
            self.only(rep, "does not declare `metadata.role: draft`", level="warn")
            self.assertEqual(self.messages(rep), [])

    def test_a_note_in_another_role_s_tree_is_not_a_warn(self):
        """Scoped to cards, and the wider form was tried first and is wrong.

        A note's bucket is a property of the citation *graph* - who cites it - while
        `metadata.role:` is a property of the *skill*, and the two diverge legitimately wherever
        a merged card names a second owner. Here `alpha`'s draft card cites `beta`'s note, so
        the note sits in the drafter's tree while `beta` remains a design-only skill; the wide
        form fired on six such cases in the real repo, which is how a warn stops being read.
        """
        with Fake() as f:
            f.skill("alpha", frontmatter=self.SKILL % ("alpha", "draft", "alpha-thing"))
            f.skill("beta", body="See roles/draft/beta.ladders.md",
                    frontmatter=self.SKILL % ("beta", "design", "beta-thing"))
            f.role_file("alpha", "draft-card.md",
                        self.CARD % ("draft-card", "alpha", "write-chapter",
                                     "Decide it. See roles/draft/beta.ladders.md"))
            f.role_file("beta", "ladders.md", self.NOTE % ("beta", "an arc advances"),
                        bucket="draft")
            rep = f.run()
            self.assertEqual(self.messages(rep), [])
            self.assertEqual(self.messages(rep, "warn"), [])

    # -- 5: no writing role is sent into `docs/` -----------------------------

    def test_a_role_file_that_cites_docs_is_a_defect(self):
        """Without this the ban is one sentence in `AGENTS.md`, held by goodwill - and 15
        citations had already crossed it, every one maintainer-facing provenance sitting in a
        file addressed to a drafter."""
        with Fake() as f:
            self.base(f)
            f.role_file("alpha", "draft-card.md",
                        self.CARD % ("draft-card", "alpha", "write-chapter",
                                     "Decide it. See roles/draft/alpha.notes.md.\n\n"
                                     "The budget is why: docs/creative-latitude.md."))
            msg = self.only(f.run(), "which its own role may not open")
            self.assertIn("docs/creative-latitude.md", msg)

    def test_provenance_in_frontmatter_is_not_a_citation(self):
        """The fix the ban is paired with. Frontmatter costs no body words and cannot read as
        an instruction, so the rationale stays attached to the file for whoever maintains it."""
        with Fake() as f:
            self.base(f)
            f.role_file("alpha", "draft-card.md",
                        "---\ntype: draft-card\nowner: alpha\ndispatcher: write-chapter\n"
                        "provenance: docs/creative-latitude.md\n---\n\n"
                        "# card\n\nDecide it. See roles/draft/alpha.notes.md\n")
            self.assertEqual(self.messages(f.run()), [])

    def test_the_design_tree_may_cite_docs(self):
        """`design` is the one role that is not denied `docs/`, and it is the role that reads
        the rationale. Binding it would push maintainer argument out of the tree it belongs in."""
        with Fake() as f:
            f.skill("alpha", body="Background: roles/design/alpha.rationale.md",
                    frontmatter=self.SKILL % ("alpha", "design", "alpha-thing"))
            f.role_file("alpha", "rationale.md",
                        "---\ntype: reference\nowner: alpha\n---\n\n# why\n\n"
                        "Open this when editing the skill. See docs/design-notes.md.\n",
                        bucket="design")
            self.assertEqual(self.messages(f.run()), [])


class TestTheReaderSplit(unittest.TestCase):
    """The reader's brief and the maintainer's procedure must not converge.

    They were one file, and splitting them is what stops a cold read arriving already knowing the
    chapters are being measured. The failure mode is silent: edit the questions in the procedure -
    the file a maintainer naturally opens - and the reader goes on answering the old ones. It
    happened for a day, ten lines deep, and `_overlap` could not see it because that check
    compares *skills* and these two files declare no owner.
    """

    BRIEF = "roles/review/reader-brief.md"
    PROC = "roles/review/reader-review.md"

    def pair(self, d, brief, proc):
        os.makedirs(os.path.join(d, "roles", "review"))
        for rel, text in ((self.BRIEF, brief), (self.PROC, proc)):
            with open(os.path.join(d, rel), "w", encoding="utf-8", newline="\n") as fh:
                fh.write(text)

    def run_check(self, d):
        rep = Report()
        cmd_health._review_split(d, rep)
        return [f.message for f in rep.findings if f.check == "review-split"]

    def test_a_shared_long_line_is_a_defect(self):
        with Fake() as f:
            shared = "Name the story in one sentence you would give a friend, and say so.\n"
            self.pair(f.dir, "# brief\n\n" + shared, "# procedure\n\n" + shared)
            found = self.run_check(f.dir)
            self.assertEqual(len(found), 1, found)
            self.assertIn("verbatim in both", found[0])

    def test_a_short_shared_line_is_not(self):
        """A heading or a stock phrase is not a copied instrument, and flagging one would make
        the check noise within a week."""
        with Fake() as f:
            self.pair(f.dir, "# brief\n\nRead it once.\n", "# procedure\n\nRead it once.\n")
            self.assertEqual(self.run_check(f.dir), [])

    def test_citing_instead_of_restating_is_clean(self):
        with Fake() as f:
            self.pair(f.dir,
                      "# brief\n\nName the story in one sentence you would give a friend here.\n",
                      "# procedure\n\nThe instrument is the brief and it is not restated in "
                      "this file at all.\n")
            self.assertEqual(self.run_check(f.dir), [])

    def test_a_repo_without_the_pair_is_silent(self):
        with Fake() as f:
            self.assertEqual(self.run_check(f.dir), [])

    def test_many_shared_lines_are_summarised_rather_than_listed(self):
        """Twenty defects for one mistake is twenty lines nobody reads to the end of."""
        with Fake() as f:
            block = "".join("Shared instrument line number %d of the table here.\n" % i
                            for i in range(9))
            self.pair(f.dir, "# brief\n\n" + block, "# procedure\n\n" + block)
            found = self.run_check(f.dir)
            self.assertEqual(len(found), 4, found)
            self.assertIn("9 lines are verbatim", found[-1])

    def test_this_repo_keeps_them_apart(self):
        rep_paths = [os.path.join(REPO, r) for r in cmd_health.REVIEW_PAIR]
        for p in rep_paths:
            self.assertTrue(os.path.isfile(p), p)
        self.assertEqual(self.run_check(REPO), [])



if __name__ == "__main__":
    unittest.main()
