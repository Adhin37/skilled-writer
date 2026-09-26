---
description: Draft the next chapter (or a specified one) and update all state
argument-hint: "[chapter number] [or: 'next 3', or a range to re-gate] [--no-confirm]"
---

Write chapter prose.

Resolve the active novel (CLAUDE.md §1). You are the **coordinator**: you run the loop below, relay
the brief for approval, and summon each role in turn. You do not write the chapter yourself, and
during a test run you write no file under `novels/` at all.

**Drafting is three phases, and this command runs all three.** Phase A produces a thirteen-line
brief and stops for approval — the cheapest gate in the toolkit, because a chapter that was going
to be a thousand words of somebody quietly feeling something gets caught for thirteen lines
instead of after the draft. Phase B drafts. Phase C runs `revision-pass` in the `gate` agent, a
context that has not watched the chapter being written. **The chapter is not reported until the
gate passes and its state is written** — there is no later command.

## The loop, one chapter

Every spawn carries the same prompt — `Novel slug: <slug>. Chapter: <N>.` — and a
`description` of the form **`draft ch N`**, **`gate ch N`** or **`fold ch N`**. The
description is not decoration: `sw trace` bills each agent to the chapter its description names,
and that is the only way a run split across agents can be measured per chapter.

1. **Spawn the `drafter`** (`draft ch N`). It runs step 0 and Phase A, writes `state/brief.md` as
   `status: proposed`, and returns **`BRIEF READY`** with the brief.
2. **Get the brief approved.** Show it to the user; relay the answer with `SendMessage` to the same
   drafter — "approved", or the lines to change. In a test run, approve it as written unless it
   breaks a hard rule (`docs/test-run-protocol.md` §3), and log both directions verbatim.
3. The drafter drafts and returns **`READY FOR GATE`** with the chapter path.
4. **Spawn the `gate`** (`gate ch N`) with **`run_in_background: false`** — your next step depends
   on it. It returns a hand-back: the `Gate:` line, a `z4>` answer, `SENT BACK` or a pass, what it
   changed, and `For design:` items — and writes the same text to `state/gate.md`.
5. **Relay the hand-back verbatim** to the drafter with `SendMessage`.
   - `SENT BACK`: the drafter redrafts the scene, returns `READY FOR GATE`, and you go back to 4.
   - A pass: the drafter writes state back (step 5), stamps the chapter `revised`, and returns the
     eight-line report.
6. **If the report's `Bible:` line is not `none`**, spawn the `architect` (`fold ch N`) with that
   line verbatim. It folds the facts into `bible/`, promotes walk-ons, and amends plan rows. Do it
   before the next chapter's Phase A, which reads what it writes.
7. Relay the report. Do not paste the chapter into the conversation. Lead with the event, never a
   word count. **Relay the fold's report too** — what it changed, what it declined, and any story
   decision it made that nobody asked for. Those are the user's to overrule, and a fold that
   answers to nobody decides the book in silence (benchmark run #6: a fold resolved who a thread's
   culprits were and when the arc's gain and loss land, and the decisions reached no one).

**When a message goes astray.** If a gate result lands in your conversation instead of the
drafter's, relay it with `SendMessage` — do not act on it yourself. If the drafter is gone (a
session limit, an error), spawn a new one with the same prompt and description. Its read-set prints
a **RESUME** line read off the disk — brief proposed or approved, chapter `drafted`, `gating`,
`gated` or `revised`, block written or not — and it restarts from there. At step 5 the hand-back is
on file in `state/gate.md`, and the RESUME line says whether it is this chapter's; if it is not
and the drafter asks, send it, and if you no longer have it either, run the gate again. A chapter
at `gating` is one a gate began and did not finish: run the gate again.

**Warm or cold.** Every chapter spawns a fresh drafter by default. Continuing the last chapter's
drafter with `SendMessage` (the same spawn prompt, the next chapter number) is an option, not the
default. Benchmark run #6 measured one warm chapter against one cold: drafter model time 755 s
against 1,531 s, zero draft cards re-opened, and a gate that changed nothing. That is one chapter,
and run #4's five warm chapters opened five cards between them, so it stays an option until a run
measures more than one.

**If an agent is unavailable.** In a normal run, run the phase inline and say so in the report —
the phases and the gate are unchanged, only the isolation is lost. In a test run, stop and log it:
a coordinator who drafted or gated has measured itself.

## Arguments

Interpret `$ARGUMENTS`:

- empty → the next unwritten chapter
- a number → that chapter. **If it already exists, ask which**: re-gate it or redraft it from the
  plan row. Never overwrite without asking. A re-gate is steps 4–5 of the loop: the gate, then a
  drafter spawned to stamp the chapter and update its block's `gate>` line.
- a range like `40-45` → re-gate each existing chapter in turn, finishing one completely —
  including its stamp — before starting the next, so an interruption leaves whole chapters behind
  it. Report once at the end.
- "next N" / "N chapters" → run the whole loop N times, **one chapter at a time**. Each brief is
  written after the previous chapter's state and fold have landed: a brief planned before chapter
  N−1 existed is planned against a ledger that is missing a chapter. Check in with the user after
  every 5.
- `--no-confirm` → the drafter writes the brief as `approved` and does not stop for approval. It
  does not skip Phase C.

Before step 1, confirm the plan row for the target chapter is complete — `event`, `temp`,
`hooktype`, goal/obstacle/turn/cost/hook, and for the opening arc its `world entry`. Those are
decided at plan time, not after. If any is
missing, have the architect run `chapter-plan` for that row first.
