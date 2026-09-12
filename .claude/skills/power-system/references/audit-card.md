---
type: audit-card
owner: power-system
dispatcher: revision-pass
pass: "5"
pass_kind: judgement
description: The power beat - cost on the page, nothing resolved by an unseen capability
when: genre in [fantasy, progression, scifi] or subgenre in [fantasy, progression, scifi]
---

# power-system — audit card

Opened by `revision-pass` **Pass 5**, alongside the world card, whenever the genre module is live.
Skip in one line if the chapter contains no use of a capability.

## The gate

> **Was anything in this chapter settled by a capability the reader had not seen used and seen
> fail?**

If yes, that is a deus ex machina however carefully the chapter foreshadowed it internally, and
the repair is structural: move the resolution to something established, or move the capability's
introduction three chapters earlier. Foreshadowing inside the chapter that needs it does not
count.

## Checks

- [ ] Every use paid its stated cost **in the same scene**, in the unit `bible/power-system.md`
      names — not reported afterwards, not owed to a later chapter
- [ ] The cost was legible to somebody: visible, audible, expensive, or noticed by a person
- [ ] A capability the reader already knows was not re-introduced at full length
- [ ] Its sensory signature matches every previous appearance
- [ ] No mechanics were explained during action
- [ ] No rank recital, and no character announced their own tier as a fact about the world
- [ ] Nothing a weaker character does was made impossible by tier alone — the counter still exists
- [ ] Any permanent gain has its row in `state/power.md` §4 and satisfies `power-scaling`

## Where it fails most often

| symptom | what it actually is | go to |
|---|---|---|
| The cost is fatigue and the next chapter opens rested | the system has no real economy | `SKILL.md` §The four hard rules — pick a cost that accumulates or that others can see |
| The fight turned on whose tier was higher | tier became the answer to conflicts | `power-scaling` — the gap is the story, the magnitude is not |
| A rule was explained mid-scene so the win would parse | the rule arrived two chapters late | `world-texture` — deliver it as a consequence, earlier |
| The gain solved problems and created none | the escalation axis has slipped onto numbers | `SKILL.md` §Progression without creep |
