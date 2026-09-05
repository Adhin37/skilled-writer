---
description: Turn optional skills on or off, or change any novel setting
argument-hint: "[e.g. 'romance-arc on' | 'mc tier 4' | nothing, to see everything]"
---

Change the active novel's configuration in `novel.md`.

If `$ARGUMENTS` is empty: show the current settings as a readable table — narration, POV, the MC
block (tier, blind spots, origin, golden finger, form lock), the romance configuration and lead,
the world clock (reactivity, crisis cap, escalation ceiling) and the ending contract, chapter
economy, content boundaries, and every optional skill with `on`/`off` and a one-line description
of what it does. Then ask what to change.

`timeline.reactivity` is the dial to reach for when the user says the story is too easy or too
brutal — raise it for a world that pushes back harder, lower it for a gentler one. If they say
it is too *punishing*, check the governor first: crisis count over cap, reaction latency under 2,
or escalations that opened nothing are the usual causes, and those are bugs rather than settings.

If `$ARGUMENTS` names a setting: apply it and report the before/after.

Optional skills and their keys:

| key | what it does |
|---|---|
| `no-harem` | love interests are people with their own goals *(on by default)* |
| `romance-arc` | structured romantic beats, obstacles and payoff scheduling |
| `combat-choreography` | spatially legible fights with stakes decided in advance |
| `litrpg-system` | game-like status screens, levels and quests, under strict discipline |
| `mystery-clues` | fair-play clue ledger and reader-vs-detective knowledge gap |
| `comedy-levity` | scheduled, character-sourced humour |
| `grimdark-consequences` | no plot armour; losses stay lost |
| `slice-of-life-texture` | downtime, work and routine that make the stakes concrete |

`bias-guard` and `mtl-detox` are **not** toggleable. If asked to disable them, say plainly that
they are not optional, and offer instead to adjust `content.rating`, `content.violence` or
`content.hard_limits`, which are the real knobs for how harsh the story is allowed to be.

**Warn before changes that are expensive mid-serial**, and say why in one line:

- `pov.mode` or `narration.person`/`tense` — every prior chapter is now inconsistent
- `mc.intel_tier` — past chapters established a level of competence readers have calibrated to
- `chapters.target_words` — readers form expectations from the first ten chapters
- `mc.gender` / `mc.pronouns` — every written chapter now misgenders the MC
- `mc.origin` or `mc.form_locked` — changes what the MC's body could do in every prior chapter;
  if turning `form_locked` on mid-novel, build the stage table backwards from what has already
  been described, and say which chapters now conflict
- `romance.lead` — changing the lead after they have been introduced is a story decision, not a
  setting; route it through `/novel-plan` instead

If the user confirms, apply it and note the change with its chapter number in `novel.md` under a
`# Configuration changes` heading, so later chapters know when the shift happened.
