---
type: reference
owner: social-fabric
description: "building the society layer, or the cast's men and women move through the world identically and read as one another with different names"
---

# Gendered experience — position, not temperament

Open this when building the society layer, when a cast's men and women move through the world
identically, or when two characters of different genders are reading as the same person with
different names.

---

## What this file is for, and what it refuses to do

A cast whose men and women behave identically is flat, and the reader feels it as a world that has
not been thought about. That complaint is real and this file answers it.

It answers it with **position**: what this society expects of each gender, what it permits, what it
punishes, and what each specific character does about that. Not with **temperament** — no trait
defaults, no "women feel more", no emotional-versus-analytical split. Three reasons, in order of
how much they cost you:

1. **A temperament rule collapses the cast into two voices.** Give every woman one processing style
   and every man another and you have written two characters and copied them, which is the exact
   defect `voice-separation` exists to prevent. Benchmark run #3 hit the same shape by accident: a
   mother and her daughter, different matrix rows, one cadence, and a reader called it immediately.
   A second, gendered template would not fix that — it would systematise it.
2. **It is not true, and untrue things write badly.** There is no established population difference
   in general intelligence by sex. What differs, hugely and visibly, is what each gender is
   *permitted to express without cost* — and that is dramatic, specific, and different in every
   society you invent. Temperament flattens; permission generates scenes.
3. **`bias-guard` owns this and overrides everything above it**, including genre convention and
   author instruction — `CLAUDE.md` hard rule 14. Its §Gender already rules out the gendered
   competence split outright. This file stays on the right side of that line and is useless if it
   does not.

The payoff is that position gives you **more** differentiation than temperament, not less, because
it varies by society, by class, by scene, and by each character's stance.

## 1. Declare the terms, per novel

Gender norms are a setting, not a constant, and they are not the same in Konoha, Gormenghast and a
generation ship. Answer these in `bible/society.md` §Gendered terms, in one line each. Where the
answer is "no difference", write that — it is a real answer and it must then hold everywhere.

| question | what it decides on the page |
|---|---|
| **Labour** | which work is coded whose; who is paid less for it; who can hold the licence rather than do the job |
| **Law & property** | who inherits, who signs, who testifies, who needs a guarantor to do either |
| **Violence** | who may carry, who may use force and be excused, who is blamed for force used on them |
| **Speech** | who speaks first, who is interrupted, whose anger reads as authority and whose as instability |
| **Mobility & risk** | who moves alone, at what hour, at what cost, and who plans routes around it |
| **Care** | who is assumed to do it, who is praised for doing any, what it costs a career |

Then run `social-fabric` §2, the propagation test, on the answers exactly as you would for the
central rule: a norm that has not reached labour, money and law is set dressing.

## 2. The stance table — the anti-template device

**This is the part that stops the above becoming two templates.** The society's expectation is
uniform; what a person does about it is not. Give every tier-A and tier-B character one stance, in
their profile, and two characters of the same gender will behave nothing alike:

| stance | how it shows up |
|---|---|
| **conforms, benefits** | fluent inside the rules, genuinely comfortable, and slow to see the cost to others |
| **conforms, resents** | does it correctly and bitterly; the resentment leaks sideways onto safer targets |
| **exploits** | is underestimated on purpose and trades on it; the most fun to write and the most dangerous to be near |
| **defies openly** | pays the posted price and keeps paying; everyone knows where they stand |
| **defies quietly** | passes, and the cost is the constant management of being found out |
| **oblivious** | has never had to notice, which is itself the position; reads objections as bad manners |
| **enforces** | polices it on others, often harder than the people it privileges — frequently the sharpest antagonist available |

A "tomboy" is not an exception to a rule here. She is one stance — *defies openly*, or *exploits* —
and so is the man who will not fight, and neither needs a special case. That is the test of whether
a model is a template: if it needs exceptions, it is one.

**Stance is not gendered.** Any character of any gender takes any row. Two women, one *enforces* and
one *exploits*, are further apart than a man and a woman who both *conform*.

## 3. How it reaches dialogue

This is the half the complaint is usually about, and all of it is **interaction**, visible on the
page, and countable:

- **Who holds the floor.** Who speaks first, who yields, who is interrupted, and — the real tell —
  who reclaims the floor afterwards and who lets it go. `sw lint` counts interruptions; it cannot
  tell you who is doing the interrupting, so decide it deliberately.
- **Direct or routed.** What each character can ask for plainly, and what they must route through a
  hint, a joke, or a third party. The same request, differently shaped, is instant characterisation.
- **What costs credibility to say.** *"I'm frightened"*, *"I want your job"*, *"I don't know"* — each
  is priced differently depending on who says it in front of whom. Price them, then let a character
  pay.
- **Who is believed without evidence**, and who produces the evidence anyway because they have
  learned they will be asked for it.
- **Who manages the room.** Smoothing, apologising, refilling, noticing the upset person. If this
  always lands on the same character, that is a fact about the society — make it one deliberately,
  and let somebody resent it — rather than an unexamined habit of the drafter.

## 4. Emotion, done honestly

Not *who feels more*. **Who is allowed to show what, and what it costs them when they do.**

Take four — anger, tears, fear, ambition — and set, per society and per character, the price of
displaying each in public, in private, and in front of a superior. The interesting writing is
almost always in the mismatch: the character who has the feeling their position does not price, and
has to route it somewhere else. A man with no permitted vocabulary for fear expresses it as
contempt. A woman whose anger is read as hysteria learns to deliver it cold and gets called
calculating for that instead.

That is the texture the "women are more emotional" shortcut is reaching for, and it is better,
because it is specific, it differs per character, and it generates scenes rather than labels.

## 5. Self-check

- [ ] `bible/society.md` §Gendered terms answers all six, or says "no difference" and means it
- [ ] The norms reached labour, money and law, not just manners (`social-fabric` §2)
- [ ] Every tier-A and tier-B character has a stance, and two characters of the same gender differ
- [ ] No trait follows from gender alone anywhere in the bible
- [ ] The competence map's `none` rows still do not sort by gender (`bias-guard` §Structural checks)
- [ ] Somebody benefits from the arrangement and is sympathetic anyway; somebody enforces it who is
      not a villain
- [ ] Emotional labour in a scene was assigned on purpose, not by default
