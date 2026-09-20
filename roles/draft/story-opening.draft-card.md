---
type: draft-card
owner: story-opening
dispatcher: write-chapter
phase: A
order: 14
description: The anchor debt, this chapter's world entry, the pace being set, and the ceiling check
when: chapter <= opening.contract_by_ch + 2
---

# story-opening — draft card

Opened by `write-chapter` **Step 1**, but **only for chapters up to `opening.contract_by_ch + 2`**.
Outside that range this card does not apply and `hook-and-pacing` has the wheel. Written here rather
than summarised there, because about 60% of readers who open chapter 1 reach chapter 2, and the
decisions that move that number are made before drafting.

**Produce:** the anchor debt — what a reader still cannot answer about world, place or canon
position, and which beat pays it — this chapter's **world entry**, the **rate** these chapters are
promising, and the ceiling check on any escalation.

## The anchor

> By the end of chapter 1 a reader can say **what kind of world this is**, **what place they are
> standing in**, and **what the POV character wants this week**. For fanfic or transmigration, also
> **which story they are in and roughly when**.

That is the whole requirement — no history, no map, no magic system, no faction list. Test it by
asking a stranger three questions: what kind of story, where and when, what does this person want.
**Three shrugs is a failed opening**, however good the prose.

Delivered on the same channel ladder as `world-texture` §1: a rule biting someone, a character
working around the world, an unexplained assumed reference, and only then direct statement.
**One named proper noun a reader could search is worth three pages of atmosphere.**

**Anchor vocabulary is front-loaded, never saved.** Every `anchor? yes` term in `lexicon.md` whose
first appearance is later than `opening.anchor_by_ch` is a defect. Deferring the word that names the
genre does not build mystery — a reader who does not know what kind of story this is has no
question, only a vague unease indistinguishable from reading something bad. In fanfic this is the
single most common structural defect, because the writer's own fluency makes the absence invisible.

## The world entry — one fact, this chapter, on a channel

The anchor is a deadline. This is the curve underneath it. `plan/chapters.md` rows 1–5 carry a
**world entry** per chapter (`chapter-plan` §Arc 1): the one fact that arrives here and the channel
that carries it. Read this chapter's row and deliver that fact. If the cell is empty, choose the
fact now and write it back before drafting.

**Spend one, not four.** An opening that hands over the whole world in chapter 1 has nothing left
to give in 2 through 5, and a reader told everything at once keeps only the part that bit
somebody. Chapter 4 owes a new fact as much as chapter 1 does.

**And the fact has to arrive as something handled.** What did this chapter's POV character's hands
or feet actually deal with — what got pushed past, paid for, picked up, put down? A world that is
only smelled, lit and felt is atmosphere. It passes every budget `world-texture` owns, and the
machine default is worst precisely here: in a chapter's first fifteen sentences, at more than twice
the human rate (`roles/draft/world-texture.narrative-space.md`).

```
felt        The compound smelled of wet stone and cold incense, and the quiet had weight.
handled     The gate stuck where it always stuck, and she put her hip into it without
            looking, the way you do with a door you have opened a thousand times.
```

The second line is an anchor, a characterisation, and a fact about how long she has lived there.
Openings buy the most from this, because the opening is where the page is worst at it by default.

## The ceiling check — before scheduling any escalation

> A consequence may not escalate past the reader's ability to price it.

1. **What makes this bad?** Name the mechanism — the file, the tribunal, the debt, the rival clan.
2. **Is that mechanism on the page yet?** Not in the bible. On the page, where a reader saw it.
3. If no: put it on the page first, as consequence — or **hold the escalation**.

The cheapest fix is almost always a bystander. One scene of the machinery consuming a stranger
prices every threat that follows for the rest of the book. In the opening arc the reader's
*understanding* climbs at least as fast as the danger.

## The promise ledger

`opening.promise` is touched on the page by `promise_touched_by_ch`, and the central advantage lands
one legible win by `first_win_by_ch` — **before** its first limit (`scaling.first_limit_by_ch`).
"Touched" is a low bar and is meant to be: present, not resolved.

## The pace contract — these chapters are setting it

`opening.pace_contract` is the tempo this book promises, written in the author's own words. Read
it, then answer one question before drafting: **at the rate this chapter runs, what does chapter 40
look like?**

If the honest answer is *faster than this book can sustain*, the chapter is overspending. An
opening drafted to convert runs quicker than any arc can keep up with, and the reader who
subscribed at that rate is the one who leaves around chapter 12 saying it stalled — not because it
became slow, but because it changed. Whatever these three chapters do is the promise.

If the slot is empty, fill it in `novel.md` now. Three chapters from here it stops being a decision
and becomes a measurement of what was already published.

Drafting chapter 1 itself: `roles/draft/story-opening.chapter-one.md`.
