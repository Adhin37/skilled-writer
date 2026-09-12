"""Integrity of the skill corpus itself.

Skills cite each other by section — `voice-separation` §3 — because line numbers rot silently.
Section citations rot silently too when a section moves into `references/`, which is exactly what
the body/references split does to twenty of them at a time. This suite is the guard.

It reads only the repo, runs in milliseconds, and needs no novel.
"""

import os
import re
import unittest

from fixtures import REPO

SKILLS = os.path.join(REPO, ".claude", "skills")


def skill_names():
    return sorted(d for d in os.listdir(SKILLS)
                  if os.path.isdir(os.path.join(SKILLS, d)))


def read(path):
    with open(path, encoding="utf-8") as fh:
        return fh.read()


def all_docs():
    """Every markdown file that may carry a citation."""
    out = []
    for root, _dirs, files in os.walk(os.path.join(REPO, ".claude")):
        out += [os.path.join(root, f) for f in files if f.endswith(".md")]
    out.append(os.path.join(REPO, "CLAUDE.md"))
    out.append(os.path.join(REPO, "README.md"))
    return sorted(out)


# The card set is DERIVED, never listed. A hand-typed roster of owners is a second copy of the
# corpus, which is the defect class this repo exists to remove - and it drifts the moment two
# cards merge, which the card budget now forces them to do. The tests below assert the
# *properties* a card set must have instead: every card is dispatched, every module has one, and
# nothing unconditional exceeds the budget.


def description(skill):
    """The `description:` field of a skill, unwrapped to one line."""
    text = read(os.path.join(SKILLS, skill, "SKILL.md"))
    fm = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    if not fm:
        return ""
    m = re.search(r"(?ms)^description:\s*(.*?)(?=\n[a-z_]+:|\Z)", fm.group(1))
    return " ".join(m.group(1).split()) if m else ""


def body(path):
    """A file with its YAML frontmatter removed.

    The knowledge-base layer puts frontmatter on every reference, and several checks here scan
    a fixed prefix of the file. Scanning the raw text would measure the frontmatter instead of
    the prose it sits above.
    """
    text = read(path)
    m = re.match(r"^---\n.*?\n---\n", text, re.S)
    return text[m.end():] if m else text


def headings(skill):
    text = read(os.path.join(SKILLS, skill, "SKILL.md"))
    nums, names = set(), set()
    for m in re.finditer(r"(?m)^#{2,3} (.+)$", text):
        head = m.group(1).strip()
        num = re.match(r"(\d+)\.", head)
        if num:
            nums.add(num.group(1))
        names.add(head.lower())
    return nums, names


class TestCitations(unittest.TestCase):

    def test_every_section_citation_resolves(self):
        names = skill_names()
        cache = {s: headings(s) for s in names}
        pattern = re.compile(r"`?(%s)`? §([0-9]+|[A-Z][A-Za-z' -]*)" % "|".join(names))
        broken = []
        for path in all_docs():
            for m in pattern.finditer(read(path)):
                skill, ref = m.group(1), m.group(2).strip().rstrip(" -")
                nums, heads = cache[skill]
                if ref.isdigit():
                    ok = ref in nums
                else:
                    ok = any(h.startswith(ref.lower()) or ref.lower().startswith(h)
                             for h in heads)
                if not ok:
                    broken.append("%s -> %s §%s"
                                  % (os.path.relpath(path, REPO), skill, ref))
        self.assertEqual(sorted(set(broken)), [],
                         "section citations pointing at a heading that no longer exists")

    def test_every_referenced_file_exists(self):
        missing = []
        pattern = re.compile(r"`((?:[a-z][a-z0-9-]*/)?references/[a-z0-9-]+\.md)`")
        for path in all_docs():
            skill_dir = os.path.dirname(path)
            if os.path.basename(skill_dir) == "references":
                skill_dir = os.path.dirname(skill_dir)
            for m in pattern.finditer(read(path)):
                target = m.group(1)
                if "/references/" in target and not target.startswith("references/"):
                    full = os.path.join(SKILLS, target)
                else:
                    full = os.path.join(skill_dir, target)
                if not os.path.isfile(full):
                    missing.append("%s -> %s" % (os.path.relpath(path, REPO), target))
        self.assertEqual(sorted(set(missing)), [], "pointers to reference files that do not exist")

    def test_every_named_skill_exists(self):
        names = set(skill_names())
        pattern = re.compile(r"`([a-z][a-z0-9]+(?:-[a-z0-9]+)+)`")
        # tokens that look like a skill name but are values, paths or filenames
        allowed = names | {"novel-init", "read-set", "kebab-case", "third-limited",
                           "third-omniscient", "third-objective", "episode-precise",
                           "major-beats", "fandom-corrupted", "no-harem", "self-insert",
                           "body-snatch", "point-of-no-return", "slow-burn", "weak-to-strong",
                           "check-chapters", "arc-level", "chapter-level", "novel-level",
                           "hand-habit", "tag-removal", "three-stroke", "cast-wide",
                           "front-page", "add-when-prominent", "best-alive"}
        unknown = set()
        for path in all_docs():
            for m in pattern.finditer(read(path)):
                tok = m.group(1)
                if tok in allowed or "." in tok or "/" in tok:
                    continue
                if tok.startswith("novel-") and os.path.isfile(
                        os.path.join(REPO, ".claude", "commands", tok + ".md")):
                    continue
                unknown.add(tok)
        # Only fail on tokens that are *almost* a skill name - a typo of a real one.
        typos = {t for t in unknown
                 if any(abs(len(t) - len(s)) <= 2 and t[:6] == s[:6] for s in names)}
        self.assertEqual(sorted(typos), [], "near-miss skill names - probably typos")


class TestArchitecture(unittest.TestCase):
    """CLAUDE.md section 8: procedure in the body, everything else in references/."""

    def test_no_skill_body_is_oversized(self):
        """A body over ~2,700 words is carrying something that belongs in references/."""
        fat = []
        for s in skill_names():
            words = len(read(os.path.join(SKILLS, s, "SKILL.md")).split())
            if words > 2700:
                fat.append("%s (%d words)" % (s, words))
        self.assertEqual(sorted(fat), [])

    def test_every_reference_states_its_trigger(self):
        """A pointer without a condition is not read, so every reference says when to open it."""
        thin = []
        for s in skill_names():
            refdir = os.path.join(SKILLS, s, "references")
            if not os.path.isdir(refdir):
                continue
            for f in sorted(os.listdir(refdir)):
                text = body(os.path.join(refdir, f))
                if not re.search(r"(?i)open (this|it|the)|opened by", text[:900]):
                    thin.append("%s/references/%s" % (s, f))
        self.assertEqual(sorted(thin), [])

    def test_revision_pass_does_not_paraphrase_its_sources(self):
        """The dispatcher points at audit cards; it does not carry their checklists."""
        body = read(os.path.join(SKILLS, "revision-pass", "SKILL.md"))
        for skill in ("voice-separation", "competence-map", "bias-guard",
                      "world-texture", "prose-quality", "story-opening", "meta-knowledge",
                      "story-craft"):
            self.assertIn("%s/references/audit-card.md" % skill, body,
                          "revision-pass must open %s's card" % skill)

    def test_every_module_is_reached_through_a_card(self):
        """A module the dispatcher can only reach as a whole SKILL.md is a module read wrong.

        All eleven optional and genre modules had zero cards. `revision-pass` step 0.2 resolved
        the active ones and said "open those", and what opened mid-draft was a 700-1,400 word
        body - a procedure for *designing* the thing, at the point where the run needed a
        decision. That is the exact split `docs/design-notes.md` describes, and the modules were
        the one corner of the corpus it had never reached.

        The rule this locks: every skill whose tier is `optional` or `genre` carries at least one
        card, and the card is what its dispatcher opens.
        """
        from swlib import kb
        idx = kb.index(REPO, refresh=True)
        carded = {f.owner for f in idx.by_type("draft-card")}
        carded |= {f.owner for f in idx.by_type("audit-card")}
        bare = sorted(name for name, skill in idx.skills.items()
                      if skill.tier in ("optional", "genre") and name not in carded)
        self.assertEqual(bare, [],
                         "modules with no card - the dispatcher would open the body instead")

    def test_unconditional_cards_stay_inside_the_budget(self):
        """The forcing function from `docs/creative-latitude.md`.

        The corpus reached nineteen draft cards and twenty-three audit cards for one chapter -
        16,359 words of instruction and 596 prohibitions before a line of story state - because
        adding a rule always meant adding a file and no number anywhere objected. Past the budget
        a new rule merges into the card that already owns its neighbourhood.

        Conditional cards are excluded: a module that fires for one novel in ten is not what
        makes the loop heavy. The unconditional set is, because every chapter of every book
        carries it.
        """
        from swlib import kb, rules
        idx = kb.index(REPO, refresh=True)
        for kind, cap in sorted(rules.CARD_BUDGET.items()):
            live = [f.owner for f in idx.by_type(kind)
                    if not f.when or f.when.strip() == "always"]
            self.assertLessEqual(len(live), cap,
                                 "%d unconditional %ss against a budget of %d: %s"
                                 % (len(live), kind, cap, ", ".join(sorted(live))))

    def test_pass_sections_count_their_cards_correctly(self):
        """A pass that says "four cards" when three resolve sends the reviewer to a missing file.

        Benchmark run #2's D4 was `revision-pass` naming a card that did not exist, and it
        recurred: the `timeline-engine` audit card was merged into `plot-threads`' and Pass 4 went
        on saying "Four cards, one per owner ... and `timeline-engine`". `sw health` catches the
        path form of that pointer; this catches the arity claim, which is how the prose form
        shows. Conditional module cards are excluded - a pass names what every novel opens.
        """
        from swlib import kb
        idx = kb.index(REPO, refresh=True)

        unconditional = {}
        for f in idx.by_type("audit-card"):
            if f.when and f.when.strip() != "always":
                continue
            for one in str(f.pass_ or "").split(","):
                unconditional.setdefault(one.strip(), set()).add(f.owner)

        words = {"one": 1, "two": 2, "three": 3, "four": 4, "five": 5, "six": 6}
        claim = re.compile(r"\b(one|two|three|four|five|six)\b[^.\n]{0,40}?\bcards\b", re.I)
        body = read(os.path.join(SKILLS, "revision-pass", "SKILL.md"))

        sections = re.split(r"^## Pass ", body, flags=re.M)[1:]
        checked = 0
        for section in sections:
            label = section.split(None, 1)[0].strip()
            if label not in unconditional:
                continue
            for word in claim.findall(section):
                checked += 1
                self.assertEqual(
                    words[word.lower()], len(unconditional[label]),
                    "Pass %s says %r cards but %d unconditional audit card(s) declare "
                    "`pass: %s`: %s"
                    % (label, word, len(unconditional[label]), label,
                       ", ".join(sorted(unconditional[label]))))
        self.assertTrue(checked, "no pass section stated a card count - the guard is inert")

    def test_every_audit_card_declares_a_pass(self):
        """A card `revision-pass` cannot place is a card that never runs."""
        from swlib import kb
        idx = kb.index(REPO, refresh=True)
        for f in idx.by_type("audit-card"):
            self.assertTrue(f.pass_, "%s declares no `pass:`" % f.rel)
            self.assertEqual(f.dispatcher, "revision-pass", f.rel)

    def test_write_chapter_dispatches_every_draft_card(self):
        """The drafting dispatcher reaches every card; it does not carry their content.

        This used to assert that `write-chapter/SKILL.md` contained each card's path as literal
        text. That proved only that a copy of the list lived there, and the copy was what the
        knowledge-base layer removed: the dispatcher now points at the read-set's CARDS block,
        which `swlib/kb.py` resolves from each card's own frontmatter. The rule is unchanged -
        the dispatcher must reach every card - so the test asserts it of the resolver instead.

        The symmetric rule to the revision-pass one above. Step 1 used to cite sixteen skill
        bodies by section, which is ~34k tokens of procedure before a word of story state -
        the load benchmark run #1 measured the model rationing.
        """
        from swlib import kb
        idx = kb.index(REPO, refresh=True)
        cards = idx.by_type("draft-card")
        self.assertTrue(cards, "the corpus has no draft cards at all")
        for f in cards:
            self.assertEqual(f.dispatcher, "write-chapter", f.rel)
            self.assertIn(f.phase, ("A", "B"), "%s declares no drafting phase" % f.rel)
            self.assertTrue(f.owner in idx.skills, "%s has no owning skill" % f.rel)

        body = read(os.path.join(SKILLS, "write-chapter", "SKILL.md"))
        self.assertIn("CARDS", body,
                      "write-chapter must point at the read-set's resolved card block")

    def test_every_draft_card_has_an_owner_that_exists(self):
        for s in skill_names():
            card = os.path.join(SKILLS, s, "references", "draft-card.md")
            if os.path.isfile(card):
                self.assertIn("write-chapter", read(card),
                              "%s's draft card should name the step that opens it" % s)

    def test_no_description_is_oversized(self):
        """A description routes; it does not teach.

        Every one of these sits in context for the whole session whether or not the skill is
        ever loaded, so the ceiling is the point. The teaching half belongs in the body.
        """
        fat = []
        for s in skill_names():
            desc = description(s)
            if len(desc) > 200:
                fat.append("%s (%d chars)" % (s, len(desc)))
        self.assertEqual(sorted(fat), [])

    def test_frontmatter_puts_description_before_metadata(self):
        """`description()` above terminates on the next column-0 `key:`.

        `metadata:` is column-0 and ends it correctly, but the keys nested under it are indented
        and do not. So a file that put `metadata:` first would have its description swallow the
        whole block, and the 200-char ceiling check below would silently start measuring YAML.
        """
        wrong = []
        for s in skill_names():
            text = read(os.path.join(SKILLS, s, "SKILL.md"))
            fm = re.match(r"^---\n(.*?)\n---\n", text, re.S)
            if not fm:
                continue
            keys = re.findall(r"(?m)^([a-z_]+):", fm.group(1))
            if "metadata" in keys and "description" in keys:
                if keys.index("description") > keys.index("metadata"):
                    wrong.append(s)
        self.assertEqual(sorted(wrong), [],
                         "`description:` must come before `metadata:` in SKILL.md frontmatter")

    def test_every_description_states_a_trigger(self):
        """The half that decides whether the skill loads at all, so the diet may not cut it."""
        thin = [s for s in skill_names()
                if not re.search(r"(?:\A|\.\s)Use\b", description(s))]
        self.assertEqual(sorted(thin), [], "descriptions with no 'Use ...' routing trigger")

    def test_every_audit_card_has_an_owner_that_exists(self):
        for s in skill_names():
            card = os.path.join(SKILLS, s, "references", "audit-card.md")
            if os.path.isfile(card):
                self.assertIn("revision-pass", read(card),
                              "%s's audit card should name the pass that opens it" % s)


if __name__ == "__main__":
    unittest.main()
