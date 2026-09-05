---
name: dialogue-voice
description: Write dialogue that identifies the speaker without tags, using each character's speech fingerprint and their current development state. Use whenever writing or revising any line of dialogue.
---

# dialogue-voice

The tag-removal test: **strip every `said X` from a page of dialogue. If a reader cannot tell who
is speaking, the scene is broken.** This skill is how you pass that test cheaply.

---

## The layer under this one

The eight fields below are a **surface**. Contractions, a vocabulary tell and a syntax tic applied
to minds that are all as quick and as articulate as the MC produce labelled clones — the reader
can tell the labels apart and still hears one person. Before the fingerprint comes the matrix in
`bible/cast/_voices.md`: **intel, articulacy, wit, heat, turn length** (`voice-separation` §1).

Two rules from that skill bind every scene written here:

- **The MC-contrast rule** — at least one speaker in the chapter differs from the MC on two or
  more axes.
- **The three-way clash** — no two speakers in a scene share intel + articulacy + wit.

The exception is a declared **mirror** — a clone, avatar, double or body-snatch, who is permitted
to share the original's fingerprint. See `voice-separation` §7.

## Before writing a scene

Load, for each speaker: their matrix row (`bible/cast/_voices.md`), their speech fingerprint
(profile), their accumulated voice deltas (`state/growth.md`), and their three calibration lines.
Two minutes here saves a revision pass.

**How much voice each speaker gets** — by cast tier (`character-profile`):

| tier | load | the test |
|---|---|---|
| **A** principal | matrix row, all eight fields, three calibration lines, every voice delta | tag-removal + transplant |
| **B** supporting | matrix row, and three fields — contractions, vocabulary tell, syntax tic — plus one calibration line | tag-removal |
| **C** walk-on | the one line in `_extras.md`: their five-minute want, their tic, what they carry, their one off-default axis | swap test |
| **D** furniture | nothing. They get function dialogue and no voice | — |

A walk-on does not need eight fields to sound like a person. They need to want something small
and specific in this scene, and to say one thing only someone in their job would say. That is
two clauses of work, and it is the difference between a character and a vending machine.

## The eight fingerprint fields, used

| field | how it shows up in a line |
|---|---|
| register | word choice ceiling and floor — "acquire" vs "get" vs "lift" |
| sentence length | and *how it changes under stress* — most characters shorten; some flood |
| contractions | the single cheapest differentiator. One character who never contracts is instantly legible |
| vocabulary tell | 3–5 words only they use. Deploy roughly once per scene, never twice in a row |
| syntax tic | answering questions with questions; trailing conditionals; starting with "So" |
| what they never say | the admission that will not cross their lips — they talk *around* it |
| profanity | none / mild / heavy / inventive-and-specific. Specific is characterisation |
| silence | what makes them stop. When they go quiet, the reader learns something |

## Rules

**One voice per line.** If a line could be moved to another character with no edit, it is
generic. Rewrite one of the two.

**The transplant test — the MC version.** Take the MC's most characteristic line in the scene and
put it in another named character's mouth. If it fits, one of the two has no voice, and the one to
rewrite is the other character, never the MC. This is the failure that produces a whole cast of
protagonists.

**Hold the turn lengths.** Each recurring speaker has a default number of words per turn. Two
characters with matching turn lengths read as one person however carefully their vocabulary
differs — it is the crudest differentiator and the most reliable.

**Walk-ons speak from their job, not from their soul.** The cheapest non-generic line an extra can
say is the one that reveals what their day is like: a price, a rule, a complaint about a rule, the
thing they have said forty times this week. No interiority, no backstory, no philosophy. The
innkeeper does not muse about fate; she says the room is taken and the levy went up.

**Characters talk past each other.** Real dialogue is two agendas colliding. Each speaker wants
something from the exchange; they rarely want the same thing. Before writing a conversation, name
what each side wants from it. If one side wants nothing, cut them or give them a want.

**Subtext by default.** Characters say the second-best thing. The direct statement is reserved —
which is what makes it land when it comes.

**Answer at an angle.** People deflect, change the subject, answer a different question, ask one
back. Straight answers are a choice with meaning.

**Interruption and overlap.** Em dash for interruption, ellipsis for trailing off. Pick the house
convention in `lexicon.md` and hold it.

**Tags: `said` and `asked`.** Almost always. `Hissed`, `growled`, `chuckled`, `smirked` are the
prose asking the reader to feel something the line failed to earn. An action beat beats an adverb:
not *"Fine," he said angrily* but *"Fine." He put the cup down harder than he meant to.*

**Beats carry blocking, and the beat must be theirs.** Use action beats to keep bodies in space and
to control rhythm — one every three to four exchanges, more in tense scenes, fewer in fast ones.
Draw each from that character's **hands** field and **pressure move** (`voice-separation` §4), so
the beat identifies the speaker as well as the line does. Never from the default gesture set —
*nodded, shrugged, sighed, raised an eyebrow, crossed their arms, ran a hand through their hair,
clenched their jaw, let out a breath* — which belongs to everyone and therefore to nobody. A line
with no beat beats a line with a generic one.

**Dialect by rhythm, not by spelling.** Phonetic spelling (`'ere, guv`) is unreadable and often
condescending. Convey origin through word order, idiom, formality and what the character takes for
granted. See `bias-guard` — accent must never be a marker of villainy or stupidity.

**Names in dialogue are rare.** People use each other's names when getting attention, being
formal, being intimate, or being cold. Not every third line.

**No expository dialogue between people who both know the thing.** If both characters know it,
they do not explain it to each other. Give the information to someone who genuinely lacks it, or
carry it in narration, or let the reader infer it.

**And nobody explains a subject they were never taught.** The other half of the same rule: before
assigning an explanation, check the speaker's row in `bible/cast/_competence.md`. Exposition handed
to whoever is standing there is how a whole cast ends up omniscient. Three better moves — give the
line to the person whose domain it is, let the speaker say they do not know and name who does, or
let them be confidently **wrong**, which is usually the best scene of the three
(`competence-map` §2, §3).

**"I don't know" is a strong line.** So is "that's not my end", "ask Dael", and "I'd guess, but
it's a guess". They read as competence, not weakness — a character who knows the edge of their own
knowledge is more credible than one who always has an answer.

## Development and voice

Apply every accumulated voice delta from `state/growth.md`. This is the concrete mechanism by
which a reader *feels* that a character has changed. A character at rung 4 with a
"drops the honorific" delta does not use the honorific — ever — unless they are regressing, and
then the reader should notice.

## Calibration procedure

When a character's voice starts drifting mid-serial:

1. Read their three calibration lines from the profile.
2. Read their most recent five lines from the last chapter they appeared in.
3. Ask: do these sound like the same person, plus the recorded deltas?
4. If not, either fix the recent lines, or — if the drift is better than the profile — update the
   profile and record it as a deliberate change.

## Failure modes

| symptom | fix |
|---|---|
| Everyone is witty | Wit is a fingerprint, not a default. Cap it at two characters and name the pressure that triggers each. `voice-separation` §1 |
| Everyone is articulate | Articulacy is an axis, and it is independent of intelligence. Give someone artic 2 and let them be exactly right in five words. |
| Every ally is as quick as the MC | The cast has to straddle the MC's tier, not sit on it. Put somebody below it and let them be correct about something concrete. |
| Two characters are interchangeable | They share intel + artic + wit. Change one axis or merge the characters. |
| The clone sounds like the original | Correct, if they are a declared mirror. Then ask what has diverged since they split, and what the tell is. `voice-separation` §7 |
| Dialogue explains the plot | Move it to narration or delete it. The reader is smarter than this. |
| Characters agree too fast | Someone should want the conversation to go somewhere else. |
| A scene is two heads talking in a void | Add a beat: where the bodies are, what one of them is doing with their hands. |
| Every walk-on is wise, or every walk-on is a wall | Give them the third stroke — one piece of their working world — and nothing else. |
| Threat-speech from a villain | Villains persuade, negotiate, and are reasonable right up until they are not. |

## Anti-patterns from the translated corpus

Never write these. See `mtl-detox` for the full list.

- "You dare?!" · "Trash!" · "Do you know who I am?" · "Court death!"
- Villains announcing their own arrogance
- Characters addressing themselves in the third person by title
- Crowd reaction blocks: bystanders narrating how impressive the MC is
- A character explaining the power system to someone who already lives in it

## Self-check

- [ ] Tags stripped — is every tier-A and tier-B speaker identifiable?
- [ ] Transplant test — the MC's best line does not fit anyone else's mouth
- [ ] At least one speaker differs from the MC on two or more axes
- [ ] No two speakers in a scene share intel + articulacy + wit
- [ ] Turn lengths held; every beat drawn from that character's hands or pressure move
- [ ] Swap test on the walk-ons — could another extra have this scene with no edit?
- [ ] Does each speaker want something distinct from this conversation?
- [ ] Any line that could belong to anyone? Rewrite it.
- [ ] Voice deltas applied?
- [ ] `said`/`asked` unless a stronger verb genuinely earns its place?
- [ ] No dialogue explaining what both speakers already know?
- [ ] Nobody explained a subject their competence map does not cover?
- [ ] Did anyone say they did not know, defer to someone, or turn out to be wrong?
