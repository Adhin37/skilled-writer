---
name: world-texture
description: Deliver the world on the page — how setting reaches the reader through consequence, friction and anchored sensory detail, at a budget that keeps a chapter from turning into a travelogue. Use while drafting any chapter, inside revision-pass, and when the world feels either flat and generic or bloated with description.
---

# world-texture

`story-bible` and `social-fabric` decide what is **true**. This skill decides what reaches the
**reader**, and in what quantity.

Two opposite failures, both fatal, and most drafts contain both:

| failure | symptom | cause |
|---|---|---|
| **Flat** | the scene could be anywhere; swap the proper nouns and nothing breaks | the world exists only in `bible/` |
| **Bloated** | readers skim; chapters open with paragraphs of scenery and history | the world reaches the page as description instead of as pressure |

The fix for flat is never "add description". It is **more consequence, more friction** — the
same detail count, doing work.

---

## 1. The four delivery channels

Ranked by cost per word. Reach for channel 4 only when 1–3 cannot carry it.

| # | channel | what it looks like | cost |
|---|---|---|---|
| 1 | **Consequence** | a rule of the world bites someone in this scene | free — it *is* the plot |
| 2 | **Friction** | a character works around the world to get what they want | free — it *is* the obstacle |
| 3 | **Assumed reference** | a character mentions a thing as obvious, unexplained | ~free — one clause |
| 4 | **Direct description** | narration states what a place is like | expensive — budgeted below |

**The rule:** for every one sentence of channel 4, the chapter should contain at least two beats
of channels 1–3. If you cannot name them, you are decorating, not building.

```
flat        The market was crowded and dangerous, full of merchants from many lands.
channel 1   The toll-taker weighed her coat, decided it was worth a copper, and took it.
channel 2   She went the long way around the fountain. Fountains had ears.
channel 3   "Not on a levy day," he said, and that was the end of the plan.
```

## 2. The description budget

Expressed per scene and per chapter, so it holds at any length. Chapters are not written to a word
count (`revision-pass` Pass 9), so neither is their description.

| item | budget |
|---|---|
| Direct description (channel 4) | **≤8% of the chapter's words.** Above that it is a travelogue |
| Sensory details **per scene** | 2–4, placed in motion, never in a block |
| Consecutive sentences of pure description | **3 maximum**, and only once per chapter |
| New proper nouns introduced | 2–3 (see `story-bible` naming; the lexicon is authoritative) |
| New invented terms | ≤1, and it must be used a second time within the chapter or cut |
| Paragraphs of world history | **0.** Always. History reaches the reader as a character's grudge |
| Chapters opening on setting | 0 — see `hook-and-pacing`'s banned openings |

**The opening arc is the exception in one direction only.** Early chapters owe the reader an
anchor — what kind of world this is, and for fan fiction which one and when (`story-opening` §1).
That debt is paid through channels 1–3, *not* by raising the channel-4 budget. A reader who does
not know where they are needs a rule biting someone, not a paragraph of scenery.

A location the reader has already visited gets **fewer** details, not the same ones re-explained:
its anchor (§4), and only what has changed since.

## 3. The load-bearing test

Every world detail on the page must do at least one of these. A detail doing none is cut in
`revision-pass`, no matter how good the sentence is.

1. **Characterises the person noticing it** (§5)
2. **Sets up a later beat** — it will be used, threatened, or paid off
3. **Anchors a location** so the reader can tell it from the others (§4)
4. **Carries a social fact** — who is allowed here, who pays, who is not present (`social-fabric`)
5. **Creates friction** — it makes the goal harder, or the workaround visible

The best details do two. *"The lamp was Guild oil, and it was burning at noon"* — anchor, social
fact, and setup, in nine words.

## 4. Anchors: how a reader learns a place

Each location in `bible/world.md` carries a **sensory signature** — two details, at least one
non-visual. That signature is not a starting point to vary from. **Repeat it verbatim-ish at
every visit.** Repetition is not laziness here; it is the entire mechanism by which a name
becomes a place in a reader's head, and it costs one clause.

- **Anchor first, then vary.** Signature detail in the first 100 words of arriving; anything new
  after that.
- **One sense per location should be non-visual.** Rooms are remembered by smell and sound far
  more than by architecture.
- **Let places change.** The undercroft that always smelled of wet chalk, smelling of smoke, is a
  plot beat that costs nothing and lands hard — precisely because the anchor was boring for
  twelve chapters.
- New durable location facts go to `set>` in the CCS block, then into the `bible/world.md` table
  (`continuity-summary`). An anchor invented in a chapter and never recorded will drift.

## 5. Perception is characterisation

**Nobody perceives a room. A specific person perceives what their life makes salient.** This is
the single highest-value technique in this skill, and it is free: the same detail count produces
both world and character.

Filter every observation through the POV character's job, wound, want and current state
(`narrator-voice` sets the distance that makes this possible):

| the POV character is | what they notice in the same tavern |
|---|---|
| a thief | the two exits, and which one the owner watches |
| a starving person | what is on other people's plates |
| a physician | the cough at the back table |
| a noble in disguise | that nobody stood when they entered |
| grieving | nothing, until something forces itself in — then far too much detail on one small thing |

Corollary: **a character does not notice what is normal to them.** A native never registers the
smell of their own city. If the POV is local, the world reaches the reader through channels 1–3,
not through their eyes — which is why outsider POVs are cheap and locals are the real test.

## 6. Depth without explanation

A world feels large in proportion to what it declines to explain. Reserve, not volume.

- **The unexplained reference.** Once every chapter or two, let a character refer to a custom,
  event, debt or place as obvious, and never gloss it. Do not explain it later either unless the
  plot needs it. This is the strongest "lived-in" signal in fiction.
- **Offhand specificity.** "the third bell", "the Sixth-Year rules", "since the levy" — a
  concrete name for a thing the reader does not know implies a system behind it.
- **Disagreement.** Two characters remembering the same event differently makes a world older
  than any history paragraph.
- **Wear and repair.** Things that were built by someone, mended by someone, and are now used for
  something else. What a world does with its ruins is characterisation of the world.
- **Off-page life.** Someone is doing an unrelated job in the background of the scene, badly.

**Cap it.** One or two unexplained references per chapter. More and the reader stops feeling
depth and starts feeling lost — the line is whether the *scene* is comprehensible without it.

## 7. Overbuilding — the symptoms

Delete on sight:

- The **establishing paragraph** at a scene's start. Enter in motion; deliver setting inside
  action (`scene-craft`).
- The **gazetteer sentence**: nations, rivers or houses listed with no scene using them.
- The **history lecture**, in narration or in dialogue between two people who both already know it.
- The **glossary cluster**: three invented words in one paragraph.
- **Explaining the reference you just made**. Trust the reader for one chapter; if it still
  matters in three, it will be explained by a consequence.
- **Symmetrical worldbuilding** — five great houses, seven schools, four elements. Real orders are
  lopsided: one dominant, one dying, one that everybody pretends does not exist.
- **Detail with no owner.** If nobody in the scene would look at it, it is the author looking.

## 8. Where this runs

| when | do |
|---|---|
| `write-chapter` step 1 | pick the chapter's **world channel**: the one thing about the world this chapter makes concrete, and which of §1's channels carries it |
| `write-chapter` step 2 | budget (§2), anchors (§4), POV filter (§5) while drafting |
| `revision-pass` Pass 5 | the checklist below; cut anything failing §3 |
| `continuity-summary` write mode | new anchors and durable facts to `set>`, then to `bible/world.md` |

**Related skills.** `story-bible` owns the facts and the location table · `social-fabric` owns
who the world is fair to, and supplies most channel-1 and channel-4 material · `power-system` /
`tech-plausibility` own the central rule whose consequences you are rendering ·
`slice-of-life-texture` (optional) deepens the household layer of the same job · `prose-quality`
owns the sentences · `mtl-detox` bans the stock scenery phrases · `narrator-voice` sets the
distance §5 depends on.

## Self-check

- [ ] Every world detail passes the load-bearing test (§3)
- [ ] At least two channel 1–3 beats for every sentence of channel 4
- [ ] 2–4 sensory details per scene, at least one non-visual, none in a block
- [ ] No run of more than three descriptive sentences; no establishing paragraph
- [ ] Every location visited hit its anchor within 100 words of arrival
- [ ] Observations are filtered through the POV character, not the author
- [ ] Nothing normal to the POV character was noticed by them as if it were strange
- [ ] ≤1 new invented term, and it recurs or is cut
- [ ] Zero paragraphs of history or gazetteer
- [ ] One or two things referred to and left unexplained — and the scene still reads
- [ ] New anchors recorded in `set>` and moved into `bible/world.md`
