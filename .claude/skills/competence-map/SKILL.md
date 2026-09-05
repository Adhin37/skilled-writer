---
name: competence-map
description: Keep every character's knowledge bounded and specialised — what they know, how deep, where the edge is, who they ask when it runs out, and how a new skill is actually acquired over chapters of failure. Use when designing any character, whenever anyone states a fact or attempts a skill on the page, and inside revision-pass. Includes the broad-knowledge clause for gods, immortals, cultivators and artificial superintelligences.
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
- It ties to `social-fabric`: who is *allowed* to learn, what costs money to know, what is guild
  secret, what is only spoken. In a world with 8% literacy, the number of people who could have
  read that ledger is a plot constraint, not a background detail.

**Delegation is competence, not weakness.** A character who knows the boundary of their own
expertise and hands the problem to the right person reads as more capable, not less. Write that
instead of having them improvise a second specialty.

**The cast-wide gap is an asset.** Keep a short list in `_competence.md` of what **nobody** in the
current cast knows. That list is a plot generator and a guard against the moment when a chapter
needs a physician and one is quietly invented.

## 5. Learning — the acquisition ladder

Characters do acquire skills, and not only the MC. The failure here is the opposite of §1: the
montage, in which somebody is bad at a thing on Tuesday and good at it on Friday.

| stage | what it looks like on the page |
|---|---|
| **0 — can't** | does not know what they do not know. The failure surprises them |
| **1 — fails knowingly** | knows what should happen and cannot make it happen. They can now *see* the gap, which is itself progress and should be written as progress |
| **2 — unreliable** | works sometimes, and they cannot tell in advance which times |
| **3 — competent** | works, slowly, with their whole attention |
| **4 — fluent** | works while they are thinking about something else |

Stage 2 → 3 is where stories cheat, and it is the longest stretch in life. Stage 4 is rare; most
characters stop at 3 in most things, and that is correct.

**The three legal sources.** A stage advance comes from a teacher, a reference, or a failure that
cost something. Never from time passing.

**The montage rule.** A serial cannot spend twenty chapters on cooking. So: **stage transitions get
a scene; the practice between them gets a clause.** The learning happens in the margins of chapters
about something else — one line of a burnt pan, a hand that has stopped shaking — and only the
transition earns page time. That is also what makes the transition land.

**Practice is a cost.** Time spent learning is time not spent on the thing the chapter is about,
and `conflict-engine` applies: name what the practice took. A character who acquires a skill for
free has acquired nothing the reader will value.

**The plateau.** Somewhere around stage 2, more repetition stops working and something else has to
change — a different teacher, an admission, a piece of equipment, a reason. Use it; it is the most
truthful thing about learning anything and it makes an excellent mid-arc beat.

Worked, five chapters apart, in the margins of five chapters about something else: *she cannot
cook* → *she can tell the bread is wrong before she cuts it, which is new* → *the third loaf in a
row is edible and she does not know why this one worked* → *she makes the thing her mother made,
slowly, and gets it right* → *she makes it while arguing about something that matters, without
looking.* Five clauses, one scene at the fourth.

**Record it.** Skill ladders live in the skill section of `state/growth.md`, beside the belief
ladders — they are a different axis and both can be in motion. A character at belief rung 2 can be
at cooking stage 3.

**Golden fingers that grant skill.** If the MC's advantage installs competence directly
(`mc-design`), this ladder is where its **cost** goes: what the skill did not come with — judgement,
context, the calluses, knowing which of two right answers this situation wants. A hand that has
never burnt itself does not know when the pan is too hot. Otherwise the advantage deletes the
character's capacity to learn anything, which is most of what a serial is made of.

## 6. The broad-knowledge clause — gods, immortals, cultivators, ASI

Some settings contain minds that genuinely do know enormously more than a person, and §1 must not
flatten them into a blacksmith with a long memory. Declare it in the profile:

```yaml
knowledge_scope: broad      # narrow (default) | broad
scope_kind: domain-god      # domain-god | long-lived | artificial | borrowed
scope_shape: ""             # what is actually broad, in one sentence
scope_boundary: ""          # what still bites, in one sentence — required
```

**Even omniscience has a shape, and the shape is the character.**

| kind | what is genuinely broad | the boundary that still bites |
|---|---|---|
| **domain god** — of wisdom, war, the harvest, the sea | everything inside the domain, natively, without having learned it | outside it they are *worse* than a mortal, because they have never had to acquire anything and do not know how ignorance feels. A god of wisdom is not a god of people |
| **long-lived** — immortal, cultivator, elf, revenant | breadth accumulated across centuries | it is **era-locked**: they know the world of four hundred years ago in extraordinary detail and this one badly. They have also forgotten more than they kept, and they mistake the forgotten for the unimportant |
| **artificial** — ASI, oracle, system core | recall and inference at a scale no person matches | trained on what someone fed it. No embodied knowledge — it has never lifted anything. It interpolates confidently across its blank regions, and cannot tell those regions from the rest |
| **borrowed** — a system, a library, a bound spirit | access, not knowledge | it must be *queried*: that takes time, costs something, and returns what was asked rather than what was needed. The character's real skill is knowing what to ask |

### The three rules that still apply

1. **Breadth is not depth is not applicability.** Knowing everything recorded about metallurgy is
   not knowing which of these two smiths is lying to you. The gap between knowledge and judgement
   is where these characters are written.
2. **Bound the access, not the knowledge.** An unbounded oracle is a plot solvent — every mystery
   dies at its feet. So the god answers three questions a year; the immortal is asleep, or bored,
   or forbidden to intervene; the ASI is airgapped and speaks through a bad channel; the system
   charges. This is a `power-system` / `tech-plausibility` limit and it goes in that file too.
3. **They are still wrong about people.** `mc-intel-meter`'s tier-5 error profile applies with
   more force here: what cannot be modelled — grief, loyalty, spite, being loved — is where a mind
   like this fails, and failing there is the only thing that makes it a character rather than a
   reference work.

**Everyone else in that setting is still narrow.** A world with gods in it is not a world where the
farmers know cosmology. A cultivation sect with an 800-year-old patriarch still has disciples who
cannot read. The clause is per-character and does not leak downward — if anything, a setting with
broad-knowledge beings in it should be *more* stratified, because knowledge is a possession there
and possessions are guarded (`social-fabric`).

## 7. Where this runs

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

**`bias-guard` outranks this skill.** Incompetence assignments must not sort by demographic. Read
the `none` and `passable` rows of `_competence.md` as a block: if the characters who cannot read,
cannot fight, cannot count or cannot cook line up with a gender, a class or a people, the map is
encoding a prejudice and needs redealing. The fix is not to make everyone equally able — it is to
make sure the *pattern* is not the book's argument. And a character learning a skill from stage 0
must be learning it because of who they are and what their life allowed, never because their
category is expected to be bad at it.

## Self-check

- [ ] Every fact stated on the page passes the provenance test — taught, did, told, read, guessing
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
