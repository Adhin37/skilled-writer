---
name: revision-pass
description: Quality gate for a drafted chapter — runs continuity, character, voice-separation, intelligence, knowledge-and-competence, structure, world-delivery, bias, MTL-artifact, prose, delivery, opening-anchor, foreknowledge and channel-mechanics checks in a fixed order and fixes what it finds. A chapter passes on what it delivers, never on its length. Use after drafting any chapter, and when the user says /novel-revise.
---

# revision-pass

A chapter is not finished when it is drafted. This is the gate. Run the passes **in this order** —
structural fixes invalidate line edits, so line editing goes last. Keep it mechanical: each pass
is a search-and-decide, not a re-read of the whole novel.

## Before you start — this file does not carry other skills' checklists

It used to. That is what made it dangerous. A model reading only this file ran *every* pass at
checklist depth, and skills `CLAUDE.md` calls non-optional never loaded at all — measured on a
real run, `bias-guard`, `voice-separation`, `competence-map` and `prose-quality` were read **zero**
times across 200 turns while their boxes were ticked on every chapter.

So the passes that need judgement now live with the skill that owns the defect, as a small
**audit card**. You open the card. The card is short, so opening it is cheap, and it is written by
the owner, so nothing here is a paraphrase.

| pass | kind of defect | what to open |
|---|---|---|
| 0 Mechanical sweep | mechanical | nothing — run the commands |
| 1 Continuity | mechanical | nothing — the read-set is the authority |
| 2 Character + voice | **distributional** | `voice-separation/references/audit-card.md` · `character-profile/references/audit-card.md` |
| 3 Intelligence + knowledge | **distributional** | `mc-intel-meter/references/audit-card.md` · `competence-map/references/audit-card.md` |
| 4 Structure | mechanical | nothing |
| 5 World | judgement | `world-texture/references/audit-card.md` |
| 6 Bias | **distributional** | `bias-guard/references/audit-card.md` — **every chapter, never rotated** |
| 7 MTL detox | mechanical | nothing — the banned list is `sw lint`'s |
| 8 Prose + microtension | judgement | `prose-quality/references/audit-card.md` |
| 9 Delivery | judgement | nothing — the five questions are here in full |
| 9b Opening | **judgement** | `story-opening/references/audit-card.md`, chapters in range only |
| 9c Foreknowledge | **distributional** | `meta-knowledge/references/audit-card.md`, if `mc.foreknowledge` |
| 9d Theme | judgement | nothing — the restraint test is here in full |
| 9e Power curve | judgement | `power-scaling/references/audit-card.md`, if `scaling.shape` is not `none` |
| 10 Mechanics | mechanical | nothing |

**Run Pass 0 first.** It settles every mechanical row in seconds and for no tokens, which is what
buys the budget for the cards. A clean sweep is **not** a passed revision: it says nothing about
2, 3, 5, 6, 9 or 9d, and a green line must never be read as a bias pass.

If the budget will not stretch to every card, rotate — but **say in the report which passes ran
without their card**. Two are not rotatable: **Pass 6**, and **Pass 9c** whenever the MC knows the
future. Each guards a defect invisible in one chapter and unrecoverable once ten are written.

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

Open **`voice-separation/references/audit-card.md`** and, if the chapter has walk-ons,
**`character-profile/references/audit-card.md`**. Work them there.

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

`sw lint` searches the whole banned list and counts narration exclamation marks and rhetorical
questions. The first two boxes are its output; the rest are structural and are yours.

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

## Pass 9 — Delivery

**This is the pass that decides whether the chapter is finished.** It replaces the old word-count
check entirely. Length is not evidence of anything: a 1,600-word chapter that moves a relationship
is finished, and a 2,400-word chapter in which everyone talks and nothing changes is not.

Answer all five in one sentence each. Write the third into the chapter's `delivers:` frontmatter.

| | question | fails when |
|---|---|---|
| **Want** | What did the POV character want in this chapter? | The honest answer is "to react to things." A chapter with no want is a chapter of weather |
| **Friction** | What person, rule or scarcity stood in the way? | The only obstacle is the MC's own hesitation, twice running |
| **Change** | **What is materially different at the end?** | The exit state equals the entry state. This is the load-bearing question |
| **Cost** | What was paid, by whom? | Nothing. See `conflict-engine` — nothing is free |
| **Next** | What does the reader now need to see? | The hook asks a question the chapter already answered |

- [ ] All five answered without straining
- [ ] **Change** names a difference, not a summary of events. *"She asks about the recount"* is
      events; *"she is now someone Tsuru watches on purpose"* is a delivery
- [ ] `delivers:` in the frontmatter matches what the chapter actually did
- [ ] If something repeated from an earlier chapter, it **escalated** — a second refusal, a second
      failure, a second interrogation costs more than the first, or one of them is cut
- [ ] The chapter passes the skim test: a reader who skipped it would lose something nameable
- [ ] **Forecast test.** Could a reader predict the next chapter from this one's ending? If yes,
      the hook is a summary, not a hook
- [ ] Opening avoids the banned patterns; re-anchoring is one clause
- [ ] Chapter ends on its last strong beat; hook concrete, final position, type rotated

**Length**, for completeness: if the chapter is far outside `chapters.length_band`, look once and
ask whether the material was split in the wrong place. Then move on. Do not pad, do not trim, and
do not record a length judgement in the report.

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

## Pass 10 — Mechanics

- [ ] Frontmatter complete, including `delivers:`
- [ ] `wordcount:` is **measured**, never estimated, and re-measured if any pass changed the body.
      It is a recorded fact that later tools read, not a target — but a wrong fact propagates into
      `state/continuity.md` and corrupts every share computed from it. Run this **last**:

      ```bash
      python3 scripts/sw.py stamp novels/<slug> -c <n> --status revised --ledger
      ```

      It measures the body, writes `wordcount:` and `status:`, and corrects `wc:` in the CCS
      block. It rewrites the frontmatter only and never touches the prose. Without Python, measure
      with `wc -w` on the body and write both numbers by hand
- [ ] Scene breaks use `* * *`
- [ ] POV label present if the chapter switches and `label_switches` is true

**The four channels** (`narrator-voice` §The four channels; the marks come from `channels:` in
`novel.md`, and `sw lint` reads them from there):

- [ ] Speech, direct thought and meta each in their declared marks; free indirect **unmarked**
- [ ] Direct thought is **budgeted — 1–3 per chapter**, at moments of decision. A chapter where
      every interior beat wears quote marks has flattened its narrator into a thought bubble;
      convert the surplus back to free indirect discourse
- [ ] **No apostrophe was mistaken for a thought mark.** `don't`, `she'd`, `the boys' room` are not
      thought. Every thought opens at a word boundary and closes before punctuation or space
- [ ] Every thought mark **inside** a speech span is an ordinary nested quotation
- [ ] Meta blocks match the format in `lexicon.md`; none opens a chapter; no two run consecutively
- [ ] Italics do the **one** job `lexicon.md` assigns them, and no other
- [ ] Nothing else is markup — no headings, bold, lists, links or author notes in the prose body

---

## When something fails

Open **`references/fixing-and-reporting.md`** — the repair order, what to do when a fix
contradicts the plan or reveals a bible gap, the two-line report format, and standalone
`/novel-revise` use.

Set `status: revised` when every pass is clean. **Lead the report with what the chapter delivers**,
and never quote a word count.
