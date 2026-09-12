---
type: audit-card
owner: plot-threads
dispatcher: revision-pass
pass: "4"
pass_kind: mechanical
description: Thread ops match the plan, ages are inside the horizon, payoffs were planted
when: always
---

# plot-threads — audit card

Opened by `revision-pass` **Pass 4**. Mostly countable against `state/threads.md` and the plan
row, which is why it is cheap and belongs early in the pass.

## The gate

> **Does every thread operation in the chapter appear in the plan row, the CCS block and the
> ledger — and nowhere else?**

A chapter that opened a thread the plan did not is not necessarily wrong; it is unrecorded, which
is how a promise gets forgotten. Amend the plan row and check the next three
(`revision-pass/references/fixing-and-reporting.md`).

## Checks

- [ ] Between 5 and 9 threads open, across all three tiers
- [ ] Every open thread has a `due` chapter inside the plan
- [ ] Nothing has been cold for 25 or more chapters without being quarantined with a stated
      reason. **Perpetual deferral is the most common complaint about long serials**
- [ ] Any thread past its horizon was escalated, paid, or deferred on the page — not silently
      carried
- [ ] Any payoff this chapter was planted at least twice, earlier, and the plants are findable
- [ ] No payoff explained its own foreshadowing back to the reader
- [ ] If this chapter closes an arc, at least one thread closed **on the page**

## Where it fails most often

| symptom | what it actually is | go to |
|---|---|---|
| The ledger is current and the chapter still feels aimless | threads are open but none is due soon | pull a `due` forward; an open promise with no deadline is not pressure |
| A payoff landed and felt unearned | one plant, or three plants all at the same subtlety | `references/foreshadowing.md` |
| Twelve threads open | the reader is tracking more than they can hold | close or merge two |
| A reveal arrived with its own explanation attached | the foreshadowing was audited back to the reader | cut the retrospective clause; trust them |
