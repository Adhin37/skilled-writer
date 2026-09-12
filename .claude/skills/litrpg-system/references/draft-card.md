---
type: draft-card
owner: litrpg-system
dispatcher: write-chapter
phase: A
order: 24
description: Whether a screen fires this chapter, and what it is allowed to decide
when: optional.litrpg-system == on
---

# litrpg-system — draft card

Opened by `write-chapter` Phase A when the module is on. The decision is usually **no**, and that
is the healthy answer: most chapters have no status block at all.

**Produce two lines for the brief:**

```
screen   one delta block, after the climb, three lines - Echo-step rank and its recovery cost
decides  nothing. The climb is won by the rope she stole in chapter 4
```

## The three decisions

1. **Does a block fire at all?** At most one per chapter. Never in the chapter's first lines —
   `hook-and-pacing` owns what an opening has to do, and a status block does none of it; in
   brackets it is a rank recital. Never two in a row, and never one standing in place of a scene.
2. **What does it show?** The delta only. An unchanged value is noise, and a reader who has
   learned to skip blocks will skip the one that mattered. Every number in it must have a concrete
   meaning the reader could state.
3. **What is it allowed to decide?** Nothing. Numbers describe capability; choices, plans and
   costs resolve the chapter. A conflict won because a stat was higher is a conflict the reader
   could have skipped.

## While drafting

- The block is the meta channel, `[…]`, in the exact shape `bible/lexicon.md` §Meta block format
  holds. Inline `[Echo-step]` for a name; the block form for a delta worth stopping on.
- **A notification is an interruption and it costs.** A screen mid-fight is attention the
  character does not have — pressure, never a reward chime.
- **No system flattery.** The system does not congratulate anyone, and it never stands in for the
  character's own reaction.
- **The system's categories are not the truth.** The gap between what it measures and what is
  actually happening is free story, and this chapter can widen it.
- **Grinding is a sentence**, not a scene, unless something goes wrong.
- A level is not a second ladder: `power-scaling` owns the mapping to `state/power.md` §2 and
  whether today's advance counts as a gain.

If a decision will not settle, open `litrpg-system/SKILL.md` §Narrative rules.
