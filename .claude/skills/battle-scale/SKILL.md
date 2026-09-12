---
name: battle-scale
description: Optional (default off). Write engagements larger than a fight - fronts, attrition, supply, command - through a viewpoint that cannot see the field. Use only while this skill is enabled.
metadata:
  type: skill
  tier: optional
  when: optional.battle-scale == on
  owns: [mass-combat, attrition, command-legibility]
---

# battle-scale

**Gate.** Applies only if `novel.md` → `optional.battle-scale` is `on`, **and** the chapter
contains an engagement bigger than a fight between people who can all see each other.

A battle is not a long duel. `combat-choreography` owns the duel — where two bodies are, what the
terrain does, how the exchange turns — and every one of its tools stops working at scale, because
its central promise is that the reader always knows where everybody is. In a battle **nobody
knows where everybody is**, including the people in command, and pretending otherwise produces
the map-with-arrows prose readers skim in paragraphs.

The problem this skill solves: an engagement the viewpoint character cannot see, written so a
reader can follow it, care about it, and be surprised by it.

---

## What lives in `references/`

| file | open it when |
|---|---|
| `references/logistics.md` | the campaign around the battle — supply, movement, disease, money, and why armies actually lose |
| `references/draft-card.md` | never, by you. `write-chapter` Phase A opens it |
| `references/audit-card.md` | never, by you. `revision-pass` Pass 4 opens it |

## 1. The one decision: what is the reader tracking?

Pick **one** and hold it for the whole engagement. Mixing them is what makes battle prose feel
like a summary of somebody else's game.

| frame | the reader follows | good for | costs you |
|---|---|---|---|
| **The body** | one person's hundred metres | terror, chaos, the cost | the reader never learns who won until somebody tells them |
| **The decision** | a commander's choices, from inside their bad information | tension, competence, blame | distance — the killing is abstract |
| **The line** | one unit's job, and whether it holds | both, in a narrow band | needs the unit established beforehand |

The first is the default and the most reliable. The second is the strongest when the commander is
a POV character whose orders will be wrong. The third needs a chapter of setup and repays it.

**Whatever the frame, the outcome reaches the reader the way it reaches the character**: late,
partial, and from somebody who might be wrong.

## 2. Command legibility

The reader must be able to answer three questions at any moment. Not *where is everyone* — that
is the thing nobody knows.

1. **What is this person trying to do?** One objective, stated in plain words. Hold the ford.
   Get the wounded out. Find out whether the left has broken.
2. **What would losing look like?** Concretely, for them. Not "defeat" — the ford lost means the
   road open means the town.
3. **How would they know?** Name the channel: a runner, a horn, the noise changing, somebody
   arriving who should not be there. **Information is the resource battles are fought with**, and
   a commander who simply knows things has been handed omniscience (`competence-map`).

Everything else — numbers, dispositions, the names of formations — is optional and mostly
harmful. A reader does not need to know the order of battle. They need to know what this person
is trying to do and how badly it is going.

## 3. Scale is conveyed by sense, not by number

*Twelve thousand men* is a number the reader files and forgets. Scale arrives through:

- **Time.** It takes an hour for an order to reach the far end and come back wrong.
- **Sound.** The thing everyone who has been in one remembers, and the reason nobody hears orders.
- **Logistics as texture.** What people are eating. What they are doing with the dead. Where the
  water is coming from.
- **The parts you cannot see.** A wing you have only heard about is more frightening than one
  described.
- **Repetition and boredom.** Most of a battle is waiting, and the waiting is where the character
  work goes.

Do **not** open on an establishing paragraph of dispositions. That is the rank recital in
uniform (`mtl-detox`), and it is where readers leave.

## 4. Attrition

The rule that separates a battle from a fight: **the loss is statistical, and it becomes a story
by being specific.**

- Casualties are decided before drafting — roughly, as a fraction — and then **one of them has a
  name the reader knows.** The fraction is why the battle matters; the name is why the reader
  feels it.
- Units degrade rather than dying. A company at half strength does not fight at half strength; it
  fights worse than that, and then it breaks.
- **Almost nobody dies fighting.** They die when the line breaks and they run, in the pursuit,
  and afterwards of their wounds. A story where the dying happens face-to-face is telling the
  reader that battles are duels.
- The survivors are not the brave ones. They are the lucky ones, and some of them know it.

## 5. What decides it

Battles are decided by cohesion, not by casualties. A unit routs long before it is destroyed,
and the question in every engagement is **which side stops being an organisation first.**

Legitimate deciders, roughly in order of how often they are the real one:

supply and the state people arrived in · surprise and where · terrain, which is the same as in a
duel but decides more · a flank or a rear · reserves committed at the right moment · somebody
important visibly falling · weather · the individual heroics the genre loves, which change an
outcome only where they change **cohesion** — the line holds because somebody was seen.

That last clause is how an exceptional character matters in a battle without the battle becoming
a duel with extras. `power-scaling` still binds: an MC who can personally decide a field is a
scaling problem, and the fix is to make the field bigger, not the reader more impressed.

## 6. Afterwards

The aftermath is not optional and it is where the chapter's delivery usually lives.

Who is counting. Who is being buried, by whom, and how badly. What the wounded are being given.
What the winner now has to garrison. Who profits. What the news says by the time it has travelled
three towns, and how wrong it is by then — `social-fabric` owns information speed, and a plan may not
violate it.

**The battle that changes nothing should not have been written**, and at this scale "changes
nothing" includes changing only who is stronger. A battle changes a map, a treasury, a
generation, or somebody's standing — `conflict-engine` owns what the chapter had to cost.

## Self-check

- [ ] One frame chosen and held for the whole engagement
- [ ] The reader can state the POV character's objective, what losing looks like, and how they
      would find out
- [ ] Nobody had information they had no channel for
- [ ] No establishing paragraph of dispositions, and no numbers doing work that sense should do
- [ ] Attrition decided beforehand, and one of the casualties is somebody the reader knows
- [ ] The engagement turned on cohesion, not on a body count
- [ ] Any individual heroics changed the outcome through other people, not instead of them
- [ ] The aftermath is on the page: the dead, the wounded, the cost of holding it
- [ ] Something outside the battle is different afterwards
