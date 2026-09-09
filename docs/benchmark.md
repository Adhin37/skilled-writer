# Benchmark — test run #2

Second end-to-end run of this toolkit, instrumented. Run on 2026-09-09.

This page replaces the run #1 benchmark entirely. Run #1 measured a 37-skill toolkit that no
longer exists: the delivery gate, the four text channels, `story-opening`, `meta-knowledge`,
`power-scaling` and the draft/audit card system all landed after it, and every one of its
headline numbers was measured against different code. What survives from it is recorded here as
*what run #1 established*, and nothing else.

The purpose was not to produce a novel. It was to find out what the toolkit costs to operate and
what breaks under load. It found six defects in the toolkit's own instrumentation — three of them
**dead or gameable checks** — and two defects in the prose that no check could see at all.

## TL;DR

| | |
|---|---|
| Model | Claude Sonnet 5, driven as a subagent |
| Produced | 1 scaffolded novel + **5 revised chapters**, 6,804 words |
| Writing run | **$21.02**, 51 min, 236 API responses |
| Revision run | **$1.79**, 10.5 min, 33 API responses |
| **Total** | **$22.81** |
| Cost per 1,000 finished words | **$3.35** |
| Skills that loaded | **27 of 41** (run #1: 16 of 37) |
| Toolkit defects found | **6** (2 high) — all fixed |
| Prose defects found *by a reader*, invisible to every check | **2** |

**The headline is not the cost.** It is that the novel passed every command in the repo — zero
defects, clean `audit`, clean `curve`, clean `cast` — and the first human to read it said the
dialogue did not sound like people and the characters were never introduced. Both were true. Both
were measurable. Neither was measured.

## What was tested

| parameter | value |
|---|---|
| Genre | `fanfic` — the heaviest configuration; it activates `fanfic-canon` + `timeline-engine` |
| Source | Naruto, **complete canon timeline** (Part I → Shippuden → post-war), `ooc_budget: low` |
| MC | transmigrator, adult, foreknowledge at `major-beats` grain, `intel_tier: 3` |
| Divergence | one: an additional Uchiha survivor extracted from the massacre |
| `timeline.reactivity` | 4 (adaptive) |
| Optional toggles | left at documented defaults; none changed |
| Harness | **one persistent subagent** for init + all 5 chapters; a **second** subagent for the revision |

The writing agent was given a pure authoring brief with no mention that it was being measured, and
told not to read `docs/`. Had it known which defects it was scored on, the skill-loading
measurement would have been worthless.

## Cost and time

### The two runs

| run | wall clock | responses | cache read | output | cost |
|---|---|---|---|---|---|
| Writing (init + ch 1–5) | 51.1 min | 236 | 86.8M | 222,318 | **$21.02** |
| Revision (ch 1–5) | 10.5 min | 33 | — | — | **$1.79** |

Cache write was 569,244 tokens, all 5-minute TTL; fresh input was 472 tokens. Base rates are the
published Sonnet 5 API rates ($2.00/M in, $10.00/M out) with the standard cache multipliers. **If
your rates differ, every dollar figure scales linearly.**

### Where the money goes

Cache read is **83%** of the writing run's bill. Output — the actual prose and thinking — is 11%.
You are not paying to write; you are paying to re-read state. Anything that shortens the read-set
is worth more than anything that shortens the prose.

### Per-chapter attribution does not work on this run, and the report says so

`trace` attributes cost by each chapter file's **last** write. The agent did a formatting sweep
across all five chapters in the final twenty seconds, so the buckets came out as ch2 $11.76 /
ch5 $6.30 / ch1 $1.28 / ch3 $0.23 / ch4 $0.11. Only the run total is trustworthy. `trace` now
warns when a chapter's bucket holds under thirty seconds of work, which is the signature.

## What run #1 established, and what changed

Run #1's four high-severity prose defects were fixed by the rewrite. Run #2 confirms all four:

| run #1 finding | run #1 | run #2 |
|---|---|---|
| 5 — dialogue starvation | 2–5% speech | **10–27%** |
| 6 — chapters cluster at the word floor | all 5 within 59 words of `min_words` | no clustering; length gate removed entirely |
| 10 — no world anchor | **0** anchor terms in 10,290 words | present from chapter 1 (10 hits) |
| 11 — foreknowledge planned to fail before it ever worked | first win never scheduled | win ch 2, first failure ch 9 |
| 9 — four never-optional skills never loaded | `bias-guard` 0, `voice-separation` 0, `competence-map` 0, `prose-quality` 0 | **all four loaded** |

**Cost rose 3.4x per finished word** — $0.98/1k in run #1 against $3.35/1k here. The toolkit got
more thorough and more expensive in the same change: 27 skills opened instead of 16, and 86.8M
cache read instead of 25.4M. That is a trade, and it should be stated as one rather than buried.

## The two defects no check could see

Both were found by a human reading chapter 1. At that moment every command in the repo reported
the novel clean.

### Dialogue that does not sound like people

> "I already have issues with dialogue — it doesn't seem like people speaking normally. Check any
> high-ranked Naruto fanfic and the opening is not this stiff and awkward."

The chapters ran 25% dialogue, comfortably inside the 25–40% target. Share says how **much** the
cast speaks and nothing about how it sounds. Measured after the fact with a new `lint` section:

| ch | lines | mean words | contractions/100 | fragments | **cut off** | longest exchange | narration between |
|---|---|---|---|---|---|---|---|
| 1 | 43 | 10.6 | 9.9 | 16% | **0** | 13 | 28 |
| 2 | 14 | 10.2 | 7.7 | 43% | **0** | 3 | **88** |
| 3 | 24 | 11.6 | 7.9 | 25% | **0** | 7 | 38 |
| 4 | 20 | 15.3 | **3.6** | 30% | **0** | 4 | 28 |
| 5 | 13 | **23.4** | 7.2 | 38% | **0** | 3 | 40 |

**Zero interruptions across 114 spoken lines.** Nobody in the book is ever cut off or trails away.
Chapter 5 averages 23 words a line — people making speeches. Chapter 2 puts 88 words of narration
between one spoken line and the next, which is dialogue carrying exposition rather than a scene.

`sw cast` gained a `near-clash` check at the same time and immediately found the structural cause
in chapter 1: the two speakers share **intel 3 + articulacy 3** and differ only in a `wit` label.
The existing `three-way-clash` requires all three axes to match, so it passed them — correctly,
and uselessly, because wit is a label that can go a whole chapter without surfacing. That is a
finding about the rule in `CLAUDE.md` section 4, not only about the code.

### Characters who are never introduced

> "It's not just about cutting people off. I mean they are not even introduced. It feels like I
> should know them and everything in their life. But that's not how a story is written."

This is the sharper defect. Chapter 1 originally introduced its second character as *"she went to
find Enko before Enko found the discrepancy first"* — a name with no role, no relationship, no
physical presence — and then ran a scene of loaded subtext between two people the reader had not
met. The prose was written as though the reader were resuming a story they already knew.

Nothing in the toolkit looked at a character's **first** appearance. `cast` audits the matrix,
`character-profile` owns the profile, `story-opening` owns the world anchor, and between them a
named character could walk on with no placement at all and every check stayed green. The revising
agent reported the same gap independently and without prompting:

> "There is no owned rule anywhere for 'a named character's first appearance must let the reader
> place them.' … I worked from craft judgment plus the coordinator's own framing, not from a skill
> file, which is exactly the kind of ambiguity `CLAUDE.md` says shouldn't exist."

`sw cast` now prints a **debut ledger** — where each character first appears, how many words pass
before they speak, and the sentence they arrive in. It prints and does not score.

## The lesson that keeps repeating: never build a numeric ship gate

Run #1 removed word-count gating because chapter 5 landed on `min_words` **exactly**. The
replacement metric was dialogue share, with a floor of 10% raised as a **defect**.

Chapter 2 of run #2 measured **10.2%**. The writing agent, unprompted and not knowing it was being
measured, explained why:

> "Chapter 2 … organically wanted under 10% dialogue. … I resolved it by giving Suzune an
> aloud-muttering habit (defensible, in-character, but **retrofitted to satisfy the gate rather
> than chosen for its own sake**)."

That is run #1's finding 6 reproducing exactly, on a new metric, two rewrites later. **Any number
that decides whether a chapter ships will be optimised, and prose optimised toward a number is
padded prose.** The floor is now measured as a five-chapter rolling mean, so no single chapter has
a number to write toward. Every dialogue-texture measurement added since is a **note** — there is
a test asserting they can never be raised to a defect.

## Toolkit defect log

| # | finding | severity | status |
|---|---|---|---|
| D1 | **The dialogue floor is a per-chapter ship gate and it was gamed in five chapters** (10.2% against a 10.0% defect threshold) | **high** | **fixed** — rolling five-chapter mean |
| D2 | **`curve` printed an empty report and two of its checks were dead.** Its only `rep.info` sat behind `if not series: return`, so a novel logging no pressure rows got a permanently clean curve — and `_flat()`, the enforcement of hard rule 11, never ran | **high** | **fixed** — unconditional position section, checks moved out of the guard, empty-log finding |
| D3 | **Two checks existed for hard rule 7 and neither fired.** The scene-break check enumerated wrong forms and missed a lone `*`; `STRAY_MARKUP` had a rule for `**bold**` and none for `*italic*` | medium | **fixed** — blocklist inverted, italic rules added |
| D4 | **`revision-pass` never named `mtl-detox`**, so it loaded zero times. `health` could not see this: its card check is card-anchored, and `mtl-detox` had no card | medium | **fixed** — card written, named, skill-anchored `health` check added |
| D5 | **`trace` had no run scoping**, and `by_chapter` guarded the tail but not the head, so every prior session in the repo fell into chapter 1's bucket | medium | **fixed** — `--since`, `--until`, `--session` |
| D6 | Arc-level checks judged an unfinished arc — `arc -a 1` raised a **DEFECT** at chapter 1 | low | **fixed** |
| R1 | **Dialogue does not sound spoken** — 0 interruptions in 114 lines, no fragments, exposition between every line | **high** | measured; partially repaired |
| R2 | **Characters arrive unintroduced** — no skill owns "a first appearance must place the person" | **high** | measured; repaired in ch 1; **rule still unowned** |

### D3, in detail — the checks were there

Both root causes were confirmed by injecting the defect into a throwaway copy:

- The scene-break check matched `***`, `---`, `~~~`, `===` and `* * * *`. A lone `*` matched none
  of them, and escaped `STRAY_MARKUP`'s bullet rule too, because that requires whitespace *and* a
  non-space character after the bullet. The writing agent produced this malformation three times
  and caught it only by manual grep.
- Italics had no rule at all, so `*She would not make it to the gate in time.*` — the exact
  hard-rule-7 violation the four channels exist to prevent — passed silently.

When the italics rule was added it immediately found a **live violation the agent believed it had
already fixed**: a written notice italicised in chapter 4.

Enumerating wrong answers cannot be complete. The check now matches anything break-shaped and
compares it against the one right answer.

## What the revision run did

A second subagent was given the reader's complaint in the reader's own words and told to run
`revision-pass` on chapters 1–5. It cost **$1.79** and opened five skills: `dialogue-voice` ×3,
`story-opening` ×3, `character-profile`, `revision-pass`, `voice-separation`.

| ch | mean words/line | | contractions/100 | | speech share | |
|---|---|---|---|---|---|---|
| | before | after | before | after | before | after |
| 1 | 10.6 | 10.1 | 9.9 | 9.9 | 25.1% | 23.6% |
| 2 | 10.2 | 10.2 | 7.7 | 7.7 | 10.2% | 10.2% |
| 3 | 11.6 | 11.7 | 7.9 | 7.8 | 22.2% | 22.3% |
| 4 | 15.3 | **12.0** | 3.6 | 3.8 | 26.6% | 25.1% |
| 5 | **23.4** | **12.7** | 7.2 | 8.8 | 26.1% | 19.7% |

Read this honestly:

- **Chapters 4 and 5 improved materially.** Chapter 5's speeches came apart into speech — mean
  turn length 23.4 → 12.7 words, spread 26.9 → 6.9. The agent diagnosed this itself as the MC's
  prose not obeying her own declared `artic 3` / `heat: banked` row.
- **Chapters 1–3 barely moved**, and chapter 2 was deliberately left alone.
- **Nobody is still ever cut off.** 123 lines now, still zero interruptions.
- **Texture improved at the cost of share.** Trimming long speeches shortened lines without adding
  new ones, so dialogue share *fell* — four chapters now sit under the 25% target where two did
  before. Two measurements of the same subsystem moved in opposite directions, and the repair the
  reader wanted is the one that made the older metric look worse. That is worth knowing before
  anyone tunes toward either number.
- The italics defect was fixed. `audit` reports **0 defects**.

The reader's underlying complaint is **not resolved**. It is now measured, which is the difference
between a defect you can work on and one you argue about.

## Skill loading

**27 of 41** skills opened during the writing run, against 16 of 37 in run #1. All four skills
that never loaded in run #1 now load. The two skills added by the rewrite were the most-opened in
the run: `meta-knowledge` ×3 and `story-opening` ×3.

Still never opened, though `CLAUDE.md` section 3 lists them as always in play: `chapter-plan`,
`story-bible`, `social-fabric`, `no-harem`, `combat-choreography`, and — before the fix —
`mtl-detox`. `chapter-plan`, `story-bible` and `social-fabric` produced their files anyway through
`novel-init`'s orchestration, so the artifact exists without its owner's reasoning ever entering
context. That is run #1's finding 9 in its original shape, narrowed but not gone.

The revision run opened only five skills — the ones its brief pointed at. A targeted revision does
not exercise the full ten-pass gate, so **D4's fix is wired but still unproven in a real run.**

## What worked

- **The delivery gate held.** All five chapters carry a `delivers:` clause naming a difference,
  5/5 CCS blocks, no length clustering at any threshold.
- **Foreknowledge is ordered correctly** — first win at chapter 2, first failure scheduled at 9.
  Run #1 had this exactly backwards and scheduled the correction before the thing being corrected
  had ever worked.
- **The agent reported its own toolkit friction accurately and bluntly**, including the gate it had
  gamed and two `lint` blind spots — both of which I confirmed independently by probe. It also
  identified the unowned first-appearance rule without being told the rule was missing.
- **`selftest` and `health` did their jobs.** 8/8 positive controls, 0 wiring defects.

## Limitations

1. **5 chapters, not 30.** Arc rollup, long-run voice drift and `timeline-engine` at scale are
   untested.
2. **One run, one model, one genre.** No variance estimate.
3. **The flat-cost claim is still untested.** Both runs used one persistent session by
   construction. It needs a cold agent writing chapter N with only `novels/<slug>/` in context.
4. **The prose repair is partial.** R1 and R2 are measured, not solved.
5. Per-chapter cost attribution was destroyed by the agent's cleanup sweep (above).
6. Cache multipliers are the standard published ratios, not confirmed for this account.

## What R1 and R2 led to

Both reader findings are now owned by a skill, stated in `CLAUDE.md`, and measured:

| | rule | measured by |
|---|---|---|
| R2 | `character-profile` §First appearance — relation, power, one concrete stroke, delivered in motion. Wired into `revision-pass` Pass 2 and its audit card | `sw cast` debut ledger |
| R1 | `dialogue-voice` §How it sounds spoken, with `references/spoken-register.md` carrying the measured failure and the repair table. Added to `prose-quality`'s card | `sw lint` dialogue texture |

`CLAUDE.md` section 4's corollary to hard rule 8 was tightened: two speakers may not share **intel
and articulacy together**, not merely all three axes. Wit is a label and can go a whole chapter
without surfacing, so a pair alike but for wit is one voice on the page — which is what
`near-clash` found in chapter 1. A second corollary now carries the first-appearance rule, and
section 5 gained two entries: no prepared statements, no character who arrives pre-loaded.

`sw cast` also gained **declared-vs-measured turn length**. This closes the gap the revising agent
named as the reason the defect survived several revision passes: `lint`'s texture line is a mean
across all speakers, so one character's turns can double while the chapter average stays healthy.
Attribution is conservative — a line counts for a speaker only when exactly one cast name appears
around it — and coverage is printed (46 of 123 lines on this novel) so the number can be weighed
rather than trusted.

## Still open

- **No compaction-event detection in `trace`**, which is what drives the cost curve in a long
  persistent session.
- `mtl-detox`'s wiring fix is unproven in a full revision pass — the revision run here was
  targeted and opened only five skills.
- **The prose repair is still partial.** The rules now exist and are measured; chapters 1–3 of this
  novel have not been revised against them, and nobody is yet ever interrupted.
- **The flat-cost claim.** Unchanged: it needs a cold agent writing chapter N with only
  `novels/<slug>/` in context.

## Reproduce it

```bash
python3 -m unittest discover tests    # 193 tests
python3 scripts/sw.py selftest        # the whole pipeline, plus 8 planted defects that must be caught
python3 scripts/sw.py health          # wiring only - says nothing about whether the advice is good
python3 scripts/sw.py audit  novels/<slug>
python3 scripts/sw.py trace  --session <agent-or-session-id>
```

**Scope every `trace`.** With no window it aggregates every session that ever ran in the repo —
on the machine that produced this run, 22 sessions and $225 of toolkit development. A time window
alone is not enough either: the session *driving* an agent runs in the same repo at the same time,
and its own file reads will be counted as the agent's skill loads. Use `--session`.

**This run's novel is not in the repo.** `.gitignore` excludes everything under `novels/` except
the template. The numbers here and the test suite are the surviving artifacts; the suite plants
the run's own defects into a synthetic novel and asserts they are caught.

Counts are as of run #2 (41 skills). `python3 scripts/sw.py health` prints the current inventory
and checks it against `CLAUDE.md` section 3.

### The measurement rule that produced these numbers

Claude Code writes one transcript row per **content block** of an API response and repeats the
whole `usage` object on every one. This run's writing agent: 1,068 rows carrying 236 responses.
Summing rows bills one request up to seven times — it overstated run #1 by 3.6x. Group rows into
responses by `(requestId, message.id)`, take the input-side fields once per group, and take
`output_tokens` as the group **maximum**, because it is a streaming counter whose early rows hold
partials. `scripts/swlib/transcripts.py` does this, with a named regression test for each rule.
