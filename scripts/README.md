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
| `readset <novel> -c N` | Assembles the bounded read-set for chapter N — the sliced rows, not the whole files, plus the active optional/genre modules and the file to open for each. `--chars`, `--locs`, `--society`, `--out` | only with `--out` |
| `lint <novel> [-c N \| --all]` | Sweeps one chapter, or every chapter with `--all`: MTL banned phrases, the AI-default cut list, narration exclamation marks, the four channels, thought budget, apostrophe collisions, stray markup, frontmatter, anchor vocabulary, ledger agreement | no |
| `arc <novel> [-a N]` | The distributional pass over one arc: per-chapter words, dialogue share, anchor count and ledger presence; the dialogue trend; the length spread; hooks; cast rotation; thread operations; foreknowledge. Ends with the judged half it cannot do | no |
| `cast <novel>` | Audits `_voices.md` and `_competence.md` as tables: the straddle rule, the wit cap, the three-way clash, turn and hand-habit collisions, the deep-expertise budget, missing rows and referrals | no |
| `curve <novel>` | The power curve: gain step size and cadence, the four requirements on every gain, unpaid boost debts, a second climax boost, pressure monotony, the trivial budget, the flat stretch, tier rising while pressure falls, and the `pwr>` line's agreement with `state/power.md`. No-ops when `scaling.shape` is `none` | no |
| `state <novel>` | Ledger against chapters, required CCS lines, block length, thread tension against last use, plan-row completeness, the promotion trigger, book-digest staleness | no |
| `status <novel>` | Progress aggregation for `/novel-status` | no |
| `stamp <novel> [-c N]` | Measures the body and writes `wordcount:`. `--status`, `--ledger` | **yes** |
| `newnovel <slug>` | Copies `novels/_template` to `novels/<slug>` | **yes** |
| `audit <novel>` | Inventory plus `lint --all`, `cast`, `state` and `curve` in one pass — the independent whole-novel gate | no |
| `history <novel>` | The whole book as a series rather than one chapter: per-chapter words, dialogue share, thought and meta counts, the dialogue and length trends, which lint checks recur across chapters, thread ages, the pressure series, and cadence from file mtimes. `--json` | no |
| `trace [novel]` | What the run cost and **which skill files it actually opened**, from Claude Code's own transcripts: API responses, the four token classes, wall clock, cost, per-chapter attribution, tool counts. `--since`, `--until`, `--transcripts`, `--rates`, `--json` | no |
| `health` | The toolkit's own wiring: skill frontmatter, uncited and dangling references, draft/audit cards against their dispatcher, `CLAUDE.md` section 3 against the directory listing, `optional:` toggles, orphan `novel.md` keys, every template accessor, documented commands against implemented ones, line-number citations | no |
| `selftest` | Builds a complete novel in a throwaway directory and runs every command against it — twice, once clean and once with named defects planted. No model, no network, a few seconds. `--keep` | temp dir only |
| `doctor` | Python version, repo root, novels found | no |

### Exit codes

| code | meaning |
|---|---|
| `0` | clean |
| `1` | findings that need a decision — not necessarily a broken file |
| `2` | bad usage, or a novel/chapter that does not exist |

Findings print one per line as `LEVEL path:line: [check] message`, at three levels: **DEFECT**
(a named gate failure), **warn** (look at it), **note** (informational; `--show note` to see
them, `-q` for defects only).

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

## Tests

```bash
python3 -m unittest discover tests    # the suite
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
