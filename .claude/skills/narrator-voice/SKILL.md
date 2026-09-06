---
name: narrator-voice
description: Establish and hold the narrating voice — person, tense, narrative distance, interiority, filtering, and the four text channels (speech, direct thought, meta, and unmarked free indirect discourse) — so the novel sounds like one book across hundreds of chapters. Use when setting up a novel, when drafting any chapter, when marking thought or system text, and when the prose starts feeling generic or inconsistent.
---

# narrator-voice

The narrator is a character even when unnamed. `novel.md` → `narration:` declares its
parameters; this skill turns them into sentences and keeps them stable for 300 chapters.

---

## What lives in `references/`

| file | open it when |
|---|---|
| `references/filtering.md` | the prose feels remote or second-hand, opening lines are going flat, or an arc has closed and the voice needs checking for drift |

The four channels stay here: they are mechanical, they are checked every chapter, and `sw lint`
reads the marks from `channels:` in `novel.md`.

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

**Interiority is the POV character's, not the narrator's.** Every POV-eligible character has a
**thought unit** — images, words, numbers, bodies, rules, people, money — recorded in
`bible/cast/_voices.md` §3, along with their thought speed and what they do facing an unknown
(`voice-separation/references/channels.md`). Two POV characters who think in the same unit narrate identically however
different their dialogue is, and that is the head-hopping smell readers notice without being able
to name it.

**Everyone else thinks through their first move.** Non-POV characters get no interiority at all —
their minds reach the page through what they reach for, look at, or say first when the situation
changes. Three people enter the same room; one checks the door, one checks the faces, one checks
the exit they came in by. Three minds, one POV, no head-hopping.

## The four channels

**This skill is the authority on how the four kinds of text are marked.** The per-novel house style
lives in `bible/lexicon.md` §House style and mirrors `novel.md` → `channels:`; change them
together or not at all. `dialogue-voice` writes the speech; `litrpg-system` and `world-texture`
write into the meta channel; this section decides what each looks like on the page.

| channel | mark | carries | budget |
|---|---|---|---|
| Speech | `"…"` | anything said aloud | 25–40% of the chapter (`dialogue-voice`) |
| Direct thought | `'…'` | the verbatim sentence a character says to themselves and not aloud | **1–3 per chapter**, at decisions |
| Meta | `[…]` | system interfaces, status deltas, in-world documents, signs, letters, narrative adjustments | as needed; never two consecutive |
| Free indirect | *unmarked* | **the default carrier of interiority** | unlimited |

### Free indirect is the default, and it is not marked

This is the rule that keeps the other three from ruining the prose. Interiority reaches the page
*inside the narration*, in the character's idiom, with no typography at all:

> She wasn't looking for anything to take. That was the part she'd have had trouble explaining, if
> anyone had asked, which nobody had, yet.

That is thought. It wears no marks, it needs none, and at `close` or `deep` distance it is
indistinguishable from the narration by design — that seamlessness *is* the effect. Everything in
§Interiority above describes this channel.

This is why **`channels.free_indirect`** is set to `unmarked` in `novel.md` and stays there. The
other three keys name a mark; this one names its absence, and it is in the config so that the
absence is a declared decision rather than an omission. A novel that gives it a mark has three
thought channels and no default.

### Direct thought is the exception, and it is budgeted

`'…'` is for the one sentence a character puts to themselves in words — usually at a decision,
usually when the free indirect voice would blur something that needs to be sharp:

> The clerk turned the form around and tapped the empty line. Guardian. She looked at it for
> longer than a four-year-old should need to look at a word.
> *'Don't help them fill it in.'*
> "I don't know," she said.

**One to three per chapter.** Past that, the narrator stops being a mind and becomes a comic strip
with thought bubbles, and the effect inverts: marked thought is emphatic *because* it is rare.

Note the interaction with distance. At **deep** distance direct thought is nearly redundant — the
prose already thinks in the character's voice — so it is used sparingly and lands hard. At
**cool** or **medium** distance it is the only interiority available, and even then the budget
holds; a cool narrator that suddenly quotes three thoughts a page has changed books.

### The three collision rules

`python3 scripts/sw.py lint novels/<slug> -c <n>` enforces all three mechanically: it strips
speech spans before counting thought, so a nested quotation can never register as thought; it
requires a thought mark to open at a word boundary and close before punctuation, so `don't` and
`the boys' room` cannot match; and it reports any mark that opens and never closes. It also
counts the direct-thought budget and flags a chapter over three.


Without these the convention breaks on contact with ordinary English.

1. **Apostrophes are not thought marks.** A thought opens at a word boundary and closes before
   punctuation or whitespace. `don't`, `she'd`, `the boys' room`, `'90s` are never thought. Any
   tool counting thought must encode this, or it will report every contraction as interiority.
   The converse matters just as much and is easy to miss: **a thought may contain contractions**,
   and most will — `'Start with what you're sure of.'` is one thought, not a broken pair. What
   distinguishes them is position, not the character: an apostrophe with a letter on both sides is
   a contraction, wherever it appears. A thought that opens and never closes on the same line is
   the error to look for, and it is usually a possessive that swallowed the closing mark.
2. **A `'…'` inside a `"…"` pair is an ordinary nested quotation.** `"He actually said 'no
   comment' to my face."` A `'…'` outside any `"…"` pair is thought. Position disambiguates and
   no third mark is introduced.
3. **Nothing else is markup.** No bold, headings, lists or links in the prose body. `*italic*` has
   exactly one job, declared in `lexicon.md` — foreign words on first use, *or* a word used as an
   object, *or* stress. Not two. Italics that mean three things mean nothing, and the commonest
   way a draft loses its emphasis is by spending it everywhere.

### Thought in non-POV heads

**None.** The channel rules do not create an exception to §Interiority: a non-POV character never
gets a `'…'`, because that would be head-hopping with punctuation on it. Their minds still reach
the page through the first move.

## Self-check

- [ ] Person and tense unchanged from `novel.md`, and unchanged within the chapter
- [ ] No knowledge on the page that the POV character could not have
- [ ] Filter verbs removed except where perceiving is the point
- [ ] Distance tightens at the chapter's hottest moment
- [ ] Metaphors drawn from the narrator's own world — and from *this* POV's thought unit
- [ ] Interiority is decision and reaction, not transcript
- [ ] Non-POV characters shown through first moves, never through interiority
- [ ] The three voice rules hold
- [ ] Free indirect discourse carries the interiority; it is unmarked
- [ ] Direct thought `'…'` used 1–3 times, at decisions, and never tagged with *she thought*
- [ ] No non-POV character got a direct thought
- [ ] No apostrophe read as a thought mark; no nested speech-quotation read as thought
- [ ] Meta `[…]` matches the `lexicon.md` format; italics do their one declared job
- [ ] Nothing else in the prose body is markup
