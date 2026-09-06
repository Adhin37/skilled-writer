---
description: Create or update a character profile
argument-hint: "<name> [or: <name> — what changed]"
---

Work on a character.

Resolve the active novel, then invoke the `character-profile` skill — with `voice-separation` and
`competence-map` alongside it, which place this person on the two cast-wide tables. Do both
placements **before** writing the profile: a character designed in isolation comes out as quick, as
articulate and as wry as the MC, and able to answer any question, because the MC is the calibration
point and unlisted domains default to "probably fine".

**Decide the tier first.** Ask, or infer it from the plan, before writing anything:

| tier | who | what to write |
|---|---|---|
| A principal | MC, love interest, deuteragonist, arc antagonist | full file from `_character-template.md` |
| B supporting | recurs across an arc, no arc of their own | short file from `_supporting-template.md` |
| C walk-on | one to three scenes | one three-stroke line in `bible/cast/_extras.md` |

If the user asks for a full profile for someone who is clearly a walk-on, say so in one line, write
the roster line, and offer the promotion — do not silently spend 600 words on a shopkeeper.

Interpret `$ARGUMENTS`:

- a name with no existing record → assign the tier, then write it at that tier. Ask at most two
  questions about their role and their relationship to the MC; infer everything else from the
  bible, the arc plan and the premise, then show the user what you decided.
- an existing name → read the record, the growth row, and their recent CCS `chg>` entries; update
  what has changed. Append continuity facts, never overwrite them.
- a name plus a description of what changed → apply it, and decide explicitly whether it is a rung
  advance (record the trigger and the voice delta), a tier-B shift, a promotion, or a correction.
- `promote <name>` → build the profile at the next tier up **from what is already on the page**;
  everything they have already said and done is canon and constrains the result.
- empty → list the cast by tier — principals with rung, supporting with shift status, a count of
  walk-ons — and ask who to work on.

A **tier-A** profile must end with the voice axes, all eight speech-fingerprint fields filled,
three original calibration lines in three emotional states, at least two incompetences, and a
five-rung ladder with triggers and voice deltas. A **tier-B** file has ten fields and one shift,
and stays near 150 words. A **tier-C** line has three strokes, one off-default axis, and no
interiority.

Register tier-A and tier-B characters in `state/growth.md` (rung 1, or `B1`) and add their row to
`bible/cast/_voices.md`. Add every named character to `bible/lexicon.md`, at every tier.

Then run the three matrix checks in §2 of `_voices.md`: the cast straddles the MC's intel tier, at
most two characters have wit, and no two rows share intel + articulacy + wit. If the new character
collides with an existing one, change an axis or say plainly that the two should be merged.

Add their competence row to `bible/cast/_competence.md` too — domain, level, **where the edge is**,
and who they refer to outside it. Respect the budget above `professional` (3 MC · 2 tier A · 1 tier
B · 1 walk-on, which is their job), and treat every unlisted domain as `none`. If this character
closes a gap in §3 of that file, say so; if they open a new one, add it.

If this character is a **clone, avatar, double or body-snatch**, they are exempt from those checks
and instead get the `mirror:` block — source, kind, convergence level, and the chapter they became
separate people — plus a row in §5. Name the tell: the one thing that does not copy, and who could
notice it. `voice-separation/references/mirror-clause.md`.

Report: for tier A, the thumbnail, the want/need/fear/lie, the matrix row against the MC's, the
three calibration lines, and — if this is an antagonist — the two-sentence version of their case.
For tier B, the thumbnail, the want, the matrix row and the shift. For tier C, the line itself.
