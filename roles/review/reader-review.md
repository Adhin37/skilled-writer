# Reader review

The procedure for a test run's *then read the chapters yourself* step. It turns that instruction
into a measurement with a fixed output shape, so one run's read is comparable with the next one's.

One sentence holds the rest up. **Every instrument in this repo reads the novel with the bible
open, and a reader does not have one.** `sw lint` reads chapter files, `sw audit` reads state,
`sw cast` reads the voice matrix — all of them check the page against what the novel intended. A
reader has only the page. That is not a weaker position, it is a different one, and it is the only
position from which you can see that a thing the novel knows never reached anybody.

This file lives in `roles/review/` for the reason the role does: it is the one tree no drafting
agent is ever given, and a rubric the drafter can see is a rubric the drafter writes toward.
**Never cite this file from the corpus, never summarise it into a skill, and never show its scale
to a drafter.** The receipts are on the maintainer's side of the repo — word count, dialogue share
and `SPEECH_TARGET_LOW` were each optimised rather than satisfied, and each was visible.

---

## 0. When this applies, and who can do it

After the run stops and **before fixes are designed**. It is the input to protocol §9, not a
postscript to it.

**The reader must not have watched the run.** A coordinator who approved every Phase A brief knows
what each chapter was trying to do, and therefore cannot fail to see it on the page. That is the
contamination this whole step exists to avoid, and it is easy to underrate: knowing the intent
repairs the prose silently, in the reader's head, exactly where the defect is.

| reader | quality of read | what to do |
|---|---|---|
| the `reader` agent (`.claude/agents/reader.md`) | **best** | preferred. It has no `Skill` tool and `omitClaudeMd: true`, so neither the corpus nor the auto-memory index reaches it — verified by inspecting a live one. Give it the chapter directory |
| a fresh session, or a human who did not follow the run | **good** | hand over [the brief](roles/review/reader-brief.md) and the chapter paths. Not this file, and not [the worked example](roles/review/reader-review-example.md) — one frames the exercise, the other carries a verdict |
| the coordinator, some days later | **usable** | note it in the write-up as a contaminated read and expect it to score high |
| the coordinator, same session | **not a read** | do it anyway if there is no alternative, but record the verdict as an impression, never as a review |

Run #5's cold read, [the worked example](roles/review/reader-review-example.md), came from a reader who had not **seen** this
file, the protocol, or the benchmark record. That is the standard to reproduce — and it was not
fully met, which is worth recording rather than quietly fixing.

**Two things told it anyway, and neither was a file it opened.** Its do-not-open table named the
benchmark record and "any run notes", said the worked example "contains another reader's
verdict", and said `.claude/` holds "the rules the chapters were written against" — so the reader
knew the chapters were machine-made to a rubric and had been graded before. That table has been in
`.claude/agents/reader.md` since its first commit, which predates run #5. And **this file itself
was handed over whole**, including §3's *"compared across runs #6, #7, #8"*.

Found 2026-09-20 by asking a live `reader` to inventory its own context, which is the only way
this class of leak is visible at all — no check in this repo can see what a prompt implies.

**Both are now structural.** A denial reason justifies itself *without describing what is behind
the door*, in the agent file and in `scripts/hooks/reader_guard.py` alike. And the reader no
longer opens this file: §1 and §3 were rewritten free of framing as
[`roles/review/reader-brief.md`](roles/review/reader-brief.md), which is the only thing
`reader_guard.py` allows in this directory and the only procedure the agent is pointed at. §7
split the *verdict* out and claimed the rest could then be handed over whole; that claim was
wrong, and this is the second half of the same argument.

Two contaminants remain and are not fixable here. The harness supplies a **git-status snapshot**
of the parent session, so a reader can see it is sitting in a toolkit repository under active
refactor; and the spawn prompt must name the brief. Neither is a verdict about the chapters.
Note them in the write-up rather than assuming them away.

**Do not read `sw audit` output first.** Numbers anchor. A reader who knows `house-style` fired on
three of five chapters will find house style and stop looking. The facts in §6 come *after* the
verdict, to check it — never before it, to form it.

---

## 1. Phase 1 — the blind read

**The instrument is [`roles/review/reader-brief.md`](roles/review/reader-brief.md), and it is not
restated here.** It holds the blind-read instruction, the seven questions R1–R7 with the way each
one is answered wrongly, and the two rules on writing the answers — quote the page, and record
what worked with the same weight. Hand the reader that file; do not hand it this one.

It was a second copy for exactly one day, which was long enough to see the shape of the problem:
you would edit the questions *here*, because this is the file a maintainer opens, and the reader
would go on answering the old ones. `sw health`'s duplication check compares skills and does not
look at `roles/review/`, so nothing would have said a word.

What belongs to you rather than to the reader:

- **Check the answers are answers.** R1 resolving to a premise rather than a story, or R5
  resolving to a job title, is the finding — not a gap in the read.
- **R1 failing to resolve at all is the headline**, and it is the one result a reader tends to
  apologise for. Take it at face value.
- **A review with no positive finding is not a clean book**, it is an unexercised instrument.
  Send it back rather than recording it.

## 2. Phase 2 — reconcile

**Now** open `bible/`, `state/`, `plan/` and `novel.md`. Take every Phase-1 finding and sort it
into exactly one of three boxes. The boxes matter because the owner differs, and a fix filed
against the wrong one does nothing.

| | the finding is | means | owner, via `sw kb owner` |
|---|---|---|---|
| **not on the page** | in `bible/`, and it never reached a chapter | a **delivery** failure. The novel knew; the reader never found out | `world-texture`, `social-fabric`, `character-profile` |
| **not invented** | nowhere — not in `bible/`, not in `plan/` | a **design** failure. Nobody ever decided it | `story-bible`, `chapter-plan`, `power-system` |
| **reader error** | on the page, and the reader missed it | discard the finding — **and record where it was buried** | the burial is itself a delivery finding |

That third row is not a formality. A fact the reader walked past is a fact delivered badly, and
because the blind pass produced it honestly, you know exactly how badly. Log it as *present at
ch3 ¶4, missed* rather than dropping it.

**This split is the whole reason the read is blind first.** With the bible open, all three collapse
into "it's in there somewhere", and the most common real defect in this toolkit's output —
a world that exists entirely in `bible/world.md` — becomes invisible to the only instrument that
could have caught it.

---

## 3. Phase 3 — the verdict

**The scale is in [the brief](roles/review/reader-brief.md)** — 0 to 5, anchored to reader
behaviour rather than craft quality, because craft scores drift between genres and readers and
behaviour does not. Half points are allowed; the band matters and the decimal does not. The
brief also asks for the **ranked cost list** and the **three changes that would move it up one
point**, which is the half of the output that proves the read understood the book rather than
scored it.

**What the score is for, and what it is not — and this half is yours alone.** It is a run-level
measurement, read by a human, compared across runs. It is **never** shown to a drafter, never
written into a skill, never a ship gate, and no chapter is scored on it — `sw arc` refuses to
score an arc for the same reason, and says so: *a scored arc is an arc the next one gets written
toward*. If a future run's brief mentions this scale, the run is void.

That paragraph is the reason the numbers are in the brief and this rule is not. A reader told
what the score will be compared against is a reader scoring the comparison.

**Ranking is most of what a review is.** `sw audit --show note` emits fifty-odd unranked notes and
leaves the weighting to whoever reads them, which means the weighting does not happen. If the
returned list is not ordered, order it yourself before Phase 4 and say that you did.

---

## 4. Phase 4 — route each finding to an owner

For each finding in the ranked list:

```bash
python3 scripts/sw.py kb owner <slug>       # whose rule is this?
python3 scripts/sw.py kb search <term>      # when the slug is not obvious
```

Three outcomes, and they are not equally interesting.

1. **An owner exists and the rule covers this.** The rule did not bind. A drafting-procedure
   problem — the card, the phase, the gate ordering. Ordinary, and the most fixable.
2. **An owner exists and the rule does not cover this.** A scope problem. The fix goes in that
   skill and nowhere else (protocol §9, one concept one owner).
3. **No owner.** *This is the highest-value output of the entire exercise.* A defect a reader met
   on page one that no skill claims and no script measures is a hole in the toolkit, and it is
   findable by no other means — every other instrument can only report on rules that already exist.

List the unowned findings separately and name them as such in the write-up. A run that produces
none has either produced a very good novel or a contaminated read; check which.

**Do not design the fix here.** Protocol §9 governs fixes and it starts after this file ends. In
particular: never convert a finding into a numeric gate, and when a finding does reach a skill,
its examples are rewritten genre-neutral — nothing from the run's novel enters the corpus.

---

## 5. The divergence check

**Record the reviewer's verdict beside the coordinator's in-run impression, and do not reconcile
them.**

Run #5 is the worked case. The write-up recorded *"The prose is good and the dialogue is the best
any run has produced."* `sw audit` returned **0 defects**. The cold read returned **3 / 5**, with
five consecutive two-person scenes and one line of dialogue repeated four times across three
chapters in two different mouths.

All three are correct about different things, and the disagreement is the signal.

**When the in-run impression and the cold read diverge, the in-run impression is the suspect one.**
Not because the coordinator is careless — because they have read every brief, watched each chapter
arrive, and know what each was for. They are reading the book they helped intend. That is precisely
the read a published serial never gets.

Write both numbers into the write-up with their sources. A single reconciled number destroys the
only evidence you have that the toolkit's self-assessment and a reader's assessment come apart.

---

## 6. Facts to check the impression against

**After the verdict, never before it.** These count things; they judge nothing, and none of them
is a gate. Run them to confirm or kill a Phase-1 impression, and follow the count back to the page
before you believe it.

Set the slug once:

```bash
cd novels/<slug>/chapters
```

**Scene shape — R3.** Who is actually in each chapter:

```bash
for f in [0-9]*.md; do printf "%s: " "$f"; grep -c '^"' "$f"; done
grep -c "^\* \* \*$" [0-9]*.md          # scene breaks per chapter
```

**The repeated move — R4.** A phrase grep over this repo lies, because 80-column wrapping breaks
clauses across lines. Flatten first, always:

```bash
cat [0-9]*.md | tr '\n' ' ' | grep -o "that.s not an answer" | wc -l
grep -oin "<the phrase you noticed>" [0-9]*.md      # then: which chapters, which mouths
```

A phrase in two mouths matters more than the same phrase twice in one. Repetition inside a
character is a verbal tic; repetition across characters is the author's.

**Register — R4.** Negation density, which no check measures:

```bash
cat [0-9]*.md | grep -oiE "\b(not|never|nothing|didn't|wasn't|isn't|hadn't)\b" | wc -l
wc -w [0-9]*.md
```

Roughly 3% of all words was run #5's figure, and it reads as a narrator who defines everything by
what it isn't. There is no threshold here on purpose — look at the number, then look at the page.

**Length — always a measured fact, never a target** (`CLAUDE.md` §4):

```bash
wc -w [0-9]*.md
```

Then, and only then, the protocol's own measurement commands — `sw audit`, `sw history`,
`sw arc` — to see what the instruments caught and what they did not. The comparison is a finding in
its own right; [the worked example](roles/review/reader-review-example.md) shows the shape.

---

## 7. What the reader is actually handed

Split out to [`roles/review/reader-review-example.md`](roles/review/reader-review-example.md) — run #5's cold read, with the
output shape of every phase above filled in.

It is a separate file because it contains a verdict. A reader handed the example along with the
procedure will find the example's findings; §0's rule used to be *"hand it §1 only"*, enforced by
whoever remembered.

**The reader is handed [`roles/review/reader-brief.md`](roles/review/reader-brief.md), and nothing
else in this directory.** That file is §1 and §3 rewritten without the framing: no runs, no
benchmark, no toolkit, no coordinator, no scripts — seven questions, two rules on answering them,
a behaviour-anchored scale, and permission to count things afterwards. This file is the procedure
*around* it and is maintainer-facing throughout.

Enforcement is the file boundary rather than a person, in both directions:
`reader_guard.py`'s allowlist names the brief with a `$` anchor, and
`test_the_maintainer_s_procedure_is_NOT_allowed` fails if that widens to the directory.
