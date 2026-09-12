# scripts/ — the mechanical toolkit

A single stdlib-only Python program that does the countable work the skills would otherwise
spell out by hand: slicing the read-set, sweeping a chapter for banned strings and channel
mechanics, auditing the cast tables, checking the ledger against the chapters, and stamping a
measured word count.

**It is an optimisation and never a dependency.** Every skill that names a command here keeps
its manual checklist directly underneath it. If Python is not installed, nothing breaks — the
model does the same checks by reading, exactly as it did before.

```bash
python3 scripts/sw.py doctor          # environment + workspace check, start here
python3 scripts/sw.py --help          # every command
```

Requires **Python 3.8+**, standard library only. No install, no build step, no packages. On a
Windows box where `python3` is not on PATH, use `python scripts/sw.py …` — the program never
shells out, so it runs identically from bash, Git Bash, PowerShell or cmd.

## Commands

Every command takes a novel as a path or a slug (`novels/my-book`, `my-book`), or resolves it
automatically when only one novel exists.

| command | what it does | writes? |
|---|---|---|
| `readset <novel> -c N` | Assembles the bounded read-set for chapter N — the sliced rows, not the whole files, plus the active optional/genre modules and the file to open for each. Also carries the world clock — the recent `state/timeline.md` log rows and the live crises. Opens with a GATE section: any earlier chapter still at `status: drafted`, the WATCH row (checks that fired in 2+ of the last 5 chapters, warns ranked above habit notes, 4 at most), the recent `gate>` lines, and the last five `z4>` answers. `--chars`, `--locs`, `--society`, `--out` | only with `--out` |
| `lint <novel> [-c N \| --all]` | Sweeps one chapter, or every chapter with `--all`: MTL banned phrases, the AI-default cut list, narration exclamation marks, the four channels, the thought budget and its floor, apostrophe collisions, stray markup, frontmatter, anchor vocabulary, ledger agreement | no |
| `arc <novel> [-a N]` | The distributional pass over one arc: per-chapter words, dialogue share, anchor count and ledger presence; the dialogue trend; the length spread; hooks; cast rotation; thread operations; foreknowledge. Ends with the judged half it cannot do | no |
| `load <novel> -c N` | What the toolkit hands the drafter for one chapter: cards, words of procedure, checkboxes and negations, per phase, plus the corpus card budget and the word budget beside it | no |
| `cast <novel>` | Audits `_voices.md` and `_competence.md` as tables: the straddle rule, the wit cap, the three-way clash, the `eq` axis, turn and hand-habit collisions, the deep-expertise budget, missing rows and referrals | no |
| `curve <novel>` | The power curve: gain step size and cadence, the four requirements on every gain, unpaid boost debts, a second climax boost, pressure monotony, the trivial budget, the flat stretch, tier rising while pressure falls, and the `pwr>` line's agreement with `state/power.md`. No-ops when `scaling.shape` is `none` | no |
| `state <novel>` | Ledger against chapters, required CCS lines, block length, **block ordering**, thread tension against last use, plan-row completeness, the promotion trigger, book-digest staleness, and the section headings every read-set slices by — checked against this novel rather than the template | no |
| `status <novel>` | Progress aggregation for `/novel-status`, and a warning for any chapter the phase C gate never ran on | no |
| `stamp <novel> [-c N]` | Measures the body and writes `wordcount:`. `--status`, `--ledger` | **yes** |
| `newnovel <slug>` | Copies `novels/_template` to `novels/<slug>` | **yes** |
| `audit <novel>` | Inventory plus `lint --all`, `cast`, `state` and `curve` in one pass — the independent whole-novel gate | no |
| `history <novel>` | The whole book as a series rather than one chapter: per-chapter words, dialogue share, thought and meta counts, the dialogue and length trends, which checks recur across chapters and at what level, the `widening` section (Pass Z4's answers and the recorded candidates), thread ages, the pressure series, and cadence from file mtimes. `--json` | no |
| `trace [novel]` | What the run cost and **which skill files it actually opened**, from Claude Code's own transcripts: API responses, the four token classes, wall clock, cost, per-chapter attribution, tool counts. `--since`, `--until`, `--transcripts`, `--rates`, `--json` | no |
| `kb <action> [args]` | Queries the craft knowledge base, derived from skill and reference frontmatter on every call and never stored. `owner <slug>` names the skill that owns a concept; `show <slug>` adds what teaches it and who cites it; `list [--type T] [--json]` prints the whole index; `search <terms>` finds passages with their heading and owner, unranked; `cards <novel> -c N [--phase A]` and `passes <novel> -c N` resolve the card set for one chapter against `novel.md`; `validate` runs the structural checks `health` also runs | no |
| `export <novel> --okf` | Projects a novel into an OKF v0.2 bundle: one document per character, location, thread and chapter, plus the ledgers, an `index.md` carrying `okf_version` and a `log.md`. Knowledge *about* the novel, not the prose — every document carries a `resource:` naming the repo file it came from. `--out` must name a directory that does not yet exist | **yes**, into `--out` only |
| `health` | The toolkit's own wiring: skill frontmatter, uncited and dangling references, draft/audit cards against their dispatcher, `CLAUDE.md` section 3 against the directory listing, `optional:` toggles, orphan `novel.md` keys, every template accessor, documented commands against implemented ones, `.claude/commands/` against `CLAUDE.md` section 7, the **card and word budgets** on the unconditional card set, **every skill's `owns:` claim for completeness and exclusivity, any pair of skills carrying the same 10-word passage, and any skill discussing another's concept without naming its owner**, line-number citations | no |
| `selftest` | Builds a complete novel in a throwaway directory and runs every command against it — twice, once clean and once with named defects planted. No model, no network, a few seconds. `--keep` | temp dir only |
| `doctor` | Python version, repo root, novels found | no |

### Exit codes

| code | meaning |
|---|---|
| `0` | clean |
| `1` | findings that need a decision — not necessarily a broken file |
| `2` | bad usage, or a novel/chapter that does not exist |

Findings print one per line as `LEVEL path:line: [check] message`, at three levels: **DEFECT**
(a named gate failure), **warn** (look at it), **note** (`--show note` to see them, `-q` for
defects only).

**The note level is not "less important", it is "not judgeable in one chapter".** One antithesis
is good writing; one scene where nobody interrupts is a scene. Those checks are notes precisely
because any single instance is fine — and a *recurrence* is a drafting habit worth fixing in the
procedure. So the two commands that look across chapters, `history` and `readset`'s WATCH row,
count habit notes alongside warns, while nothing per-chapter is scored on them. Which notes count
as habits is an allowlist (`rules.HABIT_NOTE_CHECKS`); a note that merely reports what a chapter
*contains* rather than what it keeps doing wrong — `group-scene`, whose own message says to read
it and discount it — is excluded by name.

## The dialogue and cast sections

Added after benchmark run #2, where a novel that every command called clean was described by its
first human reader as having stiff dialogue and characters who were never introduced.

| section | command | what it shows |
|---|---|---|
| dialogue texture | `lint` | turn lengths and spread, contractions per 100 spoken words, fragment share, interruptions, exchange runs, narration between lines |
| debut ledger | `cast` | where each character first appears, words before they speak, the sentence they arrive in, and which name token matched |
| turn length | `cast` | each speaker's measured mean against the `turn` their own matrix row declares, with attribution coverage |
| `near-clash` | `cast` | two speakers alike on intel **and** articulacy, differing only in wit |
| `eq-*` | `cast` | the `eq` axis: a matrix with no values, nobody reading people better than the MC, a cast whose `eq` always equals `intel`, and two speakers sharing both. All warns; the only defect is a matrix that contradicts `mc.eq_tier` |
| `group-scene` | `lint` | which scenes have three or more cast members speaking, and who they are — a trigger surface for `scene-craft/references/group-scenes.md`, never a verdict |

**None of these is a gate.** They are notes and warns, and there is a test asserting the texture
findings can never be raised to a defect. This repo has twice built a number that decided whether
a chapter shipped — word count, then dialogue share — and both were optimised within five
chapters, the second by bolting a muttering habit onto a protagonist to clear a floor by 0.2
points. Read them to find where to look; fix what a reader would feel.

There is no companion check for a child's or an elderly character's register, and that is a
decision rather than a gap: detecting who is a child would mean guessing from a turn length or
adding an axis to the voice matrix, and `voice-separation/references/age-register.md` states that
age does not get an axis. A check that guesses is a number somebody writes toward.

Turn-length attribution is deliberately conservative: a line counts for a speaker only when
exactly one cast name appears in the narration around it. Coverage is printed with the table, so a
low number is visible rather than hidden.

## Scoping a run

`trace` with no window aggregates **every** session that ever ran in this repo, because that is
what matching on `cwd` means. On the machine that produced benchmark run #2 that was 22 sessions
and $225 of toolkit development, none of it the run being measured. Bound the window:

```bash
python3 scripts/sw.py trace --since 2026-09-09T12:40 --until 2026-09-09T14:00
```

Responses outside the window are reported as a `(before --since)` row rather than folded into
chapter 1. Without a window nothing is moved — the first chapter's bucket absorbs the setup that
preceded it, as documented, and the report says so.

**Per-chapter attribution anchors on each chapter file's last write.** That is right for a
revision and wrong for an end-of-run cleanup sweep: touching five chapters in the last twenty
seconds moves their real cost into whichever chapter was written before the sweep. `trace` warns
when a chapter's bucket holds under thirty seconds of work. When it does, trust the run total and
not the rows.

## Measuring a test run, end to end

The recipe benchmark run #2 used. It needs no scratch scripts and nothing machine-specific: every
identifier below is printed by the tools themselves.

**1. Note the time before you start.** `date -u +%Y-%m-%dT%H:%M`

**2. Take a baseline** of whatever you expect to move:

```bash
python3 scripts/sw.py lint  novels/<slug> --all --show note > before-lint.txt
python3 scripts/sw.py cast  novels/<slug> > before-cast.txt
```

**3. Run the agent.** Give it an authoring brief, not a benchmarking one — an agent told which
defects it is scored on will avoid them, and the skill-loading measurement becomes worthless.

**4. Find the run.** `python3 scripts/sw.py trace` lists every session it can see, with a
`transcript` column:

```
transcript                             kind        resp     rows      wall
<session>/agent-<agentId>              subagent      236     1068   51m 03s
```

**5. Scope to it.** Any fragment of that column works — the session id, the agent id, or the whole
path:

```bash
python3 scripts/sw.py trace novels/<slug> --session <agentId>
```

**Scoping is not optional.** With no window `trace` aggregates every session that ever ran in the
repo — on the machine that produced run #2, 22 sessions and $225 of unrelated toolkit development.
And `--since` alone is **not enough**: the session *driving* an agent runs in the same repo at the
same time, so its own file reads get counted as the agent's skill loads. That mistake was made
once during run #2 and is why `--session` exists. Use `--since`/`--until` to bound a period and
`--session` to isolate one agent.

**6. Take the after-measurements** and diff them against the baseline.

## What `trace` reads, and what it does not

`sw trace` is the only command that reads anything outside the repo. It opens the JSONL
transcripts Claude Code writes under `$CLAUDE_CONFIG_DIR` (or `~/.claude`), and it extracts
exactly these fields:

`type` · `timestamp` · `cwd` · `requestId` · `message.id` · `message.model` · `message.usage` ·
and the **names** and `file_path`s of tool calls.

It never reads prompt text, tool results, or assistant prose, and it never prints them. It writes
nothing anywhere. Transcripts are selected by comparing each row's `cwd` against this repo, so a
session for a different project is not opened for measurement — and the escaped project-directory
name is never reconstructed, because that escaping differs between Windows and POSIX.

**Cost is computed, never read.** The transcripts carry no price field, so `trace` prices tokens
from a small table of published rates in `swlib/rates.py` and prints that table underneath every
dollar figure it reports. `--rates <file>` replaces it. If your rates differ, every figure scales
linearly.

One accounting rule is load-bearing and is the reason this command exists: Claude Code writes
**one row per content block** of an API response and repeats the whole `usage` object on each of
them. Summing rows bills one request as many. `docs/benchmark.md` was measured that way and
overstated the run by 3.6x. `trace` groups rows into responses by `(requestId, message.id)`, takes
the input-side fields once per group, and takes `output_tokens` — a streaming counter whose last
row holds the total — as the group maximum. It prints the naive row-sum alongside the real one so
the difference stays visible instead of merely fixed.

## What these scripts deliberately do not do

- **They never edit a prose body.** `mtl-detox` says to rewrite the sentence rather than swap a
  synonym; an auto-fixer would do precisely the forbidden thing. Linters report, the model
  rewrites.
- **They do not run `bias-guard`.** It is the one skill `CLAUDE.md` calls non-negotiable, and it
  is purely distributional — a green line from a linter must never be readable as a bias pass.
  `cast` prints the competence distribution and then says so.
- **They do not judge delivery.** Pass 9 — want, friction, change, cost, next — is the gate a
  chapter actually passes, and no part of it is countable. `lint` reports word count as a fact
  and scores it on nothing except whether the recorded number is true.
- **A clean run is not a passed revision.** It means the mechanical passes found nothing. Passes
  2, 3, 5, 6, 8 and 9 still need their skill files open. `revision-pass` says which.
- **`trace` does not score a run.** There is no good number of skill loads and no target cost. Its
  one judgement is that a skill `CLAUDE.md` section 3 calls always-in-play, in a run that opened
  skills at all, should have been opened — and that is a warning, not a gate.
- **`history` does not score a chapter.** It prints word counts and dialogue shares as a series
  because the defects worth finding are distributional, and it repeats that length is scored on
  nothing, because that table is the one most likely to be read as a scoreboard.
- **`load` does not score a novel.** It measures the *instructions*, so its output does not move
  when the prose does, and no drafting decision may cite it. Its two enforced numbers — the card
  budget and the word budget — bind the corpus and are checked by `health`, never against a book.

## Tests

```bash
python3 -m unittest discover tests    # the suite (382)
python3 scripts/sw.py selftest        # the same thing end to end, through the real CLI
```

Stdlib `unittest`, no dependency to install, and no novel required: every fixture is built in a
temp directory from the real `novels/_template`, so a test fails when the template drifts away
from the parsers.

The suite exists because these measurements are trusted by a gate that cannot see the prose. A
parser that under-detects does not look like a broken parser — it looks like a clean chapter.
Each case in `tests/test_channels.py` names, in its docstring, the wrong behaviour it pins down:
multi-paragraph speech counted as narration, curly thought marks invisible, an unmatched quote
spanning a whole file, `'twas` reported as an unterminated thought.

`tests/test_load.py` and `tests/test_trace.py` cover the two commands that measure the
**toolkit** rather than a novel, and they were the last two with no tests at all — which was the
wrong way round. A defect in `trace`'s skill detection once made the headline number wrong for
three benchmark runs and nothing failed, because a broken measurement does not look broken, it
looks like a result. Both suites assert the standing contract as well as the behaviour: neither
command may raise above a warn, `load`'s output must not move when the prose does, and no `trace`
finding may name a chapter-quality check.

`tests/test_template_wiring.py` guards the seam the other modules cannot see. Every other test
supplies its own tables, so a parser can select on a column the **shipped template** does not have
and every test still passes while the check is dead against every real novel — which is exactly
what happened to `plan_rows()`, whose `delivers` column was missing from `plan/chapters.md` for the
life of the repo. It also fails on a `novel.md` key that no skill names and no script reads, the
defect `mc.starting_power` was.

## Layout

```
scripts/sw.py             dispatcher and argument parsing
scripts/swlib/mdio.py     frontmatter, minimal YAML, pipe tables, section slicing
scripts/swlib/novelio.py  the novel workspace: config, ledger blocks, cast tables, lexicon
scripts/swlib/textstats.py  chapter body: the four channels, paragraphs, sentences, offsets
scripts/swlib/rules.py    the searchable rule sets, each citing the skill it comes from
scripts/swlib/report.py   findings and rendering
scripts/swlib/cmd_*.py    one module per command
scripts/swlib/transcripts.py  Claude Code's own transcripts, read as measurements
scripts/swlib/rates.py    model prices, and the arithmetic over them
scripts/swlib/sample.py   the complete novel `selftest` builds, clean and seeded
scripts/swlib/__init__.py
tests/                    fixtures plus one module per surface
```

## Proving it works on a new machine

```bash
git clone <this repo> && cd skilled-writer
python3 scripts/sw.py selftest
```

`selftest` scaffolds a complete novel from the shipped `novels/_template` through the real
`newnovel`, fills it with a finished six-chapter sample, and runs `readset`, `lint --all`, `cast`,
`curve`, `state`, `status`, `arc`, `history`, `stamp`, `health` and `trace` against it. Every one
must find nothing.

Then it does it again with six defects planted — a banned MTL phrase, an exclamation mark in
narration, a wrong word count, a missing `fk>` line, a pressure value contradicting its own tiers,
and a cast with nobody below the MC — and **every one must be caught by the check that owns it**.
That half is the point. A selftest that only asserts "no defects found" passes exactly as happily
when every parser is dead, which is the failure this repo describes as *a parser that
under-detects does not look like a broken parser, it looks like a clean chapter.*

Exit 0 means the toolkit works here. `--keep <dir>` leaves the built novel behind to look at.
