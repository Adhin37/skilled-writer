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
                +--------------------------------------------------------+
                v
        continuity-summary (read) --> write-chapter, in three phases
        ^                     |
        |                     |   phase A: the brief    -- stop; the user approves it
        |                     |
        |                     |   phase B: draft        [story-craft]  [narrator-voice]    ^
        |                     |                         [dialogue-voice]  [style: target]  |
        |                     |                                                            |
        |                     |   phase C: the gate     = revision-pass, in full           |
        |                     |                         [Z: THE EVENT] --- no event? ------+
        |                     |                         [9: DELIVERY]   [2: voices]
        |                     |                         [3: knowledge]  [5: world]
        |                     |                         [8b: register]  [9b: opening]
        |                     |                         [9c: foreknowledge]  [9e: the curve]
        |                     v
        +-- continuity-summary (write) -- gate> --> the next brief's WATCH row
```

`write-chapter` is the main loop and the only skill that produces prose. Three orderings are
load-bearing. `title-craft` before the scaffold, because the slug comes from the title and is
permanent. Minds → knowledge → lines in the character layer, because eight fingerprint fields
painted onto minds that all reason at the MC's speed produce a cast of labelled clones. And
**brief before draft**: Phase A spends the draft cards and produces a twelve-line brief, Phase B
drafts from that brief and four cards. Nineteen cards held open through a draft is what produces
defensive, eventless prose, and the brief is also where the user gets to say "that is not a
chapter" for twelve lines instead of after twelve hundred words.

**The gate is Phase C, not a command.** `revision-pass` runs inside `write-chapter`, every chapter,
before anything is reported — there is no `/novel-revise` and a chapter is never handed back at
`status: drafted`. It used to sit outside as a step the user remembered to take, which made it a
step the user *had* to take: a gate that has to be summoned is a gate that is skipped whenever the
run is long. Two things hold it in place. The step 6 report carries a `Gate:` line naming what was
fixed and which passes ran without their card, and `sw readset` names any ungated chapter when it
assembles the next one's read-set. What the gate had to fix goes into the CCS block as `gate>`, and
the recurring entries come back as the next brief's WATCH row — so a defect is fixed at the draft
rather than re-fixed at the gate, chapter after chapter.

## 3. Skill registry

Every skill is `.claude/skills/<name>/SKILL.md` plus a `references/` directory. The body is the
procedure; the references hold examples, catalogues and long tables, and are opened when the body
says to. See §8.

**Each skill's frontmatter declares what it owns**, and the claim is exclusive — the table below
says when to reach for a skill, `owns:` says whose rule a thing is when two skills both touch it.
The answer to "where does this rule live?" is always one skill, and every other skill cites it.

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
| `revision-pass` | The QC gate — **Phase C of `write-chapter`**, never a separate step. A chapter is not reported until this passes. |

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
| `story-craft` | Whether a beat is a scene or a summary, and the shape of a build-up. Inside `write-chapter` and `revision-pass`. |
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
4. **A chapter is judged by what it delivers, not its length — and it has to deliver an event.**
   Two fields, failing in opposite directions. **`event:`** is what *happens*: one clause a reader
   could retell, concrete verb and a target, no abstract-state nouns. **`delivers:`** is what is
   materially different afterwards. Asked only for a difference, a model writes *"proximity that
   isn't refused"* and ships eleven hundred words in which nothing occurs — which is what
   benchmark run #2 did, five times. `revision-pass` Pass Z gates on the event before Pass 9
   gates on the delivery, and `change` still names a difference, not a summary of events.
   Corollary — **the event gets the scene.** If the biggest thing that happens is not the longest
   scene, the chapter is not finished (`story-craft`).
   Corollary — **and the book changes temperature.** Every chapter declares a `temp` and a
   `hooktype` before it is drafted, checked distributionally across the arc and never scored per
   chapter (`hook-and-pacing`). Within the chapter, roughly a third of the prose carries
   information and nothing else. One temperature and one loaded sentence-shape for a whole book
   is what reads as machine-made, and no phrase list catches it (`prose-quality`).
   Nothing gates on `chapters.length_band`; nothing is padded or trimmed to reach it. A word count
   is a measured fact, reported and never scored.
   Corollary — **the important beat gets the scene.** A turn reported in a past-perfect clause is a
   scene that was skipped, and a story that summarises its own turning points is rushing however
   well it delivers on paper. Summary is for bridges (`story-craft`).
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

## 5. What good looks like

Full lists live in `mtl-detox`, `prose-quality` and `bias-guard`. This section used to be thirty
bans. It is shorter now, and the reason is the evidence: benchmark run #2 satisfied almost every
one of them — zero MTL hits, zero cut-list phrases, five chapters shipped `status: revised` — and
a reader flagged it as machine-written on page one and priced it at one star.

**A hundred prohibitions do not add up to a story.** They tell a model what not to write, it
avoids all of it, and what fills the vacuum is the model's own default register: every sentence
loaded, every scene closed on a small ironic withholding, one temperature for a whole book. That
is a *narrower* fingerprint than the cliché the bans removed. So the rules below are commitments
first and bans second, and there are ten of them.

**The seven commitments.**

1. **Something happens.** Every chapter has an `event:` — one clause a reader could retell, with a
   concrete verb and a target. Not a state, not an effect, and never an abstract noun: `trust`,
   `proximity`, `attention`, `tension` name what an event *did*, not the event.
2. **The event gets the scene.** The biggest thing that happens is the longest scene in the
   chapter. A turn reported in a past-perfect clause is a scene that was skipped, and a story
   that summarises its own turning points is rushing however well it reads (`story-craft`).
3. **The book changes temperature.** Every chapter declares a `temp` and a `hooktype` at plan
   time. Never the same temperature three chapters running; four distinct values of each per arc;
   no hook shape more than twice in five. A quiet chapter is earned by a loud one
   (`hook-and-pacing`).
4. **Sentences are allowed to be plain.** Roughly a third of a chapter carries information and
   nothing else — no dash, no reversal, no irony, no lesson appended. A narrator who loads every
   sentence has one attitude, and one attitude for a whole book is the tell no phrase list catches
   (`prose-quality` §Range before polish).
5. **Every opponent wants something legible and is competent at it.** No cannon fodder, no
   face-slap treadmill, no omniscient narrator announcing that somebody is a genius or terrifying.
6. **Nothing is free, and nobody is the MC but the MC.** Every win is paid for
   (`conflict-engine`). Somebody in the cast is slower, somebody is worse at saying it, and both
   are right about something (`voice-separation`). Nobody knows everything: "I don't know" and
   "that's not my end" are strong lines (`competence-map`).
7. **The world is delivered, not described.** Enter scenes in motion. A world fact reaches the
   reader as a consequence, a friction or an assumed reference before it is narrated
   (`world-texture`), and a central rule that has not reached labour, money and law is a stage set
   (`social-fabric`).

**The ten bans that still earn their place.**

- No stock beats: *"his expression changed drastically"*, *"as expected of"*, *"unexpectedly"*,
  *"in the next instant"*, *"trash!"*, *"you dare?"*, *"little did he know"*.
- No house-style tic on repeat: the `X, not Y` antithesis, the em-dash appositive that re-explains
  the clause before it, the aphorism at every scene close, `"A beat."` written into prose. Each is
  good once and is a fingerprint at density (`prose-quality/references/ai-default-tells.md`).
- No important beat delivered as a past-perfect clause. *"She had spent three weeks making it
  true"* is a campaign that happened offstage.
- No exposition dumps of rank ladders, no establishing paragraphs, no history lectures. This bans
  a *mode of telling*, never the build-up itself.
- No unanchored openings, and no escalation past the reader's ability to price it
  (`story-opening`).
- No cannon-fodder-to-god step and no unpriced boost. A gain is one tier, bought from somebody,
  paid for before it lands (`power-scaling`).
- No flat middle: thirty chapters where neither the MC's tier nor the pressure on them moved.
- No harem by default, and no instant mastery — skills advance by a teacher, a text or a costly
  failure, never by chapters having passed.
- No default gesture set. Nodding, shrugging, sighing, raised eyebrows and released breaths belong
  to everyone and identify nobody. And no prepared statements: if nobody is ever interrupted and
  every turn reaches a full stop, the cast is reading prose aloud rather than talking.
- No stated theme, and no ethnic, national or gendered essentialism — ever, not as villain
  shorthand either (`bias-guard`, which overrides genre convention and user-supplied tropes).

**And no chapter padded, trimmed or shipped because of its length.** A word count is a measured
fact, reported and never scored.

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

Chapter files carry YAML frontmatter (`number`, `title`, `pov`, `arc`, `event`, `delivers`,
`wordcount`, `status`). **`event`** is what happens, in one retellable clause — the Pass Z gate.
**`delivers`** is what is materially different at the end — the Pass 9 gate. `wordcount` is a
measured fact that later tools read, never a target.

`plan/chapters.md` carries `temp` and `hooktype` per row — the register ledger, decided at plan
time and checked distributionally by `sw arc` (`hook-and-pacing`).

## 7. Slash commands

`/novel-new` `/novel-plan` `/novel-write` `/novel-status`
`/novel-character` `/novel-recap` `/novel-toggle`

There is deliberately no revise command. `/novel-write` runs all three phases including the gate,
and `/novel-write <n>` on a chapter that already exists offers to re-gate it or redraft it.

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

**One concept, one owner.** Every skill declares its scope in frontmatter — `owns: [slug, slug]` —
and no two skills may claim the same slug. A skill states the rules it owns; for everything else it
**cites the owner by name and stops**. Citing is free: `sw health` strips code spans before it
compares, so a pointer never reads as a copy.

```bash
grep -H '^owns:' .claude/skills/*/SKILL.md        # the whole map, one line per skill
```

This is enforced, not aspirational. `sw health` fails a skill with no `owns:`, a slug claimed twice,
and any **pair of skills carrying the same 12-word passage** more than twice. The reason is measured:
before the rule there were 28 such pairs and 361 shared passages, and the copies had already drifted
apart — `write-chapter` and `scene-craft` held the same chapter-proportions table with different
numbers in it. A second copy is not redundancy, it is a second thing to maintain and a silent
contradiction waiting for whichever skill gets edited next. Rationale:
[design notes](docs/design-notes.md).

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
| `health` | the toolkit's own wiring: skills, cards, references, **scope claims and cross-skill duplication**, the template accessors, the docs |
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
