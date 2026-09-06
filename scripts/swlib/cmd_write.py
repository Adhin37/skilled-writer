"""The two commands that change files.

Both are deterministic bookkeeping. Neither touches a prose body: mtl-detox says to rewrite
the sentence rather than swap a synonym, so an auto-fixer would do the one thing the skill
forbids. Linters report; the model rewrites.
"""

import os
import re
import shutil

from . import mdio
from .report import Report
from .textstats import Chapter


def stamp(novel, number, status=None, sync_ledger=False):
    """Measure the body and write `wordcount:` (and optionally `status:`) into frontmatter."""
    rep = Report("stamp - %s" % novel.title)
    ch = novel.chapter(number)
    if ch is None:
        rep.defect("usage", "no chapter file numbered %d" % number)
        return rep, False

    text = mdio.read_text(ch.path)
    fm, body = mdio.split_frontmatter(text)
    if not fm:
        rep.defect("frontmatter", "chapter %d has no frontmatter to stamp" % number,
                   path=ch.path)
        return rep, False

    measured = len(body.split())
    changes = []

    new_fm, n = re.subn(r"(?m)^wordcount:.*$", "wordcount: %d" % measured, fm)
    if n == 0:
        new_fm = fm.rstrip("\n") + "\nwordcount: %d" % measured
        changes.append("added wordcount: %d" % measured)
    elif new_fm != fm:
        old = re.search(r"(?m)^wordcount:\s*(\S+)", fm)
        changes.append("wordcount %s -> %d" % (old.group(1) if old else "?", measured))

    if status:
        new_fm2, n2 = re.subn(r"(?m)^status:.*$", "status: %s" % status, new_fm)
        if n2 == 0:
            new_fm2 = new_fm.rstrip("\n") + "\nstatus: %s" % status
            changes.append("added status: %s" % status)
        elif new_fm2 != new_fm:
            old = re.search(r"(?m)^status:\s*(\S+)", new_fm)
            changes.append("status %s -> %s" % (old.group(1) if old else "?", status))
        new_fm = new_fm2

    wrote = False
    if changes:
        with open(ch.path, "w", encoding="utf-8", newline="\n") as fh:
            fh.write("---\n" + new_fm + "\n---\n" + body)
        wrote = True

    if sync_ledger:
        block = novel.block(number)
        lpath = novel.path("state", "continuity.md")
        if block and block.wc is not None and block.wc != measured:
            ltext = mdio.read_text(lpath)
            lines = ltext.split("\n")
            idx = block.line_no - 1
            lines[idx] = re.sub(r"\bwc:\d+", "wc:%d" % measured, lines[idx])
            with open(lpath, "w", encoding="utf-8", newline="\n") as fh:
                fh.write("\n".join(lines))
            changes.append("ledger =C%04d= wc:%d -> wc:%d" % (number, block.wc, measured))
            wrote = True

    rep.info("chapter %d" % number, [
        "   %s" % ch.path.replace(os.sep, "/"),
        "   body measures %d words" % measured,
        "   " + ("; ".join(changes) if changes else "already correct - nothing written"),
    ])
    return rep, wrote


def newnovel(slug, repo_root="."):
    """Copy novels/_template to novels/<slug>. Portable stand-in for `cp -r`."""
    rep = Report("newnovel")
    if not re.match(r"^[a-z0-9][a-z0-9-]*$", slug):
        rep.defect("usage", "slug must be kebab-case: lowercase letters, digits and hyphens")
        return rep, False
    src = os.path.join(repo_root, "novels", "_template")
    dst = os.path.join(repo_root, "novels", slug)
    if not os.path.isdir(src):
        rep.defect("scaffold", "template not found at %s" % src)
        return rep, False
    if os.path.exists(dst):
        rep.defect("scaffold", "novels/%s already exists - refusing to overwrite" % slug)
        return rep, False

    shutil.copytree(src, dst)
    created = []
    for root, _dirs, files in os.walk(dst):
        for f in sorted(files):
            rel = os.path.relpath(os.path.join(root, f), dst).replace(os.sep, "/")
            created.append(rel)
    rep.info("created novels/%s" % slug, ["   " + c for c in created])
    rep.info("next", [
        "   1. fill novels/%s/novel.md - every frontmatter field, no placeholders" % slug,
        "   2. bible/, then plan/, then state/ - novel-init step 3 has the order",
        "   3. novels/ is gitignored except the template; your book is not committed",
    ])
    return rep, True
