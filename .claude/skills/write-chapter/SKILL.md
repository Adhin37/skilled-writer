---
name: write-chapter
description: Draft the next chapter, orchestrating continuity, character, POV, conflict, pacing and quality into one procedure. Use when the user asks to write or continue a chapter, or says /novel-write.
---

# write-chapter

The main loop. This is the only skill that produces prose. Follow the steps in order; each one
is cheap, and skipping one is what produces the drift that ruins long serials.

---

## Step 0 — Load

1. Resolve the active novel (see `CLAUDE.md` §1). Read `novels/<slug>/novel.md`.
2. Note: `genre`, `narration.*`, `pov.*`, `mc.intel_tier`, `chapters.*`, `content.*`.

   The CONFIG block also resolves **active modules** — the optional and genre skills switched on
   for this novel — and names each one's entry point: its draft card where it has one, its
   `SKILL.md` where it does not. **Open those and no others.** A module that is not listed is off
   for this novel and costs nothing. An active one is *consulted this chapter*, not merely
   permitted.

   Without Python: read the `optional:` block and `genre` in `novel.md` and resolve the same list
   by hand, then say so in the report.
3. Determine the chapter number: highest existing file in `chapters/` + 1, unless told otherwise.
4. Run `continuity-summary` in **read mode** — `python3 scripts/sw.py readset novels/<slug> -c <N>`
   assembles it in one call, sliced rather than whole-file. You now have the read-set and the
   chapter brief. Steps 1 and 2 above are in its CONFIG block, so `novel.md` needs no separate
   read. Without Python, load the list in `continuity-summary` by hand.
5. Read the target row in `plan/chapters.md`. If it is missing or any of
   goal/obstacle/turn/cost/hook is blank, run `chapter-plan` for this row first. Do not draft
   from an incomplete row.

## Step 1 — Decide the chapter's shape (before writing a word)

Write these down for yourself. Ten lines, not a document.

Each decision below has a **draft card** — the 15–40 lines that produce that one answer, written by
the skill that owns it. Open the card, not the skill body: a body is a procedure for designing the
thing, and this step is for deciding it. Four cards are conditional and are skipped outright when
their condition is false.

| decision | card |
|---|---|
| POV character, and whether this is a switch | `pov-switch/references/draft-card.md` + the plan row |
| Scene count, the break, and per scene goal → obstacle → turn → exit | `scene-craft/references/draft-card.md`, `chapters.scenes_per_chapter` |
| Which beat is played and which is reported | `story-craft/references/draft-card.md` — the important beat gets the scene |
| What this chapter costs the POV character | `conflict-engine/references/draft-card.md` — never zero |
| Which thread ops fire | `plot-threads/references/draft-card.md` |
| Which character sounds different today, and how | `character-development/references/draft-card.md` → `state/growth.md` |
| **The voice spread**: this chapter's speakers as matrix rows, side by side — and which of them differs from the MC on two or more axes | `voice-separation/references/draft-card.md` → `bible/cast/_voices.md` |
| Anyone new on the page: their **cast tier**, decided before they speak | `character-profile/references/draft-card.md` |
| **The offstage question**: what the world does this chapter that the MC doesn't know | `timeline-engine/references/draft-card.md` → `plan/timeline.md` |
| **The world channel**: the one thing about the world this chapter makes concrete, and whether a consequence, a friction or an assumed reference carries it | `world-texture/references/draft-card.md` |
| What the MC deduces, and from which on-page clue | `mc-intel-meter/references/draft-card.md` |
| **What this chapter delivers**: the one thing that is materially different at the end | `scene-craft/references/draft-card.md` — this becomes `delivers:` in the frontmatter |
| **Who has to ask**: the thing this chapter needs known, whose map actually covers it, and who must go to someone else for it | `competence-map/references/draft-card.md` → `bible/cast/_competence.md` |
| Opening line strategy, closing hook | `hook-and-pacing/references/draft-card.md` |

**Conditional — check the condition first, and skip the card entirely if it is false.**

| condition | decision | card |
|---|---|---|
| chapter ≤ `opening.contract_by_ch + 2` | **The anchor debt** — what a reader still cannot answer about world, place or canon position, and which beat pays it — and **the ceiling check**: if this chapter escalates, is the mechanism that makes it dangerous already on the page? | `story-opening/references/draft-card.md` |
| `scaling.shape` is not `none` | **The pressure**: what gap between the MC and this chapter's opposition does the arc want — and only then, who is that opposition? | `power-scaling/references/draft-card.md` → `state/power.md` §6 |
| `mc.foreknowledge` is set | **The foreknowledge spend**: what the MC knows that bears on today, at what grain, what using it costs, and what it invalidates | `meta-knowledge/references/draft-card.md` → `state/foreknowledge.md` |
| anyone is `form_locked` | Which bodies are locked, and what they cannot do today | `mc-design/references/draft-card.md` → `state/body.md` |

Plus the **active modules** from Step 0.2, each at the entry point the read-set named for it.

A card that does not settle the question is the one case for opening its owner's `SKILL.md`; every
card names the section to open when that happens.

**Two gates, both before drafting.**

1. If **"what this chapter costs"** is empty, the chapter is not ready. Go back to
   `conflict-engine`. A chapter where the POV character only gains is filler regardless of how
   much happens in it.
2. If **"what this chapter delivers"** is a description of events rather than a difference, the
   chapter is not ready either. *"She asks Tsuru about the recount"* is events; *"she is now
   someone Tsuru watches on purpose"* is a delivery. Length will not fix a chapter that has
   nothing to deliver, and length is not what it will be judged on.

## Step 2 — Draft

Write straight through. Do not stop to self-edit; `revision-pass` handles that.

Hold these while writing:

- **Voice.** `narrator-voice/references/draft-card.md` — person, tense, distance, interiority,
  and the distance curve. It does not change mid-chapter unless `pov-switch` says a switch is
  happening.
- **Dialogue.** Every named speaker's lines must satisfy their speech fingerprint
  (`dialogue-voice/references/draft-card.md`). If you cannot tell two characters apart with the
  tags removed, fix it now.
- **The four channels.** `"…"` speech · `'…'` direct thought, **1–3 for the whole chapter**, at
  decisions · `[…]` system text and in-world documents · and **unmarked free indirect discourse,
  which is where interiority actually lives** (`narrator-voice/references/draft-card.md`). Do not tag a
  marked thought with *she thought* — the mark already said it. Do not let an apostrophe become a
  thought mark. A `'…'` inside a `"…"` is a nested quotation, not thought.
- **Enough dialogue to audit.** Target **25–40% of the chapter inside `"…"`** — spoken aloud, to
  another person; thought and meta do not count
  (`dialogue-voice/references/draft-card.md`). Under 10% is a defect: the cast has become scenery and
  every voice check in this toolkit silently no-ops, because there are no lines to tell apart.
  When two people are in a room, the beat belongs to what they *say* to each other — not to the
  POV character concluding it on their behalf. An analytical POV voice is the usual cause; it is
  pleasant to write and it quietly eats the scene.
- **Voice spread.** Hold each speaker's matrix row while writing (`voice-separation`): their turn
  length, their articulacy — which is *not* their intelligence — and whether wit is theirs at all.
  Nobody except a declared mirror reasons at the MC's speed by default; somebody in this chapter is
  slower than the MC, or worse at saying it, and is right about something anyway. Beats come from
  each character's hands and pressure move, never from the default gesture set.
- **Other minds, no interiority.** Non-POV characters think through their **first move** — what
  they reach for or look at first when the situation changes. That is the whole mechanism; the
  narration never enters a second head.
- **Walk-ons.** A new minor character gets three strokes and no more: a five-minute want, one
  habit, and one piece of their working world — plus one axis off default, so they do not speak in
  the narrator's register. No interiority, no backstory paragraph, no ladder. Do not stop to build
  a profile mid-draft — sketch them, and log the line in step 5.
- **Intelligence.** Every MC decision passes the `mc-intel-meter` trace test: the reader can name
  the on-page fact it came from.
- **Knowledge.** Every *fact* anyone states passes the `competence-map` provenance test: they were
  taught it, did it, were told it, read it, or are openly guessing. An unlisted domain is `none`,
  so somebody in this chapter says they do not know, asks the person who does, or is confidently
  wrong — and a character being wrong is more useful than a character being blank. Nobody explains
  a subject their map does not cover, however convenient their mouth is.
- **Learning.** If anyone is practising something, it appears as a clause, not a scene — unless a
  stage transition fires this chapter, which earns one. Either way the practice took time from
  something else and the chapter says what.
- **Ground the scene.** `world-texture`. Two to four concrete sensory details per scene, at least
  one non-visual, drawn from the location's signature in `bible/world.md` and hit within 100 words
  of arriving. Never a paragraph of description — details placed in motion, and **filtered through
  the POV character**: they notice what their job, wound and want make salient, and they do not
  notice what is normal to them. The world's *rules* reach the reader by biting someone or by
  being worked around, not by being narrated.
- **Cut the connective tissue.** Enter scenes late, leave early. No arrivals, no farewells, no
  walking between locations unless something happens on the way.
- **Active modules.** Apply each active module's card as you write, not afterwards.

### Chapter anatomy

Proportions, not word counts — a chapter is judged on what it delivers, so the shape is what
matters and the length is whatever the material needs.

| section | share | job |
|---|---|---|
| Cold open | ~7% | In motion. A line of dialogue, an action, or a wrong-feeling detail. Never weather, never waking up, never a recap. |
| Scene 1 | ~40% | Goal pursued, obstacle met, first turn. |
| Break | — | `* * *` |
| Scene 2 | ~40% | Consequence of the turn; the chapter's cost lands. **The delivery lands here.** |
| Hook | ~5% | The last beat. See `hook-and-pacing`. |

**Chapter 1 has its own shape** — disruption, investment, world, cliffhanger — in
`story-opening/references/chapter-one.md`. Use that instead for chapters inside the opening arc.

Across those sections, **25–40% of the words are spoken aloud**. Deviate freely when the material
wants it — but never end without a hook if `chapters.hook_required` is true.

### Recap discipline

Readers arrive a day or a week later. Re-anchor with **one clause, inside a sentence doing other
work**: "The coat she'd taken off Dael's body still smelled of the undercroft." Never a
paragraph. Never "As you'll remember".

## Step 3 — Write the file

`novels/<slug>/chapters/NNNN-<kebab-title>.md`, four-digit padded, with the frontmatter from
`chapters/_chapter-template.md` filled in — including **`delivers:`**, which is the decision you
already made in Step 1. Prose only in the body — the four channels and nothing else. No headings,
no author notes.

Leave `wordcount:` at whatever the template holds; it is stamped from the measured body in Step 4,
after revision has changed the text. It is a recorded fact, not a target.

## Step 4 — Revise

Run `revision-pass`. It opens with the mechanical sweep —

```bash
python3 scripts/sw.py lint novels/<slug> -c <N>
```

— and then runs `prose-quality`, `mtl-detox`, `bias-guard`, voice separation, competence and a
continuity check, which are judgement and are not in the sweep. Fix what it finds, in the file.

When every pass is clean, stamp the measured count and the status in one call:

```bash
python3 scripts/sw.py stamp novels/<slug> -c <N> --status revised --ledger
```

## Step 5 — Write state back

Run `continuity-summary` in **write mode**: CCS block, threads, growth, timeline, any new bible
facts. This step is not optional and not deferrable to "later". When the block is written,
`python3 scripts/sw.py state novels/<slug>` verifies it against the chapter on disk.

World bookkeeping, same pass: any new location anchor or durable social fact goes into `set>`,
then into `bible/world.md` or `bible/society.md`. An anchor invented on the page and never
recorded will drift by its third appearance.

Cast bookkeeping, same pass: every walk-on who appeared gets their roster line in
`bible/cast/_extras.md` (or their appearance chapter appended to an existing one), every named
person goes in `lexicon.md`, and anyone who hit a third appearance or changed the plot is promoted
now — with their profile built from what is already on the page. A promotion also earns a row in
`bible/cast/_voices.md` and one in `bible/cast/_competence.md`, both placed against the existing
cast rather than invented in isolation.

Foreknowledge bookkeeping, same pass, if `mc.foreknowledge` is set: every spend gets a row in
`state/foreknowledge.md` §3 with its cost and what it invalidated, statuses move in §2, and any
plot-changing spend moves at least one *other* row toward `invalidated` (§4, the observer paradox).
The chapter's CCS block carries an `fk>` line. A chapter that spent foreknowledge and left the
ledger untouched is the same class of bug as one that skipped its CCS block.

Power-curve bookkeeping, same pass, unless `scaling.shape` is `none`: every confrontation gets a
row in `state/power.md` §3 with its pressure and, at P ≥ +1, what the win cost. A permanent tier
advance goes in §4 with all four requirements — source, the chapter the price was paid, the chapter
it was set up in, and the new problem — and §1 moves with it. A boost goes in §5 with its expiry,
its debt and the chapter that debt is due. The chapter's CCS block carries a `pwr>` line, and it
must agree with §3; `sw curve` checks that it does.

Knowledge bookkeeping, same pass: a skill stage that advanced goes in the skill-ladder table of
`state/growth.md` with what caused it; a genuinely new domain a character acquired on the page goes
on the competence grid. If the chapter had to invent an expertise nobody had, record it — and say
so in the report, because it usually means the cast is missing a person.

## Step 6 — Report

Five lines to the user, no more:

```
Ch 42 — "The Ledger Room" → novels/<slug>/chapters/0042-the-ledger-room.md
Delivers: Rin can no longer use the Guild's archive, and knows who closed it to her.
Cost: Rin loses Dael's trust; Echo-step now known to the Guild.
Threads: opened T14 (forged seal), paid T09 (oath to Mira).
Next: ch 43 is planned — she reads the ledger. Say go, or tell me what to change.
```

**Lead with the delivery, and do not report a word count.** Reporting length is what taught the
drafting model to aim at it; the number lives in the frontmatter, where tools can read it.

Do not paste the chapter into chat unless asked.

---

## When something goes wrong, or the run is long

- **A drafted chapter feels wrong and you want the name of what is wrong** — open
  `references/failure-modes.md`. Thirty symptoms, each with its cause and the skill that owns
  the repair.
- **The user asked for several chapters, or the draft left the plan behind** — open
  `references/batch-and-replan.md`. The per-chapter loop rule, the 5-chapter check-in, the
  fresh-session rule for cost, and how to amend a plan row without abandoning the arc.
