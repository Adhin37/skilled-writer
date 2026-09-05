---
name: story-bible
description: Build and maintain the world bible and lexicon — setting, factions, social order, scarcity, rules and naming conventions — at the minimum size that keeps a long serial consistent. Use when starting a novel, when a chapter introduces a durable new fact, and when the world starts contradicting itself.
---

# story-bible

`bible/world.md` and `bible/lexicon.md`. The bible's job is **consistency, not completeness.**

**Scope.** This skill owns *what is true and where things are*: the constraint, the power
question, locations, factions, scarcity, rules, names. It does **not** own the society layer —
labour, money, law, knowledge, belief, mobility and what the power system did to daily life go in
`bible/society.md` via `social-fabric`. It does not own delivery either: how any of this reaches
the page, and how much of it may, belongs to `world-texture`. Write each fact once, in one file.

The failure mode at setup is a 6,000-word gazetteer of nations and calendars, none of which
affects a sentence. The failure mode mid-serial is the opposite: facts invented in chapters and
never recorded, contradicted forty chapters later.

---

## The inclusion test

A fact belongs in the bible only if it satisfies one:

1. A scene could **contradict** it.
2. It **constrains** what a character can do.
3. It will be **referenced more than once**.
4. It is a **name or spelling**.

"The empire has fourteen provinces" fails all four unless the provinces do something. Cut it.

## Building at `novel-init`

Write only what arc 1 needs, plus the constraints you have already committed to. Target: 800–1,500
words total. It grows as the story does.

**Order of operations:**

1. **The constraint.** One sentence: what makes life in this world hard. Everything else hangs
   here. *Water is owned. Magic is a debt. The ship cannot turn around.*
2. **The power question.** Who has power, what it is made of (land, violence, information,
   capital, magic), and how an ordinary person gets hurt by it. Headline only — the machinery
   underneath it is `social-fabric`'s, and runs after the power system exists.
3. **Three scarcities.** What is scarce is what plots are made of. Name three; at least one
   should be non-material — reputation, safe passage, a name in good standing. Scarcity is the
   hinge between this file and `society.md`: what is scarce decides who works, who pays and who
   is excluded.
4. **The MC's position** in that order, and what it costs them daily. This is where premise
   becomes story.
5. **Three or four locations** that arc 1 uses, each with a **sensory signature**: the two
   details that identify it instantly, at least one of them non-visual. Reuse them at every visit —
   that repetition is how a reader learns a place, and it costs nothing (`world-texture` §4).
6. **Two or three factions**, each with wants / method / fears / posture toward the MC. No faction
   is uniformly anything, and none maps onto a real-world ethnic or national group (`bias-guard`).
7. **Numbered rules of the world** — the hard constraints the story may never break. Five is
   plenty. Numbering them lets CCS blocks cite them.
8. **Open questions** — deliberate unknowns, recorded so two chapters do not fill them in
   differently.

Then the power system (`power-system`) or the canon file (`fanfic-canon`), whichever applies —
and **then `social-fabric`**, which takes that rule and works out what it did to ordinary life.
That order is not negotiable: society cannot be derived from a rule that does not exist yet.

## The lexicon

Small, boring, and the highest-value file in the repo. The single most common serial defect is the
same thing named three ways across 200 chapters.

Record: canonical spellings · what a term means in plain English · forms of address, and **when
they change** (a switch from "my lord" to a first name is a whole story beat — log it in
`state/growth.md` when it happens) · units and currency · house style decisions (numbers,
interior thought formatting, italics on invented words, chapter title case) · a per-novel banned
word list.

**Consult it before writing any proper noun.** It is cheap and always in the read-set.

## Naming

Names are the most visible worldbuilding and the easiest to get wrong.

- **Internal consistency over prettiness.** Names from one culture should share sound patterns.
  Two syllables here, hard consonants there — a reader will absorb the rule without noticing it,
  and then a foreign name will *feel* foreign without being explained.
- **Distinguishable on a phone.** No two significant characters sharing an initial, a length and
  a rhythm. Readers skim; Kaelen and Kaevan will merge.
- **Pronounceable.** A name a reader cannot say is a name they stop reading. Apostrophes are a tax.
- **Say what it does.** Prefer terms that are transparent to an English reader over invented
  vocabulary that must be glossed. Invent only where the concept has no English equivalent.
- **Cap the invented-word budget** at roughly one new term per chapter early on, fewer later.

## Exposition discipline

The bible exists so that you can *avoid* explaining. Almost everything in it should reach the
reader as consequence.

| never | instead |
|---|---|
| A paragraph explaining a faction's history | a character acts on a grudge, and the reader infers the history |
| An in-world encyclopaedia entry as a chapter opening | a rule bites someone in a scene |
| Two characters explaining their shared world to each other | give the ignorance to someone who genuinely has it |
| A rank/tier recital | show what a rank buys and what it costs |

The rule: **the reader needs to know a thing only in the sentence before it matters.** Introduce
constraints when they bind, not when they are defined. `world-texture` owns the mechanics of this
— the four delivery channels and the per-chapter description budget.

## Maintenance

- After every chapter, `continuity-summary` moves durable `set>` facts into the bible. Do not
  defer this; an unrecorded fact is a future contradiction.
- When a chapter contradicts the bible: decide which is right. Usually the chapter (it is on the
  page and the reader has seen it) — then amend the bible and check whether earlier chapters need
  a note. Record the decision; do not silently keep both.
- When a bible section has never been referenced in 50 chapters, it is either dead weight or
  material you have forgotten to use. Decide which.

## Genre notes

**Fantasy.** The power system is the load-bearing element — see `power-system`. Social order is
second: who is allowed to use power, and what happens to those who use it anyway.

**Scifi.** The bible's centre is the *one* technology the story argues about, and its second-order
social effects. See `tech-plausibility`. Resist building three centuries of history.

**Fanfic.** The bible records only what this story adds or changes; canon lives in `bible/canon.md`.
Do not restate the source's setting — record the divergence and its consequences.

## Self-check

- [ ] Every entry passes the inclusion test
- [ ] The world's constraint is stated in one sentence
- [ ] Three scarcities named
- [ ] Every location has a sensory signature, at least one sense of it non-visual
- [ ] No faction is uniformly good or evil; none maps onto a real-world group
- [ ] Every invented term is in the lexicon
- [ ] Nothing in the bible has been dumped as exposition into a chapter
- [ ] `society.md` exists and the central rule has been propagated through it (`social-fabric`)
- [ ] No social-layer material duplicated between `world.md` and `society.md`
