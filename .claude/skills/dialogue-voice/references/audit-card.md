---
type: audit-card
owner: dialogue-voice
dispatcher: revision-pass
pass: "2"
pass_kind: distributional
description: Lines that sound spoken, carry subtext, and could not be swapped
when: always
---

# dialogue-voice — audit card

Opened by `revision-pass` **Pass 2**. `voice-separation` audits the cast as minds; this card
audits the **lines**. `sw lint`'s texture notes — fragment rate, contractions, interruptions,
turn length — are the countable half and say nothing about whether anyone sounds like a person.

## The gate — read the longest turn aloud

> **If you run out of breath before the speaker does, it is prose.**

No turn past about 45 words, or exactly one in the chapter and you can say who lets them finish
and why. The essay tells are what share and contraction rate cannot see: stacked subordinate
clauses, the aimed parenthetical aside, the epigram close, pre-announced self-qualification
(`SKILL.md` §How it sounds spoken).

## Checks

- [ ] Tags stripped — is every tier-A and tier-B speaker still identifiable?
- [ ] At least one exchange per scene runs on **subtext**, and the narration did not explain it
- [ ] Every speaker in a loaded scene has a `won't say`, and it held
- [ ] Turn lengths match each speaker's declared number; every beat comes from that character's
      hands or pressure move, not from the default gesture set
- [ ] Somebody was interrupted, trailed off, or answered a question that was not asked
- [ ] Swap test on the walk-ons: could another extra have this scene with no edit?
- [ ] Each speaker wants something distinct from this conversation
- [ ] No dialogue explaining what both speakers already know
- [ ] Nobody explained a subject their competence map does not cover, and somebody said they did
      not know, deferred, or turned out to be wrong (`competence-map`)
- [ ] `said` and `asked` unless a stronger verb genuinely earns its place
- [ ] Spoken share is 25–40% of the chapter — under 10% is a defect rather than a style, and the
      count is `"…"` only: thought and meta are not dialogue

## Where it fails most often

| symptom | what it actually is | go to |
|---|---|---|
| Every line is answerable and complete | nobody is talking, they are reading prose aloud | `references/spoken-register.md` |
| Two speakers are distinct on paper and identical on the page | they share a cadence | `voice-separation` §3, the cadence test |
| The subtext is explained in the beat after it | the narration does not trust the line | delete the beat |
| A character says exactly what they mean, always | no `won't say` | `references/subtext.md` |
