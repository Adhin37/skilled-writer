---
type: reference
owner: power-system
description: building the system - choosing a cost axis, writing limits that generate plots, and the worked example
---

# power-system — designing the system

Open this at `novel-init`, or when the system exists and is not producing any plots — which is
almost always a limits problem rather than a mechanics problem.

The four hard rules are in the skill body. This file is how to actually pick them.

---

## Start from the limit, not the power

The instinct is to design what the power *does*. That is the least useful half: what a power does
generates spectacle, and what it **cannot** do generates story. A reader who can tell what is
impossible is a reader who can be surprised, and a reader who cannot is watching a cartoon.

So write the two "this can never…" sentences first, and derive the capability from them. If the
limits are hard to write, the power is too broad and needs narrowing before anything else
happens.

**The test for a good limit:** it should be possible to state a problem the MC obviously cannot
solve. If no such problem exists, there is no system, there is a wish.

## Choosing the cost axis

Costs are not interchangeable. They differ in one property — **how long the consequence lasts** —
and that property decides what kind of story you get.

| axis | lasts | produces | watch for |
|---|---|---|---|
| fatigue | until morning | nothing. It is the weakest axis available | it resets, so it never accumulates into a decision |
| material | until they buy more | supply plots, dependency, a market, a supplier with interests | it turns the power into money, which is fine if you meant it |
| time | permanently, invisibly | dread, and a character who is spending their life | it needs to be visible to somebody or it is not a cost |
| body | permanently, visibly | the strongest and the most limiting — each use is a decision the reader can count | it caps the story's length unless there is a way back |
| memory | permanently, and the character cannot audit it | the most unsettling. They do not know what they have lost | hard to escalate without cruelty |
| reputation | socially | plots about **who saw**, which is the cheapest tension there is | only works in a society that cares, so it needs `social-fabric` |
| relationship | someone else pays | the best costs in character-driven work | can become emotional bookkeeping if used every chapter |
| moral | the character carries it | works only if somebody in the cast disagrees with them about it | easily becomes the narrator's opinion (`bias-guard`) |
| debt | until the creditor calls | a person with their own interests, which is a plot in itself | the creditor must actually want something |

**Pick two.** One that bites in the scene and one that accumulates across the book. A system with
only the first has no arc; a system with only the second has no tension today.

## Writing the counter

The fourth hard rule is the one most systems fail, and it is failed silently — nobody notices
until chapter 60, when the MC is strong and nothing can threaten them.

> **How does a weaker person beat a stronger one in this world?**

Answer it concretely, with a name. The legitimate answers: preparation, terrain, numbers,
information, the stronger party having something to lose, a cost the stronger party cannot pay
today, and institutional force. If the only honest answer is "they don't", the system will run
out of story exactly when the MC becomes interesting.

The counter also has to be **available to the opposition**. A world where only the MC gets to be
clever about the rules is a world where the rules are decoration.

## The worked example

```
capability   Read the last hour of a place by touching its stone.
cannot       Never a person, only worked stone. Never more than an hour back.
cost 1       An hour of her own most recent memory, taken from the same day. (body/memory)
cost 2       The stone keeps a trace. Another reader can tell she was there. (reputation)
limit-plot   Anything important happens on wood, on the road, or more than an hour ago.
counter      Wait her out. She cannot read a room somebody sat in patiently for two hours.
gain-problem Everyone who knows what she is, knows where she has been.
learned      From her aunt, badly, over two years. She still cannot do doorways.
```

Note what the limits generate: a reason for the antagonist to be patient, a reason for the MC to
be late to everything, and a scene where she has to choose which hour of her day to lose. None of
that came from the capability.

## The three checks before it ships

1. **State a problem the system obviously cannot solve.** If you cannot, go back to the limits.
2. **Name what nobody understands about it.** Practitioners know their technique and their
   school's account of it, and a great deal of folklore they cannot distinguish from either. The
   scholar's model and the street's model disagree, and both are partly wrong — that disagreement
   is free plot and it stops the system from being narrated by whoever is standing there
   (`competence-map`).
3. **Run `social-fabric` §2 on every hard rule**, down to institution, market and household. A
   system that has not changed how ordinary people work, eat and inherit is a game mechanic with
   a setting attached.

`power-scaling` then owns the shape of it over the book: the ladder, how far ahead the opposition
stays, what a gain must carry, and what a temporary boost costs.
