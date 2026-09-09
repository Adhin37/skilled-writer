"""The four channels. Every case here was a real defect in the first parser.

Each test names the observed wrong behaviour in its docstring, so a regression reads as the
sentence that describes it rather than as an assertion number.
"""

import unittest

from fixtures import MULTI_PARAGRAPH_SPEECH, NOVEL_MD, NovelFixture
from swlib.textstats import Channels, find_speech_spans

C = Channels()


def spans(text, channels=C):
    return [text[s:e] for s, e in find_speech_spans(text, channels)]


class TestSpeechSpans(unittest.TestCase):

    def test_multi_paragraph_speech_is_all_speech(self):
        """Was: 2 spans, paragraph three counted as narration, share 40% against a true ~70%."""
        found = spans(MULTI_PARAGRAPH_SPEECH)
        self.assertEqual(len(found), 3)
        self.assertIn("By the fourth day", found[2])
        self.assertTrue(found[1].startswith('"We waited three days'))

    def test_multi_paragraph_share_matches_hand_count(self):
        with NovelFixture() as fx:
            fx.add_chapter(1, MULTI_PARAGRAPH_SPEECH)
            ch = fx.novel().chapters()[0]
            # Hand count: every word of the three quoted paragraphs is speech. The only
            # narration is "she said." and "The rain had not stopped since." — eight words.
            body_words = len(ch.body.split())
            expected = (body_words - 8) * 100.0 / body_words
            self.assertAlmostEqual(ch.speech_share, expected, delta=2.0)
            self.assertGreater(ch.speech_share, 60.0)

    def test_unmatched_quote_stops_at_the_paragraph(self):
        """Was: `[^"]*` matched newlines, so one span swallowed text to the next quote."""
        text = '"Go, she said.\n\nThe room was cold and the lamp was out.\n\n"Now."\n'
        for span in spans(text):
            self.assertNotIn("The room was cold", span)

    def test_curly_and_mixed_speech_marks(self):
        self.assertEqual(len(spans("“Go on,” she said.")), 1)
        self.assertEqual(len(spans('"Go on," she said.')), 1)
        self.assertEqual(len(spans('“Go on," she said.')), 1)

    def test_stray_closing_mark_opens_nothing(self):
        self.assertEqual(spans("She left.” The door shut."), [])


class TestThought(unittest.TestCase):

    def test_straight_thought(self):
        self.assertEqual(len(C.thought_re.findall("'Start with what you're sure of.'")), 1)

    def test_curly_thought(self):
        """Was: 0 hits. The budget silently never tripped and lint printed `thought 0/3`."""
        self.assertEqual(
            len(C.thought_re.findall("‘Start with what you’re sure of.’")), 1)

    def test_contractions_and_possessives_are_not_thoughts(self):
        self.assertEqual(
            len(C.thought_re.findall("She didn't move. The boys' room was empty.")), 0)

    def test_thought_inside_speech_is_not_counted_as_thought(self):
        with NovelFixture() as fx:
            fx.add_chapter(1, '"He said \'no\' twice," she told him.\n')
            ch = fx.novel().chapters()[0]
            self.assertEqual(len(ch.thoughts()), 0)
            self.assertEqual(ch.nested_thought_in_speech(), 1)


class TestUnterminatedThoughts(unittest.TestCase):

    def test_elisions_are_words_not_open_marks(self):
        """Was: 'twas, 'em and '99 each raised a DEFECT."""
        with NovelFixture() as fx:
            fx.add_chapter(1, "'twas nothing at all.\n\nShe grabbed 'em and ran.\n\n"
                              "The year was '99 and cold.\n")
            ch = fx.novel().chapters()[0]
            self.assertEqual(ch.unterminated_thoughts(), [])

    def test_a_genuinely_open_mark_still_reports(self):
        with NovelFixture() as fx:
            fx.add_chapter(1, "'Start with what you are sure of and work outwards\n")
            ch = fx.novel().chapters()[0]
            self.assertEqual(len(ch.unterminated_thoughts()), 1)


class TestChannelsFromConfig(unittest.TestCase):
    """`channels:` in novel.md decides the marks. It used to be documented and ignored."""

    def test_config_marks_are_read(self):
        swapped = NOVEL_MD.replace('thought: "\'…\'"', 'thought: "«…»"')
        with NovelFixture(novel_md=swapped) as fx:
            fx.add_chapter(1, "«Start with what you are sure of.»\n\n"
                              "'This is not a thought any more.'\n")
            ch = fx.novel().chapters()[0]
            self.assertEqual(len(ch.thoughts()), 1)
            self.assertIn("Start with what", ch.thoughts()[0].group(0))


if __name__ == "__main__":
    unittest.main()


class TestSceneBreaksAndMarkup(unittest.TestCase):
    """Benchmark run #2, F3. Both checks existed and neither fired.

    The scene-break check enumerated the wrong forms (`***`, `---`, `~~~`, `===`, `* * * *`) and
    so missed a lone `*` — the malformation a real writing agent produced three times. And
    `STRAY_MARKUP` had a rule for `**bold**` and none for `*italic*`, so an italicised direct
    thought, the exact hard-rule-7 violation the four channels exist to prevent, passed silently.
    """

    def _checks(self, body):
        from swlib import cmd_lint
        with NovelFixture() as fx:
            fx.add_chapter(1, body)
            novel = fx.novel()
            rep = cmd_lint.lint_chapter(novel, novel.chapters()[0])
            return [(f.check, f.level) for f in rep.findings]

    def test_a_lone_star_is_not_a_scene_break(self):
        """Was: `breaks 0`, no finding — it matched neither the blocklist nor a list bullet."""
        found = self._checks("She stopped.\n\n*\n\nThe corridor was empty.\n")
        self.assertIn(("scene-break", "warn"), found)

    def test_a_well_formed_break_stays_clean(self):
        found = self._checks("She stopped.\n\n* * *\n\nThe corridor was empty.\n")
        self.assertNotIn("scene-break", [c for c, _ in found])
        self.assertNotIn("markup", [c for c, _ in found])

    def test_other_break_shapes_are_still_caught(self):
        for shape in ("***", "---", "~~~", "===", "* * * *", "___"):
            found = self._checks("She stopped.\n\n%s\n\nIt was empty.\n" % shape)
            self.assertIn(("scene-break", "warn"), found, "%r passed as a scene break" % shape)

    def test_an_italicised_thought_is_markup(self):
        """Was: `thought 0/3` and no finding — italics had no rule at all."""
        found = self._checks("She ran.\n\n*She would not make it in time.*\n\nThe gate closed.\n")
        self.assertIn(("markup", "defect"), found)

    def test_underscore_italics_are_markup_but_snake_case_is_not(self):
        self.assertIn(("markup", "defect"),
                      self._checks("She ran.\n\n_She would not make it._\n\nIt closed.\n"))
        self.assertNotIn("markup", [c for c, _ in
                                    self._checks("He read the word some_file_name aloud.\n")])

    def test_bold_still_reports_as_bold_not_italics(self):
        """The italic rule sits after the bold rule and must not steal its hits."""
        from swlib import cmd_lint
        with NovelFixture() as fx:
            fx.add_chapter(1, "She ran.\n\n**She would not make it.**\n\nIt closed.\n")
            novel = fx.novel()
            rep = cmd_lint.lint_chapter(novel, novel.chapters()[0])
            detail = " ".join(str(f.message) + str(f.detail or "") for f in rep.findings
                              if f.check == "markup")
            self.assertIn("bold", detail)

    def test_arithmetic_and_spaced_stars_are_not_italics(self):
        for body in ("The answer was 3 * 4 * 5 and nothing else.\n",
                     "She counted 2 * 2 again.\n"):
            self.assertNotIn("markup", [c for c, _ in self._checks(body)], body)


class TestDialogueTexture(unittest.TestCase):
    """Benchmark run #2 shipped five chapters at a healthy 25% speech share that a reader called
    stiff and unnatural — complete grammatical sentences, nobody ever cut off, every line
    carrying exposition. Share says how *much* the cast speaks and nothing about how it sounds.

    These are diagnostics and none of them is a gate: a number that decides whether a chapter
    ships gets optimised, which this repo has now learned twice.
    """

    def _ch(self, body):
        with NovelFixture() as fx:
            fx.add_chapter(1, body)
            return fx.novel().chapters()[0]

    STIFF = ('"Tuesday\'s count was for the north wall kit." she said.\n\n'
             '"That is not what the requisition record indicates."\n\n'
             '"The record reflects the district set and not the perimeter set."\n')
    REAL = ('"Tuesday\'s count—"\n\n"No."\n\n"What?"\n\n'
            '"You heard me. Don\'t make me say it twice."\n')

    def test_a_cut_off_line_is_counted(self):
        self.assertEqual(self._ch(self.STIFF).speech_interruptions, 0)
        self.assertGreater(self._ch(self.REAL).speech_interruptions, 0)

    def test_fragments_are_distinguished_from_complete_sentences(self):
        self.assertLess(self._ch(self.STIFF).speech_fragment_share, 40.0)
        self.assertGreater(self._ch(self.REAL).speech_fragment_share, 60.0)

    def test_contraction_rate_separates_the_two_registers(self):
        self.assertLess(self._ch(self.STIFF).speech_contraction_rate,
                        self._ch(self.REAL).speech_contraction_rate)

    def test_narration_between_lines_measures_buried_dialogue(self):
        buried = self._ch('"One."\n\n%s\n\n"Two."\n' % (" ".join(["word"] * 80)))
        quick = self._ch('"One."\n\n"Two."\n')
        self.assertGreater(buried.narration_between_speech, 50)
        self.assertLess(quick.narration_between_speech, 10)

    def test_an_exchange_needs_lines_that_are_actually_adjacent(self):
        """A line, three paragraphs of analysis, another line is not a conversation."""
        buried = self._ch('"One."\n\n%s\n\n"Two."\n' % (" ".join(["word"] * 80)))
        quick = self._ch('"One."\n\n"Two."\n\n"Three."\n')
        self.assertEqual(buried.speech_exchange_runs[1], 1)
        self.assertEqual(quick.speech_exchange_runs[1], 3)

    def test_line_length_spread_is_zero_for_uniform_lines(self):
        self.assertEqual(self._ch('"One two three."\n\n"Four five six."\n').speech_line_spread,
                         0.0)

    def test_none_of_the_texture_findings_is_a_gate(self):
        """They are notes. Making one a defect is how the dialogue share got gamed."""
        from swlib import cmd_lint
        with NovelFixture() as fx:
            fx.add_chapter(1, self.STIFF * 3)
            novel = fx.novel()
            rep = cmd_lint.lint_chapter(novel, novel.chapters()[0])
            levels = {f.level for f in rep.findings if f.check == "texture"}
            self.assertTrue(levels, "no texture findings fired on deliberately stiff dialogue")
            self.assertEqual(levels, {"note"})


class TestPacingMarkers(unittest.TestCase):
    """A reader reported the novel "goes fast to the finish line" while every command called it
    clean. The measured signature is a turn reported inside a past-perfect clause: chapter 1's
    build-up — four earlier attempts and three weeks of scheming — was two subordinate clauses.

    These locate that. They settle nothing, and they are notes: a chapter can skip its most
    important beat with no marker at all, by starting after it.
    """

    def _ch(self, body):
        with NovelFixture() as fx:
            fx.add_chapter(1, body)
            return fx.novel().chapters()[0]

    def test_the_real_chapter_one_sentences_are_caught(self):
        for line in ("She had made this exact lie four times in six weeks.\n",
                     "She had spent three weeks making it true.\n"):
            self.assertTrue(self._ch(line).summary_markers(),
                            "missed a reported event: %r" % line)

    def test_ordinary_past_perfect_is_not_a_marker(self):
        """`had` orders two past events in normal English; only a reported *event* counts."""
        for line in ("The door had closed before she reached it.\n",
                     "He had never seen the wards lit.\n",
                     "She had the ledger open on her knee.\n"):
            self.assertEqual(self._ch(line).summary_markers(), [],
                             "false positive on: %r" % line)

    def test_time_compression_is_caught(self):
        for line in ("Over the next month she learned to read the wards.\n",
                     "By the time he arrived, the argument was over.\n",
                     "Three weeks passed before anyone noticed.\n"):
            self.assertTrue(self._ch(line).summary_markers(), "missed: %r" % line)

    def test_markers_inside_dialogue_are_not_counted(self):
        """A character may report their own past aloud; that is speech, not narration."""
        self.assertEqual(
            self._ch('"I had spent three weeks making it true," she said.\n').summary_markers(),
            [])

    def test_words_before_the_first_scene(self):
        body = "%s\n\n\"Two short,\" she said.\n" % " ".join(["word"] * 50)
        self.assertGreaterEqual(self._ch(body).words_before_first_scene, 50)
        self.assertLess(self._ch('"Go," she said.\n').words_before_first_scene, 5)

    def test_the_pacing_findings_are_only_ever_notes(self):
        """Two numeric gates in this repo have already been optimised rather than satisfied."""
        from swlib import cmd_lint
        body = ("She had spent three weeks making it true. Over the next month she learned the "
                "wards. By the time he arrived, the argument was over. She had made this exact "
                "lie four times in six weeks. Three weeks passed.\n")
        with NovelFixture() as fx:
            fx.add_chapter(1, body)
            novel = fx.novel()
            rep = cmd_lint.lint_chapter(novel, novel.chapters()[0])
            levels = {f.level for f in rep.findings if f.check == "pacing"}
            self.assertTrue(levels, "no pacing finding on deliberately reported prose")
            self.assertEqual(levels, {"note"})
