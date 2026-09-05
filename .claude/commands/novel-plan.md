---
description: Build or extend the arc plan and chapter construction list
argument-hint: "[optional: 'arc 3' | 'next 10 chapters' | a direction to take]"
---

Plan ahead.

Resolve the active novel, then invoke the `chapter-plan` skill.

Interpret `$ARGUMENTS`:

- empty → extend the chapter list so there are 12 planned rows ahead of the draft line; if the
  current arc is nearly complete, design the next arc first
- "arc N" → design that arc in full using the arc template
- "next N chapters" → add N fully-specified rows
- anything else → treat as a direction the user wants the story to take; incorporate it, and say
  which existing plan rows it invalidates before you change them

Always fill `goal → obstacle → turn → cost → threads → hook → title`, in that order, title last.

After planning, report: the arc question, the five pillar chapters, the permanent cost to the MC,
and the new chapter titles as a list. Flag any thread whose `due` chapter has passed.
