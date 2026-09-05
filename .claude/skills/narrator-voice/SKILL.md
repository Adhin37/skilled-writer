---
name: narrator-voice
description: Establish and hold the narrating voice — person, tense, narrative distance, interiority and filtering — so the novel sounds like one book across hundreds of chapters. Use when setting up a novel, when drafting any chapter, and when the prose starts feeling generic or inconsistent.
---

# narrator-voice

The narrator is a character even when unnamed. `novel.md` → `narration:` declares its
parameters; this skill turns them into sentences and keeps them stable for 300 chapters.

---

## The parameters

### Person

| mode | strength | cost | use when |
|---|---|---|---|
| `first` | maximum intimacy, voice does the heavy lifting | one head only; unreliable narration is work | character-driven, a distinctive MC voice, mystery |
| `third-limited` | intimacy plus flexibility; the platform default | requires discipline about what the POV can know | almost always |
| `third-objective` | cool, cinematic, ambiguous | no interiority; hard to sustain | thriller stretches, prologues |

There is no `third-omniscient` option. True omniscience is the vector by which the translated
corpus's worst habits enter: the narrator announcing that the MC is a genius, that the crowd was
astonished, that the young master had made a fatal mistake. If the novel needs a wider lens, use
`pov-switch` with scene-level switching, which keeps each stretch anchored in one head.

### Tense

`past` — invisible, flexible, the default. `present` — immediate, tightens pace, and grows tiring
across long chapters; it also makes flashbacks awkward. Choose once. **Never mix.**

### Distance

The single most useful dial, and the one most writers never touch. Distance is how far the prose
sits from the POV character's mind.

| distance | example |
|---|---|
| **cool** — camera outside | *Rin crossed the market and stopped at the third stall.* |
| **medium** — reports thought | *Rin crossed the market, watching for the stall she had been told about.* |
| **close** — the prose thinks in her idiom | *Third stall. The one with the bad awning. Rin kept her hands where the seller could see them.* |
| **deep** — no seam between prose and thought | *Third stall, bad awning, and the seller's eyes already on her hands. Fine. Let him look.* |

**Distance is a rhythm, not a setting.** The craft is in moving it deliberately:

- Open a scene one notch cooler to establish where we are.
- Tighten as pressure rises. The climactic beat of a chapter should be the closest prose in it.
- Pull back after a blow lands — distance is how the page conveys numbness.
- Fragment sentences as you go closer. Deep distance permits sentences that are not sentences.

`narration.distance` in `novel.md` sets the *habitual* level. Excursions are expected; drift is not.

### Interiority

`high` / `medium` / `low` — how much of the POV character's thinking reaches the page.

Even at `high`, interiority is **reaction and decision**, not a transcript. Cut any interior beat
that only restates what just happened or what the reader already concluded.

Rule of thumb: one interior beat per page, at the moment of choice. That is where thought is
dramatic; everywhere else it is filler.

## Filtering — the most common defect in AI-written prose

In close third or first, remove filter verbs. The POV *is* the camera; saying so doubles the
distance and flattens the sentence.

| filtered | direct |
|---|---|
| She saw the door was open. | The door was open. |
| He felt a chill run through him. | The cold went through his coat like it was not there. |
| She realised the ledger was a forgery. | The ledger was a forgery. Of course it was. |
| He noticed that the guard was gone. | The guard was gone. |
| She heard footsteps behind her. | Footsteps, behind her. |

Filter verbs to hunt: *saw, heard, felt, noticed, realised, watched, observed, thought, wondered,
seemed, decided, found herself, could see, was aware that*.

Keep a filter verb only when the *act of perceiving* is the point: *She watched him lie to her
mother and did nothing.*

## Holding the voice across a serial

1. **A voice sample.** Keep the best 150 words the novel has produced in `novel.md` →
   `narration.voice_notes`, or point at a chapter and line range. Read it before drafting.
2. **Three rules, written down.** Distil the voice into three enforceable rules, e.g.:
   *no simile longer than five words · never name an emotion the body can show · sentences shorten
   under threat.* Put them in `voice_notes`. Check the draft against them.
3. **Register floor and ceiling.** Decide the most and least formal words this narrator will use.
   A narrator who says "aforementioned" in one chapter and "vibe" in the next has no voice.
4. **Metaphor domain.** Draw comparisons from what this narrator would know — a smuggler's
   narrator reaches for weights, tides and prices; a scholar's for texts and taxonomy. Consistent
   metaphor sourcing is 80% of what readers call "a strong voice".

## Chapter-opening lines

The narrator's most-tested surface. Readers meet it on a scroll, days apart.

**Never open with:** weather with no stake · waking up · a recap of the last chapter · a
dictionary or in-world encyclopaedia entry · a rank/level recital · the date and time as a
standalone line.

**Do open with:** a line of dialogue mid-argument · an action already in progress · a concrete
wrong detail (something present that should not be) · a flat declarative that implies a story
(*The coat did not fit and she wore it anyway.*)

## Self-check

- [ ] Person and tense unchanged from `novel.md`, and unchanged within the chapter
- [ ] No knowledge on the page that the POV character could not have
- [ ] Filter verbs removed except where perceiving is the point
- [ ] Distance tightens at the chapter's hottest moment
- [ ] Metaphors drawn from the narrator's own world
- [ ] Interiority is decision and reaction, not transcript
- [ ] The three voice rules hold
