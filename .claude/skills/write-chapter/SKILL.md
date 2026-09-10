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

## Step 1 — Phase A: the brief (and stop)

**Drafting is two phases and this is the first one. It ends with you stopping.**

Phase A spends the cards below and produces **one brief**; Phase B drafts from that brief and four
cards, nothing else. Why it is split this way: `references/draft-cards.md`.

The brief is twelve lines, written into the chat, not into a file.

```
Ch 12 — "The Second Quarter"
event    Wren files the counter-claim and is put out of the house
temp     loud          hooktype  decision
scene 1  (~35%) goal / obstacle / turn
scene 2  (~55%) goal / obstacle / turn   <- the event happens HERE, longest scene
cost     she loses the apprenticeship, and Maro will not look at her
speakers Wren, Hesk, Maro   (Hesk differs from Wren on intel + articulacy)
world    the levy office charges for its own paperwork
asks     Wren does not know what a counter-claim costs; she has to ask Bel
threads  ^T02  vT04
next     the quarter answers in nine days
```

**Then stop and show it to the user.** They approve it, change a line, or throw it out — the
cheapest gate in the toolkit, because a chapter that was going to be a thousand words of somebody
quietly feeling something gets caught for twelve lines instead of after the draft. Skip the stop
only if told to (`/novel-write --no-confirm`, or "just write the next five"): Phase A still
happens, you simply do not wait.

**Two gates, both before drafting.**

1. **The event.** What *happens* — one clause a reader could retell, concrete verb and a target.
   *"She lies to the Hokage about the recovery list."* Asked only for "a difference", a model
   writes *"proximity that isn't refused"* and ships a chapter in which nothing occurs, so
   abstract-state nouns (`trust`, `proximity`, `attention`, `tension`, `doubt`) are rejected by
   `sw lint`. **And the event gets the scene**: if the biggest thing that happens is not the
   longest scene, the chapter is not ready.
2. **The cost.** If it is empty, go back to `conflict-engine`. A chapter where the POV character
   only gains is filler regardless of how much happens in it.

**Most of Phase A is transcription.** The plan row already holds `temp`, `hooktype`, `event`,
`goal`, `obstacle`, `turn`, `cost` and `threads` — that is what planning is for. Open a card only
for what the row does not settle.

| decision | card |
|---|---|
| Which beat is played and which is reported | `story-craft/references/draft-card.md` — **first, always** |
| Scene count, the break, and per scene goal → obstacle → turn → exit | `scene-craft/references/draft-card.md`, `chapters.scenes_per_chapter` |
| What this chapter costs the POV character | `conflict-engine/references/draft-card.md` — never zero |
| POV character, and whether this is a switch | `pov-switch/references/draft-card.md` + the plan row |
| Which thread ops fire | `plot-threads/references/draft-card.md` |
| Which character sounds different today, and how | `character-development/references/draft-card.md` → `state/growth.md` |
| **The voice spread**: this chapter's speakers as matrix rows, side by side — and which of them differs from the MC on two or more axes | `voice-separation/references/draft-card.md` → `bible/cast/_voices.md` |
| Anyone new on the page: their **cast tier**, decided before they speak | `character-profile/references/draft-card.md` |
| **The offstage question**: what the world does this chapter that the MC doesn't know | `timeline-engine/references/draft-card.md` → `plan/timeline.md` |
| **The world channel**: the one thing about the world this chapter makes concrete, and whether a consequence, a friction or an assumed reference carries it | `world-texture/references/draft-card.md` |
| What the MC deduces, and from which on-page clue | `mc-intel-meter/references/draft-card.md` |
| **Who has to ask**: the thing this chapter needs known, whose map actually covers it, and who must go to someone else for it | `competence-map/references/draft-card.md` → `bible/cast/_competence.md` |
| Opening line strategy, closing hook | `hook-and-pacing/references/draft-card.md` |

**Conditional — check the condition first, and skip the card entirely if it is false.**

| condition | decision | card |
|---|---|---|
| chapter ≤ `opening.contract_by_ch + 2` | **The anchor debt**, and **the ceiling check**: if this chapter escalates, is the mechanism already on the page? | `story-opening/references/draft-card.md` |
| `scaling.shape` is not `none` | **The pressure**: what gap the arc wants, and only then who the opposition is | `power-scaling/references/draft-card.md` → `state/power.md` §6 |
| `mc.foreknowledge` is set | **The foreknowledge spend**: what is known, at what grain, what it costs, what it invalidates | `meta-knowledge/references/draft-card.md` → `state/foreknowledge.md` |
| anyone is `form_locked` | Which bodies are locked, and what they cannot do today | `mc-design/references/draft-card.md` → `state/body.md` |

Plus the **active modules** from Step 0.2, at the entry point the read-set named for each.

A card that does not settle its question is the one case for opening its owner's `SKILL.md`.

## Step 2 — Phase B: draft

Write straight through. Do not stop to self-edit; `revision-pass` handles that.

**Four cards stay open, and no others**: `narrator-voice`, `dialogue-voice`, `story-craft`, and
the `style:` block from the read-set's CONFIG. Everything else was decided in Phase A and is in
the brief. If you find yourself reopening cards mid-draft, the brief was incomplete — finish it
first, do not draft with twenty files in play.

**Write to the temperature.** The brief says `temp`. A `loud` chapter is written loud: shorter
paragraphs, people talking over each other, the narrator keeping up rather than commenting. A
`warm` chapter is allowed to land without being undercut. The single most reliable way to sound
like a machine is to write every chapter at the same pitch regardless of what is in it.

**Let sentences be plain.** Roughly a third of the chapter should carry information and nothing
else — no dash, no reversal, no irony, no lesson appended. *"The rice was untouched. The blanket
was still folded on the bed."* A narrator who loads every sentence has one attitude, and one
attitude for a whole book is the tell that no phrase list will catch
(`prose-quality` §Range before polish).

Hold these while writing:

- **Voice.** `narrator-voice/references/draft-card.md` — person, tense, distance, interiority, the
  distance curve. It does not change mid-chapter unless `pov-switch` says a switch is happening.
- **Dialogue.** Every named speaker satisfies their fingerprint
  (`dialogue-voice/references/draft-card.md`). If you cannot tell two characters apart with the
  tags removed, fix it now.
- **The four channels.** `"…"` speech · `'…'` direct thought, **1–3 for the whole chapter**, at
  decisions · `[…]` system text and in-world documents · and **unmarked free indirect discourse,
  which is where interiority actually lives** (`narrator-voice/references/draft-card.md`). Do not
  tag a marked thought with *she thought* — the mark already said it. An apostrophe is not a
  thought mark; a `'…'` inside a `"…"` is a nested quotation.
- **Enough dialogue to audit.** Target **25–40% inside `"…"`**, spoken aloud to another person
  (`dialogue-voice/references/draft-card.md`). Under 10% is a defect: on a silent cast every voice
  check in this toolkit no-ops. When two people are in a room the beat belongs to what they *say*,
  not to the POV character concluding it on their behalf — an analytical POV voice is the usual
  cause, and it quietly eats the scene.
- **Voice spread.** Hold each speaker's matrix row (`voice-separation`). Nobody but a declared
  mirror reasons at the MC's speed: somebody here is slower, or worse at saying it, and is right
  anyway. Beats come from each character's hands, never from the default gesture set.
- **Other minds, no interiority.** Non-POV characters think through their **first move** — what
  they reach for when the situation changes. The narration never enters a second head.
- **Walk-ons.** Three strokes: a five-minute want, one habit, one piece of their working world,
  plus one axis off default. No interiority, no backstory. Sketch them; log the line in step 5.
- **Intelligence and knowledge.** Every MC decision passes the `mc-intel-meter` trace test — the
  reader can name the on-page fact it came from. Every stated fact passes the `competence-map`
  provenance test. An unlisted domain is `none`, so somebody here says they do not know, asks the
  person who does, or is confidently wrong — which is more useful than blank.
- **Learning.** Practice is a clause, not a scene, unless a stage transition fires. Either way it
  took time from something else and the chapter says what.
- **Ground the scene.** `world-texture/references/draft-card.md` — two to four concrete details
  per scene, one non-visual, within 100 words of arriving, filtered through the POV character.
  The world's *rules* reach the reader by biting someone, not by being narrated.
- **Cut the connective tissue.** Enter late, leave early. No arrivals, no farewells, no walking
  between locations unless something happens on the way.
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

Readers arrive a day or a week later. Re-anchor in **one clause, inside a sentence doing other
work**: "The coat she'd taken off Dael's body still smelled of the undercroft." Never a paragraph,
never "As you'll remember".

## Step 3 — Write the file

`novels/<slug>/chapters/NNNN-<kebab-title>.md`, four-digit padded, with the frontmatter from
`chapters/_chapter-template.md` filled in — including **`event:`** and **`delivers:`**, both
decided in Phase A. They are not the same field: `event:` is what happened, `delivers:` is what
is different afterwards. A chapter with a strong `delivers:` and a vague `event:` is the failure
this pair exists to catch. Prose only in the body — the four channels and nothing else. No headings,
no author notes.

Leave `wordcount:` as the template holds it; Step 4 stamps it from the measured body after
revision. It is a recorded fact, not a target.

## Step 4 — Revise

Run `revision-pass`. It backs the chapter up, opens with the mechanical sweep
(`sw lint novels/<slug> -c <N>`), then runs the judgement passes — `prose-quality`, `mtl-detox`,
`bias-guard`, voice, competence, continuity. Fix what it finds, in the file.

When every pass is clean, stamp the measured count and the status:

```bash
python3 scripts/sw.py stamp novels/<slug> -c <N> --status revised --ledger
```

## Step 5 — Write state back

Run `continuity-summary` in **write mode**: CCS block, threads, growth, timeline, any new bible
facts. This step is not optional and not deferrable to "later". When the block is written,
`python3 scripts/sw.py state novels/<slug>` verifies it against the chapter on disk.

World bookkeeping, same pass: any new location anchor or durable social fact goes into `set>`,
then into `bible/world.md` or `bible/society.md`. An anchor never recorded drifts by its third
appearance.

Cast bookkeeping, same pass: every walk-on gets their roster line in `bible/cast/_extras.md` (or
their chapter appended to an existing one), every named person goes in `lexicon.md`, and anyone
at a third appearance or who changed the plot is promoted now, from what is already on the page.
A promotion also earns a row in `bible/cast/_voices.md` and one in `bible/cast/_competence.md`,
both placed against the existing cast rather than invented in isolation.

Foreknowledge bookkeeping, same pass, if `mc.foreknowledge` is set: every spend gets a row in
`state/foreknowledge.md` §3 with its cost, statuses move in §2, and any plot-changing spend moves
at least one *other* row toward `invalidated` (§4, the observer paradox). The block carries an
`fk>` line. Spending foreknowledge and leaving the ledger untouched is the same class of bug as
skipping the CCS block.

Power-curve bookkeeping, same pass, unless `scaling.shape` is `none`: every confrontation gets a
row in `state/power.md` §3 with its pressure and, at P ≥ +1, what the win cost. A tier advance
goes in §4 with all four requirements and §1 moves with it; a boost goes in §5 with its expiry and
debt. The block carries a `pwr>` line, and `sw curve` checks it agrees with §3.

Knowledge bookkeeping, same pass: a skill stage that advanced goes in the skill-ladder table of
`state/growth.md` with what caused it; a genuinely new domain a character acquired on the page goes
on the competence grid. If the chapter had to invent an expertise nobody had, record it — and say
so in the report, because it usually means the cast is missing a person.

## Step 6 — Report

Six lines to the user, no more:

```
Ch 42 — "The Ledger Room" → novels/<slug>/chapters/0042-the-ledger-room.md
Event: Rin is refused at the archive door and takes the ledger anyway.
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
