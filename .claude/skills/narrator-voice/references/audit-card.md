---
type: audit-card
owner: narrator-voice
dispatcher: revision-pass
pass: "10"
pass_kind: mechanical
description: Mechanics
when: always
---

# narrator-voice — audit card

Opened by `revision-pass` Pass 10. The four channels, checked against a drafted chapter.

`CLAUDE.md` hard rule 7 is this skill's to enforce, so the checklist lives here rather than in
`revision-pass`: the marks themselves come from `channels:` in `novel.md`, and `sw lint` reads
them from there too.

---

- [ ] Speech, direct thought and meta each sit in their declared marks; free indirect discourse is
      **unmarked**, and is where interiority actually lives
- [ ] Direct thought is **budgeted — 1–3 per chapter**, at decisions. A chapter where every
      interior beat wears quote marks has flattened its narrator into a thought bubble; convert
      the surplus back to free indirect discourse
- [ ] **No apostrophe was mistaken for a thought mark.** `don't`, `she'd`, `the boys' room` are
      not thought. Every thought opens at a word boundary and closes before punctuation or space
- [ ] No marked thought is tagged *he thought* — the mark already said it
- [ ] Every thought mark **inside** a speech span is an ordinary nested quotation
- [ ] Meta blocks match the format in `lexicon.md`; none opens a chapter; no two run consecutively
- [ ] No italics anywhere in the prose body, in either spelling (`*x*`, `_x_`)
- [ ] Nothing else is markup — no headings, bold, lists, links or author notes in a prose body

`sw lint` reports the countable half of this: `thought-budget`, `channel-collision`,
`meta-channel` and `markup`. The budget is the feature — a marked thought is emphatic *because*
it is rare, so a clean parse at nine thoughts per chapter is still a failure.

If a box fails, open `SKILL.md` §The four channels, and `references/draft-card.md` for the
distance and interiority settings that decide where a thought should have been unmarked.
