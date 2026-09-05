---
name: revision-pass
description: Quality gate for a drafted chapter — runs continuity, character, intelligence, bias, MTL-artifact and prose checks in a fixed order and fixes what it finds. Use after drafting any chapter, and when the user says /novel-revise.
---

# revision-pass

A chapter is not finished when it is drafted. This is the gate. Run the passes **in this order** —
structural fixes invalidate line edits, so line editing goes last.

Keep it mechanical. Each pass is a search-and-decide, not a re-read of the whole novel.

---

## Pass 1 — Continuity (structural)

Against the read-set from `continuity-summary`.

- [ ] No contradiction with the last five CCS blocks
- [ ] No character knows something their `kno>` history does not support
- [ ] Names, terms, titles and spellings match `bible/lexicon.md` exactly
- [ ] In-world time is consistent with `state/timeline.md`; travel times plausible
- [ ] Objects, injuries and possessions persist (the coat, the scar, the debt)
- [ ] Nothing contradicts an established rule in `bible/world.md` or `bible/power-system.md`
- [ ] Character positions match where the last chapter left them

**Form check** — only if any character in the chapter has `form_locked: true`. Read
`state/body.md` §1–§2 and verify against every sentence describing them:

- [ ] Every physical description matches the CURRENT FORM row — nothing from a later stage
- [ ] No capability exceeded the stage's absolute limits (reach, strength, stamina, voice)
- [ ] Others reacted to the body, not to the mind inside it
- [ ] Any adult diction from a child's body was noticed by someone, or deliberately masked
- [ ] A stage transition, if one fired, is logged in §4 with what it enables and what it costs

## Pass 2 — Character

- [ ] Every named speaker matches their behaviour rules, or breaks one *as an event*
- [ ] Voice deltas from `state/growth.md` are applied
- [ ] Tag-removal test: speakers identifiable without attributions
- [ ] No character acted out of character for the plot's convenience
- [ ] Any rung advance was triggered, dramatised, and is audible in dialogue
- [ ] Antagonists present want something and are competent at something

**Walk-ons** — for every minor character in the chapter:

- [ ] Swap test: their scene could not be handed to a different extra unchanged
- [ ] Three strokes present — a want inside the scene, one habit, one piece of their working world
- [ ] No interiority, no backstory paragraph, no arc granted to a tier-C character
- [ ] Nobody was over-characterised on the way to dying; a death this chapter was set up earlier
- [ ] Anyone at a third appearance, or who changed the plot, is promoted and profiled
- [ ] Every named walk-on has a roster line and a lexicon entry

## Pass 3 — MC intelligence (`mc-intel-meter`)

- [ ] Every MC decision passes the trace test — name the on-page fact behind it
- [ ] None of the seven floor rules violated
- [ ] Any MC failure uses missing information, opposed will, cost, or an established blind spot
- [ ] No narration asserting the MC is clever
- [ ] Nobody was made stupid to make the MC look smart
- [ ] Tier-appropriate: no deduction above tier, no obtuseness below it

## Pass 4 — Structure

- [ ] Every scene has goal / obstacle / turn / cost
- [ ] No scene exits on a plain yes
- [ ] The chapter's cost is stateable in one concrete sentence
- [ ] At least two of the four conflict sources active
- [ ] Thread ops match the plan row; the ledger will be updated
- [ ] The `wld>` line is filled: the world did something offstage this chapter
- [ ] Any world-track event that fired is logged in the divergence ledger, with what it opened
- [ ] Crisis count is within `timeline.crisis_cap`; nothing here took an `ending.non_negotiable`
- [ ] Skim test: name the one thing a reader would miss if they skipped this chapter

## Pass 5 — Bias (`bias-guard`) — never skipped, never negotiable

- [ ] No group treated as uniformly anything by the narration
- [ ] Every named woman in the chapter wants something that is not the MC
- [ ] No character introduced by a body inventory
- [ ] No physical trait or accent signalling moral quality
- [ ] Nobody is a reward
- [ ] Any prejudice on the page belongs to a character and costs someone something

## Pass 6 — MTL detox (`mtl-detox`)

- [ ] Zero banned phrases
- [ ] Zero exclamation marks in narration
- [ ] No crowd-reaction block
- [ ] No rank recital or system lecture
- [ ] No face-slap loop; every confrontation cost the winner something
- [ ] No paragraph saying the same thing three ways

## Pass 7 — Prose (`prose-quality`)

- [ ] No phrase from the AI-default cut list
- [ ] Filter verbs removed
- [ ] Sentence and paragraph lengths visibly varied
- [ ] No paragraph opens with the same word as the one before it
- [ ] Emotions carried by behaviour or decision, not named
- [ ] One non-visual sensory detail per scene
- [ ] No dead stage business

## Pass 8 — Opening and hook (`hook-and-pacing`)

- [ ] Opening avoids the banned patterns
- [ ] Re-anchoring is one clause
- [ ] Chapter ends on its last strong beat
- [ ] Hook concrete, final position, type rotated
- [ ] Word count inside range without padding

## Pass 9 — Mechanics

- [ ] Frontmatter complete and accurate; word count real (`wc -w`)
- [ ] Scene breaks use `* * *`
- [ ] POV label present if the chapter switches and `label_switches` is true
- [ ] No headings, author notes or stray markdown inside the prose body
- [ ] Dialogue punctuation and house style per `lexicon.md`

---

## Fixing

- **Fix in the file.** Do not report a defect and leave it.
- **Structural defects can require a rewrite of a scene.** Do it. A chapter with no cost or no
  turn cannot be repaired at the sentence level.
- **When a fix contradicts the plan**, change the plan row and re-check the next three rows.
- **When a fix reveals a bible gap** (an unnamed thing, an undefined rule), add it to `bible/` in
  the same pass and say so.

Set `status: revised` in the frontmatter when all nine passes are clean.

## Reporting

Two lines, unless something structural was rewritten:

```
Revised ch 42: cut a crowd-reaction paragraph, applied Dael's rung-3 voice delta,
replaced the ending (it ran three paragraphs past the hook). 1,840 → 1,795 w.
```

If a pass found nothing, do not list it. If Pass 5 found something, always say what — the user
needs to know that the default was reaching for it.

## Standalone use

`/novel-revise <n>` runs this on an existing chapter. Load that chapter, its CCS block, the two
before it, and the profiles of everyone in it — then run all nine passes.
