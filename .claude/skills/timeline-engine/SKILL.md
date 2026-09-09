---
name: timeline-engine
description: Run the world's own plot on its own clock and make it react to the MC at a dialled intensity. Use when planning arcs, when the MC acts against a faction or canon event, and once per chapter.
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

## What lives in `references/`

| file | open it when |
|---|---|
| `references/reaction-and-governor.md` | a faction or canon power is about to react to the MC, or escalation is running hotter than the reader can carry |
| `references/fanfic-mode.md` | the novel is a fanfic. This is where the world's clock does most of its work |

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
