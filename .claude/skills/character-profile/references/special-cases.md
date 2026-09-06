# character-profile — antagonists, mirrors, fan fiction, amendments

Open the part that applies: an antagonist, a clone or double, a canon character, or an existing profile that a chapter has changed.

---

## Antagonists

Same template, plus:

- Their want must be **legible and sympathetic in isolation**. Write the two-sentence version of
  their case that would convince a reasonable reader.
- They must be **right about something** the MC is wrong about.
- They must have **a cost they are paying** for their position.
- Their competence is real and demonstrated before they lose anything — and **narrow**, like
  everyone else's. The antagonist who is a master strategist, swordsman, poisoner and administrator
  is the omniscience defect wearing a black coat; their edge is what the MC eventually gets in
  through (`competence-map` §1).

A villain who exists to be defeated is a chore. A villain whose defeat costs the reader something
is the arc.

## Mirrors — clones, avatars and doubles

A character who is a copy of another is the one case where sharing a voice is correct. Give them a
normal profile at their tier, plus the `mirror:` block in the frontmatter — `mirror`, `mirror_kind`,
`convergence`, `diverged_ch` — and a row in §5 of `_voices.md`. The rest of the profile is filled
from the source character's, changed only where their separate life has changed them.

Three things the profile must still answer, because they are what makes a double a character rather
than a duplicate file (`voice-separation/references/mirror-clause.md`):

- **What has diverged since `diverged_ch`**, and at what rate. Different experiences make different
  people; a copy who has lived thirty chapters apart and sounds identical is a puppet, which is
  legitimate only if the story says so and somebody notices.
- **The tell** — the one thing that does not copy, and who could detect it. Plant it before it is
  needed (`plot-threads`). If nothing fails to copy, record `none — deliberate`.
- **Who the reader tracks in a shared scene** — the physical tag or POV anchor that keeps two
  mirrors apart on the page, unless the confusion is the intended effect.

A double with a different body is also `form_locked: true` with its own stage row in
`state/body.md`. The exemption covers declared mirrors only: a protégé, a sibling or a rival who
"is like a younger version of the MC" is not a mirror, it is a cast with two of the same person in
it.

## Fan fiction

Canon characters get a normal profile, derived from the source, plus:

1. **Derive from behaviour, not from fandom consensus.** Base each field on what the character
   is depicted doing in canon, not on what fandom says about them.
2. **The riot trait** — the one thing a reader would not forgive you for losing. Name it in
   `bible/canon.md` and never contradict it.
3. **Speech fingerprint from canon patterns**, described in your own words: register, rhythm,
   verbal habits, what they never say. Describe the pattern; do not transcribe source lines.
4. **Write original prose.** Never reproduce dialogue, narration, or text from the source work.
   The profile stores characterization, not quotations.
5. **Divergence-driven change only** (at `ooc_budget: low`): any behaviour that differs from
   canon must trace to the divergence point through events shown on the page.
6. **Log every reinterpretation** in `bible/canon.md`'s table, with in-story justification.
7. **Canon competence has edges too.** Derive the domains from what the source shows them doing,
   and mark everything else `none` — fandom quietly promotes a character to expert in whatever a
   fic needs. They also do not know the parts of canon they were never present for, and they do not
   know the future the writer knows (`competence-map` §1 , §3).

Set `canon: true` in the frontmatter. OCs get `canon: false` and must pass the OC test: name the
job they do, and why no canon character could do it.

**Canon characters get tiers too.** A source work has hundreds of named people and this story uses
a handful. A canon character who appears in two scenes is a tier-C walk-on with three strokes —
except that stroke 2, the habit, must come from canon rather than invention, because a reader will
recognise them. The riot trait applies at every tier: it is one line, and it is cheap.

## Amending an existing profile

Profiles change; they are not carved. Amend when a chapter reveals or changes something.

- **Append, don't overwrite.** Continuity facts are permanent.
- Rung changes go in `state/growth.md` **and** in the profile's `current_rung`.
- If a chapter made a character act against their behaviour rules, decide: was it a defect
  (fix the chapter) or a development (add the rung, record the voice delta)? Never neither.
- If a character has been in ten chapters and their fingerprint has never mattered, their
  fingerprint is too weak. Sharpen it.
