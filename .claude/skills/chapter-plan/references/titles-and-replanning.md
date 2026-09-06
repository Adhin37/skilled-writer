# chapter-plan — the chapter-title pattern bank, and replanning triggers

Open this when filling the title column for a run of rows, or when the draft has diverged and you are deciding whether to replan.

---

## Titles

Rules and a pattern bank live in `plan/chapters.md` (the template's own header). Enforce:

- 2–7 words; concrete over abstract; never spoil the turn
- no colons stacking two ideas; no arc/part numbering in the title
- vary the grammatical shape across any five consecutive titles
- fanfic: never reuse a canon episode or chapter title
- read the run aloud as a list — that is how a reader meets it, scrolling on a phone

**Anti-pattern check.** If more than two titles in ten begin with "The", rewrite. If any title
could belong to any chapter of any novel ("Revelations", "The Beginning", "Awakening"), rewrite.

## Replanning triggers

`python3 scripts/sw.py state novels/<slug>` reports the first trigger below without reading the
plan: how many specified rows remain ahead of the draft line, and any row within reach of
drafting that has a blank goal, obstacle, turn, delivers, cost or hook. `write-chapter` will not
draft from an incomplete row, so this is the cheapest way to find out before it stops.


| trigger | action |
|---|---|
| Fewer than 8 planned rows ahead of the draft line | extend by 10 |
| A chapter went somewhere else | amend that row, re-check the next 3 |
| A thread has been `cold` for 20 chapters | schedule its payoff or its deliberate retirement |
| A character reached their rung 5 early | give them a new ladder or move them off-stage with dignity |
| The user is bored | look for a `cool` stretch that lost its goal; that is almost always where |
