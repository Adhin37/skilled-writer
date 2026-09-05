---
description: Compact the continuity ledger, or produce a human-readable recap
argument-hint: "[optional: 'for readers' | 'arc 2' | 'audit']"
---

Maintain or read out the continuity ledger.

Resolve the active novel, then invoke the `continuity-summary` skill.

Interpret `$ARGUMENTS`:

- empty or "compact" → run the arc rollup: write the arc digest for the most recently completed
  arc, compress the digest that is now two arcs old to 40 words, rewrite the book digest. Leave
  chapter blocks in place.
- "for readers" → write a human-facing recap of the story so far, in prose, spoiler-safe to the
  latest published chapter. This is a *separate output* — never edit the ledger into prose.
- "arc N" → rewrite that arc's digest from its chapter blocks.
- "audit" → check the ledger's integrity: every chapter has a block, every block has `kno>` and
  `hook>`, no block exceeds 12 lines, thread ids all exist in `threads.md`, names match
  `lexicon.md`, timeline is monotonic. Report defects and fix them.

Keep the ledger machine-only and compressed. Do not prettify it, do not expand it, and do not
apologise for its unreadability — that is the design.
