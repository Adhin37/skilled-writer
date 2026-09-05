---
name: prose-quality
description: Line-level editing for serialized fiction — rhythm, concreteness, verb strength, description economy, and removal of AI-default phrasing. Runs on every chapter inside revision-pass and applies while drafting.
---

# prose-quality

Sentence-level craft. `mtl-detox` removes translated-corpus residue; this skill removes the other
default register — the fluent, symmetrical, slightly hollow prose that a model produces when
nothing is pushing back.

---

## The AI-default tells

These are the phrases and shapes that mark machine-written fiction. Hunt them explicitly.

**Phrases to cut**

*a mix of X and Y* · *a testament to* · *something shifted in the air* · *the weight of X settled
over* · *a moment that stretched* · *she couldn't shake the feeling* · *little did she know* ·
*for the first time in a long time* · *a silence stretched between them* · *emotions warred within
her* · *the air was thick with tension* · *a chill ran down his spine* · *time seemed to slow* ·
*he let out a breath he didn't know he was holding* · *this changes everything*

**Shapes to break**

| shape | example | fix |
|---|---|---|
| The tricolon habit | "It was cold, it was quiet, and it was wrong." | Two items, or four. Three is the model's default cadence. |
| Balanced antithesis every paragraph | "Not a threat. A promise." | Once per chapter, maximum. It is a strong move that goes stale fast. |
| Em-dash appositive on every other sentence | "She ran — because running was all she had left." | Vary the connector, or cut the second clause. |
| Uniform sentence length | 14, 15, 13, 16 words | Deliberately write a three-word sentence and a thirty-word one. |
| Every paragraph the same length | four lines, forever | Let a one-line paragraph carry a beat. |
| Ending every scene on a portentous fragment | "And then, silence." | Earn it or cut it. |
| Naming the emotion after showing it | "...her hands shook. She was terrified." | Keep the hands. Cut the sentence. |
| Summarising the scene's meaning at its close | "It was the moment everything changed." | The reader decides that. Delete. |

## Positive standards

**Concreteness.** Every abstraction should be within one sentence of a physical fact. "The Guild
was corrupt" is nothing; "the Guild's ledger had two columns and both were true" is a scene.

**Verbs carry the sentence.** Strong verb + plain noun beats weak verb + adverb + adjective.
*He walked quickly and angrily to the door* → *He got to the door before she could stand up.*

**Specificity beats intensity.** Not "an enormous, terrifying beast" but the one detail that
makes it real — what it smells like, what it does with its weight, what it ignores.

**One image per beat.** A paragraph with three metaphors has none.

**Description in motion.** Deliver setting through a character doing something in it. Never stop
the story to describe a room. Two sensory details, placed inside action, out-perform a paragraph.
This skill owns the *sentence*; `world-texture` owns **which** details are allowed on the page and
how many. If the two seem to disagree, the budget wins — a beautifully written detail that is not
load-bearing is still cut.

**Sentence rhythm mirrors pressure.** Long, subordinated sentences for control and deliberation.
Short ones when things go wrong. Fragments at the moment of impact. Then a long one afterwards,
for the numbness.

**White space is pacing.** On a phone, a paragraph over six lines is skimmed. Break for emphasis;
a single-line paragraph is the strongest position on the page.

**Cut the obvious stage business.** Characters standing up, opening doors, walking across rooms,
nodding. If it does not change something, delete it. Nodding is the single most common dead beat.

**A beat that identifies nobody is stage business.** *Nodded · shrugged · sighed · raised an
eyebrow · crossed their arms · ran a hand through their hair · clenched their jaw · let out a
breath · looked away · smiled slightly* — the default gesture set, available to every character
and therefore attached to none. Replace with that character's own hand-habit or pressure move
(`voice-separation` §4), or cut the beat: a line with no beat beats a line with a generic one.

## Filter verbs and telling

Covered in `narrator-voice`, enforced here: *saw, heard, felt, noticed, realised, watched,
thought, wondered, seemed, decided*. Remove unless the act of perceiving is the point.

Naming emotions: *she was angry, he felt sad, they were nervous*. Replace with behaviour, or with
what the emotion makes the character *do differently*. But do not overcorrect into a body-part
catalogue — jaws clench, stomachs drop and hearts pound are their own cliché set. The best
emotional beat is usually a **decision**, not a sensation.

## Chapter-level rhythm

- Vary paragraph length across the chapter; check by eye, the shape should be irregular.
- No two consecutive paragraphs starting with the same word — especially a character name or "He"/"She".
- Read the first sentence of every paragraph in sequence. They should not all be the same shape.
- Dialogue-heavy stretches need a grounding beat every 3–4 exchanges; action stretches need one
  clear spatial anchor per paragraph.

## Word-level

- **Adverbs**: usually a symptom that the verb is wrong.
- **"Very", "really", "quite", "somewhat", "rather", "slightly"**: cut.
- **"Suddenly"**: cut. Suddenness comes from sentence length, not from the word.
- **"Began to", "started to", "proceeded to"**: cut; use the verb.
- **"That"**: delete where the sentence survives without it.
- **Repeated distinctive words**: a striking word used twice in a chapter loses both uses. Track
  the ones you like — those are the ones you will overuse.
- **Sensory balance**: sight dominates by default. Deliberately place one non-visual detail per
  scene. Smell is the most underused and the most memorable.

## Procedure

1. Search for each AI-default phrase. Cut or rewrite.
2. Search filter verbs; remove or justify.
3. Search adverbs ending `-ly`; keep the ones doing real work.
4. Scan paragraph openings for repetition.
5. Scan for uniform sentence length; break up any run of five similar-length sentences.
6. Find every named emotion; convert to behaviour or decision.
7. Find every static description block; put it in motion or cut it.
8. Read the chapter's first and last 150 words aloud. Those two passages carry the most weight.

## Self-check

- [ ] No phrase from the cut list
- [ ] Sentence lengths visibly varied
- [ ] No paragraph over six lines without a reason
- [ ] Every abstraction anchored to a physical fact within one sentence
- [ ] No emotion named where behaviour or decision would carry it
- [ ] One non-visual sensory detail per scene
- [ ] No dead stage business
