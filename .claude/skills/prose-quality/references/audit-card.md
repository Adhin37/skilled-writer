---
type: audit-card
owner: prose-quality
dispatcher: revision-pass
pass: "8"
pass_kind: judgement
description: Prose + microtension
when: always
---

# prose-quality — audit card

Opened by `revision-pass` **Pass 8**. `sw lint` finds the cut-list phrases, filter verbs, repeated
paragraph openings, runs of same-length sentences, phone-illegible paragraphs and the dialogue
share. It cannot hear rhythm, spot a named emotion, or feel a flat page, so those stay here.

**Work `sw lint`'s findings first** — cut-list phrases, filter verbs, same-length runs, repeated
paragraph openings. It quotes each one with its line, so there is nothing to re-check by reading,
and this card does not repeat them as boxes. Decide each: the rules here are `stylistic`, and a
hit you keep on purpose costs the report nothing (§When to break these).

Then the three it cannot see:

- [ ] Emotions carried by behaviour or decision, not named
- [ ] No dead stage business — a gesture that identifies nobody and moves nothing
- [ ] Nobody was present in a scene, silent, while the POV character narrated their inner state

Everything about how the dialogue *sounds* is `dialogue-voice`'s card, already open at Pass 2.

**Microtension** — the measured failure mode of machine-written fiction is an even, untroubled
surface: flatter arousal curves and less tension than human prose, page by page, even when the
plot is eventful. Tension at this scale does not come from stakes. It comes from two feelings
that do not fit, inside one person, right now.

- [ ] Open the chapter at three points at random. Each one has something unresolved on the page —
      a want pulling against a fear, a courtesy over a grudge, a decision not yet made
- [ ] No stretch of more than a page where everyone present feels one simple thing
- [ ] Agreement scenes still carry friction: someone concedes and minds it, or wants something the
      agreement does not give them
- [ ] The narration is not reassuring the reader that things are fine

**Register** — opened by `revision-pass` Pass 8b. The failure Pass 7 and Pass 8 both miss: prose
with no bad sentences and no range. Benchmark run #2 passed every phrase check in this toolkit,
shipped five chapters `status: revised`, and read as machine-written from page one because every
sentence was loaded the same way and every scene closed on the same small ironic withholding.

- [ ] `sw lint` shows no `house-style` or `em-dash` warning — or, if it does, the **density** came
      down, rather than the phrases being swapped for synonyms
- [ ] **Some sentences are plain.** Find three that carry information and nothing else: no dash,
      no reversal, no irony, no lesson appended. If there are none, that is the finding
- [ ] At least one scene closes **flat** — on an action or a line of speech, with nothing added to
      tell the reader how to feel about it
- [ ] The chapter reads at its declared `temp`. A `loud` chapter that reads `quiet` was drafted in
      the narrator's default register instead of the chapter's
- [ ] No `"A beat."` and no other stage direction; nothing that belongs in a script
- [ ] Read the last line of every scene in a row. If they all land with the same small click, the
      pitch is flat — rewrite all but one
- [ ] Across chapters: `sw lint` reports no `closer-sameness`

If a box fails, open `SKILL.md` — §Range before polish for register, §Microtension for the tension
work, the positive standards for the rest. The seven measured tells and why they cluster are in
`ai-default-tells.md`.

## What it looks like when it lands

Three plain sentences, then one that turns: *The office was cold. Maro had the window open and no
intention of closing it. She sat where he pointed.* Nothing is loaded, nothing is ironic, and the
paragraph after it can afford to be.
