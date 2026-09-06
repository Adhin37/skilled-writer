# Upgrade plan

Written 2026-09-06, after the 2026-09-06 rewrite and before any of the work below is done. It is
the execution plan for the next working session, not a record of one.

It was produced by two passes: a survey of external craft and agent-engineering research, and a
full inventory of this repo — every `SKILL.md` measured, every `sw.py` command audited, every
cross-reference resolved. Every defect in §3 is cited to a file and line, and the five load-bearing
parser defects were re-executed against `swlib` rather than taken on report.

---

## 1. TL;DR

| # | workstream | what it changes | why it is here |
|---|---|---|---|
| **W0** | Hygiene | 12 concrete inconsistencies across skills, commands and docs | The tree contradicts itself in ways that cost a model turns |
| **W1** | Trustworthy gate | `swlib` parser correctness + the repo's first `tests/` | Dialogue share — the metric that caught the flagship defect — is wrong on a standard English convention |
| **W2** | Context economy | All 40 skills split into body + `references/`; `CLAUDE.md` diet; `sw.py brief` | The contract costs ~30k tokens of instruction per chapter. The model rationed and skipped four "never optional" skills |
| **W3** | Craft features | Controlling idea · microtension + subtext · arc payoff · listing kit | Four gaps confirmed absent by grep, each matching a measured defect of AI fiction or of web serials |
| **W4** | Arc-level gate | An arc-boundary pass, countable half in `sw.py arc` | Every failure in this format is distributional, and `revision-pass` only ever sees one chapter |

**The single biggest number in this document:** following the operating contract literally costs
**~30,200 tokens** of skill text per chapter before a word of story state is read. That is the
cause of benchmark finding 9, and W2 is the fix.

**The single most dangerous number:** on prose using the standard multi-paragraph speech
convention, the linter under-reports dialogue share. On the sample now committed as a test
fixture it read **72.1%** against a true **86.9%**, and the size of the error grows with how much
of the speech sits in the middle paragraphs. Dialogue share is the metric that caught run #1's
flagship defect.

---

## 2. Where the toolkit stands

Measured, not estimated. Token figures are `wc -w × 4/3`, the same method before and after, so
the W2 targets are pass/fail against them.

| measure | value |
|---|---|
| Skills | 40 (`SKILL.md` only — **zero** supporting files anywhere) |
| Skill corpus | 7,353 lines · ~72,300 words · **~96,400 tokens** |
| The 29 "always in play" skills | ~62,700 words · **~83,600 tokens** |
| Per-chapter minimum — `write-chapter` + `revision-pass` + `continuity-summary` + the five must-open sources | **~30,200 tokens** |
| `CLAUDE.md`, loaded every session | 3,576 words · **~4,800 tokens** |
| Toolchain | `scripts/sw.py` 256 lines dispatching `scripts/swlib/` — 12 modules, 2,157 lines |
| Tests, CI, packaging | **none** — an exhaustive search returns zero |
| Benchmark run #1 | 5 chapters · $28.39 · 16 of 37 skills ever loaded |

Three items remain open from run #1 and are folded into the workstreams below: finding 9's fix has
never been validated, the flat-cost claim has never been tested cold, and the removed word-count
gate must never return in any form.

---

## 3. What the survey found

### 3.1 The mechanical gate mis-measures

`scripts/swlib/textstats.py` defines the four channel regexes at `:16-24` and everything downstream
trusts them. Five of these were re-executed against the live module during the survey; the results
below are observed, not inferred.

| # | defect | site | observed effect |
|---|---|---|---|
| 1 | Curly `‘…’` thought marks are invisible | `textstats.py:18-23` | Straight marks score 1 hit, curly score **0**. The 1–3 thought budget silently never trips and `lint` reports `thought 0/3` |
| 2 | Multi-paragraph dialogue mis-pairs | `textstats.py:16` | A three-paragraph speech yields **2 spans**; the last paragraph's dialogue falls into *narration* and is fed to the exclamation, gesture, rhetorical-question and filter-verb sweeps. Share read 72.1% against a true 86.9% on the test sample |
| 3 | An unmatched double quote spans greedily | `textstats.py:16` | `[^”"]*` matches newlines, so one span swallows narration to the next quote anywhere in the file |
| 4 | Elisions raise DEFECT-level findings | `textstats.py:108` | `'twas`, `'em` and `'99` each match `unterminated_thoughts`. `Rock 'n' roll` correctly does not |
| 5 | A UTF-8 BOM defeats frontmatter parsing | `mdio.py:18,29` | `split_frontmatter` returns empty; every chapter reads as "no YAML frontmatter at all". The repo explicitly targets Windows |
| 6 | `stamp` rewrites the whole chapter file | `cmd_write.py:55-56` | Documented as touching frontmatter only. CRLF prose is silently converted to LF, and undecodable bytes are written back as U+FFFD |
| 7 | `lint` on zero chapters exits 0 | `sw.py:76-77` | An empty novel passes the linter |
| 8 | The `channels:` config is never read | `textstats.py:16-23` | Marks are hardcoded; `novel-toggle.md:42-43` documents changing them and warns of "a mechanical re-pass" that cannot happen |
| 9 | `readset --out` writes an arbitrary path | `sw.py:61-62` | No existence check, no overwrite guard, and `scripts/README.md:28` marks the command's writes column "no" |
| 10 | `audit --all` is a no-op | `sw.py:132` | Both branches lint every chapter identically |

Defects 1–4 share a shape worth naming: **they make the gate quieter, not louder.** A parser that
under-detects looks exactly like a clean chapter. That is the same failure class as benchmark
finding 9, one layer down.

### 3.2 The corpus contradicts itself

| defect | sites |
|---|---|
| `title-craft` is untracked while five tracked files cite it | `.claude/skills/title-craft/` vs. the modified `CLAUDE.md`, `README.md`, `novel-init/SKILL.md`, `novel-new.md`, `_template/novel.md` |
| Round D writes `opening.promise` "from the hook blurb the user just gave you" — but the blurb is now written later, in Step 2b | `novel-init/SKILL.md:94` vs. `:127-143` |
| Sensory budget is **two** in one skill and **two to four** in three others | `scene-craft:105,147` vs. `world-texture:52,172`, `revision-pass:191`, `write-chapter:106` |
| Three numeric length hooks survive in a system that declares itself numberless | `hook-and-pacing:30` (~1,200-word floor), `:159` (`length_band` checklist), `sw.py:120-129` (words column) against `CLAUDE.md:176` ("no report quotes a word count") |
| A cross-file citation by line number, now stale | `story-opening:199` cites `hook-and-pacing:38-39`, which is currently length text |
| The same check runs twice in one revision | `revision-pass:191` (Pass 5) and `:236` (Pass 8) |
| Three command tables, three contents | `CLAUDE.md:330-341` omits `doctor`; `scripts/README.md:13` says start with it; `lint --all` and `readset`'s writes column disagree |
| The deep-expertise budget for walk-ons is 1 in one place and 0 in another | `novel-character.md:39-60` vs. `cmd_cast.py:18` |
| Stale documentation | `docs/benchmark.md:156` says "37 skills" (now 40); `:271` tells the reader to audit `novels/small-enough-to-miss`, which no longer exists |
| `title-craft`'s ≤60-character rule appears only in its self-check, never in its six screens | `title-craft:243` vs. `:113-120` |
| The blurb is unreadable by tooling | `novel.md` has no `blurb:` field; it lives only in the body |
| Two orphan skills, referenced by no other skill | `comedy-levity`, `mystery-clues` |

### 3.3 What is *not* a problem

Worth stating so effort does not go there.

- **Python runtime.** A 250-chapter `audit` runs in 5–10 seconds. The one genuinely quadratic path,
  `cmd_state._plan:194` calling `plan_row` per chapter, costs 0.116s at N=250. The money in this
  system is tokens, not seconds.
- **Cross-reference integrity.** All 17 state and bible paths cited across the corpus exist in
  `novels/_template/`. All nine `sw.py` subcommands referenced anywhere exist. Eight slash commands,
  eight files. No dangling references.
- **The report cap.** `report.py:77` shows at most six findings per check across a whole run, so a
  250-chapter audit and a 25-chapter audit produce identically sized reports. That is correct for
  token cost. It only needs documenting, so nobody mistakes `audit` for an enumeration.

---

## 4. What the research says

Six findings changed the design. Sources in §9.

1. **Progressive disclosure is the documented shape of a skill.** ~100 tokens of frontmatter for
   discovery, a recommended **~5,000-token ceiling** on the body, everything else in `references/`
   pulled in only when a step needs it. This repo has zero supporting files and a §8 rule requiring
   self-sufficiency. Benchmark finding 9 — `revision-pass` was self-sufficient, so `bias-guard`,
   `voice-separation`, `competence-map` and `prose-quality` were never opened — is that rule's bill.

2. **The measured defects of AI fiction name what to build.** AI narrators state the story's theme
   explicitly **77%** of the time against **52%** for human writers. AI stories are homogeneously
   positive, with flatter arousal curves and less narrative tension, and they lose narrative purpose
   over the length of a novel. The failure is over-determination, not absence — which means the fix
   is a restraint rule, not an encouragement to Say Something.

3. **Microtension** is moment-to-moment unease produced by conflicting emotions inside a character,
   not by stakes, action or dialogue. `prose-quality` owns rhythm and verb strength;
   `conflict-engine` owns what a chapter costs. The line between them has no owner in this repo.

4. **Promise, progress, payoff** — and the serial-specific failure mode, perpetual deferral. A
   volume climax must deliver real closure on something promised; refusing to let arcs resolve is
   the most common complaint about long-running webnovels. `plan/arcs.md` asks for a dramatic
   question and an answer. Nothing checks the answer arrived.

5. **Platform mechanics are measurable, and absent here.** ~60% retention from chapter 1 to 2, 80%+
   thereafter. Daily posting is the gold standard, three a week is common, and dropping below one a
   week loses Trending rank in 10–14 days. Genre lists are far easier to enter than the main list.
   Secondary tags do better added when the element becomes prominent than at chapter 1.
   `title-craft` owns the title and the blurb and stops there.

6. **Judging is unreliable enough to forbid scoring.** The strongest off-the-shelf judge reaches
   **73%** agreement with human preference on creative writing, and rubric judges are measurably
   biased by position, length and formatting. So a judged pass may locate and describe. It may never
   score, and it may never gate. This is the same rule §9 already applies to the linter — *they
   find, they do not judge* — extended to the model.

Two further sources shaped W4 rather than adding a feature: a consistency-bug taxonomy for
long-form LLM stories spanning temporal logic, character memory, world-building rules, factual
detail and style; and narrative forecasting as a tension proxy — if the next chapter is predictable
from this one, the hook is weak.

---

## 5. The upgrade

### W0 — Hygiene

Small, mechanical, and first because everything else edits the same files.

1. Commit `.claude/skills/title-craft/` **together with** its five referencing files. Committing
   them apart leaves five dangling references at `HEAD`.
2. Fix the Round D ordering bug: `novel-init/SKILL.md:94` must write `opening.promise` from the
   premise and re-check it after Step 2b, or Round D must move after Step 2b. `title-craft:52-54`
   already anticipates this hazard; make the two agree.
3. Give the sensory budget one owner. `world-texture` holds it at 2–4; `scene-craft:105,147` and
   `prose-quality:53` cite rather than restate. Delete the half-tiebreak at `prose-quality:55`.
4. Resolve the three length hooks. Either delete `hook-and-pacing:30,159` and the words column, or
   amend `CLAUDE.md:176` to say word counts are reported as diagnostics and never as findings.
   Pick one; the current text asserts both.
5. Replace `story-opening:199`'s line-number citation with a section citation. Ban line-number
   cross-references in the style guide at `CLAUDE.md` §8 — they rot silently.
6. Delete the duplicate non-visual sensory check from `revision-pass` Pass 8, keeping Pass 5.
7. Reconcile the three command tables and add `doctor` to `CLAUDE.md` §9.
8. Reconcile the walk-on deep-expertise budget between `novel-character.md` and `cmd_cast.py:18`.
9. Add the ≤60-character screen to `title-craft` Step 4, where the other five screens live.
10. Update `docs/benchmark.md:156` (37 → 40 skills) and `:271` (the audit command names a novel that
    does not exist — point it at the temp-dir fixture from W1 instead).
11. Note the two orphan skills in `CLAUDE.md` §3 as reachable only through `novel-toggle`, or wire
    them into the skills that would call them.

**Acceptance:** `git status` clean; no reference in any tracked file resolves to a missing file;
no two files state different numbers for the same budget.

### W1 — Make the gate trustworthy

Nothing downstream is worth measuring until this is done, because the numbers the gate produces are
currently wrong in the direction of passing.

**Parser fixes**, all in `scripts/swlib/`:

- Anchor speech spans to paragraph boundaries so the standard multi-paragraph convention (opening
  quote on each paragraph, closing quote only at the end) is classified as speech throughout, and an
  unmatched quote cannot swallow narration past a blank line.
- Accept curly `‘…’` and `’` for thought, and mixed pairings, from the `channels:` block rather than
  from hardcoded literals. Reading `channels:` closes defect 8 in the same change.
- Exclude leading-apostrophe elisions and year abbreviations from `unterminated_thoughts` — a lone
  `'` followed by a letter and later terminated by a word boundary is an elision, not an open mark.
- Strip a UTF-8 BOM at read in `mdio.read_text`.
- Make `stamp` rewrite the frontmatter block only, preserving the body's bytes and line endings.
  Refuse a file with undecodable bytes rather than writing U+FFFD into someone's prose.
- Constrain `readset --out` to a path inside the novel or a scratch directory, with an overwrite
  guard, and fix `scripts/README.md:28`.
- Make `lint` on a novel with zero chapters a usage error (exit 2), not a silent pass.
- Make `audit --all` do something distinct or delete the flag.

**Then the repo's first tests.** Stdlib `unittest`, no new dependency, fixtures constructed in a
temp directory so `novels/` stays story-free:

```
tests/
  test_channels.py     the matrix in §3.1 as explicit cases, plus the 40%-vs-70% share case
  test_mdio.py         BOM · CRLF · tabs for indent · unclosed quote · '#' in an unquoted value
  test_state.py        ledger/plan/thread integrity, orphan thread ids, wc: agreement
  test_write.py        stamp round-trip is byte-identical outside the frontmatter block
  test_cmds.py         zero chapters, missing frontmatter, exit codes
  fixtures.py          builds a synthetic novel in tempfile.TemporaryDirectory()
```

Run with `python3 -m unittest discover tests`. Document it in `scripts/README.md` and add it to the
`audit` section of `docs/benchmark.md` as the cheap half of reproduction.

**Acceptance:** every row of §3.1 has a failing test before the fix and a passing one after. The
multi-paragraph case reports a share within 2 points of hand-count.

> **Done.** 46 tests, `python3 -m unittest discover tests`. Two defects beyond the table were
> found and fixed while writing them: the YAML reader lost all nesting under tab indentation, and
> an unclosed quote in `novel.md` swallowed every following config key. Both are now covered.
> One plan item was not carried out as written — `docs/benchmark.md`'s "37 skills" is historical
> narration of run #1 and is accurate, so it stands; the unreproducible audit command next to it
> is what changed.

### W2 — Context economy

**The split.** Every one of the 40 skills becomes a procedure plus references:

```
.claude/skills/<name>/
  SKILL.md                      the procedure a model executes — target ≤ ~1,200 words
  references/audit-card.md      the revision-time check, authored by this skill's owner
  references/<topic>.md         worked examples, failure catalogues, genre notes, long tables
```

Rules for the split:

- The **body** keeps: what the skill owns, the procedure, the hard rules, and the pointers.
- **`references/`** takes: worked examples, failure-mode catalogues, genre-specific notes, and any
  table longer than about ten rows. Each pointer states an explicit trigger — *open this when …* —
  because an unconditioned pointer is not read.
- Every skill that `revision-pass` must consult gains **`references/audit-card.md`**, and
  `revision-pass` opens *that* instead of carrying a condensed checklist it wrote itself.

That last rule is the point of the whole workstream. `CLAUDE.md` §8 currently carves out an
exception to self-sufficiency because summaries cannot audit a cast — and run #1 showed the model
answering that requirement by reading the summary anyway. The card resolves the conflict honestly:
the model still opens the owner's file, but the file it opens is small enough to be worth opening.

Order of work, one skill per commit: the eight hot-path skills (`write-chapter`, `revision-pass`,
`continuity-summary`, `voice-separation`, `competence-map`, `bias-guard`, `story-opening`,
`meta-knowledge`), then the character group, then craft, then genre and optional.

**`CLAUDE.md` diet.** It is loaded into every session. Keep the resolution rule, the pipeline, the
registry, the hard rules, the file conventions and the toolkit table. Move the rationale essays —
why length stopped being the gate, the four-channel argument, the design history — into
`docs/design-notes.md` and link once. Target ~2,200 tokens, from ~4,800.

**`sw.py brief -c N`.** One consolidated context pack, replacing the dozen separate reads at
`write-chapter` step 0: ledger blocks N−5…N−1, the plan rows for N and N+1, the speakers' voice and
competence rows, the locations' sensory signatures, threads touching N, the foreknowledge slice, the
current form row, and the `novel.md` lines that gate behaviour. Deterministic ordering, stable
across runs, so it caches. `readset` stays as the narrower primitive.

**Free CPU wins while in there** — worth doing only because the files are already open: memoize the
table accessors on `Novel` (`plan_rows`, `threads`, `voice_rows`, `competence_rows`, …), cache
`Chapter.outside_speech` (recomputed **8×** per `lint_chapter`), and stop `lint -c N` from loading
every chapter merely to compute a maximum.

| target | before | after |
|---|---|---|
| Per-chapter must-open set | ~30,200 tokens | **≤ 12,000** |
| `CLAUDE.md` | ~4,800 tokens | **≤ 2,400** |
| Reads at `write-chapter` step 0 | ~12 | **1** |

**Acceptance:** the token measurement in §8 hits both targets, and the cold-agent test shows
`references/*.md` files actually being opened.

### W3 — Craft features

All four land inside skills that already exist. **No new skill is created.** Run #1 showed 21 of 37
skills never loading; a 41st file would be a 22nd unread one.

| feature | lands in | substance |
|---|---|---|
| **Controlling idea + restraint** | `novel.md` `theme:` block · `novel-init` · `chapter-plan` · `revision-pass` | Record a controlling idea and its strongest **counter-case** — the argument against it that a character actually gets to make and win with at least once. `chapter-plan` marks which arcs test it. The revision check is **restraint**, aimed squarely at the 77% defect: the theme is dramatized and never narrated. If it is stated aloud, a *character* states it, and is either wrong about it or pays for it. Put the 77%/52% figures in the skill text so the rule survives future editing. |
| **Microtension + subtext** | `prose-quality` · `dialogue-voice` | Microtension: unease sourced from **conflicting emotion inside one character**, applied per page rather than per chapter; the check is that a page opened at random has something unresolved in it. Subtext: upgrade `dialogue-voice:84-85` from two lines of principle to a four-technique procedure — contradicting action, evasion, irony, non-verbal tell — with at least one exchange per scene running on it. Both get a line in the relevant `audit-card.md`. |
| **Arc payoff** | `plan/arcs.md` · `plot-threads` · `sw.py state` | Every arc closes at least one thread **on the page**. Threads age: one open longer than a declared horizon is escalated, paid, or deferred with a stated reason recorded in `state/threads.md`. `sw.py state` reports thread age; it reports, it does not fail the build. Ties into the ending contract `timeline-engine` already owns. |
| **Listing kit** | `title-craft` · `hook-and-pacing` · `novel.md` `platform:` block | Tags with the add-when-the-element-becomes-prominent rule, a cover brief, and a launch-stock recommendation. A cadence table with the Trending-rank consequence, and the 60%/80% retention benchmarks stated as what the opening is designed against. Add the `blurb:` field so tooling can finally read the blurb and check it against the promise ledger. |

**Acceptance:** each feature has an `audit-card.md` line, a `novel.md` field where it needs state,
and a worked example in `references/`. None of them introduces a number that decides whether a
chapter ships.

### W4 — The arc-level gate

Every failure this format actually suffers is distributional — dialogue starvation, word-count
clustering, voice convergence, an unpaid promise, a foreknowledge advantage that never wins. All
five of run #1's high-severity findings were invisible in any single chapter. `revision-pass` sees
one chapter and cannot, in principle, catch them.

Add an arc-boundary pass, in two halves:

- **`sw.py arc N`** — the countable half. Dialogue-share trend across the arc, hook-type rotation,
  cast rotation (who has spoken in the last ten chapters), voice-matrix drift, thread ages, anchor
  vocabulary coverage, `delivers:` presence, and ledger agreement. It prints a table.
- **The judged half** — the model reads only what the script flagged, plus the arc's plan rows, and
  reports on the consistency taxonomy: temporal logic, character memory, world rules, factual
  detail, style. Plus two questions no script can ask: does the arc close what it opened, and is the
  next chapter predictable from this one?

It **locates and describes**. It never scores, and it never gates. Put the 73% agreement figure in
the skill text as the reason, so that a later editor cannot mistake the omission for an oversight.
Wire it to `/novel-recap` at arc boundaries rather than adding a slash command.

**Acceptance:** run against a synthetic arc with three planted distributional defects; all three are
located, and the report contains no score.

---

## 6. Sequencing

```
W0 hygiene  ──►  W1 gate + tests  ──►  W2 context economy  ──►  W3 features  ──►  W4 arc gate
   (hours)          (the numbers        (the split, all 40      (four, inside      (needs W1's
                     must be right       skills, hot path        existing skills)   numbers and
                     first)              first)                                     W2's cards)
```

W1 precedes everything because W2's targets, W3's checks and W4's tables are all measurements, and a
measurement taken with a broken instrument is worse than none — it is an alibi. This is the same
argument `CLAUDE.md` §9 already makes about a clean lint run not being a passed revision.

---

## 7. Non-goals

Stated explicitly, because each has been tried or is tempting:

- **No length gate, in any form.** Two versions were gamed within five chapters each. Nothing in
  this plan reintroduces one, and the words column survives only as a diagnostic.
- **No scoring judge.** 73% human agreement is not a gate.
- **No new skills.** Four new capabilities, zero new files in `.claude/skills/`.
- **No CPU optimisation beyond what is free.** The quadratic path costs 0.116s at 250 chapters.
- **No auto-fixer for prose.** `mtl-detox` requires the sentence rewritten, not the synonym
  swapped; an auto-fixer would do exactly the forbidden thing.
- **No fixture novel in `novels/`.** Tests build fixtures in a temp directory; the repo stays
  story-free.

---

## 8. Verification

| what | how |
|---|---|
| Token targets | `wc -w` over the must-open set and `CLAUDE.md`, × 4/3, before and after. Pass/fail against §5's table |
| Parser correctness | `python3 -m unittest discover tests` green, with every §3.1 row as an explicit case |
| Toolchain health | `python3 scripts/sw.py doctor` and `audit` clean against the temp-dir fixture |
| **Did the split work?** | The cold-agent test: a fresh session writes one chapter, then the transcript is read for which `SKILL.md` **and which `references/*.md`** were opened. This is the only real proof, and it simultaneously closes benchmark finding 9, which was fixed but never validated |
| Did it get cheaper? | One cold-session chapter, costed against run #1's $1.91 and 8.55M cache-read baseline. Note that run #1 used one persistent session, so this also settles the flat-cost claim the README makes and the benchmark could not support |

The last two are the ones that matter. Everything above them is machinery.

---

## 9. Sources

Craft:

- [Story Grid — The Five Commandments of Storytelling](https://storygrid.com/five-commandments-of-storytelling/)
- [Brandon Sanderson — Guide to Plot: promise, progress, payoff](https://www.brandonsanderson.com/blogs/blog/brandon-sandersons-2025-guide-to-plot-lecture-2)
- [Donald Maass on micro-tension (excerpt)](https://www.floggingthequill.com/flogging_the_quill/2009/04/microtension-an-excerpt-from-the-new-donald-maass-book.html)
- [Jane Friedman — The Art and Purpose of Subtext](https://janefriedman.com/the-art-and-purpose-of-subtext/)
- [How to Outline a Serialized Web Novel: The Volume Roadmap](https://readnovax.in/blog/how-to-outline-a-serialized-web-novel-the-volume-roadmap-en)
- [Reagan et al. — The emotional arcs of stories are dominated by six basic shapes](https://arxiv.org/abs/1606.07772)

Platform:

- [Royal Road — average first-to-second chapter retention](https://www.royalroad.com/forums/thread/134345)
- [Royal Road Rising Stars readiness checklist](https://fictionops.com/guides/royal-road-rising-stars)
- [Rising Stars data guide](https://www.chapterchronicles.com/blog/rising-stars-complete-guide/)
- [Staying on Trending after launch month](https://seosa.ink/en/blog/royal-road-trending-best-rated-long-term-strategy)

Machine-written fiction and its evaluation:

- [The AI Fiction Paradox](https://arxiv.org/pdf/2603.13545)
- [StoryScope: investigating idiosyncrasies in AI fiction](https://arxiv.org/pdf/2604.03136)
- [Lost in Stories: consistency bugs in long story generation](https://arxiv.org/html/2603.05890v1)
- [Spoiler Alert: narrative forecasting as a metric for tension](https://arxiv.org/pdf/2604.09854)
- [LitBench: reliable evaluation of creative writing](https://aclanthology.org/2026.eacl-long.362/)
- [Reliability without Validity: LLM-as-a-judge across agreement, consistency and bias](https://arxiv.org/html/2606.19544v1)
- [Dynamic hierarchical outlining with memory enhancement for long-form stories](https://arxiv.org/html/2412.13575)

Agent engineering:

- [Agent Skills — Claude platform documentation](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview)
- [Agent Skills: progressive disclosure as a system design pattern](https://www.newsletter.swirlai.com/p/agent-skills-progressive-disclosure)

Internal:

- [`docs/benchmark.md`](benchmark.md) — run #1, and the three follow-ups it left open.
