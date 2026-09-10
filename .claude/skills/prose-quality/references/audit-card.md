# prose-quality — audit card

Opened by `revision-pass` **Pass 8**. `sw lint` finds the cut-list phrases, filter verbs, repeated
paragraph openings, runs of same-length sentences, phone-illegible paragraphs and the dialogue
share. It cannot hear rhythm, spot a named emotion, or feel a flat page, so those stay here.

- [ ] No phrase from the AI-default cut list
- [ ] Filter verbs removed
- [ ] Sentence and paragraph lengths visibly varied
- [ ] No paragraph opens with the same word as the one before it
- [ ] Emotions carried by behaviour or decision, not named
- [ ] No dead stage business
- [ ] **Dialogue share is 25–40% of the chapter's words** (`dialogue-voice` §How much dialogue).
      Measure it, do not eyeball it. One chapter under 10% is a warn; a five-chapter mean under
      10% fails the pass. The fix is to give the beats to the people in the room, never to bolt on
      small talk to clear a number
- [ ] Nobody was present in a scene, silent, while the POV character narrated their inner state
- [ ] **The dialogue sounds spoken** (`dialogue-voice` §How it sounds spoken). Somebody is
      interrupted or trails off; answers come in fragments; no character delivers their own
      reasoning in one unbroken multi-clause turn. `sw lint`'s texture line says where to look —
      it is a diagnostic, never a target

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
