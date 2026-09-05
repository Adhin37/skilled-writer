---
name: character-development
description: Move characters along their arc ladders over the course of a serial so that growth is audible in how they speak and choose — not just the MC, but every recurring character, each at their own rate. Use every chapter when writing dialogue or choices, and when planning arcs.
---

# character-development

Characters are not static. In a 300-chapter serial, a supporting character who sounds the same in
chapter 200 as in chapter 20 is dead weight, and readers feel it long before they can name it.

This skill answers one question per chapter: **who is different today, and how would a reader
hear it?**

---

## Who has an arc at all

Development is expensive and not everyone gets it. By cast tier (`character-profile`):

| tier | what they get |
|---|---|
| **A** principal | the full five-rung ladder below |
| **B** supporting | **one shift** per arc — two positions, before and after, with a voice delta |
| **C** walk-on | nothing. They are the same person in both scenes they appear in, and that is correct |
| **D** furniture | nothing |

A tier-C character who "grows" is a tier-B character you haven't promoted yet. If a walk-on
changed, that is the promotion signal — take it or cut the change.

## The ladder

Every tier-A profile carries a five-rung ladder. A rung is **a belief about themselves or
the world**, not a status or a power level.

```
rung 1  the Lie, unexamined            "Debts are paid or you are nothing."
rung 2  the Lie, defended              she argues for it out loud, too hard
rung 3  the Lie, cracked               she acts on it and it costs her someone
rung 4  the Lie, held without belief   she keeps the habit, knows it is a habit
rung 5  the Lie, replaced              a new belief, paid for, with a scar attached
```

Rung 5 is not "healed". It is *changed*, at a price, with the old belief still audible when
they're tired.

## Rate

`development_rate` (1 glacial → 5 volatile) sets chapters-per-rung: ~60 / ~40 / ~25 / ~15 / ~10.
The MC is always 5.

Rate is a budget, not a schedule. A rung advances when its **trigger** fires, not when a counter
expires. Rate governs how *available* a character is to change: a rate-1 character can sit
through the same trigger three times before it takes.

## Triggers — what actually moves a rung

Only four things move a character. Anything else is a mood, not development.

| trigger | shape | example |
|---|---|---|
| **Cost paid** | they acted on the belief and it took something they cannot get back | the loyalty test that killed the friend |
| **Contradiction witnessed** | someone they respect demonstrates the belief is false | the mentor forgives a debt |
| **Failure of the old method** | the thing that always worked stops working | intimidation fails, publicly |
| **Being seen** | someone names the Lie out loud, accurately, at the wrong moment | "You don't want the name back. You want to be owed." |

Plan triggers in `plan/arcs.md` (step 7 of `chapter-plan`). Fire them in chapters. Log them in
`state/growth.md`.

## Voice delta — the part that matters

A rung advance that changes nothing about how a character *sounds* has not happened. When a
character advances, record a **voice delta** in `state/growth.md` and apply it from then on.

Deltas are small, mechanical, and cumulative. Pick one or two per rung:

| channel | rung-1 version | later-rung version |
|---|---|---|
| sentence length | long, qualifying | short, willing to stop |
| hedges | "I think maybe we could" | "We're going." |
| forms of address | "my lord" | the man's first name |
| questions | asks permission | asks for information |
| the word they never said | never says "afraid" | says it once, flatly |
| humour | deflects with a joke | lets a silence sit |
| what they notice | exits, threats | people's hands, what they want |
| who they speak for | "I" | "we", and means it |
| profanity | none | one, precisely placed |

Rule: **a reader who skipped 50 chapters should be able to tell this line is from later.**

The delta is cumulative and irreversible except by regression. Once a character has stopped
saying "my lord", going back to it is a *scene*, not a slip.

### Deltas must not converge the cast

Every channel in that table pushes the same direction — shorter, surer, more direct — which is the
direction of the MC. Applied to a whole cast over 200 chapters, growth quietly merges everyone
into the protagonist, and by the late arcs the book has one voice in it.

**A voice delta may not move a character onto the MC's axes** (`voice-separation` §6). If the
obvious delta would raise a character's articulacy to the MC's level, or hand them the MC's wit,
choose a different one — growth also runs toward *more oblique*, *slower*, *quieter*, *funnier in a
worse way*, *unable to stop explaining*. The single exception is a character whose arc is genuinely
about becoming like the MC: then somebody on the page says so, and it reads as loss or as threat.

**The drift check, once per arc.** Put one recent line from each recurring character side by side.
If the axes have compressed, restore them and log it in §6 of `bible/cast/_voices.md`.

## The other ladder — skills

Beliefs are not the only thing that moves. Characters also **acquire competence**, and that runs on
its own ladder in the skill section of `state/growth.md` (`competence-map` §5). The two are
independent: a character at belief rung 2 can be at cooking stage 3, and progress on one does not
imply progress on the other.

```
stage 0  can't                  does not know what they do not know
stage 1  fails knowingly        can see the gap now — this is progress, write it as progress
stage 2  unreliable             works sometimes; they cannot tell in advance which times
stage 3  competent              works, slowly, with their whole attention
stage 4  fluent                 works while thinking about something else
```

Three rules, and they mirror the belief ladder's:

- **A stage advances from a teacher, a reference, or a failure that cost something** — never from
  elapsed time. Time passing is the montage defect, the skill equivalent of narrating growth.
- **Stage transitions get a scene; the practice between them gets a clause.** The learning rides in
  the margins of chapters about something else. 2 → 3 is the long stretch and where stories cheat.
- **Practice is a cost** (`conflict-engine`): the hours went somewhere, and the chapter says where.

This is not an MC privilege. A supporting character quietly getting good at something across an arc
is one of the cheapest ways to make a serial feel like time is passing.

## Regression

Growth that cannot be lost is not growth. Every profile lists regression conditions — usually:
the original wound is touched, exhaustion, or the return of a person from the rung-1 era.

Regression is **temporary and visible**: the old speech pattern returns for a scene, and both the
character and the reader notice. Log it in `growth.md` as `rung 4 (regressed from 4→3, ch 118)`.
Do not silently reset a ladder.

## The MC

The MC's rate is always 5 and their ladder is the spine of the novel. Additional requirements:

**The pain budget.** The MC must face adversity that costs, on a schedule. Track it in the MC
pain ledger in `state/growth.md`.

| interval | required |
|---|---|
| every chapter | something is spent — time, trust, a resource, a lie told, an option closed |
| every 5 chapters | a real setback: a plan fails for a reason the MC could not have prevented |
| every arc | a permanent loss: a person, a capability, a belief, a place they cannot return to |
| every 2–3 arcs | a loss that is partly the MC's own fault, and that they must live with |

**Adversity must be legible.** The reader should be able to state what it cost, in one sentence,
in concrete terms. "He suffered" is not a cost. "He can never go back to Ashfall, and his sister
is still there" is.

**The relationship requirement.** At least three relationships that change *shape* over the
novel — not just deepen. Ally → creditor. Rival → the only one who understands. Mentor →
someone the MC has outgrown and must stop asking. Log shape changes as rung triggers for both
parties.

**Suffering is not a substitute for change.** An MC who is repeatedly hurt but ends the arc
believing exactly what they believed at the start has had a bad time, not an arc. Every arc ends
with the MC's ladder position stated in the arc digest.

## Per-chapter procedure

Called by `write-chapter`, step 1.

1. Read `state/growth.md` rows for the tier-A and tier-B characters in this chapter. Walk-ons have
   no rows; if one is on the page, read their line in `bible/cast/_extras.md` instead and move on.
2. For each: what rung, what voice delta applies, is their trigger scheduled here?
3. If a trigger fires: write the advance **as a scene beat**, not narration. The character does
   something their rung-1 self would not have done, and someone notices.
4. Apply every accumulated voice delta to their dialogue. This is the step that gets skipped.
5. Check the skill-ladder rows for anyone practising something: does a stage advance this chapter,
   and if so what taught them — a person, a text, or a failure that cost? If not, the practice is
   still a clause on the page, and it still took time from something else.
6. After drafting, update `growth.md`: rung, since-ch, next trigger, voice delta, and any skill
   stage that moved.

## Anti-patterns

| pattern | why it fails | instead |
|---|---|---|
| Narrating growth: "she had grown so much since Ashfall" | tells the reader to feel a change they were not shown | let her make a choice her old self could not |
| Growth by power gain | levels are not beliefs | a new capability creates a new problem; the *problem* moves the rung |
| The training montage | bad at it Tuesday, good at it Friday | the five stages, with the plateau around 2, and a named source for each advance |
| A skill acquired for free | the reader values what was paid for | name what the practice took — hours, a hand, a relationship, the thing they did not do instead |
| The instant epiphany | one speech converts a decade-old belief | crack it, let them defend it anyway, break it later |
| Everyone develops at once | flattens the cast; no contrast | stagger triggers; a rate-1 character who *doesn't* change is the measuring stick |
| Tier-A characters frozen at rung 1 | the world feels like a set | every principal gets at least one rung per two arcs, every tier-B their one shift per arc |
| Every extra given an arc | context spent on people the reader will not remember; the cast blurs | tier C does not develop — see the tier table above |
| Development the MC narrates about others | patronising, and steals their arc | show them change when the MC is not the point of the scene |

## Self-check

- [ ] `state/growth.md` is current for everyone in this chapter
- [ ] Every advance was caused by one of the four triggers
- [ ] Every advance has a recorded voice delta, and the delta is in the dialogue
- [ ] No delta moved a character onto the MC's voice axes
- [ ] Any skill stage that advanced names a teacher, a reference or a costly failure — not time
- [ ] The MC's pain ledger has an entry for this chapter
- [ ] No tier-A character has been at rung 1 for two full arcs while on-page
- [ ] No tier-C walk-on was given a rung, an epiphany or an interior life
- [ ] No growth was narrated rather than demonstrated
