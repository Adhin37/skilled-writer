"""The commands that change files.

All of them are deterministic bookkeeping. None touches a prose body: mtl-detox says to rewrite
the sentence rather than swap a synonym, so an auto-fixer would do the one thing the skill
forbids. Linters report; the model rewrites.
"""

import os
import re
import shutil

from . import mdio
from .report import Report
from .textstats import Chapter


# The frontmatter block, matched against the file exactly as it sits on disk: BOM kept,
# CRLF kept. Everything after group 2 is the prose body and is never touched.
_FM_RAW = re.compile(r"\A(\ufeff)?---[ \t]*\r?\n(.*?\r?\n)---[ \t]*\r?\n?", re.S)


def _set_field(fm, name, value, changes):
    """Replace or append one `name: value` line. Operates on LF-normalised text."""
    new, n = re.subn(r"(?m)^%s:.*$" % name, "%s: %s" % (name, value), fm)
    if n == 0:
        return fm.rstrip("\n") + "\n%s: %s\n" % (name, value), changes + [
            "added %s: %s" % (name, value)]
    if new != fm:
        old = re.search(r"(?m)^%s:\s*(\S+)" % name, fm)
        return new, changes + ["%s %s -> %s" % (name, old.group(1) if old else "?", value)]
    return new, changes


def stamp(novel, number, status=None, sync_ledger=False):
    """Measure the body and write `wordcount:` (and optionally `status:`) into frontmatter.

    Only the frontmatter block is rewritten. The body goes back byte for byte, with the file's
    own line endings, because a bookkeeping command that silently reflows someone's prose is a
    worse bug than the wrong word count it was fixing.
    """
    rep = Report("stamp - %s" % novel.title)
    ch = novel.chapter(number)
    if ch is None:
        rep.defect("usage", "no chapter file numbered %d" % number)
        return rep, False

    raw, newline, decoded = mdio.read_text_raw(ch.path)
    if not decoded:
        rep.defect("encoding", "chapter %d is not valid UTF-8 - refusing to rewrite it, "
                               "because saving it back would replace the bad bytes with U+FFFD"
                   % number, path=ch.path)
        return rep, False

    m = _FM_RAW.match(raw)
    if not m:
        rep.defect("frontmatter", "chapter %d has no frontmatter to stamp" % number,
                   path=ch.path)
        return rep, False

    bom = m.group(1) or ""
    fm = m.group(2).replace("\r\n", "\n").replace("\r", "\n")
    body_raw = raw[m.end():]

    measured = len(body_raw.split())
    changes = []

    new_fm, changes = _set_field(fm, "wordcount", measured, changes)
    if status:
        new_fm, changes = _set_field(new_fm, "status", status, changes)

    wrote = False
    if changes:
        out = bom + "---" + newline + new_fm.replace("\n", newline) + "---" + newline + body_raw
        with open(ch.path, "w", encoding="utf-8", newline="") as fh:
            fh.write(out)
        wrote = True

    if sync_ledger:
        block = novel.block(number)
        lpath = novel.path("state", "continuity.md")
        if block and block.wc is not None and block.wc != measured:
            ltext, lnl, lok = mdio.read_text_raw(lpath)
            if not lok:
                rep.defect("encoding", "state/continuity.md is not valid UTF-8", path=lpath)
                return rep, wrote
            lines = ltext.replace("\r\n", "\n").replace("\r", "\n").split("\n")
            idx = block.line_no - 1
            lines[idx] = re.sub(r"\bwc:\d+", "wc:%d" % measured, lines[idx])
            with open(lpath, "w", encoding="utf-8", newline="") as fh:
                fh.write(lnl.join(lines))
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
