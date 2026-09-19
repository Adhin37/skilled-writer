# Reader review — worked example

Run #5, cold read, 2026-09-19. The output shape of [`reader-review.md`](reader-review.md), filled
in, on `novels/grain-beneath-the-lie`.

**This file is split out of the procedure deliberately.** It carries a verdict, a ranked finding
list and a divergence note, and a reader who sees those before opening the chapters will find them
again — which is exactly the contamination the blind pass exists to prevent. The procedure itself
is now safe to hand to a reader whole. This file is not. Read it when you are learning the method
or writing a run up, never while performing one.

---

## The read
Five chapters, ~7,700 words, `novels/grain-beneath-the-lie`. Abridged to show the output shape.
The full text is in [`benchmark.md`](benchmark.md).

**R1 — the story.** *"A forensic examiner suspects the evidence in a murder case was faked."* That
is where the sentence stops after five chapters. No suspect, no theory, no move made. The finding
is that R1 could not be answered, which is itself the headline.

**R2 — next chapter?** Yes, on the strength of the premise. Not on the strength of anything that
has happened.

**R3 — scene table.** Five chapters, five two-person conversations: Ada/exam room · Ilona/alcove ·
Ada/bench · Verrick/office · Mira/flat. No crowd, no street, no tempo break. Nothing is loud, so
the quiet has nothing to be quiet against.

**R4 — the repeated move.** *"That's not an answer"* — four times, three chapters, two mouths.
Plus every one of five scenes closing on the same ironic withholding. Plus 235 negative
constructions in 7,700 words.

**R5 — characters.** Halden is a person. Ada has one note; Verrick is a job title; Thales is told
to be unreadable four separate times, which is furniture with a label on it.

**R6 — pricing the threat.** Calderford, the Silt, Founding Row, the Compact, the Bench — forty
proper nouns and no prices. What re-graining costs and why it is believed impossible never arrive,
so when the MC says the floor under his life is not solid, the reader takes his word for it.

**R7 — the biggest thing.** Offstage, six years ago, delivered as a mother's dinner-table
monologue.

**Positive control.** Chapter 3's control experiment — the MC tests the phenomenon on a worthless
training blank to rule out the mundane explanation — is real mystery craft and the best beat in the
book. *"Eleven-nineteen answered twice. This did it once, the way every clean thing is supposed
to."*

**Phase 2.** The world: *not invented* for the prices, *not on the page* for what `bible/world.md`
did hold. Two different fixes, and the blind pass is what separated them.

**Phase 3.** **3 / 5** — would read chapter 6; would stop by chapter 10. Ranked: no story underway
· one temperature · the repeated move · cast as functions · world unpriced · climax monologued.
Three changes: a suspect or a theory by chapter 3 · one scene with more than two people in it ·
put the condemned man on the page as a person before his clock runs out.

**Phase 4 — what the instruments said.** This is the column that justifies the exercise:

| finding | toolkit |
|---|---|
| no story underway | **nothing.** Every chapter carried a valid `event:`, Pass Z passed five times, `sw audit` returned 0 defects |
| five two-handers | **nothing.** `group-scene` is a situation note, excluded from the WATCH row; its inverse is unmeasured |
| repeated line across mouths | **nothing.** `echo` is within-chapter only |
| negation density | **nothing** |
| world unpriced | **nothing** — by construction: every tool reads `bible/`, so no tool can miss what never left it |
| cast as functions | **partial.** `arc-cast` warned *only one matrix character appears in the whole arc* — rotation, not depth |
| climax monologued | **partial.** Four `texture` notes on 45+ word turns caught the symptom |

Five findings with **no owner**. That is the run's most useful output and no other instrument in
the repo could have produced it.

**§5 divergence.** In-run: *"the prose is good and the dialogue is the best any run has produced."*
Cold read: 3 / 5. Both recorded. Neither reconciled.
