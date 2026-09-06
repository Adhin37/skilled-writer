---
name: plot-threads
description: Open, track, escalate and pay off every promise made to the reader — mysteries, debts, threats, oaths, foreshadowing and setups, plus the opening arc's promise ledger — using the thread ledger. Use when planning chapters, when drafting, and when auditing a novel for forgotten setups.
---

# plot-threads

Every unanswered question, unpaid debt and unfired gun is a **promise**. Readers keep a tally
whether or not the author does. `state/threads.md` is that tally, made explicit.

The defect this prevents is the most damaging one a long serial can have: threads quietly
abandoned. A reader forgives a slow payoff. A reader does not forgive discovering, at chapter 180,
that the story forgot its own chapter-12 mystery.

---

## What lives in `references/`

| file | open it when |
|---|---|
| `references/foreshadowing.md` | planting a setup, paying a thread, or auditing the novel for forgotten promises |

## Thread anatomy

| field | notes |
|---|---|
| `id` | `T01`, `T02`… never reused, even after payoff |
| `thread` | the promise in one line, phrased as what the reader is owed |
| `opened` | chapter |
| `type` | `mystery` `promise` `debt` `threat` `relationship` `setup` `oath` `secret` |
| `tension` | `hot` (touched in last 5 ch) · `warm` (last 15) · `cold` (dormant) |
| `due` | the chapter by which it must be advanced or paid |
| `status` | `open` `escalated` `paid` `subverted` `abandoned` |
| `payoff` | how it landed, filled in on payoff |

## Thread hygiene

**Counts.** Roughly 5–9 open threads at any time. Below 4, the story has nothing pending and reads
as episodic. Above 12, readers lose track and nothing feels urgent.

**Mix.** At any moment, aim for:

- 1–2 **novel-level** (the ending target; opened early, paid at the end)
- 2–3 **arc-level** (opened and paid within ~25 chapters)
- 3–4 **chapter-level** (opened and paid within 1–5 chapters — these produce the sense of momentum)

Chapter-level threads are what make a serial feel like it is *moving* even during a slow arc. If
readers say the story is dragging, this tier is usually empty.

**Every thread gets a `due`.** No exceptions. A promise without a deadline is a promise you will
forget. `due` may be revised, but only deliberately, and only forward once.

**Touch cadence.** A thread should be *referenced* — not necessarily advanced — at least every
15 chapters, or it goes cold. One clause is enough.

### Ageing — the anti-deferral rule

The most common complaint about long-running web serials is not bad prose. It is **perpetual
deferral**: hundreds of chapters in which everything is pending and nothing has landed. It does
not arrive as a decision. It accumulates one reasonable postponement at a time, and each
individual postponement is defensible.

Three rules stop it, and all three are checkable:

1. **Every arc closes at least one thread on the page.** Not advanced, not recontextualised —
   **paid**, with the payoff visible to a reader who is not tracking thread ids. An arc that only
   defers has taught the reader that nothing here resolves. `sw state` reports an arc that closed
   without a `v` operation in its ledger blocks.
2. **A thread past its `due` gets a reason, in the `carried` column, in the same pass.** One
   clause and a new `due`. *"Carried to 78: the informant's price rose and she cannot pay it yet."*
   An unexplained overrun is a forgotten promise wearing a deadline.
3. **A thread carried twice is escalated or abandoned.** Escalated means the reader can *see* it
   moving — the debt grows, the threat acquires a name, the secret is now known by one more
   person. Abandoned means it is retired on the page, deliberately, and somebody notices.

**The reader's clock is not the author's.** A thread opened in chapter 3 and paid in chapter 200
was open for a year and a half of their life. Novel-level threads earn that; a chapter-level
thread that has been running for forty chapters was mis-tiered when it was opened.

**What counts as payment.** The promise the reader was made, answered — not a different, smaller
promise answered in its place. A mystery paid by revealing that the answer is another mystery has
not been paid; it has been renamed. Subversion is legitimate and is not this: a subverted thread
answers the question and the answer is not what was expected.

**At most two active subplots per arc**, alongside the main line. The counts above are all
threads including the chapter-level ones that supply momentum; *subplots* are the arc-level lines
that need their own scenes and their own escalation. A third competes for the same page space and
is how threads get dropped — the reader does not notice a subplot vanish, they notice the story
losing shape. Track each one's status at every arc boundary as resolved, paused or escalated.

### The promise ledger — arc 1 only

The blurb makes a promise, and readers arrive holding it. Four threads open before chapter 1 is
written and are tracked like any other, but they are due earlier than anything else in the book:

| thread | due | source |
|---|---|---|
| The world anchor — what kind of story, and for fanfic which one and when | `opening.anchor_by_ch` | `story-opening` §1 |
| The genre contract | `opening.contract_by_ch` | `story-opening` §2 |
| `opening.promise` touched on the page | `opening.promise_touched_by_ch` | `story-opening` §4 |
| The central advantage's first legible win | `opening.first_win_by_ch` | `meta-knowledge` §4 |

**These are promises to a reader who has not yet decided to keep reading**, so they cannot be
paid late the way an ordinary thread can. A blurb promising foreknowledge attached to ten thousand
words in which the MC never thinks about the future is a broken promise, not a slow burn.

## The four operations

| op | notation | meaning |
|---|---|---|
| open | `~T14` | the promise is made. Must be noticeable to the reader without being announced |
| advance | `^T03` | new information, higher stakes, or a step closer. Does not resolve |
| pay | `vT09` | the promise is kept |
| abandon | `xT21` | deliberate retirement — requires a written reason and, usually, an on-page acknowledgement |

Record ops in the chapter's CCS `thr>` line and update the ledger.

## Self-check

- [ ] Every thread op in this chapter is in the CCS block and the ledger
- [ ] Between 5 and 9 threads open
- [ ] All three tiers represented
- [ ] Every open thread has a `due` inside the plan
- [ ] Nothing has been cold for 25+ chapters without being quarantined
- [ ] Any payoff this chapter was planted at least twice, earlier
- [ ] No payoff explained its own foreshadowing
