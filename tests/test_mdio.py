"""Frontmatter and the hand-rolled YAML reader.

Everything downstream reads config through here, so a silent parse failure does not look like
a parse failure. It looks like a novel with no MC.
"""

import unittest

from fixtures import NOVEL_MD, NovelFixture
from swlib import mdio


class TestReadText(unittest.TestCase):

    def test_bom_does_not_hide_the_frontmatter(self):
        """Was: a BOM made `\\A---` fail, so every chapter read as having no frontmatter."""
        with NovelFixture() as fx:
            fx.add_chapter(1, "The room was cold.\n", bom=True)
            ch = fx.novel().chapters()[0]
            self.assertNotEqual(ch.frontmatter_text, "")
            self.assertEqual(ch.number, 1)

    def test_crlf_is_normalised_for_reading(self):
        with NovelFixture() as fx:
            fx.add_chapter(1, "The room was cold.\n", newline="\r\n")
            ch = fx.novel().chapters()[0]
            self.assertNotIn("\r", ch.body)
            self.assertEqual(ch.number, 1)

    def test_read_text_raw_reports_the_line_ending(self):
        with NovelFixture() as fx:
            path = fx.add_chapter(1, "The room was cold.\n", newline="\r\n")
            _text, newline, ok = mdio.read_text_raw(path)
            self.assertEqual(newline, "\r\n")
            self.assertTrue(ok)


class TestYaml(unittest.TestCase):

    def test_tabs_keep_their_nesting(self):
        """Was: `mc:` came back {} and `name` was promoted to the top level."""
        cfg = mdio.parse_yaml("mc:\n\tname: Mira\n\tintel_tier: 4\n")
        self.assertEqual(mdio.dig(cfg, "mc.name"), "Mira")
        self.assertEqual(mdio.dig(cfg, "mc.intel_tier"), 4)

    def test_unclosed_quote_does_not_eat_the_next_key(self):
        """Was: one missing quote silently deleted the rest of the config."""
        cfg = mdio.parse_yaml('voice_notes: "never closes\nnumber: 7\nstatus: drafted\n')
        self.assertEqual(cfg.get("number"), 7)
        self.assertEqual(cfg.get("status"), "drafted")

    def test_multi_line_quoted_scalar_still_joins(self):
        cfg = mdio.parse_yaml('note: "she speaks in short bursts,\n  clipped and factual"\n')
        self.assertIn("clipped and factual", cfg["note"])

    def test_hash_after_whitespace_is_a_comment(self):
        """Per YAML: `Book #2` really is `Book`. Quote it if you meant the hash."""
        self.assertEqual(mdio.parse_yaml("title: Book #2 of three\n")["title"], "Book")
        self.assertEqual(mdio.parse_yaml('title: "Book #2 of three"\n')["title"],
                         "Book #2 of three")

    def test_colon_inside_a_value_survives(self):
        cfg = mdio.parse_yaml('title: "Naruto: The New God of Shinobi"\n')
        self.assertEqual(cfg["title"], "Naruto: The New God of Shinobi")

    def test_the_shipped_template_parses(self):
        with NovelFixture() as fx:
            novel = fx.novel()
            self.assertEqual(novel.get("mc.name"), "Rin")
            self.assertEqual(novel.get("chapters.arc_length"), 25)
            self.assertEqual(novel.get("channels.thought"), "'…'")

    def test_fixture_config_matches_the_document(self):
        cfg = mdio.parse_yaml(mdio.split_frontmatter(NOVEL_MD)[0])
        self.assertEqual(cfg["genre"], "fantasy")


if __name__ == "__main__":
    unittest.main()
