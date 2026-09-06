---
description: Compact the continuity ledger, run the arc-boundary pass, or produce a recap
argument-hint: "[optional: 'for readers' | 'arc 2' | 'audit' | 'review']"
---

Maintain or read out the continuity ledger, and run the arc-boundary pass.

Resolve the active novel, then invoke the `continuity-summary` skill.

Interpret `$ARGUMENTS`:

- empty or "compact" → run the arc rollup: write the arc digest for the most recently completed
  arc, compress the digest that is now two arcs old to 40 words, rewrite the book digest. Leave
  chapter blocks in place. **Then run the arc review below**, because a closed arc is exactly when
  the distributional defects become visible and still cheap to fix.
- "review" (or "review arc N") → the **arc-boundary pass**, and nothing else:

  ```bash
  python3 scripts/sw.py arc novels/<slug> [-a N] --show note
  ```

  That prints the countable half — the per-chapter table of words, dialogue share, anchor count,
  ledger presence and POV; the dialogue trend; the length spread; hooks; cast rotation; thread
  operations; and the foreknowledge ledger. Read its findings, then answer the questions under
  **the judged half** by reading the arc: the dramatic question, consistency, voice drift, whether
  the blurb still describes this book, the shape of the arc's tension, and whether its ending was
  predictable from its first chapter.

  **Report what you found; never score the arc.** A number attached to an arc is a number the next
  arc gets written toward, and judged scores on prose agree with human preference about 73% of the
  time at best. Say what to change and where.
- "for readers" → write a human-facing recap of the story so far, in prose, spoiler-safe to the
  latest published chapter. This is a *separate output* — never edit the ledger into prose.
- "arc N" → rewrite that arc's digest from its chapter blocks.
- "audit" → check the ledger's integrity: every chapter has a block, every block has `kno>` and
  `hook>`, no block exceeds 12 lines, thread ids all exist in `threads.md`, names match
  `lexicon.md`, timeline is monotonic. Report defects and fix them.

Keep the ledger machine-only and compressed. Do not prettify it, do not expand it, and do not
apologise for its unreadability — that is the design.
