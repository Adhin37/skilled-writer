---
name: write-chapter
description: Draft the next chapter of a webnovel. Orchestrates continuity, character, POV, conflict, pacing and quality skills into one procedure and writes the chapter file plus all state updates. Use whenever the user asks to write, draft or continue a chapter, or says /novel-write.
---

# write-chapter

The main loop. This is the only skill that produces prose. Follow the steps in order; each one
is cheap, and skipping one is what produces the drift that ruins long serials.

---

## Step 0 — Load

1. Resolve the active novel (see `CLAUDE.md` §1). Read `novels/<slug>/novel.md`.
2. Note: `genre`, `narration.*`, `pov.*`, `mc.intel_tier`, `chapters.*`, `content.*`,
   and which `optional:` keys are `on`. Only `on` skills apply.
3. Determine the chapter number: highest existing file in `chapters/` + 1, unless told otherwise.
4. Run `continuity-summary` in **read mode**. You now have the read-set and the chapter brief.
5. Read the target row in `plan/chapters.md`. If it is missing or any of
   goal/obstacle/turn/cost/hook is blank, run `chapter-plan` for this row first. Do not draft
   from an incomplete row.

## Step 1 — Decide the chapter's shape (before writing a word)

Write these down for yourself. Ten lines, not a document.

| decision | source |
|---|---|
| POV character, and whether this is a switch | `pov-switch` + the plan row |
| Scene count and where the break falls | `scene-craft`, `chapters.scenes_per_chapter` |
| Per scene: goal → obstacle → turn → exit state | `scene-craft` |
| What this chapter costs the POV character | `conflict-engine` — never zero |
| Which thread ops fire | `plot-threads` |
| Which character sounds different today, and how | `character-development` → `state/growth.md` |
| **The voice spread**: this chapter's speakers as matrix rows, side by side — and which of them differs from the MC on two or more axes | `voice-separation` §1, §3 → `bible/cast/_voices.md` |
| Anyone new on the page: their **cast tier**, decided before they speak | `character-profile` — default C, three strokes, one roster line, one off-default axis |
| Which bodies are locked, and what they cannot do today | `mc-design` → `state/body.md` §1–§2 |
| **The offstage question**: what the world does this chapter that the MC doesn't know | `timeline-engine` → `plan/timeline.md` §4 |
| **The world channel**: the one thing about the world this chapter makes concrete, and whether a consequence, a friction or an assumed reference carries it | `world-texture` §1 |
| What the MC deduces, and from which on-page clue | `mc-intel-meter` |
| **Who has to ask**: the thing this chapter needs known, whose map actually covers it, and who must go to someone else for it | `competence-map` §1, §4 → `bible/cast/_competence.md` |
| Opening line strategy, closing hook | `hook-and-pacing` |

**Gate.** If "what this chapter costs" is empty, the chapter is not ready. Go back to
`conflict-engine`. A chapter where the POV character only gains is filler regardless of how
much happens in it.

## Step 2 — Draft

Write straight through. Do not stop to self-edit; `revision-pass` handles that.

Hold these while writing:

- **Voice.** `narrator-voice` sets person, tense, distance, interiority. It does not change
  mid-chapter unless `pov-switch` says a switch is happening.
- **Dialogue.** Every named speaker's lines must satisfy their speech fingerprint
  (`dialogue-voice`). If you cannot tell two characters apart with the tags removed, fix it now.
- **Voice spread.** Hold each speaker's matrix row while writing (`voice-separation`): their turn
  length, their articulacy — which is *not* their intelligence — and whether wit is theirs at all.
  Nobody except a declared mirror reasons at the MC's speed by default; somebody in this chapter is
  slower than the MC, or worse at saying it, and is right about something anyway. Beats come from
  each character's hands and pressure move, never from the default gesture set.
- **Other minds, no interiority.** Non-POV characters think through their **first move** — what
  they reach for or look at first when the situation changes. That is the whole mechanism; the
  narration never enters a second head.
- **Walk-ons.** A new minor character gets three strokes and no more: a five-minute want, one
  habit, and one piece of their working world — plus one axis off default, so they do not speak in
  the narrator's register. No interiority, no backstory paragraph, no ladder. Do not stop to build
  a profile mid-draft — sketch them, and log the line in step 5.
- **Intelligence.** Every MC decision passes the `mc-intel-meter` trace test: the reader can name
  the on-page fact it came from.
- **Knowledge.** Every *fact* anyone states passes the `competence-map` provenance test: they were
  taught it, did it, were told it, read it, or are openly guessing. An unlisted domain is `none`,
  so somebody in this chapter says they do not know, asks the person who does, or is confidently
  wrong — and a character being wrong is more useful than a character being blank. Nobody explains
  a subject their map does not cover, however convenient their mouth is.
- **Learning.** If anyone is practising something, it appears as a clause, not a scene — unless a
  stage transition fires this chapter, which earns one. Either way the practice took time from
  something else and the chapter says what.
- **Ground the scene.** `world-texture`. Two to four concrete sensory details per scene, at least
  one non-visual, drawn from the location's signature in `bible/world.md` and hit within 100 words
  of arriving. Never a paragraph of description — details placed in motion, and **filtered through
  the POV character**: they notice what their job, wound and want make salient, and they do not
  notice what is normal to them. The world's *rules* reach the reader by biting someone or by
  being worked around, not by being narrated.
- **Cut the connective tissue.** Enter scenes late, leave early. No arrivals, no farewells, no
  walking between locations unless something happens on the way.
- **Optional skills.** Apply each `on` skill's rules as you write, not afterwards.

### Chapter anatomy (default, 2000 words)

| section | words | job |
|---|---|---|
| Cold open | 100–200 | In motion. A line of dialogue, an action, or a wrong-feeling detail. Never weather, never waking up, never a recap. |
| Scene 1 | 700–900 | Goal pursued, obstacle met, first turn. |
| Break | — | `* * *` |
| Scene 2 | 700–900 | Consequence of the turn; the chapter's cost lands. |
| Hook | 50–120 | The last beat. See `hook-and-pacing`. |

Deviate freely when the material wants it — but never end without a hook if
`chapters.hook_required` is true.

### Recap discipline

Readers arrive a day or a week later. Re-anchor with **one clause, inside a sentence doing other
work**: "The coat she'd taken off Dael's body still smelled of the undercroft." Never a
paragraph. Never "As you'll remember".

## Step 3 — Write the file

`novels/<slug>/chapters/NNNN-<kebab-title>.md`, four-digit padded, with the frontmatter from
`chapters/_chapter-template.md` filled in. Prose only in the body — no headings, no author notes.

## Step 4 — Revise

Run `revision-pass`. It runs `prose-quality`, `mtl-detox`, `bias-guard`, and a continuity check.
Fix what it finds, in the file. Set `status: revised`.

## Step 5 — Write state back

Run `continuity-summary` in **write mode**: CCS block, threads, growth, timeline, any new bible
facts. This step is not optional and not deferrable to "later".

World bookkeeping, same pass: any new location anchor or durable social fact goes into `set>`,
then into `bible/world.md` or `bible/society.md`. An anchor invented on the page and never
recorded will drift by its third appearance.

Cast bookkeeping, same pass: every walk-on who appeared gets their roster line in
`bible/cast/_extras.md` (or their appearance chapter appended to an existing one), every named
person goes in `lexicon.md`, and anyone who hit a third appearance or changed the plot is promoted
now — with their profile built from what is already on the page. A promotion also earns a row in
`bible/cast/_voices.md` and one in `bible/cast/_competence.md`, both placed against the existing
cast rather than invented in isolation.

Knowledge bookkeeping, same pass: a skill stage that advanced goes in the skill-ladder table of
`state/growth.md` with what caused it; a genuinely new domain a character acquired on the page goes
on the competence grid. If the chapter had to invent an expertise nobody had, record it — and say
so in the report, because it usually means the cast is missing a person.

## Step 6 — Report

Four lines to the user, no more:

```
Ch 42 — "The Ledger Room" (1,840 w) → novels/<slug>/chapters/0042-the-ledger-room.md
Cost: Rin loses Dael's trust; Echo-step now known to the Guild.
Threads: opened T14 (forged seal), paid T09 (oath to Mira).
Next: ch 43 is planned — she reads the ledger. Say go, or tell me what to change.
```

Do not paste the chapter into chat unless asked.

---

## Running a batch

If asked for several chapters, run the full loop per chapter — including state write-back —
before starting the next. Never draft three chapters and then reconcile state; the second
chapter must be written against the first chapter's consequences.

Pause and check in after every 5 chapters with a one-paragraph status and one question about
direction. Long unsupervised runs drift.

## When the plan and the draft disagree

The draft wins if it is better, but the plan must be updated, not ignored:

1. Write what the chapter actually became.
2. Amend that row in `plan/chapters.md`.
3. Re-check the following three rows for rows that no longer follow, and fix them.
4. Tell the user in the report line: "chapter went somewhere else — replanned 43–45."

## Common failure modes

| symptom | cause | fix |
|---|---|---|
| Chapter reads as "stuff happened" | no turn | `scene-craft` |
| Characters sound identical | fingerprints not loaded | `dialogue-voice` |
| Everyone reasons and jokes like the MC | the cast was never placed on the matrix; the MC is the model's calibration point | `voice-separation` §1, §3 — straddle the tier, cap the wit, hold the turn lengths |
| The allies are interchangeable | they share intel + articulacy + wit | `voice-separation` §3 — change one axis or merge the characters |
| Beats are all nods, shrugs and sighs | the default gesture set | `voice-separation` §4 — beats come from the hands field |
| Minor characters are wallpaper | sketched with a job and nothing else | `character-profile` — three strokes, especially the third |
| A one-scene shopkeeper got a backstory | tier not assigned before writing | `character-profile` — default C, and C has no interior |
| Scene could be anywhere; swap the nouns and nothing breaks | world lives only in `bible/` | `world-texture` §1 — add consequence and friction, not description |
| Readers skim the openings | establishing paragraphs, scenery blocks | `world-texture` §2, §7 |
| World has spectacular magic and generic peasants | rule never propagated | `social-fabric` §2 |
| MC solves it too easily | no cost budgeted | `conflict-engine` |
| MC misses the obvious | plot needs delay | `mc-intel-meter` — change the *information*, never the intelligence |
| Everyone can answer any question | unlisted domains treated as "probably fine" | `competence-map` §1 — unlisted is `none`; somebody asks, or is wrong |
| A convenient character explains the thing | exposition assigned to whoever is standing there | `competence-map` §3 — nobody explains a domain they do not have |
| Bad at it Tuesday, good at it Friday | the training montage | `competence-map` §5 — five stages, a named source per advance |
| Reader has no reason for the next chapter | weak hook | `hook-and-pacing` |
| Contradicts chapter 30 | read-set skipped | `continuity-summary` |
| Prose feels translated | genre-corpus default | `mtl-detox` |
