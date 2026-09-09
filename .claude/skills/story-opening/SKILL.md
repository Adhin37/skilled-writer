---
name: story-opening
description: Own the first chapters - world anchor, genre contract, promise ledger, stakes ceiling. Use when planning or drafting any chapter up to opening.contract_by_ch + 2, and inside revision-pass.
---

# story-opening

Chapter 1 is not the first chapter of your book. It is a **conversion event**. About 60% of readers
who open chapter 1 go on to chapter 2; from chapter 5 onward, retention runs 80% or better. Every
structural decision in this skill follows from that one asymmetry: the opening is not where the
story is best, it is where the story is *chosen*.

The two failures this skill exists to prevent are opposites, and a draft can have both at once:

| failure | what it looks like | why it kills |
|---|---|---|
| **The unanchored opening** | Beautiful, specific, in-motion prose in which the reader cannot tell what kind of world this is, what the story is about, or why anything matters | A reader who cannot place the story cannot want anything from it. They do not complain; they close the tab |
| **The gazetteer opening** | Three paragraphs of history, a map, a rank ladder, a cast list before anyone wants anything | Readers accept world information *in direct proportion to emotional investment*. Front-loaded, it is noise |

The resolution is not a compromise between them. It is **the anchor**: the smallest set of facts
that makes everything else interpretable, delivered as consequence.

**Scope.** Chapters 1 through `opening.contract_by_ch + 2`, and the whole of arc 1 for the stakes
ceiling and the promise ledger. After that this skill is done and `hook-and-pacing` has the wheel.

---

## Sections that live in `references/`

| § | file | open it when |
|---|---|---|
| 5, 6 | `references/chapter-one.md` | drafting chapter 1 itself, or wiring the opening arc into planning and revision |

The revision-time check is `references/audit-card.md`, opened by `revision-pass` Pass 9b.

## 1. The anchor

`python3 scripts/sw.py lint novels/<slug> -c <n>` counts anchor vocabulary for any chapter
inside the opening arc, using the `anchor? yes` rows of `bible/lexicon.md`, and fails the
chapter on zero. That is the floor, not the test: a chapter can hit five anchor nouns and still
leave a reader unable to say what kind of story this is. The count is mechanical; the anchor is
not.


> **By the end of chapter 1, a reader can say what kind of world this is, what kind of place they
> are standing in, and what the POV character wants this week.** For fan fiction, transmigration
> or any story set in a known world, they can also say **which story they are in and roughly when
> in it.**

That is the whole requirement. Note what it does *not* require: no history, no map, no magic
system, no faction list, no cast.

### The anchor test

Give a stranger chapter 1 and nothing else — no blurb, no cover, no tags. Ask three questions:

1. What kind of story is this?
2. Where and when is this happening?
3. What does this person want, and what is stopping them?

**Three shrugs is a failed opening**, however good the prose. This test is run in
`revision-pass` on every chapter up to `anchor_by_ch`.

### How anchors are delivered

Ranked by cost, cheapest first. Same ladder as `world-texture` §1, applied to orientation.

| # | channel | example |
|---|---|---|
| 1 | **A rule biting someone** | Rations are recounted because the war budget moved — now the reader knows there is a war, an authority, and scarcity, and nobody explained anything |
| 2 | **A character working around the world** | She performs bad handwriting on purpose, because literacy in a four-year-old is a thing that gets *noticed here* |
| 3 | **An unexplained assumed reference** | "You'll test for the Academy like everyone else." Nobody says what the Academy is. The reader now knows one exists, that it tests, and that it is normal |
| 4 | **Direct statement** | "Konoha had been at war for six years." Costs the most; budget it |

**One named proper noun a reader could search is worth three pages of atmosphere.** The name is
the anchor. A story that withholds the name of its own world is not being mysterious.

### The anchor vocabulary

`bible/lexicon.md` → Terms of art marks anchor terms with `anchor? yes`. The rule:

> **Every `anchor? yes` term whose `first appears` is later than `opening.anchor_by_ch` is a
> defect.** Anchor vocabulary is front-loaded, not saved.

Deferring the word that names the genre does not build mystery. Mystery is a question the reader
*knows they have*. A reader who does not know what kind of story they are reading has no question —
they have a vague unease, and it is indistinguishable from the feeling of reading something bad.

**In fan fiction this is the single most common structural defect**, because the writer knows the
canon so thoroughly that its absence is invisible to them. Grep is the cure: count occurrences of
your five biggest canon nouns across chapters 1–5. **Zero is a bug.**

## 2. The genre contract

> **By `contract_by_ch` (default 3), a reader who liked chapter 3 can predict the *kind* of
> pleasure chapters 10 and 50 will provide.**

Genre conventions are not constraints. They are **shorthand for promises**, and they let you skip
explaining what the reader already knows how to want. A promise broken *early* is a twist. A
promise broken *late* reads as betrayal, however good the prose.

Name the contract in `novel.md` → `opening.promise` and check it on the page:

| the contract says | so the opening must show |
|---|---|
| Progression fantasy | the gap between what the MC can do and what they could become |
| Political / institutional | that institutions decide outcomes, and that the MC is inside one |
| Mystery | a question with a knowable answer, and the MC wanting it |
| Fan fiction | which canon, roughly when, and what is different about *this* telling |
| Slow-burn character study | that the small scale is the point — a reader who wants explosions should self-select out by ch 3 |

**Deliberate subversion is allowed, early and signalled.** If chapter 40 breaks the contract,
chapter 3 must contain the thing that, on reread, was the warning.

## 3. The stakes ceiling

> **A consequence may not escalate past the reader's ability to price it.**

This is the rule that keeps an opening from "escalating too quickly," and note carefully what it
*is not*: it is not a limit on how bad things get. It is a limit on how bad things get **before the
reader can tell that they are bad.**

The failure mode in full:

- Chapter 2: the MC says one word she shouldn't know.
- Chapter 3: an adult notices.
- Chapter 4: the adult is now certain something is wrong with her.
- The reader, meanwhile, has not been told what world this is, what a file costs, who reads it, or
  what happens to anomalies here.

Every beat above is *well-written*. The escalation is real, earned, and paced. And it lands on the
reader as **a strict adult being nosy**, because the machinery that makes it a death sentence has
never been on the page. The author is writing a thriller; the reader is reading a domestic drama.

### The ceiling procedure

Before scheduling any escalation in the opening arc, answer:

1. **What makes this bad?** Name the mechanism — the file, the tribunal, the debt, the rival clan.
2. **Is that mechanism on the page yet?** Not in the bible. On the page, where a reader saw it.
3. If **no**: either put it on the page first — as consequence, per §1 — or **hold the escalation**.

Record the answer in `novel.md` → `opening.stakes_ceiling`: the worst thing allowed to happen
before the frame exists. One sentence, e.g. *"She can be noticed, but nobody may act on it until
the reader has seen what a file does to someone else."*

**The cheapest fix is almost always a bystander.** Show the machinery consuming someone the reader
does not love yet, before it turns toward someone they do. One scene of a stranger losing to the
system prices every threat that follows, for the rest of the book.

### Escalate the frame, not just the threat

In the opening arc, the reader's *understanding* must climb at least as fast as the danger. A
useful shape:

| chapter | danger | frame |
|---|---|---|
| 1 | none — a want and a friction | what kind of world, what kind of place |
| 2 | a small social cost | who has power here, and over what |
| 3 | a real threat, to someone else | what the mechanism does to people |
| 4 | the threat turns toward the MC | — the reader can now price it |
| 5 | the MC acts, and pays | — |

## 4. The promise ledger

The blurb makes a promise. The page has to keep it.

> **`opening.promise` must be *touched on the page* by `promise_touched_by_ch` (default 3), and
> the MC's central advantage must land one legible win by `first_win_by_ch` (default 5).**

The defect this prevents is specific and common: a blurb that promises *"she knows what's coming
for the Uchiha"* attached to ten thousand words in which the MC never once thinks about the future.
The blurb is not marketing that happens near the book. It is the contract, and readers arrive
holding it.

| ledger entry | source | on the page by | check |
|---|---|---|---|
| The promise | `opening.promise` | `promise_touched_by_ch` | Can a reader point to the paragraph? |
| The advantage's first win | `mc.golden_finger` | `first_win_by_ch` | Did it *work*, legibly, and did the reader see the win came from it? |
| The genre contract | §2 | `contract_by_ch` | Could a reader predict ch 10? |
| The anchor | §1 | `anchor_by_ch` | Does the anchor test pass? |

**"Touched" is a low bar and it is meant to be.** Not resolved, not explained, not paid off — just
*present*, so a reader who came for the promised thing can see it exists. One scene where the MC
tries to use the advantage and gets a partial result is enough.

The complement is `power-scaling`'s **first limit**: after the advantage has won legibly, it must
hit a wall it cannot climb, by `scaling.first_limit_by_ch`. The ordering is enforced —
`opening.first_win_by_ch` < `scaling.first_limit_by_ch` — because a reader will not invest in a
climb until they have seen the ceiling, and an advantage that only ever wins has no curve.

On win-before-failure — the hard version of this rule, and the ordering constraint that goes with
it — see `meta-knowledge` §4. It applies to any central advantage, not only foreknowledge.

## Self-check

- [ ] The anchor test (§1) passes on chapter 1 — a stranger can answer all three questions
- [ ] For fanfic/transmigration: the reader knows **which** story and roughly **when** in it
- [ ] Every `anchor? yes` term in `lexicon.md` first appears by `anchor_by_ch`
- [ ] Canon/anchor noun count across chapters 1–5 is not zero
- [ ] By `contract_by_ch`, a reader could predict what kind of pleasure ch 10 offers
- [ ] No escalation has outrun the reader's ability to price it (§3) — the mechanism is on the page
- [ ] `opening.stakes_ceiling` is written, and nothing has breached it
- [ ] `opening.promise` has been touched on the page by `promise_touched_by_ch`
- [ ] The central advantage lands a legible win by `first_win_by_ch`, before any failure
- [ ] Chapter 1's four phases are present and roughly proportioned (§5)
- [ ] The MC acts in chapter 1; they are not delivered through it
- [ ] No establishing paragraph, gazetteer sentence, history lecture or date-stamp opening
