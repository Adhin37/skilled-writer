"""The knowledge-base index.

The index is derived from frontmatter on every call rather than stored, so these tests are the
only thing standing between a typo'd `owner:` and a card that silently stops being dispatched.
They run against the real corpus as well as fixtures: a synthetic tree that supplies the thing
under test cannot catch the corpus drifting away from it.
"""

import os
import re
import shutil
import tempfile
import unittest

from fixtures import REPO


def read(path):
    with open(path, encoding="utf-8") as fh:
        return fh.read()


def write(path, text):
    with open(path, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(text)

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
        for kind, stem in (("draft-card", ".draft-card.md"), ("audit-card", ".audit-card.md")):
            bucket = os.path.join(REPO, kb.ROLES_REL, kb.CARD_ROLES[kind])
            on_disk = [f for f in os.listdir(bucket) if f.endswith(stem)]
            self.assertEqual(len(self.idx.by_type(kind)), len(on_disk), kind)

    def test_a_card_lives_in_its_role_tree_and_nowhere_else(self):
        """The split, as an assertion. A card under `.claude/skills/` is a half-done move."""
        for kind, role in kb.CARD_ROLES.items():
            for f in self.idx.by_type(kind):
                self.assertEqual(f.bucket, role, f.rel)
                self.assertTrue(f.rel.startswith("%s/%s/" % (kb.ROLES_REL, role)), f.rel)
                self.assertEqual(os.path.basename(f.rel), "%s.%s.md" % (f.owner, kind), f.rel)

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

    # Both citation forms, because a dispatcher may name a card either way and the tests below
    # must not go quiet when the layout moves under them: a regex that stops matching turns
    # `test_phase_b_owners_match_the_bullets` into a skip whose message says the bullets were
    # deleted. They were not. That is the migration's correctness proof reporting success.
    _TREE = r"(?:(?:%s)/[a-z]+/)?" % "|".join(re.escape(d) for d in kb.ROLES_DIRS)
    CARD = re.compile(r"`" + _TREE + r"([a-z-]+)[/.](?:references/)?draft-card\.md`")
    AUDIT = re.compile(r"`" + _TREE + r"([a-z-]+)[/.](?:references/)?audit-card\.md`")

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
        want = re.findall(r"- \*\*(?:.+?)\.\*\* " + self.CARD.pattern, self.wc)
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
        if not want:
            self.skipTest("the card column has been removed; the index is now the authority")
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


class TestRoles(unittest.TestCase):
    """The role axis: which agent may open a skill.

    Roles route; they move nothing. The tests that matter are that every skill is reachable by
    somebody, that the draft/gate halves still agree with the cards on disk, and that the one
    role with no corpus stays that way - a `review` view that started returning skills would
    mean the blind reader had quietly stopped being blind.
    """

    def setUp(self):
        self.idx = kb.index(REPO, refresh=True)

    def test_every_skill_declares_a_role(self):
        self.assertEqual(self.idx.roleless(), [])

    def test_no_skill_declares_an_unknown_role(self):
        self.assertEqual(self.idx.bad_roles(), [])

    def test_draft_role_matches_the_draft_cards_on_disk(self):
        by_card = set()
        for f in self.idx.by_type("draft-card"):
            by_card.add(f.owner)
        by_role = set(s.name for s in self.idx.view("draft")[0])
        # Every skill carrying a draft card must be in the draft view. The converse does not
        # hold: `bias-guard` is force: absolute and binds the drafter with no card of its own.
        self.assertEqual(by_card - by_role, set())

    def test_gate_role_matches_the_audit_cards_on_disk(self):
        by_card = set(f.owner for f in self.idx.by_type("audit-card"))
        by_role = set(s.name for s in self.idx.view("gate")[0])
        self.assertEqual(by_card - by_role, set())

    def test_review_carries_no_corpus(self):
        skills, cards = self.idx.view("review")
        self.assertEqual(skills, [])
        self.assertEqual(cards, [])
        self.assertIn("review", kb.ROLES_WITHOUT_CORPUS)

    def test_the_dispatchers_are_the_coordinate_role(self):
        self.assertEqual(sorted(s.name for s in self.idx.view("coordinate")[0]),
                         ["continuity-summary", "revision-pass", "write-chapter"])

    def test_skills_serve_more_than_one_role(self):
        # The argument against a per-role folder split, asserted rather than asserted-in-prose:
        # if this ever drops to zero the split becomes free and this test should be deleted.
        both = [s for s in self.idx.skills.values()
                if "draft" in s.role and "gate" in s.role]
        self.assertGreater(len(both), 20)

    def test_every_role_but_review_reaches_something(self):
        for role in kb.ROLES:
            if role in kb.ROLES_WITHOUT_CORPUS:
                continue
            self.assertTrue(self.idx.view(role)[0], "role %s resolves to an empty view" % role)

    def test_view_resolves_cards_against_a_novel(self):
        ctx = kbexpr.Context(None, chapter=1)
        skills, cards = self.idx.view("draft", ctx)
        self.assertTrue(skills)
        self.assertTrue(cards)
        self.assertTrue(all(f.type == "draft-card" for f, _s, _w in cards))


class TestOwnedFiles(unittest.TestCase):
    """`owned_files` is the one answer to "what is a skill's corpus?".

    It replaced four separate `os.walk`s of a skill's directory. A walk silently means
    "whatever happens to be filed here", so it attributes a misfiled note to the directory
    rather than to the owner the note declares - and it would stop comparing a file the moment
    the file moved out of the tree, without any of the four noticing.
    """

    def setUp(self):
        self.idx = kb.index(REPO, refresh=True)

    def test_it_is_the_body_plus_everything_that_declares_the_owner(self):
        for name in self.idx.skills:
            owned = self.idx.owned_files(name)
            self.assertEqual(owned[0], self.idx.skills[name].path,
                             "the body must come first - a 10-word run spans the join")
            declared = {f.path for f in self.idx.files if f.owner == name}
            self.assertEqual(set(owned[1:]), declared)

    def test_every_corpus_file_is_owned_by_exactly_one_skill(self):
        """The partition property the physical split depends on, asserted before the move."""
        seen = {}
        for name in self.idx.skills:
            for path in self.idx.owned_files(name)[1:]:
                self.assertNotIn(path, seen, "%s is owned twice" % path)
                seen[path] = name
        self.assertEqual(len(seen), len(self.idx.files))

    def test_the_order_is_stable_and_does_not_depend_on_the_directory(self):
        """Ordered by the name the corpus cites, which is the one thing a move cannot change.

        Basename order would have done before the split and after it, and gone wrong only in
        between - a skill with one card moved and one note not yet moved sorts
        `narrator-voice.audit-card.md` against `channels.md` and silently reorders the
        concatenation the duplication check reads.
        """
        by_owner = {}
        for f in self.idx.files:
            by_owner.setdefault(f.owner, []).append(f)
        for name in self.idx.skills:
            owned = self.idx.owned_files(name)[1:]
            cites = [f.cite for f in sorted(by_owner.get(name, []),
                                            key=lambda f: f.path)]
            got = []
            for path in owned:
                got.extend(f.cite for f in by_owner[name] if f.path == path)
            self.assertEqual(got, sorted(cites), name)


class TestCitationResolution(unittest.TestCase):
    """One regex and one resolver, where there used to be three copies of the regex.

    Three copies is three chances to teach the corpus a citation form that only two of them
    accept - and the one that does not accept it reports a defect against a file that is fine.
    """

    def setUp(self):
        self.idx = kb.index(REPO, refresh=True)

    def _resolve(self, text, citing=None):
        m = kb.CITATION.search(text)
        return None if m is None else self.idx.resolve(m, citing)

    def test_the_bare_form_means_my_own(self):
        self.assertIsNotNone(self._resolve("references/draft-card.md", "story-craft"))
        self.assertIsNone(self._resolve("references/draft-card.md", "bias-guard"))

    def test_the_qualified_form_names_another_skill(self):
        f = self._resolve("world-texture/references/audit-card.md", "plot-threads")
        self.assertEqual(f.owner, "world-texture")

    def test_the_written_out_form_resolves_the_same_way(self):
        a = self._resolve(".claude/skills/story-craft/references/draft-card.md")
        b = self._resolve("story-craft/references/draft-card.md")
        self.assertEqual(a.rel, b.rel)

    def test_a_word_ending_in_roles_is_not_a_role_citation(self):
        """The role tree sits at the repo root, so `roles/` is no longer preceded by a literal
        `.claude/` that bounds the match on its left. A lookbehind does that job instead, and
        without it any word ending in "roles" starts a citation.
        """
        m = kb.CITATION.search("controles/draft/story-craft.draft-card.md")
        self.assertIsNone(m if m is None else m.group("rolefile"))

    def test_both_role_tree_layouts_resolve_to_the_same_file(self):
        """A citation written before a move still names a real file on the day of the move,
        which is what lets the migration find the text it has to rewrite. Resolving is not the
        same as being correct: `test_corpus.test_every_referenced_file_exists` asks the
        filesystem, and that is the check that insists the text actually be rewritten.
        """
        for layout in kb.ROLES_DIRS:
            m = kb.CITATION.search("`%s/draft/story-craft.draft-card.md`" % layout)
            self.assertIsNotNone(m, layout)
            self.assertEqual(m.group("rolefile"), "story-craft.draft-card.md", layout)

    def test_the_bare_form_is_a_citation_only_when_the_owner_has_the_file(self):
        """One card cites this way, and a closure blind to it filed the note as unreachable."""
        self.assertIsNotNone(self._resolve("`ai-default-tells.md`.", "prose-quality"))
        self.assertIsNone(self._resolve("`ai-default-tells.md`.", "mtl-detox"))

    def test_it_resolves_none_of_the_md_files_that_are_not_citations(self):
        """`CLAUDE.md`, `novel.md` and `state/threads.md` are named all over the corpus.

        The bare form makes these *match*, which is why resolution rather than the regex is
        what J2 keys on - see the guard in `cmd_health._references`.
        """
        for text in ("see CLAUDE.md section 3", "write state/threads.md", "novel.md is the truth",
                     "chapters/0001-a.md", "open bible/world.md"):
            for name in self.idx.skills:
                self.assertIsNone(self._resolve(text, name), "%s (citing %s)" % (text, name))

    def test_every_citation_in_the_corpus_resolves(self):
        """J2, asserted directly against the corpus rather than through the report."""
        bad = []
        for name in sorted(self.idx.skills):
            for path in self.idx.owned_files(name):
                with open(path, encoding="utf-8") as fh:
                    text = fh.read()
                for m in kb.CITATION.finditer(text):
                    if m.group("bare"):
                        continue   # ordinary prose unless it resolves; see the regex comment
                    if self.idx.resolve(m, name) is None:
                        bad.append("%s -> %s" % (name, m.group(0)))
        self.assertEqual([], bad)


class TestEntryIsIndexDriven(unittest.TestCase):

    def setUp(self):
        self.idx = kb.index(REPO, refresh=True)

    def test_it_returns_the_draft_card_where_there_is_one(self):
        f = self.idx.entry("story-craft")
        self.assertTrue(f.endswith("draft-card.md"), f)
        self.assertIsNotNone(self.idx._by_rel.get(f))

    def test_it_falls_back_to_the_body(self):
        self.assertTrue(self.idx.entry("bias-guard").endswith("SKILL.md"))

    def test_it_never_guesses_a_path_that_is_not_in_the_index(self):
        """It used to `os.path.isfile` a path it had constructed, which is a second layout."""
        for name in self.idx.skills:
            rel = self.idx.entry(name)
            self.assertTrue(os.path.isfile(os.path.join(REPO, rel)), rel)


class TestReachable(unittest.TestCase):
    """The closure that sorts a corpus file into a bucket, and the seed that is easy to forget.

    A writing role reaches what its cards cite - and what its **dispatcher body** cites, because
    `draft` and `gate` each open exactly one body, preloaded through `skills:` and granted by
    path in the Read guard. Seeding from cards alone is a mistake that has been made twice here
    and failed silently both times: nothing errors, the role simply stops opening a file it
    needs, and every check stays green.
    """

    OWNED_PASSES = "%s/gate/revision-pass.owned-passes.md" % kb.ROLES_REL

    def setUp(self):
        self.idx = kb.index(REPO, refresh=True)

    def citers(self, entry):
        """Every corpus file whose text resolves to `entry`. The closure's input, measured."""
        out = []
        for f in self.idx.files:
            for m in kb.CITATION.finditer(read(f.path)):
                if self.idx.resolve(m, f.owner) is entry:
                    out.append(f.rel)
                    break
        for name, skill in self.idx.skills.items():
            for m in kb.CITATION.finditer(read(skill.path)):
                if self.idx.resolve(m, name) is entry:
                    out.append("SKILL:%s" % name)
                    break
        return sorted(out)

    def test_every_card_is_reachable_by_the_role_that_opens_it(self):
        for kind, role in kb.CARD_ROLES.items():
            reach = self.idx.reachable(role)
            for f in self.idx.by_type(kind):
                self.assertIn(f.rel, reach, f.rel)

    def test_the_dispatcher_body_is_a_seed(self):
        """The file that proved it, still proving it.

        `revision-pass.owned-passes.md` carries six of the gate's own passes and is cited by
        nothing but `revision-pass/SKILL.md` - so a card-only closure sees no citation of it at
        all and files it as unreachable. Drop the body from the seed and the gate stops opening
        Passes 1, 4, 7, 9, 9d and 10 with no error anywhere.
        """
        entry = self.idx._by_rel.get(self.OWNED_PASSES)
        self.assertIsNotNone(entry, self.OWNED_PASSES)
        self.assertEqual(self.citers(entry), ["SKILL:revision-pass"],
                         "no card cites it - the dispatcher body is the only route")
        self.assertIn("revision-pass", kb.DISPATCHER_BODIES["gate"])
        self.assertIn(self.OWNED_PASSES, self.idx.reachable("gate"))

    def test_neither_role_reaches_the_other_s_cards(self):
        """Part 7's sixth assertion, asserted where it belongs rather than as a second check.

        `cmd_health._partition()` does not implement it: it is the special case of the bucket
        comparison where the disagreement is a card's, and a `draft/` file the gate reaches
        already wants `shared/`. Pinning it here keeps the claim falsifiable without giving the
        repo two checks that fail together.
        """
        draft, gate = self.idx.reachable("draft"), self.idx.reachable("gate")
        for f in self.idx.by_type("audit-card"):
            self.assertNotIn(f.rel, draft, f.rel)
        for f in self.idx.by_type("draft-card"):
            self.assertNotIn(f.rel, gate, f.rel)

    def test_no_body_is_reachable_from_either_writing_role(self):
        """Bodies enter the closure as seeds and leave it as `SKILL:<name>`, never as a path.

        The distinction is the whole split: the dispatcher is preloaded, so its text is in the
        role's context already, and nothing the closure returns is a body a role would have to
        go and open.
        """
        for role in kb.CARD_ROLES.values():
            for rel in self.idx.reachable(role):
                self.assertFalse(rel.endswith("SKILL.md"), rel)
                if rel.startswith("SKILL:"):
                    self.assertIn(rel[len("SKILL:"):], kb.DISPATCHER_BODIES[role])

    def test_bucket_for_states_a_property_not_a_membership(self):
        """`shared` means opened by more than one role; `design` is the residue.

        Design reads every bucket, so `design` is never a claim about where the architect stops
        looking - only that no card and no dispatcher body arrives at the file.
        """
        reach = {"draft": {"a", "b"}, "gate": {"b", "c"}}
        self.assertEqual(self.idx.bucket_for("a", reach), "draft")
        self.assertEqual(self.idx.bucket_for("b", reach), "shared")
        self.assertEqual(self.idx.bucket_for("c", reach), "gate")
        self.assertEqual(self.idx.bucket_for("d", reach), "design")

    def test_a_body_dropped_into_a_role_tree_is_not_a_corpus_file(self):
        """`SKILL.md` has no `<owner>.<stem>` to read, so indexing it would invent an owner.

        It would then be reported twice - once as the body it is, and once as a file that
        "belongs in roles/design/", which is advice for a note and wrong for a body. The index
        declines it and `cmd_health._partition()` assertion 1 owns the report.

        Built in a scratch tree rather than asserted over the real corpus. This repo has no body
        in a role tree - that is the property under test - so the same assertion against `REPO`
        passes by having nothing to look at, which is the failure mode three tests here have
        already been rewritten for.
        """
        tmp = tempfile.mkdtemp(prefix="sw-kb-")
        try:
            skill = os.path.join(tmp, ".claude", "skills", "alpha")
            bucket = os.path.join(tmp, kb.ROLES_REL, "draft")
            os.makedirs(skill)
            os.makedirs(bucket)
            write(os.path.join(skill, "SKILL.md"), "---\nname: alpha\n---\n\n# alpha\n")
            write(os.path.join(bucket, "alpha.notes.md"),
                  "---\ntype: reference\nowner: alpha\n---\n\n# notes\n")
            write(os.path.join(bucket, "SKILL.md"), "---\nname: smuggled\n---\n\n# body\n")
            idx = kb.index(tmp, refresh=True)
            self.assertEqual([f.rel for f in idx.files],
                             ["%s/draft/alpha.notes.md" % kb.ROLES_REL])
        finally:
            shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    unittest.main()
