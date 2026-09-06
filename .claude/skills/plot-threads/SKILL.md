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

## Foreshadowing

**Plant three times, in decreasing subtlety.** The reader should feel they *could* have seen it.

1. **Ambient** — the detail appears as texture, doing another job entirely.
2. **Noticed** — a character remarks on it and moves on; nothing is made of it.
3. **Loaded** — it appears at a moment of tension without explanation.

Then it pays. A payoff planted once feels arbitrary; planted four times, telegraphed.

**Plant early, pay late.** The best material was planted before you knew what it was for. When
drafting, deliberately place one concrete, unexplained detail per chapter — an object, a habit, a
name, a scar. Log them in a `setup` thread with a far-off `due`. Later chapters will find uses,
and a story that pays off its own accidents feels designed.

**Never explain the foreshadowing on payoff.** No "she suddenly remembered the old man's words".
The reader makes the connection; that pleasure is the whole point.

## Payoff quality

A payoff must be:

- **Surprising and inevitable** — not what the reader predicted, but consistent with everything
  they were given.
- **Earned by cost** — the answer should hurt someone, or change what the MC must do next.
- **Load-bearing** — it changes the situation. A reveal that changes nothing is trivia.
- **Question-generating** — closing a big thread should open a smaller, sharper one. See
  `conflict-engine`.

**Never** pay off with information the reader could not have reached: a hidden twin, an unmentioned
faction, a rule of the world introduced in the same chapter it becomes decisive.

## Audit procedure

Run at every arc boundary, and whenever the user asks what is unresolved.

1. List every thread with status `open`/`escalated`.
2. Flag any `cold` for 25+ chapters → quarantine section of `threads.md`.
3. For each quarantined thread choose: **schedule** a payoff in the next arc, **subvert** it
   deliberately on the page, or **retire** it with an in-story acknowledgement (a character notes
   it no longer matters, and the reason is interesting).
4. Check the mix: at least one novel-level, two arc-level, three chapter-level.
5. Check for over-promising: more than 12 open threads means the next arc pays some off rather
   than opening more.
6. Check every thread's `due` is inside the planning horizon or explicitly novel-level.

## Anti-patterns

| pattern | fix |
|---|---|
| The forgotten mystery | the ledger, audited every arc |
| The instantly-resolved question | give every mystery at least one arc of life |
| Foreshadowing with a flashing arrow ("she'd remember that later") | plant it doing another job |
| Payoff by exposition — a character explains the whole answer | dramatise it: the reveal should happen *to* someone |
| The reveal that changes nothing | attach a consequence before writing it |
| Too many threads opened in one arc | opening is easy; budget payoffs first, then open |

## Self-check

- [ ] Every thread op in this chapter is in the CCS block and the ledger
- [ ] Between 5 and 9 threads open
- [ ] All three tiers represented
- [ ] Every open thread has a `due` inside the plan
- [ ] Nothing has been cold for 25+ chapters without being quarantined
- [ ] Any payoff this chapter was planted at least twice, earlier
- [ ] No payoff explained its own foreshadowing
