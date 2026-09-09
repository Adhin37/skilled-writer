# Spoken register — the measured failure, and the repair

Open this when `sw lint`'s dialogue-texture line looks wrong, when a scene reads as stiff, or when
you are deciding whether a turn is too long for the character speaking it.

## What it looked like when it failed

Benchmark run #2 shipped five chapters at 25% dialogue share — comfortably inside target — that
the first human to read them described as "not people speaking normally … stiff and awkward". The
texture measurements afterwards:

| ch | lines | mean words | contractions/100 | fragments | cut off | longest exchange | narration between |
|---|---|---|---|---|---|---|---|
| 1 | 43 | 10.6 | 9.9 | 16% | **0** | 13 | 28 |
| 2 | 14 | 10.2 | 7.7 | 43% | **0** | 3 | **88** |
| 3 | 24 | 11.6 | 7.9 | 25% | **0** | 7 | 38 |
| 4 | 20 | 15.3 | **3.6** | 30% | **0** | 4 | 28 |
| 5 | 13 | **23.4** | 7.2 | 38% | **0** | 3 | 40 |

**Zero interruptions in 114 spoken lines.** Nobody in the book was ever cut off or trailed away.
Chapter 5 averaged 23 words a turn — people making speeches. Chapter 2 put 88 words of narration
between one line and the next.

Share could not see any of it, and neither could `voice-separation`, `character-profile` or
`revision-pass`, because all of them ask what a line *is* and none asks how it *sounds*.

## The repair that worked

The revising agent diagnosed the deepest version itself: the POV character's prose had stopped
obeying her own matrix row. Declared `artic 3` and `heat: banked` — shorter and more precise under
pressure — and in the two highest-pressure scenes in the arc her turns ballooned into hedge-stacked
monologues. That is `artic 4/5` fluency wearing an `artic 3` label.

| instead of | write |
|---|---|
| one turn carrying the whole reasoning | a short statement, a beat of business, then the honest part |
| every line reaching a full stop | an answer of two words, and one that stops early |
| a line, three paragraphs of analysis, a line | a run of lines where two people actually talk |
| a fact delivered in someone's mouth | the fact as a consequence somebody runs into |
| everyone allowed to finish | somebody cutting in, somebody answering the question they wish had been asked |

Repairing this moved chapter 5 from a 23.4-word mean to 12.7, and its spread from 26.9 to 6.9.

## The trap

The same repair **lowered dialogue share** — trimming speeches shortens lines without adding new
ones — so chapters that had been inside the 25–40% band fell under it. Two measurements of the
same subsystem moved in opposite directions, and the repair a reader actually wanted is the one
that made the older metric look worse.

This is the whole argument for keeping texture as notes rather than gates. If either number
decided whether a chapter shipped, the fix for one would be a defect against the other, and the
model would be forced to pick the metric over the reader.

## Why a cast goes quiet

**The diagnostic.** A POV character with a strong analytical voice is the usual cause: the model
routes every beat through their reasoning because that voice is enjoyable to write. The tell is a
scene where a second person is physically present and says nothing, or says one line and is
narrated *about* for three paragraphs. Whenever another character is in the room, ask what they
would say — and let them say it instead of having the POV character infer it.

**Interiority is not a substitute for a scene.** If the POV character concludes something about
another person, the stronger version is almost always that the other person does or says the thing
and the reader concludes it. Give the deduction a surface to land on.

Two structural consequences worth holding while drafting: a chapter with only one speaking
character is a chapter `voice-separation` cannot audit, and a walk-on who never opens their mouth
cannot pass the swap test in `character-profile`. Both skills quietly no-op on a silent cast.
