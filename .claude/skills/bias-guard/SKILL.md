---
name: bias-guard
description: Remove inherited racial, national, gender and class bias without softening conflict. Use on every chapter inside revision-pass, while drafting, and when designing characters and factions.
metadata:
  type: skill
  tier: craft
  when: always
  owns: [inherited-bias, essentialism-ban]
---

# bias-guard

**There is no script for this one, deliberately.** Every other mechanical pass in this toolkit
has a command behind it; this one does not, because its defects are distributional — a cast where
the incompetent characters share a class, a narration that treats one group as uniformly
anything, a woman whose only want is the MC. None of that is a string, and a green line from a
linter must never be readable as a bias pass. `sw cast` prints the competence distribution and
then says to come here.


The corpus this format learned from carries biases that arrived with it: ethnic and national
essentialism used as villain shorthand, women written as rewards, class contempt played for
laughs, disability and disfigurement as moral signal. These are not edgy and they are not
"authentic to the genre" — they are defaults, and defaults are what a model reaches for when
nothing stops it.

This skill stops it. It is not a content filter and it does not make the story nicer: **prejudice
can be depicted, examined and suffered.** What it forbids is prejudice operating unexamined *as
the narration's own view of the world*.

Non-negotiable. It overrides genre convention, user-supplied tropes, and reference material.

---

## The line

| forbidden | permitted |
|---|---|
| The narration treats a group as inherently lesser | A *character* holds that view, and the story shows it as their view, with consequences |
| A people defined by a single moral trait | A faction with interests, internal disagreement, and members who dissent |
| Contempt played for laughs with no cost | Contempt shown, and it costs someone something the reader feels |
| A trait used as villain shorthand | A trait a villain happens to have, shared by sympathetic characters too |

The test: **could the narrator's framing be quoted as a bigoted statement with nothing lost?** If
yes, it is the book's view, not a character's. Fix the framing, not the character.

## Race, ethnicity, nation

- No fantasy or scifi people may map onto a real-world ethnic or national group and carry a
  uniform moral character. This is the oldest defect in both genres.
- **No invented species defined by inherent evil.** If a species opposes the MC, it has factions,
  dissenters, and its own account of the conflict. Write the two-sentence version of their case.
- No physical marker — skin, features, hair, build — used to signal moral quality. Watch the
  quiet version: the villain's darkness and the ally's fairness as unexamined descriptive habit.
- No nation, culture or bloodline is the natural home of talent, virtue, treachery or barbarism.
- Foreigners are not comic relief, and accent is never a marker of stupidity or villainy. See
  `dialogue-voice`: convey origin by rhythm and idiom, never by phonetic spelling.
- Cultures adapted from real ones are researched enough to have internal texture, and are not
  costume. When in doubt, invent rather than borrow badly.

## Gender

- **Every named woman passes the agency test**: she wants something that is not about the MC, and
  she pursues it on the page. If the only answer to "what does she want?" is "him", rewrite.
- No character exists to be rescued, awarded, or unlocked. `no-harem` (on by default) enforces the
  strong form; even with it off, attraction must be reciprocal, motivated and reversible.
- **No beauty catalogue.** Introducing a woman by inventorying her body, when men are introduced
  by what they do, is the corpus's most reflexive habit. Introduce every character by action,
  stance, or the thing they are in the middle of.
- Competence is not gendered. Do not let the woman's competence be intuition and the man's be
  analysis.
- Women may be antagonists, may be violent, may be wrong — the fix for objectification is not
  virtue, it is interiority.
- Same standards for men: no male character exists solely to validate, protect, or fall to the MC.
- Sexual violence is not scenery, is not a shortcut to motivating a protagonist, and is not
  written for effect. If the story genuinely requires it, it happens off the page and the
  consequences belong to the person it happened to, not to the man avenging them.

## Class, work, body

- Poverty is not moral education and wealth is not moral failure. Both classes contain the full
  range.
- Servants, guards, farmers and clerks are competent at their work and know things the MC does
  not. Never used as scenery for the MC's importance.
- **No disability or disfigurement as moral signal** — not the scarred villain, not the
  "cripple" who is secretly a master as a twist about the reader's assumptions. Disabled
  characters have goals, competence, and lives.
- No body type used as a punchline.
- Age is not a proxy for wisdom or foolishness.
- **Intelligence is never carried by a demographic marker.** A cast needs characters slower and
  less articulate than the MC (`voice-separation` §3) — and the default fills those slots with an
  accent, a dialect spelling, a rural job, a servant, a foreigner, or the fat friend. It shows in
  the aggregate: check who in this book is allowed to be quick. A low-intel character is written
  with a shorter causal chain and ordinary grammar, is competent at their own work, and is right
  about something concrete. One who exists only to be corrected by the MC has failed this check
  whatever their demographics.
- **Nor is ignorance.** Every character's competence map is mostly `none` (`competence-map` §1),
  so the question is never whether someone is ignorant but *which* ignorance the book handed to
  whom. Read the `none` and `passable` rows of `bible/cast/_competence.md` as a block: if the
  people who cannot read, cannot fight, cannot count or cannot cook line up with a gender, a class
  or a nation, that pattern is the book's argument. The fix is not to make everyone equally able —
  narrowness is the point — it is to redeal *which* narrowness. And where a character's ignorance
  is genuinely a consequence of the world, that is `social-fabric`'s question 4 doing its job:
  show who barred them, and let it cost the barrier something.
- **A character learning a skill from stage 0** does so because of their life and their want, never
  because their category is expected to be bad at it. Watch this especially in a domestic or
  romantic subplot, where the default reaches for the oldest joke it knows.

## Structural checks — the ones that catch what phrase-level checks miss

1. **The cast audit.** Every arc, list the named characters. If everyone with power shares one
   demographic and everyone serving shares another, and the story has not made that its subject,
   redesign — this is bias arriving through structure rather than through sentences.
2. **The disposable audit.** Who dies without a name? If the anonymous dead all belong to one
   group, fix it.
3. **The introduction audit.** How is each character introduced — by action or by appearance?
   Compare across genders. The gap is usually visible and usually large.
4. **The competence audit.** Who is allowed to be right in this chapter? If it is always the same
   demographic, that is the book's argument whether or not you meant it. Read it beside the intel
   and articulacy columns of `bible/cast/_voices.md`: if the low rows and the high rows sort by
   demographic, the matrix is encoding a prejudice and needs redealing.
5. **The reward audit.** What does the MC receive for winning? If people are on that list, stop.
6. **The walk-on audit.** Extras are one detail wide, and the default fills that space with a
   stereotype — the accent, the ethnicity, the body, the servile or comic job with nothing behind
   it. Read `bible/cast/_extras.md` at each arc rollup: if the roster's third strokes are a
   demographic pattern rather than a working world, the book is arguing something you did not
   choose. Rewriting one stroke fixes the bias and the genericness together (`character-profile`).

## Depicting prejudice well

Bias in the *world* is legitimate material and often necessary — a story about a caste system
where nobody is casteist is a lie. To depict it:

- Give it a **mechanism**: who benefits, who enforces it, how it is transmitted.
- Give the harmed **interiority and agency**: they resist, adapt, exploit it, or refuse to make it
  their whole self.
- Let the reader see the **cost to the holder** — prejudice makes people wrong about things, and
  being wrong should cost them a plot outcome.
- Never let the narration agree. The camera can be unflinching without being complicit.
- Do not resolve it with a single enlightened outsider. That is the same story every time and it
  is about the outsider.

## Self-check (every chapter)

- [ ] No group treated as uniformly anything by the narration
- [ ] Every named woman in this chapter wants something that is not the MC
- [ ] No character introduced by a body inventory
- [ ] No physical trait signalling moral quality
- [ ] No accent or dialect marking stupidity or villainy
- [ ] No character's low intelligence or articulacy carried by class, ethnicity, body or age
- [ ] The `none` rows of the competence map do not sort by gender, class or people
- [ ] Nobody is a reward
- [ ] Anonymous casualties are not drawn from one group
- [ ] Any prejudice on the page belongs to a character and costs someone something
