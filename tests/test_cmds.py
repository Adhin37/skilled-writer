"""The command line itself: exit codes, and the two commands that can touch the filesystem.

Exit codes are the contract skills rely on — 0 clean, 1 findings that need a decision, 2 bad
usage or missing files.
"""

import os
import subprocess
import sys
import unittest

from fixtures import REPO, NovelFixture

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
