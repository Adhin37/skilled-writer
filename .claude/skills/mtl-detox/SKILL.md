---
name: mtl-detox
description: Strip the prose artifacts and structural clichés inherited from machine-translated serialized fiction — stock phrases, crowd-reaction blocks, the face-slap loop, rank recitals, cannon-fodder antagonists. Runs on every chapter inside revision-pass, and applies while drafting.
---

# mtl-detox

Most serialized fiction in the training corpus arrived through machine translation from Chinese
web platforms. That corpus supplies the format's genuine strengths — momentum, hooks, visible
progression, generous chapter counts — and also a set of defects that read as "AI wrote this" to
an English-language audience.

This skill keeps the engine and removes the residue. It is **not** a judgement about a culture or
its literature: the defects here are artifacts of *bulk machine translation and web-serial
incentive structures*, not of Chinese fiction, which at its best has none of them. What we are
stripping is the translationese and the treadmill.

Run on every chapter. Not optional.

---

## Part 1 — Prose artifacts

### Banned phrases

Do not write these. If they appear in a draft, rewrite the sentence, do not swap a synonym.

| banned | why | instead |
|---|---|---|
| "his expression changed drastically" | reports a face instead of showing a reaction | give the specific movement, or the thing he does next |
| "as expected of the young master" | crowd flattery as narration | delete; if someone is impressed, let them act on it |
| "unexpectedly" / "to his surprise" | announces the surprise before delivering it | just deliver the fact; surprise is the reader's job |
| "in the next instant" / "in the next moment" | filler transition | start the next action |
| "little did he know" | omniscient intrusion | dramatic irony belongs in structure, not asides |
| "couldn't help but" | hedges every action | he did it |
| "a trace of X flashed through his eyes" | the corpus's universal emotion beat | one concrete physical detail, or nothing |
| "trash!" / "you dare!" / "court death!" / "do you know who I am?" | stock antagonist noise | let the antagonist say something that costs him |
| "seemed to" / "as if" stacked | evasive; refuses to commit to what is true | commit |
| "at this moment" / "at that time" | translated temporal filler | cut entirely |
| "not simple" (meaning formidable) | translationese | say what makes them formidable |
| "his heart trembled / his scalp went numb" | body-cliché catalogue | a specific, non-standard physical fact |
| "how could this be possible?!" | shock as punctuation | give the character a thought worth having |
| "so-and-so was speechless" | narration standing in for reaction | show what they do with the silence |

### Structural prose habits to remove

- **Rhetorical-question narration.** *Was this really happening? How could a mere outer disciple…?*
  One per ten chapters at most, and only in deep distance where it is genuinely the character's
  thought.
- **Exclamation marks in narration.** None. Dialogue only, and sparingly.
- **Ellipsis as a mood.** Only for a trailing-off voice.
- **Sentence-fragment reaction lines as a rhythm** (*Silence. Complete silence. Absolute
  silence.*) Once in a novel, if earned.
- **Serial adjective stacking** (*the mysterious, ancient, terrifying ruin*). Two adjectives is
  usually one too many. Pick the surprising one.
- **Repeating the same information three ways** in consecutive sentences. Translation-padding
  habit; keep the strongest version.
- **Numbers as awe** (*a hundred thousand kilograms of force!*). Scale means nothing without a
  human referent.
- **Honorific spam.** If everyone is Senior Brother This and Elder That in every line, the
  reader stops parsing names. Use forms of address as `lexicon.md` prescribes and no more.

## Part 2 — Structural clichés

### The face-slap loop

The corpus's core loop: an arrogant nobody insults the MC → the MC reveals superiority → the
nobody grovels or is destroyed → the crowd is astonished. Its problem is not that it is
satisfying; it is that it is **frictionless**, so it must repeat forever, and the story stops.

**Never write it.** Where the material wants a confrontation, use one of these instead:

| replacement | shape |
|---|---|
| **Costly win** | The MC wins and it costs — a resource, an ally, an exposure that matters later. |
| **The opponent is right** | The insult contains a truth the MC has been avoiding. |
| **Escalation, not resolution** | The MC wins the exchange and thereby acquires a real enemy. |
| **Refused fight** | The MC declines, and the reader understands exactly what that cost them. |
| **The crowd doesn't care** | Nobody is astonished. The world is not an audience for the MC. |

### Crowd-reaction blocks

Paragraphs of bystanders narrating how impressive the MC is. Delete on sight. A crowd is
individuals with their own business; if one reacts, give them a name or a specific job and one
line. Never a gasping mass.

### Rank recitals and system exposition

The narrator listing tiers, realms, levels or bloodline grades. Delete. The reader learns a power
system by watching it cost people things. If a rank absolutely must be explained, put it in the
mouth of someone with a reason to be explaining it to someone who genuinely does not know, and
keep it under 60 words. See `power-system`.

### Cannon fodder

Opponents who exist to lose. Every antagonist, down to a street enforcer, wants something legible
and is competent at their own job. The one-scene thug still has a reason to be at that door.

### Other structural habits to drop

- **The treasure/technique escalator** — a stronger artifact every ten chapters, obsoleting the
  last. See `power-system`'s escalation budget: every gain must create a new problem.
- **Sect/academy tournament arcs** as the default mid-book structure. Allowed, but the bracket is
  not a plot; the thing at stake outside the bracket is.
- **The overheard conversation** as an information-delivery mechanism, more than once a novel.
- **The mysterious old man in a ring** and other mentor-in-a-pocket devices that let the MC skip
  the cost of learning.
- **Reincarnation/transmigration foreknowledge used without limit.** If the MC knows the future,
  the future must diverge early and often, or the story has no tension. See `meta-knowledge`,
  and `mc-intel-meter`: knowledge is not intelligence.
- **Foreknowledge that only ever fails** — the opposite error, and the one careful writing falls
  into. An advantage introduced as already-unreliable, whose every appearance is a malfunction,
  is a bait-and-switch on the premise the blurb sold. It works first, legibly, then it costs, then
  it frays (`meta-knowledge` §4).
- **The unanchored opening** — chapters of well-made prose in which the reader cannot tell what
  kind of world this is or, in fanfic, which canon they are in. Not mystery; disorientation. The
  reader has no question to be curious about, only a vague unease (`story-opening` §1).
- **Time-skip training montages** that resolve a difficulty the story just established.

## Part 3 — Detox pass procedure

Run over the drafted chapter:

```bash
python3 scripts/sw.py lint novels/<slug> -c <n>
```

Steps 1-3 are that command: it holds the whole banned list above, counts exclamation marks and
question marks outside dialogue, and reports each with its line. Steps 4-8 are structural and
are yours — no script can see a crowd-reaction block or price a confrontation. Without Python,
search for each phrase by hand.

1. Search the draft for each banned phrase. Rewrite, don't substitute. The linter finds the
   string; **you** rewrite the sentence, because swapping a synonym is the failure this list
   exists to prevent.
2. Count exclamation marks outside dialogue. Target zero.
3. Count rhetorical questions in narration. Target zero, ceiling one.
4. Find every paragraph describing a group reacting to the POV character. Delete or individuate.
5. Find every passage explaining the power system. Is it in a character's mouth, with a reason,
   under 60 words? If not, cut it.
6. For every confrontation: name what it cost the winner. If nothing, apply a replacement above.
7. For every antagonist present: name what they want and what they are good at. If you cannot,
   fix the character before the sentence.
8. Read the chapter's last 200 words aloud. Translationese hides in the rhythm — flat
   subject-verb-object chains of uniform length. Vary or rewrite.

## Self-check

- [ ] Zero banned phrases
- [ ] Zero narration exclamation marks
- [ ] No crowd-reaction block
- [ ] No rank recital
- [ ] Every confrontation has a cost
- [ ] Every antagonist on the page wants something and is good at something
- [ ] No paragraph says the same thing three ways
