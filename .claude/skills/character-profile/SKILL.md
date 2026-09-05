---
name: character-profile
description: Create or amend a character profile that defines behaviour, speech and an arc ladder — including canon-derived profiles for fan fiction. Use when a new named character appears, when an existing character needs updating after a chapter changes them, or when the user says /novel-character.
---

# character-profile

One file per character in `bible/cast/<slug>.md`, from `_character-template.md`. A profile is
not a biography — it is **an instruction set for running the character consistently**, written so
that any chapter, at any point in a 400-chapter serial, produces the same person.

---

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
`mirror:` block in the frontmatter. See `voice-separation` §7 and the Mirrors section below.

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
`knowledge_scope: broad` plus a shape and a boundary (`competence-map` §6).

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

## Tier B — the short file

`_supporting-template.md`. Ten fields, and no more:

| field | note |
|---|---|
| thumbnail | one sentence, a stance toward the world, not a description |
| job in the story | why the story needs this person; if it is "explains things to the MC", redesign |
| want, this arc | concrete and pursuable in a scene |
| one domain | the single thing they know well, where that expertise stops, one incompetence, and who they refer to outside it. One above-`professional` domain is the whole budget at this tier |
| voice axes | intel · artic · wit · turn length, plus hands, pressure move and first move. The matrix row, not a fingerprint |
| three speech fields | contractions · one vocabulary tell · one syntax tic. Not eight |
| one calibration line | their voice under pressure. Not three |
| one behaviour rule | *under pressure, they →* |
| relationship to the MC | current state, and the unspoken thing |
| **the shift** | see below |
| continuity facts | scars, kin, debts, possessions |

**The shift replaces the ladder.** A tier-B character does not get five rungs. They get *one
change*: what will be different about them by the end of the arc, and the trigger that does it.
Two positions, before and after, with a voice delta on the after. They go in `state/growth.md`
with `rung: B1` → `B2`, and that is the whole span available to them.

If a tier-B character's shift starts feeling like the most interesting thing in the arc, that is
the promotion signal. Take it — promotions are how a cast stays alive.

---

## Tier A — the full procedure

1. **Job first.** What does the story need this person for? One sentence. If the answer is
   "someone for the MC to explain things to", redesign — that is not a character.
2. **Want / Need / Fear / Lie.** The Lie is the engine; development is its erosion. Want must be
   pursuable inside a scene ("get the loan renewed"), not a mood ("be respected").
3. **Competence, with edges** (`competence-map` §1). Every domain row carries *where the expertise
   stops*, and an unlisted domain is `none` rather than "probably fine" — that default is the
   difference between a specialist and the generalist-with-no-edges the model writes by itself.
   At least two incompetences, and that is a floor; the interesting ones sit *adjacent* to the
   expertise, because those are the ones a reader assumes the character has. Budget: **two** domains
   above `professional` (three for the MC), each paid for with a scene showing how it was acquired,
   scheduled or already written. Add the **referral** — who they go to when it runs out, and what
   asking costs them. If this character is a god, an immortal, a cultivator or an artificial mind,
   set `knowledge_scope: broad` and fill the shape *and* the boundary (`competence-map` §6).
4. **Behaviour rules** — five to eight if/then rules, phrased so another writer could run them.
   These make the character predictable enough that breaking a rule reads as a *event*.
5. **Voice axes, then the speech fingerprint.** The axes first — intel, articulacy, wit and its
   trigger, heat, turn length, the conversational blind spot, and the thought fields if
   `pov_eligible` (`voice-separation` §1, §5). Then all eight fingerprint fields and three
   calibration lines in three emotional states (`dialogue-voice`). In that order: eight surface
   habits laid over a mind identical to the MC's produce a labelled clone, which is the defect the
   axes exist to prevent. This is the step most often skipped and most often regretted.
6. **Body & habit** — the three body fields (`voice-separation` §4): default state, **the hands**,
   and the pressure move — plus, for tier A, their habitual standing distance and what they do when
   someone crosses it. Gestures rather than portraiture; describe what the body *does*. Nothing
   from the banned set (nodded, shrugged, sighed, raised an eyebrow, crossed their arms) — those
   identify nobody. No beauty catalogue; see `bias-guard`. If this character's body changes over
   the novel — a child growing, a shapeshifter, someone maimed or restored — set
   `form_locked: true` and give them a stage table in `state/body.md` (`mc-design`).
7. **Relationships**, including the `unspoken` column — what each pair is not saying.
8. **Arc ladder** — five rungs, each with a trigger and a voice delta. See
   `character-development`.
9. **Regression conditions** — what sends them back down.
10. **Continuity facts** — scars, ages, kin, debts, possessions.
11. Register them at rung 1 in `state/growth.md` with their development rate.

## Development rate

`development_rate` in the frontmatter, 1–5. It sets how many chapters a rung typically takes.

| rate | rung takes | who |
|---|---|---|
| 1 glacial | 60+ ch | institutions in human form; the mentor who was right all along |
| 2 slow | ~40 ch | the settled adult, the long-term antagonist |
| 3 steady | ~25 ch | most of the recurring cast |
| 4 fast | ~15 ch | the young, the newly displaced, anyone under sustained pressure |
| 5 volatile | ~10 ch | the MC (always), and characters in freefall |

The MC is always 5 — not because they are special, but because the story concentrates its
pressure on them, and pressure is what moves a ladder.

Rate applies to tiers A and B only. A tier-B character's rate governs the one shift they get, not
five rungs. Tier C has no rate and no row in `state/growth.md`.

## Antagonists

Same template, plus:

- Their want must be **legible and sympathetic in isolation**. Write the two-sentence version of
  their case that would convince a reasonable reader.
- They must be **right about something** the MC is wrong about.
- They must have **a cost they are paying** for their position.
- Their competence is real and demonstrated before they lose anything — and **narrow**, like
  everyone else's. The antagonist who is a master strategist, swordsman, poisoner and administrator
  is the omniscience defect wearing a black coat; their edge is what the MC eventually gets in
  through (`competence-map` §1).

A villain who exists to be defeated is a chore. A villain whose defeat costs the reader something
is the arc.

## Mirrors — clones, avatars and doubles

A character who is a copy of another is the one case where sharing a voice is correct. Give them a
normal profile at their tier, plus the `mirror:` block in the frontmatter — `mirror`, `mirror_kind`,
`convergence`, `diverged_ch` — and a row in §5 of `_voices.md`. The rest of the profile is filled
from the source character's, changed only where their separate life has changed them.

Three things the profile must still answer, because they are what makes a double a character rather
than a duplicate file (`voice-separation` §7):

- **What has diverged since `diverged_ch`**, and at what rate. Different experiences make different
  people; a copy who has lived thirty chapters apart and sounds identical is a puppet, which is
  legitimate only if the story says so and somebody notices.
- **The tell** — the one thing that does not copy, and who could detect it. Plant it before it is
  needed (`plot-threads`). If nothing fails to copy, record `none — deliberate`.
- **Who the reader tracks in a shared scene** — the physical tag or POV anchor that keeps two
  mirrors apart on the page, unless the confusion is the intended effect.

A double with a different body is also `form_locked: true` with its own stage row in
`state/body.md`. The exemption covers declared mirrors only: a protégé, a sibling or a rival who
"is like a younger version of the MC" is not a mirror, it is a cast with two of the same person in
it.

## Fan fiction

Canon characters get a normal profile, derived from the source, plus:

1. **Derive from behaviour, not from fandom consensus.** Base each field on what the character
   is depicted doing in canon, not on what fandom says about them.
2. **The riot trait** — the one thing a reader would not forgive you for losing. Name it in
   `bible/canon.md` and never contradict it.
3. **Speech fingerprint from canon patterns**, described in your own words: register, rhythm,
   verbal habits, what they never say. Describe the pattern; do not transcribe source lines.
4. **Write original prose.** Never reproduce dialogue, narration, or text from the source work.
   The profile stores characterization, not quotations.
5. **Divergence-driven change only** (at `ooc_budget: low`): any behaviour that differs from
   canon must trace to the divergence point through events shown on the page.
6. **Log every reinterpretation** in `bible/canon.md`'s table, with in-story justification.
7. **Canon competence has edges too.** Derive the domains from what the source shows them doing,
   and mark everything else `none` — fandom quietly promotes a character to expert in whatever a
   fic needs. They also do not know the parts of canon they were never present for, and they do not
   know the future the writer knows (`competence-map` §1, §3).

Set `canon: true` in the frontmatter. OCs get `canon: false` and must pass the OC test: name the
job they do, and why no canon character could do it.

**Canon characters get tiers too.** A source work has hundreds of named people and this story uses
a handful. A canon character who appears in two scenes is a tier-C walk-on with three strokes —
except that stroke 2, the habit, must come from canon rather than invention, because a reader will
recognise them. The riot trait applies at every tier: it is one line, and it is cheap.

## Amending an existing profile

Profiles change; they are not carved. Amend when a chapter reveals or changes something.

- **Append, don't overwrite.** Continuity facts are permanent.
- Rung changes go in `state/growth.md` **and** in the profile's `current_rung`.
- If a chapter made a character act against their behaviour rules, decide: was it a defect
  (fix the chapter) or a development (add the rung, record the voice delta)? Never neither.
- If a character has been in ten chapters and their fingerprint has never mattered, their
  fingerprint is too weak. Sharpen it.

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
