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
