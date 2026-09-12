---
type: reference
owner: revision-pass
description: "Pass 1, and keep it open to Pass 10 - the six passes that have no other owner"
---

# revision-pass — the passes nobody else owns

Open this at Pass 1 and keep it open to Pass 10. Most passes point at another skill's audit card;
these six have no other owner, so their checks live here — the same rule, one file down, so the
dispatcher stays a dispatcher.

Every row is the check, the failure it catches, and **the cheapest repair that actually fixes
it**. Reach down the repair column before reaching for a rewrite: most continuity and knowledge
defects are a clause, and a scene rewritten to fix a spelling is a scene that now needs Pass 8
again.

---

## Pass 1 — Continuity

Against the read-set. The read-set is the authority: where the chapter and the ledger disagree,
**the ledger wins unless the chapter is better**, and if the chapter is better the ledger is
amended and the amendment is reported.

| check | fails when | cheapest repair |
|---|---|---|
| No contradiction with the last five CCS blocks | a fact quietly changed between chapters — a door that was locked is open, a debt that was owed is forgotten | change this chapter. The ledger records what shipped, and a reader has already read it |
| Nobody knows what their `kno>` history does not support | a character acts on information no scene gave them | give them the moment they learned it, in a clause — or let them be *guessing*, which is usually the better scene |
| Names, terms, titles and spellings match `bible/lexicon.md` exactly | two spellings of one name across forty chapters | fix the chapter. Change the lexicon only if the new form is genuinely better, and then say so — a silent lexicon edit orphans every earlier chapter |
| In-world time agrees with `state/timeline.md`; travel is plausible | a three-day journey happens overnight because the plot needed it | move the scene, not the map. Distances are load-bearing once a reader has priced them |
| Objects, injuries and possessions persist | the coat, the scar, the debt vanish when inconvenient | one clause restores it. An injury that stops mattering is a stake the reader learns to discount |
| Nothing contradicts `bible/world.md`, `society.md` or `power-system.md` | the world bends for one scene | bend the scene. A rule broken once is a rule the reader stops believing |
| Positions match where the last chapter left them | somebody is in a room they had walked out of | a transition clause, or cut back to where they were |

### The form check — only when a character in the chapter is `form_locked`

Read `state/body.md` §1–§2 first; the CURRENT FORM row is the only description that exists.

- [ ] **The form reached the page twice** — once as a limit that bites, once as the world
      reacting to it. This box is the only one here that an empty chapter fails; `mc-design`
      owns the rule and the two halves (`mc-design/references/form-ledger.md` rule 9)
- [ ] Not every frail or childish beat was a performance the character chose. When all of them
      are, the form has stopped being a body and become a tactic
- [ ] Every physical description matches the CURRENT FORM row — nothing borrowed from a later stage
- [ ] No capability exceeded the stage's absolute limits: reach, strength, stamina, voice
- [ ] Others reacted to the **body**, not to the mind inside it
- [ ] Adult diction out of a child's body was noticed by somebody, or deliberately masked
- [ ] A stage transition, if one fired, is logged in §4 with what it enables and what it costs

The common failure is not a wrong sentence but an *absent* one: nobody in the scene registers the
body at all, and the form stops being a constraint and becomes a costume.

That is why the first box is phrased as something the chapter must *contain*. The five below it
are prohibitions, and a prohibition is satisfied by silence — run #3 passed all of them across
five chapters precisely because it never mentioned the body it was forbidden to get wrong. A
checklist made only of prohibitions cannot catch its own blind spot.

---

## Pass 4 — Structure

Four owners meet in this pass and none of them is this file, but they sit on **three** cards.
The scenes are on `scene-craft`'s audit card — goals, exits, the stated cost, the cuts. The
chapter's price is on `conflict-engine`'s. The promises are on `plot-threads`', and so is
`timeline-engine`'s world track, on that card's second half. Open those three; the checklists were
moved there because a checklist kept in this file is a checklist read without its owner.

One row has no other owner and stays here:

| check | fails when | cheapest repair |
|---|---|---|
| **Skim test** | you cannot name the one thing a reader would miss | that is a Pass 9 problem wearing a Pass 4 coat — go back to Pass Z |

---

## Pass 7 — MTL detox, the structural half

`sw lint` searches the whole banned list and counts narration exclamation marks and rhetorical
questions. These five are the ones no script can see, and the card in
`mtl-detox/references/audit-card.md` is where the detail lives.

- [ ] No crowd-reaction block — a paragraph of unnamed onlookers narrating how impressive the scene was
- [ ] No rank recital or system lecture delivered as narration
- [ ] No face-slap loop: **every confrontation cost the winner something**
- [ ] No paragraph saying the same thing three ways
- [ ] No translationese rhythm — the extra beat before a revelation, the doubled intensifier

---

## Pass 9 — Delivery, beyond the five questions

The five questions are `scene-craft`'s, on its audit card. These are the checks that belong to
this pass instead — the ones about the chapter as a unit of a serial rather than as a structure.

- [ ] `delivers:` matches what the chapter did, and the five answers on `scene-craft`'s audit
      card came without straining
- [ ] **Skim test**: a reader who skipped this chapter loses something nameable

The chapter's first and last sentences are audited on `hook-and-pacing`'s card, which is also
opened at this pass — the opening, the hook, the forecast test and the rotation are all its
concepts, and they are distributional, so they are read against the previous five chapters rather
than against this one.

**Length.** If the chapter is far outside `chapters.length_band`, ask *once* whether the material
was split in the wrong place, then move on. Never pad, never trim, and never record a length
judgement — `docs/design-notes.md` §"Why the gate is delivery, not length" is why.

---

## Pass 9d — Theme

Skip when `theme.controlling_idea` is empty. This pass tests **restraint, not presence**: the
measured failure of machine-written fiction is not an absent theme but a narrated one — AI
narrators state the story's meaning outright about 77% of the time against 52% for human writers.

- [ ] **No narration sentence states the lesson.** The narrator does not explain what the book
      means, what a character has learned, or what any of it says about people
- [ ] If the controlling idea is spoken aloud, a **character** speaks it — and is either wrong
      about it or pays for being right
- [ ] `theme.counter_case` is alive: somebody in this arc argues the other side and is allowed to
      be persuasive. A counter-case that has never won a scene makes the theme a sermon
- [ ] The chapter tests the idea through a **choice**, not through a conversation about it

The cheapest repair is almost always deletion. A narrated theme is usually the last sentence of a
scene, and the scene is better without it.

---

## Pass 10 — Mechanics

- [ ] Frontmatter complete, including **`event:`** and **`delivers:`** — different fields
- [ ] Scene breaks use `* * *`
- [ ] POV label present if the chapter switches and `label_switches` is true
- [ ] `wordcount:` is **measured**, never estimated, and re-measured if any pass changed the body

A wrong count propagates into `state/continuity.md` and corrupts every share computed from it, so
stamping runs **last**. It rewrites frontmatter only, never the prose:

```bash
python3 scripts/sw.py stamp novels/<slug> -c <n> --status revised --ledger
```

Without Python, measure the body with `wc -w` and write both numbers by hand.

**The four channels** are `narrator-voice`'s to enforce, not this file's — open
`narrator-voice/references/audit-card.md`.
