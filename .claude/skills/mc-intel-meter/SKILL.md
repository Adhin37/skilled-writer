---
name: mc-intel-meter
description: Pin the main character at a declared intelligence tier and enforce it in both directions — no unearned omniscience, and above all no idiot ball. Use whenever the MC makes a decision, a deduction, a plan, or a mistake, and when reviewing a drafted chapter for competence defects.
---

# mc-intel-meter

`novel.md` → `mc.intel_tier` declares how smart the MC is. This skill makes that number
load-bearing.

It exists because the genre's most common failure is a protagonist described as a peerless
genius who then walks into an obvious trap because the plot needs him to. **The reader forgives
a slow MC. The reader does not forgive an inconsistent one.**

---

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

## Writing intelligence on the page

**Show tier through prediction, not narration.** Never write "he was a genius" or "as expected of
the young master". Instead:

| tier | the technique |
|---|---|
| 1–2 | The MC notices one concrete detail others overlook, and acts on it a beat before others do. |
| 3 | The MC says what will happen; a page later it happens. Once per chapter, no more. |
| 4 | The MC prepares for a contingency the reader has not thought of; when it arrives, the preparation is already in place and *briefly* explained. |
| 5 | A detail planted 15 chapters ago is the answer. The MC never says "I planned this" — the reader realises it first. |

**The trace test.** For every MC decision in a draft, name the on-page fact it came from. If you
cannot point at a specific earlier sentence, either plant the clue or cut the deduction.

**The competence-tax rule.** Every plan that works costs something it did not have to: an ally's
trust, a resource, a lie that will come due. Free wins read as author favour at every tier.

**Anti-monologue.** Deduction is dramatised, not lectured. Break long reasoning across dialogue,
action, and a single short interior beat. A tier-5 MC explaining their reasoning for 600 words is
a tier-5 MC who is boring.

## Intelligence vs. knowledge vs. wisdom

Keep them separate; conflating them is what produces the insufferable protagonist.

- **Intelligence** (fixed by tier): speed and depth of inference.
- **Knowledge** (grows): what they have been told or have seen. Tracked in CCS `kno>`.
- **Expertise** (narrow, and earned): what they have been *trained* in. Bounded by domain in
  `bible/cast/_competence.md` (`competence-map`).
- **Wisdom** (their arc): whether they act well on what they know. This *should* be low early.
- **Foreknowledge** (given, and decaying): facts about a future they did not earn. Bounded by
  grain in `state/foreknowledge.md` (`meta-knowledge`). A separate axis again — a tier-2 MC with
  perfect foreknowledge still reasons like a tier-2 MC and will misuse good information, while a
  tier-5 MC with `impressions` reasons brilliantly from almost nothing.

A tier-5 MC with low wisdom is the best version of the genre: he is right about the plan and
wrong about what the plan is for.

**And foreknowledge is not a licence to be stupid.** The mirror of the rule below, and the more
tempting error: an author worried that foreknowledge trivialises the plot writes an MC who forgets
what they know, fails to plan, or never thinks about the future at all. That is the idiot ball
with extra steps. A competent person who wakes up knowing what is coming *makes a plan* — the
right way to keep tension is an incomplete map, not a dulled protagonist. See `meta-knowledge` §2.

**A high tier is not a licence to know things.** This is the defect the split above exists to
prevent, and it is the one most often waved through: a brilliant MC infers faster, but they cannot
infer a fact they were never given, and they cannot practise a craft they never learned. A tier-5
strategist who has never held a hammer does not identify the forge-mark; they reason from what the
mark's *existence* implies, or they ask someone. Every fact the MC states still passes
`competence-map`'s provenance test — taught, did, told, read, or openly guessing — and "they're
smart" is not one of the five.

## Interaction with other characters

Raising the MC by lowering everyone else is the cheapest and most damaging shortcut in the genre.
The opposite shortcut is just as common and harder to see: **giving everyone the MC's tier**, so
that every ally reasons at the protagonist's speed and the whole cast becomes one mind with several
names.

- The antagonist's effective tier is **MC tier or higher** at least once per arc.
- At least one recurring ally out-thinks the MC in their own domain, on the page.
- Ordinary people are competent at their own lives. A guard who has stood that gate for ten years
  knows things the MC does not.
- Never write a scene whose only function is other characters being astonished at the MC.

**The rest of the cast is tiered too.** This ladder applies to every named character, not just the
protagonist; their tiers are declared in `bible/cast/_voices.md` and the cast must **straddle** the
MC's — somebody above it, somebody below. `voice-separation` owns that table, along with the axis
this skill deliberately does not measure: **articulacy**, which is independent of intelligence.
The character who is right and cannot prove it, and the character who is wrong and can out-argue
anyone, are both built by separating those two numbers.

**Low tiers are written without contempt.** A tier-1 character has a shorter causal chain — they
stop at the first sufficient explanation and act on it. They do not have worse grammar, an accent,
or a class marker (`bias-guard`), they are competent at their own work, and they are right about
something concrete that the clever ones have abstracted past. A character whose only function in a
scene is to be wrong so the MC can be right is the floor rule broken from the other direction.

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
