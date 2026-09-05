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

Recorded in `bible/cast/_extras.md`, one line:

```
Marek Oss — toll clerk, Ashfall east gate — ch 12, 19 — alive
  wants: to close early | tic: stamps twice, checks the second | carries: the gate levy doubled
  last month and nobody was told why
```

That is all of it. No thumbnail, no want/need/fear/lie, no competence table, no ladder, no
calibration lines, no growth row.

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

`_supporting-template.md`. Nine fields, and no more:

| field | note |
|---|---|
| thumbnail | one sentence, a stance toward the world, not a description |
| job in the story | why the story needs this person; if it is "explains things to the MC", redesign |
| want, this arc | concrete and pursuable in a scene |
| one incompetence | one is enough at this tier |
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
3. **Competence, with at least two incompetences.** Anything above `professional` requires a
   scene showing how it was acquired, scheduled or already written.
4. **Behaviour rules** — five to eight if/then rules, phrased so another writer could run them.
   These make the character predictable enough that breaking a rule reads as a *event*.
5. **Speech fingerprint** — all eight fields, plus three calibration lines in three emotional
   states. See `dialogue-voice`. This is the field most often skipped and most often regretted.
6. **Body & habit** — two or three behaviours, gestures rather than portraiture. Describe what
   the body *does*. No beauty catalogue. See `bias-guard`. If this character's body changes over
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
- Their competence is real and demonstrated before they lose anything.

A villain who exists to be defeated is a chore. A villain whose defeat costs the reader something
is the arc.

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
- [ ] Do they want something the MC's success would cost them?
- [ ] Do they have at least two incompetences?
- [ ] Is there something they are wrong about that they will not stop being wrong about soon?
- [ ] Have you avoided defining them by appearance, ethnicity, or their relationship to the MC?

**Tier B**

- [ ] Nine fields filled, none of them a paragraph
- [ ] Their one calibration line is not interchangeable with any principal's
- [ ] The shift names a trigger and a voice delta
- [ ] They want something for a reason that predates the MC

**Tier C**

- [ ] Three strokes, one line, no interiority
- [ ] Passes the swap test — stroke 3 is specific to them
- [ ] Named ones are in `lexicon.md`
- [ ] If they die soon, they were sketched in an earlier chapter and not inflated

`bias-guard` applies at every tier and is *most* often broken at tier C, where a person is one
detail wide and the default reaches for a stereotype to fill the space. A walk-on defined by an
accent, an ethnicity, a body, or a job-plus-nothing has failed the swap test as well as the bias
audit — the same stroke fixes both.
