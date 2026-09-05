---
name: social-fabric
description: Build the society layer of the world — labour, money, law, knowledge, belief and mobility — and propagate the central magic or technology rule into ordinary life so the setting behaves like a place people live in rather than a stage. Use at novel-init after the power system or tech is defined, when the story enters a new social layer, and when the world starts feeling like a backdrop.
---

# social-fabric

`bible/society.md`. The connective tissue between the world's **central rule** (magic, technology,
canon) and the **daily life** a scene can be set in.

The defect this exists to prevent: a world with a spectacular magic system whose peasants,
markets, laws and marriages are indistinguishable from generic medieval-Europe wallpaper. If
levitation exists and nobody has invented a better way to move grain, the world is a stage set,
and every reader feels it without being able to say why.

Same discipline as `story-bible`: **consistency, not completeness.** A fact belongs here only if
it can constrain a scene, be contradicted, or recur. Target **600–1,000 words** at init.

---

## 1. The six load-bearing questions

Answer in one or two sentences each. This is the whole file's spine.

| # | question | what it buys the story |
|---|---|---|
| 1 | **Labour** — what do most people do all day, and who does the work nobody wants? | every crowd scene, every walk-on's three strokes |
| 2 | **Money** — what is wealth made of, and how does an ordinary person fall out of it? | stakes with numbers; debt plots |
| 3 | **Violence** — who may legitimately hurt whom, and what happens when someone else does? | tells the reader what a fight *costs*, socially |
| 4 | **Knowledge** — who is allowed to learn, what is written down, how does news travel and how fast? | governs every plan, secret and reveal (`mc-intel-meter`, `plot-threads`) |
| 5 | **Belief** — what do people think the world is, and what do they do on the days that matter? | ritual, oaths, taboo — the cheapest authenticity there is |
| 6 | **Mobility** — can a person change their position, and by which route? | whether the MC's ambition is even legible to the people around them |

Question 4 is where the society layer meets the cast: it decides **who was allowed to become
competent at what**, which is the constraint `competence-map` builds individual maps inside. What
costs money to learn, what is guild secret, what is only ever spoken aloud, who is barred from the
schools — those answers assign the whole cast's expertise before any single character is designed,
and in a world with 8% literacy the number of people who could have read that ledger is a plot
constraint rather than a background detail.

It is also the one most drafts skip and most need: **information speed is a hard constraint.**
Write down how long news takes to cross the map, and never let a plan violate it.

## 2. The propagation test — the core procedure

Take each numbered rule from `bible/power-system.md`, `tech-plausibility`, or `bible/canon.md`,
and force it down through three layers. Do this **once per central rule**, at init, and again
whenever the rule changes.

| layer | ask |
|---|---|
| **Institution** | who monopolised this, who regulates it, who is licensed and who is outlawed |
| **Market** | what job exists because of it; what it made cheap; what it made expensive |
| **Household** | what an ordinary family does differently at dinner because of it |

Then two inversions, which are where the good material is:

- **What died.** Name one occupation, craft or institution this rule made obsolete — and one
  person still doing it anyway.
- **What it cannot do.** Every rule has a limit (`power-system` guarantees one). Name the
  workaround ordinary people use where the rule stops. That gap is where most plots live.

```
rule        Healing magic works only within an hour of the injury.
institution Temples own the fast-riders. A licence to ride is worth more than the healing.
market      Bone-setters extinct in cities, thriving in the hills. Roads got obsessively good.
household   Nobody works alone. Working alone is how a farmer dies of a broken leg.
died        The old surgeons' guild — one still practices, and takes the cases that arrive late.
gap         Illness. Magic does nothing for a slow disease, so the world fears fevers, not blades.
```

That gap sentence is worth more to the novel than three pages of history.

## 3. The unevenness rule

Societies are not uniform, and a uniform one reads as fake in one paragraph.

- **Every rule has an exception with a name.** The prohibition and the person who is quietly
  exempt from it.
- **Class changes the same fact.** One law, three experiences: what it means to the licensed, the
  tolerated, and the excluded. Write the excluded layer explicitly — it is where the MC's costs
  come from and where most stories forget to look.
- **Geography changes it too.** The capital's version, the provincial version, the version at the
  edge where nobody enforces anything.
- **Nothing is symmetrical.** Not five equal houses; one dominant, one dying, one denied.
- **Somebody is losing.** A society with no group actively being squeezed has no plot in it.

## 4. Counter-pressure

For every institution, record **who resists it and how they survive doing so.** Black markets,
unlicensed practitioners, folk custom that outlasted the law, the thing everyone does that is
technically illegal. This is what makes a world feel governed rather than designed — and it
supplies antagonists and allies who want something legible (`conflict-engine`, `mtl-detox`'s ban
on cannon fodder).

## 5. Bias floor — non-negotiable

`bias-guard` governs this file absolutely, and this is the file where the genre corpus's defaults
do their damage.

- No culture, faction or class is uniformly anything, and none maps onto a real-world ethnic or
  national group — not as a villain, and not as a noble-savage or wise-mentor culture either.
- Social structures are **historical, not essential**: a group's position comes from law, capital
  and violence, never from what its members inherently are. If a text implies otherwise, it is a
  defect.
- Where the setting includes oppression, it is **depicted, not endorsed**: someone benefits,
  someone resists, and the narration takes no position that a person's worth follows their rank.
- Invented prejudices need the same handling as real ones — they must cost someone something on
  the page, and they belong to characters, never to the narrator.

## 6. When to write, when to grow

**At `novel-init`**, after the power system or tech: the six questions, one propagation test on
the single most important rule, and the social layer arc 1 actually enters. Nothing else.

**Grow it when:**

| trigger | add |
|---|---|
| The story enters a layer it has not shown (court, slum, army, temple, ship) | that layer's version of questions 1–4, half a page |
| A chapter invents a durable social fact | record it — via `continuity-summary`'s `set>` line |
| A new rule enters the power system | one propagation test |
| A plan turns on how fast news travels | make question 4 explicit and numeric |
| Two chapters contradict each other on a custom | resolve it here, and note which chapter was right |

**Never** write the layers the story will not enter. A novel set entirely in one city does not
need its neighbours' inheritance law.

## 7. Getting it onto the page

This file is **not** for direct exposition. Almost everything here reaches the reader as channel 1
or 2 in `world-texture`: a rule biting someone, or a character working around it.

| social fact | how the reader gets it |
|---|---|
| Licences are monopolised by temples | a character with no licence takes the long road |
| The excluded class may not testify | the MC's witness is useless, and everyone knew it but the MC |
| News takes nine days from the capital | an order arrives that everyone has already stopped obeying |
| Bone-setters are extinct in cities | a broken arm in chapter 6 is a catastrophe, not a scene of healing |

Write the fact here. Let the chapter deliver the consequence.

## 8. Genre notes

**Fantasy.** The power system decides who rules; this file decides what that does to everyone who
does not. Run the propagation test on every hard rule.

**Scifi.** Second-order social effects *are* the genre — `tech-plausibility` owns the one central
speculation, this file owns what it did to work, money and family. Run the two inversions hard.

**Fanfic.** Do not restate the source's society. Record only (a) social facts canon leaves blank
that this story needs, and (b) what the divergence changed. Flag anything invented here as
non-canon so `fanfic-canon` can audit it.

**Progression / cultivation.** The most abused case: a power ladder with no economy under it.
Ask who feeds the sects, what a spirit stone buys in bread, and what happens to the ninety-nine
percent who never cultivate. Answering that one question separates the genre's good books from
its bad ones.

## Self-check

- [ ] Six questions answered, none longer than two sentences
- [ ] The central rule has been propagated to institution, market and household
- [ ] One obsolete occupation named, and one person still doing it
- [ ] The rule's gap named — what people do where it stops working
- [ ] Every rule has a named exception; the excluded layer is written, not implied
- [ ] Counter-pressure recorded for each institution
- [ ] Information speed is explicit
- [ ] Nothing is symmetrical; somebody is losing
- [ ] No culture uniform, essentialised, or mapped onto a real-world group (`bias-guard`)
- [ ] Nothing in this file has been dumped into a chapter as exposition
- [ ] Under 1,000 words, and every entry could be contradicted by a scene
