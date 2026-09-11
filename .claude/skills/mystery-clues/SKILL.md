---
name: mystery-clues
description: Optional (default off). Run fair-play mystery mechanics - clue planting, red herrings, the knowledge gap, reveal construction. Use only while this skill is enabled.
metadata:
  type: skill
  tier: optional
  when: optional.mystery-clues == on
  owns: [clue-ledger, fair-play]
---

# mystery-clues

**Gate.** Applies only if `novel.md` → `optional.mystery-clues` is `on`.

Fair play means: **the reader had everything they needed.** The pleasure is not being fooled; it
is being fooled fairly and being able to see, afterwards, exactly where the answer was.

---

## The clue ledger

Keep a section in `state/threads.md`:

| id | clue | planted ch | what it means | how it's disguised | reader has it | MC has it |
|---|---|---|---|---|---|---|

Track the two knowledge columns separately. The gap between them *is* the mystery's tension, and
it is also what the CCS `kno>` line exists for.

## Planting

**Disguise by function, not by obscurity.** A clue is hidden by making it do another job —
characterisation, humour, atmosphere, a transaction — so the reader registers it without
weighting it. A clue nobody notices is not fair play; it is a clue the reader skimmed.

**Three plants, decreasing subtlety** (see `plot-threads`): ambient → noticed and dismissed →
loaded and unexplained.

**Plant the decisive clue early.** Ideally in the first third, when the reader is not yet
suspicious. The best clues are ones the reader already accepted as true.

**One clue, two readings.** The strongest device in the form: a fact that is fully explained by
the innocent interpretation and fully explained by the true one.

## Red herrings

- A red herring must have an **innocent explanation that is eventually given**. A misdirection
  never accounted for is a hole.
- It must arise from a character's real behaviour — they were lying, but about something else.
  Everyone in a good mystery is concealing something; almost none of it is the crime.
- **Never lie to the reader in narration.** The POV character may be wrong; the prose may not
  assert something false. Omission and misinterpretation are fair; false statement is not.

## The knowledge gap

Decide, per chapter, which mode you are in:

| mode | reader vs. MC | effect |
|---|---|---|
| **behind** | reader knows less | curiosity — the standard detective mode |
| **level** | same information | participation — the reader solves alongside |
| **ahead** | reader knows more | dread — they watch the MC walk into it |

Rotate deliberately. A whole novel in `behind` is exhausting; a whole novel in `ahead` has no
mystery. Record the mode in the chapter plan row.

**`ahead` interacts with `mc-intel-meter`:** if the reader knows something the MC does not, the MC
must not have had access to it. Check the CCS `kno>` line. An MC who fails to notice what the
reader was shown *in their presence* is an idiot-ball violation, and the fix is to change the
information, never the intelligence.

## The reveal

- **Dramatise it.** The answer should arrive as something that happens *to* someone, not as a
  drawing-room recitation. If a character must explain, they should be explaining under pressure,
  to someone who will act on it.
- **Cite two or three plants, briefly** — enough for the reader to feel the click, not a full
  audit. Trust them.
- **Never explain the foreshadowing.** No "she remembered the old man's words."
- **The answer must cost.** A solution that changes nothing is trivia. Knowing should force a
  decision the MC does not want to make.
- **Close large, open small.** The answer to the big question raises a sharper one.

## Self-check

- [ ] Every clue in the ledger with both knowledge columns tracked
- [ ] The decisive clue was planted at least twice before the reveal
- [ ] Every red herring has an innocent explanation that gets given
- [ ] No false statement in narration
- [ ] The chapter's knowledge mode is deliberate and rotated
- [ ] No `ahead` chapter requires the MC to miss something they witnessed
- [ ] Any reveal costs someone something
