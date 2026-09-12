# Coverage map

**What an agent needs in order to build a novel and then write it chapter by chapter, and where
each of those things lives.** One row per area of knowledge: the owner, the file that teaches it,
the card that spends it, and when it fires.

Provenance and maintenance only. Nothing here is loaded at runtime — same rule as
[craft-sources.md](craft-sources.md), for the same reason (benchmark finding 9: a file no
dispatcher names never enters context). The **runtime** answer to "what do I need for this
chapter" is `sw readset` and `sw kb`, and one goal of this map is that those two commands are now
complete enough that nothing is reachable only by somebody remembering it exists.

Built 2026-09-12, from a sweep that asked the opposite question to the usual one: not *is each
skill good* but *is there a subject with no owner at all*. Grepping the corpus for the obvious
candidates returned zero hits for emotional intelligence, "read the room", age-appropriate,
logistics, ecology and "group scene".

Corpus at the time of writing: **44 skills, 118 knowledge files — 30 draft cards, 32 audit cards,
56 references — 115 concepts.**

---

## How to read a row

| column | meaning |
|---|---|
| **area** | the thing an agent has to know |
| **owner** | the single skill that owns it. `sw kb owner <slug>` answers this at runtime |
| **taught in** | where the material actually is — a body section, or a `references/` file |
| **spent in** | the card that makes the decision (Phase A) or checks it (a pass). `—` means design-time only, and it is read during `novel-init` or an arc boundary rather than per chapter |
| **fires** | the trigger. `always` costs tokens on every chapter; everything else sits on the shelf |

---

## 1. Setting the novel up — once, at `novel-init`

| area | owner | taught in | spent in | fires |
|---|---|---|---|---|
| Premise interview, scaffold | `novel-init` | body · `references/scaffold.md` | — | once |
| Title, blurb, tags, slug | `title-craft` | body · `references/listing-kit.md` | — | once |
| The MC: intellect, origin, golden finger | `mc-design` | body · `references/form-ledger.md` | draft card | `form_locked` |
| The love interest, as a counterweight | `lead-interest` | body | — | `content.romance != none` |
| Person, tense, distance, the four channels | `narrator-voice` | body · `references/filtering.md` | draft card (B) · audit 10 | always |
| Whether the book switches viewpoint | `pov-switch` | body | draft card · audit 2 | `pov.mode != single` |
| What the first chapters owe the reader | `story-opening` | body · `references/chapter-one.md` | draft card · audit 9b | ch ≤ contract+2 |
| What the book argues, and the case against | `revision-pass` | `references/owned-passes.md` §9d | audit 9d | `theme` set |
| The ending contract, and what may never be taken | `timeline-engine` | body §The ending contract | `plot-threads`' card · audit 4 | always |

## 2. The world

| area | owner | taught in | spent in | fires |
|---|---|---|---|---|
| What is true, where things are, factions, names | `story-bible` | body | — | design |
| **Distances, travel time, what a map is for** | `story-bible` | `references/geography-and-travel.md` | — | *new* · the story moves |
| Labour, money, law, knowledge, belief, mobility | `social-fabric` | body §1 | — | design |
| Propagating the central rule into ordinary life | `social-fabric` | body §2 | — | design |
| **Prices, the anchor wage, debt as a deadline** | `social-fabric` | `references/prices-and-stakes.md` | — | *new* · money is a stake |
| **Religion, ritual, oaths, taboo** | `social-fabric` | `references/belief-and-ritual.md` | — | *new* · the story enters it |
| How gender is lived in this society | `social-fabric` | `references/gendered-experience.md` | — | design |
| How any of it reaches the page, at a budget | `world-texture` | body · `references/overbuilding.md` | draft card · audit 5 | always |
| Magic, cultivation, superhuman rules | `power-system` | body · **`references/system-design.md`** | **draft card · audit 5** | fantasy/scifi/progression |
| Technology, the one speculation, second-order effects | `tech-plausibility` | body | **audit 5** | scifi |
| Canon facts, the divergence point, the OOC budget | `fanfic-canon` | body · `references/canon-handling.md` | **draft card · audit 5** | fanfic |
| The world's own clock, and its reaction to the MC | `timeline-engine` | body · `references/reaction-and-governor.md` | `plot-threads`' cards · **audit 4** | always |

## 3. The cast

| area | owner | taught in | spent in | fires |
|---|---|---|---|---|
| Tiers, debut, the walk-on roster | `character-profile` | body · `references/tier-a-and-b.md` | `competence-map`'s draft card · audit 2 | always |
| Antagonists, mirrors, canon characters | `character-profile` | `references/special-cases.md` | — | as needed |
| **Non-human minds — beasts, constructs, gods** | `character-profile` | `references/nonhuman.md` | — | *new* · as needed |
| Distinctness as minds; the voice matrix | `voice-separation` | body · `references/worked-example.md` | draft card · audit 2 | always |
| **Children, adolescents, the old — cadence by age** | `voice-separation` | `references/age-register.md` | — | *new* · such a character exists |
| Clones, avatars, doubles | `voice-separation` | `references/mirror-clause.md` | — | a mirror exists |
| How intelligent, and how they fail | `mc-intel-meter` | body · `references/writing-intelligence.md` | draft card · audit 3 | always |
| **Plans, operations, deception on the page** | `mc-intel-meter` | `references/plans-and-lies.md` | — | *new* · a plan or a lie |
| **How well they read people; emotional signature; the misread** | **`social-perception`** | **body · `references/reading-people.md`** | **`mc-intel-meter`'s cards · audit 3b** | ***new* · always** |
| Who knows what, where the edge is, who they ask | `competence-map` | body · `references/broad-knowledge.md` | draft card · audit 3 | always |
| How a skill is actually acquired | `competence-map` | `references/acquisition-ladder.md` | — | a skill advances |
| Moving an arc, and the voice delta | `character-development` | body · `references/ladders.md` | `voice-separation`'s cards · **audit 2** | always |
| An MC who knows the future | `meta-knowledge` | body · `references/failure-modes.md` | draft card · audit 9c | `mc.foreknowledge` |
| Inherited bias — overrides everything | `bias-guard` | body | audit 6 | always, never rotated |

## 4. Planning

| area | owner | taught in | spent in | fires |
|---|---|---|---|---|
| The arc grid, the chapter list, `event`/`temp`/`hooktype` | `chapter-plan` | body · `references/titles-and-replanning.md` | — | every 8 chapters |
| Scene or summary, and building up before spending | `story-craft` | body · 4 references | draft card **(first, always)** · audit 9f | always |
| Promises: opened, escalated, paid, aged | `plot-threads` | body · `references/foreshadowing.md` | draft card · **audit 4** | always |
| **Twists and reveals outside a mystery** | `plot-threads` | `references/reveals-and-reversals.md` | — | *new* · a reversal |
| Stakes, cost, the antagonist standard | `conflict-engine` | body | draft card · **audit 4** | always |
| **Costs that persist — injury, exhaustion, aftermath** | `conflict-engine` | `references/aftermath.md` | — | *new* · something was taken |
| The gap between MC and opposition, over the book | `power-scaling` | body · 3 references | draft card · audit 9e | `scaling.shape != none` |
| Arc rhythm, temperature, release cadence | `hook-and-pacing` | body · `references/arc-rhythm.md` | draft card · **audit 9** | always |
| **The long middle — chapters 40 to 120** | `hook-and-pacing` | `references/the-long-middle.md` | — | *new* · arc boundary past arc 2 |

## 5. Drafting a chapter

| area | owner | taught in | spent in | fires |
|---|---|---|---|---|
| The three phases, the brief, the report | `write-chapter` | body · 3 references | — | always |
| The read-set, the CCS block, arc digests | `continuity-summary` | body · `references/block-format.md` | — | always |
| Goal, obstacle, turn, exit; the delivery test | `scene-craft` | body | draft card · audit 4+9 | always |
| **Three or more speakers in one scene** | `scene-craft` | `references/group-scenes.md` | — | *new* · 3+ speakers |
| Every line of dialogue; density and subtext | `dialogue-voice` | body · 3 references | draft card (B) · **audit 2** | always |
| Line-level editing, microtension, register range | `prose-quality` | body · `references/ai-default-tells.md` | audit 8 + 8b | always |
| MTL artifacts and structural cliché | `mtl-detox` | `references/catalogues.md` | audit 7 | always |
| A fight between people who can see each other | `combat-choreography` | body · **`references/duel-geography.md`** | **draft card · audit 4** | `optional` |
| **An engagement nobody can see the whole of** | **`battle-scale`** | **body · `references/logistics.md`** | **draft card · audit 4** | ***new* · `optional`** |
| A game-like system layer | `litrpg-system` | body | **draft card · audit 10** | `optional` |
| Fair-play clue mechanics | `mystery-clues` | body | **draft card · audit 3** | `optional` |
| Where the levity sits, and whose it is | `comedy-levity` | body | **draft card** | `optional` |
| Romantic beats across a serial | `romance-arc` | body | **draft card · audit 2** | `optional` |
| Love interests as people, not a collection | `no-harem` | body | **audit 6** | `optional`, on by default |
| Costs that stay paid | `grimdark-consequences` | body | **draft card · audit 9** | `optional` |
| Downtime, work, food, routine | `slice-of-life-texture` | body | **draft card** | `optional` |

## 6. The gate

`revision-pass` owns the pass order and the story gate. It carries no other skill's checklist: six
passes have no other owner and live in `references/owned-passes.md`; every other pass opens the
card of the skill that owns the defect. `sw kb passes` resolves the set against this novel,
modules included.

Bold rows above are what this pass added: **17 module cards, 7 audit cards for always-on skills
that had none, 2 new skills and 12 new references.**

**`social-perception` has no card of its own.** It was written with one and the card budget
took it the same day: its draft half sits on `mc-intel-meter`'s draft card and its audit half
is Pass 3b on `mc-intel-meter`'s audit card, each naming both owners ([creative-latitude.md](creative-latitude.md)
§What was built, item 6). The same merge moved `character-development` onto `voice-separation`'s cards,
`timeline-engine` onto `plot-threads`' and `character-profile` onto `competence-map`'s. A row here
names where a decision is *spent*, which after a merge is not the owner's own directory.

---

## What was deliberately not given an owner

So the next sweep does not re-litigate it.

- **A "worldbuilding" skill.** Three exist already with a clean split — `story-bible` records what
  is true, `social-fabric` works out what the central rule does to ordinary life, `world-texture`
  decides how any of it reaches the page. A fourth would have to take territory from all three.
- **An "emotion" skill separate from `social-perception`.** How a feeling is expressed and how it
  is read are the same problem, and splitting them produces two files that both describe a
  clenched jaw.
- **An economics module.** Prices belong to the society layer that already owns money; a separate
  skill would be a second place for the same facts to drift.
- **References for `romance-arc` and `litrpg-system`.** Both bodies are dense and now have cards.
  Adding a reference to satisfy a plan would be padding, which §8 exists to prevent.
- **Any new numeric gate.** The two new `sw cast` checks and everything in `sw lint` stay warns
  and notes that quote the text back. This repo has twice built a number that decided whether a
  chapter shipped — word count, then dialogue share — and both were optimised rather than
  satisfied. `docs/design-notes.md` §Why the scripts do not judge is the argument.
- **A lint check for a child's or an elderly character's register.** Detecting who is a child
  means guessing from a turn length or adding an axis to the voice matrix, and
  `voice-separation/references/age-register.md` states that age does not get an axis. A check
  that guesses is a number somebody writes toward. The group-scene note has no such problem —
  three speakers in a scene is a fact, not an inference — so that one exists.
- **Any addition to `CLAUDE.md` §5.** The seven commitments and ten bans are unchanged. That
  section's own history — a hundred prohibitions that a machine-written novel satisfied completely
  — is the reason expansion goes into knowledge and wiring rather than into more rules.

## Two things this pass had to fix on the way

- **`sw kb cards` could not reach its novel argument.** `args` is `nargs="*"` and `novel` is the
  `nargs="?"` behind it, so argparse gave the greedy one everything and the novel slot was never
  filled. It had always been broken and had never shown, because with exactly one novel in the
  repo `resolve(None)` picks it anyway. The second book breaks it — and this pass is what made
  those two commands load-bearing, so it is fixed in `sw.py` rather than left.
- **The audit-card triage table and the card-row disclaimer are now boilerplate.** Both are
  structure rather than advice, and `sw health`'s overlap detector was correctly flagging every
  new card against every other. They are cut out before comparison, kept to one canonical
  spelling each — a second accepted spelling of the same header is how the exemption becomes a
  hole.

## Still open

- **Trauma at novel scale.** `conflict-engine/references/aftermath.md` covers a cost persisting
  across chapters. A character changed permanently by what happened to them is
  `character-development`'s ladder, and the two have not been reconciled in one place.
- **Politics and negotiation as a scene type.** Partly covered — `social-fabric` has the
  institutions, `dialogue-voice` the subtext, `mc-intel-meter/references/plans-and-lies.md` the
  leverage — but nothing owns the shape of a negotiation scene the way `scene-craft` owns a scene.
- **Non-human POV.** `character-profile/references/nonhuman.md` builds one; `pov-switch` has not
  been asked whether one can narrate.
- ~~**The `eq` axis is unproven in a real run.**~~ **Settled by benchmark run #4.** Given only a
  premise and no mention of the axis, the writing agent set `mc.eq_tier` and filled `eq` for every
  cast row, with a real spread against `intel` (4/3/5/3/4 against 4/3/5/3/4) and a deliberate
  intel-5 / eq-1 antagonist. `sw cast` reports no `eq` finding of any kind. The axis reached the
  page because the **template** carries the slot — which is the general lesson, and why `sw health`
  now checks owner → template slot as well as config-key → owner.
