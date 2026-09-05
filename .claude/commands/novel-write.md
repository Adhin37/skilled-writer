---
description: Draft the next chapter (or a specified one) and update all state
argument-hint: "[chapter number] [or: 'next 3']"
---

Write chapter prose.

Resolve the active novel (CLAUDE.md §1), then invoke the `write-chapter` skill and follow all
six steps, including the state write-back in step 5.

Interpret `$ARGUMENTS`:

- empty → the next unwritten chapter
- a number → that chapter (if it already exists, ask before overwriting)
- "next N" / "N chapters" → run the full loop N times, one chapter at a time, writing state back
  between each. Pause and check in after every 5.

Before drafting, confirm the plan row for the target chapter has all seven middle columns filled.
If not, run `chapter-plan` for that row first.

Do not paste the chapter into the conversation. Report the four-line summary the skill specifies.
