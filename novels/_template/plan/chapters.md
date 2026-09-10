# Chapter construction list

The working grid. `chapter-plan` maintains it; `write-chapter` reads one row and writes it.
Keep 10–15 rows planned ahead of the draft line, never the whole book — later rows go stale.

**status**: `planned` · `drafted` · `revised` · `published`

| # | title | pov | arc | temp | hooktype | goal | obstacle | turn | event | delivers | cost | threads | hook | status |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|

Column meanings — every middle column is mandatory before a row may be drafted:

- **temp** — this chapter's temperature: `fast` · `tense` · `loud` · `warm` · `funny` · `bleak` ·
  `procedural` · `quiet`. Set it *before* drafting, or the chapter inherits the last one's. Never
  the same value three chapters running; at least four distinct values across an arc. A quiet
  chapter is earned by a loud one. See `hook-and-pacing`.
- **hooktype** — the shape of the last beat: `reveal` · `arrival` · `decision` · `question` ·
  `threat` · `reversal` · `cliff` · `quiet`. Not more than twice in any five chapters, and
  `cliff` at most once per 8–10. The eight exist so a reader cannot predict the last line — which
  is what reads as machine-made long before any individual sentence does. See `hook-and-pacing`
  §Hooks for what each one is and how to build it.
- **goal** — what the POV character is actively trying to get *in this chapter*. Concrete, not
  emotional. "Reach the ledger room", not "feel less afraid".
- **obstacle** — what stands in the way, with a will of its own where possible.
- **turn** — the thing that is not what the POV character expected. Every chapter turns.
- **event** — the thing that *happens*, in one clause a reader could retell: a concrete verb and
  a target. "She lies to the Hokage about the recovery list." Not a state, not an effect, and
  never an abstract noun — `trust`, `proximity`, `attention`, `tension` and their family are
  rejected outright, because they describe what an event *did* rather than the event. This is the
  column that stops a chapter being 1,100 words of somebody's interior weather, and the beat it
  names gets the most words in the chapter. It is copied to the chapter's `event:` frontmatter and
  must be recognisable in the CCS `ev>` line.
- **delivers** — what is materially *different* at the end, in one clause. A difference, not a
  summary of events. This is the column `revision-pass` Pass 9 gates the finished chapter on, and
  it is copied into the chapter's `delivers:` frontmatter and the CCS `dlv>` line.
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
