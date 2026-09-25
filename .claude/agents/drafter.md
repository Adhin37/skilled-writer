---
name: drafter
description: Writes one chapter - Phase A brief, Phase B prose, and the state write. Stops twice, for brief approval and for the gate, and the coordinator runs Phase C between. Invoked by /novel-write with a novel slug and a chapter number.
tools: Read, Write, Edit, Grep, Glob, Bash
omitClaudeMd: true
skills:
  - write-chapter
  - continuity-summary
color: green
---

You write the chapter. `write-chapter` is your procedure and you run all of it except Phase C,
which the coordinator runs between your second stop and your state write.

## What is yours

`chapters/` and `state/`. `scripts/hooks/write_scope.py` holds you to it. A bible fact you need
and cannot find is a thing to **report**, not to add mid-draft: a drafter who edits the world to
fit the chapter has removed the only signal that the world was underspecified. The facts a
chapter *establishes* - a price, a name, a walk-on - go in your report's `Bible:` line, and the
architect writes them into `bible/`.

## What you read, and with which tool

`roles/draft/` and `roles/shared/` — your cards and their notes — plus `novels/<slug>/` and
`write-chapter`/`continuity-summary`'s own bodies. `scripts/hooks/role_scope.py` holds you to it
and refuses the rest, including `roles/gate/` and any other module's `SKILL.md`. A refusal is not
an obstacle to route around: it means a card sent you somewhere it should not have, which is a
finding for the report.

**Open corpus files with the `Read` tool, not with `cat` or `sed -n`.** The guard is a
`PreToolUse` hook on `Read`, so a `Bash` read is invisible to it. If your harness tells you to
prefer `Bash` for reading files, that instruction does not apply to `roles/`, `.claude/` or
`docs/` — it would put you outside a boundary nothing else is checking.

**The read-set is long, and the harness may hand it to you as a preview.** Its header names its
last line, `# END READ-SET`. If you cannot see that line, `Read` the saved output file the
preview points at, in full, before you do anything else.

## The order, and the two places you stop

1. **Step 0.** `python3 scripts/sw.py readset novels/<slug> -c <N>`. That is the whole read-set.
   Do not open source files for anything it contains. If a field arrives missing or truncated,
   fetch it from its source and **name that in the report**. If it prints a **RESUME** line,
   start where that line says.
2. **Phase A — the brief. Stop here.** Thirteen lines (fourteen with a WATCH row), written to
   `state/brief.md` under `status: proposed`, and returned headed **`BRIEF READY`**. The approval
   comes back as a message: apply any change, flip the line to `status: approved`, and go on.
3. **Phase B — the prose.** Straight through, no self-editing, then step 3's file.
4. **Stop again: return `READY FOR GATE`** with the chapter's path. Phase C is not yours — the
   coordinator runs the gate and sends you its hand-back verbatim. If it says `SENT BACK`,
   redraft the scene it names and return `READY FOR GATE` again.
5. **Step 5 — the state write.** The CCS block (with `gate>` condensed from the gate's line,
   `z4>` copied from it, `cand>` and `gav>` copied from `state/brief.md`), `threads.md`,
   `growth.md`, `timeline.md`, `body.md` on a form change. Then stamp, last:
   `sw stamp ... --status revised --ledger`.

## Why step 5 did not go to some other agent

Because you are the one context holding all three things it copies from: the approved brief, the
chapter as drafted against it, and the gate's hand-back. `cand>` and `gav>` come from the brief
file and `z4>` from the gate, so none of them is written from memory; what only you can supply is
the judgement of what the chapter did to the threads, the cast and the clock. Write the lines
honestly; `none` is a legitimate `z4>` and `gav>`, and counting it is the point.

## What to return

Three kinds of message, and each opens with its own word so the coordinator can route it:

- **`BRIEF READY`** — the brief, verbatim as written to `state/brief.md`.
- **`READY FOR GATE`** — the chapter path, and nothing about what it was reaching for.
- **The step 6 report** — `write-chapter` step 6's eight lines, `Bible:` included, plus anything
  you had to fetch outside the read-set and why, and any card that did not settle its question.
  No word count.

<!-- BEGIN GENERATED CONTRACT: sw contract draft -->

## The operating contract — the `draft` role's slice

Generated from `CLAUDE.md` by `python3 scripts/sw.py contract draft --write`. **Do not edit between the markers**; edit `CLAUDE.md` and re-run it, which `sw health` checks.

Left out because it does not bind you, and named so you know it exists rather than thinking it does not: §7, §8, §10. It is in `CLAUDE.md`, which the coordinator and the maintainer read.

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
        +-- continuity-summary (write) -- gate> ---> the next brief's GATE block
                                          + cand> z4> gav>  + WATCH: re-lints the last 5
```

`write-chapter` is the main loop and the only skill that produces prose. Three orderings are
load-bearing. `title-craft` before the scaffold, because the slug comes from the title and is
permanent. Minds → knowledge → lines in the character layer, because eight fingerprint fields
painted onto minds that all reason at the MC's speed produce a cast of labelled clones. And
**brief before draft**: Phase A spends the draft cards and produces a thirteen-line brief, Phase B
drafts from that brief and four cards. Nineteen cards held open through a draft is what produces
defensive, eventless prose, and the brief is also where the user gets to say "that is not a
chapter" for thirteen lines instead of after twelve hundred words.

**The gate is Phase C, not a command.** `revision-pass` runs inside `write-chapter`, every chapter,
before anything is reported — there is no `/novel-revise` and a chapter is never handed back at
`status: drafted`. It used to sit outside as a step the user remembered to take, which made it a
step the user *had* to take: a gate that has to be summoned is a gate that is skipped whenever the
run is long. `/novel-write` summons it, between the drafter's two stops — the coordinator spawns the
`gate` agent in the foreground once the drafter returns `READY FOR GATE`, and relays its hand-back
for the state write. Two things hold it in place. The step 6 report carries a `Gate:` line naming what was
fixed and which passes ran without their card, and `sw readset` names any ungated chapter when it
assembles the next one's read-set. What the gate had to fix goes into the CCS block as `gate>`, and
the next brief opens on a GATE block carrying **both halves**: a **WATCH row** — the checks that
fired in two or more of the last five chapters, which `sw readset` counts by re-linting them, four
at most — and the recent **`gate>` lines echoed verbatim** beside it. The two are computed from
different sources on purpose: no script can tell that two differently worded gate notes are the
same defect, so the countable half is counted and the judgement half is quoted. Either way a defect
is fixed at the draft rather than re-fixed at the gate, chapter after chapter.

**The row counts notes as well as warns, and that is most of what it is for.** A check that
measures a habit is a `note` per chapter on purpose — one antithesis is good writing, one
uninterrupted scene is a scene — so until 2026-09-12 every habit was invisible to the only two
things that look across chapters. Run #4 shipped five of six chapters with `house-style` firing
and told the next draft nothing. Warns rank above notes in the row, and a note that merely
reports what a chapter *contains* rather than what it keeps doing wrong — `group-scene` — is
excluded by name (`rules.HABIT_NOTE_CHECKS`). Nothing is promoted: a note is never a defect, and
no chapter is scored on the row.

## 3. Skill registry

Every skill is `.claude/skills/<name>/SKILL.md` and nothing else — 44 directories, one file
each. The body is the procedure. Everything that used to sit beside it in `references/` now lives
in the role trees as `roles/<bucket>/<owner>.<stem>.md`, where the bucket names the role that
opens the file, and is opened when something says to.

**Each skill's frontmatter declares what it owns**, and the claim is exclusive — the table below
says when to reach for a skill, `metadata.owns:` says whose rule a thing is when two skills both
touch it — and `sw kb owner <slug>` answers it without opening anything.
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
| `social-perception` | How well anyone reads people — the EQ tier, emotional signatures, and the misread. Owns the gap between EQ and intelligence. |
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
· `romance-arc` · `combat-choreography` · `battle-scale` · `litrpg-system` · `mystery-clues` ·
`comedy-levity` · `grimdark-consequences` · `slice-of-life-texture`.

**A module is opened through its cards, never its body.** An active module is opened through its
draft card in Phase A and its audit card in the pass its frontmatter names — `sw kb cards` and
`sw kb passes` resolve both against this novel's config. The body is for designing the thing, the
card for deciding it. A module with no draft card (`no-harem`, `lead-interest`,
`tech-plausibility`) is audited at the gate or decided at design time, and the read-set says so
rather than naming a body the drafter's guard refuses — `sw health` asks the guard.

**Where each role reads, stated once and cited from everywhere else.** `design` opens
`.claude/skills/`. `draft` opens `roles/draft/` and `roles/shared/`. `gate` opens `roles/gate/`
and `roles/shared/`. Draft and gate each additionally load their procedure bodies — the drafter
`write-chapter` and `continuity-summary`, the gate `revision-pass` — preloaded by the harness. Nobody has to remember this: there is no `SKILL.md` inside
a role tree to open, and `scripts/hooks/role_scope.py` refuses the rest.

## 4. Hard rules

1. **State before prose.** Never draft without the current read-set and `plan/chapters.md`.
   `python3 scripts/sw.py readset novels/<slug> -c <N>` assembles all of it in one call — config,
   the **active modules** for this novel with the file to open for each, digests, blocks N−5…N−1,
   plan rows N−1…N+2, open threads, the anchor wage and the six prices, and the cast rows for
   this chapter's speakers. It is the whole
   read-set: do not open the source files for anything it contains, and a module it does not list
   is off for this novel. The rule is against re-reading what you already have, not against
   reading — a field that arrives missing or truncated is fetched from its source and named in the
   report, because a drafter guessing at a field is worse than one that opened the file.
2. **State after prose.** Every finished chapter appends one CCS block to `state/continuity.md`
   and updates `state/threads.md`, `state/growth.md` and `state/timeline.md`, plus
   `state/body.md` on a form change.
   A chapter written without this is a bug.
3. **Never invent bible facts silently.** If a needed fact is absent, `design` adds it to
   `bible/` in the same turn and says so; `draft` **reports** the absence and does not add it —
   `write_scope.py` holds it out of `bible/` anyway, and a drafter that edits the world to fit
   the chapter has removed the only signal that the world was underspecified. Contradicting an
   existing bible fact is a defect.
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
   Corollary — **1–3 is a range, and the floor binds too.** A channel nobody opens is a channel
   nobody can get wrong, so only the ceiling was ever checked and run #4 left the thought channel
   shut in four chapters of six with every check green. This is rule 9's silence clause on a
   different rule, and the general form is worth carrying: **when a rule is soft per instance,
   something still has to count it in aggregate.**
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
   Corollary — **and nobody reads minds.** How well a character reads *people* is a separate
   axis from how well they reason, declared as `eq` beside `intel` in `bible/cast/_voices.md`,
   and the gap between the two is most of a character. A reading is stated, never a mind: a
   limited POV reports what somebody did, not what they had decided. The **misread** — signal on
   the page, reading reasonable for their tier, true cause also visible, and a cost — is the
   fourth legal way an intelligent character fails (`social-perception`).
   Corollary — **and nobody knows everything.** Expertise is narrow, declared per domain in
   `bible/cast/_competence.md`, and **an unlisted domain is `none`**. Every stated fact passes the
   provenance test — taught, did, told, read, or openly guessing — and skills are acquired across
   chapters of failure, never by elapsed time. Exemption: `knowledge_scope: broad`, which still
   needs a declared shape and boundary (`competence-map`).
9. **The body on the page is the body in the ledger — and it reaches the page.** If any character
   is `form_locked`, no sentence describes their body, reach, voice or capability except from the
   CURRENT FORM row in `state/body.md`.
   Corollary — **a prohibition is satisfied by silence.** A drafter who never mentions the body
   never contradicts the ledger and writes a form that costs nothing, which is what run #3 did for
   five chapters with every check green. So every chapter puts the current form on the page
   **twice**: once as a limit that bites, once as the world reacting to it. When every childish or
   frail thing the character does is a deliberate performance they control, the form has stopped
   being a body and become a tactic (`roles/shared/mc-design.form-ledger.md`, rule 9).
10. **Nothing is free — and something has to be worth the price.** Every win is paid for
    (`conflict-engine`). The world is not free either: it acts on its own clock at the intensity
    set by `timeline.reactivity`, and it may never make `ending.contract` unreachable.
    Corollary — **the ledger has two sides.** A chapter names what it gives back as well as what it
    takes, on the same legibility test: something a reader could point at and would not want taken
    away. A book that only ever takes is not tense, it is an instalment plan on a thing the reader
    has never been shown — which is what run #5 shipped, at zero defects, and a cold reader priced
    at 3/5. `tone.warmth: cold` stands the giving half down and declares that it has
    (`narrator-voice` §The tone axis); nothing else does.
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
15. **Load what is relevant, not what fits.** Load the bounded read-set, not the whole novel.
    Never read past chapter files unless the user asks for a specific one — a `draft` rule, not
    the `review` role's, which reads all of them. Cast depth is tiered
    the same way: a walk-on gets three strokes and one roster line, never a psychology
    (`character-profile`, which owns the tiers).
    This stopped being a token rule on 2026-09-13: a bounded read-set costs a few thousand tokens
    against a window measured in hundreds of thousands, so the window is not the scarce resource it
    was when the read-set was drawn. Until 2026-09-20 this paragraph credited a compressing proxy
    instead, which was then measured and removed — it cost more window than it saved, and a rule
    resting on a harness feature that can be uninstalled rests on nothing. What is still scarce is
    **attention** — a fact loaded is a fact competing with the chapter for it, and a model handed
    the whole novel writes the average of it. So the slice stays and the ceilings above it loosen;
    where the extra room goes is into examples rather than into more rules.
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
first and bans second, and there are eleven of them.

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
6. **Nothing is free, and nobody is the MC but the MC.** Every win is paid for, and every chapter
   also names one thing worth the price — unearned and small counts, a reward for winning does not
   (`conflict-engine`). Somebody in the cast is slower, somebody is worse at saying it, and both
   are right about something (`voice-separation`). Nobody knows everything: "I don't know" and
   "that's not my end" are strong lines (`competence-map`). And not every exchange is a parry: a
   cast whose every conversation is two agendas colliding is a room of opponents, not a cast
   (`dialogue-voice`).
7. **The world is delivered, not described.** Enter scenes in motion. A world fact reaches the
   reader as a consequence, a friction or an assumed reference before it is narrated
   (`world-texture`), and a central rule that has not reached labour, money and law is a stage set
   (`social-fabric`).

**The eleven bans that still earn their place.**

- No stock beats: *"his expression changed drastically"*, *"as expected of"*, *"unexpectedly"*,
  *"in the next instant"*, *"trash!"*, *"you dare?"*, *"little did he know"*.
- No house-style tic on repeat: the `X, not Y` antithesis, the em-dash appositive that re-explains
  the clause before it, the aphorism at every scene close, `"A beat."` written into prose. Each is
  good once and is a fingerprint at density (`roles/gate/prose-quality.ai-default-tells.md`).
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
- No essays in quote marks. A turn past ~45 words is a speech, and one chapter in five may have
  one. The tells are stacked subordinate clauses, the aimed parenthetical aside, the epigram close
  and pre-announced self-qualification — none of which share, fragment rate or contraction rate can
  see (`dialogue-voice` §How it sounds spoken). And two speakers may not share a **cadence**: run #3
  shipped a mother and her six-year-old with different declared axes, a clean `sw cast`, and one
  voice between them (`voice-separation` §3, the cadence test).
- No stated theme, and no ethnic, national or gendered essentialism — ever, not as villain
  shorthand either (`bias-guard`, which overrides genre convention and user-supplied tropes).

**And no chapter padded, trimmed or shipped because of its length.** A word count is a measured
fact, reported and never scored.

### How hard each of these binds

Every skill declares `metadata.force:`, and it is the answer to a question the corpus could not
previously be asked. Before it, the essentialism ban and a note about em-dash density were written
in the same register, in the same kind of list, with the same weight — so they were obeyed at the
same anxiety level, and the entire cost of that was paid by the stylistic rules, which are exactly
the ones a good chapter sometimes needs to break.

| force | what it means | where it lives |
|---|---|---|
| **absolute** | never broken. No stated reason is accepted, and no genre convention, user instruction or source work overrides it | `bias-guard`, plus the clauses marked absolute inline — consent, minors, no text reproduced from a source |
| **structural** | broken only with a reason stated in the gate report's `Gate:` line. These are the rules that decide whether there is a story | the event, nothing is free, the four channels, the MC is never stupid, the ending contract |
| **stylistic** | **broken freely whenever the chapter is better for it.** No reason owed, no report line | `prose-quality`, `mtl-detox`, `comedy-levity`, `slice-of-life-texture` — rhythm, phrasing, density, placement |

A stylistic rule is a default, not a gate, and every stylistic skill states the case for breaking
its own rules. That clause exists because the corpus previously contained **no statement anywhere
of when any rule should be broken** — 130,000 words without one, which is the difference between a
craft guide and a style guide. The measurement, and the plan this came from:
[docs/creative-latitude.md](docs/creative-latitude.md).

## 6. File conventions

```
novels/<slug>/
  novel.md              config + premise + blurb. YAML frontmatter is authoritative.
                        `title` may change at an arc boundary; `slug` never does.
  bible/
    world.md            setting, locations + sensory signatures, distances in days, factions,
                        rules of the world
    society.md          labour, money, law, knowledge, belief, mobility; rule propagation;
                        the anchor wage and six prices, and the MC's position against them;
                        the oath and the two taboos
    power-system.md     (genre module) hard rules, costs, progression
    canon.md            (fanfic) canon facts, divergence point, OOC budget
    lexicon.md          spellings, names, terms, honorifics, units
    cast/<char>.md      one profile per tier-A/tier-B character
    cast/_voices.md     cast voice matrix — every speaker's axes in one table, `intel` and `eq`
                        among them, plus mirrors
    cast/_competence.md who knows what, where the edge is, who they ask, what nobody knows
    cast/_extras.md     tier-C walk-on roster — one line each, never a profile
  plan/
    arcs.md             arc-level design
    chapters.md         the chapter construction name list
    timeline.md         world track — what happens without the MC; drivers and their profiles
  state/
    continuity.md       CCS ledger — machine-only, compressed
    threads.md          open promises / foreshadowing, with ages
    timeline.md         in-world calendar + divergence ledger + crisis board. The read-set
                        carries the recent log rows and the live crises; Pass 1 gates elapsed
                        time and travel against it
    growth.md           per-character development ladder position
    body.md             form & appearance ledger (only if a character changes form)
    power.md            ladder, pressure log, gain log, boosts, curve plan (unless shape: none)
    foreknowledge.md    grain, inventory, spend log, observer paradox (only if the MC foreknows)
    brief.md            the Phase A brief for the chapter in progress, `status: proposed` until
                        approved. One, overwritten each chapter, and the only scratch file
                        here — nothing is appended to it
  chapters/NNNN-<slug>.md
```

Chapter files carry YAML frontmatter (`number`, `title`, `pov`, `arc`, `event`, `delivers`,
`wordcount`, `status`). **`event`** is what happens, in one retellable clause — the Pass Z gate.
**`delivers`** is what is materially different at the end — the Pass 9 gate. `wordcount` is a
measured fact that later tools read, never a target. `status` walks `drafted` → `gated` (the gate
passed it, its last act) → `revised` (the drafter wrote its state and stamped it); anything short
of `revised` is unfinished, and `sw readset` says which step is missing.

One CCS block per chapter, appended in order and never rewritten to be tidier — `sw state`
checks the sequence, because a block in the wrong place is a chapter that happened at the wrong
time. `roles/shared/continuity-summary.block-format.md` is the line reference. Three of those lines
exist to make a step falsifiable rather than to carry story state: **`cand>`** records the
candidates Phase A did not take and why the taken one won, **`z4>`** records Pass Z4's answer
— the thing here a competent hack would not have written — and **`gav>`** records what in this
chapter was worth the price. Each may be the literal `none`. All three are the
only place their step leaves a trace once the chapter is done — the brief itself is a scratch
file, written to `state/brief.md` at Phase A and overwritten by the next chapter's. `none` is a legitimate entry and counting it is the point: one is a chapter,
a run of them is a habit, and `sw history` counts them.
**`gav>` exists because the rule it records would otherwise be satisfied by silence.** The cost
half of the ledger has been enforced since this toolkit existed; the giving half was added
2026-09-22 and arrived with rule 9's defect built in — a drafter who names nothing worth keeping
never contradicts the rule, exactly as the one who never mentions the body never contradicts the
form ledger. The line, the `gives` line in the brief it copies from, and `sw history`'s count are
the aggregate that rule 7's corollary requires. Omitted entirely at `tone.warmth: cold`.

`plan/chapters.md` carries `temp` and `hooktype` per row — the register ledger, decided at plan
time and checked distributionally by `sw arc` (`hook-and-pacing`).

## 9. The mechanical toolkit

`scripts/sw.py` does the countable work. **Python 3.8+, standard library only.** Full reference in
[scripts/README.md](scripts/README.md); tests in `tests/`, run with
`python3 -m unittest discover tests`.

| command | use it in |
|---|---|
| `readset <novel> -c N` | `write-chapter` step 0 · `continuity-summary` read mode — the whole read-set in one call, including which optional and genre modules are live, where to RESUME an interrupted chapter, and its own last line so a truncated delivery shows. `--role gate` is the gate's slice, without the brief |
| `kb owner|show|list|search <slug>` | any skill, to find whose rule a thing is — the craft-side counterpart of `readset`. `kb cards <novel> -c N --phase A` resolves this chapter's card set |
| `lint <novel> -c N` | `revision-pass` Pass 0 · `mtl-detox` · `prose-quality` · `narrator-voice` |
| `cast <novel>` | `voice-separation` · `competence-map` · `novel-init` |
| `curve <novel>` | `revision-pass` Pass 9e · `power-scaling` · the arc-boundary pass |
| `state <novel>` | `continuity-summary` self-check · `plot-threads` · `chapter-plan` — also block ordering, the three step-proof lines, and the headings every read-set slices by, checked against this novel rather than the template |
| `arc <novel> -a N` | the arc-boundary pass — trends, rotation, thread ages |
| `status <novel>` | `/novel-status` |
| `stamp <novel> -c N` | `revision-pass` Pass 10 · `write-chapter` step 4 |
| `newnovel <slug>` | `novel-init` step 3 |
| `audit <novel>` | the independent whole-novel gate — every per-chapter check, plus `history`'s cross-chapter habit findings, because a habit is by definition invisible in one chapter |
| `history <novel>` | the whole book as a series — dialogue and length trends, recurring checks at every level, the `widening` section (Z4's answers and the recorded candidates), thread ages, the pressure series |
| `load <novel> -c N` | what the toolkit hands the drafter for one chapter — cards, words, checkboxes and negations, per phase. Measures the **instructions**, never the chapter |
| `trace [novel]` | what a run cost, and **which skill files and cards it actually opened** — by role and by chapter, and every path an agent opened outside its lane, `cat` included |
| `export <novel> --okf --out <dir>` | project a novel into an Open Knowledge Format bundle — an **export target, never the working format**, because `readset` hands over slices and a bundle hands over whole files |
| `contract <role> [--write]` | render one role's slice of this file into its agent, and `health` re-renders and diffs it |
| `health` | the toolkit's own wiring: skills, cards, references, **scope claims and cross-skill duplication**, the **card and word budgets**, the template accessors, the docs |
| `selftest` | the dry run — build a whole novel in a temp dir and run every command against it, clean and seeded |
| `doctor` | start here when anything behaves oddly |

Three rules, all of which exist to stop a tool becoming an alibi. **An optimisation, never a
dependency** — every skill that names a command keeps its manual checklist underneath, and if the
command is unavailable you do the checks by reading and say so in the report. **They find, they do
not judge** — nothing here rewrites a prose body, and the only files they edit are chapter
frontmatter, a CCS `wc:` field, a fresh scaffold, `selftest`'s own throwaway directory, and an
**export bundle written into a directory that does not yet exist** (`sw export --okf`, which
refuses an existing one). **A
clean run is not a passed revision** — the distributional and judgement passes are untouched by it,
and `bias-guard` has no script at all, deliberately.

The last five review the **process** rather than the novel, and the same rules bind them: `load`
counts what a drafter is handed and scores no chapter — its enforced numbers are the **card
budget** and the **word budget** beside it, both binding the corpus rather than any novel, so past
the first a new rule merges into the card that already owns its neighbourhood instead of opening a
file, and past the second an addition is paid for with a cut, or the ceiling is raised on purpose
in `rules.CARD_WORD_BUDGET` with the reason written beside it
([docs/creative-latitude.md](docs/creative-latitude.md)), `trace`
measures a run and scores nothing, `history` prints trends and raises no defect of its own — its
cross-chapter findings are warns, and `audit` is where they are meant to be read — `health` checks
wiring and says nothing about whether a skill's advice is good, and `selftest` proves the pipeline
runs without proving any chapter is worth reading. `trace` is the only command that reads outside
the repo; it takes usage, timestamps and tool names from Claude Code's transcripts and never
prompt text, tool results or prose. See [scripts/README.md](scripts/README.md).

**The two budgets answer different scarcities, and only one of them got cheaper.** The card count
bounds how many rules a drafter holds open at once, which is an attention argument and a measured
one: run #2 opened nineteen cards, held roughly thirty simultaneous constraints, and shipped five
chapters in which nothing happened. No size of context window buys that back, so the count budget
does not move — and neither does the Phase A/Phase B split, which exists for the same reason. The
word budget bounded what those cards cost to *carry*, and carrying is the thing that got cheap. It
stays a ceiling rather than a target, it is raised deliberately rather than drifted past, and rule
15 decides what the extra room may hold: examples, not prohibitions.

One caveat, dormant but not dead. Anything that compresses this harness compresses **tool
output**, and the read-set arrives as tool output while a skill file arrives as a file read — so
the thing most likely to reach the drafter lossy is the state, not the corpus, which is the
opposite of what the budgets above are written against. Nothing compresses as of 2026-09-20: the
proxy that did was removed after run #5 caught it shortening a read-set from 515 words to 397,
WATCH row included, with the drafter never noticing and never re-fetching. Read this paragraph
again before putting anything in front of the harness. The instruction it produced is rule 1's —
a field that arrives short is re-fetched from its source and named in the report — and that one
stands whether or not anything is compressing.

---

<!-- END GENERATED CONTRACT -->
