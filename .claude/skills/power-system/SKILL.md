---
name: power-system
description: Design and enforce a magic, cultivation or superhuman system with hard costs and limits. Use for fantasy, scifi and progression novels when building it, granting an ability, or using power.
---

# power-system

Genre module — fantasy, scifi, progression. Maintained in `bible/power-system.md`.

Reader satisfaction in this format comes from **predictable rules broken at a price**, not from
escalating magnitudes. A reader who can tell what is impossible is a reader who can be surprised.

---

## The four hard rules

Every system needs all four written down before chapter 1.

**1. Cost.** Every use takes something measurable. Name the unit. Fatigue is the weakest choice
because it resets overnight; the strongest costs are ones that accumulate or that others can see.

Good cost axes: time · memory · body (permanent) · reputation (visible use is evidence) ·
relationship (someone pays) · moral (it works on people) · finite material · debt to a party with
its own interests.

**2. Limits.** At least two sentences beginning "this can never…". Limits are where plots come
from — a locked door is worth more than a key.

**3. Learning curve.** How long a new capability takes and what acquiring it costs. If capability
arrives by discovery rather than by work, the reader stops believing in the effort.

**4. Counter.** How a weaker person beats a stronger one. **If there is no answer, the system is
broken** and the story loses tension the moment the MC is strong. Preparation, terrain, numbers,
information, and the stronger party having something to lose are all valid counters.

## Sanderson's law, stated for this format

*Your ability to solve a problem with magic is proportional to how well the reader understands
it.* Corollaries for a serial:

- A problem may only be solved with a capability the reader has already seen used **and seen
  fail**. The failure is what makes the success legible.
- Unexplained power may create problems, threaten and mystify — it may never resolve a climax.
- A new capability arriving in the chapter that needs it is a deus ex machina regardless of how
  it is foreshadowed *within* that chapter.

## Progression without creep

The genre's core pleasure is watching someone get stronger. Its core failure is that strength
outruns story: by chapter 100 nothing can threaten the MC, so the author invents a bigger sky, and
the reader stops caring about magnitudes.

**The curve itself belongs to `power-scaling`**, which owns the ladder, the distance between the
MC and the opposition, the size of a single gain and the price of a temporary boost. The gain log
lives in `state/power.md` §4, where it is in the read-set and `sw curve` can check it — a table in
`bible/` was never read by anything. This skill owns what a power *is*; that one owns how far
ahead of the MC the world stays.

What stays here is the rule the gain log enforces:

**Every gain must create a new problem.** If it only solves problems, do not grant it. Examples:

- Power that is visible makes the MC identifiable to people hunting them.
- Power that needs fuel makes the MC dependent on whoever sells it.
- Power that hurts people makes allies afraid.
- Power that requires a state of mind costs whatever produces that state.
- Power that grows on a schedule makes the MC's time valuable to others.

**Threat scaling.** After a gain, the next threat is not a stronger opponent — it is a threat the
new power **cannot address**. That is what keeps the escalation axis on stakes (see
`conflict-engine`) instead of on numbers.

**Pace.** A meaningful gain every 15–25 chapters (`scaling.gain_gap_min`). More often and gains
stop registering; less often and progression-genre readers leave. Between gains, growth is in
*skill* — new applications of the same capability, which is cheaper and reads as intelligence.

## Tiers

Tiers are an organising tool for you, not vocabulary for the reader.

- Keep tier names out of the prose wherever possible. Show tier through what someone can and
  cannot do.
- **Never open a chapter with a rank recital.** See `mtl-detox`.
- The MC's position on the ladder should be *unclear to the MC* sometimes. Certainty about one's
  own rank is a xianxia habit that removes tension.
- Avoid making tier the answer to conflicts. If the higher tier always wins, there is no story
  after the reader learns the ladder.

## Writing power on the page

- **Cost is shown in the same scene as the use.** Not later, not narrated afterwards.
- **Second use is different from first use.** A capability the reader has seen should not be
  described again at the same length. Compress; spend the words on what is new.
- **Show it fail before it matters.** Every entry in the MC's kit table has a "seen failing at"
  column. Fill it before the ability is load-bearing.
- **Sensory signature per ability.** Each capability has its own two details — what it does to the
  air, the body, the light, the sound. Reuse them; that is how a reader recognises it mid-fight.
- **Never explain mechanics during action.** If the reader needs the rule, they needed it two
  chapters ago.

## Cultivation-specific notes

If the novel uses a cultivation frame, keep the structure and drop the corpus habits:

- Realms and breakthroughs are fine. Realm recitals, sect-tournament brackets as plot, and
  bottleneck-then-epiphany resolution are not.
- A breakthrough must be **paid for and costly**, not the result of an insight arriving at the
  right moment.
- Resources (pills, techniques, artifacts) must have sources with interests. Nothing found in a
  cave by luck.
- Sects are institutions: budgets, factions, obligations, people who are bad at their jobs.
- The elder who exists to be impressed by the MC does not exist here.

## Handoff to the world

A power system that has not changed how ordinary people live is a game mechanic, not a world.

**Nobody understands the whole system.** Practitioners know their own technique, their school's
account of it, and a great deal of folklore they cannot distinguish from the first two. The
scholar's model and the street's model disagree, and both are partly wrong — that disagreement is
free plot, and it is what stops the power system from being narrated by whoever is standing there
(`competence-map` §1–§3). Where the system contains genuine gods, immortals or thousand-year
cultivators, they are declared `knowledge_scope: broad` with a shape *and* a boundary, and their
**access** is what gets limited — the patriarch is sealed, asleep, or answers once a decade —
because an unbounded oracle dissolves every mystery in the book (`competence-map/references/broad-knowledge.md`).

As soon as the rules here are stable, run **`social-fabric`** and propagate each hard rule down to
institution, market and household — who monopolised it, what job it created, what an ordinary
family does differently, what craft it made obsolete, and what people do in the gap where it does
not work. That gap is where most plots live. `world-texture` then decides how any of it reaches
the page: a rule biting someone, never a lecture.

## Self-check

- [ ] Every hard rule has been propagated through `social-fabric` §2
- [ ] Practitioners' knowledge of the system is bounded — nobody explains the whole cosmology
- [ ] Any god, immortal or long-lived cultivator has a declared shape *and* boundary, and their
      access is bounded rather than their knowledge (`competence-map/references/broad-knowledge.md`)
- [ ] Cost, limits, learning curve and counter all written down
- [ ] Every ability used this chapter paid its stated cost, on the page
- [ ] Nothing was resolved by a capability the reader had not seen used and seen fail
- [ ] Any permanent gain is a row in `state/power.md` §4 — +1 tier, with a source, a price paid
      first, a setup, and a new problem attached (`power-scaling` §3)
- [ ] No rank recital, no mechanics explained mid-action
- [ ] A weaker character could still, in principle, win — name how
- [ ] The MC's position on `state/power.md` §2's ladder is what the page shows it to be
