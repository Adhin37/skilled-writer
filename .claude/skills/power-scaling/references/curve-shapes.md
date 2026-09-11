---
type: reference
owner: power-scaling
description: choosing or changing scaling.shape, or the curve has to work in a genre whose conventions fight it — cultivation, litrpg, superhero, mundane
---

# power-scaling — the four shapes, and genre notes

Open this when choosing or changing `scaling.shape`, or when the curve has to work in a genre whose
conventions fight it. Continues `SKILL.md`'s section numbering.

## 6. The four shapes, worked

### `climb` — the default

`start_tier` 1 or 2, one gain every `gain_gap_min`+ chapters, arriving at `ceiling_tier` in time
for `endgame`.

```
tier   1   1   2   2   2   3   3   3   3   4   4   4   5   5   6
P     +1   0  +1  +1   0  +2  +1   0  +1  +1  +2   0  +1  +1  +1
arc    1───────────2───────────────3───────────────4───────────5
```

Read the second row, not the first. The MC climbs five tiers and the pressure never leaves +2…0 —
that is a working curve. The opposition rose with them, and it rose because the arc plan said so,
not because the MC got strong and something had to be found to threaten them.

**The shape of one arc**, which is the unit you actually plan: open near +2 so the arc has a wall,
sit at +1 through the middle, put the gain two-thirds through, and let the climax land at +1 *after*
the gain rather than at 0. A gain that drops the climax to 0 has bought the MC a fair fight, which
is the most satisfying place to end an arc and the easiest to get wrong by granting the gain too
late.

### `inverted` — the MC is already at the top

*One Punch Man.* The gap is negative and permanent; `P` sits at −3 and stays there. This is a real
book and the toolkit supports it, on one condition: **`scaling.substitute_tension` is non-empty and
the story actually runs on it.**

What replaces the question, in practice — pick one and commit, do not hedge across three:

| substitute | the engine | what the chapters are about |
|---|---|---|
| **recognition** | nobody knows, or the wrong person gets the credit | the gap between what the MC did and what the world recorded |
| **boredom** | winning stopped meaning anything | the search for a thing that costs something |
| **cost of being feared** | the MC's presence is itself a threat | who leaves, who lies to them, who cannot be honest in the room |
| **the people around them** | the MC is safe; nobody else is | every stake is somebody else's, and the MC cannot be everywhere |
| **the wrong problem** | force does not solve this | politics, grief, a lie, a system — things a punch cannot reach |

The failure to avoid: writing `inverted` and then *quietly reintroducing a ladder* — a villain who
can actually threaten the MC, arriving around chapter 40 because the author missed having stakes.
That is not an inverted curve, it is a `climb` with a dishonest first act. If a real threat is
coming, the shape is `plateau-late` or `regression`, and the plan should say so.

### `regression` — starts high, loses it, reclaims it

Fallen immortals, stripped cultivators, the retired legend, most reincarnation-after-death premises.

```
tier   6 │ 1   1   2   2   3   3   4   4   5 ...
         └─ the loss, ON THE PAGE
```

The one rule: **the loss is a scene, not backstory.** A novel that opens after the fall has an
`start_tier: 1` MC with a memory, which is `climb` — a perfectly good book, but the reader never
felt the loss and never gets the reclaim's payoff. If the fall matters, chapter 1 or 2 spends it.

The second rule: **reclaiming is not free re-acquisition.** Every step back up is a full gain row
in §4 with all four requirements. "They already knew how" is not a source, and knowing how while
being unable to is the most productive plateau in the genre (`competence-map` stage 1 — fails
knowingly).

### `plateau-late` — the ladder stops mattering

Climbs normally, then around the last third the tier stops moving and conflict relocates: to
politics, to whom the MC has become, to a problem force cannot reach. `ceiling_tier` is reached
early and deliberately.

This is how a long serial ends without a bigger sky. The plateau chapter is **planned into
`state/power.md` §6**, not discovered when the author runs out of tiers. Its signature: the last
gain creates a problem the gain cannot solve, and the remaining arcs are that problem.

## 7. Genre notes

**Cultivation / xianxia.** The genre's realms are `state/power.md` §2's ladder — use them, and keep
the corpus habits out (`power-system` §Cultivation-specific notes). The one adjustment: realm gaps
in the source material are *enormous*, and a straight reading makes every cross-realm fight P=+3.
Compress. Treat one realm as one tier, and let the edge close the one tier it is allowed to.
Breakthroughs are gain rows and need all four requirements — which is precisely what the
bottleneck-then-epiphany cliché skips.

**LitRPG.** Levels are a rendering of the ladder, not a second ladder (`litrpg-system`). Map a band
of levels to each tier and record the mapping in §2, or the numbers and the pressure will drift
apart and the numbers will win. A level-up is not automatically a gain row; it is one only when the
tier moves.

**Superhero / modern power.** The ladder is usually flat and short (3–4 tiers) with the interest in
*kind* rather than degree — which makes pressure a poor single number. Use the tier for raw
capability and let the arc's band be wider (±1 counts as even), then lean on `conflict-engine`'s
stake rung for the escalation the tier will not give you.

**Mundane — thriller, political, slice-of-life, literary.** `shape: none` is a legitimate answer
and turns the skill off. But before reaching for it: an ordinary MC still has a capability curve
(what they can get done, whom they can call, what a room will let them do) and still faces
opposition of a definable weight. A courtroom novel where the MC's first case is P=+2 and their
last is P=0 has a power curve and benefits from tracking it. `tiers: 4` and a ladder written in
plain nouns — *nobody · a junior · a partner · the firm* — costs a table and buys the same
monitoring.

**Fan fiction.** The source's own power structure is the ladder, and canon characters get tiers
from how they are *depicted behaving*, not from wiki numbers
(`timeline-engine/references/fanfic-mode.md`). The genre-specific trap is a self-insert whose
`start_tier` is set against canon's endgame rather than against the arc the fic actually opens in —
a tier-1 opening in a world whose ladder tops out at 7 is the correct configuration even when the
MC "knows" they will get there.
