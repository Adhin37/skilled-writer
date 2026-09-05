---
name: fanfic-canon
description: Keep a fan fiction consistent with its source — canon facts, characterization fidelity, a single divergence point, an OOC budget, and original-character integration — while writing entirely original prose. Use when starting a fanfic, when writing any canon character, and when deciding whether a canon event still happens.
---

# fanfic-canon

Genre module — `genre: fanfic`. Maintained in `bible/canon.md`.

Fanfic readers arrive knowing the source better than you do. They forgive an invented city; they
do not forgive a character who would never have said that.

---

## Rule zero — write original prose

This story is your own writing about existing characters and a shared setting.

- **Never reproduce text from the source work** — no dialogue, no narration, no lyrics, no
  excerpts, in any chapter or bible file.
- `bible/canon.md` records **facts and characterization in your own words**: what a character
  values, how they speak, what they did. It is not a quotation store.
- Re-staging a canon scene means writing it fresh, from a new angle, in your prose. If a chapter
  is only useful because it repeats a scene readers already have, it is not a chapter.
- Keep the story recognisably transformative: your plot, your prose, your consequences.

## The divergence point

The strongest structure for a fanfic is **one change, followed honestly.**

Record in `bible/canon.md`:

- **Where** — the precise canon moment the story departs.
- **The change** — one thing. Resist a list; a second change halves the coherence of the first.
- **First consequence** — what breaks immediately.
- **What stays true anyway** — the things the change does not touch, so canon does not quietly
  dissolve.

Everything downstream must follow from the change, not from author convenience. When a canon event
still happens, ask **why** it still happens given the divergence, and record the answer. When it
does not, the reason must be traceable to the change.

**Canon timeline anchors.** Keep the table of canon events with: does it happen here, and when
relative to this story. Readers track this closely.

**The canon plot is a live timeline, not a backdrop.** `timeline-engine` owns it: the canon track
in `plan/timeline.md`, each canon antagonist's reaction profile, and the rule that every arc must
move at least one canon event. It also holds the governor that keeps a reactive canon world from
becoming a grind, and the ending contract it may not foreclose. Run it alongside this skill —
canon fidelity without canon *consequence* is the commentary-track defect.

## Characterization fidelity

For each canon character used, write a normal profile (`character-profile`), derived from what
they are **depicted doing** in canon, not from fandom consensus. Fanon drift is the most common
cause of "this isn't them".

**The riot trait.** For each major canon character, name the one thing readers would not forgive
you for removing — the loyalty, the cowardice, the refusal to lie, the humour that arrives at the
worst moment. Write it in `bible/canon.md` and never contradict it.

**Speech fingerprint from canon patterns.** Describe the pattern in your own words: register,
sentence rhythm, what they deflect with, what they never say, how they change under pressure.
Then write original lines that satisfy it. The three calibration lines in the profile must be
your sentences, not remembered ones.

**Behaviour under new pressure.** The value of fanfic is putting a known person in an unknown
situation. Derive their response from their canon behaviour rules; do not import a response from
a different situation.

## The OOC budget

`novel.md` → `fanfic.ooc_budget`.

| budget | rule |
|---|---|
| **low** | Every behaviour must be canon-derivable. Change comes only from divergence consequences, shown on the page across chapters. |
| **medium** | One deliberate reinterpretation per major character, justified in `canon.md` and dramatised early enough that readers can accept it. |
| **high** | Characters re-founded; canon supplies premise and relationships. Say so in the blurb — readers who want fidelity should self-select out. |

Log **every** intentional departure in the reinterpretation table with its in-story justification.
An unlogged departure is a defect, not a choice.

**Change must be earned on the page.** At `low`, a character who ends the story different from
canon is fine — that is the point of the divergence — but the reader must have watched every step.

## Original characters

The OC test: **name the job they do, and why no canon character could do it.**

- OCs do not solve canon characters' problems for them.
- OCs do not out-perform canon characters in the canon characters' own domains, at least not
  without a longer, costlier justification than you think.
- OCs are not the audience's stand-in for admiring the cast.
- `oc_policy: co-lead` is legitimate, but then the OC needs the same arc rigour as an MC:
  ladder, wound, lie, blind spots, `intel_tier`.

## Canon scope

Decide and record what counts as canon: which volumes, seasons, adaptations, supplementary
material. Then hold it. Nothing frustrates a reader faster than a story that uses a later
revelation in chapter 5 and ignores it in chapter 40.

Also record **fanon this story rejects** — the widely-assumed-but-not-canonical readings you are
not using. It saves arguments and keeps you honest.

## What still applies

Everything else in the toolkit does. In particular:

- `bias-guard` — canon is not a licence. Source-work biases are not inherited; if canon treats a
  group as scenery, this story does not have to.
- `mc-intel-meter` — set the tier from canon behaviour, then hold it. Canon characters are
  frequently written smarter or dumber than canon to fit a plot; that is the same defect.
- `character-development` — canon characters get ladders too. A fanfic where nobody changes is a
  transcript.
- `voice-separation` — canon characters go on the matrix like anyone else, derived from how they
  actually speak in the source. A fic where the whole cast has flattened into one narrator's voice
  is the most common thing readers mean by "OOC" without being able to point at a line.
- `competence-map` — **canon competence has edges, and fandom quietly erases them.** Derive each
  character's domains from what the source depicts them *doing*, mark everything else `none`, and
  resist the promotion a scene wants. Two knowledge boundaries are specific to this genre and are
  broken constantly: a canon character does not know the parts of canon they were not present for,
  and **nobody knows the future the writer knows.** A reader can feel the difference between a
  character reasoning from what they have seen and a character quoting the wiki. The MC's
  foreknowledge, if they have any, is the exception the story is *about* — and `mc-design` already
  requires a chapter where it first turns out to be wrong.

## Self-check

- [ ] No text reproduced from the source anywhere
- [ ] One divergence point, recorded, with its first consequence
- [ ] Every canon event kept or dropped for a reason traceable to the divergence
- [ ] Each major canon character's riot trait intact
- [ ] Every departure from canon behaviour logged with in-story justification
- [ ] Speech fingerprints derived from canon patterns, calibration lines original
- [ ] No canon character knows a canon event they were not present for, or anything from the future
- [ ] Every OC passes the OC test
- [ ] Canon scope respected throughout
