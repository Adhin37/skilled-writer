# Timeline — log

In-world clock plus the record of how the MC has bent the world track. Prevents the "three days of
travel that took one chapter and also one month" class of error, and the "MC changed nothing"
class of defect.

The *plan* for what the world will do lives in `plan/timeline.md`. Maintained by
`continuity-summary` (calendar) and `timeline-engine` (divergence).

## Calendar definition

- Day/unit label used in CCS blocks: `D<n>` counting from chapter 1, day 1.
- In-world date format:
- Seasons / cycles:
- Travel-time table (used to sanity-check any journey):

| route | mode | duration |
|---|---|---|

## Log

| ch | in-world day | elapsed since prev | location | notes |
|---|---|---|---|---|

## Divergence ledger

Every MC action that touched the world track. The gap between plan and log is the story's reason
to exist — for fan fiction, it is the whole argument.

| ch | MC action | track id | effect | order | who noticed | reciprocity opened |
|---|---|---|---|---|---|---|

`effect`: `moved` · `prevented` · `altered` · `created` · `unchanged` (only with a stated reason)
`order`: 1st / 2nd / 3rd — how far downstream this reached (see the butterfly budget)
`reciprocity opened`: what this escalation gave the MC as well as cost them. Required for every
escalation, per the governor's rule 4.

**Arc rule:** every arc must contain at least one row that is not `unchanged`.

## Crisis board

Unresolved crises currently in play. Cap is `timeline.reactivity`, hard-capped at 3.

| id | crisis | opened ch | driver | what would resolve it |
|---|---|---|---|---|

## World events fired

| ch | track id | fired as planned? | what changed about it | MC's part in it |
|---|---|---|---|---|
