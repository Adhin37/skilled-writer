---
type: audit-card
owner: timeline-engine
dispatcher: revision-pass
pass: "4"
pass_kind: mechanical
description: The world moved on its own clock, and the ending is still reachable
when: always
---

# timeline-engine — audit card

Opened by `revision-pass` **Pass 4**. The world track is the half of structure that has no scene
to audit, which is why it is checked from the ledger rather than from the page.

## The gate

> **Is the `wld>` line filled, with something the POV character does not know?**

A world that only moves when the MC is watching is a stage set. The offstage question is answered
every chapter, whether or not it reaches the page this time — that is what makes the reactivity
dial mean anything.

## Checks

- [ ] The chapter's events match `timeline.reactivity`. A dial at 4 that produced no reaction to
      last chapter's noise is a dial nobody is turning
- [ ] Every world-track event this chapter is **logged in the divergence ledger**, with what it
      opened. An unrecorded divergence gets re-invented differently four chapters later
- [ ] In-world time agrees with `state/timeline.md`, and elapsed time is consistent with how long
      things take
- [ ] Crisis count is within `timeline.crisis_cap` and never above 3. When everything is urgent,
      nothing is — demote one to a pressure
- [ ] Nothing this chapter took an `ending.non_negotiable`, and `ending.contract` is still
      reachable. This is absolute: the world may cost the MC anything except the ending the user
      asked for
- [ ] Any escalation opened something as well as closing something
- [ ] Propagation stayed inside `timeline.butterfly_horizon` — beyond it, change is narrated as
      background rather than simulated
- [ ] Fanfic: this arc moved at least one canon event, and at least one canon character changed a
      decision because of the MC (`fanfic-canon`)

## Where it fails most often

| symptom | what it actually is | go to |
|---|---|---|
| The `wld>` line restates what the MC saw | the offstage question was answered onstage | it is what the MC does *not* know |
| Every faction reacts, immediately and correctly | reaction profiles have collapsed into one | `references/reaction-and-governor.md` — at least one driver is Indifferent |
| The world reacts so hard the MC cannot act | the governor is off | same file; the dial has a brake for this |
| A three-day journey happened overnight | distance stopped being load-bearing once the reader priced it | move the scene, not the map (`story-bible`) |
