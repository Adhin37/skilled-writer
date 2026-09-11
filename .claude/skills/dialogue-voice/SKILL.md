---
name: dialogue-voice
description: Write dialogue that identifies the speaker without tags, from each character's speech fingerprint. Use when writing or revising any line of dialogue.
owns: [speech-fingerprint, dialogue-density, subtext]
---

# dialogue-voice

The tag-removal test: **strip every `said X` from a page of dialogue. If a reader cannot tell who
is speaking, the scene is broken.** This skill is how you pass that test cheaply.

---

## What lives in `references/`

| file | open it when |
|---|---|
| `references/subtext.md` | building a scene between two people who want different things, or a scene is reading as an exchange of facts |
| `references/corpus-anti-patterns.md` | two characters will not separate however hard you push the fingerprints, or the dialogue is reading as machine-translated |

## The layer under this one

The eight fields below are a **surface**. Contractions, a vocabulary tell and a syntax tic applied
to minds that are all as quick and as articulate as the MC produce labelled clones — the reader
can tell the labels apart and still hears one person. Before the fingerprint comes the matrix in
`bible/cast/_voices.md`: **intel, articulacy, wit, heat, turn length** (`voice-separation` §1).

Two rules from that skill bind every scene written here:

- **The MC-contrast rule** and **the three-way clash** — `voice-separation` states both, and
  `sw cast` checks them.

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

**Run the transplant test** before the scene is done — `voice-separation` owns it, including the
rule about which of the two lines gets rewritten.

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
the beat identifies the speaker as well as the line does. Never from the default gesture set
(`voice-separation` owns the list, and `sw lint` sweeps for it): those gestures belong to everyone
and therefore to nobody. A line with no beat beats a line with a generic one.

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

Apply every accumulated voice delta from `state/growth.md` (`character-development` owns them). This is the concrete mechanism by
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

Open `references/spoken-register.md` §Why a cast goes quiet for the diagnostic and the two
structural consequences of a silent cast.

## How it sounds spoken

Share is how *much* the cast speaks. This is whether it sounds spoken.

- **People are interrupted, and interrupt.** A chapter where everyone finishes is a chapter of
  prepared statements.
- **People answer in fragments.** A line needs no subject and verb to be a line.
- **Nobody speaks in their own summary.** An unbroken multi-clause turn explaining a character's
  reasoning is the narrator using their mouth.
- **A turn past ~45 words is a speech, and at most one chapter in five gets one.** Measured per
  turn — every `"…"` span in one paragraph, counted together, because a dialogue tag dropped into
  the middle of a speech changes nothing a listener hears. `sw lint` names each one and quotes its
  opening. A monologue can be the right call — a confession, a verdict, someone who has waited
  years to say it — but it is a decision with a reason, not a default. **Ask who lets them finish
  and why nobody in the room interrupts.**
- **The essay tells.** These four are what a written argument looks like when it is put in quote
  marks, and all four are invisible to share, fragment rate and contraction rate:
  1. **Stacked subordinate clauses** — three or more `because` / `since` / `which` / `and I` limbs
     in one turn, each qualifying the last.
  2. **The rhetorical aside** — a parenthetical inserted for effect (*"and I include grown shinobi
     in that"*). Speech has asides; it does not aim them.
  3. **The epigram close** — a turn landing on a balanced aphorism. Good once a book. A cast where
     everyone does it is one writer talking to themselves in several hats.
  4. **Self-qualification** — *"I would like you to understand that as a compliment before I say
     anything else."* People revise mid-sentence; they do not pre-announce the revision.
- **Under pressure turns get shorter**, unless their `heat` row says otherwise — then hold the row.
- **Dialogue is not the delivery van for exposition.** A line that exists so the reader learns a
  fact is narration in costume.
- **Register is per character.** A cast where nobody says *don't* reads as translated.

`sw lint` prints a **dialogue texture** line per chapter: read it to find where to look, never as
a target. Open `references/spoken-register.md` for the measured failure and the repair table.

## Subtext

Subtext is two people talking about one thing and meaning another, **and both of them knowing
it** — the difference between dialogue that conveys information and dialogue a reader leans into.
Machine-written dialogue fails here by default and in a specific direction: it is
*over-determined*. Everyone says what they mean, feelings are stated by the people having them,
and the scene resolves what it raised. The repair is not to make lines cryptic; it is to give each
speaker something they will not say, and let it leak.

**Before the exchange, two lines for each speaker:**

```
wants:      what they are asking this conversation for
won't say:  the thing they will not put in words, and why not
```

Both empty means the scene has no subtext available and needs none — a clerk refusing a permit is
allowed to just refuse it. Empty for *every* scene in a chapter means the chapter is a briefing.

The five techniques, the rules of use, and the four scenes where subtext is the wrong tool:
**`references/subtext.md`**. Two that are never negotiable — **never gloss it** (if the reader
might miss it, add a beat, not a sentence of interpretation), and **articulacy sets the shape, not
the presence** (a low-articulacy character's subtext is a changed subject and a hand on a
doorframe, not an epigram).

## Self-check

- [ ] Spoken dialogue is 25–40% of the chapter's words; under 10% is a defect, not a style
- [ ] At least one exchange per scene runs on subtext, and the narration did not explain it
- [ ] Every speaker in a loaded scene has a `won't say`
- [ ] The share counts `"…"` only — thought and meta are not dialogue
- [ ] No character stood in a scene without speaking while being narrated about
- [ ] Tags stripped — is every tier-A and tier-B speaker identifiable?
- [ ] The transplant test and the axis spread hold for this scene (`voice-separation`)
- [ ] Turn lengths held; every beat drawn from that character's hands or pressure move
- [ ] **No turn over ~45 words**, or exactly one and you can say who lets them finish and why
- [ ] **No essay tells** — stacked subordinate clauses, aimed asides, epigram closes,
      self-qualification (§How it sounds spoken). Read the longest turn aloud; if you run out
      of breath before the speaker does, it is prose
- [ ] Swap test on the walk-ons — could another extra have this scene with no edit?
- [ ] Does each speaker want something distinct from this conversation?
- [ ] Any line that could belong to anyone? Rewrite it.
- [ ] Voice deltas applied?
- [ ] `said`/`asked` unless a stronger verb genuinely earns its place?
- [ ] No dialogue explaining what both speakers already know?
- [ ] Nobody explained a subject their competence map does not cover?
- [ ] Did anyone say they did not know, defer to someone, or turn out to be wrong?
