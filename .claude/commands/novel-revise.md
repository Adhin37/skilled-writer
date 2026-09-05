---
description: Run the nine-pass quality gate on a chapter and fix what it finds
argument-hint: "[chapter number, or a range like 40-45]"
---

Revise a drafted chapter.

Resolve the active novel, then invoke the `revision-pass` skill and run all nine passes in order.

Interpret `$ARGUMENTS`:

- empty → the most recently written chapter
- a number → that chapter
- a range → each chapter in turn, reporting once at the end

Load, for each target: the chapter file, its CCS block, the two preceding CCS blocks, the
profiles and growth rows of everyone in it, and `bible/lexicon.md`.

Fix defects in the file — do not report them and leave them. If a structural pass (1–4) requires
rewriting a scene, rewrite it, then re-run passes 5–9 on the new text. Update the CCS block if the
revision changed events, knowledge or thread operations.

Set `status: revised` when clean. Report in two lines. Always state explicitly if pass 5
(`bias-guard`) found anything.
