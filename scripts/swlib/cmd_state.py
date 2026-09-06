"""`sw state` - integrity of the ledger, the thread board, the plan and the roster.

Covers continuity-summary's self-check, plot-threads' dropped-thread audit, chapter-plan's
row-completeness rule and character-profile's promotion trigger. All four are bookkeeping:
comparing what one file records against what another one does.
"""

import os
import re

from . import rules
from .report import Report

PLAN_REQUIRED = ["goal", "obstacle", "turn", "delivers", "cost", "hook"]
TENSION_WINDOW = {"hot": 5, "warm": 15}
BLANK = ("", "-", "—", "–", "n/a", "tbd", "?")


def _blank(val):
    return str(val).strip().strip("*").lower() in BLANK


def run(novel):
    rep = Report("state - %s" % novel.title)
    chapters = novel.chapters()
    blocks = novel.blocks()
    last_ch = max([c.number for c in chapters if c.number] or [0])

    rep.info("position", [
        "   %d chapter file(s), %d CCS block(s), %d plan row(s), %d thread(s)"
        % (len(chapters), len(blocks), len(novel.plan_rows()), len(novel.threads()))])

    _files(novel, rep)
    _ledger(novel, rep, chapters, blocks)
    _digest(novel, rep, blocks)
    _threads(novel, rep, blocks, last_ch)
    _plan(novel, rep, chapters, last_ch)
    _roster(novel, rep, last_ch)
    return rep


def _files(novel, rep):
    """The conditional state files novel.md implies."""
    if novel.has_foreknowledge and not os.path.isfile(novel.path("state", "foreknowledge.md")):
        rep.defect("state-files", "mc.foreknowledge is set but state/foreknowledge.md is "
                   "missing", path=novel.path("novel.md"))
    if novel.form_locked and not os.path.isfile(novel.path("state", "body.md")):
        rep.defect("state-files", "mc.form_locked is true but state/body.md is missing - no "
                   "sentence may describe a locked body without it", path=novel.path("novel.md"))


def _ledger(novel, rep, chapters, blocks):
    lpath = novel.path("state", "continuity.md")
    by_num = {}
    for b in blocks:
        if b.number in by_num:
            rep.defect("ledger", "two blocks numbered =C%04d=" % b.number, path=lpath,
                       line=b.line_no)
        by_num[b.number] = b

    for c in chapters:
        if c.number and c.number not in by_num:
            rep.defect("ledger", "chapter %d is on disk with no CCS block - a chapter written "
                       "without one is a bug" % c.number, path=lpath)
    for n, b in sorted(by_num.items()):
        if not any(c.number == n for c in chapters):
            rep.warn("ledger", "block =C%04d= has no chapter file" % n, path=lpath,
                     line=b.line_no)

    for n, b in sorted(by_num.items()):
        keys = b.keys()
        for req in rules.REQUIRED_CCS:
            if req not in keys:
                rep.defect("ccs", "block =C%04d= has no `%s>` line" % (n, req), path=lpath,
                           line=b.line_no)
        if "wld" not in keys:
            rep.warn("ccs", "block =C%04d= has no `wld>` line - omit it only if genuinely "
                     "nothing moved offstage" % n, path=lpath, line=b.line_no)
        # the fix the shell version never made: fk> is required once the MC knows the future
        if novel.has_foreknowledge and "fk" not in keys:
            rep.defect("ccs", "block =C%04d= has no `fk>` line, but mc.foreknowledge is set - "
                       "record the spend, or record that nothing was spent" % n,
                       path=lpath, line=b.line_no)
        if novel.form_locked and "bod" not in keys:
            rep.defect("ccs", "block =C%04d= has no `bod>` line, but a character is "
                       "form_locked" % n, path=lpath, line=b.line_no)
        if b.line_count > rules.CCS_MAX_LINES:
            rep.defect("ccs", "block =C%04d= runs %d lines; the cap is %d"
                       % (n, b.line_count, rules.CCS_MAX_LINES), path=lpath, line=b.line_no)

        dlv, ev = b.get("dlv").strip().lower(), b.get("ev").strip().lower()
        if dlv and ev and dlv[:50] == ev[:50]:
            rep.defect("ccs", "block =C%04d= has a `dlv>` that restates its `ev>` - that is a "
                       "chapter which changed nothing" % n, path=lpath, line=b.line_no)

        # the other fix: the wc: comparison the shell script silently never ran
        ch = next((c for c in chapters if c.number == n), None)
        if ch and b.wc is not None and b.wc != ch.words:
            rep.defect("ccs", "block =C%04d= records wc:%d, the body measures %d"
                       % (n, b.wc, ch.words), path=lpath, line=b.line_no)


def _digest(novel, rep, blocks):
    lpath = novel.path("state", "continuity.md")
    digest = novel.book_digest()
    if not digest.strip():
        rep.defect("digest", "the book digest is empty - it is read first and trusted most",
                   path=lpath)
        return
    done = ""
    for line in digest.split("\n"):
        if line.startswith("done>"):
            done = line
    if blocks and re.search(r"no chapters drafted|\(none", done, re.I):
        rep.defect("digest", "`done>` still says nothing is drafted, but %d block(s) exist - "
                   "every later read-set inherits this" % len(blocks), path=lpath)
    if blocks and not done:
        rep.warn("digest", "the book digest has no `done>` line", path=lpath)


def _threads(novel, rep, blocks, last_ch):
    tpath = novel.path("state", "threads.md")
    rows = novel.threads()
    declared = {}
    for r in rows:
        tid = r.first().strip().strip("*")
        if re.match(r"^T\d+", tid):
            declared[tid] = r

    last_seen = {}
    for b in blocks:
        for line in b.keys().get("thr", []):
            for tid in re.findall(r"[~^vx]?(T\d+)", line):
                last_seen[tid] = max(last_seen.get(tid, 0), b.number)

    for tid in sorted(last_seen):
        if tid not in declared:
            rep.defect("threads", "%s is operated on in the ledger but has no row in "
                       "state/threads.md" % tid, path=tpath)

    for tid, r in sorted(declared.items()):
        status = str(r.get("status", "")).strip().lower()
        tension = str(r.get("tension", "")).strip().lower()
        if status not in ("open", "escalated"):
            continue
        seen = last_seen.get(tid)
        if seen is None:
            opened = re.sub(r"\D", "", str(r.get("opened", ""))) or "?"
            if opened.isdigit() and int(opened) <= last_ch:
                rep.warn("threads", "%s is open, opened at ch %s, and no ledger block has ever "
                         "operated on it" % (tid, opened), path=tpath, line=r.line_no)
            continue
        window = TENSION_WINDOW.get(tension)
        if window and last_ch - seen > window:
            rep.defect("threads", "%s is declared `%s` but was last touched at ch %d, %d "
                       "chapters ago - re-tension it or pay it"
                       % (tid, tension, seen, last_ch - seen), path=tpath, line=r.line_no)

    # Ageing. plot-threads section Ageing: a promise past its `due` is the mechanism behind
    # perpetual deferral, which is the complaint readers actually drop long serials over.
    ages = []
    for tid, r in sorted(declared.items()):
        if str(r.get("status", "")).strip().lower() not in ("open", "escalated"):
            continue
        opened = re.sub(r"\D", "", str(r.get("opened", "")))
        due = re.sub(r"\D", "", str(r.get("due", "")))
        age = last_ch - int(opened) if opened.isdigit() else None
        if age is not None:
            ages.append((tid, age))
        if due.isdigit() and last_ch > int(due):
            carried = str(r.get("carried", "")).strip()
            level = rep.warn if carried else rep.defect
            level("threads", "%s is past its due chapter (%s, now ch %d)%s"
                  % (tid, due, last_ch,
                     " - carried: %s" % carried if carried
                     else " and carries no deferral reason - pay it, escalate it, or record why"),
                  path=tpath, line=r.line_no)

    # Did the last completed arc close anything on the page?
    arc_len = novel.arc_length
    if last_ch >= arc_len:
        closed = last_ch // arc_len * arc_len
        lo = closed - arc_len + 1
        paid = set()
        for b in blocks:
            if b.number is None or not (lo <= b.number <= closed):
                continue
            for line in b.keys().get("thr", []):
                paid.update(re.findall(r"v(T\d+)", line))
        if not paid:
            rep.defect("threads", "arc chapters %d-%d closed without paying a single thread - "
                       "an arc that only defers is how a serial loses readers "
                       "(plot-threads section Ageing)" % (lo, closed), path=tpath)

    open_count = sum(1 for r in rows
                     if str(r.get("status", "")).strip().lower() in ("open", "escalated"))
    oldest = ", ".join("%s %dch" % (t, a) for t, a in sorted(ages, key=lambda x: -x[1])[:5])
    rep.info("threads", [
        "   %d open/escalated; last touched: %s" % (
            open_count,
            ", ".join("%s@ch%d" % (t, c) for t, c in sorted(last_seen.items())) or "none"),
        "   oldest open: %s" % (oldest or "none"),
    ])


def _plan(novel, rep, chapters, last_ch):
    ppath = novel.path("plan", "chapters.md")
    rows = novel.plan_rows()
    if not rows:
        rep.defect("plan", "no chapter construction rows found", path=ppath)
        return

    planned_ahead = 0
    for r in rows:
        num = re.sub(r"\D", "", r.first())
        if not num:
            continue
        num = int(num)
        if num > last_ch:
            planned_ahead += 1
        if num <= last_ch + 3:
            missing = [c for c in PLAN_REQUIRED if _blank(r.get(c))]
            if missing:
                level = rep.defect if num <= last_ch + 1 else rep.warn
                level("plan", "row %d is missing %s - write-chapter will not draft from an "
                      "incomplete row" % (num, ", ".join(missing)), path=ppath, line=r.line_no)

    if planned_ahead < 8:
        rep.warn("plan", "only %d planned row(s) ahead of the draft line (ch %d) - "
                 "chapter-plan runs when fewer than 8 remain" % (planned_ahead, last_ch),
                 path=ppath)

    for c in chapters:
        r = novel.plan_row(c.number) if c.number else None
        if r is None:
            rep.warn("plan", "chapter %s is drafted but has no plan row" % c.number, path=ppath)
            continue
        pstatus = str(r.get("status", "")).strip().lower()
        cstatus = str(c.meta.get("status", "")).strip().lower()
        if pstatus and cstatus and pstatus != cstatus:
            rep.warn("plan", "row %d says `%s`, the chapter file says `%s`"
                     % (c.number, pstatus, cstatus), path=ppath, line=r.line_no)


def _roster(novel, rep, last_ch):
    """character-profile: a third appearance triggers a real profile."""
    epath = novel.path("bible", "cast", "_extras.md")
    text = novel._text("bible", "cast", "_extras.md")
    if not text:
        return
    have_files = set(k.lower() for k in novel.cast_files())
    for i, line in enumerate(text.split("\n"), 1):
        m = re.match(r"^([^—\n|#]{2,60}?)\s+—.*?—\s*ch\s+([0-9,\s~–\-()a-z]+?)\s*—", line)
        if not m:
            continue
        name = m.group(1).strip()
        appearances = []
        for part in m.group(2).split(","):
            nums = re.findall(r"\d+", part)
            if nums:
                appearances.append(int(nums[0]))
        actual = [a for a in appearances if a <= last_ch]
        if len(actual) >= 3:
            slug = re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")
            if slug not in have_files and name.lower() not in have_files:
                rep.defect("promotion", "%s has appeared %d times (ch %s) and is still a "
                           "walk-on - a third appearance triggers a real profile"
                           % (name, len(actual), ", ".join(str(a) for a in actual)),
                           path=epath, line=i)
