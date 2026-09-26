"""`sw state` - integrity of the ledger, the thread board, the plan and the roster.

Covers continuity-summary's self-check, plot-threads' dropped-thread audit, chapter-plan's
row-completeness rule and character-profile's promotion trigger. All four are bookkeeping:
comparing what one file records against what another one does.
"""

import os
import re

from . import mdio, rules
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
    _sections(novel, rep)
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
    if novel.has_scaling and not os.path.isfile(novel.path("state", "power.md")):
        rep.defect("state-files", "scaling.shape is `%s` but state/power.md is missing - the "
                   "power curve cannot be tracked without it" % novel.scaling_shape,
                   path=novel.path("novel.md"))


def _sections(novel, rep):
    """Headings the read-set slices by, checked against THIS novel rather than the template.

    `sw health` has always checked these, and only ever against `novels/_template`. A live
    novel whose heading somebody renamed - or whose file an agent rewrote from memory - drops
    that section from every read-set it ever assembles, silently, and the read-set header
    tells the drafter not to open the source file for anything it lists. That is T7's shape:
    the failure is invisible precisely because the contract says not to go and look.

    A file that does not exist is not a finding here. Which files a novel owes is decided by
    its config, and `_files` above already answers that.
    """
    for parts, heading in rules.SECTION_LOOKUPS:
        path = novel.path(*parts)
        if not os.path.isfile(path):
            continue
        got = mdio.section(novel._text(*parts), heading)
        if not (got and got.strip()):
            rep.warn("sections",
                     "%s has no non-empty `%s` section - every read-set slices it by that "
                     "heading and drops it without saying so" % ("/".join(parts), heading),
                     path=path)


def _ledger(novel, rep, chapters, blocks):
    lpath = novel.path("state", "continuity.md")
    by_num = {}
    for b in blocks:
        if b.number in by_num:
            rep.defect("ledger", "two blocks numbered =C%04d=" % b.number, path=lpath,
                       line=b.line_no)
        by_num[b.number] = b

    # Sequence, not just content. `sw state` and `sw lint` both checked what a block *says*
    # and neither checked where it sat, so a block appended out of order passed both (run #4,
    # T5 - caught by a human re-reading the file). The ledger is read as a history: the CCS
    # rule is "one block per chapter, appended", and an arc digest is built by walking it in
    # order, so a block in the wrong place is a chapter that happened at the wrong time.
    numbers = [b.number for b in blocks if b.number is not None]
    out_of_order = [(prev, cur) for prev, cur in zip(numbers, numbers[1:]) if cur <= prev]
    for prev, cur in out_of_order:
        rep.defect("ledger", "block =C%04d= is written after =C%04d= - blocks are appended in "
                   "chapter order and read as a history. Move it, do not renumber it"
                   % (cur, prev), path=lpath,
                   line=next((b.line_no for b in blocks if b.number == cur), None))

    for c in chapters:
        if c.number and c.number not in by_num:
            rep.defect("ledger", "chapter %d is on disk with no CCS block - a chapter written "
                       "without one is a bug" % c.number, path=lpath)
    for n, b in sorted(by_num.items()):
        if not any(c.number == n for c in chapters):
            rep.warn("ledger", "block =C%04d= has no chapter file" % n, path=lpath,
                     line=b.line_no)

    cold = str(novel.get("tone.warmth") or "").strip().lower() == "cold"
    for n, b in sorted(by_num.items()):
        keys = b.keys()
        for req in rules.REQUIRED_CCS:
            if req not in keys:
                rep.defect("ccs", "block =C%04d= has no `%s>` line" % (n, req), path=lpath,
                           line=b.line_no)
        if "wld" not in keys:
            rep.warn("ccs", "block =C%04d= has no `wld>` line - omit it only if genuinely "
                     "nothing moved offstage" % n, path=lpath, line=b.line_no)
        # A rule satisfied by silence, three times over: until 2026-09-24 nothing asked whether
        # these lines were there at all, so run #5 shipped `cand>` on three blocks of five and
        # `gav>` on none, and `sw state` said nothing about either.
        missing = [k for k in rules.STEP_LINES if k not in keys and not (k == "gav" and cold)]
        if missing:
            rep.warn("ccs-steps", "block =C%04d= has no %s line - the literal `none` is a "
                     "legitimate entry; a missing line is a step nobody can prove ran"
                     % (n, " / ".join("`%s>`" % k for k in missing)),
                     path=lpath, line=b.line_no)
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
    # `plot-threads` owns the id format and documents it as `T01`, `T02`. The pattern here was
    # `^T\d+`, so benchmark run #5's ledger - which numbered its threads `TH01` - matched nothing,
    # `declared` came back empty, and every check below was skipped in silence while the summary
    # line above went on counting nine open threads. A parser whose input drifts must say so
    # rather than fall quiet, so the shape is read loosely and the drift is reported once.
    declared, odd = {}, []
    for r in rows:
        tid = r.first().strip().strip("*")
        if rules.THREAD_ID.match(tid):
            declared[tid] = r
            if not rules.THREAD_ID_CANON.match(tid):
                odd.append(tid)
    if odd:
        rep.warn("threads", "thread ids %s are not the `T01` form `plot-threads` documents - "
                 "they are read here, but every tool that greps for `T\\d+` will miss them"
                 % ", ".join(sorted(odd)[:6]), path=tpath)

    last_seen = {}
    for b in blocks:
        for line in b.keys().get("thr", []):
            for tid in rules.THREAD_ID_IN_TEXT.findall(line):
                last_seen[tid] = max(last_seen.get(tid, 0), b.number)

    # Benchmark run #6 (D2): the plan named `~T1`...`~T8` and no file mapped an id to a thread -
    # the drafter inferred the mapping from the order of names in a paragraph of threads.md, and
    # one later brief gave a reserved id to a different thread. An id a plan row uses has a row,
    # `planned` until the chapter that opens it.
    plan_missing = {}
    for pr in novel.plan_rows():
        for tid in rules.THREAD_ID_IN_TEXT.findall(str(pr.get("threads", ""))):
            if tid not in declared and tid not in plan_missing:
                plan_missing[tid] = re.sub(r"\D", "", pr.first()) or "?"
    for tid, rownum in sorted(plan_missing.items()):
        rep.warn("threads", "plan row %s names %s, which has no row in state/threads.md - declare "
                 "it there as `planned`, opened at the chapter that opens it" % (rownum, tid),
                 path=tpath)
    last_block = max([b.number for b in blocks if b.number is not None] or [0])

    for tid in sorted(last_seen):
        if tid not in declared:
            rep.defect("threads", "%s is operated on in the ledger but has no row in "
                       "state/threads.md" % tid, path=tpath)

    for tid, r in sorted(declared.items()):
        status = str(r.get("status", "")).strip().lower()
        tension = str(r.get("tension", "")).strip().lower()
        if status == "planned":
            # A plan written down, not a promise yet - the ageing and tension checks skip it.
            # Two things are still worth saying: a chapter already opened it and the row was not
            # flipped, or its chapter came and went without opening it.
            opened = rules.first_int(r.get("opened", ""))
            if tid in last_seen:
                rep.warn("threads", "%s is still `planned`, but ch %d operated on it - flip it "
                         "to `open`" % (tid, last_seen[tid]), path=tpath, line=r.line_no)
            elif opened.isdigit() and int(opened) <= last_block:
                rep.warn("threads", "%s was planned to open at ch %s and no block has opened it "
                         "- open it on the page, re-plan it, or retire it" % (tid, opened),
                         path=tpath, line=r.line_no)
            continue
        if status not in ("open", "escalated"):
            continue
        seen = last_seen.get(tid)
        opened = rules.first_int(r.get("opened", "")) or "?"
        if opened.isdigit() and int(opened) > last_ch:
            # Benchmark run #5 pre-registered threads as opened at ch 6 and ch 9 before ch 1
            # existed, and every check passed: the "never operated on" warn below was itself
            # gated on `opened <= last_ch`, so a thread that could not possibly have been
            # operated on was the one case exempted from being asked about. The age below then
            # came out negative. A plan is a fine thing to write down; it is not an open promise,
            # and a ledger that counts it as one is counting a debt nobody has taken on yet.
            rep.warn("threads", "%s is declared open at ch %s, but the book is only %d chapters "
                     "long - a thread planned ahead is not an open promise. Mark it `planned` "
                     "until the chapter that opens it"
                     % (tid, opened, last_ch), path=tpath, line=r.line_no)
            continue
        if seen is None:
            if opened.isdigit():
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
        opened = rules.first_int(r.get("opened", ""))
        due = rules.first_int(r.get("due", ""))
        # Clamped: a thread opened in the future aged backwards, and a negative age sorted to the
        # top of the oldest-first list, putting the newest promise where the oldest belongs.
        age = max(0, last_ch - int(opened)) if opened.isdigit() else None
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
                # The shared pattern, not a local `v(T\d+)`: the local copy survived O28's fix
                # and read `vTH06` as no payment at all, so a `TH`-numbered novel would have been
                # told at its first arc boundary that the arc paid nothing.
                paid.update(tid for op, tid in rules.THREAD_OP_IN_TEXT.findall(line)
                            if op == "v")
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
        # Benchmark run #6 (I4): the gate asked for `^T8` on row 5, the item was lost when the
        # drafter died, and the plan and the ledger have disagreed about chapter 5 since - with
        # this command reporting 0/0/0. Only a finished chapter is compared: the block is what
        # happened, the row what was planned, and one of them is out of date.
        block = novel.block(c.number) if cstatus in ("revised", "published") else None
        if block is None:
            continue
        planned = set(rules.THREAD_ID_IN_TEXT.findall(str(r.get("threads", ""))))
        done = set()
        for line in block.keys().get("thr", []):
            done.update(rules.THREAD_ID_IN_TEXT.findall(line))
        if planned != done and (planned or done):
            rep.warn("plan", "row %d plans thread(s) %s and ch %d's `thr>` operates on %s - "
                     "the row or the ledger is out of date"
                     % (c.number, ", ".join(sorted(planned)) or "none", c.number,
                        ", ".join(sorted(done)) or "none"), path=ppath, line=r.line_no)


def _roster(novel, rep, last_ch):
    """character-profile: a third appearance triggers a real profile."""
    epath = novel.path("bible", "cast", "_extras.md")
    have_files = set(k.lower() for k in novel.cast_files())
    for entry in novel.roster():
        name, i = entry["name"], entry["line"]
        actual = [a for a in entry["appearances"] if a <= last_ch]
        if len(actual) >= 3:
            slug = re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")
            if slug not in have_files and name.lower() not in have_files:
                rep.defect("promotion", "%s has appeared %d times (ch %s) and is still a "
                           "walk-on - a third appearance triggers a real profile"
                           % (name, len(actual), ", ".join(str(a) for a in actual)),
                           path=epath, line=i)
