"""The knowledge-base index.

The index is derived from frontmatter on every call rather than stored, so these tests are the
only thing standing between a typo'd `owner:` and a card that silently stops being dispatched.
They run against the real corpus as well as fixtures: a synthetic tree that supplies the thing
under test cannot catch the corpus drifting away from it.
"""

import os
import re
import unittest

from fixtures import REPO


def read(path):
    with open(path, encoding="utf-8") as fh:
        return fh.read()

from swlib import kb, kbexpr


class TestAgainstTheRealCorpus(unittest.TestCase):

    def setUp(self):
        self.idx = kb.index(REPO, refresh=True)

    def test_every_skill_is_indexed(self):
        on_disk = sorted(d for d in os.listdir(os.path.join(REPO, ".claude", "skills"))
                         if os.path.isfile(os.path.join(REPO, ".claude", "skills", d, "SKILL.md")))
        self.assertEqual(sorted(self.idx.skills), on_disk)

    def test_no_concept_is_claimed_twice(self):
        self.assertEqual(self.idx.problems, [])

    def test_every_skill_owns_something(self):
        bare = sorted(s.name for s in self.idx.skills.values() if not s.owns)
        self.assertEqual(bare, [], "every skill declares the concepts it is the authority on")

    def test_card_counts_match_the_filesystem(self):
        for kind, fname in (("draft-card", "draft-card.md"), ("audit-card", "audit-card.md")):
            on_disk = [s for s in self.idx.skills
                       if os.path.isfile(os.path.join(REPO, ".claude", "skills", s,
                                                      "references", fname))]
            self.assertEqual(len(self.idx.by_type(kind)), len(on_disk), kind)

    def test_a_card_knows_its_dispatcher(self):
        """The one inversion in the corpus: a card is opened by its dispatcher, not its skill."""
        for f in self.idx.by_type("draft-card"):
            self.assertEqual(f.dispatcher, "write-chapter", f.rel)
        for f in self.idx.by_type("audit-card"):
            self.assertEqual(f.dispatcher, "revision-pass", f.rel)

    def test_entry_prefers_the_draft_card(self):
        """The cheapest correct entry point, and the read-set must agree with the resolver."""
        from swlib import cmd_readset
        for name in self.idx.skills:
            self.assertEqual(self.idx.entry(name), cmd_readset._module_entry(name), name)

    def test_owners_map_matches_health(self):
        """`sw health` builds the same map independently; they must not disagree."""
        from swlib import cmd_health, mdio
        owners = {}
        for name in self.idx.skills:
            path = os.path.join(REPO, ".claude", "skills", name, "SKILL.md")
            cfg = mdio.parse_yaml(mdio.split_frontmatter(mdio.read_text(path))[0])
            meta = cfg.get("metadata") or {}
            for slug in kb._as_list(meta.get("owns", cfg.get("owns"))):
                owners[slug] = name
        self.assertEqual(self.idx.owners, owners)
        self.assertTrue(hasattr(cmd_health, "_owns_map"))

    def test_validate_is_clean(self):
        from swlib.report import Report
        rep = Report("t")
        from swlib import cmd_kb
        cmd_kb.validate(self.idx, rep)
        self.assertEqual([f for f in rep.findings if f.level == "defect"], [])


class TestReproducesTheDispatcherTables(unittest.TestCase):
    """The migration's correctness proof, and the gate on deleting the tables.

    Every card's `decision` and `when` was transcribed out of `write-chapter`'s two tables and
    `revision-pass`'s pass table. Until the index can reproduce those tables exactly, the tables
    are still the authority and must not be deleted. Once they are deleted this class is what
    remains of them, which is why it reads them from disk rather than restating them.
    """

    CARD = re.compile(r"`([a-z-]+)/references/draft-card\.md`")
    AUDIT = re.compile(r"`([a-z-]+)/references/audit-card\.md`")

    def setUp(self):
        self.idx = kb.index(REPO, refresh=True)
        self.wc = read(os.path.join(REPO, ".claude", "skills", "write-chapter", "SKILL.md"))
        self.rp = read(os.path.join(REPO, ".claude", "skills", "revision-pass", "SKILL.md"))

    def _table(self, text, header):
        m = re.search(re.escape(header) + r"\n\|[-| ]+\|\n((?:\|.*\n)+)", text)
        if not m:
            return []
        rows = []
        for line in m.group(1).split("\n"):
            if line.startswith("|") and not re.match(r"^\|[\s:\-|]+\|", line):
                rows.append([c.strip() for c in line.strip().strip("|").split("|")])
        return rows

    def test_phase_a_owners_match_the_table(self):
        table = self._table(self.wc, "| decision | card |")
        cond = self._table(self.wc, "| condition | decision | card |")
        if not table:
            self.skipTest("the dispatcher table has been deleted; the index is now the authority")
        want = [self.CARD.search(r[1]).group(1) for r in table]
        want += [self.CARD.search(r[2]).group(1) for r in cond]
        got = [f.owner for f in sorted(self.idx.by_type("draft-card"), key=kb._card_sort)
               if f.phase == "A"]
        self.assertEqual(got, want, "phase A card order must match write-chapter's table")

    def test_phase_b_owners_match_the_bullets(self):
        want = re.findall(r"- \*\*(?:.+?)\.\*\* `([a-z-]+)/references/draft-card\.md`", self.wc)
        if not want:
            self.skipTest("the phase B bullets have been deleted")
        got = sorted(f.owner for f in self.idx.by_type("draft-card") if f.phase == "B")
        self.assertEqual(got, sorted(want))

    def test_every_draft_card_is_dispatched_exactly_once(self):
        cards = self.idx.by_type("draft-card")
        self.assertEqual(len(cards), len({f.owner for f in cards}))
        for f in cards:
            self.assertIn(f.phase, ("A", "B"), "%s declares no phase" % f.rel)
            self.assertTrue(f.when, "%s declares no trigger" % f.rel)
            self.assertTrue(f.description, "%s declares no decision" % f.rel)

    def test_audit_card_owners_match_the_pass_table(self):
        m = re.search(r"\n\|[^\n]*pass[^\n]*\|\n\|[-| :]+\|\n((?:\|.*\n)+)", self.rp, re.I)
        if not m:
            self.skipTest("the pass table has been deleted")
        want = sorted(set(self.AUDIT.findall(m.group(1))))
        got = sorted(f.owner for f in self.idx.by_type("audit-card"))
        self.assertEqual(got, want)

    def test_every_audit_card_names_its_pass(self):
        for f in self.idx.by_type("audit-card"):
            self.assertTrue(f.pass_, "%s declares no pass" % f.rel)
            self.assertTrue(f.when, "%s declares no trigger" % f.rel)

    def test_conditional_cards_carry_a_real_condition(self):
        """The four conditional rows are the ones a migration could silently get wrong."""
        want = {"story-opening": "chapter <= opening.contract_by_ch + 2",
                "power-scaling": "scaling.shape != none",
                "meta-knowledge": "mc.foreknowledge is set",
                "mc-design": "mc.form_locked == true"}
        got = {f.owner: f.when for f in self.idx.by_type("draft-card")
               if f.owner in want}
        self.assertEqual(got, want)

    def test_every_trigger_parses_and_names_real_config(self):
        from swlib import novelio
        flat = set(_flat(novelio.Novel(os.path.join(REPO, "novels", "_template")).cfg))
        builtins = set(kbexpr.Context.BUILTINS)
        bad = []
        for f in self.idx.files:
            for expr in filter(None, [f.when]):
                for path in kbexpr.paths(expr):
                    if path not in flat and path not in builtins \
                            and not path.startswith(("optional.", "draft.")):
                        bad.append("%s: %s" % (f.rel, path))
        for s in self.idx.skills.values():
            for expr in filter(None, [s.when]):
                for path in kbexpr.paths(expr):
                    if path not in flat and path not in builtins \
                            and not path.startswith(("optional.", "draft.")):
                        bad.append("%s: %s" % (s.name, path))
        self.assertEqual(sorted(bad), [], "triggers naming config keys the template lacks")


def _flat(cfg, prefix=""):
    for key, val in (cfg or {}).items():
        path = "%s%s" % (prefix, key)
        yield path
        if isinstance(val, dict):
            for sub in _flat(val, path + "."):
                yield sub


class TestBothFrontmatterShapes(unittest.TestCase):
    """The index must read the pre- and post-migration shapes, so the two can be diffed."""

    def test_as_list_accepts_a_list_or_a_string(self):
        self.assertEqual(kb._as_list(["a", "b"]), ["a", "b"])
        self.assertEqual(kb._as_list("a, b"), ["a", "b"])
        self.assertEqual(kb._as_list("[a, b]"), ["a", "b"])
        self.assertEqual(kb._as_list(""), [])
        self.assertEqual(kb._as_list(None), [])


class TestCardResolution(unittest.TestCase):
    """Resolution is the whole point: the right cards for this chapter, and why not the others."""

    class FakeIndex(kb.Index):
        def __init__(self, files):
            self.repo_root = REPO
            self.skills, self.owners, self.problems = {}, {}, []
            self.files = files

    def card(self, owner, when, phase="A", order=None):
        return kb.FileEntry(path="/x", rel="%s/draft-card.md" % owner, type="draft-card",
                            owner=owner, dispatcher="write-chapter", phase=phase,
                            order=order, description="", when=when, concepts=[])

    def test_false_conditions_are_reported_not_dropped(self):
        idx = self.FakeIndex([self.card("a", "always"),
                              self.card("b", "chapter <= 3")])
        fired, skipped = idx.cards("draft-card", kbexpr.Context(None, chapter=9))
        self.assertEqual([f.owner for f, _s, _w in fired], ["a"])
        self.assertEqual([f.owner for f, _w in skipped], ["b"])
        self.assertTrue(skipped[0][1], "a skipped card must say why")

    def test_unknown_is_included_not_skipped(self):
        """A card wrongly opened costs tokens; one wrongly skipped costs a chapter defect."""
        idx = self.FakeIndex([self.card("a", "chapter <= nonsense.key + 1")])
        fired, skipped = idx.cards("draft-card", kbexpr.Context(None, chapter=1))
        self.assertEqual(len(fired), 1)
        self.assertIs(fired[0][1], kbexpr.UNKNOWN)
        self.assertEqual(skipped, [])

    def test_order_puts_first_always_first(self):
        idx = self.FakeIndex([self.card("zeta", "always"),
                              self.card("story-craft", "always", order=1)])
        fired, _ = idx.cards("draft-card", kbexpr.Context(None, chapter=1))
        self.assertEqual([f.owner for f, _s, _w in fired], ["story-craft", "zeta"])

    def test_phase_filters(self):
        idx = self.FakeIndex([self.card("a", "always", phase="A"),
                              self.card("b", "always", phase="B")])
        fired, _ = idx.cards("draft-card", kbexpr.Context(None, chapter=1), phase="B")
        self.assertEqual([f.owner for f, _s, _w in fired], ["b"])


if __name__ == "__main__":
    unittest.main()
