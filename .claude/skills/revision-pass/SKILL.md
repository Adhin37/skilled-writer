---
name: revision-pass
description: Quality gate for a drafted chapter — runs continuity, character, voice-separation, intelligence, knowledge-and-competence, structure, world-delivery, bias, MTL-artifact, prose, delivery, opening-anchor, foreknowledge and channel-mechanics checks in a fixed order and fixes what it finds. A chapter passes on what it delivers, never on its length. Use after drafting any chapter, and when the user says /novel-revise.
---

# revision-pass

A chapter is not finished when it is drafted. This is the gate. Run the passes **in this order** —
structural fixes invalidate line edits, so line editing goes last.

Keep it mechanical. Each pass is a search-and-decide, not a re-read of the whole novel.

## Before you start — which passes need their skill file open

The checklists below are condensed on purpose, so the cheap passes stay cheap. That has one
failure mode worth naming plainly, because it is silent: a model that reads only this file runs
*every* pass at checklist depth, and skills `CLAUDE.md` calls non-optional never load at all.
Measured on a real run — `bias-guard`, `voice-separation`, `competence-map` and `prose-quality`
were read **zero** times across 200 turns, while their boxes were ticked on every chapter.

A checklist is sufficient for a **mechanical** defect — one you find by searching for a string or
counting something. It is not sufficient for a **distributional** defect, which is invisible in
any single line and only appears across a whole cast, chapter or arc.

| pass | kind of defect | load the source skill? |
|---|---|---|
| 1 Continuity | mechanical | no — the read-set is the authority |
| 2 Character + voice | **distributional** | **yes — `voice-separation`**, for the matrix and the axes |
| 3 Intelligence + knowledge | **distributional** | **yes — `competence-map`**, for provenance and the ladder |
| 4 Structure | mechanical | no |
| 5 World | judgement | `world-texture` if anything fails |
| 6 Bias | **distributional** | **yes — `bias-guard`, every chapter.** Non-negotiable means the file gets read |
| 7 MTL detox | mechanical | no — the banned list here is complete |
| 8 Prose | judgement | `prose-quality` if anything fails |
| 9 Delivery | judgement | no — the five questions are here in full |
| 9b Opening | **judgement** | **yes — `story-opening`**, on chapters in range. §1 and §3 cannot be checklisted |
| 9c Foreknowledge | **distributional** | **yes — `meta-knowledge`**, if `mc.foreknowledge` is set |
| 10 Mechanics | mechanical | no |

Three files, every chapter: `voice-separation`, `competence-map`, `bias-guard`. Two more
conditionally: `story-opening` while the novel is inside its opening arc, `meta-knowledge` whenever
the MC knows the future. If that does not fit the budget, rotate the unconditional three on a fixed
schedule — but then **say in the report which passes ran at checklist depth**, so a ticked box is
never mistaken for an audit that did not happen. **The conditional two are not rotatable**: they
each guard a defect that is invisible in a single chapter and unrecoverable once ten are written.

---

## Pass 1 — Continuity (structural)

Against the read-set from `continuity-summary`.

- [ ] No contradiction with the last five CCS blocks
- [ ] No character knows something their `kno>` history does not support
- [ ] Names, terms, titles and spellings match `bible/lexicon.md` exactly
- [ ] In-world time is consistent with `state/timeline.md`; travel times plausible
- [ ] Objects, injuries and possessions persist (the coat, the scar, the debt)
- [ ] Nothing contradicts an established rule in `bible/world.md`, `bible/society.md` or
      `bible/power-system.md`
- [ ] Character positions match where the last chapter left them

**Form check** — only if any character in the chapter has `form_locked: true`. Read
`state/body.md` §1–§2 and verify against every sentence describing them:

- [ ] Every physical description matches the CURRENT FORM row — nothing from a later stage
- [ ] No capability exceeded the stage's absolute limits (reach, strength, stamina, voice)
- [ ] Others reacted to the body, not to the mind inside it
- [ ] Any adult diction from a child's body was noticed by someone, or deliberately masked
- [ ] A stage transition, if one fired, is logged in §4 with what it enables and what it costs

## Pass 2 — Character

- [ ] Every named speaker matches their behaviour rules, or breaks one *as an event*
- [ ] Voice deltas from `state/growth.md` are applied
- [ ] Tag-removal test: speakers identifiable without attributions
- [ ] No character acted out of character for the plot's convenience
- [ ] Any rung advance was triggered, dramatised, and is audible in dialogue
- [ ] No voice delta moved a character onto the MC's axes
- [ ] Antagonists present want something and are competent at something

**Voice separation** (`voice-separation`) — the defect that survives a clean tag-removal test,
because the fingerprints differ and the minds behind them do not:

- [ ] Transplant test — the MC's most characteristic line does not fit any other character's mouth
- [ ] At least one speaker differs from the MC on two or more axes (intel, articulacy, wit, heat,
      turn length, body)
- [ ] No two speakers in a scene share intel + articulacy + wit
- [ ] Turn lengths held; nobody drifted toward the MC's
- [ ] Wit is confined to the characters who have it, at the pressure that triggers it — nobody
      became funny because the scene had room
- [ ] Every action beat is that character's hand-habit or pressure move; zero instances of *nodded,
      shrugged, sighed, raised an eyebrow, crossed their arms, let out a breath* as identification
- [ ] Non-POV minds shown through first moves; no second head entered
- [ ] Narration draws its metaphors from this POV's thought unit
- [ ] Any low-intel character is competent at their own work and right about something concrete —
      nobody exists in this chapter to be corrected
- [ ] **Mirrors**: a clone, avatar or double sharing the original's voice is declared with
      `mirror:` and `convergence:`; what has diverged since `diverged_ch` shows; the reader can
      tell which is speaking, or a character on the page cannot either

**Walk-ons** — for every minor character in the chapter:

- [ ] Swap test: their scene could not be handed to a different extra unchanged
- [ ] Three strokes present — a want inside the scene, one habit, one piece of their working world
- [ ] One axis off default, so they are not speaking in the narrator's register
- [ ] No interiority, no backstory paragraph, no arc granted to a tier-C character
- [ ] Nobody was over-characterised on the way to dying; a death this chapter was set up earlier
- [ ] Anyone at a third appearance, or who changed the plot, is promoted and profiled
- [ ] Every named walk-on has a roster line and a lexicon entry

## Pass 3 — Intelligence and knowledge (`mc-intel-meter`, `competence-map`)

Two different things, and the pass fails most often at the seam: a high tier waved through as a
licence to know facts.

**Intelligence**

- [ ] Every MC decision passes the trace test — name the on-page fact behind it
- [ ] None of the seven floor rules violated
- [ ] Any MC failure uses missing information, opposed will, cost, or an established blind spot
- [ ] No narration asserting the MC is clever
- [ ] Nobody was made stupid to make the MC look smart
- [ ] Tier-appropriate: no deduction above tier, no obtuseness below it

**Knowledge** — every character in the chapter, not just the MC:

- [ ] Provenance test on every stated fact: taught it, did it, was told it, read it, or openly
      guessing. "They're intelligent" is not a provenance
- [ ] Nobody answered inside a domain their row in `bible/cast/_competence.md` does not list —
      unlisted is `none`, not "probably fine"
- [ ] Someone in this chapter said they did not know, went to their referral, or was confidently
      wrong. If nobody did, the cast is reading as omniscient
- [ ] No exposition handed to a convenient mouth: nobody explained a subject outside their map
- [ ] Nobody improvised a second specialty where a referral existed
- [ ] Any skill practised advanced by a teacher, a reference, or a costly failure — never by
      elapsed time; a stage transition got a scene and ordinary practice got a clause
- [ ] Practice cost something namable this chapter
- [ ] Broad-knowledge characters (`knowledge_scope: broad`) stayed inside their declared shape,
      hit their declared boundary, and had their **access** bounded rather than their knowledge

## Pass 4 — Structure

- [ ] Every scene has goal / obstacle / turn / cost
- [ ] No scene exits on a plain yes
- [ ] The chapter's cost is stateable in one concrete sentence
- [ ] At least two of the four conflict sources active
- [ ] Thread ops match the plan row; the ledger will be updated
- [ ] The `wld>` line is filled: the world did something offstage this chapter
- [ ] Any world-track event that fired is logged in the divergence ledger, with what it opened
- [ ] Crisis count is within `timeline.crisis_cap`; nothing here took an `ending.non_negotiable`
- [ ] Skim test: name the one thing a reader would miss if they skipped this chapter

## Pass 5 — World (`world-texture`)

Runs after structure (description placement follows scene shape) and before bias, so any world or
cultural material it adds is still audited by Pass 6.

- [ ] Every world detail is load-bearing — it characterises the noticer, sets up a later beat,
      anchors a location, carries a social fact, or creates friction. Cut the rest
- [ ] At least two beats of consequence / friction / assumed reference for every sentence of
      direct description
- [ ] 2–4 sensory details per scene, at least one non-visual, none delivered as a block
- [ ] No establishing paragraph; no run over three descriptive sentences; no gazetteer sentence,
      history lecture, or explanation of a reference made two pages earlier
- [ ] Every location hit its `bible/world.md` sensory signature within 100 words of arrival, and
      a revisited place was not re-explained
- [ ] Observations belong to the POV character — nothing noticed that is normal to them, nothing
      noticed that their job, wound or state would not make salient
- [ ] ≤1 new invented term, and it recurs this chapter; every proper noun matches `lexicon.md`
- [ ] Nothing contradicts `bible/society.md`; any social rule used bit someone rather than being
      narrated
- [ ] One or two things referred to and left unexplained, with the scene still comprehensible
- [ ] New anchors and durable social facts are queued for `set>`

## Pass 6 — Bias (`bias-guard`) — never skipped, never negotiable

- [ ] No group treated as uniformly anything by the narration
- [ ] Every named woman in the chapter wants something that is not the MC
- [ ] No character introduced by a body inventory
- [ ] No physical trait or accent signalling moral quality
- [ ] Nobody is a reward
- [ ] Any prejudice on the page belongs to a character and costs someone something

## Pass 7 — MTL detox (`mtl-detox`)

- [ ] Zero banned phrases
- [ ] Zero exclamation marks in narration
- [ ] No crowd-reaction block
- [ ] No rank recital or system lecture
- [ ] No face-slap loop; every confrontation cost the winner something
- [ ] No paragraph saying the same thing three ways

## Pass 8 — Prose (`prose-quality`)

- [ ] No phrase from the AI-default cut list
- [ ] Filter verbs removed
- [ ] Sentence and paragraph lengths visibly varied
- [ ] No paragraph opens with the same word as the one before it
- [ ] Emotions carried by behaviour or decision, not named
- [ ] One non-visual sensory detail per scene
- [ ] No dead stage business
- [ ] **Dialogue share is 25–40% of the chapter's words** (`dialogue-voice` §How much dialogue).
      Under 10% fails the pass: measure it, do not eyeball it. The fix is to give the beats to
      the people in the room, never to bolt on small talk
- [ ] Nobody was present in a scene, silent, while the POV character narrated their inner state

## Pass 9 — Delivery (`scene-craft`, `conflict-engine`, `hook-and-pacing`)

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
      failure, a second interrogation must cost more than the first or one of them is cut
- [ ] The chapter passes the skim test: a reader who skipped it would lose something nameable
- [ ] Opening avoids the banned patterns; re-anchoring is one clause
- [ ] Chapter ends on its last strong beat; hook concrete, final position, type rotated

**Length**, for completeness: if the chapter is far outside `chapters.length_band`, look at it once
and ask whether the material was split in the wrong place. Then move on. Do not pad, do not trim,
and do not record a length judgement in the report.

## Pass 9b — The opening (`story-opening`) — chapters ≤ `opening.contract_by_ch + 2` only

Skip entirely outside that range. Inside it, **open `story-opening`** — §1 and §3 are judgement
calls that a checklist cannot make, and this is exactly the pass that silently no-ops if you work
from the summary.

- [ ] **The anchor test.** Could a stranger reading only this chapter say what kind of story it is,
      where and when it happens, and what the POV character wants? Three shrugs is a fail
- [ ] For fanfic/transmigration: does the reader know **which** story and roughly **when** in it?
- [ ] Anchor-vocabulary count for this chapter is not zero (`lexicon.md`, `anchor? yes` terms).
      Across chapters 1–5 collectively, zero is a hard failure
- [ ] **The stakes ceiling.** Has any consequence escalated past the reader's ability to price it?
      Before a threat is dangerous, the mechanism must be on the page — not in the bible
- [ ] `opening.promise` has been touched by `promise_touched_by_ch`
- [ ] The central advantage lands a legible win by `first_win_by_ch`, before any failure
- [ ] Chapter 1 only: the MC acts; they are not delivered through the chapter by other people

## Pass 9c — Foreknowledge (`meta-knowledge`) — only if `mc.foreknowledge` is set

**Open `meta-knowledge`.** §4 is distributional — whether the advantage has ever won cannot be
seen from one chapter, and that is precisely the defect it exists to catch.

- [ ] Nothing was known at a precision `foreknowledge_grain` does not license
- [ ] Every fact stated from foreknowledge passes the provenance test
- [ ] Any spend is in `state/foreknowledge.md`, with its cost and what it invalidated
- [ ] A plot-changing spend moved at least one other row toward `invalidated` (§5, observer paradox)
- [ ] `foreknowledge_first_win_ch` < `foreknowledge_fails_ch`, and the win is on the page first
- [ ] Foreknowledge did not stand in for a skill the MC has not learned
- [ ] The `fk>` CCS line is written

## Pass 10 — Mechanics

- [ ] Frontmatter complete, including `delivers:`
- [ ] `wordcount:` is **measured** (`wc -w` where available), never estimated, and re-measured if
      any pass changed the body. It is a recorded fact that later tools read, not a target — but a
      wrong fact propagates into `state/continuity.md` and corrupts every share computed from it
- [ ] Scene breaks use `* * *`
- [ ] POV label present if the chapter switches and `label_switches` is true

**The four channels** (`narrator-voice` §The four channels; house style in `lexicon.md`):

- [ ] Speech in `"…"`, direct thought in `'…'`, meta in `[…]`, free indirect **unmarked**
- [ ] Direct thought is **budgeted — 1–3 per chapter**, at moments of decision. A chapter where
      every interior beat wears quote marks has flattened its narrator into a thought bubble;
      convert the surplus back to free indirect discourse
- [ ] **No apostrophe was mistaken for a thought mark.** `don't`, `she'd`, `the boys' room` are
      not thought. Every `'…'` opens at a word boundary and closes before punctuation or space
- [ ] Every `'…'` **inside** a `"…"` pair is an ordinary nested quotation, not thought
- [ ] Meta blocks match the format in `lexicon.md`; none opens a chapter; no two run consecutively
- [ ] Italics do the **one** job `lexicon.md` assigns them, and no other
- [ ] Nothing else is markup — no headings, bold, lists, links or author notes in the prose body

---

## Fixing

- **Fix in the file.** Do not report a defect and leave it.
- **Structural defects can require a rewrite of a scene.** Do it. A chapter with no cost or no
  turn cannot be repaired at the sentence level.
- **When a fix contradicts the plan**, change the plan row and re-check the next three rows.
- **When a fix reveals a bible gap** (an unnamed thing, an undefined rule, a social fact the
  scene assumed), add it to `bible/world.md`, `bible/society.md` or `bible/lexicon.md` in the
  same pass and say so.
- **When Pass 3 finds a knowledge gap**, prefer the cheap fix in this order: give the line to
  someone whose map covers it · have the character ask their referral · let them be *wrong* about
  it, which usually improves the scene · and only last, add the domain to their map, which is a
  permanent change to who they are.

Set `status: revised` in the frontmatter when every pass is clean.

## Reporting

Two lines, unless something structural was rewritten:

```
Revised ch 42 — delivers: Dael now owes the house a favour he cannot pay.
Cut a crowd-reaction paragraph, applied Dael's rung-3 voice delta, replaced the ending
(it ran three paragraphs past the hook).
```

**Lead with what the chapter delivers.** Do not report a word count or a word delta — it is not a
quality signal and putting it in the report is what trained the drafting model to aim at it.

If a pass found nothing, do not list it. If Pass 6 found something, always say what — the user
needs to know that the default was reaching for it.

## Standalone use

`/novel-revise <n>` runs this on an existing chapter. Load that chapter, its CCS block, the two
before it, the matrix rows in `bible/cast/_voices.md` and the competence rows in
`bible/cast/_competence.md` for its speakers, and the profiles of everyone in it — then run all
the passes.
