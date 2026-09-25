#!/usr/bin/env python3
"""PreToolUse guard: which role may READ what.

The write half of the role table is `write_scope.py`. This is the other half, and it is the one
that makes the physical split mean something. After the move there is no `SKILL.md` inside a role
tree to open by accident - but `.claude/skills/` still holds 44 bodies, `roles/gate/` still holds
36 files the drafter has no business in, and until now the only thing stopping either was a
sentence in `CLAUDE.md` §3 that a cooperating agent chose to obey.

**An allowlist for the drafter and the gate, a denylist for the architect**, and the difference
is not stylistic. The set of things a drafter legitimately opens is small and closed - its own
bucket, `shared/`, its dispatcher body, the novel - so an allowlist states it exactly. The set an
architect opens is open-ended by design: `design` reads every bucket and every body, and
enumerating that would produce a list that rots in the direction that gets guards switched off.
Two things are out of its reach - the cold-read rubric and the maintainer notes in `docs/` - so
two things are written down.

**ALLOW is consulted before DENIED, and that ordering is load-bearing.** `roles/draft/` matches
the "that belongs to another role" pattern, so a drafter reading its own bucket would be refused
with a message about somebody else's tree - which reads exactly like a correct block. Reversing
the two loops kills `test_a_role_reads_its_own_bucket`, by name.

**What this does not cover is `Bash`, and in this harness that is the main road, not a
footnote.** Measured 2026-09-20 by probing a live `drafter`, which is the only way to learn any
of it:

  - A subagent here has **no `Grep` and no `Glob`** - they are absent from its tool list, not
    merely scoped - so its only search is `grep` through `Bash`, which never reaches this hook.
    The `Grep|Glob` half of the matcher and the unrooted-search rule below are inert for the
    agents that matter, and are kept because another harness may hand them over.
  - In **auto mode the harness instructs every agent to prefer `Bash` for reading**: *"read files
    with cat, head, or sed -n ... rather than using the dedicated Read, Edit, or Write tools."*
    A drafter that follows that instruction opens an audit card with `cat` and this guard never
    runs. In the probe it arrived attached to a tool result, and the drafter obeyed the user's
    explicit "use the Read tool" over it - which is the only reason the probe measured anything.

So the honest claim is narrow, and narrower than the plan assumed. **Every `Read` an agent makes
is judged, and a deliberate `cat` is not.** It is still worth having for two reasons that do not
depend on being a wall: the four verdicts the probe exercised were exactly right, and the refusal
*names the card that sent the agent somewhere it should not be*, which is the defect worth
finding. The structural half of the job belongs to `sw health`'s partition check, which stops
such a card being written at all.

Extending this to `Bash` means pattern-matching command lines, and the failure mode runs the
wrong way: a guard that misreads a pipeline and refuses a legitimate `sw` call is a guard
somebody removes, and then nothing is guarded. If it is done, it should match a short list of
plain readers (`cat`, `head`, `sed -n`, `less`) against a denied tree and fail open on everything
else.

Contract: JSON on stdin, exit 2 blocks with the reason on stderr, exit 0 allows. Stdlib only.
Fails **open** on anything it does not understand - an unknown agent, an unparseable payload, a
tool call with no path in it. A guard that blocks work it was never meant to judge gets switched
off, and then it guards nothing.
"""

import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import reader_guard  # noqa: E402  (the reader's scope has one owner; see `verdict`)

# What each scoped role may open beyond COMMON. The architect is deliberately absent: it has no
# allowlist, only `ARCHITECT_DENIED` below.
ALLOW = {
    "drafter": (r"(^|/)roles/(draft|shared)(/|$)",
                r"(^|/)novels(/|$)",
                # The dispatcher bodies, which grant nothing new: both are already preloaded
                # through `skills:`. Naming them preserves the documented no-Python fallback -
                # `AGENTS.md` says to read the body and follow its step list by hand.
                r"(^|/)\.claude/skills/(write-chapter|continuity-summary)/SKILL\.md$"),
    "gate": (r"(^|/)roles/(gate|shared)(/|$)",
             r"(^|/)novels(/|$)",
             r"(^|/)\.claude/skills/revision-pass/SKILL\.md$"),
}

# Open to every role, deliberately and with the reason written down, because denial by omission
# here would break something documented.
#
#   scripts/ tests/    every skill that names an `sw` command keeps a manual checklist under it,
#                      and the fallback is to read the implementation when a command misbehaves.
#                      A checker's source is the rubric's *enforcement*, not the rubric: reading
#                      it is useless rather than dangerous, and refusing it would send whoever
#                      hits it to switch the guard off.
#   the root contracts already in the agent's context by preload. Refusing a file the harness
#                      handed it would be incoherent.
#   tool-results/      the harness's own copy of a tool output too long to show inline. Past
#                      ~30 KB a Bash result arrives as a 2 KB preview plus this path, and the
#                      read-set is past that by chapter 6 (46.7 KB, measured 2026-09-24). Refusing
#                      it pushed an agent that obeyed "use Read, not cat" straight onto `cat`, the
#                      one road this guard cannot see. It is the agent's own output, so reading it
#                      grants nothing - and the pattern is anchored on `tool-results/` so the
#                      auto-memory beside it under `.claude/projects/` stays out of reach.
COMMON = (r"(^|/)scripts(/|$)", r"(^|/)tests(/|$)", r"(^|/)(CLAUDE|AGENTS|README)\.md$",
          r"(^|/)\.claude/projects/.+/tool-results/[^/]+$")

# The cold-read rubric, denied to every role that is not the reader. It binds the architect too,
# and that is the point: a rubric the *novel* gets designed toward is no better than one the
# drafter writes toward, and `roles/review/reader-review.md` says so in its own second paragraph.
REVIEW = (r"(^|/)roles/review(/|$)",
          "that is the cold-read rubric, and a rubric anybody here can see is a rubric the book "
          "gets written toward. Its whole value is that the reader has not read it")

# `docs/` is six maintainer files addressed to the coordinator (`AGENTS.md`). It binds the
# architect as well as the drafter and gate: the architect invents every name in the novel, and
# `docs/benchmark.md` lists earlier runs' casts - which is how run #5's O1 house cast happened,
# through the corpus rather than through docs, and there is no reason to leave the second door.
DOCS = (r"(^|/)docs(/|$)",
        "those are maintainer notes about the toolkit, addressed to whoever edits it rather than "
        "to you. If a card sent you here, the card is the defect and reporting it is the fix")

# What the architect may not open. It has no allowlist - `design` reads every bucket and every
# body - so its whole scope is this short list of denials.
ARCHITECT_DENIED = (REVIEW, DOCS)

# Why a denial exists, so the role is told rather than merely stopped. Consulted only after
# ALLOW, so these never fire on a role's own tree.
DENIED = (
    REVIEW,
    DOCS,
    (r"(^|/)roles/(draft|gate|design)(/|$)",
     "that bucket belongs to another role. Yours is the one the read-set named, plus shared/"),
    (r"(^|/)\.claude/skills/[^/]+/SKILL\.md$",
     "a module is opened through its card, never its body - the body is for designing the thing "
     "and the card is for deciding it. `sw kb cards` and `sw kb passes` resolve yours"),
)

CATCHALL = ("you were given a bucket, a dispatcher and a novel. Everything else is context "
            "somebody else in the pipeline is responsible for")

# A search with no root starts at the repo root and reaches every tree there is, so an allowlist
# keyed on a path cannot see it. This is the accidental route the guard exists to close.
SEARCH = ("Grep", "Glob")
UNROOTED = ("a search with no `path` starts at the repo root and reads every role's tree. Pass "
            "`path` naming the tree you mean - yours, shared/, or the novel")


def targets(payload):
    """Every path-shaped value in a read-shaped tool call.

    `pattern` is included for `Glob`, where it is a path, and left alone for `Grep`, where it is
    a regex over file *contents* and a literal slash in it says nothing about what gets read.
    Grep's scope is its `path`, which is here, plus the unrooted rule above.
    """
    ti = payload.get("tool_input") or {}
    if not isinstance(ti, dict):
        return []
    keys = ["file_path", "path", "notebook_path"]
    if str(payload.get("tool_name") or "") == "Glob":
        keys.append("pattern")
    out = []
    for key in keys:
        val = ti.get(key)
        if isinstance(val, str) and val.strip():
            out.append(val)
    return out


def unrooted(payload):
    if str(payload.get("tool_name") or "") not in SEARCH:
        return False
    ti = payload.get("tool_input") or {}
    if not isinstance(ti, dict):
        return False
    return not str(ti.get("path") or "").strip()


def verdict(payload, path):
    """The reason this read is refused, or None to allow it."""
    if not payload.get("agent_id"):
        return None                          # the main session; the coordinator reads everything
    agent = str(payload.get("agent_type") or "").strip()
    if agent == "reader":
        # One owner. `reader_guard.py` holds the reader's scope and is wired from the agent file;
        # calling it from here means the reader is guarded by the settings hook as well, which is
        # the registration that does not depend on workspace trust. Copying its table instead
        # would be a second thing to maintain and a silent contradiction waiting to happen.
        return reader_guard.verdict(path)
    if agent != "architect" and agent not in ALLOW:
        return None                          # an agent this guard was not written for
    norm = os.path.normpath(path).replace(os.sep, "/")
    if agent == "architect":
        if any(re.search(rx, norm) for rx in COMMON):
            return None
        for rx, why in ARCHITECT_DENIED:
            if re.search(rx, norm):
                return why
        return None
    if any(re.search(rx, norm) for rx in ALLOW[agent] + COMMON):
        return None                          # FIRST, and the docstring says why
    for rx, why in DENIED:
        if re.search(rx, norm):
            return why
    return CATCHALL


def block(what, why):
    sys.stderr.write(
        "Blocked: %s - %s.\n"
        "If the work genuinely needs it, that is a finding about the card that sent you: report "
        "it and carry on with what you have.\n" % (what, why))
    return 2


def main():
    try:
        payload = json.loads(sys.stdin.read() or "{}")
    except (ValueError, TypeError):
        return 0
    for path in targets(payload):
        why = verdict(payload, path)
        if why:
            return block("`%s` is not yours to open" % path, why)
    if unrooted(payload) and payload.get("agent_id") and \
            str(payload.get("agent_type") or "").strip() in ALLOW:
        return block("this search is unscoped", UNROOTED)
    return 0


if __name__ == "__main__":
    sys.exit(main())
