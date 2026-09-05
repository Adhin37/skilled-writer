---
name: voice-separation
description: Keep every character distinguishable from the MC and from each other across all three channels — speech, thought and body language — by pinning each one to a cast voice matrix (intelligence, articulacy, wit, heat, turn length, body idiom) rather than letting the whole cast inherit the protagonist's register. Use when designing any character, before writing any scene with two or more speakers, and inside revision-pass. Includes the mirror clause for clones, avatars and doubles, who are permitted to converge.
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

## 2. Worked example — one situation, five people

The strongroom door has been forced. Nothing appears to be missing.

| character | axes | the line |
|---|---|---|
| Rin | intel 4 · artic 3 · dry · banked · turn 8 | "Nothing's gone." A beat. "So it wasn't for the money." |
| Dael | intel 2 · artic 5 · warm · quick · turn 30 | "Amateurs, obviously — they panicked, they ran, they left the good stuff sitting right there. You can read the whole night off the marks on that bar." |
| Mira | intel 3 · artic 2 · none · flat · turn 5 | "Who else has a key." |
| Karth | intel 1 · artic 2 · none · flat · turn 3 | "Kids." He lifts the bar back into its brackets. |
| Marek | intel 2 · artic 3 · clowning · quick · turn 15 | "Well. Somebody's had a better week than me." |

Five people, one fact, no tags needed. Rin skips a step and lands on the pivot. Dael is fluent and
wrong and nobody in the room can out-talk him. Mira does not have a theory and asks the question
that will actually solve it. Karth's causal chain ends at the first explanation, and he acts on it.
Marek is afraid.

Note what is *not* here: no phonetic spelling, no malapropism, no bad grammar. Difference comes
from the shape of the thought, never from mangled English.

---

## 3. The separation rules

**The MC-contrast rule.** Every chapter contains at least one speaker who differs from the MC on
**two or more axes**. This is the rule the user's complaint is actually about. A chapter where
everyone matches the MC's intel and articulacy has one character in it.

**The three-way clash.** No two speakers in a scene may match on intel **and** artic **and** wit.
If they do, one of them has no reason to exist separately: re-cast them, or merge them.

**The transplant test.** Take the MC's most characteristic line in the chapter and put it in
another named character's mouth. If it fits, one of the two has no voice. Rewrite the other one —
not the MC.

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

## 4. The body channel

The most under-used identifier and the cheapest. A reader who has learned a body can tell who
entered a room before anyone speaks.

Three decisions per tier-A character, two for tier B, recorded once and reused:

| field | choose one |
|---|---|
| **default state** | still · restless · occupied (always holding something) · arranged (posed) |
| **the hands** | the one thing their hands do — the single highest-value field |
| **pressure move** | goes still · gets bigger · gets smaller · gets busy · closes distance · leaves |

Plus, for tier A only: **distance** — how close they stand by habit, and what they do when someone
crosses it.

### Rules

**The beat must be theirs.** An action beat any character could perform is dead weight
(`prose-quality` bans it as stage business; here it fails as identification too). Banned as
identifiers, all of them:

*nodded · shrugged · sighed · raised an eyebrow · crossed their arms · ran a hand through their
hair · clenched their jaw · let out a breath · looked away · smiled slightly*

These are the model's default gesture set. They identify nobody. Replace with the character's
hand-habit or cut the beat entirely — a line with no beat is better than a line with a generic one.

**Body contradicts speech.** The most useful thing a beat can do is disagree with the words. *"I'm
not angry," she said, and put the cup down where it had been, exactly, twice.*

**The body is class and culture, not just personality.** Who stands, who sits without being told,
who keeps their hands visible, who does not turn their back — these come from `bible/society.md`
(`social-fabric`), and a servant and a magistrate who share a body idiom have flattened the world
as well as the cast.

**Under a locked form, the ledger wins.** If a character has `form_locked: true`, their body idiom
is expressed within the current stage's limits in `state/body.md`. A reborn child has the habit,
not the reach.

---

## 5. The thought channel

Interiority is restricted by tier — walk-ons never get any (`character-profile`) — so this channel
splits in two.

### POV-eligible characters

Three fields, in the profile, used by `narrator-voice` and `pov-switch`:

| field | values |
|---|---|
| **thought unit** | images · words · numbers · bodies · rules · people · money |
| **thought speed** | ahead of the scene · with it · one beat behind |
| **facing an unknown** | test it · avoid it · name it · ask someone · assume the worst |

The thought unit is also the **metaphor source** (`narrator-voice`): a character who thinks in
money does not reach for a tide simile. Two POV characters who think in the same unit will produce
identical narration however different their dialogue is — that is the head-hopping smell readers
notice without being able to name.

### Everyone else — the first move

No interiority. A non-POV character's mind reaches the page through **what they reach for, look at,
or say first** when the situation changes. One line in their profile: *Karth checks the door.
Dael checks the room's faces. Mira checks the exit she came in by.*

Three characters, one entrance, three minds, zero interiority. This is how the cast thinks
differently inside a single POV.

---

## 6. Anti-convergence over a long serial

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

## 7. The mirror clause — clones, avatars, doubles

Copies of a person are **exempt** from §3. A duplicate is permitted to share the original's
fingerprint, body idiom and thought unit, in whole or in part — that is the premise, not a defect.

**Declaring one.** In the duplicate's profile frontmatter:

```yaml
mirror: rin              # the source character's slug
mirror_kind: clone       # clone | avatar | projection | doppelganger | body-snatch |
                         # split-self | time-double | copy-mind | shapeshifter
convergence: drifting    # identical | drifting | inverted
diverged_ch: 47          # the chapter they became separate people
```

Add a row to the mirrors block of `bible/cast/_voices.md`. If the double has a different body, they
are also `form_locked: true` with a stage row in `state/body.md` (`mc-design`).

| convergence | speech | body | thought | use for |
|---|---|---|---|---|
| `identical` | exact | exact | exact | a projection the original drives directly; a copy in its first chapters; an impostor who has not yet slipped |
| `drifting` | same fingerprint, diverging vocabulary and deltas | same idiom, new habits from a different life | same unit, different conclusions | any duplicate that has lived independently for more than a few chapters |
| `inverted` | the fingerprint pushed to an extreme the original never reaches | the same body used differently | same unit, opposite values | the evil twin; the self the MC refused to become |

### The four rules that make a double interesting

1. **Divergence starts at separation.** From `diverged_ch`, two copies accumulate different
   experiences, and different experiences produce different people. They drift at the duplicate's
   own `development_rate`. A duplicate who sounds identical after thirty chapters of a different
   life is a puppet — legitimate *if the story says so* (a driven avatar, a mind with no
   independent memory), and then say so on the page: someone notices that it never learned
   anything.
2. **Name the tell.** If the duplicate is meant to pass as the original, decide the one thing that
   does not copy — a reflex, a piece of knowledge, a habit acquired after the split, the way they
   handle being touched — and decide **who could notice it**. That is a plot device, and it should
   be planted before it is needed (`plot-threads`). If nothing fails to copy, state that
   deliberately: the horror is that there is no test.
3. **Keep them legible in a shared scene.** When two mirrors are on the page together, the reader
   must be able to tell which is speaking, from a physical tag, position, or a POV anchor — *or*
   the confusion is the intended effect and a character on the page is confused too. Never let it
   be an accident.
4. **The exemption is exactly this wide.** It covers characters with a `mirror:` field, on the
   channels their convergence level names, and nothing else. It does not license an ally, a
   student, a sibling or a rival to share the MC's voice. "He's like a younger version of me" is
   not a mirror; it is a cast with two of the same person in it.

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
