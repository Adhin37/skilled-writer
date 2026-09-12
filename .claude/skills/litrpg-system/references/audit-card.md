---
type: audit-card
owner: litrpg-system
dispatcher: revision-pass
pass: "10"
pass_kind: mechanical
description: Screen frequency, delta-only values, and numbers that decided nothing
when: optional.litrpg-system == on
---

# litrpg-system — audit card

Opened by `revision-pass` **Pass 10**, with the mechanics, when the module is on. Mostly
countable, which is why it sits late and cheap.

## The gate

> **Did a number decide anything?**

If the chapter's conflict resolved because one value exceeded another, the story has been replaced
by a scoreboard for a chapter. The repair is to make the choice the deciding factor and let the
number describe what the choice cost.

## Checks

- [ ] At most one block, and the chapter does not open on it
- [ ] No two blocks run consecutively (`sw lint` reports this as `meta-channel`)
- [ ] Changed values only — nothing unchanged was reprinted
- [ ] Every number in the block has a concrete meaning a reader could state in their own words
- [ ] The block matches `bible/lexicon.md` §Meta block format exactly, and uses `[…]`
- [ ] No system flattery, and no system commentary standing in for a character's reaction
- [ ] Any quest declined cost something — a quest with no cost to refuse is a to-do list
- [ ] Advancement that took repetition is compressed, unless something went wrong
- [ ] Any gain created a new problem, and is reconciled with `state/power.md`

## Where it fails most often

| symptom | what it actually is | go to |
|---|---|---|
| The block is where the chapter's emotion lives | the receipt is doing the scene's job | `scene-craft` — the level-up is not the beat |
| A full sheet appeared | those belong a few times per novel, after a real transition | `SKILL.md` §Formatting discipline |
| The system knows things nobody could | an unbounded oracle in brackets | `competence-map/references/broad-knowledge.md` — declare its shape and bound its access |
| Numbers rose and nothing about how problems get solved changed | a receipt, not progression | `power-scaling` |

## What it looks like when it lands

No block until the last page, and then three lines: the rank, and the recovery cost falling from
twelve hours to six. The climb was won by the rope she stole in chapter 4. The number describes
what it cost her, and decides nothing.
