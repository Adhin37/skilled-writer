# AGENTS.md

This repository is a skill toolkit for writing serialized webnovels. Agents working here should
read **[CLAUDE.md](CLAUDE.md)** first — it is the full operating contract and applies to every
agent regardless of harness.

## 30-second orientation

- Skills live in `.claude/skills/<name>/`. `SKILL.md` is the procedure; `references/*.md` holds
  examples, catalogues and long tables, opened only when the body says to.
- Two kinds of reference are load-bearing. A **draft card** makes one decision in Phase A; an
  **audit card** checks one thing in the gate. Modules are reached through their cards, never
  through their `SKILL.md` — the body is for designing the thing, the card for deciding it.
- Slash commands live in `.claude/commands/*.md`.
- Stories live in `novels/<slug>/`. The scaffold is `novels/_template/`.
- `novels/<slug>/novel.md` is the per-novel config: genre, POV mode, MC intel tier, channels,
  and optional-skill toggles. Read it before doing anything.
- `scripts/sw.py` is a stdlib-only Python 3.8+ program that does the countable work. It is an
  optimisation, never a dependency: every skill that names a command keeps its manual checklist
  underneath.

## The one rule that matters most

Do not generate prose from memory of the conversation. Load the bounded read-set, write the
chapter, then write the state back. Consistency in a 400-chapter serial comes from the files, not
from context.

```bash
python3 scripts/sw.py readset novels/<slug> -c <N>
```

That is the whole read-set in one call — config, the modules live for this novel, the ledger
blocks and plan rows in range, open threads, the cast rows for this chapter's speakers, the world
clock, and what the gate keeps having to fix. **Do not open the source files for anything it
contains**, and a module it does not list is off for this novel. Without Python, the list it
assembles is written out in `continuity-summary`, and you say in the report that you did it by
hand.

Afterwards: one CCS block appended to `state/continuity.md`, plus `state/threads.md`,
`state/growth.md`, `state/timeline.md`, and `state/body.md` on a form change. A chapter written
without this is a bug.

## Three things that surprise people

- **The gate is not a command.** `revision-pass` is Phase C of `write-chapter` and runs on every
  chapter before anything is reported. There is no `/novel-revise`, and a chapter is never handed
  back at `status: drafted`.
- **Nothing scores a chapter by a number.** Word count and dialogue share were both tried as ship
  gates and both were optimised rather than satisfied. Every measurement is reported and gates
  nothing; findings that are only meaningful in aggregate are counted across chapters and raised
  as a *habit*, never as a per-chapter verdict.
- **One concept, one owner.** Every skill declares `metadata.owns:` in frontmatter, and the claim
  is exclusive. State the rules you own; for everything else, cite the owner by name and stop.
  `python3 scripts/sw.py kb owner <slug>` answers "whose rule is this?" without opening anything.
  `sw health` fails a skill that copies or paraphrases another's rule instead of citing it.

## Before you commit a change to the toolkit

```bash
python3 -m unittest discover tests   # 382 tests
python3 scripts/sw.py health         # wiring, scope claims, duplication, the budgets
python3 scripts/sw.py selftest       # builds a novel in a temp dir; proves every check fires
```

## If your harness has no skill system

Read `.claude/skills/write-chapter/SKILL.md` and follow its step list manually; it names every
other skill it needs and when.
