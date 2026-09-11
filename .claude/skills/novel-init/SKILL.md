---
name: novel-init
description: Start a new webnovel - interview for premise, genre, POV, tone, then scaffold novels/<slug>/. Use when the user wants to begin a novel, says /novel-new, or when no workspace exists.
owns: [premise-interview, scaffold]
---

# novel-init

Turn a user's idea into a working novel workspace. The user may know very little about their own
story — your job is to ask few enough questions that they stay engaged, and infer the rest.

**Budget: at most 6 rounds of questions.** Everything not asked, you decide and state. The title
pick in Step 2b does not count against that budget — it presents candidates you generated rather
than asking the user to supply anything.

---

## What lives in `references/`

| file | open it when |
|---|---|
| `references/scaffold.md` | Step 3: the interview is done and the workspace is about to be written. Also holds the defaults table and the failure modes |

## Step 1 — Get the premise in the user's words

If they have not already described it, ask in plain chat (not a multiple-choice tool):

> Tell me the story in a few sentences — who it follows, what goes wrong, and what makes it
> different from the last thing I read. Rough is fine.

If they answer with only a genre or a vibe ("cultivation but good"), ask exactly one follow-up:
what the protagonist *wants*, and who stops them.

## Step 2 — Structured interview

Ask with `AskUserQuestion`, batching up to 4 questions per call. Always lead each option list
with the choice you recommend for this premise, marked `(Recommended)`.

**Round A — the shape**

| question | options |
|---|---|
| Genre | Fantasy · Science fiction · Fan fiction |
| Point of view | Single POV throughout · Dual POV (MC + one other) · Rotating cast |
| Release cadence | Daily · Several times a week · Weekly (affects arc pacing) |

Do **not** ask for a chapter length. Chapters are judged by what they deliver, not their size
(`revision-pass` Pass 9); `chapters.length_band` keeps its default and is a printer's note.
Offering the number as a setup question is what makes it read as a target.

**Do ask for a style target**, in the same round, as an open question rather than options:

> *Name a book or two whose **writing** you want this to feel like — not the plot, the voice. And
> if you have a few paragraphs you love, paste them.*

Write the answer to `style.read_like` and `style.sample` in `novel.md`. This is the cheapest lever
in the whole toolkit and the only one that works by imitation instead of prohibition: a model
matches an example far more reliably than it obeys a rule. Without it the narrator defaults to
this model's own literary register — every sentence loaded, every scene closed on a small ironic
aphorism, one temperature for the whole book — which is a *more* recognisable fingerprint than
the clichés `mtl-detox` removes. If the user has no answer, say you will draft three sample
paragraphs after chapter 1 and have them pick; do not leave it empty and hope.

**Round B — the main character** → run `mc-design` for this round

Five questions, each with a **"Surprise me"** option: gender and pronouns · appearance (as *how
the world reads them*, never a body inventory) · intellect (the `mc-intel-meter` tier table, shown
with what each tier costs the author) · origin (native, reincarnator, transmigrator, regressor,
isekai, revenant) · the central advantage or golden finger.

Collect competence domains and **at least two blind spots** in the same round.

If the origin means the MC does not start in their final body, `mc-design` sets
`mc.form_locked: true` and builds `state/body.md`. Do not skip that — it is what keeps a reborn
child's description from drifting into their adult form.

If the origin or the golden finger means **the MC knows what happens next** — reincarnator,
regressor, transmigrator into a known story, fanfic self-insert — run `meta-knowledge` here too.
Collect the **grain** (`episode-precise` · `major-beats` · `impressions` · `fandom-corrupted`) and
build `state/foreknowledge.md`. Ask where it first **works** before asking where it first fails:
an advantage the reader only ever watches malfunction is a bait-and-switch on the blurb.

**Round C — the love interest** → run `lead-interest` for this round

**Only after Round B.** Ask configuration, not just "is there romance": with a male MC the default
offered is a female lead; with a female MC the default is a male lead, **with a female lead
offered as an equally available option**; non-binary and no-romance are always on the list, and
so is "decide later", which is often the best answer — a lead who emerges from the cast at chapter
20 is usually better than one designed cold.

Ask the amount of romance here too — None · Background subplot · Central — since it decides
whether the rest of the round happens at all. Set `content.romance` from the answer, and skip
straight to Round D if it is None.

**Round D — texture, the world clock, and the ending**

| question | options |
|---|---|
| Tone | Grounded and costly · Adventurous and warm · Bleak · Wry and comic |
| Content ceiling | Teen · Mature (violence and consequence on the page) |
| How much does the world push back? | Responsive — it notices and adapts *(recommended)* · Ripples — mostly local changes · Adaptive — the opposition plans around you specifically · Predatory — the world reorganises around you |

Then ask, in chat because it needs free text: **what does a good ending look like for this
story?** Record the answer verbatim in `ending.contract`, and ask who or what must survive
(`ending.non_negotiables`). Say plainly what this buys them: the world may cost the MC enormously,
but `timeline-engine` will never let it close the road to that ending, and nothing on the
non-negotiables list can be taken.

For fanfic this round matters most — see `timeline-engine`. Set `fanfic.footprint` here too.

Then fill the **`opening:`** block, mostly without asking — the defaults are right nearly always
and `story-opening` owns them. Two things are not defaults:

- **`opening.promise`** — write it from the premise, in one sentence, in the user's own words. This
  is the contract readers arrive holding, and the page has to keep it by `promise_touched_by_ch`.
  Read it back and let them correct it. **The blurb does not exist yet** — `title-craft` writes it
  at Step 2b — so write the promise now and re-check it against the blurb when that step lands. If
  they disagree, the blurb moves: the promise was confirmed by the user and the blurb was not.
- **`opening.stakes_ceiling`** — one sentence naming the worst thing allowed to happen before the
  reader can price it. Derive it from the premise; do not ask. For a story whose danger is
  institutional, it is usually *"the MC can be noticed, but nothing may act on it until the reader
  has seen the machinery take someone else."*

Then the **`scaling:`** block. Ask exactly one question — the rest is derived:

| question | options |
|---|---|
| Where does the MC start, and where does this end up? | Bottom of the ladder, climbing *(recommended)* · Already at the top, and the story is about something else · Starts strong, loses it, earns it back · Climbs, then the ladder stops mattering |

Those are `scaling.shape` — `climb` · `inverted` · `regression` · `plateau-late`. For a novel with
no capability ladder at all, set `none` and the skill and its ledger switch off; before reaching
for it, note that an ordinary MC still has a curve (`power-scaling/references/curve-shapes.md` §7).

Then, without asking: `start_tier` from the shape (1–2 for `climb`), `tiers` and `ceiling_tier`
from the premise's scope, and **`scaling.endgame`** — the final opposition and its tier, in one
line, derived from `ending.contract`. Write it down now even if it changes; a ladder with no top
is how the escalating sky starts. If the shape is `inverted`, `substitute_tension` is **required**
and is a real question: what is the story about when power is not in question? Once
`mc.golden_finger` is set, `mc-design` fills `edge_worth` and `edge_price`.

Then the **`theme:`** block, and do not ask for it either — propose it and let them correct it.
Read back the premise and the ending contract and say what the book appears to be arguing, in one
sentence: *"Loyalty you inherited is not loyalty you chose."* Then name the **counter-case** —
the strongest version of the opposite, which somebody in the story gets to make and win with at
least once. A controlling idea nobody can argue against is a sermon, and readers can hear one.

Both fields are for the author. Say so plainly when you present them: **the narrator will never
state either one.** If the user does not want the book to argue anything, leave both empty and the
theme pass skips. That is a legitimate answer for a comfort serial and a bad one for most books.

**Round E — genre module** (only the one that applies)

- *Fantasy*: what is magic made of, who controls it, and what does using it cost? Offer three
  concrete systems built from their premise rather than a menu of generic ones.
- *Scifi*: how far from now, and what is the one technology the story actually argues about?

Then one further question, in every genre, because it is the highest-value worldbuilding answer
there is and users enjoy it: **who does the work, and who lost out when this rule arrived?** One
sentence is enough — `social-fabric` derives the rest at step 3.
- *Fanfic*: source work, which canon material counts, the exact divergence point, and the
  OOC budget. Ask these in chat — they need free text.

**Round F — optional mechanics** (multi-select)

Present the optional skills as reader-facing features, not filenames:

- No harem — love interests are people with their own goals *(on by default)*
- Romance arc structure — beats, obstacles, payoff scheduling
- Detailed combat choreography
- Game-like system / status screens (LitRPG)
- Fair-play mystery clue tracking
- Comic relief scheduling
- Grimdark consequence enforcement — no plot armour
- Slice-of-life texture — food, work, weather, downtime

## Step 2b — Name the book → run `title-craft`

**Before the scaffold**, because the slug comes from the title and is permanent — `title-craft`
carries why.

Ask nothing new. Everything `title-craft` needs — premise, genre, MC origin and golden finger,
`opening.promise`, `ending.contract`, tone, `fanfic.source` — exists by the end of Round F.
Generate five candidates across five distinct strategies, screen them, and present the three
survivors with what each promises **and** what each costs. Then write the 60–120 word platform
blurb against the chosen title.

For **fan fiction the source work must be in the title line** — `Naruto: The New God of Shinobi`.
Readers browse fanfic by fandom; a title without the source name is invisible to its only
audience. This is a discoverability fact, not a style preference, and it is the one thing in this
step you say plainly even if the user overrules you.

Then run `title-craft` §Step 7 for the **listing**: 5–7 tags, a one-sentence cover brief, the
release cadence and the launch stock. These go in `platform:`. Present them as decisions with
consequences rather than as questions — the cadence in particular is chosen for a bad week, not a
good one, and the opening arc is written into it.

Record `title`, `title_alternates`, `slug` and `platform:`, and hold the blurb for step 3.

**Then re-check `opening.promise` against the blurb you just wrote.** Round D set the promise from
the premise, before the blurb existed. If the two now promise different books, the blurb is the one
that changes — the user confirmed the promise out loud and did not confirm the blurb.

## Step 4 — Report

Show the user:

- **the title, with the two runners-up underneath** — this is the first thing they will react to,
  and the cheapest thing in the whole workspace to change now
- the path, and a tree of what was created
- the blurb (this and the title are what a stranger in a library grid actually sees)
- the first 12 chapter titles with a one-line goal each
- **the MC in a paragraph** — gender, how the world reads them, tier, the two blind spots,
  origin, and their central advantage with the problem it creates
- if `form_locked`: the form stages and the chapters they change on, so the user can see the
  body plan up front
- **the love interest**, if any — who they are, what they want that is not the MC, and their
  reason to refuse
- **the voice matrix as a table** — every named character's intel, articulacy, wit and turn length
  in one block, so the user can see at a glance who is cleverer than the MC, who is slower, who is
  the only funny one, and who talks too much. This is the cheapest thing on the list to correct now
  and the most expensive to correct at chapter 40
- **the competence grid**, the same way — one line per character, their domain and where it stops,
  plus what nobody in the cast knows. That last list is the most interesting thing you can show a
  writer at this stage: it is where arc 2 comes from
- **the ending contract** back in their own words, plus the reactivity dial, so they can see the
  deal: this hard, and it ends there
- for fanfic: the first deliberate divergence — which canon event, which chapter, what the MC
  removes from it
- which optional skills are on
- **three things you decided for them**, each with a one-line "change this if…"

Then: *"`/novel-write` starts chapter 1. `/novel-toggle` changes any of the options."*

---
