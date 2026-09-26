---
name: write-chapter
description: Draft the next chapter, orchestrating continuity, character, POV, conflict, pacing and quality into one procedure. Use when the user asks to write or continue a chapter, or says /novel-write.
metadata:
  type: skill
  tier: core
  force: structural
  when: always
  role: [draft, coordinate]
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
   entry note. Steps 1 and 2 above are in its CONFIG block, so `novel.md` needs no separate
   read. Without Python, load the list in `continuity-summary` by hand.

   Its header names its own last line, `# END READ-SET`. If you cannot see that line, it reached
   you truncated - the harness shows a long output as a preview plus a saved file - so `Read`
   the saved file in full before anything else. If it prints a **RESUME** line, the disk says
   this chapter is already under way: start where that line says, not at Phase A.
5. Read the target row in `plan/chapters.md`. If it is missing, or any of `event`, `temp`,
   `hooktype`, goal/obstacle/turn/cost/hook - or in the opening arc `world entry` - is blank,
   stop and say so in your return - the architect completes the row (`chapter-plan`). Do not
   draft from an incomplete row, and do not fill it in yourself: `plan/` is design's.

## Step 1 — Phase A: the brief (and stop)

**Drafting is three phases and this is the first one. It ends with you stopping.**

Phase A spends the cards below and produces **one brief**; Phase B drafts from that brief and four
cards, nothing else. Why it is split this way: `roles/draft/write-chapter.card-index.md`.

The brief is thirteen lines — fourteen when the read-set printed a WATCH row.

```
Ch 12 — "The Second Quarter"
event    Wren files the counter-claim and is put out of the house
temp     loud          hooktype  decision
scene 1  (~35%) goal / obstacle / turn
scene 2  (~55%) goal / obstacle / turn   <- the event happens HERE, longest scene
cost     she loses the apprenticeship, and Maro will not look at her
gives    Noor walks her home the long way and lets her say none of it
speakers Wren, Hesk, Maro   (Hesk differs from Wren on intel + articulacy)
world    the levy office charges for its own paperwork
asks     Wren does not know what a counter-claim costs; she has to ask Noor
threads  ^T02  vT04
cand     1:she pays the levy 2:she talks Maro into paying -> took 3, the other two keep the house
watch    campaign-clause (3 of last 5) | speech-share (2 of last 5)
next     the quarter answers in nine days
```

The **`cand` line is `story-craft`'s three candidates** — the two you did not take, numbered as its
card numbers them, and why the taken one won. It is in the brief rather than only in your head
because this is where the user can still say *take the second one*, and because step 5 copies it
instead of remembering it.

The **`gives` line** is the other half of `cost` — the one thing here worth the price, or `none`
(`conflict-engine` §What the chapter gives back). It carries into the block as `gav>`, where a run
of `none` is the finding. Omit both at `tone.warmth: cold`.

**Write it to `novels/<slug>/state/brief.md` before you stop**, as the fenced block the template
shows, opening on `Ch <n> —`, under a first line `status: proposed`. One file, overwritten every
chapter. It is the only decision in the loop that otherwise exists solely in the conversation, and
a conversation is the one place state does not survive: run #5 lost a chapter's candidates outright
when the session holding them died, and `cand> unrecorded` is what the ledger got.

**Then stop and return it, headed `BRIEF READY`.** The approval comes back through the
coordinator: approved, a line changed, or thrown out — the cheapest gate in the toolkit, because a
chapter that was going to be a thousand words of somebody quietly feeling something gets caught
for thirteen lines instead of after the draft. On approval, apply any change and flip the first
line to `status: approved`; that file is what Phase B drafts from and what step 5 copies. Skip the
stop only if told to (`/novel-write --no-confirm`, or "just write the next five"): write the brief
as `approved` and go on.

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

Without Python: every draft card under `roles/draft/` declares its own `phase`, `order` and
`when` in frontmatter. Open every phase-A card in `order`, skipping any whose `when`
is false for this novel, and say in the report that you resolved it by hand.

A card that does not settle its question is a finding, not a door: decide from the brief and name
the card in your report. The owner's `SKILL.md` is design's to open, and your read guard refuses it.

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

- **Voice and the four channels.** `roles/draft/narrator-voice.draft-card.md`. `'…'` direct thought
  stays **1–3 for the whole chapter**, at decisions; interiority lives unmarked, in free indirect
  discourse. Distance does not change mid-chapter unless `pov-switch` says a switch is happening.
- **Dialogue.** `roles/draft/dialogue-voice.draft-card.md`. Every named speaker satisfies their
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
  early. **Chapter 1 has its own shape**, in `roles/draft/story-opening.chapter-one.md`.
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

Leave `wordcount:` as the template holds it; step 5 stamps it from the measured body, after the
gate and the state write. It is a recorded fact, not a target.

## Step 4 — Phase C: the gate

**Drafting is three phases and this is the last one. The chapter is not written until this passes
— and it is not yours to run.**

**Stop and return `READY FOR GATE`** with the chapter's path. The coordinator hands the chapter to
the `gate` agent, a context that has not watched this chapter being written, which is the whole
point of it: a gate that remembers why each line seemed worth it is not reading the chapter, it is
remembering it. The brief and the Phase A candidates stay with you, because a gate told what the
chapter was reaching for grades it on the reach. The coordinator summons it rather than you
because it decides which role runs next (`CLAUDE.md` §10), and because a gate you spawned in the
background would report to the coordinator, not to you, in a non-interactive harness.

This is still Phase C. There is no revise command, the gate is summoned by the procedure and
never by the user, and it is not deferrable: a chapter reported at `status: drafted` is the same
bug as one with no CCS block, and the next read-set says so.

The gate's hand-back comes back to you verbatim, and is on file in `state/gate.md`:

| the hand-back carries | you do |
|---|---|
| a `Gate:` line | condense it into the block's `gate>` - a dozen words, and no `gate>` line at all when the gate changed nothing (`continuity-summary`) |
| a `z4>` answer | copy it to the block's `z4>` from `state/gate.md`, the literal `none` included |
| `SENT BACK` | redraft the scene it names — back to Phase B — write the file, return `READY FOR GATE` again, and say in the report that it happened |
| `For design:` items | carry every one into your report's `Bible:` line |
| passes that ran without their card | name them in the step 6 report |

The gate sets `status: gating` as its first act and `gated` as its last, on a pass. Neither is
finished: `revised` is stamped after step 5, and the next read-set names a chapter left at either.

If no gate agent can be summoned, the coordinator runs `revision-pass` inline and says so in the
report — never you: your read guard refuses the gate's cards, and an inline gate is weaker
exactly because its runner already knows what the chapter meant.

## Step 5 — Write state back

Run `continuity-summary` in **write mode**. It owns the list: the CCS block and its three
step-proof lines — `cand>` and `gav>` **copied** from `state/brief.md`, `z4>` copied from the
gate's hand-back in `state/gate.md`, never recalled — the state files, what goes in your report's
`Bible:` line rather than into `bible/`, and the stamp, which comes last. This step is not optional and not
deferrable to "later".

## Step 6 — Report

Eight lines, no more:

```
Ch 42 — "The Ledger Room" → novels/<slug>/chapters/0042-the-ledger-room.md
Event: Sarel is refused at the archive door and takes the ledger anyway.
Delivers: Sarel can no longer use the Guild's archive, and knows who closed it to him.
Cost: Sarel loses Tibbe's trust; Echo-step now known to the Guild.
Gate: passed — cut a crowd-reaction block, replaced the ending. Pass 6 clean. Every pass had its card.
Threads: opened T14 (forged seal), paid T09 (oath to Mira).
Bible: set> the archive seals at the second bell; walk-on the door-warden (first appearance).
Next: ch 43 is planned — he reads the ledger. Say go, or tell me what to change.
```

**`Bible:` is `none` or a list**, and a list goes to the architect before the next chapter's
Phase A: every fact the page established, every walk-on and promotion, every design gap the gate
named, and `replan` when the chapter left its row. The coordinator dispatches the fold; you name
what it is.

**Lead with the delivery, and do not report a word count.** Reporting length is what taught the
drafting model to aim at it; the number lives in the frontmatter, where tools can read it.

**The `Gate:` line always says what Pass 6 found**, even when that is nothing.

Do not paste the chapter into chat unless asked.

---

## When something goes wrong, or the run is long

- **A drafted chapter feels wrong and you want the name of what is wrong** — open
  `roles/draft/write-chapter.failure-modes.md`. Thirty symptoms, each with its cause and the skill that owns
  the repair.
- **The user asked for several chapters, or the draft left the plan behind** — open
  `roles/draft/write-chapter.batch-and-replan.md`. The per-chapter loop rule, the 5-chapter check-in, the
  fresh-session rule for cost, how to resume a chapter an interruption stopped, and how a draft
  that left its row gets the plan amended without abandoning the arc.
