# Design notes

Why the toolkit is shaped the way it is. `CLAUDE.md` carries the rules; this file carries the
arguments behind them, because a model writing chapter 40 pays for every token of argument it
loads and needs none of it. Read this when you are **editing the toolkit**, not when you are
writing a chapter.

---

## The architecture: procedure in the body, everything else in `references/`

Every skill is a directory:

```
.claude/skills/<name>/
  SKILL.md                 the procedure a model executes. Short by design.
  references/draft-card.md  the decision, for skills write-chapter consults
  references/audit-card.md  the revision-time check, for skills revision-pass consults
  references/<topic>.md     worked examples, failure catalogues, genre notes, long tables
```

The body keeps what the skill owns, the procedure, the hard rules and the pointers. Everything
else moves out, and each pointer states its trigger — *open this when …* — because a pointer
without a condition is not read.

**This replaces the old self-sufficiency rule, and the reason is measured.** `CLAUDE.md` used to
require each `SKILL.md` to need no follow-up reads. Benchmark run #1 is what that cost: of 37
skills, 16 ever loaded, and the four that did not included `bias-guard`, `voice-separation`,
`competence-map` and `prose-quality` — all four described in the contract as never optional.
`revision-pass` was self-sufficient, so the model read its condensed checklists and never opened
the sources. That is not laziness. Following the contract literally cost about 30,000 tokens of
instruction per chapter before a word of story state was read, and the model rationed.

An audit card is written by the skill that owns the defect, so `revision-pass` no longer
paraphrases anyone. The model still opens the owner's file. The file is just small enough to be
worth opening.

### The drafting half, and why it came second

The card fixed revision and left drafting alone, which was half a fix. `write-chapter` step 1 went
on citing sixteen skill bodies by section — `voice-separation` §1 §3, `power-scaling` §1,
`competence-map` §1 §4 — and at the 8.6 KB average that is roughly 34,000 tokens of procedure
before a word of story state. The same load, in the same place, for the same reason, and the model
rations it the same way.

So the pair: a **draft card decides**, an **audit card checks**. Same ownership rule, same
explicit trigger, same test guarding it — `test_write_chapter_does_not_paraphrase_its_sources`
mirrors the revision-pass one exactly. The two cards are genuinely different documents. A draft
card produces an answer and is read before anything exists; an audit card produces a verdict and is
read against a draft. `voice-separation`'s draft card lays the speakers out as matrix rows and asks
which one differs from the MC; its audit card runs the transplant test on lines that now exist.

Four of the eighteen are conditional and name their condition first, so a chapter outside the
opening arc never opens `story-opening`'s card and a novel with `scaling.shape: none` never opens
`power-scaling`'s. That is the other half of the saving, and it is why the cards are per-skill
rather than one merged file: a merged file cannot be skipped in parts.

The optional and genre modules are the same problem seen from the config side. Their descriptions
sat in context for every novel whether or not the novel had a system layer or a canon, so
`sw readset` now resolves them — it already read `optional:` and `genre` — and prints the entry
point for each live one. A module the read-set does not list is off, and costs nothing. Small
modules point at their own body, because at 4 KB the body *is* the decision-sized slice; giving
them a card would only duplicate it.

## Why the gate stopped being a command

`revision-pass` used to be reachable two ways: `write-chapter` step 4 ran it, and `/novel-revise`
ran it standalone. In practice the user typed `/novel-revise` after almost every chapter, which is
the symptom worth reading carefully — **the gate was chained in the documentation and unchained in
the run.** Three things unchained it, and only the first is about the docs.

The **budget position** is the real one, and it is the same finding as the section above wearing
different clothes. Step 4 is reached after Phase A has spent the draft cards and Phase B has
written a chapter, and `revision-pass` then asks for the audit cards. That is precisely where run
#1's model rationed, and a model that rations at the gate does not announce it — it ticks the
boxes. Re-running the gate in a fresh turn is the *correct* response to that, which is why the
habit formed. What was wrong was the label on it, not the behaviour.

Nothing **enforced** it either. `sw readset` never looked at whether chapter N−1 was `revised`, and
the step 6 report had no line the gate had to answer for. This repo already documented what happens
to a rule in that position — *a rule that is measured but not surfaced is decoration* — and had
applied it to `SUMMARY_MARKERS` while leaving the gate itself unsurfaced.

And the docs **advertised it as the user's job**: section 2 drew `write-chapter -> revision-pass`
as the next link in the chain, section 3 said *"after drafting, or on `/novel-revise`"*, and section
7 listed the command beside `/novel-write` as a peer. A gate that has to be summoned is a gate that
is skipped whenever the run is long.

So the gate is **Phase C**, named like Phases A and B because it is part of the same act of
writing; the command is gone; the report carries a `Gate:` line naming what was fixed and which
passes ran without their card; and `sw readset` names any chapter still sitting at `drafted`. The
re-entry path survives as `/novel-write <n>` on a chapter that already exists, which asks whether to
re-gate or redraft — one door, and the routine case does not go through it.

**What was rejected: merging the gate into Phase B.** It is the obvious reading of "integrate
revision into the writing process" and it is wrong twice over. Structural fixes invalidate line
edits, which is why `revision-pass` is ordered the way it is; and a model told to self-edit
mid-draft writes defensively, which is the eventless prose the brief/draft split exists to prevent.
Drafting straight through and gating afterwards is the split that works. What was wrong was letting
"afterwards" mean "in some other turn, if someone asks".

### The half that stops the same fix recurring

A gate that fixes the same defect every chapter is a gate doing the draft's job. The countable half
of that is now fed forward: `sw readset` prints a **WATCH** row naming checks that fired in at least
two of the last five chapters, Phase A copies it into the brief, and Phase B writes against it. The
judgement half is a `gate>` line in the CCS block — what Phase C had to fix, a dozen words, omitted
entirely when it found nothing, so an absent line is the clean signal rather than `gate> clean`.

Two guards, both learned here. The row is **distributional and capped at three**: no chapter is
ever scored on it, for the same reason `temp` is checked across an arc and never per chapter. And it
is a **pointer at the owning skill, never a phrase list** — the section below on the anti-slop
constitution is the whole argument for why a growing ban list makes prose worse, and a watch row
that turned into one would reproduce that failure with a script behind it.

## Why the gate is delivery, not length

`chapters.length_band` is a printer's note. Nothing gates on it, and this is the third design.

The first version carried a target with tolerances. Chapters clustered against the floor — five
of them landed within 59 words of `min_words` against a target 20% higher. The tolerance was
tightened to ±15%; chapters clustered against the new implied floor, and chapter 5 landed on the
declared minimum **to the word**. In the same pass, one chapter's frontmatter was wrong by 268
words, and the wrong number had already propagated into `state/continuity.md`.

The lesson is not that the tolerance was loose. **Any number that decides whether a chapter ships
will be optimised, and prose optimised toward a length is padded or truncated prose.** So the gate
is `revision-pass` Pass 9 — want, friction, change, cost, next — and `change` must name a
difference rather than summarise events. Word count survives only as a measured fact whose
*accuracy* is checked, because everything else computed from it inherits the error.

Do not reintroduce a length gate in any form.

## The gate needed a second half: `event`

The delivery gate above is right and it is not sufficient, and benchmark run #2 is the proof.

Five chapters, all `status: revised`, all sixteen passes run, zero MTL hits, zero cut-list
phrases. A reader flagged the novel as machine-written inside a page and priced it at one star.
Pass 9 had been satisfied five times over. Here are the five `delivers:` lines it accepted:

> *proximity that isn't refused* · *attention has moved one level up* · *an institutional crack
> on day one* · *now physically inside the divergence* · *the foreknowledge win lands*

Every one names a shift in somebody's interior state, and all five are built from the same
`X — not Y, but Z` construction. **A gate phrased in abstractions is satisfied by abstractions.**
Asked for "a difference, not a summary of events", a model does not invent an event; it finds the
smallest difference it can name and writes 1,100 words around it. Chapter 5 of run #2 is a woman
persuading a child to eat some rice.

So `event:` sits beside `delivers:`, and the two fail in opposite directions. `event:` is what
*happens* — one clause a reader could retell, a concrete verb and a target — and abstract-state
nouns are rejected outright by `sw lint` rather than argued with. `delivers:` remains what is
different afterwards.

**The deeper finding is that the plan was never the problem.** Run #2's `ev>` ledger lines record
a massacre, a forged household roll, a ROOT records demand and a Hokage interrogation. Those are
set pieces. They were given 1,457, 1,323 and 1,213 words and pitched at exactly the register of
the rice chapter. The planning layer worked; the drafting layer would not dramatize what it had
planned. Hence the weight test — *is the `event` beat the longest scene in the chapter?* — and
hence `story-craft`'s draft card being promoted to the first card opened rather than the
fifteenth.

## Register is a tracked quantity, or there isn't one

Nothing in the toolkit measured *register* before run #2, and run #2 accordingly had one. Five
chapters, one temperature — quiet, interior, controlled, ironic — and four of five closing on the
same shape:

> *"The gate hung open." · "The small hand found hers, tighter, in her sleep." · "Neither did
> Enko." · "The door stayed shut, this time, and nobody was watching it."*

Each is a good last line. Together they are a tic. This is the same class of defect as dialogue
starvation and voice convergence: invisible in the chapter you are holding, obvious from four
feet away — so it belongs where those live, in the plan grid and `sw arc`, not in
`revision-pass`.

`temp` and `hooktype` are therefore **plan-time columns**. Set after drafting they would be labels
describing what came out; set before, they are constraints the prose has to meet. The vocabularies
are `hook-and-pacing`'s own — inventing a second one in `rules.py` would have given the skill and
the script different words for the same thing.

The failure mode is the one this document already documented for length: a declared `temp` becomes
a label satisfied without changing a sentence. The mitigation is the same too — the checks are
distributional (no temp three running, four distinct per arc, no hook shape more than twice in
five) and no single chapter is ever scored.

## The anti-slop constitution was fighting the last war

`CLAUDE.md` §5 was thirty bans. Run #2 satisfied nearly all of them and was still obviously
machine-written, which is the whole argument: **a hundred prohibitions do not add up to a story.**

Ban xianxia cliché and what fills the vacuum is not good prose, it is the model's *own* default
literary register — the `X, not Y` antithesis, the em-dash appositive that re-explains the clause
before it, the aphorism at every scene close, `"A beat."` written into prose as if it were a
script. Measured over 7,302 words: 62 em-dashes, 18 antitheses, an aphoristic close at nearly
every scene break. That is a **narrower** fingerprint than the cliché the bans removed, because
every model of this family writes it.

Two consequences. The section is now seven positive commitments and ten bans, because a model
given only prohibitions optimises for avoidance and has nothing left over for invention. And the
tells that matter are measured off this repo's actual output rather than copied from a generic
list — `prose-quality/references/ai-default-tells.md` names seven, with counts.

The positive rule is the load-bearing one: **some sentences must carry information and nothing
else.** The disease is uniform density, not any construction. An early version of `sw lint` tried
to score this as the share of syntactically simple narration sentences and had to be deleted: it
rated *"A promise kept was one data point."* and *"It was not yet a pattern."* as plain, because
the house aphorism **is** short and simple. Shape cannot tell a sentence that delivers information
from one that delivers a moral. That judgement stayed with the skill, and `textstats.py` carries a
comment saying why so nobody rebuilds it.

## And the surfaced rule is the only kind that exists

`CLAUDE.md` §5 banned the past-perfect campaign clause and quoted *"She had spent three weeks
making it true"* as its example. That exact sentence is in run #2's chapter 1, which shipped
`status: revised` through all sixteen passes.

`SUMMARY_MARKERS` had matched it. `sw lint` had counted it. The count was printed inside a
statistics line — *"pacing: 6 summary marker(s), 3.2 per 1000 words"* — where nothing had to
answer for it, and a note nobody has to answer for is not a rule. It is now a `campaign-clause`
warning that quotes the offending text back.

The general lesson, and it applies to every check added here: **a rule that is measured but not
surfaced is decoration**, and one buried in an aggregate is worse than absent, because the green
line reads as evidence.

## The shelf comes before the page

`title-craft` runs at the end of the `novel-init` interview, before the scaffold, and owns the two
things every reader sees before chapter 1 exists for them. A reader in a library grid gives a
title about two seconds and a blurb about fifteen, and a book with a superb chapter 1 and a
noun-stack title is a book nobody opens.

It generates five candidates across five distinct strategies rather than five rewordings of one,
because a model asked for five titles without constraint produces five of the same and the user
picks the least bad. For fan fiction the source work goes in the title line — *Naruto: The New God
of Shinobi* — because fanfic is browsed by fandom and a title without it is invisible to the only
audience it has. The slug is derived here and is permanent; the title is not.

## The opening is its own problem

`story-opening` owns chapters 1 through `opening.contract_by_ch + 2`, because chapter 1 is a
conversion event. Roughly 60% of readers who open it reach chapter 2; from chapter 5, retention
runs above 80%. Everything the toolkit does for chapter 40 is worth nothing if chapter 1 loses the
reader, and the losses there are structural rather than sentence-level: no anchor, no genre
contract, a promise the page does not keep, or a threat the reader cannot price.

The stakes ceiling is the least obvious of the four. A consequence may not escalate past the
reader's ability to price it: before a threat is dangerous, its mechanism has to have been on the
page. Otherwise the beat reads as somebody being arbitrarily strict, however well it is written.

## The world layer: three skills, three jobs

Never mixed. `story-bible` records what is true and where things are. `social-fabric` works out
what the world's central rule does to labour, money, law, knowledge, belief and mobility.
`world-texture` decides how any of it reaches the page, and at what budget.

A fact is written once, in the right file, and delivered as a consequence. A world whose central
rule has not propagated into ordinary work and money is a stage set, and readers feel it as
thinness long before they can name it.

## The character layer, and why the order matters

Three cast-wide tables, three questions, all three read as *tables* — their defects are
distributional and invisible one profile at a time.

`voice-separation` asks **who these people are as minds**: intelligence, articulacy, wit, heat,
turn length, body idiom. `competence-map` asks **what they actually know**: narrow domains with
named edges, a referral for what lies outside, and a ladder for skills acquired the slow way.
`dialogue-voice` then writes the lines.

That order is load-bearing. Eight speech-fingerprint fields painted onto minds that all reason at
the protagonist's speed and answer every question produce a cast of labelled clones — this
format's second-most-common defect, after a stage-set world. The exemptions are narrow and
declared: `mirror:` for clones, avatars and doubles, who may converge on the person they copy, and
`knowledge_scope: broad` for gods, immortals and artificial minds, who still need a declared
shape, a declared boundary, and bounded access.

## Foreknowledge fails in two opposite directions

`meta-knowledge` exists because the mechanic has two failure modes and careful writing picks
neither. The first is the oracle: knowledge that is free and accurate, so nothing is ever at risk.
The second is the handicap: knowledge introduced already-unreliable that only ever malfunctions,
which sells the reader something the blurb did not describe.

The order is fixed — **it works, then it costs, then it frays, then it betrays** — and the decay
is a consequence the MC caused by acting, not a decree scheduled at a chapter number.

Run #1 produced the sharpest instance of getting this wrong: the plan had scheduled the MC's
advantage to be introduced as doubtful at chapter 6 and disproven by chapter 12 **without ever
having worked**, and four of arc 1's five escalation rungs were its failures. An author wary of an
overpowered protagonist schedules the correction before the thing being corrected has ever won.

## The four channels, and why the budget is the point

`narrator-voice` owns four and holds them apart: `"…"` speech, `'…'` direct thought, `[…]` system
interfaces and in-world documents, and unmarked free indirect discourse — which is where
interiority actually lives.

Direct thought is budgeted at one to three a chapter. The budget *is* the feature: marked thought
is emphatic because it is rare, and a chapter that marks every interior beat has turned its
narrator into a thought bubble. The convention is recorded per novel in `channels:` and the
linter reads it from there.

The non-obvious collision: a thought containing a contraction breaks a naive parser, and so does a
speech running across paragraphs, which opens a quote on each paragraph and closes only on the
last. Both are handled in `swlib/textstats.py` and pinned by `tests/test_channels.py`.

## The power curve is a gap, not a magnitude

Four skills touched power progression before `power-scaling` existed, and each of them, correctly,
did something else. `power-system` wrote the rules a capability obeys. `conflict-engine` escalated
the stake and refused on principle to escalate the enemy. `timeline-engine` governed how hard the
world hits back. `story-opening` stopped a consequence outrunning the reader's ability to price it.
Between them there was no owner for the question a progression reader actually asks, which is *how
far ahead of me is the next thing, and is that distance still interesting.*

Three artifacts of that gap were visible in the repo. `mc.starting_power` sat in the template with
no skill anywhere mentioning it — a write-once field with no reader and no updater. The escalation
budget lived in `bible/power-system.md`, which the read-set never loads, no revision pass opens and
no script validates: `state/body.md` and `state/growth.md` both had machine checks; the power
ledger had none, so it drifted silently. And opponent strength was deliberately not an axis
anywhere, which is the right call for *escalation* and leaves nothing at all watching for an MC who
has outgrown their own book.

The governing decision is that **scaling is relative**. What a reader experiences is the distance
between what the MC can do and what the chapter demands, never the absolute tier — which is why
tracking magnitude has never worked and why the tracked quantity here is **pressure**, the
opposition's tier minus the MC's. It is also why *One Punch Man* is not a counterexample but a
configuration: it inverts the distance deliberately and relocates the tension, so `shape: inverted`
is supported and demands `substitute_tension` in writing.

Two consequences follow that are worth stating because they look like duplication and are not. The
ladder moved from `bible/` to `state/power.md` §2, because you cannot judge pressure without it and
`state/` is what the read-set loads; and the escalation budget moved with it into §4, widened with
the columns that make a gain checkable — source, the chapter the price was paid, the chapter it was
set up in. A table nothing reads is not a rule, it is a note.

The one place this skill deliberately does *not* go is severity. Whether a loss hurts belongs to
`conflict-engine`'s stake ladder, and the two axes move independently: raising both every arc is
arithmetically a working curve and dramatically nothing, because the reader never experiences a
tier, only the gap. That failure has a name in `power-scaling/references/failure-modes.md` — the
treadmill — along with the six other ways a curve dies, five of which are countable and therefore
belong to `sw curve` rather than to a checklist nobody rereads.

## The template is half of every parser

Tables are selected by their column names and sections by their heading text — deliberately, since
heading prose gets edited and column names are load-bearing. The cost of that choice is a seam:
the parser is in `scripts/`, the columns are in `novels/_template/`, and nothing was comparing
them. `plan_rows()` selected on `("#", "title", "delivers")` while the shipped
`plan/chapters.md` header ran `… | turn | cost | …`, so it returned `[]` against every novel ever
scaffolded. Every plan check in `sw state` was dead, and the read-set's plan section always said
"no plan rows in range" — advice to run `chapter-plan` on a plan the author had already written.

It survived because every test that exercised plan rows built its own table. A fixture that
supplies the thing under test cannot catch a template that does not supply it. So
`tests/test_template_wiring.py` runs the accessors against `novels/_template` itself, and the same
sweep covers the two neighbouring classes: a heading the read-set slices that no longer exists, and
a `novel.md` key that no skill names and no script reads — the shape `mc.starting_power` had, sitting
in the config for the life of the repo as a question asked at init whose answer went nowhere.

One subtlety worth keeping: `docs/` is excluded from the ownership search. This file mentions
`mc.starting_power` by name in order to explain it, and a key named only in its own post-mortem is
not a key with an owner.

## Why the scripts do not judge

Three rules govern `scripts/sw.py`, and all three exist to stop a tool becoming an alibi.

**An optimisation, never a dependency.** Every skill that names a command keeps its manual
checklist directly underneath. If Python is absent or the command errors, do the checks by reading
and say so in the report. A ticked box that was never checked is worse than an unticked one.

**They find, they do not judge.** A linter locates a string; whether that string is a defect is a
decision. Nothing rewrites a prose body, because `mtl-detox` requires the sentence rewritten
rather than the synonym swapped, and an auto-fixer would do precisely the forbidden thing. The
only files the scripts edit are chapter frontmatter, the `wc:` field of a CCS block, and a fresh
scaffold.

**A clean run is not a passed revision.** It means the mechanical passes found nothing. The
distributional ones and the judgement ones are untouched by it. `bias-guard` has no script at all,
deliberately, so that no green line can ever be mistaken for a bias pass.

The same caution applies to any judged pass. The strongest off-the-shelf model judges agree with
human preference on creative writing about 73% of the time, and rubric judges are measurably
biased by position, length and formatting. A judged pass may locate and describe. It may not score,
and it may not gate.

## Why not OKF

Google Cloud's [Open Knowledge Format](https://okf.md/) (v0.1, June 2026) is a markdown convention
for handing an agent curated context: a directory of files, each with YAML frontmatter carrying at
minimum a `type`, cross-linked with ordinary markdown links, optionally indexed by an `index.md`.
It is a good spec. It is not this repo's spec, and the reasons are worth writing down because the
surface similarity is high enough that the question will be asked again.

**OKF solves interoperability; this repo does not have that problem.** The format exists so that a
wiki written by one producer can be consumed by a different vendor's agent without translation —
many silos, many agents, no shared schema. skilled-writer has one producer and one consumer. Adding
`type: skill` to 41 files buys nothing, because nothing downstream reads it.

**Its conformance rule is the opposite of this toolkit's bet.** OKF requires consumers to tolerate
broken links, unknown types, unknown keys and missing indexes: *if it has frontmatter with `type`,
it's valid OKF, full stop.* That permissiveness is correct for a federation of independent
producers and wrong here, where the whole value is strict triggers a low-effort model cannot
wriggle out of, guarded by `test_corpus.py` and `test_template_wiring.py`. A format whose validity
rule is "has a `type` field" would loosen precisely the contract those tests exist to keep tight.

**And `readset` already beats a bundle at the one place OKF would fit.** `novels/<slug>/` is the
part of this repo that genuinely is a knowledge graph, but OKF hands an agent whole files, and the
whole point of the read-set is that it hands over *windows* — blocks N−5…N−1, plan rows N−1…N+2,
the matrix rows for this chapter's speakers. OKF has no concept of a slice, and the slice is the
entire reason the ledger can grow without the per-chapter cost growing with it.

The shape that would be correct, if a novel ever has to leave this repo, is OKF as an **export
target** — an `sw export --okf` that projects the bible and state into a conformant bundle — never
as the working format.

## Related reading

- [`benchmark.md`](benchmark.md) — run #1: what the toolkit costs to operate, and the defects that
  only appeared under load.
- [`history/upgrade-plan.md`](history/upgrade-plan.md) — the current inventory, the research behind the last round
  of changes, and what is still open.
