---
name: chapter-plan
description: Build and extend the arc plan and the chapter construction list. Use when starting a novel, when fewer than 8 planned chapters remain ahead of the draft line, when an arc ends, or on /novel-plan.
---

# chapter-plan

Produces `plan/arcs.md` (why the next 25 chapters exist) and `plan/chapters.md` (what each one
does). A serial fails at the planning layer long before it fails at the sentence layer.

---

## What lives in `references/`

| file | open it when |
|---|---|
| `references/titles-and-replanning.md` | filling the title column for a run of rows, or the draft has diverged and you are deciding whether to replan |

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
4b. Set the arc's **pressure band** and its gain, into `state/power.md` §6: the MC's tier at entry
   and exit, the top opposition tier, and where the gain lands. Open near +2 so the arc has a wall,
   hold +1 through the middle, place the gain about two-thirds through, land the climax at +1
   *after* it. The ladder in step 4 is stakes; this is the distance (`power-scaling` §1, §4).
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
   (`competence-map/references/acquisition-ladder.md`).
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
10b. **Pay something.** Name the thread this arc **closes on the page**, not the ones it advances.
    An arc that opens four threads and pays none is how a serial acquires the one complaint
    readers actually drop books over — perpetual deferral. Every thread carried past this arc
    gets a reason recorded next to it in `state/threads.md`, and a thread carried twice is either
    escalated into something the reader can see moving or abandoned outright (`plot-threads`
    §Ageing). "It pays off eventually" is not a plan; it is the absence of one.
11. **Test the idea.** If `theme.controlling_idea` is set, decide whether this arc puts it under
    pressure, and how — a **choice**, never a conversation about it. If it does, add the arc
    number to `theme.tested_in_arcs`. At least one arc in three should be on that list, and at
    least one of them is an arc where `theme.counter_case` gets the better of the argument.
12. Write the **exit hook**.
13. Fill the arc template in `plan/arcs.md`, and §4 of `plan/timeline.md`.

## Procedure — chapter rows

Work in batches of 10–12.

1. Distribute the escalation ladder's five rungs across the arc. Those become the arc's five
   pillar chapters.
2. Between pillars, chapters do one of: **pursue** (progress toward the pillar), **complicate**
   (a new obstacle), **cost** (pay for the last pillar), **reveal** (information changes the
   situation), **relate** (a relationship shifts — still with a goal and a turn).
3. For each row fill, **in this order**: goal → obstacle → turn → **delivers** → cost → threads →
   hook → title. The title comes last. A title invented first is a title the chapter has to serve.
   **`delivers`** is what is materially different at the end — a fact learned, a relationship
   moved, a position lost. If a row's `delivers` restates its `goal` or narrates its events, the
   chapter has no reason to exist and gets merged with a neighbour. This is the same test
   `revision-pass` Pass 9 applies to the draft, moved forward to where it is cheap.
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

### Arc 1 is different — the opening arc has jobs no other arc has

Rows 1–5 of the very first arc are planned against `story-opening`, not against the rhythm table
above, because they are doing something the rest of the book never has to do again: converting a
stranger into a reader. About 60% of the people who open chapter 1 reach chapter 2; from chapter 5
onward, retention runs 80% or better. Nearly all the attrition is at one join.

Four beats are **planned rows, not hoped-for outcomes** — each one names a chapter:

| beat | by | what the row must say |
|---|---|---|
| The anchor | `opening.anchor_by_ch` | which beat tells the reader what world this is — and for fanfic, which story and roughly when in it |
| The genre contract | `opening.contract_by_ch` | what makes the subgenre unmistakable |
| The promise touched | `opening.promise_touched_by_ch` | where the blurb's promise first reaches the page |
| The first win | `opening.first_win_by_ch` | where the MC's central advantage *works*, legibly |

**The frame rule.** *An escalation rung may not be scheduled before the frame it depends on.*
Before planning a chapter in which being noticed is dangerous, find the earlier row where the
reader learned what being noticed costs here. If there is no such row, insert one — usually a
bystander losing to the machinery — or move the escalation later. A threat the reader cannot price
does not read as tension; it reads as an adult being strict.

**The pressure follows the plan, not the draft.** A chapter's opposition is derived from the arc's
band in `state/power.md` §6, never invented at the strength the scene turned out to need. That
inversion is what produces cannon fodder in one direction and the god-step in the other.

**No all-failure ladders.** An arc-1 escalation ladder whose every rung is the MC's advantage
letting them down is not a ladder, it is a slide. At least one rung is a win that advantage bought.
This is the commonest way a strong premise gets planned into a weak first arc: the author, wary of
an overpowered MC, schedules the correction before the thing being corrected has ever worked. See
`meta-knowledge` §4 and `conflict-engine`.

### The volume shape, for reference

A widely-used serial roadmap, useful when `arc_length` is near 30 and worth knowing when it is not:
**1–5** hook and world entry · **6–15** the progression loop, where gains are visible and
measurable · **16–25** compounding stakes, subplots intersecting, the first approach proving
insufficient · **26–30** resolution of the arc's goal, with its consequences opening the next.
Keep **at most two active subplots** alongside the main line; a third is how threads get dropped.

## Self-check

- [ ] Every planned row has all seven middle columns
- [ ] Every arc has a permanent cost to the MC
- [ ] The antagonist's case is arguable in two sentences
- [ ] Every open thread has a `due` chapter within the planning horizon
- [ ] No three consecutive rows share a chapter type
- [ ] The five pillar chapters escalate what is *lost*, not what is *fought*
- [ ] Any expertise the arc requires is on someone's map, or is planned to be acquired or bought
