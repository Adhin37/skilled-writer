---
name: competence-map
description: Keep every character's knowledge bounded and specialised - what they know, where the edge is, who they ask. Use when designing a character, when anyone states a fact, and inside revision-pass.
owns: [competence-grid, provenance-test, acquisition-ladder]
---

# competence-map

The default AI character is a **generalist with no edges**. Ask them about metallurgy, they answer.
Ask about canon law, court etiquette, field medicine, the price of grain — they answer, at the same
confident depth, in the same paragraph. Nobody says *I don't know*. Nobody says *ask Dael, that's
his end*. Nobody is wrong about a thing they were never taught.

Real people are narrow. Someone spends a decade getting good at one thing, is passable at three
adjacent ones, and is a tourist everywhere else — and that narrowness is where scenes come from,
because it forces them to ask, to trust, to guess, and to be wrong.

This skill draws the edges and enforces them. It also governs the other half: **skills are
acquired, slowly, through failure** (§5). And it carries one deliberate exception, because a
setting with gods, immortals or an ASI in it needs different handling (§6).

**Scope.** This skill owns *domain expertise* — what a character has learned to do and to know.
Plot facts are somebody else's job: what a character has been told or has witnessed lives in the
CCS `kno>` line (`continuity-summary`), and how fast news travels lives in `bible/society.md`
(`social-fabric`). `mc-intel-meter` owns how fast they think. Those are four different things and
conflating them produces the protagonist who is a genius, therefore knows everything, therefore
has nothing to find out.

---

## Sections that live in `references/`

Section numbers are stable — other skills cite them — so the gaps below are deliberate. Open one
when its trigger fires, not by default.

| § | file | open it when |
|---|---|---|
| 5 | `references/acquisition-ladder.md` | somebody is learning something across chapters, or a skill has advanced and you need to know what that cost |
| 6 | `references/broad-knowledge.md` | the character is a god, an immortal, a cultivator with centuries, or an artificial mind — `knowledge_scope: broad` |

The revision-time check is `references/audit-card.md`, opened by `revision-pass` Pass 3.

## 1. The knowledge map

Every tier-A and tier-B character has a competence table in their profile, and a row in the
cast-wide grid at `bible/cast/_competence.md`. Three columns, and the third is the one that does
the work:

| domain | level | **where the edge is** |
|---|---|---|
| smithing | exceptional | knows steel, fuel and his own supplier; knows nothing of where the ore comes from or who controls it |
| letters | passable | reads a contract slowly, writes badly, cannot read the court hand at all |
| the city | professional | the four streets around the forge; lost past the river |

Levels are the existing five: `none` `passable` `professional` `exceptional` `best alive`.

### The four rules

**1. Unlisted is `none`, not "probably fine".** This is the rule the whole skill rests on. The
model's instinct is to treat an unlisted domain as adequate, because adequacy keeps the scene
moving. It is `none`. If a scene needs the character to know something not on their map, either
they do not know it — which is the scene — or they learned it on the page and it goes on the map.

**2. The budget above `professional`.** Deep expertise is rare and expensive:

| tier | domains above `professional` |
|---|---|
| MC | at most 3, and one of them is the golden finger's domain if there is one |
| other tier A | at most 2 |
| tier B | at most 1 |
| tier C | 1, and it is their job. It is also the only thing they know |

Anything above `professional` is paid for with a scene showing how it was acquired — already the
rule in `character-profile`, and this is the budget it operates under.

**3. Two incompetences is a floor, not a target.** Every character has far more `none` than
anything else. The interesting incompetences are the ones *adjacent* to their expertise, because
those are the ones the reader assumes they have: the surgeon who cannot set a bone, the spy who
cannot lie to someone who knows them, the general who has never handled money.

**4. Breadth costs depth.** A character with five `professional` domains has spent a life doing
that instead of getting excellent at one. That is a legitimate build — the generalist, the
fixer — but it is a *choice with a cost*, and the cost is that they lose to a specialist inside
the specialist's domain, on the page, at least once.

---

## 2. The four kinds of not-knowing

"They don't know" is a wall. These are doors — pick one, because each generates different action.

| kind | what it looks like | what it produces |
|---|---|---|
| **ignorant** | does not know the word, cannot form the question | someone must explain, or they proceed blind |
| **wrong** | a confident, outdated or folk model | **the most useful.** They act, competently, on a false premise |
| **shallow** | knows the surface, the jargon, the headline; fails the second question | exposed by anyone who actually knows |
| **rusty** | knew it once — another era, another job, another body | half-right, and the half that is wrong is dangerous |

Worked, on the same fact — *the fever in the low quarter is spreading through the water*:

- **ignorant** — "Fever's fever. You get it or you don't." Boils nothing. Drinks.
- **wrong** — "It's the air off the flats." Seals the windows, which does nothing, and keeps
  drawing from the same well. Confident, methodical, and doomed.
- **shallow** — "Water, yes, everyone knows that now." Boils the drinking water and washes the
  cups in the cistern.
- **rusty** — "We had this in the siege. Lime in the wells." Correct for a different disease.

**Prefer wrong to ignorant.** A character who does not know does nothing; a character who is wrong
does something, and the story is made of what people do.

## 3. The provenance test

**For every fact a character states on the page, name how they know it.** One of five:

they were taught it · they did it · someone told them · they read it · they are guessing

If you cannot name one, they cannot say the line. This is the knowledge counterpart to
`mc-intel-meter`'s trace test, and it catches the most common version of the defect: a character
producing the correct technical answer because the *author* knows it.

**Foreknowledge is a sixth provenance, and it is bounded like any other.** *They remember it from
before* is a legal answer only when `mc.foreknowledge` is set, only at the declared
`foreknowledge_grain`, and only for an item on the `state/foreknowledge.md` inventory. It is a
declared domain on the competence grid with an edge like every other domain, and the same rule
applies: **an unlisted item is `none`, not "probably fine."** An MC whose grain is `impressions`
cannot produce a date; one whose grain is `fandom-corrupted` cannot tell what they read from what
someone told them about it, and saying so on the page is a strength. `meta-knowledge` owns the
mechanic, its decay, and what a spend costs.

Note what foreknowledge is *not* provenance for: **a skill.** Remembering that a technique exists
is not being able to perform it, and the acquisition ladder in §5 runs at its normal speed for a
reincarnator. This is the commonest way foreknowledge is smuggled into competence it never earned.

Two corollaries:

- **Guessing is legal and should be visible.** A character who says "I'd assume it's a debt, but
  that's a guess" is more competent-seeming, not less — and it puts a flag on the page for the
  reader to remember when it turns out wrong.
- **Nobody explains a domain they do not have.** `dialogue-voice` already forbids two people who
  both know a thing explaining it to each other; this is the other half. Exposition assigned to a
  convenient mouth is how the whole cast ends up omniscient.

## 4. Specialisation implies a network

A specialist's most useful knowledge is often **who to ask**. Record one referral per tier-A and
tier-B character: *when it is outside their domain, who do they go to, and what does that cost
them?* The cost matters — a favour owed, a fee, an admission of ignorance to someone who will
remember it.

This is where the skill pays for itself:

- It generates cast (`character-profile`) and gives walk-ons a reason to exist.
- It produces plot, because the person you must ask is a person with their own wants.
- It ties to `social-fabric`, which owns who is *allowed* to learn, what costs money to know, and
  what a low literacy rate does to the list of people who could have read a given document.

**Delegation is competence, not weakness.** A character who knows the boundary of their own
expertise and hands the problem to the right person reads as more capable, not less. Write that
instead of having them improvise a second specialty.

**The cast-wide gap is an asset.** Keep a short list in `_competence.md` of what **nobody** in the
current cast knows. That list is a plot generator and a guard against the moment when a chapter
needs a physician and one is quietly invented.

## 7. Where this runs

```bash
python3 scripts/sw.py cast novels/<slug>
```

Settles the countable half: the deep-expertise budget per tier, anyone on the voice matrix with
no competence row, anyone missing a referral, and the domain-count distribution.

The distribution is printed and **not** judged. Whether the thin rows sort by gender, class or
people is the §7 question, it is the one that matters, and it is not scriptable — the command
prints the counts and then says to open `bias-guard` and make the call.


| moment | what happens |
|---|---|
| `character-profile`, tier A/B | competence table with edges, the referral, the above-`professional` budget. Row into `_competence.md` |
| `character-profile`, tier C | their third stroke *is* their domain, and it is the only one. A walk-on knows their job and not the thing next to it |
| `mc-design` | the MC's 3-domain budget; what their advantage does and does not install; and — for parallel minds, clones or accelerated thought — that those grant *throughput*, not breadth. A mind that can do six things at once still had to learn all six |
| `novel-init` | the starting map, filled as a grid, plus the cast-wide gap list |
| `chapter-plan` | if an arc turns on an expertise nobody has, that is a character to introduce or a skill to start climbing, and it is planned, not improvised at the scene |
| `write-chapter` step 1 | who needs to know what this chapter, and who has to ask |
| `write-chapter` step 2 | the provenance test on every stated fact; the referral instead of an invented second specialty |
| `revision-pass` Pass 3 | provenance sweep, the unlisted-is-`none` check, skill-ladder honesty |
| `continuity-summary` write | a stage advance is logged in `state/growth.md`; a genuinely new domain goes on the map |

**`bias-guard` outranks this skill**, and owns the sweep: read the `none` and `passable` rows of
`_competence.md` as a block and check the pattern against it. The fix is never to make everyone
equally able — it is to make sure the *pattern* is not the book's argument. And a character
learning a skill from stage 0
must be learning it because of who they are and what their life allowed, never because their
category is expected to be bad at it.

## Self-check

- [ ] Every fact stated on the page passes the provenance test — taught, did, told, read, guessing,
      or remembered-from-before at its declared grain
- [ ] No character answered inside a domain their map does not list
- [ ] Nobody exceeded the above-`professional` budget for their tier
- [ ] At least one character said they did not know, or asked someone, or was visibly wrong
- [ ] Any not-knowing is one of the four kinds, and `wrong` was preferred to `ignorant`
- [ ] Nobody improvised a second specialty where a referral was available
- [ ] Any skill advance used a teacher, a reference or a costly failure — never elapsed time
- [ ] Practice this chapter cost something; a stage transition got a scene, practice got a clause
- [ ] Broad-knowledge characters have a declared shape **and** a boundary, and their access is
      bounded rather than their knowledge
- [ ] The `none` rows of the cast map do not sort by gender, class or people
