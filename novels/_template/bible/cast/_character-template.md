---
name: ""
aliases: []
tier: A                 # A — principal. For tier B use _supporting-template.md; tier C is one
                        # line in _extras.md and gets no file at all.
role: supporting        # mc | deuteragonist | antagonist | supporting | recurring | one-arc
first_appears: 0
status: alive           # alive | dead | dormant (offstage 40+ ch, out of the read-set)
development_rate: 3     # 1 glacial .. 5 volatile   (MC always 5)
current_rung: 1         # position on the ladder below
pov_eligible: false
canon: false            # fanfic: is this a canon character?

# ── KNOWLEDGE SCOPE ──────────────────────────────────────────────────────────
# `narrow` for every mortal, however wise. `broad` ONLY for gods, immortals,
# cultivators, ASI and bound spirits. See competence-map §6 — the boundary and
# the bound on access are both required, because an unbounded oracle dissolves
# every mystery in the book.
knowledge_scope: narrow # narrow | broad
scope_kind: ""          # domain-god | long-lived | artificial | borrowed
scope_shape: ""         # what is actually broad, in one sentence
scope_boundary: ""      # what still bites — required when scope is broad

# ── MIRROR ───────────────────────────────────────────────────────────────────
# Only for clones, avatars, doubles and body-snatches. These four fields are the
# exemption from voice-separation §3 — a copy of a person may sound like them.
# Delete the block for anyone who is not a duplicate. See voice-separation §7.
mirror: ""              # slug of the source character
mirror_kind: ""         # clone | avatar | projection | doppelganger | body-snatch |
                        # split-self | time-double | copy-mind | shapeshifter
convergence: ""         # identical | drifting | inverted
diverged_ch: null       # the chapter they became separate people
---

# <Name>

Tier A — the full profile. This is the expensive template, and it is meant to be: it is for the
MC, the love interest, the deuteragonist and the arc antagonists. Everyone else costs less.
See `character-profile` for the tier table before filling this in.

## Thumbnail
<!-- One sentence a reader could repeat. Not a description — a stance toward the world. -->

## Want / Need / Fear / Lie

| | |
|---|---|
| **Want** | what they pursue, concrete and pursuable in a scene |
| **Need** | what would actually help them; usually contradicts the want |
| **Fear** | the specific outcome they organize their life against |
| **Lie** | the false belief they hold about themselves or the world |

The Lie is the engine. Development is the slow, costly erosion of the Lie.

## Competence

Owned by `competence-map`. Copy these rows into `bible/cast/_competence.md` and read the grid, not
the row — the useful facts are distributional.

| domain | level | where the edge is | evidence the reader has seen |
|---|---|---|---|

Levels: `none` `passable` `professional` `exceptional` `best alive`. Anything above
`professional` must be paid for with a scene showing how it was acquired, and the budget is
**two** above `professional` for a tier-A character, three for the MC.

**An unlisted domain is `none`, not "probably fine."** If a scene needs this character to know
something absent from the table, either they do not know it — which is the scene — or they learn it
on the page and it is added here.

**Incompetence** — at least two, and that is a floor. The interesting ones sit *adjacent* to the
expertise, because those are the ones a reader assumes the character has. A character good at
everything is not a character.

**Referral** — when it is outside their domain, who do they go to, and what does asking cost them?

**Learning** — any skill currently being acquired goes in the skill-ladder table of
`state/growth.md`: stage 0 can't → 1 fails knowingly → 2 unreliable → 3 competent → 4 fluent, with
the source of each advance (a teacher, a reference, a costly failure — never elapsed time).

**Broad knowledge** — only for gods, immortals, cultivators, ASI and bound spirits. Set
`knowledge_scope: broad` in the frontmatter and fill `scope_kind`, `scope_shape` and
`scope_boundary`. The boundary is required, and the *access* is what gets bounded, not the
knowledge. See `competence-map` §6.

## Behaviour rules

Five to eight if/then rules. These are what make the character predictable enough to be
surprising. Write them so another writer could run the character correctly.

- Under threat, they →
- When they want something from someone, they →
- When caught lying, they →
- When someone is kind to them, they →
- When they are wrong, they →
- When they are winning, they →

## Voice axes

The layer under the fingerprint. Fill this **before** the eight fields below — surface habits on an
undifferentiated mind are labels, not voices. Copy this row into `bible/cast/_voices.md` and check
it against the rest of the cast there. See `voice-separation` §1.

| axis | value |
|---|---|
| intel | 1–5, the `mc-intel-meter` ladder. May be above or below the MC's |
| articulacy | 1–5. Independent of intel — the pairing is the character |
| wit | none / dry / warm / clowning / cruel, **and the pressure that triggers it** |
| heat | flat / banked / quick / volatile |
| turn length | default words per speaking turn. A number. Hold it |
| conversational blind spot | the one thing they cannot do that the MC does easily |

**Thought fields** — only if `pov_eligible: true`. The thought unit is this character's metaphor
source in narration (`narrator-voice`); no two POV characters may share one.

| field | value |
|---|---|
| thought unit | images / words / numbers / bodies / rules / people / money |
| thought speed | ahead of the scene / with it / one beat behind |
| facing an unknown | test it / avoid it / name it / ask someone / assume the worst |

**First move** — what they reach for or look at first when a situation changes. This is how their
mind reaches the page inside someone else's POV, without interiority.

## Speech fingerprint

See `dialogue-voice` for how to use this. All eight fields required.

| field | value |
|---|---|
| register | (street / clerical / military / academic / archaic / clipped-modern) |
| sentence length | (habitual, and how it changes under stress) |
| contractions | (always / never / drops them when lying or when formal) |
| vocabulary tell | 3–5 words this character uses and no one else does |
| syntax tic | one structural habit (questions answered with questions; trailing conditionals) |
| what they never say | the word or admission that will not cross their lips |
| profanity | none / mild / heavy / inventive-and-specific |
| silence | what makes them stop talking |

**Sample lines** — three, in three different emotional states. These are the calibration set;
when in doubt, write a line and check it against these.

1. calm:
2. under pressure:
3. cornered / furious:

## Body & habit

Two or three physical behaviours, used sparingly. Not a portrait — a gesture the reader learns
to read. Avoid the beauty-catalogue; describe what the body *does*, not how it rates.

## Relationships

| with | current state | what they want from them | unspoken |
|---|---|---|---|

## Arc ladder

Five rungs from who they are now to who they end as. Each rung names the **trigger** (the kind
of event that advances them) and the **voice delta** (what audibly changes in their dialogue).
See `character-development`.

| rung | belief at this rung | trigger to advance | voice delta |
|---|---|---|---|
| 1 | | | (baseline) |
| 2 | | | |
| 3 | | | |
| 4 | | | |
| 5 | | | |

## Regression conditions
What sends them *down* a rung. Growth that cannot be lost isn't growth.

## Continuity facts
Hard details that must never contradict: scars, ages, kin, debts, oaths, possessions.

| fact | est. ch |
|---|---|
