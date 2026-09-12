---
name: revision-pass
description: Quality gate for a drafted chapter - continuity, character, voice, knowledge, structure, world, bias, prose and delivery checks in a fixed order. Use as write-chapter Phase C, on every chapter.
metadata:
  type: skill
  tier: core
  force: structural
  when: always
  owns: [pass-order, story-gate, gate-report]
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
| **Z4** | Name the thing here **a competent hack would not have written**. | The honest answer is nothing. Everything in the chapter is the obvious version, done well |

**Z4 is the one that can fail a chapter for being safe**, and it is the only question in the gate
that can. Z1 to Z3 are structural, and a chapter can satisfy all three and still be entirely
predictable — which is a fair description of what run #2 shipped past sixteen passes. A hundred
prohibitions cannot produce a surprise; they can only remove the bad ways of failing to have one
(`CLAUDE.md` §5, and `docs/creative-latitude.md` for the measurement).

What counts as an answer: a choice the reader did not see coming and believes afterwards · a
character who wanted the opposite of what the scene needed · a detail nobody would have invented
who had not thought about this world · a beat that costs the story something it will not get back.
What does not: a stylistic flourish, a withheld reveal, an ironic last line, or the chapter being
well written.

A failed Z4 is **not** a stop. **Write the answer to the block's `z4>` line, `none` included** —
the only trace this pass leaves, and one written to flatter the chapter defeats the point of
asking. Name the one place it could have taken the riskier option, and carry that into the next
brief — habits are invisible in one chapter. Three failures in five is the finding, and the
repair is in Phase A's three candidates (`story-craft`'s card), not in the prose.

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

Six passes have no other owner — 1, 4, 7's structural half, 9's, 9d and 10. Their checks moved
one file down to **`references/owned-passes.md`**, written as check / failure / cheapest repair,
so this body stays the pass order and the gates rather than a checklist nobody opened a source
for.

Run `python3 scripts/sw.py kb passes novels/<slug> -c <N>`. It names the audit card for each
pass below, with 9b, 9c and 9e already resolved against `novel.md`, so a pass whose card does not
apply to this novel is not left for you to work out. Without Python: every audit card declares
its `pass` in frontmatter — open the one whose `pass` matches the row you are on.

**Active modules arrive the same way.** A module this novel switches on — by an `optional:`
toggle or by `genre` — carries an audit card with a `pass` like everything else, and `kb passes`
prints it in the row it belongs to rather than as a separate stage. Open the card, never the
module's `SKILL.md`. The command also prints what did **not** open and why, which is the only
way a trigger that has quietly gone wrong becomes visible.

| pass | kind of defect | what to open |
|---|---|---|
| Z Story gate | judgement | nothing — the three questions above |
| 0 Mechanical sweep | mechanical | nothing — run the commands |
| 1 Continuity | mechanical | `references/owned-passes.md` §Pass 1 — the read-set is the authority |
| 2 Character + voice | **distributional** | — |
| 3 Intelligence + knowledge | **distributional** | — |
| 3b Reading people | **distributional** | — |
| 4 Structure | mechanical | three cards, four owners — `references/owned-passes.md` §Pass 4 lists them |
| 5 World | judgement | — |
| 6 Bias | **distributional** | — **every chapter, never rotated** |
| 7 MTL detox | **distributional** | `references/owned-passes.md` §Pass 7 — the banned list is `sw lint`'s; the structural half is not |
| 8 Prose + microtension | judgement | — |
| 8b Register + house style | **distributional** | `prose-quality/references/ai-default-tells.md` — the tells this model produces once the MTL list is already clean |
| 9 Delivery | judgement | `references/owned-passes.md` §Pass 9, plus `hook-and-pacing`'s card |
| 9b Opening | **judgement** | chapters in range only — `kb passes` resolves it |
| 9c Foreknowledge | **distributional** | only if `mc.foreknowledge` — not rotatable |
| 9d Theme | judgement | `references/owned-passes.md` §Pass 9d |
| 9e Power curve | judgement | only if `scaling.shape` is not `none` |
| 9f Pacing + build-up | **judgement** | — |
| 10 Mechanics | mechanical | `references/owned-passes.md` §Pass 10, and the four channels |

**Each card binds at its owner's force**, and `kb passes` marks the two that are not
`structural`. It changes what a finding obliges you to do:

| force | a finding means | owed to the report |
|---|---|---|
| **absolute** | fix it. There is no other outcome, and no reason is accepted | nothing — it is simply fixed |
| **structural** | fix it, or keep it and say why in the `Gate:` line | one clause |
| **stylistic** | **decide.** Keep it whenever the sentence does something the plain version would not | nothing |

A stylistic card that comes back with findings you deliberately kept is a card that worked. Those
rules exist to catch a *habit* rather than a sentence, so read them across the chapter and spend
the latitude they give you — `prose-quality` §Range before polish and §When to break these state
what its own rules are protecting, and `CLAUDE.md` §How hard each of these binds sets the three
forces.

**Run Pass 0 first.** It settles every mechanical row in seconds and for no tokens, which buys the
budget for the cards. A clean sweep is **not** a passed revision: it says nothing about Z, 2, 3,
5, 6, 9 or 9d, and is never a bias pass.

If the budget will not stretch to every card, rotate — but **say which passes ran without their
card**, in the report's `Gate:` line. Three never rotate: **Pass Z**, **Pass 6**, and **Pass 9c**
when the MC knows the future.

The budget is thinnest exactly here, and structurally so: Phase A spent the draft cards and phase
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

Against the read-set, which is the authority. Seven checks and the `form_locked` form check:
**`references/owned-passes.md` §Pass 1**.

## Pass 2 — Character and voice

Open **`voice-separation/references/audit-card.md`** — the cast as separate minds, and, in its
second half, whether anybody has *become* somebody else (`character-development`'s concepts, on
the same card because the two fail together). Then
**`dialogue-voice/references/audit-card.md`** for the lines. Add
**`character-profile/references/audit-card.md`** if the chapter has walk-ons **or introduces any
named character for the first time**, and **`pov-switch/references/audit-card.md`** when
`pov.mode` is not `single`. Work them there.

If the budget will not carry all four, drop `character-profile`'s first and `pov-switch`'s second,
and name them in the `Gate:` line.

A first appearance is the half of this pass that has no script and the one a reader notices
first: run `sw cast` and read the debut ledger before deciding this pass has passed.

## Pass 3 — Intelligence and knowledge

Open **`mc-intel-meter/references/audit-card.md`** and
**`competence-map/references/audit-card.md`**. Two different things, and the first card names the
seam they fail at.

## Pass 3b — Reading people

On **`mc-intel-meter`'s card**, already open from Pass 3. It sits here rather than with character
because it audits the same kind of claim: Pass 3 asks whether anybody knew something they should
not, and this asks whether anybody *understood* something they should not. `social-perception`
owns the rules; the card's second half carries them.

## Pass 4 — Structure

Three cards: **`scene-craft`** (goal, obstacle, turn, exit — already open from its Pass 9 duty),
**`conflict-engine`** (what the chapter cost) and **`plot-threads`** (the ops against the ledger,
**and `timeline-engine`'s world track and ending contract** on its second half — one card, two
owners). The skim test is the only row with no other owner:
**`references/owned-passes.md` §Pass 4**.

## Pass 5 — World

Open **`world-texture/references/audit-card.md`**. It runs after structure for the reason that card
gives, and before bias so that anything it adds is still audited by Pass 6.

## Pass 6 — Bias — never skipped, never negotiable

Open **`bias-guard/references/audit-card.md`**. Every chapter, and never rotated. That skill
explains why it has no script.

## Pass 7 — MTL detox

Open **`mtl-detox/references/audit-card.md`**. `sw lint` searches the whole banned list and counts
narration exclamation marks and rhetorical questions — that is the countable half, and a clean
sweep says nothing about the rest. The five structural checks no script can see are in
**`references/owned-passes.md` §Pass 7**.

## Pass 8 — Prose and microtension

Open **`prose-quality/references/audit-card.md`**. `sw lint` has already found the cut-list
phrases, filter verbs, repeated openings, same-length runs and the dialogue share; the card
carries what a script cannot hear.

## Pass 8b — Register and house style

Pass 7 catches MTL slop; Pass 8 catches weak lines. Neither catches prose with no bad sentences
and no range — what run #2 shipped.

Open `prose-quality/references/audit-card.md` §Register.

## Pass 9 — Delivery

**The pass that decides whether the chapter is finished**, and it replaced the old word-count check
entirely. Length is evidence of nothing.

Open **`scene-craft/references/audit-card.md`** — `scene-craft` owns the delivery test, and the card
carries the five questions and the scene-level checks. Write the **Change** answer into `delivers:`
and the Z1 answer into `event:`: two fields that fail in opposite directions. Run #2 wrote five
strong `delivers:` lines, every one describing a shift in somebody's interior state, which is
exactly how a chapter passes this pass while nothing happens in it.

Also open **`hook-and-pacing/references/audit-card.md`**: the chapter's first and last sentences
carry most of a serial's retention, and both of their defects are distributional — read against
the previous five chapters, never scored on this one. What is left over belongs to this pass
alone: **`references/owned-passes.md` §Pass 9**.

## Pass 9b — The opening — chapters ≤ `opening.contract_by_ch + 2` only

Skip entirely outside that range. Inside it, open
**`story-opening/references/audit-card.md`**.

## Pass 9c — Foreknowledge — only if `mc.foreknowledge` is set

Open **`meta-knowledge/references/audit-card.md`**. Not rotatable.

## Pass 9d — Theme

Skip if `theme.controlling_idea` is empty. This pass tests **restraint, not presence** — the
measured failure of machine-written fiction is a narrated theme, not an absent one. Four checks:
**`references/owned-passes.md` §Pass 9d**.

## Pass 9e — The power curve — only if `scaling.shape` is not `none`

Open **`power-scaling/references/audit-card.md`**. Run `sw curve` first if you have not: it finds
the step-size, cadence, unpaid-debt, monotony and ledger-agreement defects, which leaves the card
the three things a script cannot see — whether the gain was earned on the page, whether the
opponent is a person or a number, and whether the win felt free.

It sits after delivery for the reason its card gives, and before Pass 10 so a corrected tier still
reaches the frontmatter and the CCS `pwr>` line.

## Pass 9f — Pacing and build-up

Open **`story-craft/references/audit-card.md`**. Pass 9 asks whether the chapter delivered; this
asks whether it delivered at the **right size**, which no delivery test can see. `story-craft` owns
the scene-or-summary call and the repair, which is never more words.

`sw lint` prints a **pacing** line — summary markers, words before the first scene, summary-shaped
paragraph share. It says where to look and settles nothing.

## Pass 10 — Mechanics

Frontmatter, scene breaks, the POV label, and the measured word count — **`references/owned-passes.md`
§Pass 10**. Stamping runs **last**, because a pass that changes the body changes the count:

```bash
python3 scripts/sw.py stamp novels/<slug> -c <n> --status revised --ledger
```

**The four channels** are `narrator-voice`'s to enforce — open that skill's audit card. This file
does not carry other skills' checklists.

---

## When something fails

Open **`references/fixing-and-reporting.md`** — the repair order, what to do when a fix
contradicts the plan or reveals a bible gap, the report format, and re-gating a chapter that was
drafted earlier.

Set `status: revised` when every pass is clean. **Lead the report with what the chapter delivers**,
and never quote a word count. Inside `write-chapter` this pass reports as the step 6 `Gate:` line,
and the block's `gate>` line records what it fixed — which builds the next chapter's WATCH row.
