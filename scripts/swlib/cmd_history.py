"""`sw history` - the whole book as a series, rather than one chapter at a time.

`sw arc` lines chapters up inside one arc; this lines the whole book up. Every high-severity
finding in benchmark run #1 was distributional - dialogue starvation, chapters clustering at a
length floor, an advantage that never won - and none of them is visible in the chapter you are
holding. They are visible in a column.

Read-only, and computed live from what is on disk: no snapshot file, so the rule that these
scripts only ever write chapter frontmatter, a CCS `wc:` field and a fresh scaffold still holds
exactly as written. `--json` emits the rows for anyone who wants to diff two points in time.

**Word count is reported and scored on nothing.** This is the table most likely to be misread as
a scoreboard, and the gate is `revision-pass` Pass 9 - want, friction, change, cost, next. Two
versions of a length gate were gamed within five chapters each; a third is not wanted.
"""

import os
import re
import time

from . import cmd_lint, rules
from .report import Report

SPARK = " .:-=+*#"


def _spark(values, lo=None, hi=None):
    """An ASCII sparkline. ASCII on purpose: this prints to Windows consoles too."""
    vals = [v for v in values if v is not None]
    if not vals:
        return ""
    lo = min(vals) if lo is None else lo
    hi = max(vals) if hi is None else hi
    if hi <= lo:
        return SPARK[len(SPARK) // 2] * len(values)
    out = []
    for v in values:
        if v is None:
            out.append(" ")
            continue
        idx = int(round((v - lo) / float(hi - lo) * (len(SPARK) - 1)))
        out.append(SPARK[max(0, min(len(SPARK) - 1, idx))])
    return "".join(out)


def _trend(values):
    """Mean of the first half against the second. Enough to say 'rising' honestly."""
    vals = [v for v in values if v is not None]
    if len(vals) < 4:
        return None
    half = len(vals) // 2
    a = sum(vals[:half]) / float(half)
    b = sum(vals[half:]) / float(len(vals) - half)
    return a, b


def run(novel):
    rep = Report("history - %s" % novel.title)
    chapters = [c for c in novel.chapters() if c.number is not None]
    data = {"slug": novel.slug, "chapters": []}
    if not chapters:
        rep.info("history", ["   no chapters yet - nothing to trend"])
        return rep, data

    arc_len = novel.arc_length
    rows = []
    for ch in chapters:
        block = novel.block(ch.number)
        defects = _lint_counts(novel, ch)
        rows.append({
            "number": ch.number,
            "file": ch.name,
            "arc": (ch.number - 1) // arc_len + 1,
            "words": ch.words,
            "speech_share": round(ch.speech_share, 1),
            "thoughts": len(ch.thoughts()),
            "metas": len(ch.metas()),
            "scene_breaks": ch.scene_breaks(),
            "paragraphs": len(ch.paragraphs()),
            "status": str(ch.meta.get("status", "")),
            "delivers": str(ch.meta.get("delivers", "")),
            "has_block": block is not None,
            "defects": defects["defect"],
            "warnings": defects["warn"],
            "checks": defects["checks"],
            "mtime": _mtime(ch.path),
        })
    data["chapters"] = rows

    _table(rep, rows)
    _dialogue(rep, rows)
    _length(rep, rows)
    _defects(rep, rows)
    _threads(novel, rep, rows, data)
    _curve(novel, rep, data)
    _cadence(rep, rows, data)
    return rep, data


def _mtime(path):
    try:
        return os.path.getmtime(path)
    except OSError:
        return None


def _lint_counts(novel, ch):
    sub = Report()
    cmd_lint.lint_chapter(novel, ch, sub)
    counts = {"defect": 0, "warn": 0, "checks": {}}
    for f in sub.findings:
        if f.level in counts:
            counts[f.level] += 1
        if f.level in ("defect", "warn"):
            counts["checks"][f.check] = counts["checks"].get(f.check, 0) + 1
    return counts


def _table(rep, rows):
    lines = ["   %4s %4s %7s %7s %6s %5s %6s %5s %4s  %s"
             % ("ch", "arc", "words", "speech", "thght", "meta", "breaks", "defct", "ccs",
                "delivers")]
    for r in rows:
        lines.append("   %4d %4d %7d %6.1f%% %6d %5d %6d %5d %4s  %s"
                     % (r["number"], r["arc"], r["words"], r["speech_share"], r["thoughts"],
                        r["metas"], r["scene_breaks"], r["defects"],
                        "yes" if r["has_block"] else "NO", r["delivers"][:34]))
    total = sum(r["words"] for r in rows)
    lines.append("   %d chapters, %d body words. Word count is a measured fact here and is"
                 % (len(rows), total))
    lines.append("   scored on nothing - the gate is revision-pass Pass 9.")
    rep.info("chapters", lines)


def _dialogue(rep, rows):
    shares = [r["speech_share"] for r in rows]
    lines = ["   %s   %.0f%% -> %.0f%% (floor %.0f, target %.0f-%.0f)"
             % (_spark(shares, 0, max(rules.SPEECH_TARGET_HIGH, max(shares))),
                shares[0], shares[-1], rules.SPEECH_FLOOR,
                rules.SPEECH_TARGET_LOW, rules.SPEECH_TARGET_HIGH)]
    starved = [r["number"] for r in rows if r["speech_share"] < rules.SPEECH_FLOOR]
    below = [r["number"] for r in rows if rules.SPEECH_FLOOR <= r["speech_share"]
             < rules.SPEECH_TARGET_LOW]
    move = _trend(shares)
    if move:
        lines.append("   first half %.1f%%, second half %.1f%%" % move)
    rep.info("dialogue share", lines)

    if starved:
        rep.defect("history-dialogue",
                   "%d chapter(s) under the %.0f%% floor: %s - on a silent cast "
                   "voice-separation, dialogue-voice and competence-map all silently no-op"
                   % (len(starved), rules.SPEECH_FLOOR, _runs(starved)))
    elif len(below) >= max(3, len(rows) // 2):
        rep.warn("history-dialogue",
                 "%d of %d chapters sit below the %.0f%% target: %s - the run-#1 shape, and "
                 "invisible in any single chapter"
                 % (len(below), len(rows), rules.SPEECH_TARGET_LOW, _runs(below)))


def _length(rep, rows):
    words = [r["words"] for r in rows]
    lines = ["   %s   %d -> %d words" % (_spark(words), words[0], words[-1]),
             "   min %d / median %d / max %d, spread %d"
             % (min(words), sorted(words)[len(words) // 2], max(words),
                max(words) - min(words))]
    lines.append("   Printed, never scored. Any number that decides whether a chapter ships")
    lines.append("   gets optimised, and prose optimised toward a length is padded prose.")
    rep.info("length", lines)


def _defects(rep, rows):
    by_check = {}
    for r in rows:
        for check, n in r["checks"].items():
            by_check.setdefault(check, []).append(r["number"])
    if not by_check:
        rep.info("lint over time", ["   no defects or warnings in any chapter"])
        return
    lines = ["   %-18s %6s  %s" % ("check", "chs", "chapters")]
    for check in sorted(by_check, key=lambda c: (-len(by_check[c]), c)):
        chs = by_check[check]
        lines.append("   %-18s %6d  %s" % (check, len(chs), _runs(chs)))
    lines.append("   A check firing on most chapters is a habit, not a chapter defect - fix it")
    lines.append("   in the drafting procedure rather than one chapter at a time.")
    rep.info("lint over time", lines)

    for check, chs in sorted(by_check.items()):
        if len(rows) >= 4 and len(chs) >= max(3, int(len(rows) * 0.6)):
            rep.warn("history-habit",
                     "`%s` fires on %d of %d chapters - that is a drafting habit"
                     % (check, len(chs), len(rows)))


def _threads(novel, rep, rows, data):
    last = max(r["number"] for r in rows)
    seen = {}
    for b in novel.blocks():
        for line in b.keys().get("thr", []):
            for tid in re.findall(r"[~^vx]?(T\d+)", line):
                seen[tid] = max(seen.get(tid, 0), b.number)
    out, lines = [], ["   %-6s %-10s %-6s %-34s %s"
                      % ("id", "status", "tens", "thread", "last touched")]
    for r in novel.threads():
        status = str(r.get("status", "")).strip().lower()
        if status not in ("open", "escalated"):
            continue
        tid = r.first().strip()
        touched = seen.get(tid)
        age = (last - touched) if touched else None
        out.append({"id": tid, "status": status, "age": age,
                    "thread": r.get("thread"), "due": r.get("due")})
        lines.append("   %-6s %-10s %-6s %-34s %s"
                     % (tid, status, str(r.get("tension")), r.get("thread")[:34],
                        ("ch %d, %d ago" % (touched, age)) if touched else "never"))
    data["threads"] = out
    if not out:
        return
    rep.info("open threads (%d)" % len(out), lines)
    # A thread cannot be overdue before there has been time to touch it. Ageing against the
    # arc's *planned* length flagged every untouched thread at chapter 1. Benchmark run #2, F6.
    horizon = min(novel.arc_length, last)
    stale = [t for t in out
             if (t["age"] is None and last >= horizon) or (t["age"] or 0) >= horizon]
    if stale:
        rep.warn("history-threads",
                 "%d open thread(s) untouched for %d chapter(s) or never touched: %s - a thread "
                 "past its horizon is escalated, paid, or deferred with a stated reason"
                 % (len(stale), horizon, ", ".join(t["id"] for t in stale[:8])))


def _curve(novel, rep, data):
    if not novel.has_scaling:
        return
    pressure = []
    for r in novel.pressure_rows():
        digits = re.sub(r"\D", "", r.first())
        p = _signed(r.get("p"))
        if digits and p is not None:
            pressure.append((int(digits), p))
    data["pressure"] = pressure
    if not pressure:
        return
    pressure.sort()
    vals = [p for _, p in pressure]
    lines = ["   pressure  %s   %+d -> %+d" % (_spark(vals), vals[0], vals[-1]),
             "   logged at ch %s" % ", ".join(str(c) for c, _ in pressure[:16])]
    gains = []
    for r in novel.gain_rows():
        digits = re.sub(r"\D", "", r.first())
        if digits:
            gains.append(int(digits))
    if gains:
        lines.append("   tier gains at ch %s" % ", ".join(str(g) for g in sorted(gains)))
        data["gains"] = sorted(gains)
    rep.info("power curve over time", lines)
    if len(set(vals)) == 1 and len(vals) >= 4:
        rep.warn("history-curve",
                 "every logged confrontation sits at P=%+d - the gap is the story, and a "
                 "constant gap is a flat one" % vals[0])


def _signed(text):
    m = re.search(r"[-+]?\d+", str(text or ""))
    return int(m.group(0)) if m else None


def _cadence(rep, rows, data):
    stamps = [r["mtime"] for r in rows if r["mtime"]]
    if len(stamps) < 2:
        return
    days = {}
    for t in stamps:
        days[time.strftime("%Y-%m-%d", time.localtime(t))] = days.get(
            time.strftime("%Y-%m-%d", time.localtime(t)), 0) + 1
    data["cadence"] = days
    span_days = max(1, int((max(stamps) - min(stamps)) // 86400) + 1)
    lines = ["   %d chapter files last modified across %d day(s), %.1f per active day"
             % (len(stamps), span_days, len(stamps) / float(len(days))),
             "   " + "  ".join("%s x%d" % kv for kv in sorted(days.items())[-8:]),
             "   From file mtimes, so a fresh `git clone` resets them all to the clone time.",
             "   Treat this as a signal about the working copy, not a publication record."]
    rep.info("cadence", lines)


def _runs(numbers):
    """[1,2,3,7,9,10] -> '1-3, 7, 9-10'. A list of chapter numbers a reader can scan."""
    nums = sorted(set(numbers))
    if not nums:
        return "-"
    out, start, prev = [], nums[0], nums[0]
    for n in nums[1:]:
        if n == prev + 1:
            prev = n
            continue
        out.append(str(start) if start == prev else "%d-%d" % (start, prev))
        start = prev = n
    out.append(str(start) if start == prev else "%d-%d" % (start, prev))
    return ", ".join(out)
