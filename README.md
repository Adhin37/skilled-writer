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

**Character** — `character-profile`, `character-development`, `mc-intel-meter`, `dialogue-voice`,
`lead-interest`

**Craft** — `narrator-voice`, `pov-switch`, `scene-craft`, `conflict-engine`, `plot-threads`,
`timeline-engine`, `hook-and-pacing`, `prose-quality`, `mtl-detox`, `bias-guard`

**Genre modules** — `power-system`, `tech-plausibility`, `fanfic-canon`

**Optional, toggled per novel** — `no-harem` (on by default), `romance-arc`,
`combat-choreography`, `litrpg-system`, `mystery-clues`, `comedy-levity`,
`grimdark-consequences`, `slice-of-life-texture`

Seven of these deserve a note:

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
.claude/skills/<name>/SKILL.md    the skills
.claude/commands/*.md             the slash commands
novels/_template/                 the per-novel scaffold
novels/<slug>/                    your novel: config, bible, plan, state, chapters
```

See [CLAUDE.md](CLAUDE.md) for the full operating contract.
