---
name: social-perception
description: Pin how well each character reads other people, and make the gap between that and their intelligence do work. Use when designing a character, when anyone judges anyone, and inside revision-pass.
metadata:
  type: skill
  tier: character
  when: always
  owns: [eq-tier, emotional-signature, misread]
---

# social-perception

`novel.md` → `mc.eq_tier` declares how well the MC reads people; `bible/cast/_voices.md` carries
an `eq` column for everyone else. This skill makes those numbers load-bearing, the same way
`mc-intel-meter` makes `mc.intel_tier` load-bearing.

It exists because the corpus writes one kind of mind. A protagonist is clever, and cleverness is
allowed to cover everything: he out-thinks the schemer *and* knows what his mother is not saying
*and* reads the room on arrival. That character has no interior weather and no reason to be
surprised by anyone, which removes every relationship plot in the book at a stroke.

**Intelligence and social perception are different axes.** The gap between them is where a
character lives.

---

## What lives in `references/`

| file | open it when |
|---|---|
| `references/reading-people.md` | writing the moment somebody judges somebody — the observation ladder, what each tier is allowed to conclude, and how a misread is written so the reader sees past it |
| `references/draft-card.md` | never, by you. `write-chapter` Phase A opens it |
| `references/audit-card.md` | never, by you. `revision-pass` Pass 3b opens it |

## 1. The tiers

| tier | name | what they get from a face | what they do with it | error profile |
|---|---|---|---|---|
| 1 | **Blunt** | the stated content, and strong signals only — shouting, tears | takes people at their word, and is hurt when the word was not the meaning | misses that anything was happening at all |
| 2 | **Literal** | notices the mismatch, cannot name it | knows something is wrong; guesses at the cause and usually guesses self-referentially | assumes they are the subject of other people's moods |
| 3 | **Competent** | reads mood, hierarchy and the obvious withholding | adjusts. Manages a room without thinking about it | over-trusts a first read, and does not revisit it |
| 4 | **Acute** | reads intent, the shape of what is not being said, who in the room is afraid | can steer a conversation to where they want it | models everyone accurately except the people they need something from |
| 5 | **Uncanny** | reads the private thing the person has not admitted to themselves | can be unbearable to sit near | knows what everyone feels and has no idea what to do about their own |

**The error profile is not optional.** It is what makes the tier survive contact with a plot. A
tier-5 reader who is also wise about their own life is not a character, they are a device.

## 2. The gap rule

Set `eq` independently of `intel`. **The interesting characters are the ones where the two
disagree**, and a cast where every row has `intel == eq` has one kind of mind in it wearing
different names.

| shape | what it produces |
|---|---|
| high intel, low eq | builds a correct plan that nobody will execute, because he never noticed they were frightened |
| low intel, high eq | two steps behind on the facts and the first to know who is lying |
| high both | needs an opponent who is also high both, or a problem that is not about people |
| low both | not stupid — just outside the conversation everyone else is having. Sympathetic and very usable |

`mc-intel-meter` owns the intel ladder, the inference budget, and the three legal ways a smart MC
fails. This skill adds the fourth: **the misread** (§4).

## 3. Emotional signature — what a feeling looks like on this person

The rule against naming emotions is `prose-quality`'s, and it leaves a vacuum: told not to write
*she was angry*, a drafter reaches for the nearest body and produces the nodding, sighing,
jaw-clenching set that belongs to everyone and identifies nobody (`voice-separation` owns that
ban). The positive rule is here.

Every tier-A and tier-B character gets **four entries**, in their profile:

```
fear      goes quiet and starts tidying. Answers questions that were not asked
anger     over-polite. Uses your full name
grief     works. Will not stop working, and is bad at it
relief    talks too much, then is embarrassed about it
```

Three requirements:

- **They are not universal.** If two characters share a signature, one of them is unwritten.
  Fear that looks like stillness in one person looks like jokes in another and neither is the
  default.
- **They are legible from outside.** This is what another character sees, not what the feeling
  is. The POV character's interiority is `narrator-voice`'s channel; this is the body somebody
  else has to interpret.
- **They are wrong sometimes.** The same behaviour has more than one cause, which is what makes
  §4 possible at all.

## 4. The misread — the fourth legal failure

A character may fail because they read another person correctly-shaped and wrong. This is a
legitimate way for an intelligent protagonist to lose, and it is the one the corpus never uses.

For it to be fair rather than arbitrary, all four must hold:

1. **The signal was on the page**, in the scene, available to the reader.
2. **The reading was reasonable** — it is the interpretation their tier and their history would
   produce, not a lapse.
3. **The true cause was also on the page**, in something the reader saw and the character did
   not weight.
4. **It costs.** A misread that costs nothing is a texture beat, not a failure.

The reader's pleasure here is the same as in a fair-play mystery: being able to see, afterwards,
exactly where the other reading was. A misread that only the narrator could have caught is the
idiot ball wearing a new coat, and `mc-intel-meter`'s floor still applies — nobody forgets what
the reader watched them learn.

## 5. What a tier may conclude

**Nobody reads a face perfectly, at any tier.** Bodies are ambiguous; the same stillness is fear,
calculation, or a person who is simply cold. What rises with tier is not accuracy but **the
quality of the question** — a tier-4 observer notices that the stillness wants explaining, and is
still guessing at why.

So: a character states a *reading*, never a fact about another mind. *She had decided something
before she came in* is a reading. *She had decided to refuse him* is narration that has left this
character's head, and in a limited POV it is a viewpoint breach (`pov-switch`, `narrator-voice`).

The ladder from observation to conclusion, per tier, with worked examples:
`references/reading-people.md`.

## 6. Where it meets the other character skills

| this skill owns | the neighbour owns |
|---|---|
| how well somebody reads people, and what they conclude | `mc-intel-meter` — how well they reason, and the intel tier itself |
| who **catches** what a line is doing | `dialogue-voice` — subtext, what the line carries under what it says |
| what a feeling looks like on a given person | `voice-separation` — the ban on the shared gesture set, and the axes a character may not drift across |
| the misread as a failure lever | `conflict-engine` — what the failure then costs |
| a character's read of another | `character-profile` — their relationship, history and standing |

A character's `eq` sits in the voice matrix beside `intel` because its defects are cast-wide:
you cannot see that everyone in the book reads people equally well by reading one profile.
`sw cast` checks the pair.

## Self-check

- [ ] `mc.eq_tier` is set, and it is not simply equal to `mc.intel_tier`
- [ ] Every tier-A and tier-B character has an `eq` value in `bible/cast/_voices.md`
- [ ] At least one character reads people **better** than the MC, and one worse
- [ ] No two recurring characters share `intel` + `eq`
- [ ] Each has four emotional-signature entries, and no two characters share one
- [ ] Nobody stated another character's interior state as fact
- [ ] Every conclusion about a person is inside the reader's reach — the signal was on the page
- [ ] Any misread this chapter satisfies all four conditions in §4
- [ ] No character was made socially blind purely to let the MC notice something
