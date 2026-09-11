---
name: lead-interest
description: Choose and design the primary love interest, in any configuration. Use during novel-init right after mc-design, and when a new primary lead is introduced mid-novel.
owns: [primary-lead]
---

# lead-interest

**Gate.** Applies if `novel.md` → `content.romance` is `subplot` or `central`. If `none`, skip
entirely and do not introduce a love interest by default — a novel with no romance is a valid
novel and the corpus's habit is to add one anyway.

**Hard ordering dependency: run this after `mc-design`.** The lead is built as a counterweight to
a specific person; designing them before the MC exists produces a generic love interest, which is
the failure this skill exists to prevent.

`romance-arc` handles the *structure* of the romantic line — beats, obstacles, timing. This skill
handles *who they are*. Both respect `no-harem` and `bias-guard`.

---

## Step 1 — Configuration

Ask this only after the MC's gender is recorded. Present the default first, and make every option
equally available — do not treat any configuration as the one needing justification.

| MC | default offered | also offered |
|---|---|---|
| male | **female lead** | male lead · non-binary lead · no romance · decide later |
| female | **male lead** | **female lead** · non-binary lead · no romance · decide later |
| non-binary | ask directly | any configuration |

"Decide later" is a real answer, and often the right one: the lead can be chosen from characters
who already exist once the story has run 20 chapters, which almost always produces a better
relationship than one designed in advance. If chosen, set `romance.configuration: undecided` and
revisit at the first arc boundary.

Record `romance.lead_gender` and `romance.configuration` in `novel.md`.

## Step 2 — The counterweight principle

The lead is not "someone who suits the MC". The lead is **the person whose existence makes the MC
harder to be.**

Build them against the MC's sheet, explicitly:

| MC has | lead should |
|---|---|
| blind spots (`mc.blind_spots`) | see clearly in at least one of them, and say so |
| competence domains | be better than the MC at something the MC values, demonstrably |
| a Lie | not share it — ideally, have built their life against it |
| a want | want something that competes with it, at least sometimes |
| a tier | not be measurably dumber. A lead who exists to be impressed is furniture |

The last row is the one that goes wrong most often. `mc-intel-meter` forbids making other
characters stupid to elevate the MC; that rule applies here with double force, because the corpus
default is a lead whose entire characterisation is *reacting to him*.

## Step 3 — Design the character

Write a full profile (`character-profile`). No shortcuts — the lead needs everything a
deuteragonist needs. Set `role: deuteragonist` if `content.romance: central`, else `supporting`.

Mandatory, beyond the standard template:

- **A goal with a deadline that has nothing to do with the MC**, active in arc 1, that the reader
  can watch them pursue. If the honest answer to "what does she want?" is "him", start over.
- **A life that predates the MC** — obligations, debts, people, a reputation, a job. They were
  mid-story when the MC arrived.
- **A reason to say no.** Something real that makes the relationship costly for *them*. This is
  the romantic plot's engine; without it there is only delay.
- **Their own five-rung ladder**, with a development rate. If `central`, rate 4–5.
- **The two-sentence version of their view of the MC** — including what they find irritating,
  wrong, or worrying. Affection without a specific criticism reads as worship.
- **How they are introduced.** Not by appearance. By what they are in the middle of doing, badly
  or well (`bias-guard`).

## Step 4 — First meeting

Plan it as a chapter row, not as an event that will happen eventually.

- **The first impression should be wrong** in a way that takes chapters to correct — in either
  direction. Instant accurate mutual recognition removes fifty chapters of material.
- **They meet over something else.** Both are pursuing their own goals; the meeting is friction,
  not destiny.
- **The MC is not automatically interesting to them.** Whatever draws them in is specific, stated,
  and comes later.

Record the introduction chapter in `romance.lead_introduced_ch` and open a `relationship` thread
in `state/threads.md`.

## Additional leads

`no-harem` (on by default) allows **one active romantic line at a time**. If the user asks for a
second lead:

- With `no-harem: on` — a second *candidate* is fine; a second *active line* is not. One resolves,
  or one is unrequited and is dealt with honestly. Say this plainly rather than quietly refusing.
- With `no-harem: off` — every additional lead needs this skill run in full, independently: their
  own goal, their own reason to say no, their own ladder. Multi-partner stories are harder, not
  easier, and the arrangement itself has to be examined rather than assumed.

## Mid-novel use

When a lead emerges from the existing cast rather than being designed up front — usually the best
outcome — run steps 2 and 3 retroactively against their existing profile: check the counterweight
table, add the reason to say no if it is missing, and give them a goal with a deadline if their
arc has quietly collapsed into the MC's.

## Self-check

- [ ] Configuration chosen by the user, not inferred from the MC's gender
- [ ] The lead is better than the MC at something the MC values
- [ ] The lead sees clearly in at least one of the MC's blind spots
- [ ] They have an on-page goal with a deadline unrelated to the MC
- [ ] They have a real reason to refuse the relationship
- [ ] They have their own ladder and development rate
- [ ] They are introduced by action, not by appearance
- [ ] Their view of the MC includes a specific criticism
- [ ] `no-harem` and `bias-guard` checks pass
