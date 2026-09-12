---
type: reference
owner: voice-separation
description: children, teenagers and the old - the cadence differences the voice matrix does not capture
---

# voice-separation — age and register

Open this when the cast contains anyone substantially younger or older than the adults, or when
the cadence test has flagged a pair and one of them is a child.

The matrix axes are built for adults talking to adults. Two characters can hold different `intel`,
`artic`, `wit` and `turn` values, pass every check in `sw cast`, and still read as one voice when
one of them is six — because what separates a child from an adult is not how clever they are. It
is **sentence architecture, subject range, and what they do when they do not know something.**

Benchmark run #3 shipped a mother and her six-year-old with different declared axes, a clean cast
check, and one voice between them. This file is the fix.

---

## What actually changes with age

| | young child (~4–7) | child (~8–12) | adolescent | adult | old |
|---|---|---|---|---|---|
| **clause depth** | one. Two joined by *and* | two, rarely subordinated | full range, unevenly | full range | full range, shorter by choice |
| **subject range** | the present, the concrete, themselves | rules, fairness, categories, mastery | status, the future, the self as a project | consequences, other people | the past as evidence, and the present as a repeat |
| **when they don't know** | assert something else confidently | ask, or pretend they knew | conceal it | ask, defer, or guess openly | say so, at length, or not care |
| **time** | now and soon | today and the holidays | this year, and forever | seasons, deadlines | decades, and very recent things poorly |
| **negotiation** | repetition and volume | bargaining, precedent, *that's not fair* | leverage, and testing what holds | trade | refusal, often without explanation |
| **interruption** | constant, without noticing | on topic change | strategic | situational | as a right |

The single most reliable marker is the **first row**. A six-year-old does not produce a sentence
with a subordinate clause in it, and an adult who wants something produces three. Nothing else on
the page separates them as fast, and no axis in the matrix measures it.

## The three things a child is not

- **Not a small adult.** Not with less vocabulary and the same reasoning shape underneath.
- **Not stupid.** Children reason well from what they have, which is the wrong set of facts.
  A child's wrong conclusion should be *well-argued from a bad premise* — that is the funny,
  true, and characterising version.
- **Not a device.** A child whose only function is to be endangered, to say the innocent thing
  that lands the theme, or to make an adult sympathetic is furniture, and `bias-guard` §agency
  binds here the same as anywhere.

The adjacent error: **the uncanny child**, who speaks in aphorisms and sees through everyone. It
is the same defect as the wise old mentor — an age used as a licence for the narrator's own
insight.

## Competence, which is where age plays fair

A child's `eq` is often higher than their `intel` would predict and their **vocabulary for it is
absent**: they know exactly what the mood in the room is and cannot name it, so it arrives as
behaviour — going quiet, getting louder, asking an unrelated question at the wrong moment. That
mismatch is a genuine social-perception state, not a simplification (`social-perception` owns the
tier; this is what it sounds like without the words).

For the old: `competence-map` binds unchanged. Age is not expertise, and experience is expertise
**in a world that may have moved**. The most interesting old character is right about the
mechanism and wrong about the current facts.

## Adolescents

The hardest to write and the most often written as adults with worse judgement. What actually
separates them: the **register switches by audience** more sharply than at any other age — one
voice with parents, another with peers, a third with an adult they respect — and the switch is
visible and deliberate. A teenager who sounds the same in all three rooms is an adult.

Their turn lengths are bimodal: monosyllables where a question is an intrusion, and long fluent
runs about the thing they care about. Hold both, in the same chapter.

## What to put in the matrix

Age does not get its own axis — it is not a dial and it does not belong beside `intel`. Instead,
when a character is a child or notably old, record it where it will actually be read:

- their `turn` number, set from the table above, not from their personality;
- **one clause-depth note in the `cannot` column** of §4 — *cannot hold two clauses*, *cannot ask
  for help without an excuse*;
- their emotional signature in the profile, which for a child is usually more legible than an
  adult's, not less.

Then run the cadence test in §3 as normal. If the child and the nearest adult still read alike,
the problem is clause depth and it is fixed in one pass over their dialogue.
