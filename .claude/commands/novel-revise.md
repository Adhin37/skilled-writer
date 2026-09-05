---
description: Run the ten-pass quality gate on a chapter and fix what it finds
argument-hint: "[chapter number, or a range like 40-45]"
---

Revise a drafted chapter.

Resolve the active novel, then invoke the `revision-pass` skill and run all ten passes in order.

Interpret `$ARGUMENTS`:

- empty → the most recently written chapter
- a number → that chapter
- a range → each chapter in turn, reporting once at the end

Load, for each target: the chapter file, its CCS block, the two preceding CCS blocks, the
profiles and growth rows of everyone in it, the `bible/cast/_voices.md` rows for its speakers,
`bible/lexicon.md`, and the `bible/world.md` rows for the locations it uses (plus
`bible/society.md` if it turns on a social rule).

Fix defects in the file — do not report them and leave them. If a structural pass (1–4) requires
rewriting a scene, rewrite it, then re-run passes 5–10 on the new text. Update the CCS block if the
revision changed events, knowledge or thread operations.

Set `status: revised` when clean. Report in two lines. Always state explicitly if pass 6
(`bias-guard`) found anything.

Pass 2 carries the **voice-separation** block: the transplant test, the three-way clash, turn
lengths, and the default-gesture sweep. If a chapter fails it repeatedly, the defect is in the
matrix rather than in the chapter — say so and offer to redeal `bible/cast/_voices.md`.
