---
name: mc-intel-meter
description: Pin the MC at a declared intelligence tier and enforce it both ways - no unearned omniscience, no idiot ball. Use on any MC decision, deduction, plan or mistake, and when reviewing a draft.
---

# mc-intel-meter

`novel.md` → `mc.intel_tier` declares how smart the MC is. This skill makes that number
load-bearing.

It exists because the genre's most common failure is a protagonist described as a peerless
genius who then walks into an obvious trap because the plot needs him to. **The reader forgives
a slow MC. The reader does not forgive an inconsistent one.**

---

## What lives in `references/`

| file | open it when |
|---|---|
| `references/writing-intelligence.md` | the MC is deducing, planning or failing and you need the technique rather than the rule — including the intelligence / knowledge / wisdom distinction |
| `references/audit-card.md` | never, by you. `revision-pass` Pass 3 opens it |

## The tiers

| tier | name | how they think | inference budget | error profile |
|---|---|---|---|---|
| 1 | Ordinary | Reacts well, plans one step. Learns by consequence. | states each step aloud or on the page | misses implications; recovers by persistence |
| 2 | Sharp | Notices what others miss. Plans two steps. | may skip one obvious step | right about facts, wrong about people's motives |
| 3 | Smart | Reads situations and people. Plans three steps with a fallback. | skips routine steps, shows the key one | over-trusts their own read; blind to their own motives |
| 4 | Brilliant | Builds plans that survive contact. Models opponents accurately. | shows only the pivot; the reader reconstructs the rest | solves the stated problem, not the real one; underestimates irrational actors |
| 5 | Genius | Sees the shape of the whole board. Plans branch. | shows the conclusion; the clue was planted chapters ago | catastrophically bad at what cannot be modelled — grief, loyalty, being loved |

**Inference budget** = how many reasoning steps may happen off the page. Higher tier, more may
be skipped — but every skipped step must be *reconstructible* by an attentive reader from
material already given.

**Error profile** is not optional. It is what makes the tier believable. A tier-5 MC who is also
wise about people is not a character, he is a wish.

## The floor — applies at every tier

The MC never:

1. Forgets something the reader watched them learn. (Check `kno>` in the CCS block.)
2. Fails to ask the obvious question when a person who would answer it is standing there.
3. Walks into a trap the reader saw coming, unless the MC's own reason for walking in is stated
   and defensible.
4. Explains their plan to an enemy who then escapes with it.
5. Is surprised by a rule of the world the reader was taught in a previous chapter.
6. Wins by remembering, at the exact moment of need, an ability the reader has never seen.
7. Ignores a resource in their possession that would trivially solve the problem — unless a
   stated cost prevents its use.

Any of these in a draft is a defect. **The fix is never to lower the MC's intelligence.**

## The three legal ways to make a smart MC fail

When the plot needs the MC not to succeed, use one of these. Only these.

| lever | what it looks like | example |
|---|---|---|
| **Missing information** | They reason correctly from what they have; what they have is incomplete or planted. | The ledger is accurate. The ledger was written to be found. |
| **Opposed will** | Someone at least as capable wants the opposite, and moves first. | She predicted his approach because she taught him. |
| **Cost** | They see the right answer and cannot afford it. | He knows the door is a decoy. Checking it means leaving the child alone. |

A fourth, used sparingly: **the blind spot** — from `mc.blind_spots` in `novel.md`. A tier-4
strategist who cannot read affection may misjudge who will betray him. This must be established
early and stay consistent; it is character, not convenience.

## Review checklist (run in `revision-pass`)

- [ ] Every MC decision passes the trace test
- [ ] No violation of the seven floor rules
- [ ] Any MC failure uses information / opposed will / cost / established blind spot
- [ ] No narration asserting the MC is smart
- [ ] No character was made stupid to make the MC look smart
- [ ] No character was made *as clever as the MC* by default — the cast straddles the tier
- [ ] No fact was known because the character is intelligent — every one has a provenance
- [ ] Nobody answered inside a domain their competence map does not list
- [ ] Deduction dramatised, not monologued
- [ ] If tier ≥ 4: the reader could have reached the conclusion from planted material
- [ ] If tier ≤ 2: the MC has not suddenly deduced something above their tier
