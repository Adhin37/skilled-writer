# AGENTS.md

This repository is a skill toolkit for writing serialized webnovels. Agents working here should
read **[CLAUDE.md](CLAUDE.md)** first — it is the full operating contract and applies to every
agent regardless of harness.

## 30-second orientation

- Skills live in `.claude/skills/<name>/`. `SKILL.md` is the procedure; `references/*.md` holds
  examples, catalogues and long tables, opened only when the body says to.
- Slash commands live in `.claude/commands/*.md`.
- Stories live in `novels/<slug>/`. The scaffold is `novels/_template/`.
- `novels/<slug>/novel.md` is the per-novel config: genre, POV mode, MC intel tier,
  chapter length, and optional-skill toggles. Read it before doing anything.

## The one rule that matters most

Do not generate prose from memory of the conversation. Read the bounded state set
(`state/continuity.md`, `plan/chapters.md`, `state/threads.md`, the relevant `bible/cast/*.md`),
write the chapter, then write the state back. Consistency in a 400-chapter serial comes from
the files, not from context.

## If your harness has no skill system

Read `.claude/skills/write-chapter/SKILL.md` and follow its step list manually; it names every
other skill it needs and when.
