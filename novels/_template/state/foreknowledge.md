# Foreknowledge ledger

Maintained by `meta-knowledge`. **In the read-set for every chapter while `mc.foreknowledge` is
non-empty.** Delete this file if no character knows the future.

> **The gate.** The MC may not act on a fact that is not a row below, and may not act on a row
> above its declared grain. A `major-beats` memory does not produce a date. A row marked
> `invalidated` is gone — the MC may still *believe* it, and being wrong on the page is a scene,
> but the narration never treats it as true again.

---

## 1. THE GRAIN

`mc.foreknowledge_grain`, restated so it is in front of you while writing:

| grain | the MC can | the MC cannot |
|---|---|---|
| `episode-precise` | name events, order, and roughly when | know anything offstage in the source |
| `major-beats` | name the big turns and roughly who | order them confidently; date them |
| `impressions` | recognise a name, feel dread at a place | state what happens, or when |
| `fandom-corrupted` | recall vividly — **and be wrong** | tell what they read from what they were told |

The grain is a hard ceiling on every plan the MC makes. It is also the source of most of their
mistakes, which is the point: a wrong plan built honestly from a low grain is drama, while a right
plan built from a grain the MC does not have is a cheat the reader can smell.

## 2. THE INVENTORY

Every item the MC believes about what is coming. Written **before** the inventory scene, so the
scene has something to draw on.

| id | what they believe | grain | status | first spent (ch) | invalidated by |
|---|---|---|---|---|---|
| K1 | | | untested | — | — |

`status` — `untested` (never acted on) · `confirmed` (it happened as remembered) ·
`spent` (acted on; the advantage is used up) · `invalidated` (proven wrong, or butterflied away).

**Nothing starts `confirmed`.** Confirmation is an on-page event.

## 3. THE SPEND LOG

Every time foreknowledge is used. One row per use, appended as it fires; also a `fk>` line in that
chapter's CCS block.

| ch | item | used to | worked? | what it cost | what it invalidated |
|---|---|---|---|---|---|

`what it cost` is mandatory and is rarely the golden finger's declared price. The real cost is
usually **exposure**: acting precisely on knowledge you cannot explain having is a signature.

`what it invalidated` is the observer paradox doing its work — see §4.

## 4. THE OBSERVER PARADOX

**Acting on foreknowledge is the fastest way to destroy it.** Every spend that changes an outcome
must move at least one *other* row toward `invalidated`, because the future the MC remembers was
the future in which they did not act.

| the MC changed | therefore these rows are now suspect |
|---|---|

Keep this table honest and foreknowledge decays on its own, as a consequence the MC caused, rather
than by authorial decree at a scheduled chapter. This is the same ledger `timeline-engine` runs
for divergence; cross-reference the row ids rather than duplicating them.

## 5. THE ARC OF THE ADVANTAGE

The one check that a single chapter cannot make. Fill it during planning, not after.

| beat | chapter | on the page? |
|---|---|---|
| The inventory scene — the MC works out what they know and what they will do | | |
| **The first win** — it works, legibly, and the reader sees it came from foreknowledge | | |
| The first crack — a detail is off, and the MC notices before the reader does | | |
| The first failure — it is wrong, and it costs | | |

**Order is enforced: first win strictly before first failure.** An advantage the reader only ever
watches malfunction is not an advantage; it is a handicap the blurb lied about. See
`meta-knowledge` §4.

## 6. WHO SUSPECTS

| who | noticed what (ch) | concluded | acting on it? |
|---|---|---|---|

Being noticed is a plot event and belongs in `state/threads.md`, not only here.
