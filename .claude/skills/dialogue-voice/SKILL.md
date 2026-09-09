---
name: dialogue-voice
description: Write dialogue that identifies the speaker without tags, from each character's speech fingerprint. Use when writing or revising any line of dialogue.
---

# dialogue-voice

The tag-removal test: **strip every `said X` from a page of dialogue. If a reader cannot tell who
is speaking, the scene is broken.** This skill is how you pass that test cheaply.

---

## What lives in `references/`

| file | open it when |
|---|---|
| `references/corpus-anti-patterns.md` | two characters will not separate however hard you push the fingerprints, or the dialogue is reading as machine-translated |

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
to share the original's fingerprint. See `voice-separation/references/mirror-clause.md`.

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
which is what makes it land when it comes. This is a procedure, not a mood; see §Subtext, below.

**Answer at an angle.** People deflect, change the subject, answer a different question, ask one
back. Straight answers are a choice with meaning.

**Interruption and overlap.** Em dash for interruption, ellipsis for trailing off. Pick the house
convention in `lexicon.md` and hold it.

**Punctuation and channels.** Speech goes in `"…"`. A quotation *inside* a line of speech takes
single marks as normal English — `"He actually said 'no comment' to my face."` — and this does not
collide with the direct-thought channel, because thought is a `'…'` that stands outside any `"…"`
pair. The full rule set is `narrator-voice` §The four channels; this skill defers to it.

**Tags: `said` and `asked`.** Almost always. `Hissed`, `growled`, `chuckled`, `smirked` are the
prose asking the reader to feel something the line failed to earn. An action beat beats an adverb:
not *"Fine," he said angrily* but *"Fine." He put the cup down harder than he meant to.*

**Beats carry blocking, and the beat must be theirs.** Use action beats to keep bodies in space and
to control rhythm — one every three to four exchanges, more in tense scenes, fewer in fast ones.
Draw each from that character's **hands** field and **pressure move** (`voice-separation/references/channels.md`), so
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
(`competence-map` §2 , §3).

**"I don't know" is a strong line.** So is "that's not my end", "ask Dael", and "I'd guess, but
it's a guess". They read as competence, not weakness — a character who knows the edge of their own
knowledge is more credible than one who always has an answer.

## Development and voice

Apply every accumulated voice delta from `state/growth.md`. This is the concrete mechanism by
which a reader *feels* that a character has changed. A character at rung 4 with a
"drops the honorific" delta does not use the honorific — ever — unless they are regressing, and
then the reader should notice.

## How much dialogue

The fingerprints in this skill only reach the reader through lines that actually get spoken. A
chapter can pass every test above and still fail, because the test never ran: if the cast barely
speaks, there is nothing to tell apart.

**Target 25–40% of the chapter's words inside double quotation marks** — spoken aloud, to another
person. That is the register of the format. It is not a stylistic preference; it is what makes a
chapter feel like events happening between people rather than one mind narrating its own analysis.

**Speech only.** Direct thought (`'…'`) and meta text (`[…]`) are different channels and do not
count toward this share — see `narrator-voice` §The four channels. A chapter can be 40% marked
text and still be one person alone in their own head, which is the exact defect this target
exists to catch. Measure what is inside `"…"` and nothing else.

| share | what it reads as | verdict |
|---|---|---|
| under 10% | interior monologue with quotes attached | a warn on one chapter; a **defect** when the five-chapter mean falls here — the cast is scenery |
| 10–20% | literary-introspective | allowed only as a deliberate, occasional chapter |
| 25–40% | the serialized format | target |
| over 55% | radio play; setting and interiority starve | pull back |

**The floor is measured over five chapters, not one.** A single near-silent chapter is a
legitimate choice — a solo infiltration, a character alone with a body. `sw lint` warns on it and
moves on. The **defect** (`speech-starvation`) fires only when the mean of the trailing five
chapters falls under 10%, because that is the shape of the real failure: a cast that has stopped
speaking. Do not write toward the floor. A chapter inflated with muttering to clear a number is
the padding this target exists to prevent, and it has happened — benchmark run #2, chapter 2, at
10.2%.

**The diagnostic.** A POV character with a strong analytical voice is the usual cause: the model
routes every beat through their reasoning because that voice is enjoyable to write. The tell is a
scene where a second person is physically present and says nothing, or says one line and is
narrated *about* for three paragraphs. Whenever another character is in the room, ask what they
would say — and let them say it instead of having the POV character infer it.

**Interiority is not a substitute for a scene.** If the POV character concludes something about
another person, the stronger version is almost always that the other person does or says the thing
and the reader concludes it. Give the deduction a surface to land on.

Two structural consequences worth holding while drafting: a chapter with only one speaking
character is a chapter `voice-separation` cannot audit, and a walk-on who never opens their mouth
cannot pass the swap test in `character-profile`. Both skills quietly no-op on a silent cast.

## Subtext

Subtext is two people talking about one thing and meaning another, **and both of them knowing
it**. It is the difference between dialogue that conveys information and dialogue a reader leans
into, and it is the single most reliable way to stop a scene reading as an exchange of facts.

Machine-written dialogue fails here by default and fails in a specific direction: it is
*over-determined*. Everyone says what they mean, feelings are stated by the people having them,
and the scene resolves what it raised. The repair is not to make lines cryptic. It is to give each
speaker something they will not say, and then let it leak.

**Before the exchange, write two lines for each speaker:**

```
wants:      what they are asking this conversation for
won't say:  the thing they will not put in words, and why not
```

If `won't say` is empty for both, the scene has no subtext available and does not need any — a
clerk refusing a permit is allowed to just refuse it. If it is empty for *every* scene in a
chapter, the chapter is a briefing.

**Four techniques.** At least one exchange per scene runs on one of them.

| technique | how it works | example |
|---|---|---|
| **Contradicting action** | the words say one thing, the body says the other. The reader believes the body | *"I'm not worried."* She checked the door again. |
| **Evasion** | answering a different question, or answering with a question. Where they dodge is the information | *"Where were you Tuesday?" — "Is that what he told you I was doing?"* |
| **Irony** | saying the opposite, meant to be caught. Needs a relationship that can carry it, or it reads as confusion | *"By all means, take your time."* |
| **The displaced object** | the conversation is nominally about the permit, the horse, the weather. It is about the marriage | Two people discuss a leaking roof for a page and one of them is deciding whether to leave |

**Rules of use.** Subtext costs the reader attention, so it is spent, not sprinkled.

- **Never gloss it.** The narration does not explain what was really meant. If the reader might
  miss it, add a beat — a look, a pause, an object picked up — not a sentence of interpretation.
  A glossed subtext is worse than none, because it teaches the reader to stop working.
- **Somebody in the room can be wrong about it.** The best version of the technique is a listener
  who takes the surface meaning while the reader takes the real one.
- **The direct statement is the payoff.** When a character finally says the thing plainly, it lands
  because three scenes went around it. That is what the reserve is *for*. A book with no direct
  statements is as flat as a book with nothing but.
- **Articulacy sets the shape, not the presence.** A low-articulacy character has subtext too;
  theirs is a changed subject and a hand on a doorframe, not an epigram.

## Self-check

- [ ] Spoken dialogue is 25–40% of the chapter's words; under 10% is a defect, not a style
- [ ] At least one exchange per scene runs on subtext, and the narration did not explain it
- [ ] Every speaker in a loaded scene has a `won't say`
- [ ] The share counts `"…"` only — thought and meta are not dialogue
- [ ] No character stood in a scene without speaking while being narrated about
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
