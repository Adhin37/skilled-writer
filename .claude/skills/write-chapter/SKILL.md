---
name: write-chapter
description: Draft the next chapter, orchestrating continuity, character, POV, conflict, pacing and quality into one procedure. Use when the user asks to write or continue a chapter, or says /novel-write.
metadata:
  type: skill
  tier: core
  force: structural
  when: always
  owns: [draft-phases, chapter-report]
---

# write-chapter

The main loop. This is the only skill that produces prose. Follow the steps in order; each one
is cheap, and skipping one is what produces the drift that ruins long serials.

---

## Step 0 — Load

1. Resolve the active novel (see `CLAUDE.md` §1). Read `novels/<slug>/novel.md`.
2. Note: `genre`, `narration.*`, `pov.*`, `mc.intel_tier`, `chapters.*`, `content.*`.

   The CONFIG block also resolves **active modules** — every skill this novel's config switches
   on, whether by an `optional:` toggle, by `genre`, or by a config gate like `content.romance`
   — and names each one's entry point: its draft card where it has one, its `SKILL.md` where it
   does not. A gated one prints its condition beside it. **Open those and no others.** A module
   that is not listed is off for this novel and costs nothing. An active one is *consulted this
   chapter*, not merely permitted.

   Without Python: read `optional:`, `genre` and `subgenre` in `novel.md`, and check the two
   config gates — `content.romance` for `lead-interest`, `pov.mode` for `pov-switch`. Each skill
   states its own condition as `metadata.when`. Resolve the list by hand, then say so in the
   report.
3. Determine the chapter number: highest existing file in `chapters/` + 1, unless told otherwise.
4. Run `continuity-summary` in **read mode** — `python3 scripts/sw.py readset novels/<slug> -c <N>`
   assembles it in one call, sliced rather than whole-file. You now have the read-set and the
   chapter brief. Steps 1 and 2 above are in its CONFIG block, so `novel.md` needs no separate
   read. Without Python, load the list in `continuity-summary` by hand.
5. Read the target row in `plan/chapters.md`. If it is missing or any of
   goal/obstacle/turn/cost/hook is blank, run `chapter-plan` for this row first. Do not draft
   from an incomplete row.

## Step 1 — Phase A: the brief (and stop)

**Drafting is three phases and this is the first one. It ends with you stopping.**

Phase A spends the cards below and produces **one brief**; Phase B drafts from that brief and four
cards, nothing else. Why it is split this way: `references/draft-cards.md`.

The brief is twelve lines — thirteen when the read-set printed a WATCH row — written into the
chat, not into a file.

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
watch    campaign-clause (3 of last 5) | speech-share (2 of last 5)
next     the quarter answers in nine days
```

**Then stop and show it to the user.** They approve it, change a line, or throw it out — the
cheapest gate in the toolkit, because a chapter that was going to be a thousand words of somebody
quietly feeling something gets caught for twelve lines instead of after the draft. Skip the stop
only if told to (`/novel-write --no-confirm`, or "just write the next five"): Phase A still
happens, you simply do not wait.

**Two gates, both before drafting.**

1. **The event**, as `chapter-plan` defines the field: what *happens*, in one clause a reader could
   retell. It is already in the plan row — check it is a real one rather than an abstract-state
   noun, which `sw lint` rejects outright. **And the event gets the scene**: if the biggest thing
   that happens is not the longest scene, the chapter is not ready.
2. **The cost.** If it is empty, go back to `conflict-engine`. A chapter where the POV character
   only gains is filler regardless of how much happens in it.

**The watch line** is the read-set's WATCH row, copied. Omit it when there was none.

**Most of Phase A is transcription.** The plan row already holds `temp`, `hooktype`, `event`,
`goal`, `obstacle`, `turn`, `cost` and `threads` — that is what planning is for. Open a card only
for what the row does not settle.

The read-set's **CARDS** block lists this chapter's cards, in order, with the conditional ones
already resolved against `novel.md` — and each card's own one-line statement of what it decides.
Open exactly those, in that order, plus the **active modules** from step 0.2 at the entry point
the read-set named for each.

It also prints **CARDS NOT OPENED** and why. If a condition there looks wrong for this chapter,
say so before drafting rather than opening the card anyway: a trigger nobody questions is how a
card silently stops applying.

Without Python: every draft card under `.claude/skills/` declares its own `phase`, `order` and
`when` in frontmatter. Open every phase-A card in `order`, skipping any whose `when`
is false for this novel, and say in the report that you resolved it by hand.

A card that does not settle its question is the one case for opening its owner's `SKILL.md`.

## Step 2 — Phase B: draft

Write straight through. Do not stop to self-edit; Phase C handles that.

**Four cards stay open, and no others**: `narrator-voice`, `dialogue-voice`, `story-craft`, and
the `style:` block from the read-set's CONFIG. Everything else was decided in Phase A and is in
the brief. If you find yourself reopening cards mid-draft, the brief was incomplete — finish it
first, do not draft with twenty files in play.

**Write to the temperature.** The brief says `temp`. A `loud` chapter is written loud: shorter
paragraphs, people talking over each other, the narrator keeping up rather than commenting. A
`warm` chapter is allowed to land without being undercut. The single most reliable way to sound
like a machine is to write every chapter at the same pitch regardless of what is in it.

**Let sentences be plain.** Roughly a third of the chapter carries information and nothing else.
`prose-quality` owns the range — what a plain sentence is, and why one attitude for a whole book is
the tell no phrase list catches.

Hold these while writing. Each names its owner, and the detail is there rather than here.

- **Voice and the four channels.** `narrator-voice/references/draft-card.md`. `'…'` direct thought
  stays **1–3 for the whole chapter**, at decisions; interiority lives unmarked, in free indirect
  discourse. Distance does not change mid-chapter unless `pov-switch` says a switch is happening.
- **Dialogue.** `dialogue-voice/references/draft-card.md`. Every named speaker satisfies their
  fingerprint, and **25–40% of the words sit inside `"…"`**, spoken aloud to another person. Under
  10% is a defect: on a silent cast every voice check in this toolkit no-ops.
- **Voice spread.** The brief's `speakers` line. Nobody but a declared mirror reasons at the MC's
  speed, and beats come from each character's hands, never the default gesture set.
- **Other minds, no interiority.** Non-POV characters think through their **first move** — what
  they reach for when the situation changes. The narration never enters a second head.
- **What is known, and by whom.** The brief's `asks` line. Every MC decision traces to an on-page
  fact the reader can name (`mc-intel-meter`); every stated fact has a provenance
  (`competence-map`). Somebody here does not know, and says so. Practice is a clause, not a scene.
- **Walk-ons.** Three strokes — a five-minute want, one habit, one piece of their working world —
  plus one axis off default. No interiority, no backstory. Log the line in step 5.
- **The world.** The brief's `world` line, at `world-texture`'s budget: two to four concrete
  details per scene, one non-visual, within 100 words of arriving, filtered through the POV
  character. The world's *rules* reach the reader by biting someone.
- **Shape and movement.** The brief fixed the scene split; the proportions it sits in are
  `scene-craft` §Chapter assembly, and the cuts are §Entering and leaving — enter late, leave
  early. **Chapter 1 has its own shape**, in `story-opening/references/chapter-one.md`.
- **Active modules.** Apply each active module's card as you write, not afterwards.
- **The watch line.** Whatever the brief's `watch` names, this draft does not do again — a clause
  here, a rewrite in Phase C.

## Step 3 — Write the file

`novels/<slug>/chapters/NNNN-<kebab-title>.md`, four-digit padded, with the frontmatter from
`chapters/_chapter-template.md` filled in — including **`event:`** and **`delivers:`**, both
decided in Phase A. They are not the same field: `event:` is what happened, `delivers:` is what
is different afterwards. A chapter with a strong `delivers:` and a vague `event:` is the failure
this pair exists to catch. Prose only in the body — the four channels and nothing else. No headings,
no author notes.

Leave `wordcount:` as the template holds it; Step 4 stamps it from the measured body after
revision. It is a recorded fact, not a target.

## Step 4 — Phase C: the gate

**Drafting is three phases and this is the last one. The chapter is not written until this passes.**

Run `revision-pass` in full and fix what it finds, **in the file**. There is no revise command
and it is not deferrable: a chapter reported at `status: drafted` is the same bug as one with no
CCS block, and the next read-set says so.

Two things this step owes the report. If Pass Z sends the chapter back to Phase B, redraft the
scene, gate the new text, and say that it happened. If the budget would not stretch to every audit
card, `revision-pass` says which passes may rotate — name the ones that ran without theirs.

When every pass is clean, stamp the measured count and the status:

```bash
python3 scripts/sw.py stamp novels/<slug> -c <N> --status revised --ledger
```

## Step 5 — Write state back

Run `continuity-summary` in **write mode**. That skill owns the procedure; the table is the list
it covers, so a glance says whether anything was missed. This step is not optional and not
deferrable to "later". When the block is written,
`python3 scripts/sw.py state novels/<slug>` verifies it against the chapter on disk.

| written | when |
|---|---|
| the CCS block, plus a `gate>` line naming what Phase C had to fix | always. `continuity-summary` owns when the line is present and when it is absent |
| a `cand>` line: the Phase A candidates you did not take, and why the taken one won | always, when the three-candidate step ran. It is the only place that step's output survives the conversation |
| a `z4>` line: Pass Z4's answer, or the literal `none` | always. `none` is a real answer and the reason the line exists — one is a chapter, a run of them is a habit |
| `state/threads.md`, `state/growth.md`, `state/timeline.md` | always |
| `set>` facts into `bible/world.md`, `bible/society.md`, `bible/lexicon.md` | a location anchor, price, custom or name reached the page. One never recorded drifts by its third appearance |
| a roster line in `bible/cast/_extras.md` | any walk-on. A third appearance or a changed plot promotes them **now**, earning rows in `_voices.md` and `_competence.md`, placed against the existing cast |
| `state/body.md` §1, §2, §4 | a `form_locked` character changed stage |
| `state/power.md` §3–§5, and the `pwr>` line | unless `scaling.shape` is `none`. `sw curve` checks the line agrees with §3 |
| `state/foreknowledge.md` §2–§4, and the `fk>` line | `mc.foreknowledge` is set. A plot-changing spend moves at least one *other* row toward `invalidated` — the observer paradox |
| the skill-ladder table in `state/growth.md` | a stage advanced, with what caused it |

If the chapter had to invent an expertise nobody in the cast had, record it **and say so in the
report** — it usually means the cast is missing a person.

## Step 6 — Report

Seven lines to the user, no more:

```
Ch 42 — "The Ledger Room" → novels/<slug>/chapters/0042-the-ledger-room.md
Event: Rin is refused at the archive door and takes the ledger anyway.
Delivers: Rin can no longer use the Guild's archive, and knows who closed it to him.
Cost: Rin loses Dael's trust; Echo-step now known to the Guild.
Gate: passed — cut a crowd-reaction block, replaced the ending. Every pass had its card.
Threads: opened T14 (forged seal), paid T09 (oath to Mira).
Next: ch 43 is planned — he reads the ledger. Say go, or tell me what to change.
```

**Lead with the delivery, and do not report a word count.** Reporting length is what taught the
drafting model to aim at it; the number lives in the frontmatter, where tools can read it.

**The `Gate:` line always says what Pass 6 found**, even when that is nothing.

Do not paste the chapter into chat unless asked.

---

## When something goes wrong, or the run is long

- **A drafted chapter feels wrong and you want the name of what is wrong** — open
  `references/failure-modes.md`. Thirty symptoms, each with its cause and the skill that owns
  the repair.
- **The user asked for several chapters, or the draft left the plan behind** — open
  `references/batch-and-replan.md`. The per-chapter loop rule, the 5-chapter check-in, the
  fresh-session rule for cost, and how to amend a plan row without abandoning the arc.
