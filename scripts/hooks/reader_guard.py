#!/usr/bin/env python3
"""PreToolUse guard for the `reader` agent: chapters and the procedure, nothing else.

`roles/review/reader-review.md` is built on one claim - that a reader who has not seen what the novel
*intended* can see things no instrument can, because every instrument in the repo reads the
novel with the bible open. That claim is only worth as much as the reader's blindness, and until
now the blindness was a list of directories in a prompt.

This is the mechanical half. An allowlist, not a blocklist: a blocklist has to predict every
route into `bible/`, and the reader only ever has business in two places.

Contract: hook input as JSON on stdin, exit 2 to block with the reason on stderr, exit 0 to
allow. Stdlib only, like everything else here. Fails **open** on a malformed payload - a guard
that crashes the reader teaches you to remove the guard, and the prompt list is still in place.

Wired from `.claude/agents/reader.md`. Frontmatter hooks need workspace trust, so treat this as
defence in depth rather than a wall: the `do not open` table in the agent body stays.
"""

import json
import os
import re
import sys

# Anything the reader may look at. Everything else is a block.
#
# Checked before REASONS, which is load-bearing rather than incidental: the brief lives at
# `roles/review/reader-brief.md`, inside the tree the corpus rule below denies wholesale. The
# reader's own instructions would otherwise be refused, and the `$` anchor is what keeps
# everything else in that directory on the far side of the line.
#
# **The brief, not `reader-review.md`.** That file is the maintainer's procedure and it names what
# the exercise is for - numbered runs, the write-up, the routing of findings to owners. A reader
# that has read it knows the chapters are being measured, which is the one thing the role exists
# to not know. Splitting the verdict out was the first half of this; splitting the *framing* out
# is the second, and it was only visible by inspecting a live reader's context.
ALLOW = (
    re.compile(r"(^|/)novels/[^/]+/chapters(/|$)"),
    re.compile(r"(^|/)roles/review/reader-brief\.md$"),
)

# Why each denial exists, so the reader is told rather than merely stopped.
#
# **A reason may justify a denial without describing what is behind the door.** These strings are
# the ones a reader actually sees, at the moment it is paying most attention - and they used to
# say "another reader's verdict and findings" and "the rules the chapters were written against",
# which between them told a blind reader that the chapters were machine-made to a rubric and had
# been graded before. Measured 2026-09-20 by inspecting a live `reader`'s context. Each reason
# still carries a distinct keyword, because two rules that produce the same words are two rules a
# test cannot tell apart.
REASONS = (
    (re.compile(r"(^|/)(bible|plan|state)(/|$)"),
     "that is what the novel intended. Knowing the intent repairs the prose silently, in your "
     "head, exactly where the defect is"),
    (re.compile(r"reader-review-example|benchmark|test-run-protocol"),
     "that already reports on these chapters, and you would find the same things and believe "
     "you had found them yourself"),
    (re.compile(r"(^|/)(\.claude|roles)(/|$)"),
     "that is about how the book was made rather than about what is on the page"),
    (re.compile(r"(^|/)novel\.md$"),
     "that is the novel's setup, not its pages"),
)


def targets(payload):
    """Every path-shaped value in a tool call. Read takes file_path, Grep and Glob take path
    plus a pattern that can itself be a path, and a future tool will take something else - so
    scan the values rather than naming the keys."""
    ti = payload.get("tool_input") or {}
    if not isinstance(ti, dict):
        return []
    out = []
    for key in ("file_path", "path", "notebook_path", "pattern", "glob"):
        val = ti.get(key)
        if isinstance(val, str) and ("/" in val or val.endswith(".md")):
            out.append(val)
    return out


def verdict(path):
    norm = os.path.normpath(path).replace(os.sep, "/")
    if any(rx.search(norm) for rx in ALLOW):
        return None
    for rx, why in REASONS:
        if rx.search(norm):
            return why
    return ("you were given one directory to read. Everything else is context about the novel, "
            "and you are here because you do not have it")


def main():
    try:
        payload = json.loads(sys.stdin.read() or "{}")
    except (ValueError, TypeError):
        return 0
    for path in targets(payload):
        why = verdict(path)
        if why:
            sys.stderr.write(
                "Blocked: `%s` is not yours to open - %s.\n"
                "Read the chapters you were pointed at, and roles/review/reader-brief.md for "
                "what to do with them. If a finding needs a fact you do not have, that absence IS "
                "the finding: say so and move on.\n" % (path, why))
            return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
