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
| Anyone new on the page: their **cast tier**, decided before they speak | `character-profile` — default C, three strokes, one roster line |
| Which bodies are locked, and what they cannot do today | `mc-design` → `state/body.md` §1–§2 |
| **The offstage question**: what the world does this chapter that the MC doesn't know | `timeline-engine` → `plan/timeline.md` §4 |
| What the MC deduces, and from which on-page clue | `mc-intel-meter` |
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
- **Walk-ons.** A new minor character gets three strokes and no more: a five-minute want, one
  habit, and one piece of their working world. No interiority, no backstory paragraph, no ladder.
  Do not stop to build a profile mid-draft — sketch them, and log the line in step 5.
- **Intelligence.** Every MC decision passes the `mc-intel-meter` trace test: the reader can name
  the on-page fact it came from.
- **Ground the scene.** Two concrete sensory details per scene, drawn from the location's
  signature in `bible/world.md`. Not a paragraph of description — two details, placed in motion.
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

Cast bookkeeping, same pass: every walk-on who appeared gets their roster line in
`bible/cast/_extras.md` (or their appearance chapter appended to an existing one), every named
person goes in `lexicon.md`, and anyone who hit a third appearance or changed the plot is promoted
now — with their profile built from what is already on the page.

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
| Minor characters are wallpaper | sketched with a job and nothing else | `character-profile` — three strokes, especially the third |
| A one-scene shopkeeper got a backstory | tier not assigned before writing | `character-profile` — default C, and C has no interior |
| MC solves it too easily | no cost budgeted | `conflict-engine` |
| MC misses the obvious | plot needs delay | `mc-intel-meter` — change the *information*, never the intelligence |
| Reader has no reason for the next chapter | weak hook | `hook-and-pacing` |
| Contradicts chapter 30 | read-set skipped | `continuity-summary` |
| Prose feels translated | genre-corpus default | `mtl-detox` |
