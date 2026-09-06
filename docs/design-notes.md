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

## Related reading

- [`benchmark.md`](benchmark.md) — run #1: what the toolkit costs to operate, and the defects that
  only appeared under load.
- [`upgrade-plan.md`](upgrade-plan.md) — the current inventory, the research behind the last round
  of changes, and what is still open.
