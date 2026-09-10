---
description: Draft the next chapter (or a specified one) and update all state
argument-hint: "[chapter number] [or: 'next 3'] [--no-confirm]"
---

Write chapter prose.

Resolve the active novel (CLAUDE.md §1), then invoke the `write-chapter` skill and follow all
six steps, including the state write-back in step 5.

**Drafting is two phases.** Phase A (step 1) produces a twelve-line brief — the event, the
temperature, the hook shape, the scenes, the cost, who speaks — and then **stops and shows it to
the user**. Phase B drafts only after they approve it or change it. This is the cheapest gate in
the toolkit: a chapter that was going to be a thousand words of somebody quietly feeling
something gets caught for twelve lines instead of after the draft.

Interpret `$ARGUMENTS`:

- empty → the next unwritten chapter
- a number → that chapter. If it already exists, ask before overwriting
- "next N" / "N chapters" → run the full loop N times, one chapter at a time, writing state back
  between each. Pause and check in after every 5. Phase A still runs for each chapter; present
  all N briefs together, once, before drafting any of them.
- `--no-confirm` → run Phase A but do not stop for approval. The brief still gets written and
  still gates the draft; the user simply is not asked.

Before drafting, confirm the plan row for the target chapter is complete — including **`event`**,
**`temp`** and **`hooktype`**, which are decided at plan time and not after. If any is missing,
run `chapter-plan` for that row first.

Do not paste the chapter into the conversation. Report the six-line summary the skill specifies,
leading with the event and never with a word count.
