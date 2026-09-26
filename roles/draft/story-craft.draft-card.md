---
type: draft-card
owner: story-craft
dispatcher: write-chapter
phase: A
order: 1
description: Which beat is played and which is reported
when: always
provenance: docs/creative-latitude.md
---

# story-craft — draft card

Opened by `write-chapter` at drafting time. The scene-versus-summary decision, in the form you need
while writing rather than while planning.

**This is the first card you open, not the fifteenth.**

## Before the rule: three ways this chapter could go

Write **three one-line answers** to the chapter's central question — how the plan row's `event`
actually happens — and take the second or third unless the first is clearly the best story.

```
1  She confronts Marek about the ledger.                     <- the first thing anyone would write
2  She lets him keep believing she hasn't noticed, and
   uses the afternoon he thinks he has.
3  She tells Sabra instead, who is the wrong person to tell.
```

Sixty seconds, and it is the only step in the whole draft loop that **widens** rather than
narrows. Every other card in Phase A converges on one answer, which is correct for each of them
individually and, summed over nineteen cards, produces the median of everything the rules allow —
competent, defensible, and the thing a reader means by "machine-written" when they cannot point at
a line.

Three rules make it work rather than becoming a ritual:

- **Candidate 1 is the obvious one.** Write it down deliberately so the other two have something
  to be different from. Do not try to make it good.
- **They differ in what somebody *does*,** not in tone, wording or how much is revealed. Three
  phrasings of one beat is one candidate.
- **Taking candidate 1 is allowed** — say why in the brief, in a clause. A card that can only be
  answered one way is a card that is not being used.

The candidates are cheap here and expensive later: this is the last point at which the chapter is
still one line long.

**Number them, because the numbers are written down.** The rejected two and the reason the taken
one won go on the brief's `cand` line, and from there to the CCS block's `cand>` line at step 5
(`roles/shared/continuity-summary.block-format.md`). That ledger line is where this step's output
survives the run: before it existed, benchmark run #4 ran five chapters through this card and no
measurement could tell whether the step had happened at all.

**The rule: the important beat gets the scene.** The chapter's `event:` field names it. The test
is arithmetic, and it is the one to run first:

> **Is the `event` scene the longest scene in the chapter?**

If not, the chapter is not ready. Not "add words to it" — find out why the drafting is avoiding
it, because that is almost always the real problem.

**The same rule holds across the chapter break.** When the last chapter closed by promising a beat
on the page — *"I'll tell him I'm out on the east road"*, said to the one person the lie will
cost — this chapter plays that beat, lands its consequence, or its brief names the chapter that
will. Opening two days later with the beat stepped over is the past-perfect skip at the scale of
the book, and a cold reader named exactly that scene as the loss they felt most. Read the previous
block's `hook>` and `open>` lines at Phase A for anything spoken aloud as a next move.

Benchmark run #2 is what this test exists to catch. Its plan was strong: chapter 2 walks into a
massacre and carries out a survivor, chapter 4 is the governor personally probing a lie. Those
chapters ran 1,457 and 1,213 words and were pitched exactly like the chapter about persuading a
child to eat rice. Nothing was mis-planned. The set pieces were simply never *played* — they were
summarised in scene, at a controlled distance, and closed on a quiet ironic line. A story that
does that to its own turning points is rushing however well each sentence reads.



- [ ] Name this chapter's most important beat. It is in **scene**, not reported
- [ ] Every beat given summary is a bridge — travel, repetition already established, elapsed time in
      which nothing turned
- [ ] Nothing the reader will later be asked to feel happened offstage
- [ ] No past-perfect clause carries a turn. Scan for `had <verb>ed`: if something is changing
      inside that sentence, a scene was skipped — play it, or cut the reference and let the reader
      meet it fresh
- [ ] A win in this chapter was bought by a failure the reader **watched**, not one they were told
      about
- [ ] The `event` beat is **dramatized, not narrated past**: it happens in front of the reader, in
      real time, with the POV character inside it rather than assessing it afterwards

**In the opening arc, additionally:**

- [ ] The reader has watched the ordinary world work before it breaks
- [ ] Anyone carrying a scene was met before they were asked to carry it
- [ ] A rule bit somebody before it bit the protagonist

**Build-up is not a slower chapter.** It is the same want, friction, change, cost and hook, played
instead of summarised. If a chapter feels like it needs to slow down, the fix is almost never fewer
events — it is one of the events getting the scene it deserved.

**The follow-through is the pacing dial.** After a hard beat, a short reaction → dilemma → decision.
Skipping it entirely makes a chapter a highlight reel; overrunning it stops the story
(`scene-craft` §The follow-through).

If a box fails, the repair is the same one every time: find the beat that was reported and play
it — the want, the friction, the turn, in front of the reader. `roles/shared/story-craft.scene-and-summary.md`
carries the worked decision and the past-perfect catalogue.
