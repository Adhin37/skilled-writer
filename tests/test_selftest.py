"""The dry run of novel-init, and the sample novel it is built on.

The sample is the only novel this repo ships, and every claim `sw selftest` makes rests on it
being genuinely clean rather than merely unexamined. So the clean variant is asserted to produce
nothing from any command, and each planted defect is asserted to be caught by the check that
owns it - a planted defect nobody finds means that check is dead, which reads exactly like a
clean chapter.
"""

import os
import shutil
import tempfile
import unittest

from fixtures import REPO, TEMPLATE  # noqa: F401  (puts scripts/ on sys.path)

from swlib import (cmd_arc, cmd_cast, cmd_curve, cmd_history, cmd_lint, cmd_readset,
                   cmd_selftest, cmd_state, cmd_status, cmd_write, sample)
from swlib.novelio import Novel


class Built(object):
    """The sample novel, scaffolded the way a user would get it."""

    def __init__(self, seeded=False):
        self.seeded = seeded

    def __enter__(self):
        self.dir = tempfile.mkdtemp(prefix="sw-sample-")
        os.makedirs(os.path.join(self.dir, "novels"))
        shutil.copytree(TEMPLATE, os.path.join(self.dir, "novels", "_template"))
        rep, ok = cmd_write.newnovel(sample.SLUG, self.dir)
        if not ok:
            raise AssertionError("newnovel refused: %s" % rep.render())
        self.root = os.path.join(self.dir, "novels", sample.SLUG)
        sample.build(self.root, seeded=self.seeded)
        self.novel = Novel(self.root)
        return self

    def __exit__(self, *exc):
        shutil.rmtree(self.dir, ignore_errors=True)
        return False

    def reports(self):
        n = self.novel
        return [("lint", cmd_lint.run(n, None)), ("cast", cmd_cast.run(n)),
                ("curve", cmd_curve.run(n)), ("state", cmd_state.run(n)),
                ("status", cmd_status.run(n)), ("arc", cmd_arc.run(n, 1)),
                ("history", cmd_history.run(n)[0])]


class TestCleanSample(unittest.TestCase):

    def test_no_command_finds_anything(self):
        with Built() as b:
            bad = []
            for name, rep in b.reports():
                for f in rep.findings:
                    if f.level in ("defect", "warn"):
                        bad.append("%s: %s %s: %s" % (name, f.level, f.check, f.message[:70]))
            self.assertEqual(bad, [], "the sample novel is supposed to be clean")

    def test_the_dialogue_share_sits_in_the_target_band(self):
        """On a silent cast the three voice skills do not fail - they no-op."""
        with Built() as b:
            for c in b.novel.chapters():
                self.assertTrue(25.0 <= c.speech_share <= 40.0,
                                "ch %s is at %.1f%% dialogue" % (c.number, c.speech_share))

    def test_word_counts_are_measured_not_hardcoded(self):
        with Built() as b:
            for c in b.novel.chapters():
                self.assertEqual(c.meta.get("wordcount"), c.words)
                self.assertEqual(b.novel.block(c.number).wc, c.words)

    def test_stamp_writes_nothing_to_a_correct_chapter(self):
        with Built() as b:
            rep, wrote = cmd_write.stamp(b.novel, 6)
            self.assertFalse(wrote, "stamp rewrote a file whose count was already right")
            self.assertEqual(rep.exit_code, 0)

    def test_the_read_set_carries_the_slices_it_is_defined_as_carrying(self):
        with Built() as b:
            text = cmd_readset.build(b.novel, 4, ["Wren", "Maro"], ["The Tidehouse"],
                                     want_society=True)
            for want in ("=C0003=", "Wren", "Maro", "Salt and Ledger", "VOICE MATRIX"):
                self.assertIn(want, text)
            self.assertNotIn("=C0004=", text,
                             "the read-set for ch 4 must stop at the previous block")


class TestPositiveControl(unittest.TestCase):

    def test_every_planted_defect_is_caught_by_the_check_that_owns_it(self):
        with Built(seeded=True) as b:
            caught = set()
            for _name, rep in b.reports():
                caught.update((f.check, f.level) for f in rep.findings
                              if f.level in ("defect", "warn"))
            for check, where, what, level in sample.SEEDED:
                self.assertIn((check, level), caught,
                              "planted %s in %s (%s) and nothing reported it at %s"
                              % (check, where, what, level))

    def test_the_seeds_have_no_side_effects(self):
        """A seed that trips extra checks makes the control less exact than it reads."""
        with Built(seeded=True) as b:
            caught = set()
            for _name, rep in b.reports():
                caught.update(f.check for f in rep.findings if f.level == "defect")
            self.assertEqual(sorted(caught - {c for c, _, _, _ in sample.SEEDED}), [])


class TestSelftestCommand(unittest.TestCase):

    def test_it_passes_against_this_repo(self):
        empty = tempfile.mkdtemp(prefix="sw-noxs-")
        try:
            rep = cmd_selftest.run(REPO, transcript_root=empty)
            bad = ["%s: %s" % (f.check, f.message[:90]) for f in rep.findings
                   if f.level == "defect"]
            self.assertEqual(bad, [])
            self.assertEqual(rep.exit_code, 0)
        finally:
            shutil.rmtree(empty, ignore_errors=True)

    def test_it_removes_its_workspace_on_success(self):
        empty = tempfile.mkdtemp(prefix="sw-noxs-")
        keep = os.path.join(tempfile.mkdtemp(prefix="sw-keep-"), "here")
        try:
            rep = cmd_selftest.run(REPO, transcript_root=empty)
            paths = [l.strip() for h, lines in rep.sections if h == "workspace"
                     for l in lines]
            self.assertTrue(any("removed" in p for p in paths), paths)
            self.assertFalse(os.path.isdir(paths[0]), "the temp workspace outlived the run")

            os.makedirs(keep)
            cmd_selftest.run(REPO, keep=keep, transcript_root=empty)
            self.assertTrue(os.path.isdir(os.path.join(keep, "clean", "novels", sample.SLUG)),
                            "--keep did not leave the built novel behind")
        finally:
            shutil.rmtree(empty, ignore_errors=True)
            shutil.rmtree(os.path.dirname(keep), ignore_errors=True)


if __name__ == "__main__":
    unittest.main()
