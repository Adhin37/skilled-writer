---
name: pov-switch
description: Decide whether a novel switches viewpoint, who is eligible, and how to execute it. Use when setting up a novel, planning chapters, and before any chapter that changes POV character.
owns: [pov-mode, viewpoint-switch]
---

# pov-switch

Governed by `novel.md` → `pov:`. **Read it first.** If `pov.mode: single` and
`switch_granularity: never`, this skill's answer is always no — enforce that and stop.

Head-hopping is the most common structural defect in serialized fiction and the fastest way to
lose reader attachment. Every switch must be paid for.

---

## Choosing the mode (at `novel-init`)

| mode | POV characters | switches at | best for | cost |
|---|---|---|---|---|
| `single` | 1 | never | strongest attachment; mystery; a distinctive voice; anything by a low-effort model | the reader only knows what one person knows |
| `dual` | 2 | chapter | two-sided conflict; romance; a rival who is right | halves the time spent with each |
| `rotating` | 3–5 | chapter | ensemble, war, political fantasy | long gaps between visits; readers form favourites and skim |
| `ensemble` | 6+ | chapter | epic scope | almost always a mistake in a serial — the reader has no one to follow |

Record the chosen mode in `pov.mode` and the eligible viewpoints in **`pov.pov_characters`**,
ordered, first is primary. That list is the authority: nobody outside it narrates, and adding a
name to it mid-novel is an arc-boundary decision, never a chapter-level one. Each name on it also
needs a `pov_eligible: true` row in `bible/cast/_voices.md` §3, because a POV character without a
declared thought unit narrates in the MC's voice (`voice-separation`).

**Recommend `single` unless the premise structurally requires otherwise.** A premise requires
more than one POV only when the story depends on the reader knowing something the MC cannot —
a conspiracy running in parallel, a second protagonist with equal claim, a rival whose choices
must be understood rather than guessed.

### Granularity

- `chapter` — switch only at chapter boundaries. **Strongly preferred.** Clean, phone-readable,
  hard to get wrong.
- `scene` — switch at `* * *` breaks. Allowed, but never more than one switch per chapter.
- `never` — locked.

Mid-scene switching is forbidden in all modes. Two heads in one scene is head-hopping.

### `antagonist_pov`

| setting | meaning |
|---|---|
| `never` | the antagonist stays opaque; their competence is inferred from effects. Best for mystery and for dread. |
| `rare` | 1–2 chapters per arc, at moments where their reasoning changes the stakes |
| `scheduled` | a genuine second protagonist; use `dual` instead |

An antagonist POV trades menace for understanding. Spend it deliberately: the chapter where the
reader stops being afraid of the villain and starts being afraid *for* someone.

## When a switch is justified

A switch must pass **at least one**:

1. **Information the MC cannot have** and the reader needs now for dread or irony.
2. **A decision made elsewhere** that will hit the MC later, and matters more if seen being made.
3. **A parallel line of action** running on its own clock.
4. **A character's arc** that requires being inside their head to land — usually a rung advance
   that would look like betrayal from outside.

A switch fails if: it exists to show the MC being impressive from outside; it delivers exposition
more conveniently; it dodges a hard scene in the MC's head; or it happens because the MC is
asleep and the chapter needs filling.

## Executing a switch

1. **Announce it structurally.** If `pov.label_switches: true`, the POV name is the first line
   under the chapter title, italicised, alone. Consistent labelling is a kindness to serial
   readers, not a crutch.
2. **Establish the new head in the first two sentences** — through idiom, not announcement. The
   sentence rhythm, the metaphor source and what the character notices should identify them
   before the name does.
3. **Different eyes see different things.** A soldier entering a room registers exits and hands.
   A merchant registers cloth and prices. If the new POV notices the same details the last one
   would, the switch bought nothing.
   Two mechanical checks (`voice-separation/references/channels.md`): their **thought unit** — images, words, numbers,
   bodies, rules, people, money — supplies this chapter's metaphors, and no two POV characters may
   share one. Their **thought speed** — ahead of the scene, with it, one beat behind — sets whether
   the narration arrives at conclusions before or after the reader does. A POV character whose
   thought unit and speed match the MC's has not changed the camera, only the name above it.
4. **Hold to their knowledge.** The new POV knows what their CCS `kno>` entries say and nothing
   more. This is the highest-risk moment for a continuity break.
5. **Their voice, their deltas.** Load their fingerprint and growth row exactly as for dialogue.
   Narration in their POV is coloured by their register.
6. **Never re-narrate a shown scene from the other side** unless the whole point is that they
   perceived it differently — and then only once in a novel.

## Return discipline

- **Never leave the MC for more than two consecutive chapters.** Serial readers came for one
  person; a three-chapter absence produces skimming, and skimming produces drop-off.
- End a non-MC chapter on a hook that points *at* the MC's situation, so the return feels like
  arrival rather than interruption.
- Keep a rough budget: in `dual`, 60/40 toward the MC; in `rotating`, the MC gets at least half.

## Planning

`plan/chapters.md` has a `pov` column. Assign POV during arc planning, not while drafting —
deciding mid-draft is how a switch ends up unjustified. Record the POV in the CCS header.

## Self-check

- [ ] `novel.md` permits this switch at this granularity
- [ ] The switch passes at least one justification test
- [ ] The new POV is identifiable from voice within two sentences
- [ ] Nothing on the page exceeds this POV's knowledge
- [ ] What they notice differs from what the previous POV would have noticed
- [ ] Their thought unit is not the MC's, and it is the source of this chapter's metaphors
- [ ] The MC has not been absent for more than two chapters
- [ ] No mid-scene switching anywhere in the chapter
