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
novel-init -> mc-design -> lead-interest -> character-profile -----------+
                       \  [voice-separation] [competence-map]            |
                        +-> story-bible -> power-system|tech-plausibility|canon
                                                    -> social-fabric     |
                                                                         v
                                                                    chapter-plan
                                                                         |
                        +------------------------------------------------+
                        v
        continuity-summary (read)  ->  write-chapter  ->  revision-pass
                                    [voice-separation]   [pass 2: voices]
                                    [competence-map]     [pass 3: knowledge]
                                    [world-texture]      [pass 5: world]
                        ^                                      |
                        +-------- continuity-summary (write) <--+
```

**The world layer.** Three skills, three jobs, never mixed: `story-bible` records what is true and
where things are · `social-fabric` works out what the world's central rule (magic, tech, canon)
does to labour, money, law, knowledge, belief and mobility · `world-texture` decides how any of it
reaches the page, and at what budget. A fact is written once, in the right file, and delivered as
consequence.

**The character layer.** Three cast-wide tables, three questions, and all three are read as
*tables* because their defects are distributional and invisible one profile at a time.
`voice-separation` asks **who these people are as minds** — intelligence, articulacy, wit, heat,
turn length, body idiom — and holds them apart from the MC and from each other, with the mirror
clause exempting declared clones and doubles. `competence-map` asks **what they actually know** —
narrow domains with named edges, a referral for what lies outside, and a five-stage ladder for
skills acquired the slow way — with the broad-knowledge clause covering gods, immortals and
artificial minds. `dialogue-voice` then writes the lines. That order matters: eight fingerprint
fields painted onto minds that all reason at the protagonist's speed and answer every question
produce a cast of labelled clones, which is this format's second-most-common defect after a
stage-set world.

`write-chapter` is the main loop. It is the only skill that produces prose.

## 3. Skill registry

**Core loop** — always in play:

| Skill | Use when |
|---|---|
| `novel-init` | New novel. Interviews the user, scaffolds `novels/<slug>/`. |
| `mc-design` | Designing the MC: gender, appearance, intellect, origin, golden finger. Also owns the form ledger for a non-final-form MC. Runs before all other cast work. |
| `story-bible` | Building or amending world, factions, locations, lexicon. |
| `social-fabric` | The society layer — labour, money, law, knowledge, belief, mobility — and propagating the power/tech rule into ordinary life. |
| `world-texture` | Delivering the world on the page: consequence over description, sensory anchors, the description budget. Runs while drafting and inside `revision-pass`. |
| `chapter-plan` | Producing/extending the arc grid and the chapter construction name list. |
| `continuity-summary` | Before every chapter (read) and after every chapter (write). Compressed, machine-only. |
| `write-chapter` | Drafting a chapter. Orchestrates everything else. |
| `revision-pass` | QC gate, ten passes. A chapter is not done until this passes. |

**Character** — always in play:

| Skill | Use when |
|---|---|
| `character-profile` | Creating or amending any named character. Owns the cast tiers — full profiles for principals, a short file for supporting, one roster line for walk-ons. |
| `voice-separation` | Keeping every character distinct from the MC and from each other in speech, thought and body. Owns the cast voice matrix and the mirror clause for clones and doubles. |
| `competence-map` | Bounding what each character knows and can do — domains, edges, referrals — and running skill acquisition over chapters of failure. Owns the broad-knowledge clause for gods, immortals and ASI. |
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
   Corollary — **the world is delivered, not described.** Every world fact reaches the reader as
   a consequence, a friction or an assumed reference before it is ever reached as narration, and
   direct description is budgeted (`world-texture` §1–§2). A world whose central rule has not
   propagated into ordinary labour, money and law is a stage set (`social-fabric` §2).
4. **The MC is never stupid.** See `mc-intel-meter`. Failures come from missing information,
   opposed will, or cost — never from the MC forgetting what they already know.
   Corollary — **and nobody else is the MC.** Intelligence, articulacy and wit are per-character
   axes, declared in `bible/cast/_voices.md`; the cast straddles the MC's tier rather than sitting
   on it, at most two characters are funny, and no two speakers in a scene share intel +
   articulacy + wit (`voice-separation` §3). The one exemption is a declared `mirror:` — a clone,
   avatar, double or body-snatch may sound like the person they copy (§7).
   Corollary — **and nobody knows everything.** Being clever is not knowing things. Expertise is
   narrow, declared per domain in `bible/cast/_competence.md`, and **an unlisted domain is `none`**,
   never "probably fine". Every fact a character states passes the provenance test — taught, did,
   told, read, or openly guessing — and skills are acquired across chapters of failure, never by
   elapsed time (`competence-map` §1, §3, §5). The exemption is `knowledge_scope: broad` for gods,
   immortals, cultivators and artificial minds, who still need a declared shape, a declared
   boundary, and bounded *access* (§6).
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
- No establishing paragraphs, gazetteer sentences or history lectures. Enter scenes in motion;
  the world arrives inside the action or not at all.
- No wallpaper societies: if the world's central rule would have changed how people eat, work,
  travel or are judged, it has, and the story shows it.
- No cast of protagonists: allies, rivals, clerks and villains do not all reason at the MC's speed,
  argue as fluently, or land the same jokes. Somebody is slower, somebody is worse at saying it,
  and both are right about something.
- No universal experts. Nobody answers every question at the same confident depth; people are
  narrow, say so, ask someone, or are wrong. "I don't know" and "that's not my end" are strong
  lines, and a character who is confidently mistaken beats one who is conveniently informed.
- No instant mastery. A skill goes can't → fails knowingly → unreliable → competent → fluent, and
  it advances by a teacher, a text or a costly failure — never by chapters having passed.
- No default gesture set. Nodding, shrugging, sighing, raised eyebrows, crossed arms and released
  breaths belong to every character and identify none; a beat comes from that person's hands.

## 6. File conventions

```
novels/<slug>/
  novel.md              config + premise. YAML frontmatter is authoritative.
  bible/
    world.md            setting, locations + sensory signatures, factions, rules of the world
    society.md          labour, money, law, knowledge, belief, mobility; rule propagation
    power-system.md     (genre module) hard rules, costs, progression
    canon.md            (fanfic) canon facts, divergence point, OOC budget
    lexicon.md          spellings, names, terms, honorifics, units
    cast/<char>.md      one profile per tier-A/tier-B character
    cast/_voices.md     cast voice matrix — every speaker's axes in one table, plus mirrors
    cast/_competence.md who knows what, where the edge is, who they ask, what nobody knows
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

**One deliberate exception.** `revision-pass` is a dispatcher, and its condensed checklists must
never become a substitute for the skills they summarise. A pass whose defects are *distributional*
— `voice-separation`, `competence-map`, `bias-guard` — opens its source file every chapter. A
summary is enough to check a string; it is not enough to audit a cast. See `revision-pass`
§Before you start.
