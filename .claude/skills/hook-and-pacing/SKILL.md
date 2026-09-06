---
name: hook-and-pacing
description: Control serial pacing — chapter length, opening lines, chapter-end hooks, arc rhythm and release cadence — so readers come back for the next chapter. Use when drafting any chapter's opening and closing, and when planning arc temperature.
---

# hook-and-pacing

Serialized fiction is read one chapter at a time, days apart, on a phone, by someone who is
following six other stories. Every chapter has to re-earn the reader. This skill is about the two
positions that do that work: the first 100 words and the last 100.

---

## What lives in `references/`

| file | open it when |
|---|---|
| `references/arc-rhythm.md` | planning an arc's temperature, or the story is reading as relentless or as flat over a stretch of chapters |

## Chapter length is not a quality metric

**A chapter is judged by what it delivers, not by how long it is.** The gate is
`revision-pass` Pass 9 — want, friction, **change**, cost, next — and this skill has nothing to
add to it. `novel.md` → `chapters.length_band` is a printer's note: the range outside which a
chapter is worth a second look, and nothing more.

This is a correction, and the history is worth knowing because the failure repeats. This skill
used to carry a target with tolerances. Chapters then clustered against the floor. The tolerance
was tightened to ±15% of target; chapters clustered against the new implied floor, and one landed
on the declared minimum **to the word**. A number that gates publication gets optimised, and prose
optimised toward a length is padded or truncated prose. There is no version of this rule that
does not get gamed, so there is no rule.

What the band is still good for:

- Under ~1,200 words a chapter reads as a fragment — usually a real signal that the material was
  split in the wrong place, not that it needs padding.
- Over ~3,000 it gets abandoned mid-chapter on a commute, and a chapter abandoned halfway is worse
  than one never started.
- **Consistency is a reader expectation, not a target.** Readers form a sense of your chapter size
  from the first ten and feel short-changed by sudden deviation. A chapter at half your usual size
  needs a reason; it does not need filler.
- Higher release cadence supports shorter chapters. Weekly releases need more substance per
  chapter and a stronger recap clause.

**Never pad, and never trim to a number.** If the chapter's material ends, it ends. If it runs
long and every scene is delivering, ship it long. The only length question worth asking is the
skim test (`references/arc-rhythm.md`): *would a reader lose anything by skipping this?*

**What to do when a chapter comes out short.** Not padding — diagnosis. A short chapter almost
always means one of: the turn happened offstage, the cost was skipped, or a scene ended at its
first obstacle instead of its consequence. Fix the delivery and the length follows. Pulling
material forward from the next chapter is legitimate; adding sentences is not.

## Openings

The reader is deciding whether to keep going. You have two sentences.

**Never open with:** weather · waking up · a recap paragraph · an in-world encyclopaedia entry ·
a rank or status recital · a date/time stamp alone · a character reflecting on the last chapter.

**Openings that work:**

| type | shape |
|---|---|
| Mid-argument | a line of dialogue already in conflict |
| Action in progress | the verb is already happening |
| Wrong detail | something present that should not be, stated flatly |
| Declarative with a story inside it | *The coat did not fit and she wore it anyway.* |
| Consequence first | open on the aftermath, fill in backwards inside the scene |
| Contradiction of the last hook | the hook promised a fight; open on the two of them eating |

**Re-anchoring.** Readers arrive days later. Carry the recap in **one clause inside a sentence
doing other work** — never a paragraph, never "as you'll recall". If a chapter genuinely needs
more context than one clause, the previous chapter's hook was unclear.

## Hooks

`chapters.hook_required: true` means every chapter ends on one. A hook is not a cliffhanger — a
sword swinging mid-air every chapter exhausts readers and cheapens the real ones.

A hook is **an unresolved pressure the reader wants relieved.**

| hook type | what it does | frequency |
|---|---|---|
| **Revelation** | new information reframes what came before | often |
| **Arrival** | someone or something appears | often |
| **Decision** | the MC chooses, and the reader wants the consequence | often |
| **Question** | a fact that does not fit | often |
| **Threat** | a clock starts, or an intention is stated | moderate |
| **Reversal** | what the reader thought was true is not | occasional |
| **Cliffhanger** | physical peril, unresolved | **max once per 8–10 chapters** |
| **Quiet** | a line that lands emotionally; no question at all | once per arc, after a heavy chapter |

**Construction.**

1. End on the **last strong beat**, not on the wind-down after it. The most common hook failure
   is three paragraphs past the right stopping point.
2. Put the hook in the **final sentence or short paragraph**, alone on the line.
3. Make it **concrete**. "Something was wrong" is not a hook. "Her father's name was the first
   line in the ledger" is.
4. **Do not answer it in the first line of the next chapter.** Let it breathe for a page.
5. **Rotate types.** Three revelation hooks in a row and the reader stops feeling them.
6. The **arc-ending hook** is the strongest in the arc — usually a reversal or a threat that
   reframes the next 25 chapters.

**Hook honesty.** A hook that implies a fight and delivers a conversation is a bait. It works once
and costs trust. Deliver the thing you implied, or deliver something better and more surprising —
never something smaller.

## Pacing within a chapter

| register | sentence & paragraph shape |
|---|---|
| fast | short sentences, short paragraphs, dialogue with few beats, cuts between actions |
| medium | mixed lengths, action beats between exchanges, one grounding detail per paragraph |
| slow | longer subordinated sentences, interiority, sensory detail, silence given room |

Vary it *within* the chapter, not just between chapters. A 2,000-word chapter at one speed is
monotonous whatever that speed is. The standard shape: medium open → fast through the turn →
slow for the follow-through → fast for the hook.

## Self-check

- [ ] Opening does not use a banned pattern; it earns the second sentence
- [ ] Re-anchoring is one clause, not a paragraph
- [ ] The chapter ends on its last strong beat, not after it
- [ ] The hook is concrete and in the final sentence or paragraph
- [ ] Hook type differs from the previous two chapters
- [ ] No cliffhanger if one fired within the last 8 chapters
- [ ] Pace varies within the chapter
- [ ] The chapter passes the skim test
- [ ] The chapter delivers a **change** — `revision-pass` Pass 9, not a word count
- [ ] Nothing was padded, and nothing was trimmed, to reach a number
- [ ] If the chapter is far outside `length_band`, that was a decision and not an accident
