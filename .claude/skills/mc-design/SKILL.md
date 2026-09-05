---
name: mc-design
description: Design the main character with the user — gender, appearance, intellect, origin (native, reincarnator, transmigrator, regressor) and central advantage or golden finger — each category offering a "surprise me" option. Also establishes the form ledger that keeps a non-final-form MC (a reborn infant, a weakened body, a pre-evolution form) physically consistent until they mature. Use during novel-init before any other cast work, and when the MC changes form.
---

# mc-design

Runs inside `novel-init`, **before** the rest of the cast and before `lead-interest`. Everything
downstream — the arc plan, the cast, the romance, the power system — is shaped by who this person
is and what body they are in.

Output: the MC's profile in `bible/cast/`, the `mc:` block in `novel.md`, and — when the MC does
not start in their final form — `state/body.md`.

---

## The five questions

Ask these with `AskUserQuestion`, in this order, batched. **Every question carries a
"Surprise me" option.**

### 1. Gender and pronouns

Options: Male · Female · Non-binary · Surprise me.

Record `mc.gender` and `mc.pronouns`. Pronouns are then fixed for the whole novel; the lexicon
enforces them. If the MC's origin involves a body change that crosses gender (a transmigrator in
another body), ask which pronouns the *narration* uses and note the answer in `state/body.md` —
this must be decided once and never drift.

### 2. Appearance

Do not ask for a body inventory, and do not write one (`bias-guard`). Ask instead for
**how the world reads them**, which is what actually generates scenes:

| axis | question |
|---|---|
| Legibility | do people guess right about them at a glance, or wrong? |
| Class marker | does their body say wealth, labour, hunger, indoor work? |
| Memorability | forgettable, or impossible to describe without one specific detail? |
| The one detail | the single thing a witness would report |

A useful MC is usually *misread* by their appearance in a way that costs or protects them. Record
two or three details maximum — enough to be consistent, few enough to stay flexible. Put the
summary in `mc.appearance_note` and the detail in the profile.

### 3. Intellect

Delegate to `mc-intel-meter`'s tier table. Present all five tiers with what each *costs the
author*, not just what it grants:

> Tier 4–5 require the plot to be built out of plans the reader can follow, and require you to
> plant clues chapters in advance. Tier 2–3 is easier to write well and rarely disappoints.

Also collect, in the same round or immediately after: **competence domains** (where the tier
applies at full strength) and **at least two blind spots**. The blind spots are mandatory —
without them `mc-intel-meter` cannot make a smart MC fail legitimately.

**Cap the domains at three**, and name the edge of each — where the expertise stops
(`competence-map` §1). The tier is how fast the MC thinks; it is not a licence to know things.
Everything off that list is `none`, which is what gives the MC people to ask, things to get wrong,
and skills to actually learn over the next two hundred chapters. Ask the user directly: *what is
your MC simply not good at, that most protagonists are?* It is one of the most productive answers
in this whole interview.

A note for the ambitious build: **parallel minds, accelerated thought and clone-swarms grant
throughput, not breadth.** A mind that runs six trains of thought still had to learn all six
subjects, one at a time, and a thousand copies of an ignorant person are a thousand ignorant
people. If the advantage is meant to confer knowledge as well as speed, that is a different and
much more expensive golden finger, and §"the cost" applies with force.

### 4. Origin

| origin | what it means | what it obliges |
|---|---|---|
| `native` | born to this world, no outside knowledge | the cleanest to write; the MC learns as the reader does |
| `reincarnator` | died, reborn into a new body, memories intact | the form ledger below. Usually starts as a child |
| `transmigrator` | moved into another body or world, same mind | the form ledger. Someone else's life, face, and debts |
| `regressor` | sent back to their own earlier life | foreknowledge that must decay — see below |
| `isekai` | pulled bodily into another world | no form problem; a culture and language problem instead |
| `revenant` | returned changed — undead, restored, rebuilt | the form ledger, plus what the new body cannot do |

**Foreknowledge decays.** For `reincarnator` and `regressor`: the MC's knowledge of what will
happen must start diverging early and often. Record in the profile: what they know, how precise
it is, and **the first chapter where it is wrong**. A story where foreknowledge stays reliable has
no tension after chapter 20. Foreknowledge is also not intelligence — `mc-intel-meter` tiers
still apply, and a tier-2 MC with perfect foreknowledge still reasons like a tier-2 MC.

### 5. The central advantage (golden finger)

What the MC has that others do not. Offer these, plus "Surprise me" and "None".

| archetype | shape | must not |
|---|---|---|
| **System / interface** | quantified feedback, quests, ranks | narrate the story or resolve fights. See `litrpg-system` |
| **Past-life knowledge** | knows techniques, events, or a craft from before | stay accurate; it must fail and mislead |
| **Bound entity** | a spirit, AI, or passenger with its own agenda | be a mentor who supplies answers. See below |
| **Anomalous body** | regeneration, adaptation, immunity | remove physical stakes; give it a visible cost |
| **One broken rule** | a single law of the world does not apply to them | be broad. The narrower the rule, the better the story |
| **Absorption** | copies skills, memories, or abilities from others | be free. Taking should cost, and should leave a trace |
| **Time** | rewind, foresight, loops | be unlimited. Every use must be paid for and countable |
| **Outside craft** | knowledge from another world — medicine, engineering | work without materials, labour, and someone's permission |
| **None** | the advantage is character: nerve, patience, a reputation | be secretly a golden finger by chapter 30 |

For whichever is chosen, fill in and record in `novel.md` and `bible/power-system.md`:

- `golden_finger` — one sentence a reader could repeat
- `gf_cost` — what each use takes, measurable
- `gf_limit` — two sentences beginning "this can never…"
- **the problem it creates** — mandatory. An advantage that only solves problems flattens the
  novel. Visible power makes the MC identifiable; a system makes them legible to whoever built
  it; foreknowledge makes them act on a future that no longer exists.
- **who knows** — concealment is a plot engine; decide early who has guessed.

**The bound-entity warning.** A knowledgeable companion is the fastest route to the
mentor-in-a-pocket defect (`mtl-detox`): the MC stops needing to figure anything out. If chosen,
the entity must have its own goals, be wrong sometimes, withhold things, and cost something to
consult.

---

## "Surprise me"

Do not roll dice. Generate **three options derived from the premise**, show them in one or two
lines each, choose the one that creates the most friction with the story already described, and
say why in a sentence. The user can overrule instantly, which is the point — people react to
options far more readily than they invent from nothing.

If the user picks "Surprise me" for everything, build a coherent whole rather than five
independent picks, and present the MC as a paragraph for approval.

---

## The form ledger — non-final-form MCs

**Trigger.** Set `mc.form_locked: true` and create `state/body.md` whenever the MC does not start
in the body they will have for most of the novel:

- reborn as an infant or child
- transmigrated into someone else's body
- a weakened, injured, sealed or de-levelled starting state
- a species or form that will evolve
- any case where the eventual "final form" differs visibly from chapter 1

**The rule this exists to enforce: while `form_locked` is true, no sentence may describe the MC's
body, reach, voice, capability, or how strangers treat them except from the CURRENT FORM row in
`state/body.md`.** Read that row before writing any such sentence. It is small and always in the
read-set.

### The eight form rules

1. **The mind is old; the body is new.** Knowledge, judgement and intent carry over. Strength,
   reach, stamina, coordination, voice and bladder do not. Never write a capability the current
   form cannot deliver, however experienced the mind is.
2. **The world reacts to the body.** This is the entire dramatic engine of the trope. Adults talk
   over a child. A servant's face opens no doors. A ruined body draws pity or contempt, and both
   are useful. If the MC's form does not change how a scene goes, the form is decorative.
3. **No final-form leakage.** Height, presence, features, bearing, the voice they will have — none
   of it may appear before its stage. This is the specific error the ledger exists to prevent, and
   it is easy to make: the writer knows what the MC looks like at the end and lets it bleed
   backwards.
4. **Enumerated limits per stage, and they are absolute.** Each stage lists what the body cannot
   do: lift, reach, run, ride, hold a weapon, be believed, be unaccompanied, be served, read
   without help, be taken seriously. A limit may be *worked around* with cleverness and cost —
   never ignored.
5. **The articulacy problem.** A child body speaking with adult diction is noticed. Either the MC
   masks — and masking is effort, and slips are scenes — or they do not, and someone draws a
   conclusion. Both are plot. What is forbidden is a four-year-old speaking like a strategist
   while everyone finds it unremarkable.
6. **Transitions are scheduled events, not drift.** Each stage change has a chapter number, a
   trigger, and an on-page moment. Between transitions, nothing about the body changes. Growth
   that happens gradually and invisibly is how continuity errors get in.
7. **Time and growth are tracked together.** A body ages with `state/timeline.md`. If two in-world
   years pass, the stage table must account for it. Check both files at every arc rollup.
8. **Other characters' memories are form-anchored.** Someone who knew the MC at stage 1 and meets
   them at stage 3 does not recognise them, or recognises them by something specific that
   persisted. Decide which, and record it.

### The CCS line

When a form changes, add a `bod>` line to that chapter's CCS block:

```
bod> Rin: F2 juvenile -> F3 adolescent (ch 88, growth spurt over the winter) / can now reach the
     upper shelves, voice broke, Vesh no longer speaks over her
```

Record what the change **enables** and what it **costs** — a new form closes doors too. A child
who could go unnoticed cannot any more.

### Non-MC use

The ledger takes any character who changes form: a child growing across 300 chapters, a
shapeshifter, someone maimed, someone restored. Add a row. Long serials get ages wrong constantly,
and the ledger is cheap.

### Copies of the MC

If the golden finger produces duplicates — clones, avatars, projections, a split self, a mind
copied into another body — or if the story gives the MC a doppelganger, each copy is its own
character file with a `mirror:` block, and it is the one case where sharing a voice is correct
rather than a defect. `voice-separation` §7 owns that: the convergence level (identical / drifting
/ inverted), the chapter they became separate people, and **the tell** — the one thing that does
not copy, and who could notice it.

Two things this ledger contributes. A copy with a different body is `form_locked: true` with its
own stage table here, so its reach and voice come from its own row and not the original's. And a
copy that can be *destroyed and remade* needs its `now costs` column filled like any other
transition: an advantage that spawns free bodies is a golden finger with no cost, which §"the cost"
already forbids.

## Writing the MC's profile

Fill `bible/cast/<mc>.md` from the template with everything above, plus the standard requirements
(`character-profile`): want/need/fear/lie, behaviour rules, the voice axes, all eight
speech-fingerprint fields, three original calibration lines, at least two incompetences, and a
five-rung ladder.

Three MC-specific additions:

- `development_rate: 5`, always. The story concentrates its pressure here.
- The MC's row in `bible/cast/_voices.md` is written first and is **the calibration point, not the
  ceiling**. `mc.intel_tier` fills the intel column; articulacy, wit, heat and turn length are
  chosen here like anyone else's, and the rest of the cast is then dealt around it — somebody
  quicker, somebody slower, and at most one other person who is funny (`voice-separation` §1).
- The **wound** should predate the origin event where possible. A reincarnator whose only defining
  experience is having died is thin; what they were like *before* they died is the character.

## Self-check

- [ ] Gender, pronouns, appearance, tier, origin and advantage all recorded in `novel.md`
- [ ] At least two blind spots
- [ ] The advantage has a cost, two limits, and a problem it creates
- [ ] For reincarnator/regressor: the chapter where foreknowledge first fails is chosen
- [ ] If the MC does not start in final form, `form_locked: true` and `state/body.md` exists
- [ ] Every form stage lists its absolute limits and its transition chapter
- [ ] No final-form detail appears anywhere in an earlier stage's description
- [ ] The MC's appearance is recorded as how the world reads them, not as an inventory
- [ ] The MC has a `_voices.md` row, and the cast was dealt around it rather than up to it
- [ ] At most three competence domains, each with its edge named; everything else is `none`
- [ ] If the advantage installs skill, what it does *not* install is written down
- [ ] Any duplicate the advantage produces has a `mirror:` block, a convergence level and a tell
