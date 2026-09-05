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

## Setup

Clone the repo and open it with [Claude Code](https://claude.com/claude-code). There is nothing
to install and no build step — the toolkit is markdown. Claude Code discovers `.claude/skills/`
and `.claude/commands/` automatically, and reads `CLAUDE.md` on every session.

```bash
git clone <this-repo> skilled-writer
cd skilled-writer
claude
```

Works on Windows, macOS and Linux. Nothing in the repo hardcodes a path, a drive or a shell:
`.claude/settings.json` uses project-relative permission rules, `.gitattributes` normalises line
endings to LF, and `.gitignore` keeps generated books, per-machine tool state and OS cruft out.

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

## The skills

**Core loop** — `novel-init`, `mc-design`, `story-bible`, `chapter-plan`, `continuity-summary`,
`write-chapter`, `revision-pass`

**World** — `story-bible`, `social-fabric`, `world-texture`

**Character** — `character-profile`, `voice-separation`, `character-development`, `mc-intel-meter`,
`dialogue-voice`, `lead-interest`

**Craft** — `narrator-voice`, `pov-switch`, `scene-craft`, `conflict-engine`, `plot-threads`,
`timeline-engine`, `hook-and-pacing`, `prose-quality`, `mtl-detox`, `bias-guard`

**Genre modules** — `power-system`, `tech-plausibility`, `fanfic-canon`

**Optional, toggled per novel** — `no-harem` (on by default), `romance-arc`,
`combat-choreography`, `litrpg-system`, `mystery-clues`, `comedy-levity`,
`grimdark-consequences`, `slice-of-life-texture`

Ten of these deserve a note:

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

## Layout

```
CLAUDE.md                         the operating contract, loaded every session
.claude/skills/<name>/SKILL.md    the skills
.claude/commands/*.md             the slash commands
.claude/settings.json             shared permissions (relative paths — portable)
novels/_template/                 the per-novel scaffold
novels/<slug>/                    your novel: config, bible, plan, state, chapters (gitignored)
```

See [CLAUDE.md](CLAUDE.md) for the full operating contract.
