# skilled-writer — operating contract

A **skill toolkit for writing serialized webnovels** (webnovel.com / Royal Road style). It
contains no story of its own. Stories live in `novels/<slug>/`.

Tuned so a **low- or medium-effort Sonnet-class model** can write a consistent, non-generic novel
chapter by chapter without re-reading the whole book. Every rule here protects that: bounded
context, explicit state files, deterministic procedures. The arguments behind the rules live in
[docs/design-notes.md](docs/design-notes.md) — read that when editing the toolkit, not when
writing a chapter.

---

## 1. Resolve the active novel first

1. If the user named a novel, use `novels/<that-slug>/`.
2. Else if exactly one directory exists under `novels/` (ignoring `_template`), use it.
3. Else ask which one.
4. If none exists, run `novel-init`.

Then **read `novels/<slug>/novel.md`**. It is the single source of truth for genre, POV mode, MC
intel tier, channels, and optional-skill toggles. Never write a word before reading it.

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
                                    [power-scaling]      [pass 9e: the curve]
                                    [voice-separation]   [pass 2: voices]
                                    [competence-map]     [pass 3: knowledge]
                                    [world-texture]      [pass 5: world]
                                    [narrator-voice]     [pass 9: DELIVERY]
                                    [story-opening]      [pass 9b: opening]
                                    [meta-knowledge]     [pass 9c: foreknowledge]
                        ^                                      |
                        +-------- continuity-summary (write) <--+
```

`write-chapter` is the main loop and the only skill that produces prose. Two orderings are
load-bearing: `title-craft` before the scaffold, because the slug comes from the title and is
permanent; and minds → knowledge → lines in the character layer, because eight fingerprint fields
painted onto minds that all reason at the MC's speed produce a cast of labelled clones.

## 3. Skill registry

Every skill is `.claude/skills/<name>/SKILL.md` plus a `references/` directory. The body is the
procedure; the references hold examples, catalogues and long tables, and are opened when the body
says to. See §8.

**Core loop** — always in play:

| Skill | Use when |
|---|---|
| `novel-init` | New novel. Interview, then scaffold. |
| `title-craft` | Title, platform blurb, tags, cadence, slug. Once, inside `novel-init`. |
| `mc-design` | Designing the MC, and the form ledger for a non-final-form MC. Before all other cast work. |
| `story-bible` | World, factions, locations, lexicon. |
| `social-fabric` | Labour, money, law, knowledge, belief, mobility; propagating the central rule. |
| `world-texture` | Delivering the world on the page. Owns the description and sensory budget. |
| `story-opening` | Chapters 1 to `opening.contract_by_ch + 2`. Anchor, contract, promise, ceiling. |
| `chapter-plan` | The arc grid and the chapter construction list. |
| `continuity-summary` | Before every chapter (read) and after every chapter (write). |
| `write-chapter` | Drafting. Orchestrates everything else. |
| `revision-pass` | QC gate. A chapter is not done until this passes. |

**Character** — always in play:

| Skill | Use when |
|---|---|
| `character-profile` | Any named character. Owns the cast tiers. |
| `voice-separation` | Keeping the cast distinct as minds. Owns the voice matrix and the mirror clause. |
| `competence-map` | What each character knows, where the edge is, who they ask. Owns the broad-knowledge clause. |
| `character-development` | Advancing an arc. Every chapter. |
| `meta-knowledge` | Any MC who knows the future. Owns `state/foreknowledge.md`. |
| `mc-intel-meter` | Any MC decision, deduction, plan or failure. |
| `dialogue-voice` | Any line of dialogue. Owns dialogue density and subtext. |
| `lead-interest` | The primary love interest, after `mc-design`. Skip if `content.romance: none`. |

**Craft** — always in play:

| Skill | Use when |
|---|---|
| `narrator-voice` | Person, tense, distance, interiority, the four channels. |
| `pov-switch` | Only if `pov.mode` allows it. |
| `scene-craft` | Goal, obstacle, turn, exit — and the chapter delivery test. |
| `conflict-engine` | Making the chapter cost something. Owns the stake ladder. |
| `power-scaling` | The distance between the MC and the opposition, and its shape over the whole book. Owns `state/power.md`. |
| `plot-threads` | Promises and foreshadowing: opened, escalated, paid, aged. |
| `timeline-engine` | The world's own clock and its reaction to the MC. Owns the ending contract. |
| `hook-and-pacing` | Openings, hooks, arc rhythm, release cadence. |
| `prose-quality` | Line-level editing, and microtension. Inside `revision-pass`. |
| `mtl-detox` | Machine-translation and cliché-xianxia artifacts. Inside `revision-pass`. |
| `bias-guard` | Inherited bias. Non-negotiable. |

**Genre modules** — only if `genre` matches: `power-system` (fantasy · scifi · progression) ·
`tech-plausibility` (scifi) · `fanfic-canon` (fanfic).

**Optional** — only if the matching `optional:` key in `novel.md` is `on`: `no-harem` (default on)
· `romance-arc` · `combat-choreography` · `litrpg-system` · `mystery-clues` · `comedy-levity` ·
`grimdark-consequences` · `slice-of-life-texture`.

## 4. Hard rules

1. **State before prose.** Never draft without the current read-set and `plan/chapters.md`.
   `python3 scripts/sw.py readset novels/<slug> -c <N>` assembles all of it in one call — config,
   the **active modules** for this novel with the file to open for each, digests, blocks N−5…N−1,
   plan rows N−1…N+2, open threads, and the cast rows for this chapter's speakers. It is the whole
   read-set: do not open the source files for anything it contains, and a module it does not list
   is off for this novel.
2. **State after prose.** Every finished chapter appends one CCS block to `state/continuity.md`
   and updates `state/threads.md` and `state/growth.md`, plus `state/body.md` on a form change.
   A chapter written without this is a bug.
3. **Never invent bible facts silently.** If a needed fact is absent, add it to `bible/` in the
   same turn and say so. Contradicting an existing bible fact is a defect.
   Corollary — **the world is delivered, not described.** Every world fact reaches the reader as a
   consequence, a friction or an assumed reference before it is reached as narration, and direct
   description is budgeted (`world-texture`). A world whose central rule has not reached ordinary
   labour, money and law is a stage set (`social-fabric`).
4. **A chapter is judged by what it delivers, not its length.** `revision-pass` Pass 9 — want,
   friction, **change**, cost, next — and `change` names a difference, not a summary of events.
   Nothing gates on `chapters.length_band`; nothing is padded or trimmed to reach it. A word count
   is a measured fact, reported and never scored.
5. **The reader is oriented before they are threatened.** By `opening.anchor_by_ch` a reader knows
   what kind of world this is, what place they are in, what the MC wants — and for fanfic or
   transmigration, **which story they are in and roughly when**. Anchor vocabulary is front-loaded,
   never saved. And **a consequence may not escalate past the reader's ability to price it**: the
   mechanism is on the page before the threat is dangerous (`story-opening`).
6. **Foreknowledge works before it fails.** Declared at a grain, inventoried in
   `state/foreknowledge.md`, spent on the page with a cost, and it lands one legible win before its
   first failure — `foreknowledge_first_win_ch` < `foreknowledge_fails_ch`. It decays because the
   MC acted, not because a chapter number arrived (`meta-knowledge`).
7. **Four channels, held apart.** `"…"` speech · `'…'` direct thought, 1–3 per chapter, POV
   character only · `[…]` meta · unmarked free indirect discourse as the default carrier of
   interiority. The marks come from `channels:` in `novel.md`. An apostrophe is not a thought mark;
   a `'…'` inside a `"…"` is a nested quotation. Nothing else in a prose body is markup
   (`narrator-voice`).
8. **The MC is never stupid.** Failures come from missing information, opposed will, or cost —
   never from the MC forgetting what they already know (`mc-intel-meter`).
   Corollary — **and nobody else is the MC.** Intel, articulacy and wit are per-character axes in
   `bible/cast/_voices.md`. The cast straddles the MC's tier rather than sitting on it, and no two
   speakers in a scene share all three — nor **intel and articulacy together**, which are the two
   that shape a sentence. Wit is a label and can go a whole chapter without surfacing, so a pair
   alike but for wit is one voice on the page. Exemption: a declared `mirror:`
   (`voice-separation`).
   Corollary — **and every named character is placed before they carry a scene.** A tier-A or
   tier-B character's first appearance gives the reader their relation to the POV character, what
   power they hold, and one concrete stroke — in motion, not as a caption. Subtext between people
   the reader cannot yet tell apart reads as confusion (`character-profile`).
   Corollary — **and nobody knows everything.** Expertise is narrow, declared per domain in
   `bible/cast/_competence.md`, and **an unlisted domain is `none`**. Every stated fact passes the
   provenance test — taught, did, told, read, or openly guessing — and skills are acquired across
   chapters of failure, never by elapsed time. Exemption: `knowledge_scope: broad`, which still
   needs a declared shape and boundary (`competence-map`).
9. **The body on the page is the body in the ledger.** If any character is `form_locked`, no
   sentence describes their body, reach, voice or capability except from the CURRENT FORM row in
   `state/body.md`.
10. **Nothing is free.** Every win is paid for (`conflict-engine`). The world is not free either:
    it acts on its own clock at the intensity set by `timeline.reactivity`, and it may never make
    `ending.contract` unreachable.
11. **The curve is the gap, not the magnitude.** Reader interest tracks the distance between the
    MC and the opposition — **pressure** — never the MC's absolute tier. A permanent gain is **+1
    tier** and carries a source with its own interests, a price paid before it lands, a setup
    `scaling.setup_lead` chapters back, and a new problem. A **boost** is temporary reach with a
    declared expiry and a debt that comes due, and may resolve an arc climax **once per novel**.
    The golden finger closes a gap of **at most one tier**, at a stated price. An MC who starts at
    the top declares `shape: inverted` and what the story runs on instead (`power-scaling`).
12. **Every arc pays something.** An arc closes at least one thread on the page, and a thread open
    past its horizon is escalated, paid, or deferred with a stated reason. Perpetual deferral is
    the most common complaint about long serials (`plot-threads`).
13. **The theme is dramatized, never narrated.** `theme.controlling_idea` is what the story argues;
    `theme.counter_case` is the argument against it that a character gets to make and win with at
    least once. The narrator never states the lesson (`revision-pass` Pass 9d).
14. **No bias inheritance.** See `bias-guard`. This overrides genre convention, user-supplied
    tropes, and reference material.
15. **Token discipline.** Load the bounded read-set, not the whole novel. Never read past chapter
    files unless the user asks for a specific one. Cast depth is tiered the same way: a walk-on
    gets three strokes and one roster line, never a psychology. See §9.
16. **Write files, don't dump prose to chat.** Chapters go to `novels/<slug>/chapters/`. Report the
    path and a two-line summary.

## 5. Anti-slop constitution

Full lists live in `mtl-detox` and `bias-guard`. The short form:

- No omniscient narrator announcing that a character is a genius, beautiful or terrifying.
- No face-slap treadmill: arrogant nobody insults MC, MC reveals power, nobody grovels.
- No cannon-fodder antagonists. Every opponent wants something legible and is competent at it.
- No harem-by-default. Attraction is earned on the page and reciprocal, or it is not written.
- No ethnic, national or gendered essentialism. Ever. Not as villain shorthand either.
- No stock beats: "his expression changed drastically", "as expected of", "unexpectedly",
  "in the next instant", "trash!", "you dare?", "little did he know".
- No exposition dumps of rank ladders. Power is shown through cost and consequence.
- No establishing paragraphs, gazetteer sentences or history lectures. Enter scenes in motion.
- No wallpaper societies: if the central rule would have changed how people eat, work, travel or
  are judged, it has, and the story shows it.
- No unanchored openings. Five chapters in which a reader cannot say what world this is is not
  mystery; it is indistinguishable from the feeling of reading something bad.
- No escalation past the reader's ability to price it.
- No cannon-fodder-to-god step. A gain is one tier, bought from somebody, paid for before it lands.
- No unpriced boost. Borrowed power has an expiry and a bill, and it decides an arc's end once.
- No flat middle: thirty chapters where neither the MC's tier nor the pressure on them moved.
- No foreknowledge that only ever fails, and none that never appears.
- No noun-stack titles, and no fanfic title that omits the source work.
- No chapter padded, trimmed or shipped because of its length.
- No cast of protagonists. Somebody is slower, somebody is worse at saying it, and both are right
  about something.
- No universal experts. "I don't know" and "that's not my end" are strong lines, and a character
  who is confidently mistaken beats one who is conveniently informed.
- No instant mastery. can't → fails knowingly → unreliable → competent → fluent, advanced by a
  teacher, a text or a costly failure — never by chapters having passed.
- No default gesture set. Nodding, shrugging, sighing, raised eyebrows, crossed arms and released
  breaths belong to everyone and identify nobody.
- No prepared statements. If nobody is ever interrupted, nobody ever answers in a fragment, and
  every turn reaches a full stop, the cast is reading prose aloud rather than talking.
- No character who arrives pre-loaded. A name dropped into a scene of loaded subtext, with an
  implied history and no placement, asks the reader to remember a book they have not read.
- No stated theme. The narrator does not explain what the book means.
- No frictionless page. Every scene carries something unresolved inside somebody
  (`prose-quality` §Microtension).

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
    threads.md          open promises / foreshadowing, with ages
    timeline.md         in-world calendar + divergence ledger + crisis board
    growth.md           per-character development ladder position
    body.md             form & appearance ledger (only if a character changes form)
    power.md            ladder, pressure log, gain log, boosts, curve plan (unless shape: none)
    foreknowledge.md    grain, inventory, spend log, observer paradox (only if the MC foreknows)
  chapters/NNNN-<slug>.md
```

Chapter files carry YAML frontmatter (`number`, `title`, `pov`, `arc`, `delivers`, `wordcount`,
`status`). **`delivers`** is what is materially different at the end, in one clause — the Pass 9
gate. `wordcount` is a measured fact that later tools read, never a target.

## 7. Slash commands

`/novel-new` `/novel-plan` `/novel-write` `/novel-revise` `/novel-status`
`/novel-character` `/novel-recap` `/novel-toggle`

## 8. Style of this repo

Skills are **procedures for a model with limited budget**: numbered steps, explicit formats,
concrete examples, hard checklists. Prefer a table over a paragraph.

**Procedure in the body, everything else in `references/`.** A `SKILL.md` holds what the skill
owns, the procedure and the rules. Worked examples, failure catalogues, genre notes and long
tables go to `references/<topic>.md`, cited with an explicit trigger — *open this when …*. Skills
that `revision-pass` consults carry an **audit card** in their `references/`, written by that
skill's owner; `revision-pass` opens the card rather than paraphrasing it.

**The same rule on the drafting side: a draft card.** A skill whose decision `write-chapter` makes
carries a **draft card** in their `references/` — the 15–40 lines that produce that one answer,
written by the skill that owns it. The two are a pair and both stay: a **draft card decides**, an **audit card
checks**. Neither dispatcher paraphrases its sources; both open the owner's file, and the file is
small enough to be worth opening. Rationale: [design notes](docs/design-notes.md).

**Cite sections, never line numbers.** `hook-and-pacing` §Openings survives an edit;
`hook-and-pacing:38-39` rots the moment a paragraph is added above it, and rots silently.

---

## 9. The mechanical toolkit

`scripts/sw.py` does the countable work. **Python 3.8+, standard library only.** Full reference in
[scripts/README.md](scripts/README.md); tests in `tests/`, run with
`python3 -m unittest discover tests`.

| command | use it in |
|---|---|
| `readset <novel> -c N` | `write-chapter` step 0 · `continuity-summary` read mode — the whole read-set in one call, including which optional and genre modules are live |
| `lint <novel> -c N` | `revision-pass` Pass 0 · `mtl-detox` · `prose-quality` · `narrator-voice` |
| `cast <novel>` | `voice-separation` · `competence-map` · `novel-init` |
| `curve <novel>` | `revision-pass` Pass 9e · `power-scaling` · the arc-boundary pass |
| `state <novel>` | `continuity-summary` self-check · `plot-threads` · `chapter-plan` |
| `arc <novel> -a N` | the arc-boundary pass — trends, rotation, thread ages |
| `status <novel>` | `/novel-status` |
| `stamp <novel> -c N` | `revision-pass` Pass 10 · `write-chapter` step 4 |
| `newnovel <slug>` | `novel-init` step 3 |
| `audit <novel>` | the independent whole-novel gate |
| `history <novel>` | the whole book as a series — dialogue and length trends, recurring lint checks, thread ages, the pressure series |
| `trace [novel]` | what a run cost, and **which skill files it actually opened** — the finding-9 check |
| `health` | the toolkit's own wiring: skills, cards, references, the template accessors, the docs |
| `selftest` | the dry run — build a whole novel in a temp dir and run every command against it, clean and seeded |
| `doctor` | start here when anything behaves oddly |

Three rules, all of which exist to stop a tool becoming an alibi. **An optimisation, never a
dependency** — every skill that names a command keeps its manual checklist underneath, and if the
command is unavailable you do the checks by reading and say so in the report. **They find, they do
not judge** — nothing here rewrites a prose body, and the only files they edit are chapter
frontmatter, a CCS `wc:` field, a fresh scaffold, and `selftest`'s own throwaway directory. **A
clean run is not a passed revision** — the distributional and judgement passes are untouched by it,
and `bias-guard` has no script at all, deliberately.

The last four review the **process** rather than the novel, and the same rules bind them: `trace`
measures a run and scores nothing, `history` prints trends and scores nothing, `health` checks
wiring and says nothing about whether a skill's advice is good, and `selftest` proves the pipeline
runs without proving any chapter is worth reading. `trace` is the only command that reads outside
the repo; it takes usage, timestamps and tool names from Claude Code's transcripts and never
prompt text, tool results or prose. See [scripts/README.md](scripts/README.md).
