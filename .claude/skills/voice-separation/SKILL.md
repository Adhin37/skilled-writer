---
name: voice-separation
description: Keep the cast distinct as minds - speech, thought and body pinned to a voice matrix, not the MC's register. Use when designing a character, before any multi-speaker scene, and inside revision-pass.
metadata:
  type: skill
  tier: character
  force: structural
  when: always
  owns: [voice-matrix, mirror-clause, transplant-test, default-gesture-set, first-move, drift-check]
---

# voice-separation

The default failure of AI-written fiction is not bad dialogue. It is **one mind wearing several
names**. Every character ends up as quick as the MC, as articulate as the MC, as wry as the MC —
because the model writes the smartest line it can for whoever is speaking, and the MC is the
calibration point.

`dialogue-voice` gives a character a *surface* — contractions, a vocabulary tell, a syntax tic.
Those are labels on identical minds. This skill supplies the layer underneath: **how much this
person can work out, how well they can say it, whether they find any of it funny, and what their
body is doing meanwhile.** Get that right and the surface fingerprints stop being decoration.

One exception, and it is deliberate: copies of a person may sound like that person. See §7.

---

## Sections that live in `references/`

Section numbers are stable — other skills cite them — so the gaps below are deliberate. Open one
when its trigger fires, not by default.

| § | file | open it when |
|---|---|---|
| 2 | `references/worked-example.md` | the axes feel abstract and you want five people answering one question |
| 4, 5 | `references/channels.md` | drafting a scene: how a body identifies its owner, and how a non-POV mind is shown without entering it |
| 7 | `references/mirror-clause.md` | a clone, avatar, double or body-snatch is on the page. This is the one exemption from §3 |
| 3 | `references/age-register.md` | the cast contains a child, an adolescent or a notably old character — the cadence differences no axis in the matrix measures |

The revision-time check is `references/audit-card.md`, opened by `revision-pass` Pass 2.

## 1. The cast voice matrix

Six axes. Every tier-A and tier-B character gets a row in `bible/cast/_voices.md`, and the same
values live in their profile. One table, one screen — because sameness is a property of a *cast*
and is invisible when you read profiles one at a time.

| axis | values | what it changes on the page |
|---|---|---|
| **intel** | 1–5, the `mc-intel-meter` ladder | how many steps they arrive at, and how many they skip |
| **artic** | 1–5, below | whether they can put it into words |
| **wit** | none · dry · warm · clowning · cruel | what they do with pressure |
| **heat** | flat · banked · quick · volatile | sentence length and what breaks first |
| **turn** | a number of words | their default speaking turn. Mechanical. Hold it |
| **body** | one hand-habit + one pressure move | the tag-free identification (§4) |

### Intelligence — reuse the tier ladder

The five tiers in `mc-intel-meter` apply to the whole cast, not just the MC. Same meanings, same
inference budget, same rule that a tier is **reconstructible**: whatever a character skips, an
attentive reader could have derived.

The MC's tier is declared in `novel.md`. Everyone else's is declared here, and the cast must
**straddle** it — see §3.

### Articulacy — the axis that does the most work

| artic | speech |
|---|---|
| 1 | Concrete nouns, abandoned sentences. Points, does not explain. |
| 2 | States the fact, never the reason. Short declaratives. |
| 3 | Ordinary competent speech. Explains when asked; fumbles abstractions. |
| 4 | Fluent. Builds an argument inside one turn. Chooses words. |
| 5 | Persuasive at will. Can make a wrong thing sound right. |

**Intel and articulacy are independent, and the pairing is the character.** This decoupling is the
single most effective cure for a cast that all sounds like the protagonist.

| pairing | who they are | why they are useful |
|---|---|---|
| **high intel / low artic** | right, and cannot prove it | their frustration is a plot engine; the MC must interpret them |
| **low intel / high artic** | wrong, and convincing | the best non-villain obstacle in fiction; nobody can refute them fast enough |
| **high / high** | dangerous | use once. If it is the MC, somebody still out-argues them in their own domain |
| **low / low** | the literal one | correct about physical things everyone clever has abstracted past |

### Wit — a fingerprint, not a default

Assign real wit to **at most two** of the recurring cast. If everyone is funny, nobody is, and the
narration has no register left for an actual joke.

| wit | the shape | name the trigger |
|---|---|---|
| none | says the thing | — |
| dry | understatement, delivered flat, never signposted | usually danger |
| warm | jokes that include the other person | usually affection they will not state |
| clowning | volume and self-deprecation | usually fear |
| cruel | accurate, and aimed | usually loss of control |

Every joker jokes **at a specific pressure**. Record it. A character who is funny at uniform
intensity is a comedian, not a person. And the joke should be doing a second job: it says the
thing they cannot say straight.

If `optional.comedy-levity` is `on`, that skill governs the scene-level comic beats; this axis
still governs *who* is allowed to make them.

### Heat

| heat | under pressure |
|---|---|
| flat | nothing changes. The unnerving one |
| banked | shorter, more precise, then one sentence too honest |
| quick | interrupts, overlaps, answers before the question ends |
| volatile | floods, repeats, escalates, then stops dead |

### Turn length

Give each recurring character a default word budget per speaking turn — 4, 12, 25, 40 — and hold
it. It is the crudest device here and the most reliable: two characters with the same turn length
read as the same person no matter how carefully their vocabulary differs.

---

## 3. The separation rules

```bash
python3 scripts/sw.py cast novels/<slug>
```

The first four rules below are arithmetic over the matrix, and this settles them outright:
the straddle, the wit cap, the three-way clash, plus turn-length and hand-habit collisions.
Run it whenever a row changes, and at every arc rollup. The transplant test is not in it —
that one needs the chapter.

**It checks the table, not the prose.** A well-formed matrix that the drafted dialogue ignores
passes this command and fails the book, which is why Pass 2 still opens this file.


**The MC-contrast rule.** Every chapter contains at least one speaker who differs from the MC on
**two or more axes**. This is the rule the user's complaint is actually about. A chapter where
everyone matches the MC's intel and articulacy has one character in it.

**The three-way clash.** No two speakers in a scene may match on intel **and** artic **and** wit.
If they do, one of them has no reason to exist separately: re-cast them, or merge them.

**The transplant test.** Take the MC's most characteristic line in the chapter and put it in
another named character's mouth. If it fits, one of the two has no voice. Rewrite the other one —
not the MC.

**The cadence test — transplant the *shape*, not the line.** The matrix separates minds. It does
not separate **rhythm**, and rhythm is the drafter's own and leaks into everybody. Compare the
longest turn of any two speakers in the scene and ask whether they are built the same way: same
clause count, same place the sentence turns, same landing. If yes, they are one voice wearing two
rows however far apart their declared axes sit.

Benchmark run #3 is the worked case. A mother at `intel 3 / artic 4` and her six-year-old daughter
at `intel 4 / artic 3` passed `sw cast` cleanly — different rows, no clash — and read as the same
person, because both built every turn the same way: **a long balanced sentence, then a short flat
one landing on a bare assertion.** Mother: *"No. It really isn't. It's just true."* Daughter:
*"It smells like Tuesday. Same as every Tuesday."* Two rows, one rhythm. (What was *in* those
turns is `dialogue-voice` §How it sounds spoken; this test is only about their shape.)

**Give each recurring speaker one cadence and write it in their profile** — floods then stops ·
builds in even clauses · starts flat and sharpens · never finishes · answers before you finish
asking. Then hold it. No script can check this: the axes are numbers and cadence is a shape, so
it is read for, at the arc rollup and in `revision-pass` Pass 2.

**Straddle the MC.** Across the recurring cast, at least one character is above the MC's intel tier
and at least one is below. `mc-intel-meter` already requires the antagonist to reach or exceed the
MC once per arc and an ally to out-think them in their own domain; this is the same requirement
stated as a cast property.

**The conversational blind spot.** Every recurring character is *unable* to do one thing the MC
does easily — hold an argument, stay quiet, lie, ask for something, be direct, be funny. Record it
as the eighth speech field's cousin: `what they never say` is content; this is capability.

**Ordinary is a legitimate setting.** Most people in most novels are intel 2–3, artic 3, wit none.
That is not a flaw to be corrected. A cast of exceptional talkers has no floor, and without a floor
the exceptional ones do not read as exceptional.

---

## 6. Anti-convergence over a long serial

Start the drift check with `sw cast`: if two rows have converged on paper, it says so before you
read a line. What it cannot see is the commoner case — rows that still differ while the dialogue
under them has quietly merged. For that, the side-by-side below is the only instrument.


A 300-chapter serial converges by default. Voice deltas (`character-development`) all push the
same way — shorter sentences, fewer hedges, more directness — and by chapter 200 the cast has
merged into the MC.

**A voice delta may not move a character onto the MC's axes.** If a rung advance would raise a
character's articulacy to the MC's level, or grant them the MC's wit, pick a different delta.
Growth has many directions: a character can become *more* oblique, *slower*, *quieter*, *funnier
in a worse way*. Only one exception — if a character genuinely becoming like the MC is the point of
their arc, someone on the page says so, and it reads as loss or as threat.

**The drift check, once per arc.** Read one line from each recurring character, from the most
recent chapter they appeared in, side by side. If the axes have compressed, restore them and note
it in `state/growth.md`.

---

## 8. Where this runs

| moment | what happens |
|---|---|
| `character-profile`, any tier | assign the axes before writing a line. Tier A full row + thought fields; tier B intel/artic/wit/turn + hands + pressure; tier C one off-default axis |
| `mc-design` | the MC's tier is `mc.intel_tier`; the rest of their row goes in the profile like anyone's |
| `write-chapter` step 1 | load the matrix rows for this chapter's speakers; confirm the MC-contrast rule before drafting |
| `write-chapter` step 2 | hold turn lengths and body idioms while writing; beats come from the hands field |
| `revision-pass` Pass 2 | transplant test, three-way clash, banned-beat sweep |
| `character-development` | every voice delta checked against §6 |
| `chapter-plan`, new arc | when a new recurring character is introduced, place them on the matrix relative to the existing cast, not in isolation |

**Tier C.** A walk-on gets no matrix row. They get **one axis off default** — the one who will not
stop talking, the one who answers in three words, the one who thinks this is funny — which costs a
clause and is the difference between an extra and a function. Tier D gets nothing.

**`bias-guard` outranks this skill.** Low intelligence and low articulacy are never carried by
accent, dialect spelling, ethnicity, class, body, or age, and a low-intel character never exists
to be corrected — they are right about something concrete, and they are competent at their own
work. `mc-intel-meter`'s floor applies in reverse too: nobody is written stupid to make the MC
look smart.

## Self-check

- [ ] Every speaker in this chapter has matrix values, or is a tier-C with one off-default axis
- [ ] At least one speaker differs from the MC on two or more axes
- [ ] No two speakers in a scene share intel + artic + wit
- [ ] Transplant test: the MC's best line does not fit anyone else's mouth
- [ ] Turn lengths held; nobody drifted toward the MC's
- [ ] Every action beat is that character's, not from the banned gesture set
- [ ] Non-POV minds shown through first moves, not interiority
- [ ] POV narration uses that POV's thought unit as its metaphor source
- [ ] Any voice delta applied does not move a character onto the MC's axes
- [ ] Mirrors declared with `mirror`, `convergence` and `diverged_ch`; the tell is named
- [ ] No difference carried by accent, dialect spelling or a demographic marker
- [ ] No non-POV character got a marked `'…'` thought
