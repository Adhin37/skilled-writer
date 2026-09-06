# skilled-writer

A toolkit of AI skills for writing **serialized webnovels** — the 1,500–2,500-words-per-chapter,
hook-every-chapter format used on webnovel.com, Royal Road and similar platforms.

It is built so a cheap, fast model (Sonnet-class at low or medium effort) can write chapter 250
of your novel and still remember that the swordsman lost two fingers in chapter 61, that your MC
never uses contractions when lying, and that the debt thread you opened in chapter 12 is still
unpaid.

Genres supported out of the box: **fantasy**, **science fiction**, **fan fiction**.

## Why it exists

Most of the serialized fiction an AI has absorbed comes from machine-translated Chinese webnovels.
That corpus is enormous, and it carries defects: a face-slapping loop instead of a plot, harem
casts where the women have no goals, ethnic and national essentialism used as villain shorthand,
protagonists who are called geniuses while behaving like idiots, and a translated prose register
full of tells ("unexpectedly", "his expression changed drastically", "as expected of the young
master").

This toolkit keeps the *engine* of the format — fast hooks, escalating stakes, visible progression,
serial cadence — and explicitly strips the rest. Two skills, `mtl-detox` and `bias-guard`, run on
every chapter and are not optional.

**A chapter is judged by what it delivers, not by how long it is.** The gate is five questions —
what did the POV character want, what stood in the way, **what is materially different at the
end**, what did it cost, and what does the reader now need to see. Word count is recorded as a
fact and scored on nothing. That is a correction: earlier versions gated on a target with
tolerances, and chapters clustered against the floor, then against the tightened floor, then
landed on the declared minimum to the word. Any number that decides whether a chapter ships gets
optimised, and prose optimised toward a length is padded or truncated prose.

## Setup

Clone the repo and open it with [Claude Code](https://claude.com/claude-code). There is nothing
to install and no build step — the toolkit is markdown. Claude Code discovers `.claude/skills/`
and `.claude/commands/` automatically, and reads `CLAUDE.md` on every session.

```bash
git clone <this-repo> skilled-writer
cd skilled-writer
claude
```

### Optional: Python 3.8+

The toolkit ships a small stdlib-only program, [`scripts/sw.py`](scripts/README.md), that does
the countable work the skills would otherwise do by reading: slicing the read-set, sweeping a
chapter for banned phrases and channel mechanics, auditing the cast tables, and checking the
ledger against the chapters. It makes chapters cheaper and the mechanical QC independent of
whether the model remembered to look.

```bash
python3 scripts/sw.py doctor        # start here; reports version and workspace
```

**Nothing breaks without it.** Every skill that names a command keeps its manual checklist
directly underneath, and the model does the same checks by reading, exactly as before. No
packages, no install, no build step — the standard library is the whole dependency.

| OS | getting Python | note |
|---|---|---|
| **Linux** | preinstalled on nearly every distribution | `python3` |
| **macOS** | `python3` ships as a Command Line Tools shim; the first run offers to install it | `python3` |
| **Windows** | not preinstalled — `winget install Python.Python.3`, or the python.org installer (tick *Add to PATH*) | use `python` if `python3` is not found |

### Portability

Works on Windows, macOS and Linux. Nothing in the repo hardcodes a path, a drive or a shell:
`.claude/settings.json` uses project-relative permission rules, `.gitattributes` normalises line
endings to LF, and `.gitignore` keeps generated books, per-machine tool state and OS cruft out.

**On Windows specifically**: Claude Code's Bash tool runs through Git Bash, which comes with
[Git for Windows](https://git-scm.com/download/win). The scripts here sidestep that question
entirely — they are invoked as `python3 scripts/sw.py …`, never shell out, and never build a
path by hand, so they behave identically from bash, Git Bash, PowerShell or `cmd`. Output is
forced to UTF-8, because novel prose is full of em-dashes and a legacy console code page would
otherwise crash on the first one.

Your novels live in `novels/<slug>/` and are **gitignored by default** — see
[novels/README.md](novels/README.md) if you want to version one.

## Quick start

```
/novel-new
```

The model interviews you (premise, genre, POV, tone, how smart your MC is, which optional
mechanics you want), then scaffolds `novels/<your-slug>/` with a config file, a story bible, a
cast, an arc plan and a chapter list.

Then, per chapter:

```
/novel-write          # drafts the next planned chapter, updates all state
/novel-revise         # QC gate: prose, continuity, bias, MTL artifacts
```

Other commands: `/novel-status`, `/novel-plan`, `/novel-character`, `/novel-recap`, `/novel-toggle`.

## What it costs to run

Measured on a real run — one Naruto fan fiction, Claude Sonnet 5, scaffold plus five revised
chapters. Full method, raw tables and caveats in [docs/benchmark.md](docs/benchmark.md).

| | |
|---|---|
| Setup — interview + full scaffold, one-time | **~$21**, ~40 min |
| Each chapter after that | **~$1.90**, ~4 min |
| A 30-chapter arc, end to end | **~$115**, ~3 hours |

Three things worth knowing before you start:

- **You are not paying for prose.** Output was 3% of the bill. The other 97% is the model reading
  state back in. Cheap chapters come from a small read-set, not from short chapters.
- **Setup is most of your first day's spend** — about eleven chapters' worth. It buys a bible, a
  cast with a voice matrix and a competence grid, an arc plan and twelve planned chapters.
- **Cost per chapter is flat only if you start a fresh session periodically.** Inside one long
  session it climbs with conversation length: cache reads rose ~34% over three consecutive
  chapters. The *read-set* is bounded; the *session* is not. `/novel-write` in a new session
  picks up from the state files, and that is the cheap path.

Run the audit on your own chapters to check the four channel shares, anchor vocabulary in the
opening arc, `delivers:` presence, MTL artifacts, the cast tables and ledger integrity —
independently of the model that wrote them:

```bash
python3 scripts/sw.py audit novels/<slug>
```

It reports word count as a fact and scores only whether the recorded number is *true*, because a
wrong one propagates into the continuity ledger.

**On the read-set.** Most of the bill above is the model reading state back in, and the read-set
is specified as *slices* — this chapter's speakers, this chapter's locations, the last five
ledger blocks. A model cannot read half a file, so in practice it read all of them, and the
ledger grows with every chapter written. `sw readset` emits the slices instead. Measured on the
sample novel, as bytes handed to the model: **62% smaller at chapter 6, 81% at chapter 45**, and
where the whole-file set grew by 107 KB across that span the sliced one grew by 5 KB. That is a
measurement of the bundle, **not** of the dollar figures above — those came from a real
instrumented run and are not revised here on the strength of a byte count. Benchmark run #2 will
settle it.

**These are numbers from one run of one genre**, stopped deliberately at chapter 5 when it turned
up two defects worth fixing. It is a rough order of magnitude, not a quote.

## The skills

**Core loop** — `novel-init`, `title-craft`, `mc-design`, `story-bible`, `story-opening`,
`chapter-plan`, `continuity-summary`, `write-chapter`, `revision-pass`

**World** — `story-bible`, `social-fabric`, `world-texture`

**Character** — `character-profile`, `voice-separation`, `competence-map`, `meta-knowledge`,
`character-development`, `mc-intel-meter`, `dialogue-voice`, `lead-interest`

**Craft** — `narrator-voice`, `pov-switch`, `scene-craft`, `conflict-engine`, `plot-threads`,
`timeline-engine`, `hook-and-pacing`, `prose-quality`, `mtl-detox`, `bias-guard`

**Genre modules** — `power-system`, `tech-plausibility`, `fanfic-canon`

**Optional, toggled per novel** — `no-harem` (on by default), `romance-arc`,
`combat-choreography`, `litrpg-system`, `mystery-clues`, `comedy-levity`,
`grimdark-consequences`, `slice-of-life-texture`

Fourteen of these deserve a note:

- **`title-craft`** runs once, before the workspace directory even exists, and owns the two
  things a stranger sees *before* chapter 1 is available to them: the **title** and the
  **platform blurb**. Asked for five titles, a model reliably produces five rewordings of one
  idea, so the skill demands five *strategies* — role-plus-fracture, first-person claim,
  mechanism, understated flat, destination — and forbids two candidates from sharing a strategy
  or a first noun. The survivors are screened: truncate at 30 characters and see what is left,
  say it aloud and try to spell it back, name three books you would confuse it with, hold it
  against `opening.promise`, and ask whether it is still true at chapter 100. For **fan fiction
  the source work goes in the title line** — *Naruto: The New God of Shinobi* — because fanfic is
  browsed by fandom and a title that omits the search term is invisible to the only audience it
  has. The slug is derived here and is permanent; the title is not, and the runners-up are kept
  in `title_alternates` for the rename at chapter 40.

- **`story-opening`** exists because chapter 1 is not the first chapter of a book, it is a
  **conversion event**: roughly 60% of the people who open it reach chapter 2, and from chapter 5
  retention runs 80% or better. Nearly all your attrition is at one join. The skill owns everything
  up to `opening.contract_by_ch + 2` and enforces four things a first arc owes a reader — the
  **anchor** (what kind of world, what kind of place, what the MC wants, and for fan fiction
  *which story and roughly when in it*), the **genre contract** by chapter 3, the **promise
  ledger** that holds the blurb to the page, and the **stakes ceiling**, which is the one most
  drafts miss: *a consequence may not escalate past the reader's ability to price it.* An opening
  can be well-written, well-paced and completely unplaceable — a measured run of this toolkit
  produced five chapters and ten thousand words containing zero occurrences of its source's
  setting, factions or central power, while its suspicion plot escalated to "an adult is now
  certain something is wrong with her." Every beat was earned; none of it landed, because the
  machinery that made it dangerous had never been on the page. Anchor vocabulary is therefore
  front-loaded by rule, and escalation waits for the frame it depends on.

- **`meta-knowledge`** runs any MC who knows what happens next — self-inserts, transmigrators into
  a novel, regressors, reincarnators — and it exists because the mechanic fails in two opposite
  directions. The **oracle** has accurate, unlimited, free foreknowledge and no tension after
  chapter 20. The **handicap** is subtler, commoner in careful writing, and worse: foreknowledge
  introduced as already-unreliable, whose every appearance is a malfunction, so the reader was
  promised an advantage in the blurb and shown only a disability. The fix is an order —
  **it works, then it costs, then it frays, then it betrays** — enforced as
  `foreknowledge_first_win_ch` < `foreknowledge_fails_ch`. Around that sit a declared **grain**
  (`episode-precise` · `major-beats` · `impressions` · `fandom-corrupted`) that caps what any plan
  may assume, the **inventory scene** where the MC actually sits down and triages what they know —
  the beat readers came for, and the one whose absence says loudest that the author does not intend
  to use the premise — and the **observer paradox**: acting on foreknowledge is the fastest way to
  destroy it, because the future the MC remembers is the one in which they did not act. That last
  makes decay a consequence the MC caused rather than a decree at a scheduled chapter, and it hands
  a foreknowing MC the graceful exit — events butterfly, but *people's natures* do not, so what
  they end up trading on is character rather than plot.

- **`competence-map`** fixes the other half of the same problem: the AI character is a **generalist
  with no edges** who answers every question at the same confident depth, so nobody ever says *I
  don't know*, *that's not my end*, or *ask Dael*. Real people are narrow — a decade on one thing,
  passable at three adjacent ones, tourists everywhere else — and that narrowness is where scenes
  come from, because it forces someone to ask, to trust, to guess, and to be wrong. So every
  character gets domains with a **named edge**, a budget on deep expertise (three for the MC, one
  for a supporting character), a **referral** for what lies outside it and what asking costs them,
  and one governing default: **an unlisted domain is `none`, not "probably fine."** Every stated
  fact then passes a provenance test — taught it, did it, was told it, read it, or openly guessing —
  and "they're intelligent" is not a provenance, because a high tier makes you infer faster, not
  know more. Ignorance comes in four flavours and the skill prefers the productive one: a character
  who is *wrong* acts, while a character who is blank just stalls. Skills are acquired the honest
  way, on a five-stage ladder — can't → fails knowingly → unreliable → competent → fluent — where
  advances come from a teacher, a text or a costly failure and never from chapters having passed,
  with a plateau around stage 2 and a rule that keeps it affordable in a serial: **transitions get a
  scene, practice gets a clause.** The deliberate exception is settings with gods, immortals,
  cultivators or an ASI in them: those declare `knowledge_scope: broad` and are handled on the
  principle that **even omniscience has a shape** — a god of wisdom is not a god of people, an
  immortal's breadth is era-locked, an ASI has never lifted anything and interpolates confidently
  across its own blank regions — and that you bound the *access*, not the knowledge, because an
  unbounded oracle dissolves every mystery in the book.

- **`voice-separation`** attacks the defect that gives AI-written fiction away fastest: every
  character reasons as quickly as the MC, argues as fluently, and lands the same dry jokes, because
  the protagonist is what the model calibrates against. Fingerprints do not fix it — contractions
  and a vocabulary tell painted over identical minds produce *labelled* clones. So the whole cast
  goes on a matrix instead: **intelligence** (the `mc-intel-meter` ladder, applied to everyone),
  **articulacy** as a separate axis — the character who is right and cannot prove it and the one
  who is wrong and can out-talk anyone are built by pulling those two numbers apart — plus wit,
  emotional heat, a default words-per-turn budget, and a body idiom whose one hand-habit does more
  tag-free identification than any amount of dialect. The cast must **straddle** the MC's tier, at
  most two people are funny, no two speakers share intel + articulacy + wit, and the MC's best line
  must not fit anyone else's mouth. Thought is a channel too: POV characters get a **thought unit**
  (images, numbers, bodies, money) that becomes their metaphor source, and everyone else's mind
  reaches the page through their **first move** — three people enter a room, one checks the door,
  one checks the faces, one checks the exit — with no interiority at all. Over a long serial the
  skill also blocks the slow merge, since growth deltas all push toward the MC's register by
  default. One deliberate exemption: **clones, avatars, doubles and body-snatches** declare a
  `mirror:` and are allowed to sound like the person they copy — with the questions that make a
  double interesting still enforced, namely what has diverged since they split, and which single
  thing failed to copy.

- **The world trio.** `story-bible` records what is true and where things are. **`social-fabric`**
  works out the society under it — labour, money, law, knowledge, belief, mobility — and runs the
  **propagation test**: every hard rule of the magic or technology is forced down through
  institution, market and household, then asked what occupation it destroyed and what people do in
  the gap where it stops working. That gap is where most plots live, and skipping this step is how
  you get a spectacular magic system sitting on top of generic medieval wallpaper.
  **`world-texture`** then governs delivery, which is the half most drafts get wrong in both
  directions at once: flat *and* bloated. It ranks four channels by cost — a rule biting someone,
  a character working around the world, an unexplained passing reference, and only last, actual
  description — puts a hard budget on the last one, requires every detail to be load-bearing,
  filters what is noticed through the POV character's job and wound, and reserves one or two
  things per chapter that are referred to and never explained. That reserve is what makes a world
  feel bigger than the page.

- **`timeline-engine`** runs the world on its own clock. For most genres it stays coarse — the
  antagonist's plan and two or three standing clocks. For **fan fiction it is the centre of the
  toolkit**, because the genre's defining failure is an MC who changes nothing: canon fires on
  its original schedule while a self-insert or a replaced background character watches. The
  engine fixes that with a **reactivity dial** (1 inert → 5 predatory), a **reaction profile** per
  antagonist — the patient strategist who studies you for ten chapters before moving, the chaotic
  who fixates on you next week for no strategic reason, the institution that opens a file and
  never forgets — and one hard rule: **every arc must move at least one world-track event.**
  It also carries a **governor** so that reactive never means hopeless (crisis cap, minimum
  reaction latency so you get to prepare, an opportunity opened for every escalation, wins that
  stick) and an **ending contract** recorded in your own words that the world is never permitted
  to make unreachable.

- **`mc-design`** runs the MC interview — gender, appearance, intellect, origin, and the central
  advantage (golden finger) — with a **"surprise me"** option on every question that generates
  three premise-derived options rather than rolling dice. It also owns the **form ledger**: if
  your MC is a reincarnator reborn as an infant, a transmigrator in someone else's body, or
  anything else that isn't their final form yet, `state/body.md` locks their description to the
  current stage. No adult height, presence or voice leaks backwards into the child, and the
  revision gate checks it on every chapter.
- **`lead-interest`** picks and builds the primary love interest, and runs *after* the MC is
  designed, because the lead is built as a counterweight to a specific person. Male MC defaults
  to a female lead; female MC defaults to a male lead **with a female lead equally on offer**;
  "decide later" is a first-class answer.

- **`character-profile`** tiers the cast, because profiling everyone the way you profile the MC is
  how a long serial runs out of context. Principals get the full file — Lie, ladder, eight speech
  fields, three calibration lines. Supporting characters get nine fields and **one shift** instead
  of five rungs. A walk-on — the toll clerk, the informant, the rival who dies next chapter — gets
  **three strokes on one roster line**: what they want in the next five minutes, one habit, and one
  piece of their working world. That third stroke is the whole trick; it is what makes an extra a
  window onto the world instead of a function in a scene, and it costs twenty-five words. Nobody is
  promoted in anticipation — a third appearance or a decision that changes the plot triggers a real
  profile, built retroactively from what is already on the page.

- **`continuity-summary`** maintains a compressed, machine-only ledger (one dense block per
  chapter, rolled up into arc digests and a book digest). It is deliberately unreadable to
  humans — it is context fuel, not a recap. This is what makes chapter 250 cheap to write.
- **`mc-intel-meter`** pins the MC at a declared intelligence tier (Ordinary → Genius) and
  enforces it in both directions: no unearned omniscience, and no idiot ball. Failure must come
  from missing information, opposed will, or cost.
- **`character-development`** gives every named character a five-rung arc ladder and a
  development rate, so a supporting character sounds different in chapter 200 than in chapter 20.
  The MC's rate is always maximum.

## Configuring

Everything user-tunable lives in the YAML frontmatter of `novels/<slug>/novel.md`. Edit it by
hand or via `/novel-toggle`. Optional skills read their own key and no-op if it is `off`.

## Scripts

[`scripts/sw.py`](scripts/README.md) — Python 3.8+, standard library only.

| command | what it does |
|---|---|
| `readset <novel> -c N` | assembles the bounded read-set for chapter N — sliced rows, not whole files |
| `lint <novel> [-c N \| --all]` | one chapter, or every chapter: MTL phrases, the AI-default cut list, the four channels, thought budget, apostrophe collisions, stray markup, frontmatter, anchor vocabulary |
| `arc <novel> [-a N]` | the distributional pass over one arc: dialogue trend, length spread, hooks, cast rotation, thread ops, anchor coverage |
| `cast <novel>` | the voice matrix and competence grid as tables: straddle, wit cap, three-way clash, expertise budget |
| `state <novel>` | ledger against chapters, required CCS lines, thread tension against last use, plan-row completeness, promotion triggers |
| `status <novel>` | progress aggregation for `/novel-status` |
| `stamp <novel> -c N` | measures the body, writes `wordcount:` and `status:` |
| `newnovel <slug>` | portable copy of `novels/_template` |
| `audit <novel>` | the independent whole-novel gate |
| `doctor` | environment and workspace check |

Exit `0` clean, `1` findings that need a decision, `2` bad usage. Findings print one per line as
`LEVEL path:line: [check] message`.

Three things they deliberately do not do. **They never edit a prose body** — `mtl-detox` requires
the sentence rewritten rather than the synonym swapped, so an auto-fixer would do precisely the
forbidden thing; linters report, the model rewrites. **There is no script for `bias-guard`**,
because its defects are distributional and a green line from a linter must never be readable as a
bias pass. And **a clean run is not a passed revision** — it means the mechanical passes found
nothing, and says nothing about delivery, voice separation, competence or bias.

## Layout

```
CLAUDE.md                         the operating contract, loaded every session
.claude/skills/<name>/SKILL.md    the skills
.claude/commands/*.md             the slash commands
.claude/settings.json             shared permissions (relative paths — portable)
scripts/sw.py                     the mechanical toolkit (optional, Python 3.8+)
novels/_template/                 the per-novel scaffold
novels/<slug>/                    your novel: config, bible, plan, state, chapters (gitignored)
```

See [CLAUDE.md](CLAUDE.md) for the full operating contract.
