---
type: reference
owner: timeline-engine
description: a faction or canon power is about to react to the MC, or escalation is running hotter than the reader can carry
---

# timeline-engine — reaction profiles and the difficulty governor

Open this when a faction or canon power is about to react to the MC, or when escalation is running hotter than the reader can carry.

---

## Reaction profiles

Every driver on the world track gets a profile. This is what makes the world feel run by people
rather than by a schedule.

| profile | how it reacts | latency | fidelity | archetype |
|---|---|---|---|---|
| **Strategist** | Patient. Gathers information before moving. Revises the plan correctly. Treats the MC as a variable to be used first, removed second. | slow (4–10 ch) | high — reads the MC's actions accurately | the informed, charismatic long-game villain: e.g. All For One in *My Hero Academia* |
| **Chaotic** | Fast, disproportionate, personal. May fixate on the MC for a reason that isn't strategic. Cannot be negotiated with reliably. Escalates when frustrated. | fast (1–3 ch) | low — often wrong about what the MC did, which is its own danger | the volatile heir with something to prove: e.g. Shigaraki |
| **Institution** | Procedural, slow, and it never forgets. Opens a file. Responds with policy, not violence. | very slow (10+ ch) | high but rigid — reads the record, not the person | a hero commission, a guild, a state |
| **Rival** | Matches the MC's growth curve (`state/power.md` §1). Reacts to being surpassed. | medium (2–5 ch) | high in their shared domain, blind outside it | the peer who was supposed to be first |
| **Indifferent** | Does not react at all. A plague, a market, a season, a prophecy already in motion. | n/a | n/a | the pressure that doesn't care who you are |

**A world needs at least two profiles in play, and one of them should be Indifferent.** A world
where everything is a reaction to the MC is as unreal as one where nothing is.

**Latency is a design tool, not a delay.** The gap between the MC's action and the world's answer
is where dread lives, and it is where the MC gets to prepare. A strategist who responds instantly
is just a chaotic with better manners.

**Fidelity generates plot.** A driver that misreads what the MC did produces the best material in
this whole system: the MC is punished for something they didn't do, or credited with something
they didn't intend, and now has to decide whether to correct the record.

---

## The governor — why this is not nightmare mode

The user's story ends well. That is a constraint on the engine, not a hope. Six mechanical rules,
all scaled by the dial:

1. **Proportional response.** Opposition allocates attention by threat rank. The MC is rarely rank
   one early, and the strongest driver on the board does not turn its full attention on them
   simply because it could. Record who the driver's *actual* priority is; usually it is not the MC.

2. **Latency is protection.** At dial 3, minimum reaction latency is 2 chapters. The MC always
   gets room to see it coming and prepare. Instant retaliation is a dial-5 event and is spent, not
   habitual.

3. **Crisis cap.** Simultaneous unresolved crises may not exceed the dial number, hard-capped at
   **3**. Before adding a fourth, resolve one — even partially, even badly. Compounding disaster
   past three reads as authorial punishment and readers disengage.

4. **The reciprocity rule.** Every escalation also opens something: an ally who steps forward, an
   intelligence leak, an enemy's mistake, a resource that was not available before. Ratio 1:1,
   logged in the ledger. This is the difference between *hard* and *hopeless*.

5. **Wins stick.** A threat the MC defeats stays defeated for at least one arc. No retroactive
   rescue of the opposition, no "it was a body double" — that is `grimdark-consequences`'
   no-retroactive-rescue rule pointed the other way.

6. **The recovery beat.** In the chapter after a major world escalation lands, the MC keeps
   something: a relationship, a place, a small competence. `slice-of-life-texture` does this well
   if enabled; a single grounded paragraph does it otherwise.

Escalation ceiling per arc is `timeline.escalation_ceiling` (default: one stake-rung per arc, per
`conflict-engine`'s ladder). The world escalates by one rung, not three.

---
