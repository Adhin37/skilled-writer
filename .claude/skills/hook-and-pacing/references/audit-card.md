---
type: audit-card
owner: hook-and-pacing
dispatcher: revision-pass
pass: "9"
pass_kind: distributional
description: The opening earns the second sentence, the hook is not a summary
when: always
---

# hook-and-pacing — audit card

Opened by `revision-pass` **Pass 9**. Two sentences carry most of a serial chapter's retention —
its first and its last — and both of their defects are distributional: fine once, fatal at
density. Read this chapter's against the previous five, not on its own.

## The two gates

> **Does the first sentence earn the second?**

Not by being clever. By putting the reader somewhere, with somebody, mid-action. Re-anchoring is
**one clause**, not a paragraph of recap — and a chapter that opens on weather, a date stamp, a
status block or a character waking up has spent its strongest position on nothing.

> **Could a reader predict the next chapter from this one's ending?**

If yes, the hook is a summary wearing a question mark. A hook asks something the chapter did not
answer, in concrete terms, in final position.

## Checks

- [ ] The opening uses no banned pattern, and re-anchors in one clause
- [ ] The chapter ends on its last strong beat — not on the paragraph after it
- [ ] The hook is concrete and sits in the final sentence or paragraph
- [ ] Its **type** differs from the previous two chapters, and no type has run more than twice in
      the last five
- [ ] No cliffhanger if one fired within the last eight chapters
- [ ] Pace varies **within** the chapter — long stretches and short ones, not one tempo
- [ ] The chapter's `temp` matches the plan row, and is not the third identical one running
- [ ] Nothing was padded and nothing trimmed to reach a number. If the chapter is far outside
      `chapters.length_band`, that was a decision, recorded once and not scored

## Where it fails most often

| symptom | what it actually is | go to |
|---|---|---|
| Every chapter closes on a withheld beat | one hook shape doing the whole book | `references/arc-rhythm.md` — rotate the type, not the intensity |
| Every chapter closes on an ironic line | the register never changes | `prose-quality` §Range before polish |
| The opening summarises the last chapter | recap where the anchor should be | one clause, then move |
| The hook is strong and the chapter delivered nothing | the hook is doing the chapter's job | Pass Z, and `scene-craft`'s card |
