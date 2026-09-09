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


# write-chapter step 1 and step 2: every skill whose decision is made from a card.
DRAFT_CARD_OWNERS = (
    "pov-switch", "scene-craft", "conflict-engine", "plot-threads",
    "character-development", "voice-separation", "character-profile", "mc-design",
    "timeline-engine", "world-texture", "mc-intel-meter", "story-opening",
    "power-scaling", "meta-knowledge", "competence-map", "hook-and-pacing",
    "narrator-voice", "dialogue-voice",
)


def description(skill):
    """The `description:` field of a skill, unwrapped to one line."""
    text = read(os.path.join(SKILLS, skill, "SKILL.md"))
    fm = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    if not fm:
        return ""
    m = re.search(r"(?ms)^description:\s*(.*?)(?=\n[a-z_]+:|\Z)", fm.group(1))
    return " ".join(m.group(1).split()) if m else ""


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
                text = read(os.path.join(refdir, f))
                if not re.search(r"(?i)open (this|it|the)|opened by", text[:900]):
                    thin.append("%s/references/%s" % (s, f))
        self.assertEqual(sorted(thin), [])

    def test_revision_pass_does_not_paraphrase_its_sources(self):
        """The dispatcher points at audit cards; it does not carry their checklists."""
        body = read(os.path.join(SKILLS, "revision-pass", "SKILL.md"))
        for skill in ("voice-separation", "competence-map", "bias-guard",
                      "world-texture", "prose-quality", "story-opening", "meta-knowledge"):
            self.assertIn("%s/references/audit-card.md" % skill, body,
                          "revision-pass must open %s's card" % skill)

    def test_write_chapter_does_not_paraphrase_its_sources(self):
        """The drafting dispatcher points at draft cards; it does not carry their content.

        The symmetric rule to the revision-pass one above. Step 1 used to cite sixteen skill
        bodies by section, which is ~34k tokens of procedure before a word of story state -
        the load benchmark run #1 measured the model rationing.
        """
        body = read(os.path.join(SKILLS, "write-chapter", "SKILL.md"))
        for skill in DRAFT_CARD_OWNERS:
            self.assertIn("%s/references/draft-card.md" % skill, body,
                          "write-chapter must open %s's draft card" % skill)

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
