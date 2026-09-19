"""`sw cast` - the two checks benchmark run #2's reader found by reading, and no tool had.

The reader's report was: "I already have issues with dialogue - it doesn't seem like people
speaking normally" and then, more precisely, "they are not even introduced. It feels like I should
know them and everything in their life." Both were true of a novel on which every command
reported clean.
"""

import re
import unittest

from fixtures import NovelFixture, NOVEL_MD  # noqa: F401

from swlib import cmd_cast

VOICES = """# Cast voice matrix

## 1. THE MATRIX

| character | tier | intel | artic | wit | heat | turn | hands | pressure | first move |
|---|---|---|---|---|---|---|---|---|---|
%s
"""


def voices(*rows):
    return VOICES % "\n".join(rows)


def findings(rep, level=None):
    return [(f.check, f.level) for f in rep.findings
            if level is None or f.level == level]


class TestNearClash(unittest.TestCase):
    """`three-way-clash` needs intel + artic + wit to match. Run #2's two chapter-1 speakers were
    intel 3 / artic 3 and differed only in a `wit` label, so it passed them - correctly, and
    uselessly, because wit can go a whole chapter without surfacing.
    """

    MC = "| Ana | MC | 3 | 3 | dry | flat | 14 | taps | still | the door |"

    def _run(self, *rows):
        with NovelFixture() as fx:
            fx.write("bible/cast/_voices.md", voices(self.MC, *rows))
            fx.add_chapter(1, '"Go on," she said.\n')
            return cmd_cast.run(fx.novel())

    def test_two_speakers_alike_but_for_wit_are_a_warn(self):
        rep = self._run("| Bo | A | 3 | 3 | none | flat | 10 | still | busy | the board |",
                        "| Cy | B | 1 | 2 | warm | quick | 8 | rubs | smaller | the floor |")
        self.assertIn(("near-clash", "warn"), findings(rep))

    def test_it_is_never_a_defect(self):
        """Two people can legitimately reason alike, and a declared mirror is exactly that."""
        rep = self._run("| Bo | A | 3 | 3 | none | flat | 10 | still | busy | the board |",
                        "| Cy | B | 1 | 2 | warm | quick | 8 | rubs | smaller | the floor |")
        self.assertEqual([c for c, lv in findings(rep, "defect") if c == "near-clash"], [])

    def test_a_cast_separated_on_intel_or_artic_is_clean(self):
        rep = self._run("| Bo | A | 4 | 2 | none | flat | 10 | still | busy | the board |",
                        "| Cy | B | 1 | 3 | warm | quick | 8 | rubs | smaller | the floor |")
        self.assertNotIn("near-clash", [c for c, _ in findings(rep)])


class TestDebutLedger(unittest.TestCase):
    """Nothing looked at a character's *first* appearance, so a name could walk on with no
    placement and every check stayed green.
    """

    def _debuts(self, body, *rows):
        with NovelFixture() as fx:
            fx.write("bible/cast/_voices.md", voices(*rows))
            fx.add_chapter(1, body)
            rep = cmd_cast.run(fx.novel())
            for heading, lines in rep.sections:
                if heading == "debuts":
                    return lines
            return []

    ROWS = ("| Ana | MC | 3 | 3 | dry | flat | 14 | taps | still | the door |",
            "| Bo | A | 1 | 2 | warm | quick | 8 | rubs | smaller | the floor |")

    def test_it_reports_where_each_character_arrives(self):
        lines = self._debuts("Ana counted them twice.\n\nShe went to find Bo.\n\n"
                             '"Two short," she said.\n', *self.ROWS)
        joined = " ".join(lines)
        self.assertIn("Ana", joined)
        self.assertIn("Bo", joined)

    def test_it_prints_which_name_token_matched(self):
        """A clan name shared with the world can match before the person does, and no counting
        rule separates the two - so the ledger shows its working instead of guessing."""
        lines = self._debuts("The Kito compound wall was long.\n\nKito Ren opened the door.\n",
                             "| Kito Ren | A | 2 | 2 | none | flat | 9 | still | busy | away |")
        self.assertTrue(any("Kito" in l for l in lines))

    def test_it_measures_the_gap_before_a_character_speaks(self):
        lines = self._debuts("Bo was there.\n\n%s\n\n\"Now,\" Bo said.\n" % " ".join(["word"] * 60),
                             *self.ROWS)
        row = [l for l in lines if l.strip().startswith("Bo")]
        self.assertTrue(row and "words" in row[0])

    def test_it_is_information_only(self):
        with NovelFixture() as fx:
            fx.write("bible/cast/_voices.md", voices(*self.ROWS))
            fx.add_chapter(1, "Ana counted.\n\nBo arrived.\n")
            rep = cmd_cast.run(fx.novel())
            self.assertEqual([c for c, lv in findings(rep) if c == "debuts"], [])


class TestAlternationRecovery(unittest.TestCase):
    """Benchmark run #5, O14. Attribution needs a cast name in the narration around a line, so a
    well-written untagged two-hander — the scene a writer is supposed to be able to leave untagged
    — scored 4 of 52 lines, `_cadence` bailed under its four-sentence floor, and run #3's cadence
    test never ran on the one chapter where two characters demonstrably shared a cadence. The
    instrument went blind exactly where the prose got good.

    The recovery never assumes the convention, it checks it: a gap is filled only when the
    attributed turns bracketing it agree on parity, so a scene that is not strictly alternating
    reports nothing rather than reporting a guess.
    """

    ROWS = ("| Ana | MC | 3 | 3 | dry | flat | 6 | taps | still | the door |",
            "| Bo | A | 1 | 2 | warm | quick | 9 | rubs | smaller | the floor |")

    def _lines(self, body):
        with NovelFixture() as fx:
            fx.write("bible/cast/_voices.md", voices(*self.ROWS))
            fx.add_chapter(1, body)
            rep = cmd_cast.run(fx.novel())
        for heading, lines in rep.sections:
            if heading.startswith("turn length"):
                return lines
        return []

    def _recovered(self, body):
        for line in self._lines(body):
            m = re.search(r"(\d+) more recovered", line)
            if m:
                return int(m.group(1))
        return 0

    def _count(self, name, body):
        for line in self._lines(body):
            parts = line.split()
            if parts and parts[0] == name:
                return int(parts[3])          # character, declared, measured, lines
        return 0

    # Ana and Bo tag the outer turns; the four between them are bare quotes. Four unattributed
    # turns and an even gap means the run ends on the speaker it started with — consistent.
    ALTERNATING = "\n\n".join([
        'Ana set the slip down. "One two three four five six," she said.',
        '"Seven eight nine ten eleven twelve."',
        '"Thirteen fourteen fifteen sixteen."',
        '"Seventeen eighteen nineteen twenty."',
        '"Twenty-one twenty-two twenty-three."',
        'Bo pushed it back. "Twenty-four twenty-five twenty-six," Bo said.',
    ]).replace("she said", "Ana said")

    def test_a_bracketed_run_is_recovered(self):
        self.assertEqual(self._recovered(self.ALTERNATING), 4)

    def test_recovered_turns_reach_the_speakers_own_row(self):
        """The point of the recovery: a per-speaker number that was n=1 becomes a sample."""
        self.assertEqual(self._count("Ana", self.ALTERNATING), 3)
        self.assertEqual(self._count("Bo", self.ALTERNATING), 3)

    def test_a_run_whose_ends_disagree_on_parity_stays_unattributed(self):
        """Two turns between two tags by the same speaker cannot be strict alternation — it would
        land the second tag on Bo. The scene is one this cannot read, so it says nothing rather
        than guessing."""
        body = "\n\n".join([
            'Ana set the slip down. "One two three," Ana said.',
            '"Four five six seven."',
            '"Eight nine ten eleven."',
            'Ana pushed it back. "Fifteen sixteen," Ana said.',
            'Bo shrugged. "Seventeen eighteen," Bo said.',
        ])
        self.assertEqual(self._recovered(body), 0)

    def test_nothing_is_recovered_before_the_first_tag_or_after_the_last(self):
        """An unbracketed run has only one end to check against, which is not a check."""
        body = "\n\n".join([
            '"One two three four."',
            '"Five six seven eight."',
            'Ana looked up. "Nine ten eleven," Ana said.',
            'Bo looked back. "Twelve thirteen," Bo said.',
            '"Fourteen fifteen sixteen."',
        ])
        self.assertEqual(self._recovered(body), 0)

    def test_a_third_speaker_switches_the_recovery_off(self):
        """Alternation is a two-speaker convention. With three on the page the next line is a
        choice, not a turn order, and `scene-craft` says so."""
        rows = self.ROWS + ("| Cy | B | 2 | 2 | none | flat | 7 | still | busy | the wall |",)
        body = self.ALTERNATING + '\n\nCy shook his head. "Twenty-seven twenty-eight," Cy said.'
        with NovelFixture() as fx:
            fx.write("bible/cast/_voices.md", voices(*rows))
            fx.add_chapter(1, body)
            rep = cmd_cast.run(fx.novel())
        text = " ".join(l for h, ls in rep.sections if h.startswith("turn length") for l in ls)
        self.assertNotIn("recovered by alternation", text)

    def test_recovery_does_not_reach_across_a_scene_break(self):
        """Two scenes are two conversations. Bracketing across the break would pair the last turn
        of one with the first of the next, which is not a bracket at all."""
        body = "\n\n".join([
            'Ana set it down. "One two three," Ana said.',
            '"Four five six seven."',
            "* * *",
            '"Eight nine ten eleven."',
            'Bo pushed it back. "Twelve thirteen," Bo said.',
        ])
        self.assertEqual(self._recovered(body), 0)


PROFILE = """---
name: "%s"
tier: A
role: supporting
first_appears: %s
status: alive
---

# %s
"""


class TestFirstAppearsIsRead(unittest.TestCase):
    """`first_appears:` has sat in both cast templates since the scaffold was written and was
    read by nothing at all, which is how it came to be wrong in two of benchmark run #5's seven
    profiles. It is also exactly the field a tool needs to check CLAUDE.md rule 8's clause that
    every named character is placed before they carry a scene, and the debut ledger beside it
    already knows the true answer.
    """

    ROWS = ("| Ana | MC | 3 | 3 | dry | flat | 14 | taps | still | the door |",
            "| Bo | A | 1 | 2 | warm | quick | 8 | rubs | smaller | the floor |")

    def _run(self, first_appears, body=None):
        body = body or "Ana counted them twice.\n\nBo came in late.\n"
        with NovelFixture() as fx:
            fx.write("bible/cast/_voices.md", voices(*self.ROWS))
            fx.write("bible/cast/bo.md", PROFILE % ("Bo", first_appears, "Bo"))
            fx.add_chapter(1, body)
            return cmd_cast.run(fx.novel())

    def test_a_wrong_first_appears_is_named(self):
        msgs = [f.message for f in self._run(4).findings if f.check == "first-appears"]
        self.assertTrue(msgs)
        self.assertIn("Bo", msgs[0])
        self.assertIn("4", msgs[0])

    def test_the_true_chapter_is_printed_beside_the_declared_one(self):
        """The finding is only useful if it says what to write instead."""
        msgs = [f.message for f in self._run(4).findings if f.check == "first-appears"]
        self.assertIn("1", msgs[0])

    def test_a_correct_first_appears_says_nothing(self):
        rep = self._run(1)
        self.assertEqual([f for f in rep.findings if f.check == "first-appears"], [])

    def test_an_unset_first_appears_says_nothing(self):
        """The template ships `0`, and a scaffold that has not been filled in yet is not a
        defect - `novel-init` owns that, and nagging about it here would fire on every new
        novel before a word is written."""
        rep = self._run(0)
        self.assertEqual([f for f in rep.findings if f.check == "first-appears"], [])

    def test_it_is_never_more_than_a_note(self):
        """A character who genuinely first appears offstage, or in a chapter the read-set does
        not reach, is a legitimate reason for the field to disagree with the prose."""
        for f in self._run(4).findings:
            if f.check == "first-appears":
                self.assertEqual(f.level, "note")

    def test_a_character_outside_the_read_window_is_not_guessed_at(self):
        """A name that never appears in any chapter on disk has no measured debut to compare
        against, so there is nothing to say."""
        with NovelFixture() as fx:
            fx.write("bible/cast/_voices.md", voices(*self.ROWS))
            fx.write("bible/cast/cy.md", PROFILE % ("Cy", 9, "Cy"))
            fx.add_chapter(1, "Ana counted them twice.\n")
            rep = cmd_cast.run(fx.novel())
            self.assertEqual([f for f in rep.findings if f.check == "first-appears"], [])


class TestTurnLength(unittest.TestCase):
    """`sw lint`'s texture line is a mean across all speakers, so one character's turns can
    double while the chapter average stays healthy. Run #2's revising agent found exactly that
    by hand — the MC declared `turn: 14` and ran to 23.4 words in the two scenes that mattered —
    and named it as the reason the defect survived several revision passes.
    """

    ROWS = ("| Ana | MC | 3 | 3 | dry | flat | 6 | taps | still | the door |",
            "| Bo | A | 1 | 2 | warm | quick | 9 | rubs | smaller | the floor |")

    def _run(self, body):
        with NovelFixture() as fx:
            fx.write("bible/cast/_voices.md", voices(*self.ROWS))
            fx.add_chapter(1, body)
            return cmd_cast.run(fx.novel())

    LONG = "\n\n".join(
        ['Ana looked up. "%s," Ana said.' % (" ".join(["word"] * 30)) for _ in range(5)])

    def test_a_dialogue_tag_does_not_halve_a_speakers_turn(self):
        """Run #3, T4, second home. The span-vs-turn bug was fixed in `textstats` for the chapter
        mean and survived HERE, re-implemented, in the per-speaker view that exists precisely to
        catch what a chapter mean hides. Splitting one 30-word turn with a tag must not read as
        two 15-word turns."""
        rows = ("| Ana | MC | 3 | 3 | dry | flat | 20 | taps | still | the door |",
                "| Bo | A | 1 | 2 | warm | quick | 9 | rubs | smaller | the floor |")

        def run(body):
            with NovelFixture() as fx:
                fx.write("bible/cast/_voices.md", voices(*rows))
                fx.add_chapter(1, body)
                return findings(cmd_cast.run(fx.novel()))

        # Declared 20. One 30-word turn is +50% and must be noted; split by a tag it used to
        # measure as two 15-word turns, which is -25% and inside tolerance - the drift vanished.
        whole = "\n\n".join(['Ana looked up. "%s," Ana said.' % (" ".join(["word"] * 30))
                              for _ in range(5)])
        tagged = "\n\n".join(['Ana looked up. "%s," Ana said. "%s"'
                               % (" ".join(["word"] * 15), " ".join(["word"] * 15))
                               for _ in range(5)])
        self.assertIn(("turn-drift", "note"), run(whole))
        self.assertIn(("turn-drift", "note"), run(tagged),
                      "a dialogue tag hid a speaker's real turn length")

    def test_a_speaker_far_off_their_declared_turn_is_noted(self):
        rep = self._run(self.LONG)
        self.assertIn(("turn-drift", "note"), findings(rep))

    def test_it_is_never_a_defect(self):
        rep = self._run(self.LONG)
        self.assertEqual([c for c, lv in findings(rep, "defect") if c == "turn-drift"], [])

    def test_a_speaker_on_their_row_is_not_noted(self):
        body = "\n\n".join(['Ana looked up. "One two three four five six," Ana said.'
                            for _ in range(5)])
        self.assertNotIn("turn-drift", [c for c, _ in findings(self._run(body))])

    def test_too_few_attributed_lines_to_judge(self):
        """Three long lines is not evidence; the check must wait for a sample."""
        body = 'Ana looked up. "%s," Ana said.' % (" ".join(["word"] * 40))
        self.assertNotIn("turn-drift", [c for c, _ in findings(self._run(body))])

    def test_an_ambiguous_line_is_not_attributed(self):
        """Two cast names around a line means we do not know who spoke; count it for neither."""
        body = "\n\n".join(['Ana watched Bo. "%s," someone said.' % (" ".join(["word"] * 30))
                            for _ in range(6)])
        self.assertNotIn("turn-drift", [c for c, _ in findings(self._run(body))])


EQ_VOICES = """# Cast voice matrix

## 1. THE MATRIX

| character | tier | intel | eq | artic | wit | heat | turn | hands | pressure | first move |
|---|---|---|---|---|---|---|---|---|---|---|
%s
"""


def eq_voices(*rows):
    return EQ_VOICES % "\n".join(rows)


class TestEqAxis(unittest.TestCase):
    """`social-perception`: how well somebody reads people, as a column beside intel.

    The defect it exists to catch is cast-wide and invisible in a profile - everybody reasoning
    and reading at the same level, so nobody can be surprised by anyone. Every finding here is a
    warn except the one that contradicts `novel.md`, because a novel may legitimately not use the
    axis yet and should be told once rather than blocked.
    """

    # Rin is the fixture MC at intel_tier 3.
    MC = "| Rin | MC | 3 | 2 | 3 | dry | flat | 14 | taps | still | the door |"

    def _run(self, *rows, **kw):
        with NovelFixture() as fx:
            if kw.get("novel_md"):
                fx.write("novel.md", kw["novel_md"])
            fx.write("bible/cast/_voices.md", eq_voices(self.MC, *rows))
            fx.add_chapter(1, '"Go on," she said.\n')
            return cmd_cast.run(fx.novel())

    def test_a_matrix_with_no_eq_column_warns_once(self):
        with NovelFixture() as fx:
            fx.write("bible/cast/_voices.md",
                     voices("| Rin | MC | 3 | 3 | dry | flat | 14 | taps | still | the door |",
                            "| Bo | A | 4 | 2 | none | flat | 10 | still | busy | the board |"))
            fx.add_chapter(1, '"Go on," she said.\n')
            rep = cmd_cast.run(fx.novel())
        self.assertIn(("eq", "warn"), findings(rep))
        self.assertEqual([c for c, lv in findings(rep, "defect") if c == "eq"], [])

    def test_a_separated_cast_is_clean(self):
        rep = self._run("| Bo | A | 4 | 4 | 4 | none | flat | 10 | still | busy | the board |",
                        "| Cy | B | 2 | 3 | 2 | warm | quick | 8 | rubs | smaller | the floor |")
        self.assertEqual([c for c, lv in findings(rep) if c.startswith("eq")], [])

    def test_nobody_above_the_mc_warns(self):
        rep = self._run("| Bo | A | 4 | 1 | 4 | none | flat | 10 | still | busy | the board |",
                        "| Cy | B | 2 | 2 | 2 | warm | quick | 8 | rubs | smaller | the floor |")
        self.assertIn(("eq-straddle", "warn"), findings(rep))

    def test_a_cast_whose_eq_always_equals_intel_warns(self):
        """The single mind with several names - the shape this axis exists to break.

        Needs a flat MC too, so this one builds its own matrix rather than using the class row.
        """
        with NovelFixture() as fx:
            fx.write("bible/cast/_voices.md", eq_voices(
                "| Rin | MC | 3 | 3 | 3 | dry | flat | 14 | taps | still | the door |",
                "| Bo | A | 4 | 4 | 4 | none | flat | 10 | still | busy | the board |",
                "| Cy | B | 2 | 2 | 2 | warm | quick | 8 | rubs | smaller | the floor |"))
            fx.add_chapter(1, '"Go on," she said.\n')
            rep = cmd_cast.run(fx.novel())
        self.assertIn(("eq-flat", "warn"), findings(rep))

    def test_two_speakers_sharing_intel_and_eq_warn(self):
        rep = self._run("| Bo | A | 4 | 4 | 4 | none | flat | 10 | still | busy | the board |",
                        "| Cy | B | 4 | 4 | 2 | warm | quick | 8 | rubs | smaller | the floor |")
        self.assertIn(("eq-clash", "warn"), findings(rep))

    def test_the_matrix_must_agree_with_novel_md(self):
        """The one defect: a declared `mc.eq_tier` the matrix contradicts, as for intel_tier."""
        md = NOVEL_MD.replace("intel_tier: 3", "intel_tier: 3\n  eq_tier: 5")
        rep = self._run("| Bo | A | 4 | 4 | 4 | none | flat | 10 | still | busy | the board |",
                        novel_md=md)
        self.assertIn(("eq", "defect"), findings(rep))


CAST_FILE = """---
name: "%s"
tier: B
first_appears: 1
---

## Speech fingerprint

| field | value |
|---|---|
| register | clerical |
| contractions | %s |
"""


class TestSpeechFingerprint(unittest.TestCase):
    """The declared `contractions` cell, read against the page for the first time.

    Benchmark run #5: a guild master's file declared `never` and his dialogue carried ten. Nine
    cast rows in that novel declared the field and no command had ever opened one - `sw lint`
    pools every speaker into a single chapter-wide rate and only flags the low side, so the only
    thing that caught it was the drafter reading its own cast file during Pass 10.
    """

    MC = "| Rin | MC | 3 | 3 | dry | flat | 14 | taps | still | the door |"
    BO = "| Bo | A | 4 | 4 | none | flat | 10 | still | busy | the board |"
    CY = "| Cy | B | 2 | 2 | warm | quick | 8 | rubs | smaller | the floor |"

    def _run(self, declared, prose, who="Bo"):
        with NovelFixture() as fx:
            fx.write("bible/cast/_voices.md", voices(self.MC, self.BO, self.CY))
            fx.write("bible/cast/bo.md", CAST_FILE % (who, declared))
            fx.add_chapter(1, prose)
            return cmd_cast.run(fx.novel())

    CONTRACTS = ('"I don\'t know," Bo said.\n\n'
                 '"It isn\'t mine," Bo said.\n\n'
                 '"You can\'t have it," Bo said.\n\n'
                 '"That\'s the whole of it," Bo said.\n')
    PLAIN = ('"I do not know," Bo said.\n\n'
             '"It is not mine," Bo said.\n\n'
             '"You cannot have it," Bo said.\n\n'
             '"That is the whole of it," Bo said.\n')

    def test_declared_never_against_a_contracting_speaker_is_noted(self):
        rep = self._run("never", self.CONTRACTS)
        self.assertIn(("fingerprint", "note"), findings(rep))

    def test_declared_always_against_a_speaker_who_never_contracts_is_noted(self):
        rep = self._run("always", self.PLAIN)
        self.assertIn(("fingerprint", "note"), findings(rep))

    def test_a_kept_fingerprint_is_silent(self):
        rep = self._run("never", self.PLAIN)
        self.assertEqual([c for c, lv in findings(rep) if c == "fingerprint"], [])

    def test_it_is_never_more_than_a_note(self):
        """A character may break his own fingerprint because the scene is better for it. A
        number a chapter has to clear is a number somebody writes toward.
        """
        rep = self._run("never", self.CONTRACTS)
        self.assertEqual([lv for c, lv in findings(rep) if c == "fingerprint"], ["note"])

    def test_a_conditional_cell_is_left_to_judgement(self):
        """`drops them when lying` is not arithmetic, and a check that guesses gets optimised."""
        rep = self._run("drops them when formal", self.CONTRACTS)
        self.assertEqual([c for c, lv in findings(rep) if c == "fingerprint"], [])

    def test_too_few_attributed_turns_to_judge(self):
        rep = self._run("never", '"I don\'t know," Bo said.\n\n"It isn\'t mine," Bo said.\n')
        self.assertEqual([c for c, lv in findings(rep) if c == "fingerprint"], [])

    def test_a_cast_file_with_no_fingerprint_table_is_not_an_error(self):
        with NovelFixture() as fx:
            fx.write("bible/cast/_voices.md", voices(self.MC, self.BO, self.CY))
            fx.write("bible/cast/bo.md", '---\nname: "Bo"\ntier: B\n---\n\nNo table here.\n')
            fx.add_chapter(1, self.CONTRACTS)
            rep = cmd_cast.run(fx.novel())
        self.assertEqual([c for c, lv in findings(rep) if c == "fingerprint"], [])
