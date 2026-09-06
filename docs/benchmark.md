# Benchmark — test run #1

First end-to-end run of this toolkit, instrumented. Run on 2026-09-05.

The purpose was not to produce a novel. It was to find out what the toolkit costs to operate, and
to find the defects that only appear under load. It succeeded at both, and it was **stopped
deliberately at chapter 5** because it found two systemic defects worth fixing before spending
another ~$90 reproducing them 25 more times.

## TL;DR

| | |
|---|---|
| Model | Claude Sonnet 5, driven as a subagent |
| Produced | 1 scaffolded novel + **5 revised chapters**, 8,140 words |
| Wall clock | **58 minutes** of model time (66 min including review) |
| Cost | **$28.39** |
| Setup (interview + full scaffold) | **$20.76**, 42 min, one-time |
| **Steady-state cost per chapter** | **~$1.91 and ~3.7 min** |
| Cost per 1,000 finished words | ~$1.17 at steady state |
| Skills that actually loaded | **16 of 37** |
| High-severity defects found | **3** (all fixed) |

**A 30-chapter arc would have cost roughly $115 and ~3 hours.** A 250-chapter novel would not
cost 250 x $1.91 — see [The flat-cost claim](#the-flat-cost-claim), which is the one headline
number in the README that this run does **not** support.

## What was tested

| parameter | value |
|---|---|
| Genre | `fanfic` — chosen because it activates the largest skill surface (`fanfic-canon` + `timeline-engine`) |
| Source | Naruto, manga Parts I-II only, `ooc_budget: low` |
| MC | reincarnator, `form_locked: true` (age 4 -> 12), `intel_tier: 4` |
| Divergence | one change: a canon character survives an event he does not survive in canon |
| `timeline.reactivity` | 4 (adaptive) |
| Harness | **one persistent subagent** across init + all 5 chapters, driven by messages, simulating a single continuous author session |

The MC configuration was deliberately chosen to exercise the two least-tested mechanisms in the
repo: the `state/body.md` form ledger, and bounded foreknowledge under `competence-map`.

## Cost and time

### Per phase

| phase | wall clock | turns | cost |
|---|---|---|---|
| Interview (1 round, 6 batched questions) | ~5 min | 10 | — |
| Scaffold (19 files) | ~37 min | 45 | — |
| **Setup total** | **42 min** | **55** | **$20.76** |
| Chapters 1-5 | 23 min | 145 | $7.63 |
| **Total** | **58 min** | **200** | **$28.39** |

### Per chapter (steady state)

Chapter 1's bucket absorbs all of setup. Chapters 2-5 are the honest per-chapter figures.

| ch | min | cache read | cache write | output | turns | cost |
|---|---|---|---|---|---|---|
| 1 (+setup) | 41.7 | 11.87M | 6.85M | 67,001 | 104 | ~$20.76 |
| 2 | 4.7 | 8.55M | 51K | 2,812 | 24 | $1.87 |
| 3 | 3.7 | 7.29M | 43K | 6,991 | 19 | $1.64 |
| 4 | 2.9 | 8.11M | 37K | 2,813 | 20 | $1.74 |
| 5 | 3.4 | 11.49M | 26K | 2,526 | 27 | $2.39 |

### Where the money goes

Token totals for the whole run:

| class | tokens | rate | cost |
|---|---|---|---|
| Cache read | 49,478,510 | $0.20/M | $9.90 |
| Cache write | 7,051,900 | $2.50/M | $17.63 |
| Output | 85,875 | $10.00/M | $0.86 |
| Fresh input | 400 | $2.00/M | ~$0.00 |

Two things to notice:

- **Output is 3% of the bill.** You are not paying for prose; you are paying to re-read state.
  8,140 words of finished chapter cost $0.86 to generate and $27.53 to think about.
- **77% of output tokens were thinking** (66,066 of 85,875).

Base rates ($2.00/M in, $10.00/M out for Sonnet 5) are the published API rates. Cache rates use
the standard multipliers — 5-minute cache write at 1.25x input, cache read at 0.1x input. This run
measured 100% 5-minute TTL, so no 1-hour rate applies. **If your rates differ, every dollar figure
here scales linearly.**

## The flat-cost claim

The README says the toolkit is built so that "chapter 250 costs what chapter 5 costs," on the
strength of the bounded read-set and the compressed CCS ledger.

**This run does not support that claim, and could not have.** Cache-read tokens per chapter went
8.55M (ch2) -> 7.29M -> 8.11M -> 11.49M (ch5). That is context accumulating inside one long-lived
session, not the read-set growing — but the cost is real either way, and it rose ~34% across three
chapters.

The honest statement is narrower and still useful:

> The **read-set** stays bounded, so the work of writing chapter 250 is bounded. The **session**
> does not. Cost per chapter is flat only if you start a fresh session periodically; in one
> continuous session it climbs with conversation length.

Testing the strong version needs a cold agent writing chapter N with nothing but `novels/<slug>/`
in context. That was not run here (the persistent-agent design was chosen deliberately, to surface
drift instead). **It is the single highest-value follow-up.**

## Skill loading — the most important finding

Only **16 of 37 skills** were ever read. That is not automatically bad; genre modules and disabled
optional skills *should* stay unloaded. What matters is *which* ones didn't load:

| skill | CLAUDE.md status | times loaded |
|---|---|---|
| `bias-guard` | "Non-negotiable", runs every chapter | **0** |
| `voice-separation` | "Always in play" | **0** |
| `competence-map` | "Always in play" | **0** |
| `prose-quality` | Runs inside `revision-pass` | **0** |
| `mtl-detox` | "Not optional", runs every chapter | 1 |
| `revision-pass` | QC gate | 1 |

`revision-pass` **was** loaded — and it carries condensed inline checklists for all of the above.
The model read the summary and never opened the source.

This is an architectural consequence, not model laziness: `revision-pass` is written to be
self-sufficient, so it is. The effect is a two-tier quality gate:

- Defects the checklist names **explicitly and mechanically** were caught cleanly. Zero banned
  MTL phrases, zero narration exclamation marks, zero default gestures across 8,140 words.
- Defects that need the **full skill's reasoning** — distributional properties, judgement calls —
  went unseen. Both high-severity findings below are of this kind.

If you rely on `bias-guard` or `voice-separation` doing what their own files say, be aware that on
this run neither file was ever in context.

## Defect log

| # | finding | severity | status |
|---|---|---|---|
| 0 | `novel-init` instructs `cp -r`, but shipped `settings.json` allowed only `ls/wc/find/grep/rg` — the repo denied its own documented happy path | medium | fixed (permissions) |
| 3 | Setup burns ~$21 and 42 min before chapter 1 exists | medium | documented, not a bug |
| 4 | `novel-init` reads all 11 template files individually before copying the tree | low | **fixed** — copy-first instruction added |
| 5 | **Dialogue starvation** — chapters ran **2-5% dialogue** against a 25-40% format norm | **high** | **fixed** |
| 6 | **Chapters cluster at the word floor** — 1600/1619/1619/1643/1659 against `target_words: 2000` | **high** | fixed, then **superseded** — see below |
| 10 | **No world anchor.** Zero occurrences of `Konoha`, `Uchiha`, `shinobi`, `chakra`, `ninja`, `village`, `Academy` or `Hokage` across 10,290 words. Nothing on the page identified the setting, the fandom, or the genre — while the suspicion plot escalated to `certain-something-is-off` by ch 4 | **high** | **fixed** — new `story-opening` skill |
| 11 | **The MC's foreknowledge never appears, and was planned to fail before it worked.** Zero on-page references to knowing the future; the plan introduced it as doubtful at ch 6 and disproved it at ch 12, and four of arc 1's five escalation rungs were foreknowledge failures | **high** | **fixed** — new `meta-knowledge` skill |
| 12 | **No convention for thought or meta text.** `lexicon.md` declared *italic, unquoted*; the prose used unmarked free indirect discourse throughout and italics for three other jobs at once | medium | **fixed** — four channels in `narrator-voice` |
| 8 | One supporting character's line was more logically sophisticated than her declared articulacy rating | low | open, chapter-level |
| 9 | **Four "never optional" skills never loaded** (above) | **high** | **fixed** — `revision-pass` now names which passes must open their source skill; `CLAUDE.md` §8 carves out the exception to self-sufficiency |

### Finding 5 — dialogue starvation

Every chapter passed all ten revision passes at 2-5% dialogue. Measured share by chapter: 2%, 3%,
4%, 4%, 5%.

The cause: **no dialogue-density guidance existed anywhere in 37 skills.** `dialogue-voice`
governs how a line *sounds*, never how many there are. So a model with an analytical POV voice
routes every beat through the protagonist's reasoning, and nothing objects.

This matters beyond register. `voice-separation`, `dialogue-voice` and `competence-map` — three
skills and a cast matrix, the most elaborate subsystem in the repo — all operate on spoken lines.
On a silent cast they do not fail; they **silently no-op**. There is nothing to tell apart.

Fixed by adding: a `## How much dialogue` section to `dialogue-voice` with a share table and the
diagnostic; a hold-while-drafting bullet, an anatomy note and two failure-mode rows to
`write-chapter`; and a measured check to `revision-pass` Pass 8.

### Finding 6 — chapters cluster at the floor

All five chapters landed 17-20% under `target_words`, every one within 59 words of `min_words`.
`revision-pass` Pass 9 checked "word count inside range" — and 1,600 *is* inside range — so the
target was never enforced. The defect is invisible in any single chapter and obvious across five.

Fixed by making `hook-and-pacing` state that the floor is a tolerance rather than a goal (target
±15%), adding a five-chapter trend check, and updating Pass 9 to check against target.

### Finding 6, revisited — the fix was the wrong shape

The ±15% repair worked, and then the defect moved. On the next reading, chapter 5 landed on
**exactly 1,600 words** — the declared `min_words`, to the word — and chapter 4's frontmatter
claimed 1,619 against an actual 1,887, a wrong number that had already propagated into
`state/continuity.md`.

The lesson is not that the tolerance was too loose. It is that **any number which decides whether
a chapter ships will be optimised**, and prose optimised toward a length is padded or truncated
prose. The word-count gate has since been removed entirely and replaced by a structural delivery
test — want, friction, **change**, cost, next — with length kept only as a measured fact whose
*accuracy* is checked, because a wrong one corrupts every share computed from it.

### Both fixes validated

A **cold agent** was then given only `/novel-revise 1-5` — no hint about dialogue, word counts, or
what had changed. Unprompted, it reported:

> "the dialogue share (2.4%-5.4%) and word counts (all within 60 words of the 1600 floor against a
> 2000-word target) fail systematically across all five chapters"

Both findings, measured rather than eyeballed, plus the systemic read. It then repaired them:

| ch | dialogue before | after | of the words added |
|---|---|---|---|
| 1 | 2% | **25%** | +530 dialogue, +83 narration |
| 2 | 3% | **25%** | +517 dialogue, +143 narration |
| 3 | 4% | **25%** | +489 dialogue, +120 narration |

~80% of the growth was dialogue: narrated beats converted into spoken ones, which is the repair
`dialogue-voice` asks for and not the padding `hook-and-pacing` forbids. It also re-measured the
stale `wordcount` frontmatter itself. **Before the fix these same chapters passed all ten passes
with the defects untouched.**

Chapters 4-5 were left unrevised — the fix was demonstrated and there was no reason to keep paying
to re-demonstrate it.

Caveat on the first attempt: it was killed by a session rate limit partway through chapter 1, and
that partial state (5% dialogue) briefly looked like an under-repair. It was not. A five-chapter
revision is large enough to hit a session limit; expect to resume.

## What worked

Worth recording, because it is the majority of the run:

- **The form ledger is excellent.** `state/body.md` was set up without being asked for — a
  reincarnator aged 4->12 triggered it automatically — and it produced the best writing in the
  book. A door the MC physically cannot open. A top shelf a dragged-over crate still doesn't
  reach. Feet not touching the floor. Chapters 1-5 hit a physical ceiling on purpose three times.
- **Canon handling was disciplined.** The agent found a wrong date in a web search result and
  rejected it by reasoning from internal consistency against a character's age, rather than
  trusting the source.
- **It caught a flaw in the author's own premise** — the requested 8-year runway was arithmetically
  incompatible with the MC being an age-mate of the canon cast — and proposed a fix.
- **Nobody exists to be corrected.** The supporting character with the *lowest* intel rating
  out-manoeuvres the tier-4 protagonist in chapter 3, winning on domain authority, and the MC
  concedes it on the page. That is `voice-separation`'s hardest rule, honoured without the file
  ever being loaded.
- **State discipline held.** 5/5 CCS blocks present and within cap, every one carrying `kno>`,
  `hook>` and `wld>`; no orphaned thread IDs; word counts in frontmatter matched reality exactly.
- **The interview was efficient** — one round, six batched questions, each led with a
  recommendation, against a documented budget of six rounds.

## Limitations

Read the numbers with these in mind:

1. **5 chapters, not 30.** Arc rollup (ch 25), long-run voice drift, and `timeline-engine` at
   scale are all untested.
2. **One run, one model, one genre.** No variance estimate. Fanfic is the heaviest configuration;
   original fantasy would load fewer skills and cost less.
3. **The two fixes are unvalidated.**
4. **One persistent session**, so the flat-cost claim could not be tested (above).
5. **21 skills never executed**, including all six untoggled optional ones.
6. `slice-of-life-texture` was enabled by the agent against the planned defaults, so this is not
   quite a clean default-configuration measurement.
7. Cache multipliers are the standard published ratios, not separately confirmed for this account.

## Reproduce it

Chapter QC (this ships with the repo):

```bash
python3 scripts/sw.py audit novels/<your-slug>
```

It measures the four channel shares, anchor vocabulary across the opening arc, `delivers:`
presence, wordcount accuracy, MTL banned phrases, narration exclamation marks, the default gesture
set, the cast tables, and CCS ledger integrity — the mechanical half of `revision-pass`, run
independently so the gate cannot mark its own homework. Length is reported and never scored.

**This benchmark's own novel is gone.** `novels/small-enough-to-miss` was never committed —
`.gitignore` excludes everything under `novels/` except the template — so the numbers above are
the only surviving artifact of run #1, and the audit command that used to be printed here could
not be run by anyone. What replaces it is the test suite, which plants findings 6, 10 and 12 into
a synthetic novel in a temp directory and asserts that the audit catches them:

```bash
python3 -m unittest discover tests
```

Counts in this document are as of run #1 (37 skills). The repo has grown since; `docs/upgrade-plan.md`
carries the current inventory.

> **Note, added after run #1.** This was originally `docs/check-chapters.sh`, a bash + awk + perl
> + python script. It has been replaced by `scripts/sw.py audit`, which is stdlib Python and runs
> on Windows without a POSIX shell. Three defects came over in the port: the shell version's
> ledger `wc:`-versus-body comparison never ran at all (a mangled parameter expansion made it
> match nothing, and it printed an empty section that read as a pass), its anchor matcher counted
> `the Leaf` by looking for a bare case-insensitive `leaf`, and it printed the `fk>` line count
> as neutral information rather than asserting it against the block count. On this novel that
> last one is a real finding: chapters 4 and 5 have no `fk>` line, and `mc.foreknowledge` is set.

Cost accounting: subagent usage is **not** in the main session transcript. It lives at
`~/.claude/projects/<escaped-cwd>/<session-id>/subagents/agent-<agentId>.jsonl`, one
`.message.usage` object per assistant row. Sum `input_tokens`, `cache_creation_input_tokens`,
`cache_read_input_tokens` and `output_tokens` separately — a single blended token number will
misprice the run by an order of magnitude, since cache reads and cache writes differ 12.5x.
