---
name: timeline-engine
description: Run the world's own plot on its own clock, and make it react to the MC at a dialled intensity — light for most genres, central for fan fiction, where it prevents the "MC changes nothing and canon happens anyway" defect. Includes a difficulty governor so escalation never becomes nightmare mode, and an ending contract the world is not allowed to foreclose. Use when planning arcs, when the MC acts against a faction or canon event, and once per chapter to ask what happened offstage.
---

# timeline-engine

Owns `plan/timeline.md` (what the world is going to do) and the divergence half of
`state/timeline.md` (what it actually did, and why that differs).

The problem it solves has two failure modes, and most stories pick one:

- **Inert world.** The MC acts, and nothing outside the scene changes. In fan fiction this is
  epidemic: a self-insert or a replaced background character does nothing to the plot, canon
  proceeds on rails, and the story is a commentary track.
- **Runaway world.** Everything reacts to everything, the opposition is omniscient and relentless,
  and the story becomes a survival grind the reader stops enjoying.

This skill sits between them, on a dial, and refuses to let the world close the road to the
ending the author declared.

---

## Weight by genre

| genre | how much of this runs |
|---|---|
| original fantasy / scifi | **light.** The world track is the antagonist's plan plus two or three standing clocks. Coarse — what the world does, no fine detail. |
| progression / political | **medium.** Factions move on their own schedules and notice a rising player. |
| **fan fiction** | **heavy.** This is the skill's centre of gravity. The canon track is a real timeline the MC is standing in the middle of. |

Do not build a 200-entry world chronology for a story that needs six lines. The inclusion test
from `story-bible` applies: an entry earns its place only if it will fire on the page or change
what a character does.

---

## The two tracks

**World track** (`plan/timeline.md`) — what would happen with no MC, or with an MC who changed
nothing. For fanfic this is the canon plot, recorded **in your own words** as events and
motivations; never as reproduced text from the source (`fanfic-canon` rule zero).

| id | event | baseline ch | driver | what it needs to succeed | status |
|---|---|---|---|---|---|

`status`: `pending` · `moved` · `prevented` · `altered` · `fired` · `replaced`

**Actual track** — the same events after the MC exists. The gap between the two *is the story's
justification for existing*, and the divergence ledger is where it is recorded.

---

## The reactivity dial

`novel.md` → `timeline.reactivity`, 1–5. Set at `novel-init`. This is the main control.

| dial | name | what the world does | fanfic feel |
|---|---|---|---|
| 1 | **Inert** | Events fire on their baseline chapters. The MC affects only their immediate scene. | Canon on rails. Legitimate only for character-study or slice-of-life fanfic where canon is scenery — say so in the blurb. |
| 2 | **Ripples** | Local and personal changes stick. Major beats still land, roughly on time, sometimes differently. | Canon recognisable; the edges are yours. |
| 3 | **Responsive** | Opposition notices, adapts, and re-plans. Some beats move, one or two are prevented, new ones appear that canon never had. | **Default.** The story is now genuinely alternate. |
| 4 | **Adaptive** | The opposition models the MC specifically, allocates resources against them, and plans around their known capabilities. | The MC is a named factor in other people's strategies. |
| 5 | **Predatory** | The world reorganises around the MC as a primary variable — to recruit, use, or remove. | High tension. Requires the governor below to stay readable. |

Dial 4–5 is **not** nightmare mode. Intensity of reaction and cruelty of outcome are separate
axes; the governor controls the second one.

---

## Reaction profiles

Every driver on the world track gets a profile. This is what makes the world feel run by people
rather than by a schedule.

| profile | how it reacts | latency | fidelity | archetype |
|---|---|---|---|---|
| **Strategist** | Patient. Gathers information before moving. Revises the plan correctly. Treats the MC as a variable to be used first, removed second. | slow (4–10 ch) | high — reads the MC's actions accurately | the informed, charismatic long-game villain: e.g. All For One in *My Hero Academia* |
| **Chaotic** | Fast, disproportionate, personal. May fixate on the MC for a reason that isn't strategic. Cannot be negotiated with reliably. Escalates when frustrated. | fast (1–3 ch) | low — often wrong about what the MC did, which is its own danger | the volatile heir with something to prove: e.g. Shigaraki |
| **Institution** | Procedural, slow, and it never forgets. Opens a file. Responds with policy, not violence. | very slow (10+ ch) | high but rigid — reads the record, not the person | a hero commission, a guild, a state |
| **Rival** | Matches the MC's growth curve. Reacts to being surpassed. | medium (2–5 ch) | high in their shared domain, blind outside it | the peer who was supposed to be first |
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

## The divergence ledger

Lives in `state/timeline.md`. Every MC action that touches the world track gets a row.

| ch | MC action | world-track id | effect | order | who noticed |
|---|---|---|---|---|---|

`effect`: `moved` (earlier/later) · `prevented` · `altered` · `created` (an event canon never had)
· `unchanged` (recorded deliberately, with a reason)

### The impact rule

**Every arc must move at least one world-track event.** Moved, prevented, altered or created —
`unchanged` does not count. If an arc ends and the timeline is identical to baseline, the MC was
a tourist, and the story has no reason to exist alongside its source.

Check this at every arc rollup. It is the single most important test in this skill.

### Canon characters must notice

For fanfic, a corollary: by the end of arc 1, at least one canon character has **changed a
decision** because of the MC. Not been impressed — *changed a decision*. The absence of that is
the tell that the MC is a spectator.

---

## The butterfly budget

Without a budget, changes either stop at the scene (inert) or cascade until the source material is
unrecognisable by chapter 30 and nothing is at stake.

| order | scope | simulate? |
|---|---|---|
| **1st** | The event itself and everyone in the room | yes, on the page |
| **2nd** | People whose plans depended on it; the driver's next move | yes, on the page, within 5 chapters |
| **3rd** | Institutions, factions, public reaction, the world track's later entries | yes, but as **background** — a rumour, a headline, a changed price, a canon event that now fires three chapters late |
| **4th+** | Everything downstream of that | **narrate, do not simulate.** One line at an arc boundary |

`timeline.butterfly_horizon` sets how many arcs ahead a change is allowed to reach. Default 2.

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

## The ending contract

Recorded at `novel-init` in `novel.md` → `ending:`. **In the user's own words** — "happy ending"
means different things and the author's definition is the only one that counts.

```yaml
ending:
  contract: ""        # what a satisfying ending looks like, in the user's words
  tone: hopeful       # hopeful | bittersweet | triumphant | quiet | earned-peace
  non_negotiables: [] # who must survive; what must be true at the end
```

**The point-of-no-return check.** Before firing any world-track event, ask: does this make the
ending contract unreachable? If yes, do not fire it as written. Change its scale, its timing, or
its target. The world may cost the MC enormously; it may not close the road.

This is checked at three moments: when planning an arc, before firing a major world event, and at
every arc rollup. Anything on `ending.non_negotiables` is protected from the timeline engine
absolutely — the world can threaten it, and must never actually take it.

That is not a cheat. Tension comes from the reader's belief that something *could* be lost, and
that belief is sustained by near-misses and by real losses among things not on the list.

---

## Fan fiction mode

### MC footprint archetypes

How much the MC's mere existence perturbs canon from chapter 1. Record in `novel.md` →
`fanfic.footprint`.

| archetype | footprint | the trap |
|---|---|---|
| **Self-insert** | Low at first — an extra person in a world that had a plot. | Ends up narrating canon. Give them a position that *touches* a canon event by chapter 5. |
| **Replaced extra** | Medium — they occupy a minor canon character's slot, so that character's small canon actions are now theirs to take or refuse. | The slot's canon actions get taken identically. The first divergence should be the MC refusing one. |
| **OC in canon** | Medium-high — a person canon did not account for, with their own relationships. | Solving canon characters' problems for them (`fanfic-canon`'s OC test). |
| **Canon character, different choices** | High — the divergence point is theirs. | Drifting to OOC without logging it (`fanfic-canon`'s OOC budget). |
| **Canon character, new circumstance** | High | Canon events firing on schedule despite a changed person. |

### The canon track

Record the source's plot as world-track entries in your own words: event, roughly when, who drives
it, and — the important column — **what it needs to succeed**. That last one is where an MC
intervenes. A canon event isn't prevented by the MC being strong; it is prevented by the MC
removing one of the three things it needed.

### Reading canon antagonists correctly

The MHA case the user raised is the model. Two drivers in one setting, with opposite profiles:

- A **strategist** who is patient, well-informed, charismatic, and whose plans are explicitly not
  static — an MC who interferes gets studied, then recruited, then removed, in that order, over
  many chapters.
- A **chaotic** whose reactions are fast, personal and disproportionate, and who may target the MC
  for reasons that make no strategic sense at all.

An MC in that world faces real threat — which is the point — and the governor is what keeps it a
story rather than a grind. Derive each canon antagonist's profile from **how they are depicted
behaving in canon**, not from how powerful they are.

### The static-canon defect

Symptoms, all of which mean the dial is effectively 1 regardless of what the config says:

- Canon events fire on their original chapters with the MC present as a witness
- Canon characters treat the MC as background
- The MC's victories are in fights canon never had, against opponents canon never used
- Nothing in the divergence ledger has status `prevented` or `created`
- The story could be summarised without mentioning the MC
- **The MC's foreknowledge keeps working.** If canon knowledge is still reliable in arc 3, the
  world is not moving — the future the MC remembers was the one in which they did nothing, so a
  world that reacts must be invalidating that memory as it goes

**Divergence and foreknowledge decay are the same event, seen from two sides.** A row here with
status `prevented` or `created` is a row in `state/foreknowledge.md` moving toward `invalidated`.
Cross-reference the ids rather than keeping two accounts of one fact; `meta-knowledge` §5 owns the
other half. Doing this is what makes decay a consequence the MC caused instead of an authorial
decree at a scheduled chapter.

---

## Integration into the cycle

**At `novel-init`** — set `reactivity`, `butterfly_horizon`, `escalation_ceiling`, and the
`ending` block. Build the world track for arcs 1–3. Assign a reaction profile to every driver.
For fanfic, record the canon track and the footprint archetype.

**At `chapter-plan`** (new step, after the escalation ladder) — check which world-track entries
fire during this arc, assign them chapters, and confirm the arc moves at least one of them.
Run the point-of-no-return check against the ending contract.

**At `write-chapter` step 1** — answer **the offstage question**: *what did the world do this
chapter that the MC does not know about?* One line. Most chapters it is small. It goes in the CCS
block and it is why the reader believes the world is running.

**In the CCS block** — a `wld>` line when anything moved offstage:

```
wld> AFO: shifts recruitment target after the warehouse (latency 6, fires ~ch51) /
     canon W03 (license exam) still pending, unmoved / market price of agar doubles
```

**At `revision-pass`** — pass 1 gains: the divergence ledger is updated for anything the MC did to
the world track, and no world event fired that the ledger does not record.

**At arc rollup** — the divergence audit:

1. Did this arc move at least one world-track event? If not, that is a defect; fix it in the next
   arc's plan.
2. For fanfic: has a canon character changed a decision because of the MC?
3. Are any changes reaching past `butterfly_horizon`? Narrate them, do not simulate them.
4. Is the ending contract still reachable? Are all `non_negotiables` intact?
5. Crisis count within cap?
6. Escalation within ceiling — one rung, not three?
7. Reciprocity: did each escalation this arc open something?

---

## Self-check

- [ ] The reactivity dial is set, and the chapter's events match it
- [ ] Every driver has a reaction profile, latency and fidelity
- [ ] At least two profiles in play, one of them Indifferent
- [ ] The offstage question is answered in this chapter's `wld>` line
- [ ] The divergence ledger is current
- [ ] This arc moves at least one world-track event
- [ ] Fanfic: at least one canon character has changed a decision because of the MC
- [ ] Crisis count ≤ dial, ≤ 3
- [ ] Every escalation this arc opened something as well as closing something
- [ ] The ending contract is still reachable and no non-negotiable was taken
