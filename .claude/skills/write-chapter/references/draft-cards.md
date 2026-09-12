---
type: reference
owner: write-chapter
description: "Phase A, for anything the plan row does not already settle - why the cards are split from the bodies, and what to do when one does not settle its question"
---

# write-chapter — the draft cards

Opened by `write-chapter` Phase A, for anything the plan row does not already settle. If the row
in `plan/chapters.md` is complete, most of Phase A is transcription and most of this file stays
shut.

A **draft card decides**; an audit card checks. Open the card, not the owner's `SKILL.md`: a body
is a procedure for *designing* the thing, and Phase A is for deciding it. A card that does not
settle its question is the one case for opening its owner's `SKILL.md`; every card names the
section to open when that happens.

---

## Always

| decision | card |
|---|---|
| Which beat is played and which is reported | `story-craft/references/draft-card.md` — **first, always** |
| Scene count, the break, per-scene goal → obstacle → turn → exit | `scene-craft/references/draft-card.md`, `chapters.scenes_per_chapter` |
| What this chapter costs the POV character | `conflict-engine/references/draft-card.md` — never zero |
| POV character, and whether this is a switch | `pov-switch/references/draft-card.md` + the plan row |
| Which thread ops fire | `plot-threads/references/draft-card.md` |
| Who sounds different today, and how | `character-development/references/draft-card.md` → `state/growth.md` |
| **The voice spread** for this chapter's speakers | `voice-separation/references/draft-card.md` → `bible/cast/_voices.md` |
| Anyone new on the page: their **cast tier**, decided before they speak | `character-profile/references/draft-card.md` |
| **The offstage question** — what the world does this chapter that the MC does not know | `timeline-engine/references/draft-card.md` → `plan/timeline.md` |
| **The world channel** this chapter opens | `world-texture/references/draft-card.md` |
| What the MC deduces, and from which on-page clue | `mc-intel-meter/references/draft-card.md` |
| **Who has to ask** for what this chapter needs known | `competence-map/references/draft-card.md` → `bible/cast/_competence.md` |
| Opening line strategy, closing hook | `hook-and-pacing/references/draft-card.md` |

## Conditional — check the condition first, and skip the card entirely if it is false

| condition | decision | card |
|---|---|---|
| chapter ≤ `opening.contract_by_ch + 2` | **The anchor debt** and **the ceiling check** | `story-opening/references/draft-card.md` |
| `scaling.shape` is not `none` | **The pressure** — what gap between the MC and this chapter's opposition the arc wants, and only then who that opposition is | `power-scaling/references/draft-card.md` → `state/power.md` §6 |
| `mc.foreknowledge` is set | **The foreknowledge spend** | `meta-knowledge/references/draft-card.md` → `state/foreknowledge.md` |
| anyone is `form_locked` | Which bodies are locked, and what they cannot do today | `mc-design/references/draft-card.md` → `state/body.md` |

## The modules — a card each, not a body

An active module is consulted through **its draft card**, the same as anything else here. Opening
a module's `SKILL.md` mid-draft is the mistake this whole split exists to prevent: a body is a
procedure for designing the thing, and Phase A is for deciding it. Every module below is off for
most novels and costs nothing when it is; the read-set names the ones that are on.

| condition | decision | card |
|---|---|---|
| `genre`/`subgenre` is fantasy, scifi or progression | Which capability fires, and what it takes | `power-system/references/draft-card.md` |
| `genre`/`subgenre` is fanfic | Which canon fact this chapter touches | `fanfic-canon/references/draft-card.md` |
| `optional.combat-choreography` **and physical conflict** | The five decisions before a blow | `combat-choreography/references/draft-card.md` |
| `optional.battle-scale` **and an engagement above one fight** | Fronts, attrition, and what the POV can see | `battle-scale/references/draft-card.md` |
| `optional.litrpg-system` | Whether a screen fires, and what it may decide | `litrpg-system/references/draft-card.md` |
| `optional.mystery-clues` | The knowledge mode, and which clue moves | `mystery-clues/references/draft-card.md` |
| `optional.romance-arc` | Which romantic beat fires, or none | `romance-arc/references/draft-card.md` |
| `optional.grimdark-consequences` | What this chapter takes, and what is left to protect | `grimdark-consequences/references/draft-card.md` |
| `optional.slice-of-life-texture` | Which ordinary thing rides inside the scene | `slice-of-life-texture/references/draft-card.md` |
| `optional.comedy-levity` | Where the levity sits, and whose it is | `comedy-levity/references/draft-card.md` |

`tech-plausibility` and `no-harem` decide nothing at draft time and carry audit cards only —
`revision-pass` opens them.

---

## Why this file is separate

Benchmark run #2 opened nineteen cards before writing a word and held roughly thirty simultaneous
constraints through the draft. The chapters that came out were short, defensive and eventless —
a model spending its budget on not-failing has none left for deciding what happens. Splitting the
list out is not tidying: Phase A is meant to *spend* these and produce one brief, so that Phase B
drafts from the brief and four cards and nothing else.
