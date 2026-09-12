---
type: audit-card
owner: fanfic-canon
dispatcher: revision-pass
pass: "5"
pass_kind: distributional
description: Canon fidelity, the OOC budget, and whether the reader can place the story
when: genre in [fanfic] or subgenre in [fanfic]
---

# fanfic-canon — audit card

Opened by `revision-pass` **Pass 5** in fan fiction. The first check is the one that is invisible
from the inside, so run it first and mechanically.

## The gate — chapters 1 to `opening.anchor_by_ch`

> **Count the chapter's canon proper nouns. Zero is a defect.**

You know the source too well for its absence to register. A measured example ran five chapters and
10,000 words with no occurrence of its setting's name, its central power, its factions, or any
canon proper noun, and read as unplaceable to everyone but its author. `sw lint`'s anchor count is
the countable half; the judgement is whether a new reader could say which story this is.

## Checks

- [ ] No text reproduced from the source — not a line of dialogue, not a phrase of narration
- [ ] Every canon event this chapter kept or dropped is traceable to `fanfic.divergence_point`,
      not to what the scene needed
- [ ] Each canon character's defining trait survived the chapter intact
- [ ] Every departure from canon behaviour is logged with its justification, and the arc is
      within `fanfic.ooc_budget`
- [ ] Nobody knew a canon event they were not present for
- [ ] Nobody but the MC knew anything from the future — and if the MC did, `meta-knowledge` ran
- [ ] Canon characters sound like the source, not like the narrator
- [ ] Every original character passes the OC test
- [ ] Nothing outside `fanfic.canon_scope` was treated as binding

## Where it fails most often

| symptom | what it actually is | go to |
|---|---|---|
| A canon character is sharper or blanker than the source | the intel tier moved to fit the plot | `mc-intel-meter` — the tier is set from canon behaviour and then held |
| Everyone sounds like the POV character | the OOC readers actually complain about, with no line to point at | `voice-separation` |
| A canon character knows the whole setting | fandom's quiet promotion of narrow expertise | `competence-map` — an unlisted domain is `none` |
| Canon happens offstage and unchanged | the commentary-track defect: fidelity without consequence | `timeline-engine` — every arc moves at least one canon event |
| The source's treatment of a group was inherited | canon is not a licence | `bias-guard`, which overrides this skill and every other |
