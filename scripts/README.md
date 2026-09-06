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
| `readset <novel> -c N` | Assembles the bounded read-set for chapter N — the sliced rows, not the whole files. `--chars`, `--locs`, `--society`, `--out` | only with `--out` |
| `lint <novel> [-c N \| --all]` | Sweeps one chapter, or every chapter with `--all`: MTL banned phrases, the AI-default cut list, narration exclamation marks, the four channels, thought budget, apostrophe collisions, stray markup, frontmatter, anchor vocabulary, ledger agreement | no |
| `arc <novel> [-a N]` | The distributional pass over one arc: per-chapter words, dialogue share, anchor count and ledger presence; the dialogue trend; the length spread; hooks; cast rotation; thread operations; foreknowledge. Ends with the judged half it cannot do | no |
| `cast <novel>` | Audits `_voices.md` and `_competence.md` as tables: the straddle rule, the wit cap, the three-way clash, turn and hand-habit collisions, the deep-expertise budget, missing rows and referrals | no |
| `state <novel>` | Ledger against chapters, required CCS lines, block length, thread tension against last use, plan-row completeness, the promotion trigger, book-digest staleness | no |
| `status <novel>` | Progress aggregation for `/novel-status` | no |
| `stamp <novel> [-c N]` | Measures the body and writes `wordcount:`. `--status`, `--ledger` | **yes** |
| `newnovel <slug>` | Copies `novels/_template` to `novels/<slug>` | **yes** |
| `audit <novel>` | Inventory plus `lint --all`, `cast` and `state` in one pass — the independent whole-novel gate | no |
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

## Tests

```bash
python3 -m unittest discover tests
```

Stdlib `unittest`, no dependency to install, and no novel required: every fixture is built in a
temp directory from the real `novels/_template`, so a test fails when the template drifts away
from the parsers.

The suite exists because these measurements are trusted by a gate that cannot see the prose. A
parser that under-detects does not look like a broken parser — it looks like a clean chapter.
Each case in `tests/test_channels.py` names, in its docstring, the wrong behaviour it pins down:
multi-paragraph speech counted as narration, curly thought marks invisible, an unmatched quote
spanning a whole file, `'twas` reported as an unterminated thought.

## Layout

```
scripts/sw.py             dispatcher and argument parsing
scripts/swlib/mdio.py     frontmatter, minimal YAML, pipe tables, section slicing
scripts/swlib/novelio.py  the novel workspace: config, ledger blocks, cast tables, lexicon
scripts/swlib/textstats.py  chapter body: the four channels, paragraphs, sentences, offsets
scripts/swlib/rules.py    the searchable rule sets, each citing the skill it comes from
scripts/swlib/report.py   findings and rendering
scripts/swlib/cmd_*.py    one module per command
scripts/swlib/__init__.py
tests/                    fixtures plus one module per surface
```
