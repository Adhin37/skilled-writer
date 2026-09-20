---
type: reference
owner: world-texture
description: the world is present but nothing happens in it - the atmosphere failure, what it is measured to be, and the repair
provenance: docs/craft-sources.md §The second pass
---

# world-texture — narrative space, or why the world reads as weather

Open this when the world is **vivid and inert**: the prose is full of light, smell, mood and
heat, the description budget is not being broken, and the place still does not feel like somewhere
a person could get anything done. That is a distinct failure from flat and from bloated, and it is
the one a machine drafter reaches for by default.

## The five kinds of space

A sentence that carries any spatial information carries it in one of five modes. The scheme is
phenomenological — space as *lived* rather than as measured — and the examples are the source's.

| space | what it is | example |
|---|---|---|
| **action** | space the character moves through and acts on; objects enable or obstruct a goal, and possession of the place is taken by hand and foot | *"He jumped up, jerked the window-shade, and dragged his chair closer to examine the shoes"* |
| **perceived** | space sensed and *felt*; diffuse sensation with no direction and no goal — weather, light, smell, mood — and the setting sometimes acting on the character like a creature | *"The terror of loneliness among those overhanging mountains gripped at the boy's throat"* |
| **visual** | space looked at from a standstill; detached, observational, the character unaffected | *"He glanced from Tom to the cabin"* |
| **descriptive** | spatial information tied to nobody's agency; neutral scene-setting | *"On either side of the towpath were farms and gardens"* |
| **none** | no spatial relation, or a place only imagined, remembered or planned | — |

Where two co-occur, the dominant one wins. Visual and perceived differ by whether the character is
merely looking or is being *absorbed*; visual and descriptive differ by whether anyone is doing the
observing.

## What was measured

Four models against human fiction, in English and German, a thousand stories each.

- **Human writing runs on action space.** Machine writing overproduces **perceived** space.
- **Openings, first fifteen sentences:** perceived space at **0.47** for the strongest offender,
  against a human **0.19**. All four models exceeded the human figure.
- **Whole chapters:** human corpus mean **0.083**; models **0.17 to 0.33**. Even at their lowest
  point within a chapter, all four produced **two to three times** the human amount.
- **Action space** falls away across the story for most models, while in human writing it drifts
  slightly *up*.
- **Descriptive space is the mode models match most closely.** The category we already budget is
  the one that was never the problem.
- The skew is present from chapter one, holds across the whole story, and **peaks at every chapter
  boundary** — which for this toolkit is every chapter, because a chapter is drafted in a fresh
  session.

One diagnosis of a machine-written opening: it *"arrests movement from the second sentence
onward"*, producing a world **felt before it is actively inhabited**.

The study measures a divergence from human writing. It deliberately does **not** claim readers
enjoy it less — one cited study found readers rated machine stories *more* absorbing. So this is a
craft default, not a gate, and nothing here scores a chapter.

## Why this toolkit was already right and still exposed

`CLAUDE.md` rule 3 says the world is **delivered, not described** — as a consequence, a friction or
an assumed reference. That *is* action space, in our own vocabulary, and §1's channel ladder is
the right instrument.

The exposure is in the enforcement. The ≤8% cap and the three-consecutive-sentence rule both count
**direct description** — descriptive and visual space — and a mood sentence is neither. Atmosphere
arrives as interiority, which `narrator-voice` makes the default carrier and rightly so, so it
passes every count this skill owns. A chapter can sit at 4% description, hit its sensory quota,
anchor every location, and still be entirely weather.

Two of our own defaults point the same way and are not wrong, only unbalanced: *2–4 sensory
details per scene, at least one non-visual* is satisfied by smell and sound, which are the easiest
things to sense without touching; and a location's **sensory signature** is by construction a
perception. Neither needs changing. What they need is a third thing beside them.

## The repair

**The handled-noun test.** Name the noun this scene's POV character's hands or feet dealt with.
Not looked at, not smelled, not felt the mood of — picked up, pushed past, climbed, jammed, paid
for, put down. If a scene has no such noun, its world was felt and not inhabited.

The repair is never more description, and it is not less atmosphere either. It is giving the same
detail something to be in the way of.

```
perceived   The forge-quarter smelled of hot iron, and the heat pressed against her
            face like a held breath.
action      She turned her shoulder to get past the quench-barrel, and the heat came
            off it hard enough that she took the long side of the aisle.
```

Both carry the heat. The second one also says the aisle is narrow, that she has been here before,
and that the barrel is where it always is.

**Three places to spend it, cheapest first.** An object that resists — a door that sticks, a latch
sized for someone taller. A route chosen because of the place — going round, going under, waiting.
A thing put down or picked up, which is how a reader learns what a person is carrying.

**And openings buy the most**, because that is where the skew is largest. A chapter that opens on
somebody handling something has spent its most expensive sentences on the mode the page is worst
at by default. This is also the cheapest possible version of `hook-and-pacing`'s ban on opening on
setting: the fix is not a different subject, it is the same place with a verb in it.
