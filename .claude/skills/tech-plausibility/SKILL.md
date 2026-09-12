---
name: tech-plausibility
description: Keep science-fiction technology coherent and consequential - one speculation, honest second-order effects, no hand-waving. Use for scifi when designing the setting or when tech matters.
metadata:
  type: skill
  tier: genre
  force: structural
  when: genre in [scifi] or subgenre in [scifi]
  owns: [speculation-budget, second-order-effects]
---

# tech-plausibility

Genre module — `genre: scifi`. Recorded in `bible/power-system.md` (technology is this genre's
power system) and `bible/world.md`.

Science fiction is not futurism. Its job is not to predict correctly; it is to **follow one
change honestly** and dramatise what living with it costs.

---

## The one speculation

Pick **one** central technology or change the story is actually about. Everything else in the
setting is background and should be treated with a light hand.

Then:

1. **What it does**, in one sentence a reader could repeat.
2. **What it cannot do.** Two limits minimum. Limits are the plot.
3. **What it costs** — energy, time, material, a person, legality, health.
4. **Who controls it.** Access is where science fiction becomes political, and where scenes are.
5. **How long it has existed.** A technology ten years old and one two centuries old produce
   completely different societies; be specific, because everything below depends on it.

## Second-order effects — the part most stories skip

First-order effects are obvious and boring (the car goes faster). Second- and third-order effects
are where the story is.

Ask, for the central speculation:

| domain | question |
|---|---|
| Work | which jobs vanished, which appeared, who is now unemployable |
| Law | what crimes became possible; how enforcement adapted; what is still legal but shouldn't be |
| Class | who got rich; who was made cheap; what the poor version of the technology looks like |
| Intimacy | how it changed families, courtship, grief, raising children |
| Language | the slang it produced; the dead words |
| Body | what people now do to themselves, routinely, that would have been shocking |
| Backlash | who refuses it, and whether they are permitted to |

Answer four of these. They will supply more scenes than the technology itself.

**The poor version.** The single most useful worldbuilding question in science fiction: what does
this look like for someone who cannot afford the good one? That is where the texture is.

## Consistency rules

- **Capabilities are fixed.** A technology that can do X in chapter 5 can do X in chapter 200, and
  everyone in the world knows it. Antagonists have access to the same tech tree.
- **If it exists, it is used everywhere it would help.** The most common scifi defect: a
  capability that appears only when the plot wants it. Ask, for each scene, why the technology is
  not solving this.
- **Costs stay constant** unless something in the story changes them, and then the change is a
  plot event.
- **No technology introduced in the chapter that needs it.** Same rule as `power-system`.
- **Infrastructure implies infrastructure.** Someone maintains it, someone was trained to, someone
  is on call at 3 a.m. Those people know things and can be characters.

## Hardness

Decide and hold a level; mixing them is what makes a setting feel arbitrary.

| level | contract with the reader |
|---|---|
| **hard** | real physics; violations are the story's central question and are argued for |
| **middle** | one or two named impossibilities (FTL, artificial gravity), rigorously consistent, everything else follows known science |
| **soft** | technology is texture and metaphor; consistency of *rules* still required, physics not |

Most serials sit at middle. Whatever the level, **internal consistency is non-negotiable** — a
soft setting is not an inconsistent one.

## Writing technology on the page

- **Through use, never through specification.** Characters do not explain their own tools to each
  other. The reader learns a technology by watching it work, break, and be worked around.
- **Familiarity.** Characters are bored by their own world. The wonder belongs to the reader, and
  it arrives through precision, not through awe.
- **The interface, not the mechanism.** What a character *does* with a thing — the gesture, the
  wait, the annoyance — is more evocative than how it works.
- **Failure states are characterisation.** What people do when the technology fails tells the
  reader what it means to them.
- **Jargon budget.** One new term per chapter early, fewer later. Every term goes in
  `bible/lexicon.md` with a plain-English meaning. If a term needs a gloss every time it appears,
  rename it.

## AI, uploads, and other minds

If the story includes artificial minds, decide early and record: are they people? Who says so, and
who profits from the answer? Do not let the story be vague about it while borrowing the emotional
weight of both answers.

**An ASI is not omniscient, it is differently ignorant.** Declare it `knowledge_scope: broad` with
`scope_kind: artificial`, and fill the boundary (`competence-map/references/broad-knowledge.md`): it was trained on what
somebody fed it, it has no embodied knowledge — it has never lifted anything, been cold, or waited
— and it interpolates confidently across its blank regions without being able to tell those regions
from the rest. Its recall is superhuman and its judgement about people is a guess dressed as a
number. Then bound the **access** rather than the knowledge: latency, an airgap, a bad channel, a
query budget, an operator who chooses the questions. An unbounded oracle dissolves every mystery in
the book, and the limit belongs in this file alongside the other capability limits.

## Handoff to the world

The second-order effects worked out here are recorded and extended in `bible/society.md` via
**`social-fabric`** — that skill takes the central speculation down through institution, market
and household, names the occupation it destroyed and the workaround people use where it fails.
In science fiction those consequences *are* the genre; do not leave them as a list here.
`world-texture` governs how they reach the page: consequence and friction, never a briefing.

## Self-check

- [ ] The central speculation has been propagated through `social-fabric` §2
- [ ] One central speculation, stated in one sentence
- [ ] Two hard limits recorded
- [ ] Four second-order effects worked out, including the poor version
- [ ] Antagonists have comparable access to the tech
- [ ] Nothing was solved this chapter by an unestablished capability
- [ ] No character explained their own technology to someone who lives with it
- [ ] Users know how to *use* it, not how it works — the technicians are separate people
- [ ] Any artificial mind has a declared boundary and a bounded access channel
- [ ] Every new term is in the lexicon with a plain meaning
