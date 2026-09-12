---
type: draft-card
owner: fanfic-canon
dispatcher: write-chapter
phase: A
order: 21
description: Which canon fact this chapter touches, and whether the divergence explains it
when: genre in [fanfic] or subgenre in [fanfic]
---

# fanfic-canon — draft card

Opened by `write-chapter` Phase A in fan fiction. Decides this chapter's contact with the source.

**Produce two lines for the brief:**

```
canon    Academy intake runs on schedule - it is not touched by the divergence
ooc      none. Every canon character behaves as the source depicts them
```

## The four decisions

1. **Which canon facts does this chapter stand on?** Name them. Anything outside
   `fanfic.canon_scope` is not canon and not a contradiction — it is simply not in play.
2. **Does the divergence reach here?** If a canon event still happens in this chapter, say *why*
   it still happens given the change, and record the answer. If it does not happen, the reason is
   traceable to the change, never to convenience.
3. **Is any canon character acting against the source?** Every departure is spent from
   `fanfic.ooc_budget` and logged with its in-story justification. Derive their behaviour from
   what the source depicts them doing, not from what the scene needs.
4. **What does nobody know?** A canon character does not know the parts of canon they were not
   present for, and nobody but the MC knows the future. This is the boundary fandom erases
   fastest; `competence-map` owns the general rule and this is its sharpest case.

## In the opening arc — chapters 1 to 5

**Count the canon nouns before drafting, not after.** The setting's name, the central power, the
factions, the canon characters. Zero across a chapter is a bug: a reader who arrived from a blurb
naming a canon character has had no contact with the promise.

The cheapest placement is **age as a calendar** — a character the audience knows, at an age they
can compute, doing something ordinary. One sentence, and the reader knows exactly when they are.

## While drafting

- **Original prose only.** No dialogue, narration or lyrics reproduced from the source, anywhere.
  A re-staged canon scene is written fresh, from a new angle, or it is not a chapter.
- Canon characters go on the voice matrix like anyone else, derived from how they actually speak
  in the source (`voice-separation`).
- The canon plot is a live track with its own clock — `timeline-engine` owns what it does this
  chapter whether or not the MC is looking.

If a decision will not settle, open `references/canon-handling.md`.
