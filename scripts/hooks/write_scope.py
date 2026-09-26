#!/usr/bin/env python3
"""PreToolUse guard: which role may write where under `novels/`.

The role table in `CLAUDE.md` §10 gives each role exactly one thing it writes - the architect
`bible/` `plan/` `novel.md` and the state seeds, the drafter `chapters/` `state/`, the gate edits
that chapter and writes its hand-back, the coordinator nothing during a test run. Until now every
one of those was a sentence in a document and held by goodwill, and `docs/test-run-protocol.md` §2
is the one whose violation voids a run: a benchmark where the coordinator repaired the output
measures the coordinator.

**Why this is a hook and not a `permissions.deny` rule.** Deny rules are global - they apply to
the main conversation *and* to subagents, and a subagent's `tools:` can only narrow what it
inherited, never re-grant it. So denying `Write(novels/**)` to stop the coordinator would stop
the drafter too, which is the one agent that must write there.

The discriminator is `agent_id`, which the harness puts in the hook payload for a subagent tool
call and omits for a main-thread one. Deliberately **not** `transcript_path` containing
`/subagents/`: that is how `sw trace` tells them apart in *finished* files, but the transcript is
written asynchronously and lags the live conversation, so it is the wrong source at hook time.

Contract: JSON on stdin, exit 2 blocks with the reason on stderr, exit 0 allows. Stdlib only.
Fails **open** on anything it does not understand - an unknown agent, a payload it cannot parse,
a path it cannot classify. A guard that blocks work it was never meant to judge gets removed, and
then it guards nothing.
"""

import json
import os
import re
import sys

NOVELS = re.compile(r"(^|/)novels/")

# What each role may write, and the sentence that says why it is the wrong hand for the rest.
#
# The architect also writes `state/`, except the brief. Its own procedures put it there and were
# refused until 2026-09-24: `novel-init` step 9 seeds the ledger, threads, growth, calendar, body
# and foreknowledge files before chapter 1 exists; `chapter-plan` sets the arc's band in
# `power.md` §6; the arc rollup writes digests into `continuity.md`. A design decision that
# happens to live in a state file is still a design decision. `state/brief.md` stays the
# drafter's: it is the approved plan for the chapter in progress. `state/gate.md` is the gate's
# hand-back, written once per chapter and copied from at step 5 (run #6, I4: the one hand-off that
# had no file lost a design item when the drafter died), so it is the gate's alone - a drafter
# that could edit it could rewrite what the gate said about its chapter.
SCOPE = {
    "architect": ((r"(^|/)novels/[^/]+/(bible|plan)(/|$)", r"(^|/)novels/[^/]+/novel\.md$",
                   r"(^|/)novels/[^/]+/state/(?!brief\.md$|gate\.md$)[^/]+$"),
                  "the architect decides what the story is. Chapters and the brief are written by "
                  "the drafter, from the plan you leave it, and the hand-back by the gate"),
    "drafter": ((r"(^|/)novels/[^/]+/chapters(/|$)",
                 r"(^|/)novels/[^/]+/state/(?!gate\.md$)"),
                "the drafter writes the chapter and the state. A bible fact you need and cannot "
                "find is a thing to report, not to add mid-draft, and the gate's hand-back is "
                "copied from, never edited"),
    "gate": ((r"(^|/)novels/[^/]+/chapters(/|$)", r"(^|/)novels/[^/]+/state/gate\.md$"),
             "the gate repairs the chapter it was given and writes its hand-back to "
             "state/gate.md. It does not move the state the chapter is checked against"),
}

# The gate has `Write` for its hand-back and nothing else: every chapter it touches already exists,
# and repairing one is an `Edit`. Keyed on the tool name, which the payload carries.
GATE_HANDBACK = r"(^|/)novels/[^/]+/state/gate\.md$"

# The coordinator's marker. Present -> a test run is under way and the main session writes no
# file under `novels/`. Absent -> an ordinary run, where editing a chapter on request is the job
# (`CLAUDE.md`: the protocol "does not apply to a normal run").
MARKER = ".test-run"


def targets(payload):
    """Every path-shaped value in a write-shaped tool call."""
    ti = payload.get("tool_input") or {}
    if not isinstance(ti, dict):
        return []
    out = []
    for key in ("file_path", "path", "notebook_path"):
        val = ti.get(key)
        if isinstance(val, str) and val:
            out.append(val)
    return out


def test_run_active(payload):
    cwd = payload.get("cwd") or os.environ.get("CLAUDE_PROJECT_DIR") or ""
    return bool(cwd) and os.path.exists(os.path.join(cwd, MARKER))


def verdict(payload, path):
    """The reason this write is refused, or None to allow it."""
    norm = os.path.normpath(path).replace(os.sep, "/")
    if not NOVELS.search(norm):
        return None                      # outside the novel tree; not this guard's business
    agent = str(payload.get("agent_type") or "").strip()
    if not payload.get("agent_id"):
        if not test_run_active(payload):
            return None                  # ordinary run: the main session may edit on request
        return ("this is the coordinator and a test run is active. You approve the brief and "
                "route the roles; you write nothing under novels/. A run where the coordinator "
                "repaired the output measures the coordinator")
    allowed = SCOPE.get(agent)
    if allowed is None:
        return None                      # an agent this guard was not written for
    if not any(re.search(rx, norm) for rx in allowed[0]):
        return allowed[1]
    if (agent == "gate" and payload.get("tool_name") == "Write"
            and not re.search(GATE_HANDBACK, norm)):
        return ("the gate repairs a chapter with Edit and uses Write for its hand-back only. A "
                "gate that can rewrite a chapter whole can replace it instead of repairing it")
    return None


def main():
    try:
        payload = json.loads(sys.stdin.read() or "{}")
    except (ValueError, TypeError):
        return 0
    for path in targets(payload):
        why = verdict(payload, path)
        if why:
            sys.stderr.write(
                "Blocked: `%s` is not yours to write - %s.\n"
                "Report what needs changing there and let the role that owns it make the "
                "change.\n" % (path, why))
            return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
