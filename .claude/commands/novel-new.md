---
description: Start a new webnovel — interview, then scaffold novels/<slug>/
argument-hint: "[optional: a one-line premise]"
---

Start a new webnovel.

If `$ARGUMENTS` is non-empty, treat it as the user's premise and skip the opening question.

Invoke the `novel-init` skill and follow it exactly:

1. Get the premise in the user's own words (or from `$ARGUMENTS`).
2. Run the structured interview with `AskUserQuestion`, batched, at most 6 rounds. Lead each
   option list with your recommendation for this premise.
   - Round B is `mc-design`: gender, appearance, intellect, origin, golden finger — **every one
     of those five carries a "Surprise me" option**, which generates three premise-derived
     candidates rather than a random pick.
   - Round C is `lead-interest`, and it runs **only after** the MC exists. Offer every
     configuration; never infer the lead's gender from the MC's.
3. Copy `novels/_template/` to `novels/<slug>/` and fill in every file in the order the skill
   specifies — `novel.md` first, then bible, MC, love interest, rest of cast, arc plan, chapter
   list, state seeds.
4. Delete the files that do not apply: `bible/canon.md` for non-fanfic,
   `bible/power-system.md` for a genre with no power system, `state/body.md` if nothing in the
   novel changes form. If `mc.form_locked` is true, fill `body.md` completely — every stage, its
   absolute limits, and its transition chapter — before any chapter is written.
5. Report: the tree, the blurb, the first 12 chapter titles, the MC in a paragraph (tier, blind
   spots, origin, advantage and the problem it creates), the form stages if locked, the love
   interest and what they want that is not the MC, which optional skills are on, and three
   decisions you made for them.

Do not start writing chapter 1 in this command. End by telling the user that `/novel-write`
begins it and `/novel-toggle` changes any option.
