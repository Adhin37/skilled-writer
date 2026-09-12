"""The command line itself: exit codes, and the two commands that can touch the filesystem.

Exit codes are the contract skills rely on — 0 clean, 1 findings that need a decision, 2 bad
usage or missing files.
"""

import os
import re
import subprocess
import sys
import unittest

from fixtures import NOVEL_MD, REPO, NovelFixture

SW = os.path.join(REPO, "scripts", "sw.py")
BODY = "The room was cold.\n\n\"Shut it,\" she said.\n\nHe shut it.\n"


def run(*args):
    proc = subprocess.run([sys.executable, SW] + list(args),
                          stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return proc.returncode, proc.stdout.decode("utf-8"), proc.stderr.decode("utf-8")


class TestUsage(unittest.TestCase):

    def test_lint_on_a_novel_with_no_chapters_is_a_usage_error(self):
        """Was: exit 0. An empty novel passed the linter."""
        with NovelFixture() as fx:
            code, _out, err = run("lint", fx.root)
            self.assertEqual(code, 2)
            self.assertIn("no chapters", err)

    def test_missing_novel_is_a_usage_error(self):
        code, _out, _err = run("lint", os.path.join(REPO, "does", "not", "exist"))
        self.assertEqual(code, 2)

    def test_doctor_runs_clean(self):
        code, out, _err = run("doctor")
        self.assertEqual(code, 0)
        self.assertIn("environment", out)

    def test_audit_has_no_dead_all_flag(self):
        code, _out, err = run("audit", "--all")
        self.assertEqual(code, 2)
        self.assertIn("unrecognized arguments", err)


class TestReadsetOut(unittest.TestCase):

    def test_out_refuses_a_path_outside_the_repo_and_temp(self):
        with NovelFixture() as fx:
            fx.add_chapter(1, BODY)
            target = os.path.join(os.path.expanduser("~"), "sw-should-not-exist.md")
            code, _out, err = run("readset", fx.root, "-c", "1", "--out", target)
            self.assertEqual(code, 2)
            self.assertIn("--out must be inside", err)
            self.assertFalse(os.path.exists(target))

    def test_out_refuses_to_overwrite(self):
        with NovelFixture() as fx:
            fx.add_chapter(1, BODY)
            existing = fx.path("chapters", "0001-chapter.md")
            code, _out, err = run("readset", fx.root, "-c", "1", "--out", existing)
            self.assertEqual(code, 2)
            self.assertIn("refuses to overwrite", err)
            with open(existing, encoding="utf-8") as fh:
                self.assertIn("number: 1", fh.read())

    def test_out_writes_when_the_path_is_allowed(self):
        with NovelFixture() as fx:
            fx.add_chapter(1, BODY)
            target = fx.path("readset.md")
            code, out, _err = run("readset", fx.root, "-c", "1", "--out", target)
            self.assertEqual(code, 0)
            self.assertTrue(os.path.isfile(target))
            self.assertIn("written to", out)


class TestReadsetModules(unittest.TestCase):
    """write-chapter step 0.2 opens the listed modules and no others, so the list must be exact.

    Every assertion is scoped to the block: skill names also occur in the lexicon and in the
    prose of other sections, and a whole-output search reports those as active modules.
    """

    @staticmethod
    def modules_block(out):
        return out.split("### active modules", 1)[1].split("\n##", 1)[0]

    @staticmethod
    def cards_block(out):
        tail = out.split("### CARDS -", 1)[1].split("\n##", 1)[0]
        return tail.split("\n", 1)[1]

    def test_the_card_set_is_resolved_into_the_read_set(self):
        """The block that replaces write-chapter's hand-typed table."""
        with NovelFixture() as fx:
            fx.add_chapter(1, BODY)
            code, out, _err = run("readset", fx.root, "-c", "1")
            self.assertEqual(code, 0)
            self.assertIn("### CARDS -", out)
            block = self.cards_block(out)
            # story-craft is the card the contract calls "first, always", so it leads.
            self.assertTrue(block.strip().startswith("story-craft"), block[:120])
            self.assertIn("draft-card.md", block)

    def test_a_card_that_does_not_apply_is_named_with_its_reason(self):
        """A condition that is quietly wrong must not look like a card that never applied."""
        with NovelFixture() as fx:
            fx.add_chapter(9, BODY)
            code, out, _err = run("readset", fx.root, "-c", "9")
            self.assertEqual(code, 0)
            self.assertIn("### CARDS NOT OPENED", out)
            skipped = out.split("### CARDS NOT OPENED", 1)[1].split("\n##", 1)[0]
            # chapter 9 is past the opening window, and the row has to say so rather than
            # leaving the card silently absent.
            self.assertIn("story-opening", skipped)
            self.assertIn("false", skipped)

    def test_a_config_gated_skill_is_listed_when_its_gate_is_open(self):
        """`lead-interest` and `pov-switch` are switched on by config, not by an `optional:` key.

        They were absent from this block for the life of the repo, so a novel with a romance was
        never told that `lead-interest` applied to it - the drafter had to carry the condition
        from CLAUDE.md section 3 by memory, which is the hand-maintained retrieval the knowledge
        base exists to remove. The condition prints beside the row, because a gated skill turning
        up is the surprising case.
        """
        from fixtures import NOVEL_MD
        md = NOVEL_MD.replace("  mode: single", "  mode: dual")
        if "romance:" in md:
            md = re.sub(r"(?m)^(\s*)romance:.*$", r"\1romance: central", md)
        else:
            md = md.replace("\ngenre: fantasy", "\ngenre: fantasy\ncontent:\n  romance: central")
        with NovelFixture(novel_md=md) as fx:
            fx.add_chapter(1, BODY)
            code, out, _err = run("readset", fx.root, "-c", "1")
            self.assertEqual(code, 0)
            block = self.modules_block(out)
            self.assertIn("lead-interest", block)
            self.assertIn("content.romance != none", block)
            self.assertIn("pov-switch", block)
            self.assertIn("pov.mode != single", block)

    def test_a_config_gated_skill_is_absent_when_its_gate_is_shut(self):
        """The converse, and the reason the default has to come from `novelio`'s own defaults.

        A novel that never mentions `pov.mode` must not have `pov-switch` switched on by the
        absence reading as "not single".
        """
        with NovelFixture() as fx:                     # pov.mode: single, no content.romance
            fx.add_chapter(1, BODY)
            code, out, _err = run("readset", fx.root, "-c", "1")
            self.assertEqual(code, 0)
            block = self.modules_block(out)
            self.assertNotIn("pov-switch", block)
            self.assertNotIn("lead-interest", block)

    def test_genre_switches_a_module_on_and_off_modules_are_absent(self):
        with NovelFixture() as fx:          # genre: fantasy, no `optional:` block
            fx.add_chapter(1, BODY)
            code, out, _err = run("readset", fx.root, "-c", "1")
            self.assertEqual(code, 0)
            block = self.modules_block(out)
            self.assertIn("power-system", block)          # fantasy switches it on
            self.assertNotIn("tech-plausibility", block)  # scifi only
            self.assertNotIn("litrpg-system", block)      # optional, and off

    def test_an_optional_toggle_puts_its_module_in_the_list(self):
        novel_md = NOVEL_MD.replace("status: drafting",
                                    "status: drafting\n\noptional:\n  litrpg-system: on")
        with NovelFixture(novel_md=novel_md) as fx:
            fx.add_chapter(1, BODY)
            code, out, _err = run("readset", fx.root, "-c", "1")
            self.assertEqual(code, 0)
            block = self.modules_block(out)
            self.assertIn("litrpg-system", block)
            self.assertNotIn("mystery-clues", block)

    def test_every_listed_entry_point_exists_on_disk(self):
        with NovelFixture() as fx:
            fx.add_chapter(1, BODY)
            _code, out, _err = run("readset", fx.root, "-c", "1")
            paths = [ln.split("->", 1)[1].strip()
                     for ln in self.modules_block(out).splitlines() if "->" in ln]
            self.assertTrue(paths, "fantasy should switch at least one module on")
            for rel in paths:
                self.assertTrue(os.path.isfile(os.path.join(REPO, rel)),
                                "readset named a module entry point that does not exist: %s" % rel)



class TestReadsetCharacterMatching(unittest.TestCase):
    """Short names in the ledger must still find full names in the tables.

    Benchmark run #4, T7. `_match` compared whole cells for equality, so a `chg>` line naming
    `Yakumo` never matched the matrix row `Yakumo Kurama`, and the read-set printed "(no matrix
    rows for these characters)" for the voice matrix, the growth ladder and the competence grid
    at once — while its own header tells the drafter not to open the source files for anything it
    lists. The three sections a drafter can least afford to lose, dropped in silence.
    """

    class Row(object):
        def __init__(self, name):
            self.name = name

        def first(self):
            return self.name

    def match(self, names):
        from swlib import cmd_readset

        rows = [self.Row(n) for n in ("Yakumo Kurama", "Souta Kurama", "Enji Kurama",
                                      "Sachi Kurama", "Hiruzen Sarutobi")]
        return [r.first() for r in cmd_readset._match(rows, names)]

    def test_a_given_name_finds_the_full_row(self):
        self.assertEqual(["Yakumo Kurama"], self.match(["Yakumo"]))

    def test_a_distinctive_surname_finds_the_full_row(self):
        self.assertEqual(["Hiruzen Sarutobi"], self.match(["Sarutobi"]))

    def test_a_shared_clan_name_matches_nobody(self):
        """Otherwise every Kurama is in every scene, which is no slice at all."""
        self.assertEqual([], self.match(["Kurama"]))

    def test_a_full_name_still_matches_exactly_one(self):
        self.assertEqual(["Sachi Kurama"], self.match(["Sachi Kurama"]))

    def test_several_names_return_several_rows(self):
        self.assertEqual(["Yakumo Kurama", "Sachi Kurama"], self.match(["Yakumo", "Sachi"]))

    def test_an_unknown_name_returns_nothing(self):
        self.assertEqual([], self.match(["Kakashi"]))


class TestReadsetGateSection(unittest.TestCase):
    """The read-set names what the phase C gate left behind, before the chapter is drafted."""

    @staticmethod
    def gate_block(out):
        return out.split("## GATE", 1)[1].split("\n## 0.", 1)[0] if "## GATE" in out else ""

    def test_a_predecessor_left_at_drafted_is_a_defect(self):
        with NovelFixture() as fx:
            fx.add_chapter(1, BODY)                        # the fixture ships `status: drafted`
            _code, out, _err = run("readset", fx.root, "-c", "2")
            block = self.gate_block(out)
            self.assertIn("DEFECT", block)
            self.assertIn("ch 1", block)

    def test_a_gated_predecessor_says_nothing(self):
        with NovelFixture() as fx:
            fx.add_chapter(1, BODY)
            path = fx.path("chapters", "0001-chapter.md")
            with open(path, encoding="utf-8") as fh:
                text = fh.read()
            with open(path, "w", encoding="utf-8", newline="\n") as fh:
                fh.write(text.replace("status: drafted", "status: revised"))
            _code, out, _err = run("readset", fx.root, "-c", "2")
            self.assertNotIn("DEFECT", self.gate_block(out))

    def test_the_count_is_one_line_however_many_are_ungated(self):
        with NovelFixture() as fx:
            for n in range(1, 5):
                fx.add_chapter(n, BODY)
            _code, out, _err = run("readset", fx.root, "-c", "5")
            block = self.gate_block(out)
            self.assertEqual(block.count("DEFECT"), 1, "one line, not one per chapter")
            self.assertIn("4 ungated below 5", block)

    def test_a_broken_run_is_not_offered_as_a_range(self):
        """`/novel-write 1-4` would re-gate chapters 2 and 3, which already passed."""
        with NovelFixture() as fx:
            for n in range(1, 5):
                fx.add_chapter(n, BODY)
            for n in (2, 3):
                path = fx.path("chapters", "%04d-chapter.md" % n)
                with open(path, encoding="utf-8") as fh:
                    text = fh.read()
                with open(path, "w", encoding="utf-8", newline="\n") as fh:
                    fh.write(text.replace("status: drafted", "status: revised"))
            _code, out, _err = run("readset", fx.root, "-c", "5")
            block = self.gate_block(out)
            self.assertNotIn("1-4", block)
            self.assertIn("ch 1, 4", block)

    def test_gate_lines_from_recent_blocks_are_echoed(self):
        with NovelFixture() as fx:
            fx.add_chapter(1, BODY)
            fx.add_ledger([1])
            path = fx.path("state", "continuity.md")
            with open(path, encoding="utf-8") as fh:
                text = fh.read()
            with open(path, "w", encoding="utf-8", newline="\n") as fh:
                fh.write(text.rstrip() + "\ngate> campaign-clause x2\n")
            _code, out, _err = run("readset", fx.root, "-c", "2")
            self.assertIn("campaign-clause x2", self.gate_block(out))

    def test_a_first_chapter_has_no_gate_section(self):
        with NovelFixture() as fx:
            _code, out, _err = run("readset", fx.root, "-c", "1")
            self.assertNotIn("## GATE", out)


class TestLintAndAudit(unittest.TestCase):

    def test_lint_reports_findings_with_exit_1(self):
        with NovelFixture() as fx:
            # a narration exclamation mark and an AI-default phrase are both defects
            fx.add_chapter(1, "The room was cold!\n\nHe shut it.\n")
            code, out, _err = run("lint", fx.root, "--show", "note")
            self.assertEqual(code, 1)
            self.assertIn("0001-chapter.md", out)
            self.assertIn("narration-bang", out)

    def test_audit_runs_over_every_chapter(self):
        with NovelFixture() as fx:
            fx.add_chapter(1, BODY)
            fx.add_chapter(2, BODY)
            _code, out, _err = run("audit", fx.root)
            self.assertIn("0001-chapter.md", out)
            self.assertIn("0002-chapter.md", out)

    def test_audit_sees_a_habit_no_single_chapter_shows(self):
        """Run #3. The writing agent offered "`sw audit` returns 0 defects" as proof the novel was
        clean while a drafting habit ran through 4 of its 5 chapters, because every check `audit`
        composed was per-chapter. A habit is not visible in one chapter by definition."""
        quiet = ("She counted the sacks again and wrote the number down in the second column "
                 "where nobody would look for it until the quarter closed.\n")
        with NovelFixture() as fx:
            for n in range(1, 6):
                fx.add_chapter(n, quiet)
            _code, out, _err = run("audit", fx.root)
            self.assertIn("history-dialogue", out,
                          "audit lost the cross-chapter view it was given in run #3")


if __name__ == "__main__":
    unittest.main()


class TestDialogueStarvation(unittest.TestCase):
    """Benchmark run #2, F1. A per-chapter floor raised as a defect is a number that decides
    whether a chapter ships, and it was optimised within five chapters: ch2 landed at 10.2%
    against a 10.0% gate, and the writing agent volunteered that it had retrofitted a muttering
    habit onto the MC to clear it. That is finding 6's signature on a new metric. The defect is
    now measured over a five-chapter mean, so there is no single-chapter number to write toward.
    """

    QUIET = ("She counted the sacks again and wrote the number down in the second column "
             "where nobody would look for it until the quarter closed.\n")
    LOUD = ('"Shut the door," she said. "And then tell me what you actually saw, all of it, '
            'in the order it happened, and do not tidy it up for me on the way."\n')

    def _findings(self, shares):
        """`shares` is one 'quiet'/'loud' word per chapter."""
        from swlib import cmd_lint
        with NovelFixture() as fx:
            for n, kind in enumerate(shares, start=1):
                fx.add_chapter(n, self.QUIET if kind == "quiet" else self.LOUD)
            novel = fx.novel()
            rep = cmd_lint.run(novel, None)
            return {(f.check, f.level) for f in rep.findings}

    def _history_findings(self, shares):
        """The same fixture, put through `history` instead of `lint`.

        Benchmark run #3, T1: the guard below was scoped to one command, so the per-chapter gate
        simply came back in another one - `cmd_history` raised a book-level DEFECT the moment any
        single chapter fell under the floor, and a novel with one deliberately quiet chapter
        failed. A rule this repo has now re-learned three times is worth testing at every command
        that can express it, not at the one where it was last fixed.
        """
        from swlib import cmd_history
        with NovelFixture() as fx:
            for n, kind in enumerate(shares, start=1):
                fx.add_chapter(n, self.QUIET if kind == "quiet" else self.LOUD)
            rep, _data = cmd_history.run(fx.novel())
            return {(f.check, f.level) for f in rep.findings}

    def test_one_quiet_chapter_is_a_warn_not_a_defect(self):
        """Was: a defect on any single chapter under 10%, so the number got written toward."""
        found = self._findings(["quiet"])
        self.assertIn(("speech-share", "warn"), found)
        self.assertNotIn(("speech-share", "defect"), found)

    def test_no_command_makes_one_quiet_chapter_a_defect(self):
        """Run #3, T1. One quiet chapter among talking ones is a choice, and no command may
        raise it to a defect - `speech-starvation` over a window is the only gate on this
        metric."""
        for cmd, found in (("lint", self._findings(["loud", "loud", "quiet", "loud", "loud"])),
                           ("history",
                            self._history_findings(["loud", "loud", "quiet", "loud", "loud"]))):
            defects = {check for check, level in found if level == "defect"}
            self.assertNotIn("history-dialogue", defects,
                             "%s raised a defect for a single quiet chapter" % cmd)
            self.assertNotIn("speech-share", defects,
                             "%s raised a defect for a single quiet chapter" % cmd)

    def test_five_quiet_chapters_are_a_defect(self):
        """Run #1's real shares were 2, 3, 4, 4, 5% and every chapter passed the gate."""
        self.assertIn(("speech-starvation", "defect"), self._findings(["quiet"] * 5))

    def test_a_talking_cast_never_trips_it(self):
        self.assertNotIn(("speech-starvation", "defect"), self._findings(["loud"] * 5))

    def test_it_waits_for_a_full_window(self):
        """Four quiet chapters is not yet evidence; the check must not fire early."""
        self.assertNotIn(("speech-starvation", "defect"), self._findings(["quiet"] * 4))

    def test_it_fires_once_per_command_not_once_per_chapter(self):
        """`cmd_history` lints every chapter to build its trend table. A novel-level verdict
        evaluated inside `lint_chapter` would be counted once per chapter and then reported as a
        habit firing on the whole book - one finding wearing N hats."""
        from swlib import cmd_lint
        with NovelFixture() as fx:
            for n in range(1, 9):
                fx.add_chapter(n, self.QUIET)
            novel = fx.novel()
            rep = cmd_lint.run(novel, None)
            starve = [f for f in rep.findings if f.check == "speech-starvation"]
            self.assertEqual(len(starve), 1, "the window verdict was counted per chapter")

    def test_lint_chapter_stays_strictly_per_chapter(self):
        """The contract `cmd_history` depends on: no novel-level verdict in here."""
        from swlib import cmd_lint
        with NovelFixture() as fx:
            for n in range(1, 9):
                fx.add_chapter(n, self.QUIET)
            novel = fx.novel()
            for ch in novel.chapters():
                rep = cmd_lint.lint_chapter(novel, ch)
                self.assertEqual(
                    [f.check for f in rep.findings if f.check == "speech-starvation"], [],
                    "lint_chapter emitted a novel-level finding")

    def test_history_does_not_report_the_window_as_a_per_chapter_habit(self):
        from swlib import cmd_history
        with NovelFixture() as fx:
            for n in range(1, 9):
                fx.add_chapter(n, self.QUIET)
            rep = cmd_history.run(fx.novel())[0]
            body = " ".join(l for _h, lines in rep.sections for l in lines)
            self.assertNotIn("speech-starvation", body)


class TestHabitNotes(unittest.TestCase):
    """The note tier reaches the two cross-chapter detectors, and never reaches a chapter.

    Note-level checks are the habit checks - a thing that is fine once and a fingerprint at
    density. Both mechanisms that look across chapters (`readset`'s WATCH row, `history`'s
    habit table) read `cmd_lint.check_counts`, which counted only defects and warns, so every
    habit was invisible to the only two things able to see one. Benchmark run #4 shipped five
    of six chapters with `house-style` firing and told the drafter nothing.
    """

    # Narration, because `house_style_hits` exempts dialogue on purpose: the defect is the
    # *narrator* having one register. Each line carries one `X, not Y` antithesis.
    HABIT_BODY = (
        "The room was cold, not empty.\n\n"
        "She counted the coins, not the notes.\n\n"
        "\"Shut it,\" she said.\n\nHe shut it.\n"
    )

    def _populate(self, fx, chapters=5):
        for n in range(1, chapters + 1):
            fx.add_chapter(n, self.HABIT_BODY)
        return fx

    def test_a_habit_note_reaches_the_watch_row(self):
        """Was: house-style fired on five of five chapters and the row never named it."""
        from swlib import cmd_readset
        with NovelFixture() as fx:
            self._populate(fx)
            row, _gate = cmd_readset.watch_row(fx.novel(), 6)
            self.assertTrue(any("house-style" in item for item in row),
                            "a habit note that recurred is missing from WATCH: %r" % row)

    def test_a_habit_note_reaches_the_history_table(self):
        with NovelFixture() as fx:
            self._populate(fx)
            code, out, _err = run("history", fx.root)
            self.assertIn("house-style", out)
            self.assertIn("note", out)
            self.assertNotEqual(code, 2)

    def test_a_situation_note_never_reaches_the_watch_row(self):
        """`group-scene` reports what a chapter contains, and says "Read it and discount it".

        A book with group scenes in every chapter has group scenes. That is not a habit, and
        the WATCH row is what the gate keeps having to fix.
        """
        from swlib import cmd_lint, cmd_readset, rules
        self.assertIn("group-scene", rules.SITUATION_NOTE_CHECKS)
        self.assertNotIn("group-scene", rules.HABIT_NOTE_CHECKS)
        with NovelFixture() as fx:
            self._populate(fx)
            novel = fx.novel()
            for ch in novel.chapters():
                self.assertNotIn("group-scene", cmd_lint.check_counts(novel, ch)["notes"])
            row, _gate = cmd_readset.watch_row(novel, 6)
            self.assertFalse(any("group-scene" in item for item in row), row)

    def test_a_note_is_never_counted_as_a_defect_or_a_warn(self):
        """The standing rule: nothing here may become a number that decides shipping.

        Word count and then dialogue share were both built as ship gates and both were
        optimised rather than satisfied (docs/benchmark.md). A note promoted to a warn is the
        same mistake with a different name, so the count is asserted rather than trusted.
        """
        from swlib import cmd_lint
        from swlib.report import Report
        with NovelFixture() as fx:
            self._populate(fx)
            novel = fx.novel()
            for ch in novel.chapters():
                counts = cmd_lint.check_counts(novel, ch)
                self.assertIn("house-style", counts["notes"])

                # The bucket is decided by the finding's LEVEL, never by its check name. Two
                # checks deliberately fire at more than one level - `house-style` notes each
                # construction and warns on the aggregate rate, `thought-budget` notes the
                # floor and raises a defect on the ceiling - so a name-based rule would be
                # both wrong and quietly restrictive.
                sub = Report()
                cmd_lint.lint_chapter(novel, ch, sub)
                scored = set(f.check for f in sub.findings
                             if f.level in ("defect", "warn"))
                self.assertEqual(set(counts["checks"]), scored)
                for f in sub.findings:
                    if f.level == "note" and f.check not in scored:
                        self.assertNotIn(f.check, counts["checks"],
                                         "note-level %r leaked into the scoring tier"
                                         % f.check)

    def test_warns_outrank_notes_in_the_watch_row(self):
        """Notes fire far more often, so a frequency-first sort evicted every warn.

        WATCH_CAP is small by design. Ranking on frequency alone traded one blind spot for
        another: the row that named recurring warns stopped naming them.
        """
        from swlib import cmd_readset
        body = self.HABIT_BODY + "\n" + "\n\n".join(
            ["It was late." for _ in range(2)]) + "\n"
        with NovelFixture() as fx:
            for n in range(1, 6):
                fx.add_chapter(n, body)
            novel = fx.novel()
            hits = {}
            for ch in novel.chapters():
                from swlib import cmd_lint
                counts = cmd_lint.check_counts(novel, ch)
                for c in counts["checks"]:
                    hits.setdefault(c, ["warn", 0])[1] += 1
                for c in counts["notes"]:
                    hits.setdefault(c, ["note", 0])[1] += 1
            recurring_warns = [c for c, (lvl, n) in hits.items()
                               if lvl == "warn" and n >= cmd_readset.WATCH_MIN]
            if not recurring_warns:
                self.skipTest("fixture produced no recurring warn to rank")
            row, _gate = cmd_readset.watch_row(novel, 6)
            for check in recurring_warns:
                self.assertTrue(any(check in item for item in row),
                                "recurring warn %r evicted from WATCH by notes: %r"
                                % (check, row))


class TestNoteTierRegistry(unittest.TestCase):
    """Every note-level check is classified, so a new one cannot be silently forgotten.

    The habit set is an allowlist: a new note check is a situation note until somebody decides
    otherwise. What this forbids is a note check in *neither* set, which would read as a
    deliberate classification and is actually an omission.
    """

    def test_every_note_check_is_classified(self):
        from swlib import rules
        with open(os.path.join(REPO, "scripts", "swlib", "cmd_lint.py"),
                  encoding="utf-8") as fh:
            source = fh.read()
        names = set(re.findall(r'rep\.note\("([a-z0-9-]+)"', source))
        self.assertTrue(names, "no note-level checks found - did the call shape change?")
        known = rules.HABIT_NOTE_CHECKS | rules.SITUATION_NOTE_CHECKS
        self.assertEqual(sorted(names - known), [],
                         "unclassified note check(s): add to HABIT_NOTE_CHECKS or "
                         "SITUATION_NOTE_CHECKS in rules.py")

    def test_the_two_sets_do_not_overlap(self):
        from swlib import rules
        self.assertEqual(rules.HABIT_NOTE_CHECKS & rules.SITUATION_NOTE_CHECKS, frozenset())


class TestWideningArtifacts(unittest.TestCase):
    """`cand>` and `z4>` - the two steps that used to leave no trace anywhere.

    The three-candidate step happens inside the Phase A brief, which is written into the
    conversation and discarded, and Pass Z4's answer went nowhere at all. Benchmark run #4 ran
    five chapters through both and could not tell whether either had fired - which
    docs/benchmark.md calls a worse state than untested. These two optional CCS lines are the
    artifact, and this asserts they survive the round trip and get counted.
    """

    EXTRA = ("cand> 2:she pays the clerk 3:she waits for the shift change -> took 3, "
             "paying makes her a customer\nz4> %s\n")

    def _novel(self, fx, answers):
        for n in range(1, len(answers) + 1):
            fx.add_chapter(n, BODY)
        fx.add_ledger(list(range(1, len(answers) + 1)))
        with open(fx.path("state", "continuity.md"), encoding="utf-8") as fh:
            text = fh.read()
        # Splice the two lines in above each block's `hook>`, which every block carries.
        out, i = [], 0
        for line in text.splitlines(True):
            if line.startswith("hook>"):
                out.append(self.EXTRA % answers[i])
                i += 1
            out.append(line)
        fx.write("state/continuity.md", "".join(out))
        return fx.novel()

    def test_the_lines_parse_and_reach_the_read_set(self):
        from swlib import cmd_readset
        with NovelFixture() as fx:
            novel = self._novel(fx, ["the clerk is the one who is frightened"] * 3)
            rows, nones = cmd_readset.z4_row(novel, 4)
            self.assertEqual(len(rows), 3)
            self.assertEqual(nones, 0)
            self.assertIn("frightened", rows[0])

    def test_none_is_counted_rather_than_ignored(self):
        """`none` is a legitimate answer, and counting it is the entire point of the line."""
        from swlib import cmd_readset
        with NovelFixture() as fx:
            novel = self._novel(fx, ["none", "none", "the clerk is frightened"])
            _rows, nones = cmd_readset.z4_row(novel, 4)
            self.assertEqual(nones, 2)

    def test_history_reports_the_widening_section(self):
        with NovelFixture() as fx:
            self._novel(fx, ["none"] * 3)
            code, out, _err = run("history", fx.root)
            self.assertIn("widening", out)
            self.assertIn("candidates recorded", out)
            self.assertNotEqual(code, 2)

    def test_a_block_carrying_both_lines_is_within_the_cap(self):
        """Every block of the heaviest live novel already sat at the old cap of 15."""
        from swlib import rules
        with NovelFixture() as fx:
            novel = self._novel(fx, ["none"] * 2)
            for b in novel.blocks():
                if b.number is not None:
                    self.assertLessEqual(b.line_count, rules.CCS_MAX_LINES)

    def test_both_lines_stay_optional(self):
        """A ledger written before these existed must not become defective."""
        with NovelFixture() as fx:
            for n in (1, 2):
                fx.add_chapter(n, BODY)
            fx.add_ledger([1, 2])
            code, out, _err = run("state", fx.root)
            self.assertNotIn("cand", out)
            self.assertNotIn("`z4>`", out)
            self.assertNotEqual(code, 2)
