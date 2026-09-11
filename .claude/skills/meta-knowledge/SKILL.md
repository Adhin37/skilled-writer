---
name: meta-knowledge
description: Run an MC who knows what happens next - grain, inventory, win before failure, observer paradox. Use when designing a foreknowing MC, whenever foreknowledge is spent, and inside revision-pass.
owns: [foreknowledge-ledger, observer-paradox]
---

# meta-knowledge

An MC who knows what is coming is one of the format's strongest engines and its most reliably
botched one. Two failures, and most drafts pick one and commit:

| failure | symptom | why it kills |
|---|---|---|
| **The oracle** | Foreknowledge is accurate, unlimited and free. The MC pre-empts every threat | No tension after ~chapter 20. Every scene is a formality |
| **The handicap** | Foreknowledge is introduced as already-unreliable and exists only to be wrong | The reader was promised an advantage and shown a disability. They invested in something the author was embarrassed by |

The second is subtler, more common in careful writing, and worse — because the author believes
they are being sophisticated. **A blurb that promises "she knows what's coming" and a plan whose
first foreknowledge beat is *"realizes she can no longer tell fan theory from what she actually
read"* have made a bait-and-switch**, no matter how well the prose behaves.

The correct shape is neither. **Foreknowledge is a resource with a grain, a cost, and a decay rate
the MC causes themselves.** It works, then it costs, then it frays, then it betrays — in that
order.

**Scope.** Any MC with `mc.foreknowledge` set: reincarnators, regressors, transmigrators into a
known story, fanfic self-inserts, prophecy-holders, and time-loopers. Not genre-savvy characters
who merely know tropes — that is `voice-separation`, not this.

---

## Sections that live in `references/`

Section numbers are stable — other skills cite them — so the gaps are deliberate.

| § | file | open it when |
|---|---|---|
| 6, 7 | `references/failure-modes.md` | foreknowledge is not landing (it is always one of seven named shapes), or you are deciding how much of the source the prose may assume |

The revision-time check is `references/audit-card.md`, opened by `revision-pass` Pass 9c.

## 1. The grain

Foreknowledge is never "they know the plot." It is declared at a **grain**, and the grain is a hard
ceiling on every plan the MC is allowed to make.

| grain | can | cannot | best for |
|---|---|---|---|
| `episode-precise` | name events, their order, roughly when | know what happened offstage in the source; know anything after their knowledge ends | short runways, thriller pacing |
| `major-beats` | name the big turns and who is at them | order them confidently; put dates on them | most stories — the default |
| `impressions` | recognise a name; feel dread at a place; know a person is dangerous | state what happens, or when | long runways, character-first work |
| `fandom-corrupted` | recall vividly, in detail — **and be wrong** | distinguish what they read from what they were told about it | self-inserts; the richest option |

Set `mc.foreknowledge_grain` at `mc-design` time. Then hold it:

> **An `impressions` MC does not produce a date. A `major-beats` MC does not produce an order.**
> If a plan on the page requires precision the grain does not license, the plan is a cheat, and a
> reader who knows the source will feel it before they can name it.

`fandom-corrupted` deserves its own note, because it is the honest model for most self-inserts and
it is *generative rather than limiting*: the MC's memories are a blend of the text, other people's
theories, and things they argued about online years ago. They cannot separate the strands. This
produces confident, specific, **checkable** wrongness — which is a plot engine, where vague
uncertainty is only a fog.

## 2. The inventory scene

> **Early — by `opening.first_win_by_ch` — the MC sits down and works out what they know, how sure
> they are, and what they are going to do about it.**

This is the beat readers came for, and its absence is the loudest possible signal that the author
does not intend to use the premise. **A competent person who wakes up knowing the future makes a
plan.** Not a good plan, necessarily. Not a correct one. But they triage, and they triage on the
page, because that is the scene the blurb sold.

What the scene contains:

1. **The sort.** What do I actually know? What am I sure of, and what am I reconstructing?
2. **The clock.** How long until the first thing I remember? What does that give me time for?
3. **The lever.** Of everything I know, what can a person in my current position *touch*? — this
   is where `state/body.md` and `competence-map` bite: a four-year-old orphan's lever set is
   nearly empty, and discovering that is the scene's turn.
4. **The plan.** One sentence a reader could repeat. It should be *adequate* — the best plan
   available to someone this smart with this information — and it should be **wrong in a way the
   reader cannot yet see**.

**Do not make the MC stupid to preserve tension** (`mc-intel-meter`). Make the plan good and the
information incomplete. A tier-4 MC produces a tier-4 plan; if that plan would trivially solve the
book, the problem is the plot, not the MC.

**Where it goes.** The MC does not need a quiet room. The inventory can run under a chore, a walk,
a fever, an interrogation. What it may not be is a summary paragraph — it is a scene with a turn,
and the turn is usually §2.3, the moment the lever set turns out to be smaller than the knowledge.

## 3. Foreknowledge is not intelligence, and not competence

Three separate axes. Keep them apart:

| axis | owned by | a high value means |
|---|---|---|
| Intelligence | `mc-intel-meter` | infers faster from what is present |
| Competence | `competence-map` | can *do* a narrow set of things |
| Foreknowledge | this skill | holds facts about a future they did not earn |

Neither of the other two axes bends for foreknowledge; each stays with its owner above. What
belongs to this skill is the gap they leave: knowing the answer is not knowing the method, and that gap is where the
best chapters in this subgenre live.

**Foreknowledge is a declared domain in `bible/cast/_competence.md`** with an edge like any other,
and the provenance test applies to every fact stated from it: *read it, was told it, saw it, or
openly guessing.* "I remember" is a provenance — but "I remember, and I read three arguments about
whether it was true" is a better one.

## 4. Win before failure

> **The advantage scores at least one legible, load-bearing win before its first failure, and the
> reader must be able to see the win came from foreknowledge.**
> Enforced as: `foreknowledge_first_win_ch` **<** `foreknowledge_fails_ch`. Both required.

"Legible" and "load-bearing" are both doing work:

- **Legible** — the reader can point to the moment and say *that worked because she knew*. A win
  the MC could have got by being observant is not a foreknowledge win. Somebody should be surprised
  by an outcome the MC was not surprised by.
- **Load-bearing** — it changes something that matters. Correctly predicting the weather is not a
  win. Being in the right room when a decision is made is.

The full arc of the advantage, tracked in `state/foreknowledge.md` §5:

| beat | what it does | typical placement |
|---|---|---|
| Inventory | establishes there *is* an advantage, and its shape | by `first_win_by_ch` |
| **First win** | pays the reader's investment; makes the premise real | `foreknowledge_first_win_ch` |
| First crack | a detail is off. The MC notices; the reader worries | between win and failure |
| **First failure** | it is wrong, and it costs | `foreknowledge_fails_ch` |
| The reckoning | the MC has to act without it | arc climax or later |

**Escalation ladders may not be all-failure.** An arc whose five rungs are five foreknowledge
failures has no ladder — it has a slide. At least one rung is a win the foreknowledge bought, or
the arc is redesigned. See `conflict-engine`.

**`mc.foreknowledge_known_by`** lists who has worked out that the MC knows things they should not.
It starts empty. Every name added is a plot event, so it goes in `state/threads.md` as well, and
the reasoning behind it belongs in §6 of `state/foreknowledge.md`.

## 5. The observer paradox

> **Acting on foreknowledge is the fastest way to destroy it.** The future the MC remembers is the
> future in which they did not act.

This is the engine that makes decay *earned* instead of decreed. Every spend that changes an
outcome moves at least one other ledger row toward `invalidated` — recorded in
`state/foreknowledge.md` §4, cross-referenced to `timeline-engine`'s divergence ledger rather than
duplicated.

| the MC does | first-order | second-order — this is where knowledge dies |
|---|---|---|
| Saves someone who died in the source | that person lives | everything they now do is off-source. Every memory involving them is suspect |
| Warns an institution | the institution acts early | the source's timing is gone. So is every event that depended on it |
| Takes a position that was someone else's | the MC is in the room | that someone else is now somewhere the MC has no memories of |

The practical rule for the writer: **big spends buy big outcomes and cost big swathes of the
ledger.** An MC who understands this — and a smart one will, quickly — starts *rationing* their
interventions, which is a far more interesting character than one who is merely wrong a lot.

`timeline.butterfly_horizon` bounds how far this is simulated before it becomes background.

**The one thing that does not decay** is knowledge about *people's natures* — what someone wants,
what they are afraid of, what they will do under pressure. Events butterfly; character does not,
until the MC changes the person. This is what a foreknowing MC should end up trading on once the
event knowledge is spent, and it is the graceful path out of the oracle problem.

## Integration

| when | do |
|---|---|
| `mc-design` | Set `foreknowledge`, `foreknowledge_grain`, `first_win_ch`, `fails_ch`. Create `state/foreknowledge.md` and fill §1–§2 |
| `chapter-plan` | Schedule the inventory scene, the first win and the first failure as explicit rows, in that order. Check the arc ladder is not all-failure (§4) |
| `write-chapter` step 1 | Does this chapter spend foreknowledge? At what grain? What does the spend invalidate? |
| `write-chapter` step 5 | Append to the spend log; move statuses; add the `fk>` CCS line |
| `timeline-engine` | Divergence rows and foreknowledge invalidation are the same event seen twice — cross-reference ids |
| `revision-pass` | The foreknowledge pass. **Open this file; do not work from the checklist summary** — §4 is distributional and cannot be checked from one chapter |

## Related skills

`mc-design` owns the golden finger this usually is · `mc-intel-meter` owns the tier, and the rule
that knowledge is not intelligence · `competence-map` owns the provenance test and holds
foreknowledge as a bounded domain · `timeline-engine` owns divergence, the butterfly budget and the
reactivity dial that decides who reacts to the MC's impossible accuracy · `fanfic-canon` owns what
canon *is* · `story-opening` owns the first-win deadline and the promise ledger ·
`plot-threads` tracks the ones the MC opened by knowing too much.

## Self-check

- [ ] `foreknowledge_grain` is set, and no plan on the page exceeded it
- [ ] The inventory scene happened, on the page, as a scene with a turn
- [ ] The MC's plan is the best one available to someone at their tier with their information
- [ ] `foreknowledge_first_win_ch` < `foreknowledge_fails_ch`, both set
- [ ] The first win is legible — a reader can point to it and see foreknowledge caused it
- [ ] The arc's escalation ladder contains at least one rung the foreknowledge won
- [ ] Every spend this chapter is in the log, with its cost and what it invalidated
- [ ] At least one other ledger row moved toward `invalidated` after a plot-changing spend
- [ ] No fact was stated that fails the provenance test
- [ ] Foreknowledge did not substitute for a skill the MC has not learned
- [ ] Someone, somewhere, is starting to notice the MC is right too often
- [ ] The prose rewards source knowledge without requiring it
