# Chapter construction list

The working grid. `chapter-plan` maintains it; `write-chapter` reads one row and writes it.
Keep 10–15 rows planned ahead of the draft line, never the whole book — later rows go stale.

**status**: `planned` · `drafted` · `revised` · `published`

| # | title | pov | arc | goal | obstacle | turn | cost | threads | hook | status |
|---|---|---|---|---|---|---|---|---|---|---|

Column meanings — all seven middle columns are mandatory before a row may be drafted:

- **goal** — what the POV character is actively trying to get *in this chapter*. Concrete, not
  emotional. "Reach the ledger room", not "feel less afraid".
- **obstacle** — what stands in the way, with a will of its own where possible.
- **turn** — the thing that is not what the POV character expected. Every chapter turns.
- **cost** — what this chapter takes. May be small (a lie told, an hour lost, an ally's respect)
  but never zero. See `conflict-engine`.
- **threads** — ids from `state/threads.md`: `^` advance, `~` open, `v` pay.
- **hook** — the final beat, in five words. See `hook-and-pacing`.

---

## Title conventions

Titles are read as a scrolling list on a phone. They do three jobs: promise, distinguish, and
avoid spoiling.

- 2–7 words. No subtitles, no colons stacking two ideas.
- Concrete noun or a line of dialogue beats an abstraction. "The Ledger Room" beats "Revelations".
- Never spoil the turn. "The Ledger Room" ✓ — "Her Father Was the Buyer" ✗.
- No numbering inside the title ("Arc 2 Part 3"). The number column handles that.
- Vary the grammatical shape across any run of five: not five noun phrases in a row.
- Recurring formulas are allowed *once* as a motif (e.g. three chapters called "Debt", "Interest",
  "Collection") and only when the payoff lands on the third.
- For fanfic, do not reuse canon episode or chapter titles.

## Title pattern bank

| pattern | example shape |
|---|---|
| Place, definite | The Undercroft |
| Object with a claim on it | Her Brother's Coat |
| Overheard line | "Say That Again" |
| Transaction | Payment in Full |
| Understatement of violence | A Quiet Morning at the Gate |
| Role reversal | The Student Sets the Test |
| Countdown | Nine Hours of Water |

## Batch-planning rule

When generating a run of chapter titles, generate the `goal/obstacle/turn/cost` first and the
title last. A title invented before the beat is a title the chapter then has to serve.
