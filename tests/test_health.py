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

from swlib import cmd_health


def checks(rep, level="defect"):
    return {f.check for f in rep.findings if f.level == level}


class Fake(object):
    """A minimal repo: .claude/skills plus whatever the test writes."""

    def __enter__(self):
        self.dir = tempfile.mkdtemp(prefix="sw-health-")
        self.skills = os.path.join(self.dir, ".claude", "skills")
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
            rd = os.path.join(d, "references")
            if not os.path.isdir(rd):
                os.makedirs(rd)
            with open(os.path.join(rd, fname), "w", encoding="utf-8", newline="\n") as fh:
                fh.write(text)
        return d

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


if __name__ == "__main__":
    unittest.main()
