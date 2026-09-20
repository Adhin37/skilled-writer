---
type: reference
owner: scene-craft
description: scenes where the turn is a concession - the reserve, the currency, the walk-away, and how ground actually gets given on the page
---

# scene-craft — negotiation, and scenes where somebody has to give ground

Open this when the turn of the scene is **who concedes what**: a bargain, a hearing, a truce, a
council meeting, a hostage exchange, an interrogation where both sides hold something.

The failure has two halves and they are opposites. Either the scene is a **debate** — both parties
state a position and then restate it with more force, nothing is exchanged, and it ends when the
author runs out of arguments — or it is a **capitulation**, where one side was simply right and
the other folds, which is an announcement with a delay in front of it.

Both come from the same missing decision: nobody worked out what either side would actually take.

---

## Before drafting: four numbers per side

Write these down for **both** parties. They are the whole preparation, and a scene with them is
very hard to write badly.

| | the question | the scene fails when |
|---|---|---|
| **the ask** | what they say they want, out loud, first | both sides' answer is "to win" |
| **the reserve** | what they will actually settle for — never the ask, never stated aloud | nobody has one, so no concession is available and the scene can only be a debate |
| **the currency** | what they hold that the other side genuinely values | the only thing on offer is agreement itself |
| **the walk-away** | what happens to them if there is no deal | both sides can walk comfortably, so neither of them needs this room |

**The walk-away is the leverage**, and writing it down is what stops leverage being a personality
trait. Nobody is powerful in a negotiation; somebody can simply survive no-deal longer than the
other, and every hard line in the scene is priced off that asymmetry. When the weaker party wins
anyway, it is because they changed what the other's walk-away costs — not because they argued
better.

The gap between the ask and the reserve is the room the scene has to move in. If either gap is
zero, cut the scene or change the numbers.

## The turn

The unit is unchanged — goal, obstacle, turn, exit, and never a plain yes. What is specific here
is **what the turn is made of**:

> Somebody discovers that the other side's reserve or walk-away is not what they assumed.

Three shapes, in rough order of how often they earn their place:

- **A currency nobody knew was on the table.** One side wants something the other did not know
  they had, and would have given cheaply an hour ago.
- **A walk-away that was a bluff — or that turns out to be real.** The second is stronger and
  rarer: the party everyone assumed was desperate can genuinely leave.
- **A third want intruding.** Somebody in the room has their own business and it will not wait.
  At three or more speakers this becomes the dominant shape, and `roles/design/scene-craft.group-scenes.md`
  owns it.

## How the exit reads

The four legal exit states are in `SKILL.md` and nothing here replaces them. What each one looks
like across a table:

| exit | in a negotiation |
|---|---|
| **Yes, but** | the deal closes at a price that creates the next problem. The workhorse |
| **No, and** | no deal, and the relationship is now worse than before they sat down |
| **No, but** | no deal on the ask, but something smaller was agreed, or somebody learned what the other actually wants |
| **Yes, and** | both sides do better than they came for. Rarer here than anywhere, because a negotiation is the one scene type where the reader is counting |

The strongest variant of *Yes, but* in a serial is **the deal both sides know will not hold.**
Everybody signs, nobody believes it, and the scene exits on a shared, unstated understanding that
this is temporary — closing the scene and opening a thread in the same beat (`plot-threads`).

## On the page

**A concession is an action, not a sentence.** People almost never say *I accept*. They sit down.
They put the thing on the table. They stop using the title they had been using. They offer tea.
Somebody's second stops writing. The reader reads the change in posture before they read the
terms, and it is more convincing than either party explaining their reasoning.

**Keep one concrete thing on the table** — a document, a number, a key, a name written down. The
whole scene routes through it, everybody can look at it, and it saves the reader from holding an
abstraction while also holding four titles. This is the fix in `SKILL.md`'s Political row, and it
is doing more work than it looks like.

**Nobody argues in their best form.** People in a room with something to lose repeat themselves,
go at the weakest point rather than the real one, and answer a question from four exchanges ago.
The cadence and the interruptions are `dialogue-voice`'s, and the subtext — what is meant and not
said — is owned there too.

**Procedure is a weapon.** Who sets the agenda, who speaks last, who may be kept waiting, what the
room's rules actually are. This is where the society layer pays out in a scene rather than in
description: `social-fabric` owns the institutions, and a negotiation is the cheapest place to
show that they bite.

## Where this is not the right file

| what you are actually writing | whose rule it is |
|---|---|
| the plan behind the ask, what is withheld from the reader, and lying in the room | `roles/draft/mc-intel-meter.plans-and-lies.md` |
| who at the table can read whom, and the misread | `social-perception` |
| three or more speakers, blocking, turn allocation | `roles/design/scene-craft.group-scenes.md` |
| what the court, guild or council *is* | `social-fabric` |
| whether this beat deserves a scene at all | `story-craft` |
| what the deal cost, and who pays it later | `conflict-engine` |

## Anti-patterns

| pattern | why it fails | instead |
|---|---|---|
| The villain explains their leverage | the scene stops so somebody can narrate the stakes | let them use it once, small, and let the other side price it |
| Both sides fully informed | with nothing to discover there is no turn, only arithmetic | each side is wrong about exactly one of the other's four numbers |
| The clever line that wins it | a negotiation decided by phrasing teaches the reader nothing has weight | the line only lands because the walk-away shifted underneath it |
| Terms the reader cannot price | a concession means nothing if nobody knows what the thing is worth | one anchor price on the page first (`roles/shared/social-fabric.prices-and-stakes.md`) |
| The deal that ends the problem | closes a thread and opens nothing | somebody has to go home and deliver these terms to people who were not in the room |
| Negotiating with someone who has no choice | that is a demand, and it is a shorter scene | give the weaker party one real currency, however small |
