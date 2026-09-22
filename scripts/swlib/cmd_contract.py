"""`sw contract <role>` - one role's slice of the operating contract, rendered.

One source, N rendered artifacts. `CLAUDE.md` stays the only place a rule is written; this cuts
it down to what a given role is actually bound by and writes the result into that role's agent
file, between markers. `cmd_health._contract()` re-renders and diffs, so a hand edit inside the
markers is a defect rather than a divergence nobody notices.

**Why the agent file and not a nested `CLAUDE.md`.** The plan called for
`roles/<bucket>/CLAUDE.md` plus `omitClaudeMd: true`. Claude Code loads a subdirectory's
`CLAUDE.md` *on demand* - "instead of loading them at launch, they are included when Claude reads
files in those subdirectories" - and a subagent starts in the main conversation's working
directory, which is the repo root. So a `CLAUDE.md` placed in `roles/draft/` would always be in the on-demand class: a
drafter with `omitClaudeMd: true` would begin Phase A with no contract at all and pick one up
only after its first card read. An agent file's body is the system prompt and is there at
startup, which is the property the contract needs.

**Sections, not rules.** The binding table is keyed on `## N.` and nothing finer, because a
finer table is one that rots: a rule added to §4 next month would need an entry, and the entry
would be forgotten. Distinctions inside a section are stated *inline* in `CLAUDE.md` instead -
§4.3 says in as many words that `design` adds a bible fact and `draft` reports it - which is the
pattern §10's own role table already uses.

**Order is source order, and that is worth keeping.** The rendered block runs §1 → §9 as
`CLAUDE.md` writes them, which puts the hard rules and what-good-looks-like in the middle and the
mechanical-toolkit reference last. Nothing here depends on that, but if anything ever truncates a
long prompt, the part lost first is the one a drafter can most afford to lose. Reordering
`CLAUDE.md` would quietly give that up.

**The default is "this binds you".** `CONTRACT_EXCLUDES` lists only what a role does not get, so
a new section reaches every role until somebody decides otherwise. That is the failure direction
to want: a rule wrongly carried costs a few hundred words, and one wrongly dropped costs a
chapter.
"""

import os
import re

from . import kb, mdio, rules

# Which agent file carries each role's contract. `review` is deliberately absent: the reader's
# blindness IS its enforcement, and a rendered contract would be the rubric it must not have.
# `coordinate` is the main session, which loads `CLAUDE.md` whole.
ROLE_AGENT = {"draft": "drafter", "gate": "gate", "design": "architect"}

# Agents that must not inherit the project's instructions, and the reason each one must not. A
# rendered contract and `omitClaudeMd: true` are a **pair**: the flag without the contract leaves
# an agent with no rules, and the contract without the flag hands it the same rules twice.
#
# `reader` carries no contract and is here for the other half of what the flag does. Measured
# 2026-09-20 by inspecting two live subagents: one with the flag received neither `CLAUDE.md` nor
# the auto-memory index, and one without it received both. The docs list auto memory nowhere in
# the subagent startup set, so this is the only evidence there is - and for the reader it is the
# difference between a cold read and one that arrived knowing what previous runs were criticised
# for. Nothing else in this repo can reach that channel: it is not a tool call, so no hook sees it.
OMIT_CLAUDE_MD = {
    "drafter": "it carries a rendered contract, and without this it receives that contract twice",
    "gate": "it carries a rendered contract, and without this it receives that contract twice",
    "architect": "it carries a rendered contract, and without this it receives that contract "
                 "twice",
    "reader": "its whole value is not having read the rubric, and this is also the only thing "
              "that keeps the auto-memory index out of a cold read",
}

SOURCE = "CLAUDE.md"
BEGIN = "<!-- BEGIN GENERATED CONTRACT: sw contract %s -->"
END = "<!-- END GENERATED CONTRACT -->"
HEADING = re.compile(r"(?m)^## +(\d+)\. +(.*)$")


def sections(text):
    """`(number, body)` for each `## N.` section of the source, in order.

    The preamble is not returned at all. It is addressed to whoever opened the repo - what the
    toolkit is, and the instruction to read `docs/test-run-protocol.md` before a benchmark - and
    that instruction binds the coordinator and names a file two of the three roles may not open.
    """
    hits = list(HEADING.finditer(text))
    out = []
    for i, m in enumerate(hits):
        end = hits[i + 1].start() if i + 1 < len(hits) else len(text)
        out.append((m.group(1), text[m.start():end].rstrip() + "\n"))
    return out


def render(repo_root, role):
    """The contract block for `role`, markers included."""
    if role not in ROLE_AGENT:
        raise KeyError(role)
    src = mdio.read_text(os.path.join(repo_root, SOURCE))
    drop = tuple(rules.CONTRACT_EXCLUDES.get(role, ()))
    kept, left = [], []
    for number, body in sections(src):
        (left if number in drop else kept).append((number, body))
    if not kept:
        raise ValueError("%s: every section excluded" % role)

    lines = [BEGIN % role, "",
             "## The operating contract — the `%s` role's slice" % role, "",
             "Generated from `%s` by `python3 scripts/sw.py contract %s --write`. **Do not edit "
             "between the markers**; edit `%s` and re-run it, which `sw health` checks."
             % (SOURCE, role, SOURCE), ""]
    if left:
        lines += ["Left out because it does not bind you, and named so you know it exists rather "
                  "than thinking it does not: %s. It is in `%s`, which the coordinator and the "
                  "maintainer read."
                  % (", ".join("§%s" % n for n, _b in left), SOURCE), ""]
    lines += ["---", ""]
    for _number, body in kept:
        lines.append(body)
    lines += [END, ""]
    return "\n".join(lines)


# A `§N` pointer inside the contract body. Named sections (`§How hard each of these binds`,
# `hook-and-pacing` §Openings) are deliberately not matched: only a number can name a section this
# renderer might have dropped.
CROSSREF = re.compile(r"§(\d+)")


def dangling(repo_root, role):
    """`§N` pointers in a role's slice that name a section the role was not given.

    A cross-reference is fine in `CLAUDE.md`, where every section is present, and becomes a
    pointer into nothing the moment a slice is cut - and the role cannot follow it even in
    principle, because `role_scope.py` refuses it `CLAUDE.md`. Found 2026-09-22 by asking a live
    drafter what it held: three sentences in its own contract pointed at §8 and §10 as though
    they were in front of it.

    The generated header is skipped on purpose. Its omissions line *names* §7, §8 and §10, which
    is the one place in the file those numbers should appear - telling a role what it does not
    have is the opposite of pointing it at something it cannot read.
    """
    drop = set(rules.CONTRACT_EXCLUDES.get(role, ()))
    if not drop:
        return []
    body = render(repo_root, role)
    first = HEADING.search(body)
    if first is None:
        return []
    out = []
    for m in CROSSREF.finditer(body, first.start()):
        if m.group(1) not in drop:
            continue
        line = body.count("\n", 0, m.start())
        out.append((m.group(0), body.split("\n")[line].strip()))
    return out


def agent_path(repo_root, role):
    return os.path.join(repo_root, ".claude", "agents", ROLE_AGENT[role] + ".md")


def current(repo_root, role):
    """The block the agent file carries today, or None if it carries none."""
    path = agent_path(repo_root, role)
    if not os.path.isfile(path):
        return None
    text = mdio.read_text(path)
    begin = BEGIN % role
    if begin not in text or END not in text:
        return None
    start = text.index(begin)
    end = text.index(END, start) + len(END)
    return text[start:end] + "\n"


def write(repo_root, role):
    """Replace the block in place, or append it. Returns (path, changed)."""
    path = agent_path(repo_root, role)
    text = mdio.read_text(path)
    block = render(repo_root, role)
    begin = BEGIN % role
    if begin in text and END in text:
        start = text.index(begin)
        end = text.index(END, start) + len(END) + 1
        new = text[:start] + block + text[end:]
    else:
        new = text.rstrip("\n") + "\n\n" + block
    if new == text:
        return path, False
    with open(path, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(new)
    return path, True


def run(repo_root, args):
    role = args.role
    if role not in ROLE_AGENT:
        print("no contract for role %r - the roles with one are %s"
              % (role, ", ".join(sorted(ROLE_AGENT))))
        print("`review` has none on purpose: a reader that has read the rubric is not a reader.")
        return 2
    if not getattr(args, "write", False):
        print(render(repo_root, role), end="")
        return 0
    path, changed = write(repo_root, role)
    rel = os.path.relpath(path, repo_root).replace(os.sep, "/")
    words = len(render(repo_root, role).split())
    whole = len(mdio.read_text(os.path.join(repo_root, SOURCE)).split())
    print("%s  %s  (%d words of %d in %s)"
          % ("wrote  " if changed else "current", rel, words, whole, SOURCE))
    return 0


def roles_with_contracts():
    return sorted(ROLE_AGENT)


assert set(ROLE_AGENT) <= set(kb.ROLES), "a contract for a role the index does not know"
