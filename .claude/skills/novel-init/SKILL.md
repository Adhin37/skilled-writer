---
name: novel-init
description: Start a new webnovel. Interviews the user for premise, genre, POV, MC intelligence tier, tone and optional mechanics, then scaffolds novels/<slug>/ with config, bible, cast, arc plan and chapter list. Use when the user wants to begin a novel, says /novel-new, or when no novel workspace exists yet.
---

# novel-init

Turn a user's idea into a working novel workspace. The user may know very little about their own
story — your job is to ask few enough questions that they stay engaged, and infer the rest.

**Budget: at most 6 rounds of questions.** Everything not asked, you decide and state. The title
pick in Step 2b does not count against that budget — it presents candidates you generated rather
than asking the user to supply anything.

---

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

**Before the scaffold, because the slug is derived from the title and there is no rename path.**
`sw.py newnovel` refuses to overwrite an existing directory; renaming afterwards means moving the
tree by hand and fixing every path that points at it.

Ask nothing new. Everything `title-craft` needs — premise, genre, MC origin and golden finger,
`opening.promise`, `ending.contract`, tone, `fanfic.source` — exists by the end of Round F.
Generate five candidates across five distinct strategies, screen them, and present the three
survivors with what each promises **and** what each costs. Then write the 60–120 word platform
blurb against the chosen title.

For **fan fiction the source work must be in the title line** — `Naruto: The New God of Shinobi`.
Readers browse fanfic by fandom; a title without the source name is invisible to its only
audience. This is a discoverability fact, not a style preference, and it is the one thing in this
step you say plainly even if the user overrules you.

Record `title`, `title_alternates` and `slug`, and hold the blurb for step 3.

**Then re-check `opening.promise` against the blurb you just wrote.** Round D set the promise from
the premise, before the blurb existed. If the two now promise different books, the blurb is the one
that changes — the user confirmed the promise out loud and did not confirm the blurb.

## Step 3 — Scaffold

Copy the scaffold. Use paths relative to the repo root, never absolute ones — this repo is used
on both Windows and Linux.

```bash
python3 scripts/sw.py newnovel <slug>
```

This is the portable form: it needs no shell, refuses to overwrite an existing novel, rejects a
slug that is not kebab-case, and prints the tree it created. Failing that:

```bash
cp -r novels/_template novels/<slug>          # macOS / Linux / Git Bash
```

If neither is available, create the directories and write each template file out instead; the
tree is small and the file list is in `CLAUDE.md` §6. Do not rely on any one shell being present.

**Copy first, then read.** Do not read the template files before copying them — copy the tree, then
open only the file you are about to fill, one at a time. Reading all eleven up front costs a turn
each and teaches you nothing the copy did not already put on disk.

The copy step must be permitted. If the shell refuses it, say so rather than silently falling
back — a denied copy is a settings problem, not a reason to hand-write the tree.

Slug is the one `title-craft` derived in Step 2b — kebab-case, 4–5 words. **It is permanent.**
The title may change at a later arc boundary; the directory every path hangs off does not.
Never scaffold under `untitled`: if Step 2b was skipped, go back and run it.

Note for the user, once, at the end: `novels/` is gitignored except the template, so their book
is not committed to the toolkit repo by default.

Then fill in, in this order:

1. **`novel.md`** — every frontmatter field. No field left as a placeholder. `title`,
   `title_alternates` and `slug` come from Step 2b; paste the blurb `title-craft` wrote into
   `# Hook (platform blurb)` rather than writing a second one. Write the premise, tone
   references, themes and the ending target. Delete the `fanfic:` block for non-fanfic.
2. **`bible/world.md`** via `story-bible`. Enough to write 25 chapters, not a gazetteer.
3. **`bible/lexicon.md`** — names and terms invented so far, plus house style decisions.
4. **`bible/power-system.md`** via `power-system` (fantasy/scifi) or **`bible/canon.md`** via
   `fanfic-canon`. Delete the file that does not apply.
4b. **`bible/society.md`** via `social-fabric` — **after** step 4, never before: the six
   questions, and one propagation test taking the most important rule down into institution,
   market and household. This is the step that stops a spectacular magic system from sitting on
   top of generic medieval wallpaper. Keep it under 1,000 words; write only the social layer
   arc 1 actually enters.
5. **`bible/cast/`** — the MC's profile first, via `mc-design` + `character-profile`. Then the
   love interest via `lead-interest`, if there is one. Then 3–5 other characters who appear in
   arc 1, **each at its tier**: full profiles only for principals, the short file for supporting
   characters, and nothing at all for people arc 1 merely walks past — they get sketched when
   they are written. Keep `_character-template.md`, `_supporting-template.md` and the empty
   `_extras.md` in place; they are the references for future characters.
5b. **`bible/cast/_voices.md`** via `voice-separation` — a matrix row for every character written
   in step 5, filled in **together, as a table**, not one at a time. Then run
   `python3 scripts/sw.py cast novels/<slug>`, which checks both this file and step 5c's, or run
   the three checks in §2 of that file by hand: the cast straddles the MC's intel tier, at most two characters have wit, and no
   two rows share intel + articulacy + wit. This is the step that decides the book will not be one
   voice in several costumes, and it is far cheaper here than in chapter 40. Delete §5 (Mirrors) if
   nothing in the novel duplicates a person.
5c. **`bible/cast/_competence.md`** via `competence-map` — the same move for knowledge. A row per
   character: domain, level, and **where the edge is**, plus a referral each, and §3, *what nobody
   in this cast knows*. Fill it as a grid so the distribution is visible: does anyone read, who is
   the only one who can fight, what would this cast have to buy? Unlisted is `none`, which is what
   gives arc 1 its errands and its wrong answers. Fill §4 only if the book contains gods, immortals,
   cultivators or artificial minds — their boundary and their access bound are required fields, not
   decoration, because an unbounded oracle dissolves every mystery you have planned.
6. **`plan/timeline.md`** via `timeline-engine` — the drivers with their reaction profiles, the
   world track for arcs 1–3, standing clocks, and the point-of-no-return watch. For fanfic, the
   canon track and the first deliberate divergence. Keep this coarse for original fiction: the
   antagonist's plan plus two or three clocks is enough.
7. **`plan/arcs.md`** via `chapter-plan` — arc 1 in full, arcs 2–3 in one line each.
8. **`plan/chapters.md`** via `chapter-plan` — the first 12 rows, fully specified.
9. **`state/`** — initialise `continuity.md` book digest, seed `threads.md` with the threads
   arc 1 opens (including the romance thread if there is one), seed `growth.md` with every tier-A
   character at rung 1 and every tier-B at `B1`, set the calendar in `timeline.md`. If `mc.form_locked` is true, fill in
   `body.md` completely — every stage, its limits and its transition chapter — before chapter 1 is
   written. If nothing in the novel changes form, delete `body.md`. If `mc.foreknowledge` is set,
   fill `foreknowledge.md` — the grain, the inventory of what the MC believes, and §5's arc of the
   advantage with the inventory scene, the first win and the first failure placed **in that
   order**. If nobody knows the future, delete `foreknowledge.md`.

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

## Defaults when the user won't decide

| field | default | why |
|---|---|---|
| pov.mode | `single` | Cheapest to keep consistent, strongest reader attachment. |
| mc.intel_tier | `3` | Smart enough to be satisfying, no plot-engineering burden. |
| chapters.length_band | `1500-2600` | A printer's note, never a gate. Do not raise it as a question. |
| opening.anchor_by_ch | `1` | The reader is oriented before they are threatened. |
| mc.foreknowledge_grain | `major-beats` | If the MC knows the future at all. Precise enough to plan on, loose enough to be wrong. |
| arc_length | `25` | Roughly a month of daily releases. |
| narration | third-limited, past, close | Widest tolerance, easiest voice to hold. |
| mc.origin | `native` | No form ledger, no foreknowledge decay; the MC learns as the reader does. |
| mc.golden_finger | `none` | An advantage is easy to add at chapter 30; removing one is not. |
| romance.configuration | `undecided` | A lead chosen from the existing cast at chapter 20 is almost always better than one designed cold. |
| timeline.reactivity | `3` | The world notices and adapts without becoming a grind. |
| ending.tone | `hopeful` | Never default the *contract* — ask for it in the user's words. |
| title | never defaulted | Always show three screened candidates. `"Untitled"` reaching the scaffold is a bug. |
| optional | only `no-harem` and `combat-choreography` on | Adding mechanics later is easy; removing them mid-serial is not. |

Never default `mc.gender` — ask it. Never infer `romance.lead_gender` from the MC's gender without
offering every configuration.

## Failure modes

- **Don't** interrogate. If the user gives short answers, stop asking and start building; they
  will correct a draft far more readily than they will fill in a form.
- **Don't** accept "make it like <popular novel>" as a spec. Ask which single element they want
  borrowed, and write that element down in tone references.
- **Don't** invent a 5000-word bible. Everything in `bible/` must be needed by arc 1 or by a
  decision you have already made.
- **Don't** ship a world whose central rule changed nothing about how people live. One
  propagation test at init is the minimum (`social-fabric` §2), and it costs six lines.
- **Don't** leave `blind_spots` empty. Two minimum, or `mc-intel-meter` cannot do its job.
- **Don't** build a starting cast where everyone is as quick and as articulate as the MC. Fill
  `_voices.md` as a table and check the three rules in §2 — somebody below the MC's tier, at most
  two funny people, no duplicate intel/articulacy/wit triples. Left undone at init, this defect is
  invisible for twenty chapters and then permanent.
- **Don't** scaffold before the book has a name. The slug is derived from the title and is
  permanent; a workspace built under `untitled` is a directory rename later for no reader-visible
  gain. And **don't** ship a fanfic whose title omits the source work — it is the search term.
- **Don't** give anyone an open-ended competence. Three domains for the MC, two for a principal,
  one for a supporting character, and everything unlisted is `none`. A cast where everyone can
  answer everything has no errands, no referrals and no reason for half its members to exist.
