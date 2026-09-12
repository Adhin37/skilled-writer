---
name: slice-of-life-texture
description: Optional (default off). Add downtime, work, food and routine so the world feels inhabited and high-stakes chapters have something to threaten. Use only while this skill is enabled.
metadata:
  type: skill
  tier: optional
  force: stylistic
  when: optional.slice-of-life-texture == on
  owns: [downtime]
---

# slice-of-life-texture

**Gate.** Applies only if `novel.md` → `optional.slice-of-life-texture` is `on`.

**Relation to the always-on world skills.** `world-texture` runs in every novel and governs how
much of the world may reach the page at all — its budget still binds here. This skill deepens one
band of that work: the household layer, expanded from an occasional detail into a deliberate
recurring channel. The domestic facts it uses come from `bible/society.md` (`social-fabric`) —
what things cost, who does which work, what a family does on the days that matter — so that
downtime is specific to *this* world rather than generically cosy.

Constant peril numbs. Texture is what the danger is *for*: a reader can only fear the loss of a
life they have seen someone living.

---

## What texture is

Not description. **Ordinary competence, ordinary obligation, ordinary pleasure**, shown while
something else is happening.

| channel | example |
|---|---|
| Work | how a character actually earns; the part of it they are good at; the part they hate |
| Food | who cooks, what it costs, what it means when someone makes the good thing |
| Money | rent, debts, the price of the boots. Specific numbers, consistently |
| Repair | mending, cleaning, maintaining. What a person's hands do at rest |
| Weather & season | affecting plans and moods, not opening chapters |
| Sleep | where, how badly, next to whom |
| Small rituals | the order they do things in; what they always do before leaving |
| Idle talk | conversation that is not about the plot, between people who like each other |

## Rules

**Texture rides along; it does not stop the story.** Put it inside a scene with a goal. The
argument happens over the mending; the confession happens while the stew burns. A chapter that is
*only* texture is a chapter readers skip, and in a serial that habit spreads.

**Budget: one or two beats per chapter**, unless the novel is deliberately slow-paced. A full
downtime chapter earns its place once per arc — after a heavy loss, or immediately before the
climax, where it functions as dread.

**Specificity or nothing.** "They ate dinner" is not texture. "She ate standing up because the
chair was still broken" is character, economics and mood in nine words.

**It must be threatenable.** Every domestic detail you establish is something the plot can take.
This is the mechanism: texture converts abstract stakes into concrete ones. The reader who has
watched someone repair that roof will feel it burn.

**Ordinary competence is characterisation.** What a person is good at when nothing is at stake
tells the reader more than any fight.

**Recurring texture builds a home.** The same tea, the same walk, the same argument. Repetition
is how a place becomes real — and how its absence, later, registers.

## Interaction with pacing

Use texture as the `cool` stretch of the arc rhythm (`chapter-plan`) — but a cool chapter still
has a goal, a turn and a cost. The texture is the *medium*; the scene structure is unchanged.

Strongest placements:
- Immediately after an arc climax, while the cost is still being absorbed
- Immediately before a known danger, so the reader is counting what is at risk
- During a journey, where routine is the only structure available


## When to break these — `force: stylistic`

The budget and the placements are **defaults, not gates**.

Break them when the texture *is* the chapter: a festival, a meal that is a negotiation, a day of
work where the work is what changes. A whole downtime chapter is allowed more often than the
once-an-arc guidance says when the novel's cadence is genuinely slow and the user asked for that —
`chapters.arc_length` and `style.read_like` are better evidence than this budget.

The requirement that does not bend is the one the budget exists to serve: **the scene still has a
goal and a turn.** Texture rides inside a scene; a chapter with neither is a chapter readers skip,
and in a serial that habit spreads to the next one.

## Self-check

- [ ] Every texture beat sits inside a scene with a goal
- [ ] Details are specific enough to be threatened later
- [ ] No more than two beats this chapter, unless it is the arc's downtime chapter
- [ ] At least one thing shown that a character is quietly good at
- [ ] Nothing has stopped the story to describe a room
