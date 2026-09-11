"""`sw health` finds the wiring defects it claims to, and finds none in this repo.

The second half is the load-bearing one: these checks exist so that somebody who edits a skill
learns they broke a pointer. If they were only ever run against synthetic fixtures, the repo
could drift out from under them exactly the way `plan_rows()` did.
"""

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

    def test_a_card_named_by_its_dispatcher_is_accepted(self):
        with Fake() as f:
            f.skill("write-chapter", body="open `alpha/references/draft-card.md` at step 1")
            f.skill("alpha", body="body", references={"draft-card.md": "# card"})
            self.assertNotIn("skill-card", checks(f.run()))

    def test_a_line_number_citation_is_a_defect(self):
        """`hook-and-pacing:38-39` rots silently the moment a paragraph is added above it."""
        with Fake() as f:
            f.skill("alpha", body="see hook-and-pacing:38-39 for the rule")
            self.assertIn("line-citation", checks(f.run()))

    def test_an_ordinary_section_citation_is_not_flagged(self):
        with Fake() as f:
            f.skill("alpha", body="see `hook-and-pacing` section Openings for the rule")
            self.assertNotIn("line-citation", checks(f.run()))


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
