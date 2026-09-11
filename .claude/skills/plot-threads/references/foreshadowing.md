---
type: reference
owner: plot-threads
description: planting a setup, paying a thread, or auditing the novel for forgotten promises
---

# plot-threads — foreshadowing, payoff quality and the audit

Open this when planting a setup, when a thread is about to be paid, or when auditing a novel for forgotten promises.

---

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

```bash
python3 scripts/sw.py state novels/<slug>
```

Cross-references the board against the ledger: which thread each block operated on, how long ago
each open thread was last touched, whether that matches its declared `tension`, and any id
operated on in the ledger with no row on the board. Run it before the manual audit below — it
finds the dropped thread, and you decide what to do about it.


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
