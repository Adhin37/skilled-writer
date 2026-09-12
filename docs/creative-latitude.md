# Creative latitude

**The toolkit has one lever — prohibition — and every round of tuning has added more of it.** This
file measures that, argues it is now the binding constraint on quality rather than a protection
against slop, and proposes the second lever.

Measured 2026-09-12, immediately after the knowledge-base expansion documented in
[coverage-map.md](coverage-map.md) — an expansion which made the problem worse and is the reason
it got noticed.

---

## The measurement

Over the whole craft corpus — 118 files, 130,873 words:

| | count | per 1,000 words |
|---|---|---|
| negation tokens (*never · no · cannot · fails · defect · banned · avoid · wrong*) | 3,942 | **30.1** |
| generative constructs (*pick one · choose · options · candidates · strategies · e.g.*) | 224 | **1.7** |
| checkbox items | 720 | — |

**The ratio is 17.6 : 1.** Twenty-eight of the ninety-one substantial files contain no generative
construct at all.

Two structural findings matter more than the ratio:

- **Three files out of 118 contain machinery that generates options** — `mc-design`'s option
  triad, `title-craft`'s five strategies, `novel-init`'s interview. All three run **once, at
  setup**. There is no option-generating machinery anywhere in the per-chapter loop.
- **The corpus contains zero statements of when a rule should be broken.** Not one clause, in
  130,000 words, saying *here is where this stops applying*.

### What one chapter now costs

Resolved against the live novel at chapter 6:

| phase | cards | words of instruction | checkboxes | negations |
|---|---|---|---|---|
| A — the brief | 19 | 7,915 | 9 | 259 |
| C — the gate | 23 | 8,444 | 207 | 337 |
| **total** | **42** | **16,359** | **216** | **596** |

Sixteen thousand words of instruction and 596 prohibitions reach the model before a line of story
state does.

`write-chapter/references/draft-cards.md` describes benchmark run #2 as having opened **nineteen
cards** and held "roughly thirty simultaneous constraints", and says of the result: *"a model
spending its budget on not-failing has none left for deciding what happens."* Phase A is at
nineteen cards again. Phase C is at twenty-three.

## Why this is the binding constraint now

The repo already contains the argument, in `CLAUDE.md` §5:

> A hundred prohibitions do not add up to a story. They tell a model what not to write, it avoids
> all of it, and what fills the vacuum is the model's own default register [...] That is a
> *narrower* fingerprint than the cliché the bans removed.

That paragraph was written after benchmark run #2 shipped five chapters that satisfied almost
every rule in the toolkit and were priced at one star by the first human who read them. The
conclusion drawn was to cut §5 from thirty bans to ten. The conclusion **not** drawn was that the
same logic applies to the other 129,000 words, and since then the corpus has grown by every
mechanism except the one §5 identified as missing.

Three consequences, in the order they bite:

1. **Budget.** Attention spent on compliance is not available for invention. This is the repo's
   own stated diagnosis of run #2 and it is quantified above.
2. **Convergence.** Every card in the draft loop narrows toward one answer. Nothing widens. A
   pipeline with no divergent step produces the median of what the rules permit, and the median of
   a well-specified space is competent and unsurprising — which is the failure mode a reader
   describes as "machine-written" without being able to point at a line.
3. **Flattened force.** The essentialism ban and the em-dash density note are written in the same
   register, with the same weight, in the same kind of list. A model cannot tell them apart, so it
   obeys both at the same anxiety level. The cost of that is paid entirely by the stylistic rules,
   which are exactly the ones a good chapter sometimes needs to break.

## What already works, and should be built on

**`style.sample`** is the one positive lever in the toolkit: three to six sentences of target
register in `novel.md`, read in Phase B. The template's own comment is the thesis of this file —
*"the single cheapest lever on register, and the only one that works by imitation rather than by
prohibition."* It is right, it is wired, and it is one field.

The proposals below are that idea applied to the rest of the pipeline.

---

## The plan

### 1. Measure the load, and bound it

`sw` measures everything about a chapter and nothing about the instructions handed to the drafter.
Add **`sw load <novel> -c N`**: cards, words, checkboxes and negations for Phase A and Phase C, as
the table above. A maintainer number, never a chapter gate.

Then a budget the corpus has to live inside — **Phase A ≤ 12 cards, Phase C ≤ 15** — enforced by
`sw health`. Past the budget, a new card must *merge* with an existing one rather than join the
queue. The expansion that prompted this file added ten audit cards without anything, anywhere,
objecting.

### 2. The divergent step — three options, then choose

The per-chapter loop has no widening move. Give it exactly one, in the card that already runs
first: **`story-craft`'s draft card asks for three candidate answers to the chapter's central
question, and requires the second or third to be chosen unless the first is clearly best.**

Cheap, bounded, and it attacks convergence at the only point where it can be attacked — before the
brief is written. `mc-design` owns `option-triad` for character design; this is that concept
extended to the draft, and it should be owned by whichever of the two the ownership rule prefers
rather than duplicated.

### 3. Positive exemplars beside the failure tables

Every audit card carries a *"where it fails most often"* table. None carries its opposite. Add to
each card a **two-line worked example of the rule landing well** — not a rule restated, a sentence
or exchange that does the thing.

This is the `style.sample` mechanism at skill scale, and it is the highest-value item here: a
model matches an example far more reliably than it obeys a rule, which the template already says
and the corpus nowhere exploits.

### 4. Three tiers of force, declared in frontmatter

Every rule gets a tier, and the tier is visible where the rule is:

| tier | meaning | examples |
|---|---|---|
| **absolute** | never broken, no stated reason accepted | `bias-guard` in full · consent · no text reproduced from a source · minors |
| **structural** | broken only with a reason stated in the gate report | the event · nothing is free · the four channels · the MC is never stupid |
| **stylistic** | broken freely whenever the chapter is better for it | em-dash density · gesture set · turn length · opening patterns · dialogue share |

Then add the clause the corpus does not contain anywhere: for every **stylistic** rule, one line
on when breaking it is correct. A craft guide without that is a style guide.

### 5. A gate question that can fail a safe chapter

Pass Z asks three questions — is there an event, does it get the scene, would a reader click next.
All three are structural, and a chapter can pass all of them and be entirely predictable. That is
a fair description of what run #2 shipped.

Add **Z4: name the thing in this chapter that a competent hack would not have written.** If the
honest answer is nothing, that is a finding. Judgement, unscored, never a number — the same
contract as the rest of Pass Z.

### 6. Prune

Work the 720 checkboxes down. Three cuts, in order of safety: boxes that restate what `sw lint`
already finds and quotes; boxes no reader would ever feel; boxes that appear on two cards because
two passes consult the same skill. Target the count, not any individual rule — the aggregate is
the defect.

---

## What was built, and what it measures now

All six, in the order below. Measured against the same live novel at chapter 6.

| | before | after |
|---|---|---|
| cards opened for one chapter | 44 | **37** |
| Phase A cards | 19 | **15** |
| Phase C cards | 23 | **20** |
| **words of instruction (A+C)** | **16,359** | **16,550** |
| checkboxes live at once | 216 | **199** |
| generative constructs in the per-chapter loop | **0** | **15** |
| positive exemplars on the cards | **0** | **20** |
| skills stating when to break their own rules | **0** | **5** |

**The words row is the one that did not move, and it is the row that matters.** The card count
fell 17% and the instruction load rose 1.2% — Phase C alone grew by 374 words. The merges in item
6 moved text between files rather than removing it, and a merged card costs a drafter exactly what
its two halves cost separately. `rules.CARD_BUDGET` bounds the card *count*, so nothing objected.

**Closed 2026-09-12, as a ratchet rather than a cut.** `rules.CARD_WORD_BUDGET` bounds the words
too, enforced by `sw health` beside the count, set a hair above the measured figure so a wording
fix is free and a genuine addition is not. That was the actual hole: the ratchet was on the wrong
number.

The cutting half is reported honestly as **largely spent**. This plan named three safe cuts and
two of them no longer have anything to take: there is not one checkbox text shared between any
two skills (`sw health`'s duplication rule got there first), and the boxes restating a `sw lint`
finding went in the same pass that wrote this section. What remains is prose, and prose is where
the advice lives — so the budget is a ceiling to lower deliberately, never a licence to cut
advice toward a number.

And benchmark run #4 **demoted the item**, which this file should say plainly: the same corpus was
affordable to a cold agent (33 cards, $3.21) and unaffordable to a warm one (5 cards across five
chapters). What decays is not the size of the instruction but the model's willingness to spend
context on it once the conversation is long. The prune is maintenance. A fresh session per chapter
is the quality fix.

1. **`sw load <novel> -c N`** reports cards, words, checkboxes and negations per phase, and
   `rules.CARD_BUDGET` caps the unconditional set at 12 draft cards and 15 audit cards. `sw health`
   fails past it and `tests/test_corpus.py` asserts it. Nothing about it touches a chapter.
2. **`metadata.force:`** on every skill — `absolute` (1), `structural` (39), `stylistic` (4).
   `sw kb passes` marks the two that are not structural, `revision-pass` states what each obliges,
   and `CLAUDE.md` §How hard each of these binds is the contract. Four stylistic skills now carry
   a **§When to break these**, which is the clause the corpus previously contained nowhere.
3. **A §What it looks like when it lands** on all 29 audit cards — two or three lines of the rule
   working, beside the failure table that was previously the card's only illustration.
4. **Three candidates**, in `story-craft`'s draft card, which is the one that opens first. The
   only widening step in a loop where every other card converges.
5. **Pass Z4** — *name the thing here a competent hack would not have written.* The only question
   in the gate that can fail a chapter for being safe. A failure is a note and a WATCH row, never
   a stop: it is a habit, and the repair is in Phase A's candidates rather than in the prose.
6. **The merges.** The budget forced four draft cards and three audit cards to fold into the card
   that already owned their neighbourhood — `social-perception` into `mc-intel-meter`,
   `character-development` into `voice-separation`, `timeline-engine` into `plot-threads`,
   `character-profile` into `competence-map`. Each merged card names both owners in its opening
   lines. Plus a prune of the boxes `sw lint` already finds and quotes.

**What did not improve: the corpus-wide ratio**, which went from 17.6 : 1 to 18.8 : 1. The
exemplars and break clauses are themselves prose about failure, and the merges moved text rather
than deleting it. That number was a diagnostic, not the target, and reporting it honestly matters
more than moving it.

**But the same cause reached the per-chapter loop, which was the target.** The count fell and the
words did not, for exactly the reason the ratio did not move: nothing here deleted anything. Five
of the six items landed as designed and are measured above; the sixth — the prune — is the one
that would have moved the words, and it was sequenced last on the argument that it is safest to
cut once there is positive material to cut toward. That material now exists.

## Sequencing

**1 → 4 → 3 → 2 → 5 → 6.** Measurement first, because the budget is what stops the corpus growing
back. Tiering second, because it is pure annotation, changes no advice, and immediately relieves
the flattened-force problem. Exemplars third — the highest value and the most writing. The
divergent step and Z4 change drafting behaviour and want a benchmark run to evaluate. The prune is
last because it is safest to cut once the positive material exists to cut toward.

## What this is not

Not a case for fewer rules in general, and not a case against any specific rule. Almost every one
is individually defensible and most were bought with a measured failure. The claim is narrower and
only about the aggregate: **a corpus that is 94% prohibition by token has one tool, and the thing
it is now most likely to produce is a novel with no defects in it.**

`bias-guard` is untouched by all of this and is not negotiable — it is the clearest case of a rule
whose force is absolute, and giving it a tier is how that stops being indistinguishable from a
note about dashes.

## Backlog — found during the expansion, unrelated to the above

- ~~**`tests/test_corpus.py` hardcodes `DRAFT_CARD_OWNERS` and `MODULE_CARD_OWNERS`.**~~ **Done** —
  both registries are derived from frontmatter and the tests assert the property rather than the list.
- **`kb passes` descriptions are inconsistent.** Cards written before the expansion describe
  themselves by pass name — "Bias", "Structure" — and newer ones by what they check. The
  dispatcher line is only useful in the second form; normalise.
- **Pass 2 now opens five cards**, the widest in the gate. First candidate for the merge that
  item 1's budget would force.
- **`sw kb cards` could not reach its novel argument** — fixed in `sw.py`; see
  [coverage-map.md](coverage-map.md).
