---
name: character-profile
description: Create or amend a character profile that defines behaviour, speech and an arc ladder — including canon-derived profiles for fan fiction. Use when a new named character appears, when an existing character needs updating after a chapter changes them, or when the user says /novel-character.
---

# character-profile

One file per character in `bible/cast/<slug>.md`, from `_character-template.md`. A profile is
not a biography — it is **an instruction set for running the character consistently**, written so
that any chapter, at any point in a 400-chapter serial, produces the same person.

---

## What lives in `references/`

Open one when its trigger fires, not by default.

| file | open it when |
|---|---|
| `references/tier-a-and-b.md` | actually writing a principal's or a supporting character's file — the two procedures and the development-rate dial. Tier C never needs it |
| `references/special-cases.md` | the character is an antagonist, a clone or double, or a canon character — or an existing profile needs amending after a chapter changed them |
| `references/audit-card.md` | `revision-pass` Pass 2 opens this for the walk-ons. You do not |

## Cast tiers — decide this before writing anything

Most people in a novel are not characters, and profiling them like characters is how a
400-chapter serial runs out of context. Assign a tier the moment a new person appears.
**The default is C.** Promote on evidence, never in anticipation.

| tier | who | record | budget |
|---|---|---|---|
| **A — principal** | MC, love interest, deuteragonist, arc antagonists — anyone whose beliefs the story is *about* | full file, `_character-template.md` | ~600 w |
| **B — supporting** | recurs across an arc and does a job, but has no arc of their own: the squad-mate, the handler, the fence the MC keeps going back to | short file, `_supporting-template.md` | ~150 w |
| **C — walk-on** | one to three scenes and gone: the toll clerk, the informant, the rival who dies next chapter | one line in `bible/cast/_extras.md` | ~25 w |
| **D — furniture** | crowds, the guard who says *halt*, anyone the reader will never be asked to remember | nothing | 0 |

A tier-C character does not need a Lie, a ladder, a fear, a childhood, or anything a therapist
would recognise. **They need to not be interchangeable.** That is a different problem with a
much cheaper solution.

Add every *named* character to `bible/lexicon.md` in the same pass, at every tier. Always. A
spelling costs one line and a wrong spelling in chapter 90 costs a reader.

Two characters get their own skill first, then come back here for the tier-A profile:
the **MC** (`mc-design` — gender, appearance, intellect, origin, golden finger, form ledger) and
the **primary love interest** (`lead-interest`).

---

## Place them on the voice matrix before writing the file

A profile written in isolation produces a character who is as quick, as articulate and as wry as
the MC — because the MC is what the model calibrates against. Before filling in any template,
open `bible/cast/_voices.md` and put this person on it: **intel, articulacy, wit, heat, turn
length, hands, pressure, first move** (`voice-separation` §1). Read down the columns, not across
the row: you are deciding who they are *relative to the cast that already exists*.

Three constraints, checked in that file and not in this one:

- The cast **straddles** the MC — somebody above their intel tier, somebody below.
- At most **two** characters have wit other than `none`. Ordinary is the correct default.
- No two characters share **intel + articulacy + wit**. If a new character's row already exists
  under another name, change one of them or merge them.

Copies of a person — clones, avatars, doubles, body-snatches — are exempt, and declare it with the
`mirror:` block in the frontmatter. See `voice-separation/references/mirror-clause.md` and the Mirrors section below.

## And on the competence grid, for the same reason

`bible/cast/_competence.md` is the second cast-wide table, and it fails the same way: written one
profile at a time, every character comes out able to answer any question at the same confident
depth. Put the new character on the grid — **domain, level, and where the edge is** — and read the
columns (`competence-map` §1).

- An **unlisted domain is `none`**, never "probably fine". This one rule does most of the work.
- Above `professional` is budgeted: 3 for the MC, 2 for other tier A, 1 for tier B, 1 for a walk-on
  and it is their job.
- Every character has a **referral** — who they go to when it runs out, and what asking costs.
- Update §3, *what nobody here knows*. A cast-wide gap is a plot generator, and it stops a later
  chapter from quietly inventing a physician because it needed one.

Gods, immortals, cultivators and artificial minds are the exception here, and they declare it with
`knowledge_scope: broad` plus a shape and a boundary (`competence-map/references/broad-knowledge.md`).

---

## Tier C — the three-stroke sketch

Three strokes, invented on the spot, recorded as one line. This is the entire method.

1. **A want inside the scene.** What they are trying to get through in the next five minutes —
   *close early, not be blamed, get the cart moving.* A five-minute goal, not a life goal.
2. **One habit, physical or verbal.** Small, concrete, and repeatable if they come back.
   *Stamps twice and checks the second one. Says "right then" before bad news.*
3. **One piece of the world they carry.** A price, a grievance, a rule they enforce, a rumour,
   something that changed at their work last month. **This is the stroke that matters.** It turns
   a function in a scene into a window onto the world — and it is where thread seeds, foreshadowing
   and world texture enter the story without an exposition scene.
   It is also their **entire competence map**: a walk-on knows their job and not the thing standing
   next to it. The toll clerk knows the levy and not why it was raised; the ferryman knows the river
   and not the town on the far bank. That edge is what stops an extra from becoming a convenient
   mouth for whatever the scene needs explained (`competence-map` §3).

Plus **one axis off default** (`voice-separation` §8) — not a fingerprint, one way of being unlike
everyone else in the scene: the one who will not stop talking, the one who answers in three words,
the one who thinks this is funny, the one who does not look up from their hands. A walk-on without
it speaks in the narrator's register, and the narrator's register is the MC's.

Recorded in `bible/cast/_extras.md`, one line:

```
Marek Oss — toll clerk, Ashfall east gate — ch 12, 19 — alive
  wants: to close early | tic: stamps twice, checks the second | carries: the gate levy doubled
  last month and nobody was told why | voice: answers in three words or fewer
```

That is all of it. No thumbnail, no want/need/fear/lie, no competence table, no ladder, no
calibration lines, no growth row, no matrix row.

**The swap test.** Not the tag-removal test — that is for tier A and B. Ask: *could this scene be
handed to any other extra with no edit?* If yes, they are generic. One stroke fixes it, and it is
almost always stroke 3.

**No interiority below tier B.** The narration never tells us what a walk-on feels or once was.
What they want is visible in what they do with their hands. A paragraph of backstory for someone
with two scenes is the cost the tier system exists to avoid.

**The doomed-extra rule.** A character written to die next chapter gets the *same* three strokes as
any other walk-on, delivered in the chapter *before* the one where they matter. Sudden
characterization is a death flag and readers read it fluently — the man who is abruptly given a
daughter and a woodworking hobby on page two is dead by page nine, and everyone knows it. Nor
should you inflate them to make the death land: a death lands from what it costs the survivor, not
from how much the reader knew about the corpse.

## Promotion and demotion

`python3 scripts/sw.py state novels/<slug>` reads the roster in `bible/cast/_extras.md`, counts
each walk-on's appearances **in drafted chapters only** — a planned future appearance is not an
appearance — and flags anyone at three or more who still has no profile. The other trigger,
*changed the plot*, is a judgement it cannot make; that one is yours.


**Promotion is retroactive, and it is triggered, not scheduled.** Promote when either fires:

- a third appearance, or
- they make a decision that changes the plot — at any appearance, including the first.

Then write the file *from what is already on the page*. Everything already written is canon and
constrains the profile: the three strokes become the seed of the want, the fingerprint and a
continuity fact. Do not contradict a line they have already said in order to get a tidier profile.

**Demotion.** A tier-B character with no appearance in 40 chapters and nothing scheduled goes
`status: dormant` in their frontmatter and drops out of the read-set until they return. Keep the
file — continuity facts are permanent — just stop paying for it every chapter.

**Roster budget.** When `_extras.md` passes ~50 lines, split it into sections by location or
faction and load only the sections the chapter touches. When a walk-on has not been referenced in
three arcs and is not dormant-with-a-purpose, they can be dropped from the roster entirely; if
they reappear, they are a new sketch.

## Quality bar

**Tier A**

- [ ] Could another writer run this character from the file alone?
- [ ] Are their three sample lines distinguishable from every other character's, tags removed?
- [ ] Do they differ from the MC on at least two voice axes — or are they a declared mirror?
- [ ] Is there something conversational they cannot do that the MC does easily?
- [ ] Do they want something the MC's success would cost them?
- [ ] Do they have at least two incompetences, one of them adjacent to their expertise?
- [ ] Does every competence row name **where the edge is**, and is the above-`professional` budget
      respected — with a referral for what lies outside?
- [ ] Is there something they are wrong about that they will not stop being wrong about soon?
- [ ] Have you avoided defining them by appearance, ethnicity, or their relationship to the MC?

**Tier B**

- [ ] Ten fields filled, none of them a paragraph
- [ ] Their matrix row is in `_voices.md` and differs from every other row on at least two axes
- [ ] One domain, one edge, one referral — and everything else is `none`
- [ ] Their one calibration line is not interchangeable with any principal's
- [ ] The shift names a trigger and a voice delta
- [ ] They want something for a reason that predates the MC

**Tier C**

- [ ] Three strokes, one line, no interiority
- [ ] One axis off default, so they do not speak in the MC's register
- [ ] Passes the swap test — stroke 3 is specific to them
- [ ] Named ones are in `lexicon.md`
- [ ] If they die soon, they were sketched in an earlier chapter and not inflated

`bias-guard` applies at every tier and is *most* often broken at tier C, where a person is one
detail wide and the default reaches for a stereotype to fill the space. A walk-on defined by an
accent, an ethnicity, a body, or a job-plus-nothing has failed the swap test as well as the bias
audit — the same stroke fixes both.
