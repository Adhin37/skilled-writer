---
description: Compact the continuity ledger, run the arc-boundary pass, or produce a recap
argument-hint: "[optional: 'for readers' | 'arc 2' | 'audit' | 'review']"
---

Maintain or read out the continuity ledger, and run the arc-boundary pass.

Resolve the active novel, then **invoke the `architect` agent** (description `recap arc N`) to run
`continuity-summary`'s arc rollup. It is the one role that can do the whole job: the digests land
in `state/continuity.md` and the drift and competence audits in `bible/cast/`, and the architect
writes both. The review and "for readers" modes only read, so you may run those yourself. If the
agent is unavailable, run it inline and say so — in a test run, stop and log it instead.

Interpret `$ARGUMENTS`:

- empty or "compact" → run the arc rollup: write the arc digest for the most recently completed
  arc, compress the digest that is now two arcs old to 40 words, rewrite the book digest. Leave
  chapter blocks in place. **Then run the arc review below**, because a closed arc is exactly when
  the distributional defects become visible and still cheap to fix.
- "review" (or "review arc N") → the **arc-boundary pass**, and nothing else:

  ```bash
  python3 scripts/sw.py arc novels/<slug> [-a N] --show note
  python3 scripts/sw.py curve novels/<slug>            # the whole book's power curve
  ```

  The first prints the countable half — the per-chapter table of words, dialogue share, anchor
  count, ledger presence and POV; the dialogue trend; the length spread; hooks; cast rotation;
  thread operations; the foreknowledge ledger; and this arc's pressure range and gains. The second
  is the whole-book view, and an arc boundary is the only place the curve's slow failures are
  visible: a flat middle, gains drifting closer together, ten fights in one band, or pressure
  falling while the MC's tier rises. Check the arc you just closed against its row in
  `state/power.md` §6, and set the next arc's band before planning it.

  Read both sets of findings, then answer the questions under **the judged half** by reading the
  arc: the dramatic question, consistency, voice drift, whether the blurb still describes this
  book, the shape of the arc's tension, and whether its ending was predictable from its first
  chapter.

  **Report what you found; never score the arc.** A number attached to an arc is a number the next
  arc gets written toward, and judged scores on prose agree with human preference about 73% of the
  time at best. Say what to change and where.
- "for readers" → write a human-facing recap of the story so far, in prose, spoiler-safe to the
  latest published chapter. This is a *separate output* — never edit the ledger into prose.
- "arc N" → rewrite that arc's digest from its chapter blocks.
- "audit" → check the ledger's integrity against `continuity-summary` §Self-check — its list, not
  a copy of it: `python3 scripts/sw.py state novels/<slug>` runs the countable half. Report
  defects; the fixes go to the role that owns each file, never to you in a test run.

Keep the ledger machine-only and compressed. Do not prettify it, do not expand it, and do not
apologise for its unreadability — that is the design.
