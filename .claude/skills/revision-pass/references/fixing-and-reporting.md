# revision-pass — fixing, reporting, standalone use

Open this when a pass has found something and you are deciding what to change, or when you are
writing the report at the end.

## Fixing

- **Fix in the file.** Do not report a defect and leave it.
- **Structural defects can require a rewrite of a scene.** Do it. A chapter with no cost or no
  turn cannot be repaired at the sentence level.
- **When a fix contradicts the plan**, change the plan row and re-check the next three rows.
- **When a fix reveals a bible gap** — an unnamed thing, an undefined rule, a social fact the
  scene assumed — add it to `bible/world.md`, `bible/society.md` or `bible/lexicon.md` in the same
  pass, and say so.
- **When Pass 3 finds a knowledge gap**, prefer the cheap fix in this order: give the line to
  someone whose map covers it · have the character ask their referral · let them be *wrong* about
  it, which usually improves the scene · and only last, add the domain to their map, which is a
  permanent change to who they are.

Set `status: revised` in the frontmatter when every pass is clean.

## Reporting

Two lines, unless something structural was rewritten:

```
Revised ch 42 — delivers: Dael now owes the house a favour he cannot pay.
Cut a crowd-reaction paragraph, applied Dael's rung-3 voice delta, replaced the ending
(it ran three paragraphs past the hook).
```

**Lead with what the chapter delivers.** Do not report a word count or a word delta — it is not a
quality signal, and putting it in the report is what trained the drafting model to aim at it.

If a pass found nothing, do not list it. If Pass 6 found something, **always say what** — the user
needs to know that the default was reaching for it. If the mechanical sweep did not run, say so;
and if any pass ran at checklist depth without its card open, name it. A ticked box that was never
checked is the failure mode the whole gate exists to prevent.

## Standalone use

`/novel-revise <n>` runs the gate on an existing chapter. Run the three commands first — they
replace most of the loading:

```bash
python3 scripts/sw.py lint novels/<slug> -c <n>
python3 scripts/sw.py cast novels/<slug>
python3 scripts/sw.py state novels/<slug>
```

Then load that chapter, its CCS block, the two before it, the matrix rows in
`bible/cast/_voices.md` and the competence rows in `bible/cast/_competence.md` for its speakers,
and the profiles of everyone in it. Then run all the passes.

## Revising a range

`/novel-revise 1-5` is large enough to hit a session limit partway through. Expect to resume, and
finish one chapter completely — including its `stamp` — before starting the next, so a partial run
leaves whole chapters behind it rather than a half-revised one.
