# Test-run protocol

The rules that bind the **coordinator** during a benchmark run of this toolkit — the session the
user is talking to, not the agent that writes the novel. Read this in full before the run starts.

One sentence holds the rest up. **A test run measures the toolkit, so anything the coordinator
does by hand is a thing the toolkit did not have to do, and the run measures the coordinator
instead.** Run #3's numbers are worthless for exactly that reason: all five of its `gate>` lines
read *"full redraft per coordinator note"*. A human directed every repair, every chapter shipped,
and the run learned nothing about whether the corpus can produce a chapter.

This file lives in `docs/` on purpose. The writing agent is told not to read `docs/`, and that
instruction covers this file first: an agent that has read the protocol is an agent writing for the
measurement.

---

## 0. When this applies

**A test run** is one the user asks for as a test, trial, benchmark or evaluation. The deliverable
is a measurement; the novel is a by-product and is thrown away afterwards. Every rule below binds.

**A normal run** is one where the deliverable is the novel. **None of this applies.** The user is
the author, you are their assistant, and editing a chapter when they ask is the job.

If both readings are open, ask before writing anything. The question is cheap and the run is not.

## 1. The one thing that is flexible

**The novel** — genre, world, premise, MC, and anything else the user names in the opening prompt.
That is the variable. The protocol is not.

Three things are fixed in the other direction: they belong to the **agent**, and the coordinator
never supplies them, because they are what the run is measuring.

| the agent invents | the coordinator supplies |
|---|---|
| every name — characters, places, factions, the title, and therefore the slug. In the role pipeline that means the **architect runs the interview and `title-craft`** and returns each round as numbered questions (`/novel-new`); the coordinator never proposes a name | the one-line seed, in the user's genre |
| the power system, the ladder, the cast, the arc plan, the chapter list | interview answers that are author taste: tone (**both** Round D answers — `tone.register` and `tone.warmth`, which are recorded and which the run must state), cadence, rating, the ending contract, the non-negotiables |
| every craft decision inside a chapter | approval of the Phase A brief |

Parameters the user did not name and the agent should not invent — harness shape, model, proxy
state, optional toggles — are **declared variables**: you choose each one before the run, write it
and its reason into the configuration table, and never change it mid-run. If the user says nothing,
the default is *held constant with the previous run*, so the new genre is the only thing that moved.
A parameter chosen mid-run is a confound with no baseline.

## 2. You never touch the novel

**No file under `novels/` is ever written by the coordinator.** Not a chapter, not a bible file,
not a state file, not a plan row, not one character of YAML frontmatter.

| forbidden on any path under `novels/` | allowed, and expected |
|---|---|
| `Edit`, `Write`, `NotebookEdit` | `Read`, `cat`, `sed -n`, `grep`, `wc`, `diff` |
| `sed -i`, `tee`, `>`, `>>`, `cp`/`mv`/`rm` into it, a `python3 -c` that opens a file for writing | every `sw` command that only prints: `readset` `lint` `audit` `history` `state` `cast` `curve` `arc` `status` `load` `trace` `kb` `health` `selftest` `doctor` |
| `sw stamp`, `sw newnovel` — they write, so the agent runs them | copying *out* of `novels/` into the scratchpad, which is how anything survives |

### Arm the guard: `touch .test-run`

Since 2026-09-19 this rule has a mechanism, and it is opt-in by design. `scripts/hooks/write_scope.py`
runs before every `Write`, `Edit` and `NotebookEdit` in the session and in every subagent, and it
refuses a path under `novels/` from the **coordinator** — the call with no `agent_id` — whenever a
`.test-run` file exists at the project root. Subagent writes are unaffected: each role is held to
its own column of the §10 table instead.

```bash
touch .test-run       # first thing, before §5's pre-flight
rm .test-run          # after the write-up, not before
```

Do it first, and record in the defect log that you did. **An unarmed run is not a failed run, but
it is a weaker one** — the number it reports rests on the coordinator having remembered, which is
precisely the thing the rule exists because nobody does. If you find the marker missing partway
through, create it, say when, and treat everything before that point as resting on goodwill.

The guard fails open on anything it cannot parse, so it will never be the reason a run stalls. It
also cannot see a shell redirect: `sed -i`, `tee` and `>` go through `Bash`, not `Write`, and the
table above is still the binding rule. The hook narrows the gap; it does not close it.

**The moment the rule exists for** is not the moment you feel like rewriting a paragraph. It is the
moment the run breaks, the fix is one line of YAML, and a repair by hand is faster than another
agent round-trip. That is the expensive moment, and the correct move is the slow one.

**A broken file under `novels/` is a finding, not a chore.** It means a skill did not handle
something a skill is supposed to handle. Fixing it yourself deletes the finding and leaves the
skill broken for the next run.

**If the agent's session dies, you do not finish its work.** Start a new agent, hand it the state,
and tell it to handle the interrupted chapter *the way the skill says to handle an interrupted
chapter* — without saying what the skill says. If the corpus cannot win that on its own, that is
the thing worth knowing.

**If you edit a novel file anyway** — by accident, or because the run genuinely cannot continue —
log the edit verbatim in the defect log, mark that chapter and every chapter after it **assisted**,
and say so in the write-up. An unlogged hand-edit is the one failure that silently invalidates
every number on the page.

### The toolkit is frozen for the duration

The other half of the same rule. During the run you do not fix `scripts/`, `.claude/` or the
template, and neither does the agent. A toolkit that changes mid-run makes the chapters
incomparable with each other, and the run loses its own control.

Fixing comes after the run stops (§9). If a bug blocks the run outright, fix it, record the commit
and which two chapters it landed between, and treat the chapters either side as **separate
samples** that are never pooled.

## 3. Intervention policy

This is the methodology, not a detail.

- **Approve each Phase A brief as written**, unless it breaks the contract outright — a hard rule
  in `CLAUDE.md` §4, not a disagreement of taste. Thirteen lines you would have written differently
  is not a contract break.
- **Interview answers are author taste, freely given.** Hold a written answer sheet *before* the
  run so your answers do not drift across six rounds of questions.
- **Craft direction mid-draft is not.** No beat, no structure, no fix, no line, no "try X here".
- **State restoration is still an intervention.** *"Re-gate rather than redraft"* is an instruction.
  Log it, mark the chapter assisted, and flag it wherever its numbers appear.
- **Praise the technique, never quote the line back.** Quoting the drafter's own sentences as
  praise feeds them straight into the next chapter. Run #5's agent caught this before the
  coordinator did.
- **Hand back the questions the agent owns.** *"That is yours to invent"* is a complete answer.
- **Log every exchange verbatim, both directions.** Your `SendMessage` text is part of the
  measurement.
- **Report assisted and unassisted chapters separately.** Never as one average.

## 4. What the agent is told

- **A pure authoring brief, with no mention that it is being measured.** A drafter that knows it is
  being scored optimises for the score.
- **Told not to read `docs/`** — this file and `benchmark.md` above all, which names the exact
  defects the run exists to observe.
- **It runs every command and writes every file.** Say so explicitly in the brief.
- **It cannot reach the user interactively**, so its brief says to end its turn with numbered
  questions; answer with `SendMessage`, which keeps the whole run in one session.
- Hold the harness shape constant with whichever run you intend to compare against, and name it in
  the configuration table. **Run #6 cannot**: it is the first run through the role pipeline, and
  that change is the declared variable its write-up leads with.

### The harness shape, since run #6

Runs #1–#5 drove one warm general agent through init and every chapter. The role pipeline is four
agents under one coordinator, and `/novel-write` is the loop:

| step | who | what reaches the coordinator |
|---|---|---|
| init | `architect`, spawned with the seed | interview rounds as numbered questions; answer each from the answer sheet with `SendMessage` |
| Phase A | `drafter`, description `draft ch N` | `BRIEF READY` and the brief — approve it as written (§3) |
| Phase B | the same drafter, resumed | `READY FOR GATE` |
| Phase C | `gate`, description `gate ch N`, **foreground** | the hand-back — relay it to the drafter **verbatim**, never summarised |
| step 5 | the same drafter, resumed | the eight-line report, `Bible:` line included |
| fold | `architect`, description `fold ch N` — only when `Bible:` is not `none` | what it folded, and what it declined |
| review | `reader`, after the run stops (§8) | the verdict |

- **The descriptions are part of the measurement.** `sw trace` bills each subagent to the chapter
  its description names; an agent spawned as "continue" is billed by write times, and a gate that
  edits nothing then vanishes from its chapter.
- **One fresh drafter per chapter is the default — the cold harness.** Continuing one drafter across
  chapters with `SendMessage` is the warm one. Declare which, per chapter, in the configuration
  table; the benchmark queue asks for one deliberate warm pair against a cold one, same day.
- **Every relay is an intervention you do not make.** You pass the brief's approval, the gate's
  hand-back and the `Bible:` line along unchanged. A paraphrased hand-back is craft direction.

## 5. Before the run

### Start a fresh session — and verify, because a fresh session is not proof

**Whether an edit to an agent file takes effect mid-session is not predictable.** `.claude/agents/*.md`
— an agent's `tools`, its `skills`, its `omitClaudeMd` flag and its whole prompt body — is
resolved by the harness on its own schedule, and the same question has now gone **both ways**: on
2026-09-20 a drafter spawned after an edit carried the *old* body; on 2026-09-22 one spawned
minutes after an edit carried the *new* one. Neither errored, and both spawns succeeded, so a
stale definition is indistinguishable from a current one by looking.

`.claude/settings.json` is the reliable half: a hook registered there has been picked up
mid-session every time it has been tried. So a run can sit on a new guard and an old agent at once
and look entirely normal.

**So: make every toolkit change, start a new session, and then confirm by asking.** A fresh
session removes the uncertainty about *which* version is loaded; it does not by itself tell you,
and nothing on disk does either. The inventory below is the only instrument. If an agent file
changed at any point during the run, the run is over — finish it, write it up, and note that the
change landed mid-run.

### Pre-flight

```bash
git rev-parse --short HEAD                       # record the SHA
date -u +%FT%TZ                                  # record the UTC start
python3 -m unittest discover tests               # must be green before anything starts
python3 scripts/sw.py health
python3 scripts/sw.py selftest
touch .test-run                                  # arms the coordinator write guard (§2)
```

- **A run against a broken toolkit measures nothing.** All three must pass first.
- **Capture the baseline** — the `sw audit` / per-chapter lint column as it stands today, before
  any toolkit change. Diffing against it afterwards is what proves a cross-chapter fix did not leak
  into per-chapter scoring.
- **Record the proxy state, the model, and the harness shape** in the configuration table. No
  proxy has sat in front of the harness since 2026-09-20; if one is put back, every token and cost
  figure it touches is confounded, and that has to be written down, not remembered.
- **Declare the stop condition in advance** — N chapters — and write it into the log.
- **`novels/` is gitignored and there is no undo.** Anything you want to survive the run goes to
  the scratchpad *and* into the write-up.

### Ask the first agent what it was handed

Before the first chapter, spawn the `drafter` **and the `gate`** — and the `architect`, if it has not
run the interview yet — each on a throwaway question: *list the numbered sections of any operating
contract you were given, and say whether you received a memory index*. Record each answer in the
configuration table. It costs one cheap turn and it is the only way
to see three things that are invisible to every check in this repo:

| what you are looking for | what it means |
|---|---|
| §7, §8 or §10 present | `omitClaudeMd: true` did not take effect, or the agent definition is stale. The drafter is carrying the coordinator's and the maintainer's rules |
| the contract missing entirely | the rendered block is absent or the flag is set without it. **Stop** — a drafter with no contract is not a run |
| a memory index present | the auto-memory hooks are in the drafter's context. Check what they say before continuing; an index line naming past run outcomes is a drafter told what to avoid |

**No script can do this.** `sw health` verifies the block is in the file and that the flag is
declared; whether either reaches a running agent is a fact about the harness, and asking is the
only instrument.

## 6. During the run

- **Log the Phase A brief.** Since 2026-09-19 the agent writes the approved brief to
  `state/brief.md`, but that file holds one brief and the next chapter overwrites it — so the
  *series* of them still exists nowhere but your log, and whether the agent writes the file at all
  is one of the things run #6 is measuring. Run #5's chapter 4 carries `cand> unrecorded` because
  the session holding its brief died.
- **Log every hand-off** — brief, approval, `READY FOR GATE`, the gate's hand-back, the `Bible:`
  line, the fold's answer — verbatim, both directions.
- **Log every interruption**: timestamp, which phase it landed in, and what the agent did on
  resume. Run #5's headline finding came entirely out of these rows.
- **At each chapter boundary, append the trace** —
  `sw trace novels/<slug> --session <this session's id> --role drafter,gate,architect` — to the
  findings file: cost and cards by role, per chapter, and any `trace-routing` finding, which is the
  only place a `cat` of another role's card shows up.

### Interrupting on purpose

Run #5's headline — the contract is lost at an interruption, not with session age — rests on two
accidental interruptions against two clean chapters. Repeat it deliberately, once:

1. Choose the chapter and the phase **before the run starts**, and write both into the log.
   Mid-Phase C is the case the queue names.
2. When the phase begins, stop that agent (`TaskStop`). Log the timestamp and the last thing it did.
3. Spawn a fresh drafter with the chapter's usual prompt and description. Say nothing about what
   happened beyond "the previous session stopped" — its read-set's RESUME line is the mechanism
   under test, and telling it where to resume measures you.
4. Record: whether it acted on the RESUME line, the phase it resumed at, whether it re-opened the
   cards the phase names (`sw trace --role`), and whether the chapter's `cand>`/`gav>` still came
   from `state/brief.md`.
- **Write every finding down the moment you see it** — see below. This is the rule that decides
  whether the run produced anything.
- **Verify every claim against disk.** The agent's step reports paraphrase file contents — five
  separate times in run #5, including a reworded `ending.contract`. **Report ≠ disk.**
- **Do not steer.** A finding prevented is a finding not collected. If you can see the chapter
  heading for a defect, let it arrive and write it down.

### Write every finding down in the turn you see it

**A finding that exists only in the conversation is a finding you are about to lose.** A test run is
long by construction — several chapters, several sessions, an interruption or three — and a long run
gets compacted. Compaction keeps the narrative and drops the particulars, and in a benchmark the
particulars *are* the finding: the exact line a check printed, the file and line it named, which
phase the interruption landed in, the number before and the number after. Reconstructing those from
a transcript is expensive when it works and impossible once the transcript has rotated.

This is the one failure that runs straight against the point of the exercise. The run exists to
improve the toolkit. A defect that was observed and then lost improved nothing, and cost a chapter
of budget to produce.

- **Write it in the same turn you see it, before doing anything else.** Not at the chapter boundary,
  not once you have confirmed it — an unconfirmed observation is written down *as* unconfirmed.
- **Two files, and both matter.** The working log is a findings file in the scratchpad, appended to
  all run long. The durable record is `docs/benchmark.md` in the repo, which survives `/tmp`
  cleanup, session death and compaction alike. **Flush the scratchpad into the repo at every chapter
  boundary.** Run #5 lost its findings file to `/tmp` cleanup mid-run and had to rebuild it from the
  session transcript; chapter 4's `cand>` line reads `unrecorded` because the session holding it
  died first. Both were avoidable by one append.
- **Improvement ideas count, not only defects.** *This could be clearer*, *this cap may be a wall*,
  *nothing measures this* — watch items are the cheapest thing to lose and the hardest to recover,
  because unlike a defect they leave no artifact on disk to be rediscovered from.
- **Verbatim, never paraphrased.** Each entry carries the command that produced it and its exact
  output line, plus `file:line` where there is one. A paraphrase cannot be re-verified once the
  novel is deleted, and `novels/` is gitignored.
- **An entry is six fields and thirty seconds**: id · severity · one-line claim · evidence verbatim ·
  what you expected instead · status. That is the whole cost, against reconstructing it later or
  losing it outright.
- **Assume every turn is the last one before a compaction.** You get no warning you can plan around.

## 7. Stopping

Stop at the declared chapter count, or when the measurement is complete — whichever comes first.
Do not extend a run to make a number look better.

**If the run is finished later**, after fixes have shipped or in a new session, those chapters are
a **second sample**, not more of the first. Report them in their own section, say which variables
moved, and pool nothing: no cost figure, no cards-opened count, no "n of N chapters" ratio may span
the two halves.

## 8. Then read the chapters yourself

**This is not optional.** Every decisive finding in runs #1–#5 came from a human reading the
output, including every one that no script could see.

- Read the **files**, not the step reports.
- **A clean run is not a passed revision.** Run #5's chapter 5 lints 0/0/0 and carries two defects
  a reader meets on the page: a beat left stacked on its own replacement, and a detail that
  contradicts its own relative clause.
- **Record what worked, with the same weight as what broke.** The defect log runs defect-heavy by
  construction, and a run with no positive controls cannot tell a working mechanism from an
  unexercised one.

**The procedure for this step is [`roles/review/reader-review.md`](../roles/review/reader-review.md).** Follow it rather than
reading however you happen to read: it fixes the order (blind pass, then reconcile against
`bible/` and `state/`), the output shape, and the 0–5 scale, which is what makes one run's read
comparable with the next one's.

**That file is yours, not the reader's.** It names what the exercise is for — numbered runs, this
protocol, routing findings to owners — so a reader that has read it knows the chapters are being
measured. What the reader gets is
[`roles/review/reader-brief.md`](../roles/review/reader-brief.md): the same questions and the same
scale with the framing removed. `reader_guard.py` allows the brief by name and refuses the rest of
that directory, so this is a file boundary rather than a thing to remember.

**Run the blind pass with the `reader` agent.** `.claude/agents/reader.md` does the read and the
verdict, and it is the only reader in the table whose blindness is enforced rather than promised:
no `Skill` tool, `omitClaudeMd: true` — which keeps out the auto-memory index as well as
`CLAUDE.md`, measured — and a `PreToolUse` hook that allows `chapters/` and
[`roles/review/reader-brief.md`](../roles/review/reader-brief.md) and refuses everything else,
**this file and the worked example included**. **You do §2, §4 and §5 yourself**, with its
findings in hand; those need `bible/` and `sw kb owner`, and a reader that opens either has
stopped being one.

**Then ask it what it was handed, in a separate turn after the verdict is written.** Not before:
the question names the fact that its context is under examination, which is itself a hint. Record
the answer beside the verdict. Two contaminants are known and unfixable — the harness supplies a
git-status snapshot of the parent session, so the reader can see it is in a toolkit repository,
and the spawn prompt must name the brief — and a third would be new information. A cold read whose
contamination is written down is worth more than one assumed to be clean, which is the same
argument §5's divergence check makes about the in-run impression.

A note worth keeping, because it was nearly missed: before `omitClaudeMd`, *any* agent spawned to
do this step inherited the whole operating contract and arrived knowing `event:`, Pass Z and the
ten bans. It would have read as a reader and graded as the toolkit.

The instruction has been here since run #1 and the procedure has not, which is why §8 has been the
most valuable step in this protocol and the least reproducible. A cold read of run #5 returned
**3 / 5** on plot-starvation and register monotony against **0 defects** from `sw audit` and an
in-run impression of *"the prose is good and the dialogue is the best any run has produced"*
(`benchmark.md`, *What the chapters look like*). Three instruments, three answers, and nothing in
the toolkit noticing they disagreed. §5 of the review procedure is about that disagreement.

### The measurement commands

```bash
python3 scripts/sw.py audit   novels/<slug> --show note
python3 scripts/sw.py history novels/<slug>
python3 scripts/sw.py state   novels/<slug>
python3 scripts/sw.py arc     novels/<slug> -a 1
python3 scripts/sw.py cast    novels/<slug>
python3 scripts/sw.py curve   novels/<slug>
python3 scripts/sw.py load    novels/<slug> -c <N>
python3 scripts/sw.py trace   novels/<slug> --session <coordinator-session-id>   # by role, per chapter, routing
python3 scripts/sw.py readset novels/<slug> -c <N+1>          # inspect the GATE/WATCH row
python3 scripts/sw.py readset novels/<slug> -c <N> --role gate   # confirm the gate's slice has no brief
grep -n 'cand>\|z4>\|gav>\|pwr>' novels/<slug>/state/continuity.md
```

### Traps that have cost a run before

| trap | what to do |
|---|---|
| **`sw trace` unscoped aggregates every session ever run in this repo** — and a time window is not enough, because the driving session runs in the same repo at the same time | always `--session`: the coordinator's session id takes in every agent it spawned; `--role drafter,gate,architect` then leaves the coordinator's own reads out |
| **`audit --show note` prints six findings per check**, then "... N more" | read the counts, not the visible rows, and `sw history` for the per-check series |
| Cards used to need counting by hand | `sw trace` reports them since 2026-09-19 — a `cards` column per chapter, a `-- cards` section per card. A Phase A card opened for chapter N+1 before N's file is finished lands in N's row, so read a boundary-straddling pair as one figure |
| **Subagent usage is not in the parent transcript** | read the per-agent transcript file |
| **The toolkit changes under the novels** | compare against the re-linted column, never against run-time numbers |
| **A phrase grep over this repo lies** — 80-column wrapping breaks clauses across lines | `tr '\n' ' '` first, or grep a two-word window |
| **A compressing proxy mangles Bash output** and leaves no mark — none since 2026-09-20, so check rather than assume | pull anything you need verbatim with `Read`, not `cat` |
| **zsh does not word-split unquoted variable expansions** | one `sw` invocation per command; never a loop over a string of arguments |

## 9. Fixing, after the run has stopped

The repairs cannot be designed in advance — that is what the run is for. What binds them:

- **One concept, one owner.** A fix goes in the skill whose `metadata.owns:` claims the slug
  (`sw kb owner <slug>`); every other skill cites it. `sw health` enforces this.
- **Never add a numeric ship gate.** Word count (#1), dialogue share (#2) and `SPEECH_TARGET_LOW`
  (#5) were each optimised rather than satisfied. **The severity tier is the incentive** — a warn is
  a gate whatever the doctrine says.
- **A script may find; it may not judge or rewrite prose.**
- **Card budgets bind the corpus.** `CARD_BUDGET` does not move. Past `CARD_WORD_BUDGET` an
  addition is paid for with a cut, or the ceiling is raised deliberately with the reason written
  beside it.
- **Length on a worked example is cheap; another prohibition is dear** (`CLAUDE.md` §8).
- **Nothing from this run's novel enters the corpus.** No character name, place, faction or piece of
  genre vocabulary reaches `.claude/**`, `novels/_template/**`, or any string a script prints. Run
  #5's O1 is what happens when it does: the corpus had one house cast and the drafter reused it.
- **Attribute pre-existing issues as pre-existing.** An issue known before the run started is not a
  run finding.

Then verify:

```bash
python3 -m unittest discover tests     # plus a new test for each testable fix
python3 scripts/sw.py health           # 0 defects
python3 scripts/sw.py selftest
python3 scripts/sw.py audit novels/<slug> --show note   # diff against the baseline
```

Per-chapter defect and warning counts should move **only where a fix intended them to**. Holding
them byte-identical across a cross-chapter change is the invariant this repo keeps, after twice
building a number that decided whether a chapter shipped.

## 10. The write-up

A run section in [`benchmark.md`](benchmark.md), carrying:

- the configuration table, with every declared variable and its reason;
- the TL;DR, cost buckets and cards-opened figures, each marked with its confounds;
- the pre-registered checklist, each item **works · fails · cannot be evaluated** — and *cannot be
  evaluated* is a worse state than *fails*, because it looks like a pass;
- the defect log, with severities, status, and positive controls logged with equal weight;
- **what reading the chapters found, in its own section**, separate from what the scripts found;
- assisted and unassisted chapters reported separately, with every intervention quoted;
- limitations, including sample size, and every variable that moved at once.

Nothing is committed unless the user asks.

## 11. The checklist

```
before    [ ] test run or normal run — established
          [ ] **fresh session** — no agent file edited since it started (§5)
          [ ] configuration table written, every declared variable has a reason
          [ ] tests + health + selftest green; SHA, UTC start, proxy state recorded
          [ ] baseline audit/lint column captured
          [ ] stop condition declared
          [ ] answer sheet written for the interview
          [ ] `.test-run` created — the write guard is armed, not merely intended
          [ ] drafter and gate asked what they were handed; contract present, §7/§8/§10 absent (§5)
          [ ] harness declared: cold or warm per chapter; the interruption's chapter and phase chosen
during    [ ] agent brief: authoring only, no mention of measurement, do not read docs/
          [ ] no coordinator write under novels/ — not once
          [ ] toolkit frozen
          [ ] every finding + improvement idea written to disk in the turn it was seen
          [ ] scratchpad findings flushed into docs/benchmark.md at each chapter boundary
          [ ] every Phase A brief logged; every intervention logged verbatim
          [ ] every interruption logged with phase and timestamp
          [ ] every hand-off relayed verbatim and logged; trace appended at each chapter boundary
          [ ] claims verified against disk, not against the agent's report
after     [ ] stopped at the declared count
          [ ] measurement commands run, trace scoped with --session, per role
          [ ] every chapter read by a human, per roles/review/reader-review.md
          [ ] reader given roles/review/reader-brief.md — never this file, never the example
          [ ] reader asked what it was handed, and the answer recorded as a contaminant
          [ ] reader review: verdict, ranked findings, unowned findings, divergence
          [ ] fixes designed only now; one owner each; no numeric ship gate
          [ ] tests + health + selftest green again; audit diffed against the baseline
          [ ] write-up in benchmark.md; halves of a split run never pooled
          [ ] nothing committed unless asked
```
