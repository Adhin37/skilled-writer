---
name: hook-and-pacing
description: Control serial pacing — chapter length, opening lines, chapter-end hooks, arc rhythm and release cadence — so readers come back for the next chapter. Use when drafting any chapter's opening and closing, and when planning arc temperature.
---

# hook-and-pacing

Serialized fiction is read one chapter at a time, days apart, on a phone, by someone who is
following six other stories. Every chapter has to re-earn the reader. This skill is about the two
positions that do that work: the first 100 words and the last 100.

---

## Chapter length

Set in `novel.md` → `chapters:`. Platform default: **~2,000 words**, floor 1,600, ceiling 2,600.

- **Consistency matters more than the number.** Readers form an expectation from your first ten
  chapters and feel short-changed by deviation.
- Under 1,200 reads as a fragment. Over 3,000 gets abandoned mid-chapter on a commute — and a
  chapter abandoned mid-way is worse than one not started.
- Higher release cadence supports shorter chapters. Weekly releases need more substance per
  chapter and a stronger recap clause.
- **`target_words` is the target; the floor and ceiling are tolerances, not goals.** Aim for
  `target_words` ±15%. A run of chapters all landing within a few dozen words of `min_words` is
  not consistency — it is the target being quietly ignored, and readers who were promised ~2,000
  words are getting a fifth less book per chapter. Check the trend across the last five chapters,
  not just the current one: the defect is invisible in any single chapter that is technically
  "in range".
- **Never pad to a word count.** If the chapter's material ends at 1,500 words, either pull
  material forward from the next chapter or ship at 1,500. Padding is visible and it is the
  fastest way to train readers to skim.

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

## Pacing across an arc

Use the arc rhythm table in `chapter-plan`. The load-bearing insight: the **cool stretch after
the midpoint is not optional**. It is what gives the climax somewhere to rise from. But cool
chapters still have goals, turns and costs — cool means lower temperature, never lower stakes.

**The skim test.** If a reader could skip a chapter and lose nothing, the chapter is filler. For
each chapter, name the one thing a reader would miss. If you cannot, merge it with its neighbour.

## Serial-specific practices

- **Front-load the promise.** Chapters 1–3 must establish the MC's want, the world's constraint,
  and the tone. Readers decide by chapter 3, sometimes by chapter 1.
- **Chapter 1 is not a prologue.** Prologues are skipped. If the prologue material matters, it is
  chapter 1; if it does not, cut it.
- **Batch endings.** If releasing several chapters at once, the last of the batch carries the
  strongest hook; interior chapters can end softer.
- **Arc breaks are drop-off points.** The end of an arc is where readers decide whether to
  continue. Open the next arc's question *before* the current one closes.
- **Titles are pacing too.** The chapter list is read as a scroll; a run of flat titles reads as a
  flat stretch of story. See `chapter-plan`.

## Self-check

- [ ] Opening does not use a banned pattern; it earns the second sentence
- [ ] Re-anchoring is one clause, not a paragraph
- [ ] The chapter ends on its last strong beat, not after it
- [ ] The hook is concrete and in the final sentence or paragraph
- [ ] Hook type differs from the previous two chapters
- [ ] No cliffhanger if one fired within the last 8 chapters
- [ ] Pace varies within the chapter
- [ ] The chapter passes the skim test
- [ ] Word count within `min_words`–`max_words`, with no padding
- [ ] Word count near `target_words` (±15%), not parked against a bound
- [ ] The last five chapters are not all clustered at the same bound
