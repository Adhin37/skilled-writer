"""`sw cast` - the two checks benchmark run #2's reader found by reading, and no tool had.

The reader's report was: "I already have issues with dialogue - it doesn't seem like people
speaking normally" and then, more precisely, "they are not even introduced. It feels like I should
know them and everything in their life." Both were true of a novel on which every command
reported clean.
"""

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
