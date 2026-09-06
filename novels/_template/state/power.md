# Power curve

Maintained by `power-scaling`. **Sections 1, 2 and 5 are in the read-set for every chapter while
`scaling.shape` is not `none`.** Delete this file if `scaling.shape` is `none`.

> **The gate.** No sentence may make a character more or less capable than §1 and §2 say they are.
> A confrontation is placed by choosing its **pressure** first and deriving the opponent's tier
> from it — never by inventing an opponent and pricing them afterwards. A capability the reader has
> not seen used *and seen fail* does not decide an outcome.

---

## 1. CURRENT STANDING

The row the writing model reads before every chapter.

| character | tier | since ch | the edge | what the edge cannot buy | active boost? |
|---|---|---|---|---|---|

`the edge` is `scaling.edge_worth` — `0` or `1`, **never 2**. Column 5 is load-bearing and must
stay true. One row for the MC, one for each antagonist whose tier the reader is tracking.

## 2. THE LADDER

One ladder, used for everybody, sized by `scaling.tiers`. Tier *names* stay out of the prose.

| tier | what it lets you do | what it still cannot do | how many alive | who the reader has met |
|---|---|---|---|---|
| 1 | | | | |
| 2 | | | | |
| 3 | | | | |

Column 3 does the work: capabilities alone are a power fantasy, capabilities *and* their limits
are a set of plots. Column 5 stops the escalating sky — a tier the reader has never met cannot
generate pressure.

## 3. THE PRESSURE LOG

One row per confrontation, appended as it is written. Also a `pwr>` line in that chapter's CCS
block — the two must agree, and `sw curve` checks that they do.

| ch | opposition | their tier | MC tier | P | outcome | what it cost |
|---|---|---|---|---|---|---|

`P` = their tier − MC tier. Bands: **+2** hopeless · **+1** outmatched · **0** even ·
**−1** favoured · **−2** trivial. See `power-scaling` §1 for what each band obliges you to do.

`what it cost` is mandatory at P ≥ +1 and is not "they were tired afterwards". A win at +1 costs
something that is still costing at the end of the chapter.

A chapter with no confrontation gets no row. Long runs without rows are fine; long runs where the
rows are all the same number are the monotony defect.

## 4. THE GAIN LOG

Every permanent tier advance. **At most +1 per row**, and every column is mandatory — a gain
missing one of them is a defect, not a style choice.

| ch | from → to | source | price paid (ch) | set up in ch | what it obsoletes | new problem |
|---|---|---|---|---|---|---|

- **source** — a person or institution with its own interests. Nothing found in a cave by luck.
- **price paid (ch)** — the chapter the price was paid, which must be *before* this one. Paid
  after, it is a receipt; paid before, it is a decision.
- **set up in ch** — where the mechanism was first named, at least `scaling.setup_lead` chapters
  back.
- **new problem** — if the gain only solves things, do not grant it.

Minimum `scaling.gain_gap_min` chapters between rows. Between gains, growth is in *skill*, which
lives in `state/growth.md` and costs nothing (`competence-map`).

## 5. ACTIVE BOOSTS

Temporary reach above the current tier. Legitimate, and never free.

| ch | boost | above tier by | expires ch | the debt | due ch | paid? | climax? |
|---|---|---|---|---|---|---|---|

**the debt** is what it costs *afterwards*, not its cost during use · **due ch** is within
`scaling.boost_debt_due`, and a row unpaid past it is a defect · **climax?** is `yes` if this
boost resolved an arc climax, and there is **at most one `yes` in the novel**.

A boost lets the MC *survive* a P ≥ +2 encounter. Winning one costs the ladder.

## 6. THE CURVE PLAN

Filled during `chapter-plan`, not discovered while drafting. This is the route from the beginner
village to `scaling.endgame`.

| arc | chapters | MC tier entry → exit | top opposition | pressure band | the gain, and where |
|---|---|---|---|---|---|

Shape for one arc: open near +2 so the arc has a wall, hold +1 through the middle, place the gain
about two-thirds through, and land the climax at +1 *after* it. See
`power-scaling/references/curve-shapes.md` §6.

Check the last row against `ending.contract`. A curve that arrives where the ending cannot happen
is a defect on both sides (`timeline-engine` §The ending contract).
