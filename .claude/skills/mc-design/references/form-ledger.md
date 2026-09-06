# mc-design — the form ledger

Open this only for an MC who is not in their final form — a reborn infant, a weakened body, a pre-evolution shape. Skip it entirely otherwise.

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

**`mc.final_form_reached_ch`** records the chapter the last transition lands, once it is known.
It is the chapter after which `form_locked` no longer gates a description, and setting it is what
closes the ledger.

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
rather than a defect. `voice-separation/references/mirror-clause.md` owns that: the convergence level (identical / drifting
/ inverted), the chapter they became separate people, and **the tell** — the one thing that does
not copy, and who could notice it.

Two things this ledger contributes. A copy with a different body is `form_locked: true` with its
own stage table here, so its reach and voice come from its own row and not the original's. And a
copy that can be *destroyed and remade* needs its `now costs` column filled like any other
transition: an advantage that spawns free bodies is a golden finger with no cost, which §"the cost"
already forbids.
