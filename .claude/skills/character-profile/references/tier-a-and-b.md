# character-profile — the tier A and tier B procedures

Open this when actually writing a principal's or a supporting character's file. Tier C never needs it.

---

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
   set `knowledge_scope: broad` and fill the shape *and* the boundary (`competence-map/references/broad-knowledge.md`).
4. **Behaviour rules** — five to eight if/then rules, phrased so another writer could run them.
   These make the character predictable enough that breaking a rule reads as a *event*.
5. **Voice axes, then the speech fingerprint.** The axes first — intel, articulacy, wit and its
   trigger, heat, turn length, the conversational blind spot, and the thought fields if
   `pov_eligible` (`voice-separation` §1 and `voice-separation/references/channels.md`). Then all eight fingerprint fields and three
   calibration lines in three emotional states (`dialogue-voice`). In that order: eight surface
   habits laid over a mind identical to the MC's produce a labelled clone, which is the defect the
   axes exist to prevent. This is the step most often skipped and most often regretted.
6. **Body & habit** — the three body fields (`voice-separation/references/channels.md`): default state, **the hands**,
   and the pressure move — plus, for tier A, their habitual standing distance and what they do when
   someone crosses it. Gestures rather than portraiture; describe what the body *does*. Nothing
   from the default gesture set (`voice-separation` owns the list) — those identify nobody. No beauty catalogue; see `bias-guard`. If this character's body changes over
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
