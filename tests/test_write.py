"""`stamp` is the only command that edits a file a human wrote. It must not touch the prose.

The documented contract is "frontmatter, the CCS `wc:` field, and a fresh scaffold". The first
implementation re-serialised the whole chapter, which converted CRLF prose to LF and wrote
U+FFFD over any byte it could not decode.
"""

import unittest

from fixtures import NovelFixture
from swlib import cmd_write

BODY = "The room was cold.\n\n\"Shut it,\" she said.\n\nHe shut it.\n"


class TestStamp(unittest.TestCase):

    def test_body_is_byte_identical_after_stamping(self):
        with NovelFixture() as fx:
            fx.add_chapter(1, BODY, wordcount=1)
            before = fx.read_bytes("chapters/0001-chapter.md")
            rep, wrote = cmd_write.stamp(fx.novel(), 1)
            after = fx.read_bytes("chapters/0001-chapter.md")
            self.assertTrue(wrote)
            self.assertNotEqual(before, after)
            body_before = before.split(b"---", 2)[2]
            body_after = after.split(b"---", 2)[2]
            self.assertEqual(body_before, body_after)

    def test_crlf_prose_stays_crlf(self):
        """Was: a CRLF chapter came back LF, so `stamp` showed as a whole-file diff."""
        with NovelFixture() as fx:
            fx.add_chapter(1, BODY, wordcount=1, newline="\r\n")
            cmd_write.stamp(fx.novel(), 1)
            raw = fx.read_bytes("chapters/0001-chapter.md")
            self.assertIn(b"\r\n", raw)
            # every LF is half of a CRLF: nothing was converted on the way through
            self.assertEqual(raw.count(b"\n"), raw.count(b"\r\n"))

    def test_bom_is_preserved(self):
        with NovelFixture() as fx:
            fx.add_chapter(1, BODY, wordcount=1, bom=True)
            cmd_write.stamp(fx.novel(), 1)
            self.assertTrue(fx.read_bytes("chapters/0001-chapter.md").startswith(b"\xef\xbb\xbf"))

    def test_wordcount_is_corrected(self):
        with NovelFixture() as fx:
            fx.add_chapter(1, BODY, wordcount=9999)
            cmd_write.stamp(fx.novel(), 1)
            self.assertEqual(fx.novel().chapters()[0].meta["wordcount"], len(BODY.split()))

    def test_nothing_written_when_already_correct(self):
        with NovelFixture() as fx:
            fx.add_chapter(1, BODY)
            before = fx.read_bytes("chapters/0001-chapter.md")
            _rep, wrote = cmd_write.stamp(fx.novel(), 1)
            self.assertFalse(wrote)
            self.assertEqual(before, fx.read_bytes("chapters/0001-chapter.md"))

    def test_undecodable_bytes_are_refused_not_replaced(self):
        """Was: the bad byte came back as U+FFFD, permanently, inside the author's prose."""
        with NovelFixture() as fx:
            path = fx.add_chapter(1, BODY, wordcount=1)
            with open(path, "rb") as fh:
                raw = fh.read()
            with open(path, "wb") as fh:
                fh.write(raw.replace(b"The room", b"The r\xffom"))
            before = fx.read_bytes("chapters/0001-chapter.md")
            rep, wrote = cmd_write.stamp(fx.novel(), 1)
            self.assertFalse(wrote)
            self.assertEqual(before, fx.read_bytes("chapters/0001-chapter.md"))
            self.assertTrue(any(f.check == "encoding" for f in rep.findings))

    def test_missing_frontmatter_is_refused(self):
        with NovelFixture() as fx:
            fx.add_chapter(1, BODY, frontmatter="No frontmatter here.\n")
            rep, wrote = cmd_write.stamp(fx.novel(), 1)
            self.assertFalse(wrote)
            self.assertTrue(any(f.check == "frontmatter" for f in rep.findings))


class TestNewNovel(unittest.TestCase):

    def test_refuses_to_overwrite(self):
        with NovelFixture() as fx:
            root = fx.repo_root
            rep, ok = cmd_write.newnovel(fx.slug, root)
            self.assertFalse(ok)
            self.assertTrue(any("refusing to overwrite" in f.message for f in rep.findings))

    def test_rejects_a_bad_slug(self):
        with NovelFixture() as fx:
            root = fx.repo_root
            _rep, ok = cmd_write.newnovel("Not A Slug", root)
            self.assertFalse(ok)


if __name__ == "__main__":
    unittest.main()
