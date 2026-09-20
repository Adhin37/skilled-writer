---
type: reference
owner: timeline-engine
description: "the novel is a fanfic. This is where the world's clock does most of its work"
---

# timeline-engine — fan fiction mode

Open this only for a fanfic. It is where the world's clock does the most work — it is what stops canon happening on schedule around an MC who changed things.

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
