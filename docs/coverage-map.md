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

Corpus: **44 skills, 114 reference files — 26 draft cards, 29 audit cards, 59 others — 117
concepts.** `sw kb list` prints the live index and ends with those totals. `sw load` prints what
one chapter of a given novel actually resolves to, which is the number that matters and is always
smaller: a module that is off for this book costs nothing.

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
| **The rate those chapters promise — `pace-contract`** | `story-opening` | body §2 | draft card · audit 9b | *new* · ch ≤ contract+2 |
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
| **Whether it is handled or only felt — the mode, not the volume** | `world-texture` | body §1 · `references/narrative-space.md` | draft card · audit 5 | *new* · always |
| **Which world fact arrives in which of chapters 1–5** | `chapter-plan` | body §Arc 1 | `story-opening`'s cards | *new* · arc 1 |
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

**Three of the bold rows are later and are not in those counts** — the world pass of 2026-09-13,
which added no skill and no card: `world-texture`'s mode rule and its `narrative-space.md`,
`chapter-plan`'s world-entry column for chapters 1–5, and `story-opening`'s `pace-contract`, a
config slot rather than a check. Provenance: [craft-sources.md](craft-sources.md) §The second pass.

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
- **A lint check for narrative space.** The atmosphere failure — a world that is vivid, inside
  every budget, and never handled — is measured and real, and it stays a craft default carried by
  `world-texture/references/narrative-space.md` and one box on each of two cards. Separating action
  space from perceived space took the source paper fine-tuned classifiers at macro-F1 0.82. A
  regex over mood words would be inferring, which is the same objection as the bullet above, and a
  chapter would be edited to beat it. The handled-noun test is a question a person answers.
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

- **One-sided rules.** A rule stated as a range or a positive requirement, where only the
  violation-by-excess is detectable and the violation-by-absence is invisible. The pattern is named
  in `mc-design/references/form-ledger.md` rule 9 and is worth re-running against any new rule that
  states a range. **Swept again on 2026-09-13** — results below.

- ~~**Trauma at novel scale.**~~ **Closed 2026-09-13.** `character-development` owns
  `lasting-harm`; `conflict-engine/references/aftermath.md`'s *permanently* row hands off to it
  instead of stopping at continuity facts, and `state/growth.md` carries the column.
- ~~**Politics and negotiation as a scene type.**~~ **Closed 2026-09-13.**
  `scene-craft/references/negotiation.md`, a scene type under `scene-craft` with no slug of its
  own, on the `group-scenes.md` precedent.
- ~~**Non-human POV.**~~ **Closed 2026-09-13.** `pov-switch` §Non-human viewpoints answers
  eligibility and what the four channels mean for a mind without language.

### The one-sided-rule sweep, 2026-09-13

Method: every stated range, floor or positive requirement in the corpus, against the one question
— **does anything count this in aggregate?** Recorded in full so the next sweep starts here.

**Found and closed: the divergence ledger's own arc rule.** `state/timeline.md` carries the line
verbatim — *every arc must contain at least one row that is not `unchanged`* — and **no script read
the table at all**; the only mention of it anywhere in `scripts/` was a `readset` comment excluding
it from the read-set. It is the shape at its purest: a divergence row is only ever wrong by *saying*
something, so an empty ledger cleared every check in the repo. Both live novels were running that
way at six chapters with `sw audit` reporting 0 defects, one of them while declaring
`timeline.reactivity: 4`. Closed by `_divergence` in `cmd_arc.py` (`arc-divergence`), with
`novelio.divergence_rows()` registered in `TABLE_ACCESSORS` so the template cannot drift the columns
out from under it silently — the failure `plan_rows()` already had once.

It is a **warn**, never a defect, and it lives in `sw arc` rather than `sw audit` because it is an
*arc* rule and `audit` has no arc to evaluate it against. An MC who genuinely changed nothing this
arc is legitimate — a siege, a confinement, a stretch spent learning — and the point of the check is
that this becomes a stated decision rather than an empty table nobody looked at.

**Checked and found fine — do not re-litigate:**

| rule | why it is covered |
|---|---|
| `'…'` direct thought 1–3 | floor is a note and sits in `rules.HABIT_NOTE_CHECKS`; ceiling is a defect |
| speech share 25–40% | `SPEECH_FLOOR` defect below 10%, warn below 25%, warn above 40% |
| temperature / hooktype | `TEMP_RUN_MAX` and `HOOK_WINDOW_MAX` cap repeats, `ARC_MIN_DISTINCT` is the floor |
| the 45-word dialogue turn | CLAUDE.md allows one chapter in five; `texture` is a habit note and the WATCH row fires at two in five, so the allowance *is* the check |
| threads closed per arc | `arc-payoff`, with the drafting-position rule so an unfinished arc is a note |
| foreknowledge spent | `arc-foreknowledge` warns when an arc spends none |
| `wld>` presence | `sw state` warns on a block that omits it |
| CCS block keys | every key in `block-format.md` is read by at least one script; no orphans |

**Left alone, with reasons:** `set>` facts (checked, fine) · `world-texture`'s non-visual detail and
the plain-sentence third (deliberately unscripted — `textstats.py` documents why shape cannot see
the third) · em-dash, house-style and closer rates (ceilings only, and a floor would be meaningless).

**Found, not closed.** Two, both raised by the steps immediately before this sweep:

- **The inverse shape: a check that fires where the rule does not apply.** A non-linguistic POV
  chapter (`pov-switch` §Non-human viewpoints) trips `thought-budget`'s floor and drags
  `speech-share` down, both correct about the numbers and wrong about the chapter. `thought-budget`
  is in `HABIT_NOTE_CHECKS`, so a run of such chapters reaches the WATCH row and tells the next
  draft to open a channel that character cannot have. The existing suppressor,
  `narration.interiority: low`, is novel-level and too coarse — the same novel's human POV chapters
  should still be checked. The fact needed to scope it is already on disk: `pov-switch` requires a
  declared thought unit per POV character in `bible/cast/_voices.md` §3, so lint could read it
  rather than gaining a new config key. Resolved in prose for now — the channel is *declared shut*
  and the `Gate:` line says so — which is correct but manual.
- ~~**`sw health`'s overlap detector versus a shared section form.**~~ **Closed 2026-09-13**, and
  half of it deliberately left alone. The heading *Where this is not the right file* plus the table
  header `| the case | the owner |` yielded exactly three shared 10-word runs against `OVERLAP_MAX`
  of 2, so two skills adopting both warned on boilerplate rather than on copied advice — which is
  what happened between `character-development` and `scene-craft` while this plan was being written.
  **Only the heading is now in `BOILERPLATE`.** It is a genuine convention: three references carry
  it, and *cite the owner and stop* is a rule rather than a style, so more will. The column header
  is not — exactly one file uses it, `aftermath.md` writes the same section as prose, and exempting
  a two-word-pair header on one file's evidence is precisely how the tuple grows into the hole its
  own comment warns about. The section under the heading is free to be a table or a paragraph, and
  its columns are free to say something; `negotiation.md`'s read *what you are actually writing* /
  *whose rule it is*, which is better than *the case* / *the owner* and cost nothing to keep.

- ~~**The `eq` axis is unproven in a real run.**~~ **Settled by benchmark run #4.** Given only a
  premise and no mention of the axis, the writing agent set `mc.eq_tier` and filled `eq` for every
  cast row, with a real spread against `intel` (4/3/5/3/4 against 4/3/5/3/4) and a deliberate
  intel-5 / eq-1 antagonist. `sw cast` reports no `eq` finding of any kind. The axis reached the
  page because the **template** carries the slot — which is the general lesson, and why `sw health`
  now checks owner → template slot as well as config-key → owner.
