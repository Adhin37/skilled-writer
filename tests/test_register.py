"""The register ledger, the event gate, and the house style.

All three come out of benchmark run #2, which shipped five chapters that passed every check this
toolkit had — zero MTL hits, zero cut-list phrases, `status: revised` — and which a reader
flagged as machine-written inside a page.

Nothing here scores a chapter. `event` is the one hard gate, because a chapter with no event is
a chapter with nothing to dramatize; everything else is a warn or a note, measured across a
window, for the reason `docs/design-notes.md` gives at length: a number that decides whether one
chapter ships is a number the next chapter gets written toward.
"""

import unittest

from fixtures import MULTI_PARAGRAPH_SPEECH, NovelFixture
from swlib import cmd_arc, cmd_lint, rules


def messages(rep):
    return [f.message for f in rep.findings]


def levels(rep, check):
    return [f.level for f in rep.findings if f.check == check]


def lint_one(fx, n=1):
    return cmd_lint.lint_chapter(fx.novel(), fx.novel().chapter(n))


class TestEventGate(unittest.TestCase):
    """`delivers:` asks for a difference and gets an abstraction. `event:` asks for the thing
    a reader could retell."""

    def test_an_abstract_state_is_rejected(self):
        with NovelFixture() as fx:
            fx.add_chapter(1, MULTI_PARAGRAPH_SPEECH,
                           event="the trust between them deepens")
            rep = lint_one(fx)
            self.assertIn("defect", levels(rep, "event"))

    def test_run_2s_actual_deliveries_would_have_been_caught(self):
        """Verbatim from the shipped novel. Every one names an effect, not an event."""
        for line in ("proximity that isn't refused",
                     "attention has moved one level up",
                     "Enko is now watching Suzune on purpose"):
            with NovelFixture() as fx:
                fx.add_chapter(1, MULTI_PARAGRAPH_SPEECH, event=line)
                self.assertIn("defect", levels(lint_one(fx), "event"),
                              "should have been rejected: %r" % line)

    def test_a_concrete_event_passes(self):
        with NovelFixture() as fx:
            fx.add_chapter(1, MULTI_PARAGRAPH_SPEECH,
                           event="Rin argues with the clerk and leaves without the permit")
            self.assertEqual(levels(lint_one(fx), "event"), [])

    def test_an_event_longer_than_a_clause_warns(self):
        with NovelFixture() as fx:
            fx.add_chapter(1, MULTI_PARAGRAPH_SPEECH,
                           event=" ".join("word%d" % i for i in range(rules.EVENT_MAX_WORDS + 6)))
            self.assertIn("warn", levels(lint_one(fx), "event"))

    def test_a_missing_event_is_a_frontmatter_defect(self):
        with NovelFixture() as fx:
            fx.add_chapter(1, MULTI_PARAGRAPH_SPEECH, event="")
            self.assertTrue(any("`event:` missing" in m for m in messages(lint_one(fx))))


class TestCampaignClause(unittest.TestCase):
    """CLAUDE.md section 5 bans this and names the example. `sw lint` counted it and printed the
    count inside a statistics line, where nothing had to answer for it — so it shipped."""

    def test_the_exact_sentence_claude_md_bans_is_surfaced_as_a_finding(self):
        body = ('"You are late," he said.\n\n'
                "Suzune had spent three weeks making it true, and nobody had noticed.\n\n"
                '"I know," she said.\n')
        with NovelFixture() as fx:
            fx.add_chapter(1, body)
            rep = lint_one(fx)
            self.assertIn("warn", levels(rep, "campaign-clause"))
            self.assertTrue(any("spent three weeks making it true" in (f.detail or "")
                                for f in rep.findings))

    def test_ordinary_prose_does_not_trip_it(self):
        with NovelFixture() as fx:
            fx.add_chapter(1, MULTI_PARAGRAPH_SPEECH)
            self.assertEqual(levels(lint_one(fx), "campaign-clause"), [])


class TestHouseStyle(unittest.TestCase):
    """The tells this model produces once the MTL cut-list is already clean. Individually fine,
    which is why each is a note and only the density warns."""

    def test_the_density_warns_but_one_instance_does_not(self):
        once = '"Go," she said.\n\nIt was weather, not prophecy, and she went.\n'
        with NovelFixture() as fx:
            fx.add_chapter(1, once)
            self.assertEqual(levels(lint_one(fx), "house-style"), ["note"])

    def test_run_2s_constructions_are_all_recognised(self):
        body = ("It was weather, not prophecy. Not relief. A beat.\n\n"
                "She held it for exactly as long as an innocent person would, "
                "in the same flat register she used for everything.\n")
        with NovelFixture() as fx:
            fx.add_chapter(1, body)
            labels = {f.message for f in lint_one(fx).findings if f.check == "house-style"}
            for want in ("X, not Y antithesis", "`Not X.` fragment negation",
                         "`A beat.` - a stage direction, not prose"):
                self.assertIn(want, labels)

    def test_dialogue_is_exempt(self):
        """A character may talk in antitheses as a fingerprint. The narrator may not."""
        spoken = '"It was weather, not prophecy, and not a warning either," she said.\n'
        with NovelFixture() as fx:
            fx.add_chapter(1, spoken)
            self.assertEqual(levels(lint_one(fx), "house-style"), [])

    def test_em_dash_density_warns(self):
        """Run #2 chapter 1 ran 9.5 dashes per 1000 words of narration. The cap is 6."""
        filler = " ".join(["she waited by the window and counted"] * 8)
        para = "She went to the door — the one thing she had left — and %s.\n\n" % filler
        with NovelFixture() as fx:
            fx.add_chapter(1, para * 8)          # ~500 words, 16 dashes
            self.assertIn("warn", levels(lint_one(fx), "em-dash"))

    def test_a_short_chapter_is_not_judged_on_a_rate(self):
        """A per-1000-word rate needs a denominator worth dividing by."""
        with NovelFixture() as fx:
            fx.add_chapter(1, "She went to the door — the one thing left — and waited.\n")
            self.assertEqual(levels(lint_one(fx), "em-dash"), [])


class TestCloserSameness(unittest.TestCase):
    """Run #2 ended four of five chapters on a short withheld beat. Each is a good last line;
    four in a row is a tic, and it is only visible across chapters."""

    CLOSERS = ["The gate hung open.",
               "The small hand found hers.",
               "Neither did Enko.",
               "The door stayed shut.",
               "Nobody was watching it."]

    def _novel(self, fx, closers):
        for i, tail in enumerate(closers, start=1):
            fx.add_chapter(i, '"Go," she said.\n\nHe went out into the road.\n\n%s\n' % tail)
        fx.add_ledger(list(range(1, len(closers) + 1)))

    def test_four_short_withheld_closes_in_five_chapters_warns(self):
        with NovelFixture() as fx:
            self._novel(fx, self.CLOSERS)
            rep = cmd_lint.run(fx.novel())
            self.assertIn("warn", levels(rep, "closer-sameness"))

    def test_varied_closes_do_not_warn(self):
        varied = ['"Then we go tonight," she said, and picked up the lamp.',
                  "The gate hung open.",
                  'He laughed at her, which was the first mistake he made that evening, and she '
                  'let him keep laughing until he understood what she had actually said to him.',
                  '"Run," Maro told her, and she ran.',
                  "Neither did Enko."]
        with NovelFixture() as fx:
            self._novel(fx, varied)
            self.assertEqual(levels(cmd_lint.run(fx.novel()), "closer-sameness"), [])


class TestRegisterLedger(unittest.TestCase):
    """temp and hooktype, declared at plan time and checked as a distribution."""

    HEAD = ("# Chapter construction list\n\n"
            "| # | title | pov | arc | temp | hooktype | goal | obstacle | turn | event | "
            "delivers | cost | threads | hook | status |\n"
            "|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|\n")

    def _plan(self, fx, pairs):
        rows = ["| %d | T%d | Rin | 1 | %s | %s | g | o | t | Rin takes the ledger | d | c | "
                "~T01 | h | drafted |" % (i, i, t, h) for i, (t, h) in enumerate(pairs, start=1)]
        fx.write("plan/chapters.md", self.HEAD + "\n".join(rows) + "\n")
        for i in range(1, len(pairs) + 1):
            fx.add_chapter(i, MULTI_PARAGRAPH_SPEECH)
        fx.add_ledger(list(range(1, len(pairs) + 1)))

    def test_run_2s_flat_arc_is_caught(self):
        """Five chapters, one temperature, one hook shape."""
        with NovelFixture() as fx:
            self._plan(fx, [("quiet", "reveal")] * 5)
            msgs = messages(cmd_arc.run(fx.novel(), 1))
            self.assertTrue(any("runs 3 chapters straight" in m for m in msgs))
            self.assertTrue(any("only 1 distinct temperature" in m for m in msgs))
            self.assertTrue(any("only 1 distinct hook shape" in m for m in msgs))

    def test_a_varied_arc_raises_nothing(self):
        with NovelFixture() as fx:
            self._plan(fx, [("tense", "reveal"), ("procedural", "decision"), ("warm", "quiet"),
                            ("tense", "reversal"), ("bleak", "arrival"), ("loud", "threat")])
            self.assertEqual(levels(cmd_arc.run(fx.novel(), 1), "arc-register"), [])

    def test_a_hook_shape_three_times_in_five_warns(self):
        with NovelFixture() as fx:
            self._plan(fx, [("tense", "reveal"), ("warm", "reveal"), ("loud", "decision"),
                            ("bleak", "reveal"), ("fast", "arrival")])
            msgs = messages(cmd_arc.run(fx.novel(), 1))
            self.assertTrue(any("hook shape `reveal` used 3 times" in m for m in msgs))

    def test_an_unknown_temp_is_rejected(self):
        with NovelFixture() as fx:
            self._plan(fx, [("sombre", "reveal")])
            self.assertTrue(any("is not one of" in m for m in messages(lint_one(fx))))

    def test_an_unset_temp_warns_at_lint(self):
        with NovelFixture() as fx:
            self._plan(fx, [("", "")])
            msgs = messages(lint_one(fx))
            self.assertTrue(any("has no `temp`" in m for m in msgs))
            self.assertTrue(any("has no `hooktype`" in m for m in msgs))


class TestShrinkage(unittest.TestCase):
    """1938 -> 1457 -> 1323 -> 1213 -> 1151. Reported as a signal about event density, never
    as a length gate: `docs/design-notes.md` is right that a shipping number gets optimised."""

    def test_a_monotonic_slide_is_reported(self):
        with NovelFixture() as fx:
            for i, n in enumerate([400, 300, 240, 200, 170], start=1):
                fx.add_chapter(i, " ".join(["word"] * n) + ".\n")
            fx.add_ledger(list(range(1, 6)))
            msgs = messages(cmd_arc.run(fx.novel(), 1))
            self.assertTrue(any("get shorter every chapter" in m for m in msgs))

    def test_it_is_never_a_defect(self):
        with NovelFixture() as fx:
            for i, n in enumerate([400, 300, 240, 200, 170], start=1):
                fx.add_chapter(i, " ".join(["word"] * n) + ".\n")
            fx.add_ledger(list(range(1, 6)))
            self.assertNotIn("defect", levels(cmd_arc.run(fx.novel(), 1), "arc-shrinkage"))

    def test_a_steady_run_is_silent(self):
        with NovelFixture() as fx:
            for i, n in enumerate([300, 280, 310, 290, 305], start=1):
                fx.add_chapter(i, " ".join(["word"] * n) + ".\n")
            fx.add_ledger(list(range(1, 6)))
            self.assertEqual(levels(cmd_arc.run(fx.novel(), 1), "arc-shrinkage"), [])


if __name__ == "__main__":
    unittest.main()
