"""The command line itself: exit codes, and the two commands that can touch the filesystem.

Exit codes are the contract skills rely on — 0 clean, 1 findings that need a decision, 2 bad
usage or missing files.
"""

import os
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

    def test_one_quiet_chapter_is_a_warn_not_a_defect(self):
        """Was: a defect on any single chapter under 10%, so the number got written toward."""
        found = self._findings(["quiet"])
        self.assertIn(("speech-share", "warn"), found)
        self.assertNotIn(("speech-share", "defect"), found)

    def test_five_quiet_chapters_are_a_defect(self):
        """Run #1's real shares were 2, 3, 4, 4, 5% and every chapter passed the gate."""
        self.assertIn(("speech-starvation", "defect"), self._findings(["quiet"] * 5))

    def test_a_talking_cast_never_trips_it(self):
        self.assertNotIn(("speech-starvation", "defect"), self._findings(["loud"] * 5))

    def test_it_waits_for_a_full_window(self):
        """Four quiet chapters is not yet evidence; the check must not fire early."""
        self.assertNotIn(("speech-starvation", "defect"), self._findings(["quiet"] * 4))
