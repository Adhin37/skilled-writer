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
     |                 \  [meta-knowledge] [voice-separation]            |
     |                  \  [competence-map]                              |
     |                  +-> story-bible -> power-system|tech-plausibility|canon
     |                                              -> social-fabric     |
     +-> title-craft -> [scaffold]                                       |
         (title, blurb, slug)                                            v
                                                        story-opening -> chapter-plan
                                                                         |
                        +------------------------------------------------+
                        v
        continuity-summary (read)  ->  write-chapter  ->  revision-pass
                                    [voice-separation]   [pass 2: voices]
                                    [competence-map]     [pass 3: knowledge]
                                    [world-texture]      [pass 5: world]
                                    [narrator-voice]     [pass 9: DELIVERY]
                                    [story-opening]      [pass 9b: opening]
                                    [meta-knowledge]     [pass 9c: foreknowledge]
                        ^                                      |
                        +-------- continuity-summary (write) <--+
```

**The gate is delivery, not length.** A chapter passes `revision-pass` Pass 9 on five questions —
want, friction, **change**, cost, next — and never on its word count. `chapters.length_band` is a
printer's note. Every prior attempt to gate on length was gamed: chapters clustered on the floor,
then on the tolerance, then landed on the declared minimum to the word.

**The shelf comes before the page.** `title-craft` runs once, at the end of the `novel-init`
interview and before the scaffold, and owns the two things every reader sees *before* chapter 1
exists for them: the **title** and the **platform blurb**. It generates five candidates across
five distinct strategies rather than five rewordings of one, screens them on truncation,
collision, promise-match and whether the name survives to chapter 100, and for fan fiction puts
the source work in the title line — `Naruto: The New God of Shinobi` — because fanfic is browsed
by fandom and a title without it is invisible. The slug is derived here and is **permanent**; the
title is not.

**The opening is its own problem.** `story-opening` owns chapters 1 through
`opening.contract_by_ch + 2`, because chapter 1 is a conversion event — about 60% of readers who
open it reach chapter 2, and from chapter 5 retention runs 80%+. It enforces the world anchor, the
genre contract, the promise ledger, and the ceiling that stops escalation outrunning the reader's
ability to price it.

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

**Foreknowledge.** `meta-knowledge` owns any MC who knows what happens next — self-inserts,
transmigrators into a novel, regressors, reincarnators. It exists because the mechanic fails in
two opposite directions and careful writing picks the second: the oracle whose knowledge is free
and accurate, and the handicap that is introduced already-unreliable and only ever malfunctions.
The order is fixed — **it works, then it costs, then it frays, then it betrays** — and decay is a
consequence the MC caused by acting, not a decree scheduled at a chapter number.

**Text channels.** `narrator-voice` owns four and holds them apart: `"…"` speech · `'…'` direct
thought, budgeted at 1–3 a chapter · `[…]` system interfaces and in-world documents · and
**unmarked free indirect discourse, which is where interiority actually lives**. The budget is the
point. Marked thought is emphatic because it is rare; a chapter that marks every interior beat has
turned its narrator into a thought bubble.

`write-chapter` is the main loop. It is the only skill that produces prose.

## 3. Skill registry

**Core loop** — always in play:

| Skill | Use when |
|---|---|
| `novel-init` | New novel. Interviews the user, scaffolds `novels/<slug>/`. |
| `title-craft` | Naming the book and writing the platform blurb. Once, inside `novel-init`, before the scaffold — the slug comes from the title. Owns the fanfic source-in-title rule. |
| `mc-design` | Designing the MC: gender, appearance, intellect, origin, golden finger. Also owns the form ledger for a non-final-form MC. Runs before all other cast work. |
| `story-bible` | Building or amending world, factions, locations, lexicon. |
| `social-fabric` | The society layer — labour, money, law, knowledge, belief, mobility — and propagating the power/tech rule into ordinary life. |
| `world-texture` | Delivering the world on the page: consequence over description, sensory anchors, the description budget. Runs while drafting and inside `revision-pass`. |
| `story-opening` | Chapters 1 to `opening.contract_by_ch + 2` — the world anchor, the genre contract, the promise ledger, and the stakes ceiling. |
| `chapter-plan` | Producing/extending the arc grid and the chapter construction name list. |
| `continuity-summary` | Before every chapter (read) and after every chapter (write). Compressed, machine-only. |
| `write-chapter` | Drafting a chapter. Orchestrates everything else. |
| `revision-pass` | QC gate. A chapter is not done until this passes. |

**Character** — always in play:

| Skill | Use when |
|---|---|
| `character-profile` | Creating or amending any named character. Owns the cast tiers — full profiles for principals, a short file for supporting, one roster line for walk-ons. |
| `voice-separation` | Keeping every character distinct from the MC and from each other in speech, thought and body. Owns the cast voice matrix and the mirror clause for clones and doubles. |
| `competence-map` | Bounding what each character knows and can do — domains, edges, referrals — and running skill acquisition over chapters of failure. Owns the broad-knowledge clause for gods, immortals and ASI. |
| `character-development` | Advancing a character's arc; called by `write-chapter` every chapter. |
| `meta-knowledge` | Any MC who knows the future — grain, the inventory scene, win-before-failure, the observer paradox. Owns `state/foreknowledge.md`. |
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
4. **A chapter is judged by what it delivers, not its length.** `revision-pass` Pass 9 —
   want, friction, **change**, cost, next — and `change` names a difference, not a summary of
   events. `chapters.length_band` is a printer's note; nothing gates on it, nothing is padded or
   trimmed to reach it. Every length gate this repo has tried was optimised into the prose within
   five chapters. A word count is a **measured fact, reported and never scored** — `sw.py` prints
   one and `hook-and-pacing` reads one as a diagnosis; neither may decide whether a chapter ships.
5. **The reader is oriented before they are threatened.** By `opening.anchor_by_ch` a reader knows
   what kind of world this is, what kind of place they are in, what the MC wants — and for fanfic
   or transmigration, **which story they are in and roughly when**. Anchor vocabulary is
   front-loaded, never saved: a first arc with zero canon or setting nouns is a bug, not a slow
   burn. And **a consequence may not escalate past the reader's ability to price it** — before a
   threat is dangerous, the mechanism must be on the page, not in the bible (`story-opening`).
6. **Foreknowledge works before it fails.** If the MC knows the future, it is declared at a grain,
   inventoried in `state/foreknowledge.md`, spent on the page with a cost, and it lands one
   legible win before its first failure — `foreknowledge_first_win_ch` < `foreknowledge_fails_ch`.
   It decays because the MC acted, not because a chapter number arrived. An MC who never refers to
   knowing what is coming has wasted the premise; one whose knowledge only ever malfunctions has
   sold the reader something the blurb did not describe (`meta-knowledge`).
7. **Four channels, held apart.** `"…"` speech · `'…'` direct thought, 1–3 per chapter, POV
   character only · `[…]` meta · unmarked free indirect discourse as the default carrier of
   interiority. An apostrophe is not a thought mark; a `'…'` inside a `"…"` is a nested quotation.
   Nothing else in a prose body is markup (`narrator-voice`).
8. **The MC is never stupid.** See `mc-intel-meter`. Failures come from missing information,
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
9. **The body on the page is the body in the ledger.** If any character has `form_locked: true`,
   no sentence describes their body, reach, voice or capability except from the CURRENT FORM row
   in `state/body.md`. A reborn child does not have their adult form's height, presence or voice.
10. **Nothing is free.** Every win in a chapter is paid for. See `conflict-engine`.
   The world is not free either: it acts on its own clock and reacts to the MC at the intensity
   set by `timeline.reactivity`, and it may never make `ending.contract` unreachable.
11. **No bias inheritance.** See `bias-guard`. This overrides genre convention, user-supplied
   tropes, and reference material.
12. **Token discipline.** Load the bounded read-set, not the whole novel. Never read past
   chapter files unless the user asks for a specific one. Cast depth is tiered the same way: a
   walk-on gets three strokes and one roster line, never a psychology. See `character-profile`.
   The read-set is specified as **slices** — this chapter's speakers, this chapter's locations,
   blocks N−5…N−1 — and `python3 scripts/sw.py readset novels/<slug> -c <N>` emits exactly those.
   Reading the whole file instead is how a bounded read-set turns into a ledger that grows
   forever. See §9.
13. **Write files, don't dump prose to chat.** Chapters go to `novels/<slug>/chapters/`.
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
- No unanchored openings: five chapters in which a reader cannot say what kind of world this is,
  or which canon they are standing in, is not mystery — it is disorientation, and it is
  indistinguishable from the feeling of reading something bad.
- No escalation past the reader's ability to price it. A threat whose mechanism has never been on
  the page reads as somebody being strict, however well the beat is written.
- No foreknowledge that only ever fails, and none that never appears. An MC who knows the future
  makes a plan — an adequate one, from incomplete information — and the reader watches it work
  before they watch it break.
- No noun-stack titles. *Shadow Blade Chronicles: Legacy of the Eternal Flame* is four hundred
  other books; strip the filler and name what is actually on offer. And no fanfic title that omits
  the source work — it is the search term the entire audience uses.
- No chapter padded, trimmed, or shipped because of its length.
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
  novel.md              config + premise + blurb. YAML frontmatter is authoritative.
                        `title` may change at an arc boundary; `slug` never does.
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
    foreknowledge.md    grain, inventory, spend log, observer paradox (only if the MC knows the future)
  chapters/NNNN-<slug>.md
```

Chapter files carry YAML frontmatter (`number`, `title`, `pov`, `arc`, `delivers`, `wordcount`,
`status`). **`delivers`** is what is materially different at the end, in one clause — the Pass 9
gate. `wordcount` is a measured fact that later tools read, never a target.

## 7. Slash commands

`/novel-new` `/novel-plan` `/novel-write` `/novel-revise` `/novel-status`
`/novel-character` `/novel-recap` `/novel-toggle`

## 8. Style of this repo

Skills are written as **procedures for a model with limited budget**: numbered steps, explicit
formats, concrete examples, hard checklists. Prefer a table over a paragraph.

**Cite sections, never line numbers.** `hook-and-pacing` §Openings survives an edit;
`hook-and-pacing:38-39` rots the moment a paragraph is added above it, and rots silently — the
citation still resolves, to the wrong text.

**One deliberate exception to self-sufficiency.** `revision-pass` is a dispatcher, and its condensed checklists must
never become a substitute for the skills they summarise. A pass whose defects are *distributional*
— `voice-separation`, `competence-map`, `bias-guard` — opens its source file every chapter. A
summary is enough to check a string; it is not enough to audit a cast. Two more open
conditionally: `story-opening` while the novel is inside its opening arc, and `meta-knowledge`
whenever the MC knows the future. Both guard defects that are invisible in a single chapter and
unrecoverable once ten are written — *is the reader oriented?* and *has the advantage ever won?*
are questions no checklist can answer. See `revision-pass` §Before you start.

---

## 9. The mechanical toolkit

`scripts/sw.py` does the countable work: slicing the read-set, sweeping a chapter for banned
strings and channel mechanics, auditing the cast tables as tables, checking the ledger against
the chapters, and stamping a measured word count. **Python 3.8+, standard library only.** Full
reference in [scripts/README.md](scripts/README.md).

| command | use it in |
|---|---|
| `readset <novel> -c N` | `continuity-summary` read mode · `write-chapter` step 0 |
| `lint <novel> -c N` | `revision-pass` Pass 0 · `mtl-detox` · `prose-quality` · `narrator-voice` · `story-opening` |
| `cast <novel>` | `voice-separation` §3, §6 · `competence-map` §7 · `novel-init` step 5b |
| `state <novel>` | `continuity-summary` self-check · `plot-threads` · `chapter-plan` · `character-profile` |
| `status <novel>` | `/novel-status` |
| `stamp <novel> -c N` | `revision-pass` Pass 10 · `write-chapter` step 4 |
| `newnovel <slug>` | `novel-init` step 3 |
| `audit <novel>` | the independent whole-novel gate |
| `doctor` | start here when anything behaves oddly — Python version, repo root, novels found |

Three rules govern how they are used, and all three exist to stop a tool becoming an alibi:

1. **An optimisation, never a dependency.** Every skill that names a command keeps its manual
   checklist directly underneath. If Python is absent or the command errors, do the checks by
   reading and **say so in the report** — a ticked box that was never checked is worse than an
   unticked one.
2. **They find, they do not judge.** A linter locates a string; whether that string is a defect
   is a decision. Nothing here rewrites a prose body, because `mtl-detox` requires the sentence
   rewritten rather than the synonym swapped, and an auto-fixer would do exactly the forbidden
   thing. The only files they edit are frontmatter, the `wc:` field of a CCS block, and a fresh
   scaffold.
3. **A clean run is not a passed revision.** It means the mechanical passes found nothing. The
   distributional ones — `voice-separation`, `competence-map`, `bias-guard` — and the judgement
   ones — delivery, world, opening — are untouched by it. `bias-guard` has no script at all,
   deliberately, so that no green line can ever be mistaken for a bias pass.
