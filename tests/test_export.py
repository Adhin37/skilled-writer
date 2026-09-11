"""`sw export --okf`.

The bundle is an export target, so these tests check two things: that it is conformant OKF, and
that producing it never touches the novel it was projected from.
"""

import os
import shutil
import tempfile
import unittest

from fixtures import NovelFixture

BODY = "The room was cold.\n\n\"Shut it,\" she said.\n\nHe shut it.\n"

from swlib import cmd_export, mdio


class TestExport(unittest.TestCase):

    def setUp(self):
        self.out = os.path.join(tempfile.mkdtemp(prefix="sw-okf-"), "bundle")

    def tearDown(self):
        shutil.rmtree(os.path.dirname(self.out), ignore_errors=True)

    def _build(self, fx):
        return cmd_export.build(fx.novel(), self.out).write()

    def test_every_document_has_a_type(self):
        """OKF section 11's one universal requirement."""
        with NovelFixture() as fx:
            fx.add_chapter(1, BODY)
            self._build(fx)
            for sub, _d, files in os.walk(self.out):
                for f in files:
                    if not f.endswith(".md") or f in cmd_export.__dict__.get("RESERVED", ()):
                        continue
                    if f in ("index.md", "log.md"):
                        continue
                    fm = mdio.parse_yaml(
                        mdio.split_frontmatter(mdio.read_text(os.path.join(sub, f)))[0])
                    self.assertTrue(str(fm.get("type") or "").strip(),
                                    "%s has no type" % os.path.join(sub, f))

    def test_the_root_index_declares_the_version(self):
        with NovelFixture() as fx:
            fx.add_chapter(1, BODY)
            self._build(fx)
            fm = mdio.parse_yaml(
                mdio.split_frontmatter(mdio.read_text(os.path.join(self.out, "index.md")))[0])
            self.assertEqual(str(fm.get("okf_version")), cmd_export.OKF_VERSION)

    def test_every_document_says_where_it_came_from(self):
        """`resource:` is the honest half: the bundle is a projection, not the original."""
        with NovelFixture() as fx:
            fx.add_chapter(1, BODY)
            self._build(fx)
            for sub, _d, files in os.walk(self.out):
                for f in files:
                    if f in ("index.md", "log.md"):
                        continue
                    fm = mdio.parse_yaml(
                        mdio.split_frontmatter(mdio.read_text(os.path.join(sub, f)))[0])
                    self.assertTrue(fm.get("resource"), "%s names no source" % f)

    def test_it_does_not_touch_the_novel(self):
        """The novel is the thing being described; describing it may not modify it."""
        with NovelFixture() as fx:
            fx.add_chapter(1, BODY)
            before = _snapshot(fx.root)
            self._build(fx)
            self.assertEqual(_snapshot(fx.root), before)

    def test_the_prose_is_not_copied_into_the_bundle(self):
        """Knowledge about the novel, not a second copy of the book."""
        with NovelFixture() as fx:
            fx.add_chapter(1, BODY)
            self._build(fx)
            text = mdio.read_text(os.path.join(self.out, "chapters", "0001.md"))
            self.assertNotIn(BODY.strip()[:60], text)


def _snapshot(root):
    out = {}
    for sub, _dirs, files in os.walk(root):
        for f in sorted(files):
            p = os.path.join(sub, f)
            out[os.path.relpath(p, root)] = os.path.getsize(p)
    return out


if __name__ == "__main__":
    unittest.main()
