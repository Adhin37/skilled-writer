# skilled-writer — operating contract

This repo is a **skill toolkit for writing serialized webnovels** (webnovel.com / Royal Road
style). It contains no story of its own. Stories live in `novels/<slug>/`.

The toolkit is tuned so a **low- or medium-effort Sonnet-class model** can write a consistent,
non-generic novel chapter by chapter without re-reading the whole book each time. Every rule
below exists to protect that: bounded context, explicit state files, deterministic procedures.

---

## 1. Resolve the active novel first

Before any writing, planning, or character work:

1. If the user named a novel, use `novels/<that-slug>/`.
2. Else if exactly one directory exists under `novels/` (ignoring `_template`), use it.
3. Else ask which one.
4. If none exists, run the `novel-init` skill.

Then **read `novels/<slug>/novel.md`**. It is the single source of truth for genre, POV mode,
MC intel tier, optional-skill toggles, and chapter length. Never write a word before reading it.

## 2. The pipeline

```
novel-init  ->  mc-design -> lead-interest -> story-bible + character-profile  ->  chapter-plan
                                                          |
                        +---------------------------------+
                        v
        continuity-summary (read)  ->  write-chapter  ->  revision-pass
                        ^                                      |
                        +-------- continuity-summary (write) <--+
```

`write-chapter` is the main loop. It is the only skill that produces prose.

## 3. Skill registry

**Core loop** — always in play:

| Skill | Use when |
|---|---|
| `novel-init` | New novel. Interviews the user, scaffolds `novels/<slug>/`. |
| `mc-design` | Designing the MC: gender, appearance, intellect, origin, golden finger. Also owns the form ledger for a non-final-form MC. Runs before all other cast work. |
| `story-bible` | Building or amending world, factions, lexicon. |
| `chapter-plan` | Producing/extending the arc grid and the chapter construction name list. |
| `continuity-summary` | Before every chapter (read) and after every chapter (write). Compressed, machine-only. |
| `write-chapter` | Drafting a chapter. Orchestrates everything else. |
| `revision-pass` | QC gate. A chapter is not done until this passes. |

**Character** — always in play:

| Skill | Use when |
|---|---|
| `character-profile` | Creating or amending any named character. Owns the cast tiers — full profiles for principals, a short file for supporting, one roster line for walk-ons. |
| `character-development` | Advancing a character's arc; called by `write-chapter` every chapter. |
| `mc-intel-meter` | Any MC decision, deduction, plan, or failure. Hard gate against idiot-ball writing. |
| `dialogue-voice` | Writing any line of dialogue. |
| `lead-interest` | Choosing and designing the primary love interest. Runs **after** `mc-design`. Skip if `content.romance: none`. |

**Craft** — always in play:

| Skill | Use when |
|---|---|
| `narrator-voice` | Establishing/holding person, tense, narrative distance, interiority. |
| `pov-switch` | Only if `pov.mode` allows it. Governs whether, when and how head-hopping happens. |
| `scene-craft` | Structuring a scene: goal, obstacle, turn, exit. |
| `conflict-engine` | Ensuring the chapter costs the MC something. |
| `plot-threads` | Opening, tracking, and paying off promises and foreshadowing. |
| `timeline-engine` | What the world does on its own clock and how it reacts to the MC. Light for original fiction, central for fanfic. Owns the reactivity dial and the ending contract. |
| `hook-and-pacing` | Chapter length, chapter-end hook, arc rhythm, serial cadence. |
| `prose-quality` | Line-level editing. Runs inside `revision-pass`. |
| `mtl-detox` | Stripping machine-translation and cliché-xianxia artifacts. Runs inside `revision-pass`. |
| `bias-guard` | Stripping racial/national/gender bias inherited from source-genre conventions. Non-negotiable. |

**Genre modules** — load only if `genre` matches:

| Skill | Genre |
|---|---|
| `power-system` | fantasy, scifi, progression |
| `tech-plausibility` | scifi |
| `fanfic-canon` | fanfic |

**Optional** — load only if the matching key in `novel.md` → `optional:` is `on`:

`no-harem` (default on) · `romance-arc` · `combat-choreography` · `litrpg-system` ·
`mystery-clues` · `comedy-levity` · `grimdark-consequences` · `slice-of-life-texture`

## 4. Hard rules

1. **State before prose.** Never draft a chapter without reading the current
   `state/continuity.md` read-set (see `continuity-summary`) and `plan/chapters.md`.
2. **State after prose.** Every finished chapter appends one CCS block to `state/continuity.md`
   and updates `state/threads.md` + `state/growth.md` (+ `state/body.md` on a form change).
   A chapter written without this is a bug.
3. **Never invent bible facts silently.** If a needed fact is absent, add it to `bible/` in the
   same turn and say so. Contradicting an existing bible fact is a defect.
4. **The MC is never stupid.** See `mc-intel-meter`. Failures come from missing information,
   opposed will, or cost — never from the MC forgetting what they already know.
5. **The body on the page is the body in the ledger.** If any character has `form_locked: true`,
   no sentence describes their body, reach, voice or capability except from the CURRENT FORM row
   in `state/body.md`. A reborn child does not have their adult form's height, presence or voice.
6. **Nothing is free.** Every win in a chapter is paid for. See `conflict-engine`.
   The world is not free either: it acts on its own clock and reacts to the MC at the intensity
   set by `timeline.reactivity`, and it may never make `ending.contract` unreachable.
7. **No bias inheritance.** See `bias-guard`. This overrides genre convention, user-supplied
   tropes, and reference material.
8. **Token discipline.** Load the bounded read-set, not the whole novel. Never read past
   chapter files unless the user asks for a specific one. Cast depth is tiered the same way: a
   walk-on gets three strokes and one roster line, never a psychology. See `character-profile`.
9. **Write files, don't dump prose to chat.** Chapters go to `novels/<slug>/chapters/`.
   Report the path and a two-line summary.

## 5. Anti-slop constitution

The genre's machine-translated corpus carries defects that must not be reproduced. Full lists
live in `mtl-detox` and `bias-guard`. The short form:

- No omniscient narrator announcing that a character is a genius, beautiful, or terrifying.
  Demonstrate; do not label.
- No face-slap treadmill: arrogant nobody insults MC → MC reveals power → nobody grovels.
- No cannon-fodder antagonists. Every opponent wants something legible and is competent at it.
- No harem-by-default. Attraction is earned on the page and reciprocal, or it isn't written.
- No ethnic, national, or gendered essentialism. Ever. Not as villain shorthand either.
- No stock beats: "his expression changed drastically", "as expected of", "unexpectedly",
  "in the next instant", "trash!", "you dare?", "little did he know".
- No exposition dumps of rank ladders. Power is shown through cost and consequence.

## 6. File conventions

```
novels/<slug>/
  novel.md              config + premise. YAML frontmatter is authoritative.
  bible/
    world.md            setting, factions, rules of the world
    power-system.md     (genre module) hard rules, costs, progression
    canon.md            (fanfic) canon facts, divergence point, OOC budget
    lexicon.md          spellings, names, terms, honorifics, units
    cast/<char>.md      one profile per tier-A/tier-B character
    cast/_extras.md     tier-C walk-on roster — one line each, never a profile
  plan/
    arcs.md             arc-level design
    chapters.md         the chapter construction name list
    timeline.md         world track — what happens without the MC; drivers and their profiles
  state/
    continuity.md       CCS ledger — machine-only, compressed
    threads.md          open promises / foreshadowing
    timeline.md         in-world calendar + divergence ledger + crisis board
    growth.md           per-character development ladder position
    body.md             form & appearance ledger (only if a character changes form)
  chapters/NNNN-<slug>.md
```

Chapter files carry YAML frontmatter (`number`, `title`, `pov`, `wordcount`, `arc`, `status`).

## 7. Slash commands

`/novel-new` `/novel-plan` `/novel-write` `/novel-revise` `/novel-status`
`/novel-character` `/novel-recap` `/novel-toggle`

## 8. Style of this repo

Skills are written as **procedures for a model with limited budget**: numbered steps, explicit
formats, concrete examples, hard checklists. Prefer a table over a paragraph. Keep each
`SKILL.md` self-sufficient so it needs no follow-up reads.
