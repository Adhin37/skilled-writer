# Benchmark — test run #4

Fourth end-to-end run of this toolkit, instrumented. Run on 2026-09-12.

This page replaces the run #2 benchmark. Run #3 was never written up, and seventeen citations
across `CLAUDE.md`, six skills and five scripts named it as the evidence for a rule; it is
reconstructed below from the artifacts that survive. What is kept from earlier runs is recorded as
*what run #N established*, and nothing else.

The purpose was not to produce a novel. It was to evaluate **six changes to the drafting loop that
had shipped without ever running** — the three-candidate widening step, Pass Z4, twenty positive
exemplars, the `metadata.force:` tiers, the card budget and four card merges
([creative-latitude.md](creative-latitude.md)) — plus the `eq` axis, which was wired, checked and
unexercised.

One of those seven is now proven. Two cannot be evaluated at all. And the run found something
nobody was looking for, which a second, cold agent then explained.

## TL;DR

| | |
|---|---|
| Model | Claude Sonnet 5, driven as a subagent |
| Produced | 1 scaffolded novel + **5 gated chapters**, 5,904 words |
| Run | **$31.58**, 56m 54s, 277 API responses |
| Cost per 1,000 finished words | **$5.35** (run #2: $3.35) |
| `sw audit` | **0 defects**, 11 warnings (run #3: 0 defects, 16 warnings) — 17 re-linted today, see below |
| Skills that loaded | **13 of 44** warm · **24 of 44** cold (run #2: 27 of 41) |
| **Cards opened** | **5 across five warm chapters** · **33 in one cold chapter** |
| Toolkit defects found | **8** (3 high) |

**The headline is the card count.** `sw readset` ran seven times. Every time it printed the
resolved card set for that chapter — every card, by full path, under the line *"Open these in
order, and no others."* Across the whole run the model opened **five cards**, four of which were
the config-gated modules listed in the shorter block above the card list. It opened **no audit
card at all**; Phase C ran off `revision-pass`'s body.

That is benchmark run #1's finding 9 — *"`revision-pass` was self-sufficient, so the model read
its condensed checklists and never opened the sources"* — reproducing after the entire draft-card
and audit-card architecture was built to prevent it.

**And then the cold chapter explained it.** A second agent, fresh session, no history, was pointed
at the same novel and told to write chapter 6. It opened **17 draft cards and 16 audit cards** —
essentially the whole resolved set — and cost **$3.21**, less than the warm run's $3.79 mean.

So the card architecture is not broken and the instruction load is not unaffordable. **Both
collapse inside a long session.** The warm agent was rationing by chapter 2, and what it rationed
away first was every card. This is run #2's Limitation 3 — the untested flat-cost claim — coming
back as something much more serious than cost: **contract fidelity degrades within a session, and
no number in the repo was watching it.**

## What was tested

| parameter | value |
|---|---|
| Genre | `fanfic` — the heaviest configuration |
| Source | Naruto; MC **Yakumo Kurama** rewritten as a reincarnator |
| Foreknowledge | corrupted, `fandom-corrupted` grain |
| Body | `form_locked` — an adult mind in a six-year-old body |
| POV | single, close third, past |
| Scaling | `climb`, 7 tiers · `timeline.reactivity` 4 · `content.romance: none` |
| Harness | **one subagent**, init + all 5 chapters, no human approval at Phase A |

Run #3's configuration was held constant on purpose, because the six changes under test are
genre-neutral and a comparison needs a baseline. The writing agent was given a pure authoring
brief with no mention that it was being measured, and told not to read `docs/`. It was **not**
told to set `eq_tier` or fill `cadence`; whether the template makes that happen unprompted was the
test.

## The seven things under test

| | result |
|---|---|
| **the `eq` axis** | **works.** Unprompted: `eq_tier: 3` in `novel.md`, and an `eq` value for all five cast rows — 4, 3, 5, 3, 4 against intel 4, 3, 5, 3, 4. `sw cast` reports **zero findings**: straddle holds, no `eq-flat`, no `eq-clash`. Run #3's matrix had no `eq` column at all |
| **`cadence`** | **works.** Filled for all five speakers, with genuinely distinct shapes ("flat statements building to a hard point", "even complete clauses building to one formal closing judgment", "floods when explaining") |
| **positive exemplars** | **probably works, not isolable.** `echo` went 1 chapter → 0, `para-opening` 4 of 5 → 1 of 5. But the cards carrying the exemplars were not opened, so the improvement cannot be attributed to them |
| **`metadata.force:` tiers** | **no evidence either way.** No gate report broke a stylistic rule and said so. A run with zero deliberate breaks is indistinguishable from a run where the tiers changed nothing |
| **card merges** | **partially confirmed.** `social-perception`'s content reached the page (the `eq` axis is filled and used) without its skill being opened, which is what a merge is supposed to achieve |
| **three candidates** | **cannot be evaluated** |
| **Pass Z4** | **cannot be evaluated** |

### The two that cannot be evaluated, and why

Neither leaves an artifact. The three-candidate step happens inside Phase A's brief, and **the
brief is never persisted** — it is written into the conversation and discarded. Pass Z4 asks *name
the thing here a competent hack would not have written*, and its output is a note that goes
nowhere. The CCS block has fourteen fields and none of them records either.

Grepping the finished novel for any trace of candidates, Z4, or the hack question returns nothing.
`docs/creative-latitude.md` §Sequencing said of exactly these two that they "change drafting
behaviour and want a benchmark run to evaluate." They got one, and it could not see them.

**Fix before run #5:** give the brief a file, or add one CCS field. Until then these two are
unfalsifiable, which is a worse state than untested.

## Cost

| | run #2 | run #4 |
|---|---|---|
| total | $22.81 | **$31.58** |
| setup + ch 1 | ~$21 | **$11.28** |
| per chapter after | ~$1.90 | **$3.79** mean |
| finished words | 6,804 | 5,904 |
| **per 1,000 words** | **$3.35** | **$5.35** |
| cache read | 86.8M | **135.4M** |

Cache read is again the overwhelming majority of the bill; output was 272,751 tokens. **Setup got
cheaper and chapters got dearer**, and the total per finished word rose 60%. The read-set is
bounded by design, but it grew: 135.4M cache read against 86.8M for a comparable five chapters.

**Per-chapter attribution worked for the first time.** Run #2's buckets were destroyed by an
end-of-run formatting sweep, and `trace` has warned about that signature since. This run has no
bucket under two minutes, so the per-chapter figures above are real:

| ch | responses | wall | cost |
|---|---|---|---|
| 1 (+ all setup) | 124 | 34m 53s | $11.28 |
| 2 | 36 | 6m 06s | $4.35 |
| 3 | 19 | 2m 19s | $2.35 |
| 4 | 27 | 3m 10s | $3.48 |
| 5 | 36 | 4m 55s | $4.96 |

## The cold chapter — the flat-cost claim, finally tested

`docs/benchmark.md` has listed this as untested since run #2: *"it needs a cold agent writing
chapter N with only `novels/<slug>/` in context."* Run #4 did it. A second agent, new session, no
conversation history, was pointed at the finished five-chapter novel and told to write chapter 6
through the full contract.

| | warm (chapters 2–5) | cold (chapter 6) |
|---|---|---|
| cost | $3.79 mean | **$3.21** |
| API responses | 30 mean | 46 |
| wall | 4m 07s mean | 16m 44s |
| skills opened | — | **24 of 44** |
| **draft cards opened** | **5 across four chapters** | **17** |
| **audit cards opened** | **0** | **16** |
| words | 1,044 mean | 1,249 |

**Cost per chapter is flat — slightly better than flat.** The claim holds.

The finding nobody was looking for is the rest of the table. The cold agent reported, unprompted,
*"Every pass ran with its card; none rotated."* The trace confirms it: 16 audit cards for one
chapter, against zero for the five that preceded it. It also caught two things the warm run had
left — an unpopulated `state/timeline.md` Log table that had been skipped for five chapters, and a
location used in chapter 5's prose but never given a bible row.

It took four times the wall clock of a warm chapter, which is the honest cost: reading the cards
is most of what the extra time buys.

## What the chapters look like

Against run #3 — and note that **run #3's numbers are post-redraft**. Every one of its five
`gate>` lines begins "full redraft per coordinator note": a human read them and directed the
repair. Run #4 had no such intervention at any point.

| | run #3 (redrafted) | run #4 (first pass) |
|---|---|---|
| body words | 4,695 | **5,904** |
| `sw audit` | 0 defects, 16 warnings | **0 defects, 11 warnings** |
| `para-opening` | 4 of 5 chapters | **1 of 5** |
| `echo` | 1 | **0** |
| `speech-share` below target | 4 of 5 | **3 of 5** |
| `campaign-clause` | 2 | 2 |
| `eq` warning | present | **gone** |
| interruptions across 5 chapters | 3 | 3 |
| longest turn, by chapter | 21 / 43 / 19 / 30 / 28 | 37 / **48** / 23 / 39 / 36 |

Read this honestly:

- **The habit findings improved materially, unaided.** `para-opening` stopped being a habit and
  `echo` disappeared. Run #3 needed a directed redraft to get where run #4 arrived on its own.
- **Dialogue got more varied and longer.** Turn-length spread rose (7.4–14.1 against 4.9–10.5),
  which is the good direction. But chapter 2's longest turn is **48 words, past the 45-word
  `TURN_CEILING`**, and that breach is a `note` — so it never reaches the WATCH row and the next
  chapter is not warned about it. Run #3's post-redraft ceiling was 43.
- **`speech-share` is still a habit at 3 of 5.** Third run in a row. The gate keeps repairing it
  per chapter rather than the draft avoiding it.
- **The gate did real work by itself.** Its own `gate>` lines: *"re-pointed event/delivers to the
  tea scene, the actual longest scene"* (the event-gets-the-scene rule, caught unaided),
  *"added one interruption for texture"* (run #2's R1 defect, self-corrected), *"split two
  overlong turns with beats/interjections"*.

The last point matters more than it looks. The gate produced these repairs **without opening a
single audit card**. Whatever `revision-pass`'s body and the model's priors carry is doing the
work, and the twenty audit cards are not.

## Toolkit defect log

| # | finding | severity | status |
|---|---|---|---|
| T1 | **`sw trace`'s skill detection is blind to Bash reads.** It scans `file_path`/`path` arguments and the `Skill` tool, never a shell command string. It reported **"0 of 44 skills opened"** for a run that opened thirteen, because the model read them with `cat`/`sed` | **high** | **fixed** — the scanner now reads command strings too; run #4's number was recovered retroactively |
| T2 | **Contract fidelity decays inside a session.** 5 cards opened across five warm chapters and zero audit cards, against 33 in one cold chapter of the same novel. `readset` printed the full resolved set with paths on every invocation in both cases | **high** | **open** — the finding of the run |
| T7 | **`sw readset` silently dropped the voice matrix, the growth ladder and the competence grid.** `_match` compared whole name cells for equality, so a `chg>` line naming `Yakumo` never matched the matrix row `Yakumo Kurama` — and the read-set header tells the drafter not to open the source files for anything it lists. Caught only because the cold agent went and read them anyway | **high** | **fixed** — token matching, with a single shared token accepted only when it belongs to one row |
| T3 | **The three-candidate step and Pass Z4 leave no artifact**, so neither can be evaluated by any run | medium | **fixed** — two optional CCS lines, `cand>` and `z4>`; `sw history` has a `widening` section and the read-set echoes the last five answers |
| T4 | **`sw lint`'s `[group-scene]` check matches on any name token ≥2 characters**, so a shared clan surname matches every clan member. In a Kurama-clan novel it flagged four speakers in scenes with one | medium | **fixed** — a token shared by several rows is dropped |
| T8 | **`[group-scene]` never attributes a spoken span to a person**, so a character named inside someone else's line counts as present and speaking. Its message claimed otherwise | low | **fixed** — the note now states what it measures and says naming is not speaking |
| T5 | **Nothing checks CCS block ordering.** A block landed out of sequence and `sw state`/`sw lint` passed it — they check block *content*, never block *sequence*. Caught by the writing agent on a manual re-read | medium | **fixed** — `sw state` checks the sequence, and `selftest` plants one |
| T6 | **`sw curve` requires a `pwr>` line on every CCS block once `scaling.shape` is not `none`, including chapters with no confrontation.** Stated in the reference but the worked example shows only the combat case; the agent missed it until chapter 5 and had to backfill all five blocks | low | **fixed** — the message and the audit card give the no-contest form outright |

T1 is the one that should worry a maintainer most, because it is a **measurement** defect and the
finding-9 number is what runs #1, #2 and #3 were all scored on. Those numbers are only valid for
runs in which the model happened to read with the `Read` tool.

## What reading the chapters found

Added 2026-09-12. Limitation 6 below said no human had read run #4's output, and that every
decisive finding in runs #1–#3 came from exactly that. Somebody read them. The two findings are
not about the prose — which is good, and the gate's unaided repairs hold up — but about what the
toolkit is able to *see*.

### A. Every habit-shaped check was invisible to both habit detectors

`cmd_lint.check_counts` built its `checks` dict from defect- and warn-level findings only. Both
cross-chapter mechanisms read it: the read-set's WATCH row and `sw history`'s habit table.
Meanwhile every check that measures a habit is deliberately a **note**, because one antithesis is
good writing and one uninterrupted scene is a scene.

So the findings that are *only* meaningful across chapters were structurally excluded from the
only two things in the toolkit that look across chapters.

| check | fired on | reached WATCH | in `sw history` |
|---|---|---|---|
| `house-style` (the `X, not Y` antithesis) | **5 of 6** | no | no |
| `filter-verb` | 5 of 6 | no | no |
| `texture` (nobody interrupted, no contractions, over-long turns) | 4 of 6 | no | no |
| `weasel` | 2 of 6 | no | no |
| `turn-length` past `TURN_CEILING` | ch2 at 48, ch6 at 49 | no | no |

The antithesis rate across the book is **25 constructions in 7,153 words — 3.5 per 1,000, rising
to 7.2/1k in chapter 6**, against run #2's 2.5/1k on the same tell. It is the construction
`prose-quality/references/ai-default-tells.md` documents best and it got *worse*, unseen, because
no single chapter crosses the 6.0/1k per-chapter threshold.

This page had already noticed the chapter-2 turn-length case and called out exactly this
mechanism — *"that breach is a `note` — so it never reaches the WATCH row"* — and treated it as
one check's problem. It was the whole tier's.

Fixed. Notes now feed both detectors, in a second bucket. Two things the first attempt got wrong:
notes fire far more often, so a frequency-first sort evicted every recurring warn from a
three-item row — warns rank strictly above notes now, and `WATCH_CAP` went 3 → 4. And the note
tier holds two different kinds of thing: `group-scene` reports what a chapter *contains* and its
own message ends *"Read it and discount it"*. `rules.HABIT_NOTE_CHECKS` is an allowlist,
`SITUATION_NOTE_CHECKS` its counterpart, and a test fails if a note check lands in neither.

No note was promoted to a warn or a defect. Per-chapter lint output is byte-identical on both
live novels — the invariant that matters, given this repo has twice built a number that decided
whether a chapter shipped and had it optimised rather than satisfied.

### B. "A prohibition is satisfied by silence" recurs, and nobody had swept for it

`thought-budget` checked only the ceiling. `CLAUDE.md` hard rule 7 declares `'…'` direct thought
at **1–3 per chapter**; run #4 wrote **zero in four of six chapters**, and neither lint, nor the
gate, nor the ledger said a word. The channel the user chose deliberately went unused in
two-thirds of the book.

That is run #3's rule-9 discovery — *a drafter who never mentions the body never contradicts the
ledger* — recurring on a different rule. The repo named the failure shape and never checked
whether any other rule had it.

The sweep found one more, and it is the sharper one: **the gate's own form check was made
entirely of prohibitions.** Rule 9's *twice* — the rule written specifically to close this hole
for the body ledger — lives in `mc-design/references/form-ledger.md` and had never reached a
checkbox in `revision-pass`. Every box in that check was satisfiable by an empty chapter.

Both are fixed; the floor is a note, because one interior-free chapter is a choice and a run of
them is the finding, which is what finding A's tier is now for.

Checked and **not** a problem: `set>` facts, recorded on every block of both novels. Deliberately
left unscripted: `world-texture`'s non-visual detail, and the plain-sentence third —
`textstats.py` documents why shape cannot see the latter, and that decision stands.

### C. `state/timeline.md` reached no read-set at all

Written every chapter by `continuity-summary`, gated by `revision-pass` Pass 1 and
`plot-threads`' audit card, exported by `sw export` — and absent from `sw readset`, including
from its NOT LOADED list, so a drafter could not have asked for it by name. That is the mechanism
behind the cold agent finding its Log table empty for five chapters.

### What this says about the run's numbers

"0 defects, 11 warnings" was true and meant less than it sounded, in a way nobody could have
measured at the time: three of the book's five most-fired checks could not reach a warning at
all. Re-linted today the same six chapters raise **five** `history-habit` findings. The chapters
did not change.

## What run #3 established

Reconstructed from `novels/naruto-will-not-be-sealed/` and its ledger, since no write-up was made
at the time. Run #3 wrote five chapters of a Naruto reincarnation fanfic and its shipped state was
reached by a **coordinator-directed redraft of all five chapters**. What that redraft had to fix,
in its own `gate>` lines, is the evidence behind six rules now in the corpus:

| what the redraft fixed | what it bought |
|---|---|
| Turns cut from essay length — a 107-word speech, a 73-word "best liar" essay, a 50-word longest turn | `dialogue-voice` §How it sounds spoken; the ~45-word ceiling in `CLAUDE.md` §5 |
| A mother and her six-year-old with different declared axes, a clean `sw cast`, and one voice between them | **the cadence test** (`voice-separation` §3), `references/age-register.md`, and the `cadence` axis |
| `form_locked` applied but decorative — zero limit-that-bites beats in five chapters, every check green | **`CLAUDE.md` hard rule 9's second half**: a prohibition is satisfied by silence, so the form must reach the page twice per chapter |
| Stray italics used as emphasis | `narrator-voice`'s "nothing else is markup" clause and `lint`'s italic rule |
| Em-dash density, sentence-rhythm runs, weasel words, a `"A beat."` fragment | `prose-quality/references/ai-default-tells.md` |
| A setup that never paid off as a physical limit | `story-craft`'s build-up thesis |

Run #3's lasting contribution is **hard rule 9's silence clause**, and it is the sharpest lesson
in the repo's history: five chapters passed every check precisely *because* the drafter never
mentioned the body it was forbidden to get wrong.

## What runs #1 and #2 established

| finding | status at run #4 |
|---|---|
| #1/5 — dialogue starvation (2–5% speech) | fixed; 12–30% here |
| #1/6 — chapters cluster at the word floor | fixed; length gate removed entirely, spread 952–1,728 |
| #1/10 — no world anchor | fixed; anchor vocabulary present from chapter 1 |
| #1/11 — foreknowledge planned to fail before it worked | fixed; first legible win at chapter 4 |
| **#1/9 — never-optional skills never load** | **regressed.** 21 always-in-play skills never opened, including all four run #2 fixed: `bias-guard`, `voice-separation`, `competence-map`, `prose-quality` |
| #2/R1 — nobody is ever interrupted | improved; 3 interruptions, one added by the gate on purpose |
| #2/R2 — characters arrive unintroduced | holds; `sw cast`'s debut ledger clean |
| #2/D1 — any numeric ship gate gets gamed | holds; no gate was gamed, because no per-chapter number decides shipping |

## The lesson, updated

Run #1 removed word count as a ship gate. Run #2 removed dialogue share. Both had been optimised
rather than satisfied. Run #4 adds a different one, about instruction rather than measurement:

**The session, not the corpus, is what the contract is spent against.** The read-set is complete
and correct. The cards are resolved, conditional ones skipped, each named with a path and a
one-line description of the decision it makes. Handed that list from a cold start, a Sonnet-class
model opens essentially all of it for $3.21. Handed the identical list an hour into the same
conversation, it opens five files across five chapters and none of the gate's.

This is a correction to `docs/creative-latitude.md`, which argued from token counts that the
**corpus** is the binding constraint on quality and proposed a prune. The measurement here does
not support that as the first move: the same corpus, the same 17,000 words of instruction, was
affordable cold and unaffordable warm. What decays is not the size of the instruction but the
model's willingness to spend context on it once the conversation is long.

That does not retire the prune — 16,550 words of instruction before a line of story state is still
worth reducing, and `sw load` now prints the unconditional word figure so the next attempt has the
right number. It re-orders it. **The cheaper and larger win is to make a fresh session per chapter
the default path rather than an efficiency tip**, which `README.md` currently recommends for cost
alone. It turns out to buy contract fidelity, and that is the more valuable half.

The uncomfortable part stands: the warm chapters were **good** — 0 defects, fewer warnings than
run #3's directed redraft — and were written almost entirely without the cards. Whatever
`CLAUDE.md`, the read-set and the model's priors carry is doing more of the work than the corpus
is, and no run before this one could have told the difference.

## Limitations

1. **5 chapters, not 30.** Arc rollup, long-run voice drift and `timeline-engine` at scale remain
   untested.
2. **One run, one model, one genre.** Still no variance estimate, and all four runs have been
   Naruto fanfic. A non-fanfic run is the obvious next one.
3. **The warm/cold contrast is n=1 on each side.** One warm run of five chapters against one cold
   chapter. It is a large effect (5 cards against 33) with an obvious mechanism, but it is two
   samples, and the cold chapter is also the *sixth* chapter of a book that was already built —
   an easier job than chapter 1. Repeat it before restructuring anything on the strength of it.
4. **Candidates and Z4 remain unevaluated** (T3).
5. Cache multipliers are the standard published ratios, not confirmed for this account.
6. ~~**No human has read these chapters.**~~ **Done, 2026-09-12** — see *What reading the
   chapters found* above. It held again: two defects, neither visible to any script, and the
   larger of them was a blind spot in the scripts themselves.

## Reproduce it

```bash
python3 -m unittest discover tests    # 331 tests
python3 scripts/sw.py selftest        # the pipeline, plus planted defects that must be caught
python3 scripts/sw.py health          # wiring only
python3 scripts/sw.py audit  novels/<slug>
python3 scripts/sw.py trace  --session <agent-id>
```

**Scope every `trace`.** With no window it aggregates every session that ever ran in the repo. A
time window alone is not enough either: the session driving an agent runs in the same repo at the
same time. Use `--session`.

**The novels are not in the repo.** `.gitignore` excludes everything under `novels/` except the
template. The numbers here and the test suite are the surviving artifacts.

### The measurement rules that produced these numbers

Claude Code writes one transcript row per **content block** and repeats the whole `usage` object
on every one — this run: 1,105 rows carrying 277 responses, a 1.78x inflation on the input side.
Group rows into responses by `(requestId, message.id)`, take input-side fields once per group, and
take `output_tokens` as the group **maximum**. `scripts/swlib/transcripts.py` does this, with a
named regression test for each rule.

And, new in this run: **count a skill as opened whether its path arrives in a tool argument or
inside a shell command.** T1 is what that rule is for.
