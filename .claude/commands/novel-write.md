---
description: Draft the next chapter (or a specified one) and update all state
argument-hint: "[chapter number] [or: 'next 3', or a range to re-gate] [--no-confirm]"
---

Write chapter prose.

Resolve the active novel (CLAUDE.md §1), then invoke the `write-chapter` skill and follow all
six steps, including the Phase C gate in step 4 and the state write-back in step 5.

**Drafting is three phases, and this command runs all three.** Phase A (step 1) produces a
twelve-line brief — the event, the temperature, the hook shape, the scenes, the cost, who speaks —
and then **stops and shows it to the user**. Phase B drafts only after they approve it or change
it; that is the cheapest gate in the toolkit, because a chapter that was going to be a thousand
words of somebody quietly feeling something gets caught for twelve lines instead of after the
draft. Phase C (step 4) runs `revision-pass` on what came out.

**The chapter is not reported until the gate passes.** Do not hand back a chapter at
`status: drafted`, and do not defer the gate to a later turn or a later command — there is no
later command. If Pass Z sends the chapter back to Phase B, redraft the scene and gate the new
text, and say so in the report.

Interpret `$ARGUMENTS`:

- empty → the next unwritten chapter
- a number → that chapter. **If it already exists, ask which**: re-gate it (Phase C only — run
  `revision-pass` over the existing prose and fix what it finds) or redraft it from the plan row.
  Never overwrite without asking.
- a range like `40-45` → re-gate each existing chapter in turn, finishing one completely —
  including its `stamp` — before starting the next, so an interruption leaves whole chapters
  behind it. Report once at the end.
- "next N" / "N chapters" → run the full loop N times, one chapter at a time, writing state back
  between each. Pause and check in after every 5. Phase A still runs for each chapter; present
  all N briefs together, once, before drafting any of them.
- `--no-confirm` → run Phase A but do not stop for approval. The brief still gets written and
  still gates the draft; the user simply is not asked. It does not skip Phase C.

Before drafting, confirm the plan row for the target chapter is complete — including **`event`**,
**`temp`** and **`hooktype`**, which are decided at plan time and not after. If any is missing,
run `chapter-plan` for that row first.

Do not paste the chapter into the conversation. Report the seven-line summary the skill specifies,
leading with the event and never with a word count.
