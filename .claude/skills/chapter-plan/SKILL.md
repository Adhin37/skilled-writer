---
name: chapter-plan
description: Build and extend the arc plan and the chapter construction name list — chapter numbers, titles, goal/obstacle/turn/cost, thread operations and hooks. Use when starting a novel, when fewer than 8 planned chapters remain ahead of the draft line, when an arc ends, or when the user says /novel-plan.
---

# chapter-plan

Produces `plan/arcs.md` (why the next 25 chapters exist) and `plan/chapters.md` (what each one
does). A serial fails at the planning layer long before it fails at the sentence layer.

---

## Planning horizon

| layer | how far ahead | how firm |
|---|---|---|
| Ending target | whole novel | a direction, revisable |
| Arcs | current + next 2, one line each | current arc firm, others sketch |
| Chapter rows | 10–15 ahead of the draft line | firm; nearest 5 fully specified |

**Never plan the whole book at chapter granularity.** Rows more than ~15 ahead go stale as soon
as a chapter surprises you, and stale rows are worse than no rows: they get followed.

## Procedure — new arc

1. Read the book digest, the previous arc digest, open threads, and the growth ledger.
2. Write the arc's **dramatic question** — one sentence, answerable yes/no.
3. Write the **antagonistic force** and argue their case in two sentences from their own seat.
   If you cannot, redesign; a cannon-fodder antagonist ruins 25 chapters.
4. Build the **escalation ladder**: five rungs, each raising the cost of failure. Escalation is
   not "a stronger enemy" — it is a *worse thing to lose*.
5. Fix the **midpoint reversal**: the chapter where the MC's understanding is proven wrong.
6. Fix the **cost**: what the MC permanently loses. Required. Not "almost".
7. Assign **character rungs**: who advances, on which chapter, and what audibly changes. Check each
   planned voice delta against `voice-separation` §6 — growth must not walk a character onto the
   MC's axes. Any character the arc introduces as a recurring presence gets their matrix row now,
   placed against the existing cast, not invented in isolation when they first speak.
8. Assign **threads**: opened, paid, carried forward.
8b. Check the arc's **expertise**: does it turn on knowledge nobody in the cast has
   (`bible/cast/_competence.md` §3)? If so, decide now which it is — a character to introduce, a
   referral the MC has to buy, or a skill someone starts climbing. Deciding this at the scene means
   inventing a physician on the spot. If an arc *is* a learning arc for someone, place the stage
   transitions on specific chapters and leave the practice as clauses in between
   (`competence-map` §5).
9. Run `timeline-engine`: which world-track events fire in this arc, on which chapters, and how
   each reaches the MC. **Confirm the arc moves at least one of them** — moved, prevented,
   altered or created. An arc that leaves the world track untouched is an arc the MC was a
   tourist in. Then run the point-of-no-return check: does anything scheduled here make
   `ending.contract` unreachable, or take a `non_negotiable`? If so, rescale, delay or redirect it.
10. Name the arc's **world layer**: which part of the world this arc makes concrete — a place, an
    institution, a class, a trade — and the two or three chapters that show it working. If it is
    a layer the story has not entered before (court, slum, army, temple, ship), run `social-fabric`
    for half a page on it *before* the rows are written, not while drafting. An arc set entirely
    in already-established territory answers "nothing new", which is a legitimate answer once.
11. Write the **exit hook**.
12. Fill the arc template in `plan/arcs.md`, and §4 of `plan/timeline.md`.

## Procedure — chapter rows

Work in batches of 10–12.

1. Distribute the escalation ladder's five rungs across the arc. Those become the arc's five
   pillar chapters.
2. Between pillars, chapters do one of: **pursue** (progress toward the pillar), **complicate**
   (a new obstacle), **cost** (pay for the last pillar), **reveal** (information changes the
   situation), **relate** (a relationship shifts — still with a goal and a turn).
3. For each row fill, **in this order**: goal → obstacle → turn → cost → threads → hook → title.
   The title comes last. A title invented first is a title the chapter has to serve.
4. Vary the chapter *type* — never three `pursue` rows in a row.
5. Check the arc's rhythm against the shape below.

### Arc rhythm (25 chapters)

| chapters | function | temperature |
|---|---|---|
| 1–3 | new situation, new want, first obstacle | rising |
| 4–8 | pursue and complicate; the arc's world gets specific (`world-texture` — through consequence, not description) | steady |
| 9–11 | first pillar; a win with a price | hot |
| 12–14 | midpoint reversal — the MC was wrong about the problem | hot |
| 15–17 | fallout; the cost lands; relationships shift | cool, but not idle |
| 18–22 | the real problem pursued, with worse odds | rising hard |
| 23–24 | climax; the permanent loss | hottest |
| 25 | consequence and exit hook; next arc visible | falling, then a spike |

The `cool` stretch is load-bearing. Serials that run hot for 25 straight chapters exhaust the
reader and flatten the climax. But *cool ≠ idle*: chapter 16 still has a goal, a turn and a cost.

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

| trigger | action |
|---|---|
| Fewer than 8 planned rows ahead of the draft line | extend by 10 |
| A chapter went somewhere else | amend that row, re-check the next 3 |
| A thread has been `cold` for 20 chapters | schedule its payoff or its deliberate retirement |
| A character reached their rung 5 early | give them a new ladder or move them off-stage with dignity |
| The user is bored | look for a `cool` stretch that lost its goal; that is almost always where |

## Self-check

- [ ] Every planned row has all seven middle columns
- [ ] Every arc has a permanent cost to the MC
- [ ] The antagonist's case is arguable in two sentences
- [ ] Every open thread has a `due` chapter within the planning horizon
- [ ] No three consecutive rows share a chapter type
- [ ] The five pillar chapters escalate what is *lost*, not what is *fought*
- [ ] Any expertise the arc requires is on someone's map, or is planned to be acquired or bought
