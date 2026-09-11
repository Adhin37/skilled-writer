"""`sw status` - the file-reading half of /novel-status.

Aggregation only. The command file still owns the human-facing report: this hands it the
numbers so it does not have to open six files to count them.
"""

import re

from . import cmd_readset
from .report import Report


def run(novel):
    rep = Report("status - %s" % novel.title)
    chapters = novel.chapters()
    blocks = novel.blocks()
    last = max([c.number for c in chapters if c.number] or [0])
    arc_len = novel.arc_length
    arc = ((last - 1) // arc_len + 1) if last else 1

    by_status = {}
    for c in chapters:
        by_status[str(c.meta.get("status", "?"))] = by_status.get(str(c.meta.get("status", "?")), 0) + 1

    rep.info("position", [
        "   chapter %d of arc %d (arc length %d)" % (last, arc, arc_len),
        "   %s" % ", ".join("%s: %d" % kv for kv in sorted(by_status.items())),
        "   in-world: %s" % (blocks[-1].header_field("t") if blocks else "-"),
        "   genre %s | reactivity %s | POV %s | MC tier %s"
        % (novel.get("genre"), novel.get("timeline.reactivity"), novel.get("pov.mode"),
           novel.get("mc.intel_tier")),
    ])

    stale = cmd_readset.ungated(novel, last + 1)
    if stale:
        rep.warn("gate", "%d chapter(s) never passed the phase C gate - newest is ch %d at "
                 "`status: %s`. `/novel-write %d` re-gates it."
                 % (len(stale), stale[0].number,
                    str(stale[0].meta.get("status", "")).strip() or "?", stale[0].number),
                 path=stale[0].path)

    rep.info("last three chapters (dlv> - translate for the user, do not paste)", [
        "   ch %d: %s" % (b.number, b.get("dlv") or "(no dlv>)") for b in blocks[-3:]] or ["   none"])

    last_seen = {}
    for b in blocks:
        for line in b.keys().get("thr", []):
            for tid in re.findall(r"[~^vx]?(T\d+)", line):
                last_seen[tid] = max(last_seen.get(tid, 0), b.number)
    trows = []
    for r in novel.threads():
        status = str(r.get("status", "")).strip().lower()
        if status not in ("open", "escalated"):
            continue
        tid = r.first().strip()
        seen = last_seen.get(tid)
        age = ("last touched ch %d (%d ago)" % (seen, last - seen)) if seen else "never touched"
        trows.append("   %-5s %-8s %-6s %s | due: %s | %s"
                     % (tid, status, str(r.get("tension")), r.get("thread")[:46],
                        r.get("due"), age))
    rep.info("open threads (%d)" % len(trows), trows or ["   none"])

    rep.info("character arcs", [
        "   %-12s rate %-3s rung %-4s since ch %-4s next: %s"
        % (r.first(), r.get("rate"), r.get("rung"), r.get("since ch"), r.get("next trigger")[:44])
        for r in novel.growth_rows()] or ["   none"])

    skills = novel.skill_rows()
    if skills:
        rep.info("skill ladders", [
            "   %-12s %-28s stage %s (since ch %s)"
            % (r.first(), r.get("skill")[:28], r.get("stage"), r.get("since ch"))
            for r in skills])

    nxt = []
    for r in novel.plan_rows():
        num = re.sub(r"\D", "", r.first())
        if num.isdigit() and last < int(num) <= last + 3:
            nxt.append("   ch %-4s %-28s %s" % (num, r.get("title")[:28], r.get("delivers")[:70]))
    rep.info("next up", nxt or ["   nothing planned ahead - run chapter-plan"])

    if novel.has_foreknowledge:
        rep.info("foreknowledge", [
            "   grain %s | first win due ch %s | first failure due ch %s"
            % (novel.get("mc.foreknowledge_grain"), novel.get("mc.foreknowledge_first_win_ch"),
               novel.get("mc.foreknowledge_fails_ch")),
            "   fk> lines in ledger: %d of %d blocks"
            % (sum(1 for b in blocks if b.has("fk")), len(blocks))])

    rep.info("ending contract (never let the world foreclose this)", [
        "   %s" % str(novel.get("ending.contract", "(unset)"))[:300]])
    nn = novel.get("ending.non_negotiables") or []
    if nn:
        rep.info("non-negotiables", ["   - %s" % x for x in nn])
    return rep
