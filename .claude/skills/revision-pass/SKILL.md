---
name: revision-pass
description: Quality gate for a drafted chapter - continuity, character, voice, knowledge, structure, world, bias, prose and delivery checks in a fixed order. Use as write-chapter phase C, on every chapter.
---

# revision-pass

A chapter is not finished when it is drafted. This is the gate, and it is **Phase C of
`write-chapter`** — not a later step, not a command the user types. Every chapter arrives here
before it is reported, and does not leave until it is `status: revised`.

Run the passes **in this order** — structural fixes invalidate line edits, so line editing goes
last. Each pass is a search-and-decide, not a re-read.

## Pass Z — the story gate. Run this first, and be willing to stop here.

Sixteen passes in a fixed order is the right shape for *fixing* a chapter and the wrong shape for
deciding whether it is worth fixing. Run #2 ran all sixteen on every chapter and shipped five
`status: revised` chapters a reader flagged as machine-written on page one. Nothing in the sixteen
asked the only question that mattered. Three that do, gating all of it:

| | question | fails when |
|---|---|---|
| **Z1** | What **happens** — one clause, concrete verb, a target? | The honest answer needs an abstract noun. `trust`, `attention`, `tension` name what an event *did*; they are not it |
| **Z2** | Is that beat the **longest scene** in the chapter? | The biggest moment is reported or held at a distance while something smaller gets the room |
| **Z3** | Would a reader **click next**? | The last line is the fourth withheld beat in a row, or the hook asks what the chapter answered |

If Z1 or Z2 fails, **stop**. Do not run passes 0–10. A chapter whose central event never got
played does not have prose problems, and polishing it yields a well-written chapter nobody wants
to read — precisely what run #2 shipped, five times. `sw lint` reports the countable half:
`event` for Z1, `closer-sameness` for Z3. Z2 is yours.

Stopping here means **going back to Phase B** and playing the scene, then gating the new text. It
is the loop working, and the report says it happened.

---

## Before you start — this file does not carry other skills' checklists

It used to, and that is what made it dangerous: a model reading only this file ran every pass at
checklist depth while `bias-guard`, `voice-separation`, `competence-map` and `prose-quality` were
read **zero** times across 200 measured turns, boxes ticked on every chapter. So the judgement
passes now live with the skill that owns the defect, as a small **audit card** — cheap to open,
and written by the owner, so nothing here is a paraphrase.

| pass | kind of defect | what to open |
|---|---|---|
| Z Story gate | judgement | nothing — the three questions above |
| 0 Mechanical sweep | mechanical | nothing — run the commands |
| 1 Continuity | mechanical | nothing — the read-set is the authority |
| 2 Character + voice | **distributional** | `voice-separation/references/audit-card.md` · `character-profile/references/audit-card.md` |
| 3 Intelligence + knowledge | **distributional** | `mc-intel-meter/references/audit-card.md` · `competence-map/references/audit-card.md` |
| 4 Structure | mechanical | nothing |
| 5 World | judgement | `world-texture/references/audit-card.md` |
| 6 Bias | **distributional** | `bias-guard/references/audit-card.md` — **every chapter, never rotated** |
| 7 MTL detox | **distributional** | `mtl-detox/references/audit-card.md` — the banned list is `sw lint`'s; the structural half is not |
| 8 Prose + microtension | judgement | `prose-quality/references/audit-card.md` |
| 8b Register + house style | **distributional** | `prose-quality/references/ai-default-tells.md` — the tells this model produces once the MTL list is already clean |
| 9 Delivery | judgement | nothing — the five questions are here in full |
| 9b Opening | **judgement** | `story-opening/references/audit-card.md`, chapters in range only |
| 9c Foreknowledge | **distributional** | `meta-knowledge/references/audit-card.md`, if `mc.foreknowledge` |
| 9d Theme | judgement | nothing — the restraint test is here in full |
| 9e Power curve | judgement | `power-scaling/references/audit-card.md`, if `scaling.shape` is not `none` |
| 9f Pacing + build-up | **judgement** | `story-craft/references/audit-card.md` |
| 10 Mechanics | mechanical | `narrator-voice/references/audit-card.md` for the four channels |

**Run Pass 0 first.** It settles every mechanical row in seconds and for no tokens, which buys the
budget for the cards. A clean sweep is **not** a passed revision: it says nothing about Z, 2, 3,
5, 6, 9 or 9d, and is never a bias pass.

If the budget will not stretch to every card, rotate — but **say which passes ran without their
card**, in the report's `Gate:` line. Three never rotate: **Pass Z**, **Pass 6**, and **Pass 9c**
when the MC knows the future.

The budget is thinnest exactly here, and structurally so: phase A spent the draft cards and phase
B spent a chapter before this pass was reached. Rotating and saying so is honest. Ticking a box you
did not check is what put five machine-written chapters past sixteen passes.

---

## Pass 0 — Mechanical sweep

```bash
python3 scripts/sw.py lint novels/<slug> -c <n>     # this chapter
python3 scripts/sw.py cast novels/<slug>            # the two cast tables, as tables
python3 scripts/sw.py curve novels/<slug>           # the power curve, if scaling.shape is set
```

`lint` covers Pass 7 in full, the countable half of Pass 8, Pass 10 in full, the default-gesture
sweep in Pass 2, the anchor count in Pass 9b, and the ledger's agreement with the chapter. `cast`
settles the arithmetic in Passes 2 and 3 — the straddle rule, the wit cap, the three-way clash,
the deep-expertise budget. `curve` settles the arithmetic in Pass 9e — step size, gain cadence,
unpaid boost debts, pressure monotony and the `pwr>` line's agreement with the ledger. The sweep
tells you **where** to look and never **whether** it is a problem.

Findings print as `LEVEL path:line: [check] message`. A **DEFECT** is a named gate failure; a
**warn** wants a decision.

**If Python is unavailable**, run every pass by reading, and say in the report that the sweep did
not run. The scripts are an optimisation, never a dependency.

## Pass 1 — Continuity

Against the read-set from `continuity-summary`.

- [ ] No contradiction with the last five CCS blocks
- [ ] No character knows something their `kno>` history does not support
- [ ] Names, terms, titles and spellings match `bible/lexicon.md` exactly
- [ ] In-world time is consistent with `state/timeline.md`; travel times plausible
- [ ] Objects, injuries and possessions persist — the coat, the scar, the debt
- [ ] Nothing contradicts an established rule in `bible/world.md`, `society.md` or `power-system.md`
- [ ] Character positions match where the last chapter left them

**Form check** — only if a character in the chapter is `form_locked`. Read `state/body.md` §1–§2:

- [ ] Every physical description matches the CURRENT FORM row — nothing from a later stage
- [ ] No capability exceeded the stage's absolute limits: reach, strength, stamina, voice
- [ ] Others reacted to the body, not to the mind inside it
- [ ] Any adult diction from a child's body was noticed by someone, or deliberately masked
- [ ] A stage transition, if one fired, is logged in §4 with what it enables and what it costs

## Pass 2 — Character and voice

Open **`voice-separation/references/audit-card.md`**, and
**`character-profile/references/audit-card.md`** if the chapter has walk-ons **or introduces any
named character for the first time**. Work them there.

A first appearance is the half of this pass that has no script and the one a reader notices
first: run `sw cast` and read the debut ledger before deciding this pass has passed.

## Pass 3 — Intelligence and knowledge

Open **`mc-intel-meter/references/audit-card.md`** and
**`competence-map/references/audit-card.md`**. Two different things, and the pass fails most often
at the seam: a high intel tier waved through as a licence to know facts.

## Pass 4 — Structure

- [ ] Every scene has goal / obstacle / turn / cost
- [ ] No scene exits on a plain yes
- [ ] The chapter's cost is stateable in one concrete sentence
- [ ] At least two of the four conflict sources active
- [ ] Thread ops match the plan row; the ledger will be updated
- [ ] The `wld>` line is filled: the world did something offstage this chapter
- [ ] Any world-track event that fired is logged in the divergence ledger, with what it opened
- [ ] Crisis count is within `timeline.crisis_cap`; nothing took an `ending.non_negotiable`
- [ ] Skim test: name the one thing a reader would miss if they skipped this chapter

## Pass 5 — World

Open **`world-texture/references/audit-card.md`**. Runs after structure, because description
placement follows scene shape, and before bias, so anything it adds is still audited by Pass 6.

## Pass 6 — Bias — never skipped, never negotiable

Open **`bias-guard/references/audit-card.md`**. Every chapter. There is no script for this pass
anywhere in the toolkit, deliberately.

## Pass 7 — MTL detox

Open **`mtl-detox/references/audit-card.md`**. `sw lint` searches the whole banned list and
counts narration exclamation marks and rhetorical questions — the first two boxes are its output.
The rest are structural: no script can see a crowd-reaction block, price a confrontation, or hear
translationese in a rhythm, and a clean sweep says nothing about any of them.

- [ ] Zero banned phrases
- [ ] Zero exclamation marks in narration
- [ ] No crowd-reaction block
- [ ] No rank recital or system lecture
- [ ] No face-slap loop; every confrontation cost the winner something
- [ ] No paragraph saying the same thing three ways

## Pass 8 — Prose and microtension

Open **`prose-quality/references/audit-card.md`**. `sw lint` has already found the cut-list
phrases, filter verbs, repeated openings, same-length runs and the dialogue share; the card
carries what a script cannot hear.

## Pass 8b — Register and house style

Pass 7 catches MTL slop; Pass 8 catches weak lines. Neither catches prose with no bad sentences
and no range — what run #2 shipped.

Open `prose-quality/references/audit-card.md` §Register.

## Pass 9 — Delivery

**The pass that decides whether the chapter is finished**, and it replaced the old word-count
check entirely. Length is evidence of nothing.

Answer all five in one sentence each. Write the third into `delivers:` and the Z1 answer into
`event:` — different fields, failing in opposite directions. Run #2 wrote five strong `delivers:`
lines, every one describing a shift in somebody's interior state, which is exactly how a chapter
passes this pass while nothing happens in it.

| | question | fails when |
|---|---|---|
| **Want** | What did the POV character want here? | The honest answer is "to react to things." A chapter with no want is a chapter of weather |
| **Friction** | What person, rule or scarcity stood in the way? | The only obstacle is the MC's own hesitation, twice running |
| **Change** | **What is materially different at the end?** | The exit state equals the entry state. This is the load-bearing question |
| **Cost** | What was paid, by whom? | Nothing. See `conflict-engine` — nothing is free |
| **Next** | What does the reader now need to see? | The hook asks a question the chapter already answered |

- [ ] All five answered without straining, and `delivers:` matches what the chapter did
- [ ] **Change** names a difference, not a summary of events. *"She asks about the recount"* is
      events; *"she is now someone Tsuru watches on purpose"* is a delivery
- [ ] Anything repeated from an earlier chapter **escalated** — a second refusal or interrogation
      costs more than the first, or one of them is cut
- [ ] Skim test: a reader who skipped it would lose something nameable
- [ ] **Forecast test.** If a reader could predict the next chapter from this one's ending, the
      hook is a summary, not a hook
- [ ] Opening avoids the banned patterns; re-anchoring is one clause
- [ ] Chapter ends on its last strong beat; hook concrete, final position, type rotated

**Length**: if the chapter is far outside `chapters.length_band`, ask once whether the material
was split in the wrong place, then move on. Never pad, trim, or record a length judgement.

## Pass 9b — The opening — chapters ≤ `opening.contract_by_ch + 2` only

Skip entirely outside that range. Inside it, open
**`story-opening/references/audit-card.md`**.

## Pass 9c — Foreknowledge — only if `mc.foreknowledge` is set

Open **`meta-knowledge/references/audit-card.md`**. Not rotatable.

## Pass 9d — Theme

Skip if `theme.controlling_idea` is empty. The measured failure mode of machine-written fiction is
not an absent theme but a **narrated** one: AI narrators state the story's meaning outright about
77% of the time against 52% for human writers. So this pass tests restraint, not presence.

- [ ] **No narration sentence states the lesson.** The narrator does not explain what the book
      means, what a character has learned, or what any of it says about people
- [ ] If the controlling idea is spoken aloud, a **character** speaks it — and is either wrong
      about it, or pays for being right
- [ ] `theme.counter_case` is alive: somebody in this arc argues the other side and is allowed to
      be persuasive. If the counter-case has never won a scene, the theme is a sermon
- [ ] The chapter tests the idea through a choice rather than through a conversation about it

## Pass 9e — The power curve — only if `scaling.shape` is not `none`

Open **`power-scaling/references/audit-card.md`**. Run `sw curve` first if you have not: it finds
the step-size, cadence, unpaid-debt, monotony and ledger-agreement defects, which leaves the card
the three things a script cannot see — whether the gain was earned on the page, whether the
opponent is a person or a number, and whether the win felt free.

This pass sits after delivery because a chapter that delivers nothing has no curve to audit, and
before Pass 10 so a corrected tier still reaches the frontmatter and the CCS `pwr>` line.

## Pass 9f — Pacing and build-up

Open **`story-craft/references/audit-card.md`**. Pass 9 asks whether the chapter delivers; this asks
whether it delivered at the **right size**, which a delivery test cannot see — a chapter that
summarises its own turning point still has a want, a friction, a change, a cost and a hook.

`sw lint` prints a **pacing** line (summary markers, words before the first scene, summary-shaped
paragraph share). It says where to look and settles nothing: a chapter can skip its most important
beat without one past-perfect clause, by starting after it.

The repair is never more words. It is reallocation — a reported beat becomes a played one, and a
played bridge goes back to being a bridge.

## Pass 10 — Mechanics

- [ ] Frontmatter complete, including `event:` and `delivers:`
- [ ] `wordcount:` is **measured**, never estimated, and re-measured if any pass changed the body.
      A wrong count propagates into `state/continuity.md` and corrupts every share computed from
      it. Run this **last** — it rewrites frontmatter only, never the prose:

      ```bash
      python3 scripts/sw.py stamp novels/<slug> -c <n> --status revised --ledger
      ```

      Without Python, measure the body with `wc -w` and write both numbers by hand
- [ ] Scene breaks use `* * *`
- [ ] POV label present if the chapter switches and `label_switches` is true

**The four channels** — open `narrator-voice/references/audit-card.md`. Hard rule 7 is that
skill's to enforce, and this file does not carry other skills' checklists.

---

## When something fails

Open **`references/fixing-and-reporting.md`** — the repair order, what to do when a fix
contradicts the plan or reveals a bible gap, the report format, and re-gating a chapter that was
drafted earlier.

Set `status: revised` when every pass is clean. **Lead the report with what the chapter delivers**,
and never quote a word count. Inside `write-chapter` this pass reports as the step 6 `Gate:` line,
and the block's `gate>` line records what it fixed — which builds the next chapter's WATCH row.
