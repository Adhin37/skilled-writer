---
type: audit-card
owner: narrator-voice
dispatcher: revision-pass
pass: "10"
pass_kind: mechanical
description: Whether free indirect carries the interiority, and every surviving thought mark sits at a decision
when: always
---

# narrator-voice — audit card

Opened by `revision-pass` Pass 10. The four channels, checked against a drafted chapter.

`CLAUDE.md` hard rule 7 is this skill's to enforce, so the checklist lives here rather than in
`revision-pass`: the marks themselves come from `channels:` in `novel.md`, and `sw lint` reads
them from there too.

---

**`sw lint` settles the mechanical half outright** and quotes every hit: `thought-budget`,
`channel-collision`, `meta-channel`, `markup`. Apostrophes mistaken for thought marks, nested
quotations, italics, stray markup, meta blocks in the wrong place — all of it is found by reading
nothing. Work the findings; do not re-check them here.

Three judgements are left, and they are the whole pass:

- [ ] Free indirect discourse is carrying the interiority, **unmarked**. A chapter where every
      interior beat wears quote marks has flattened its narrator into a thought bubble, and a
      clean parse at nine thoughts is still a failure — the budget is the feature, because a
      marked thought is emphatic only while it is rare
- [ ] Each `'…'` that survived is at a **decision**, and is the sentence that character would
      actually say to themselves
- [ ] No marked thought is tagged *he thought* — the mark already said it

If a box fails, the repair is at the line rather than in another file. Strip the marks and let the
sentence keep running inside the narration, in that character's idiom. An interior beat belongs at
a moment of choice, so the one that survives is the one where something is decided, and the rest
go unmarked.

## What it looks like when it lands

*She wasn't going to ask again. That was the part she would have had trouble explaining.* Free
indirect, unmarked, in her rhythm — and the chapter's single `'…'` is four pages later, at the
moment she decides to lie.
