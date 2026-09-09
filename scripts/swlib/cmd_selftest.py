"""`sw selftest` - the dry run of `novel-init`, and the proof that a fresh clone works.

Scaffolds a complete novel in a throwaway directory, fills it from `sample.py`, and runs every
command in the toolkit against it. No model, no interview, no network, no API key, a few seconds.
If this exits 0, the pipeline works on this machine.

**The positive control is the point.** A selftest that only asserts "no defects" passes exactly as
happily when every parser is dead - which is the failure `docs/benchmark.md` describes as "a parser
that under-detects does not look like a broken parser, it looks like a clean chapter". So it runs
twice: once on a clean novel where every command must find nothing, and once on the same novel with
six named defects planted in it, where each one must be caught by the check that owns it. A defect
that was planted and not found is itself a DEFECT.

The scaffold comes from the shipped `novels/_template` through the real `newnovel`, so this also
fails when the template drifts away from the parsers.
"""

import os
import shutil
import tempfile

from . import (cmd_arc, cmd_cast, cmd_curve, cmd_health, cmd_history, cmd_lint,
               cmd_readset, cmd_state, cmd_status, cmd_trace, cmd_write, sample)
from .novelio import Novel
from .report import Report


class Step(object):
    __slots__ = ("name", "ok", "defects", "warns", "note")

    def __init__(self, name, ok, defects=None, warns=None, note=""):
        self.name = name
        self.ok = ok
        self.defects = defects
        self.warns = warns
        self.note = note


def _scaffold(repo_root, workdir, seeded):
    """Build a novel the way a user would: copy the template, run newnovel, fill it."""
    template = os.path.join(repo_root, "novels", "_template")
    if not os.path.isdir(template):
        raise IOError("novels/_template is missing at %s" % template)
    os.makedirs(os.path.join(workdir, "novels"))
    shutil.copytree(template, os.path.join(workdir, "novels", "_template"))
    rep, ok = cmd_write.newnovel(sample.SLUG, workdir)
    root = os.path.join(workdir, "novels", sample.SLUG)
    if not ok:
        return None, rep, 0
    files = sample.build(root, seeded=seeded)
    return root, rep, len(files)


def _clean_pass(repo_root, workdir, rep):
    """Every command against a novel that should give every one of them nothing to say."""
    steps = []
    root, screp, filled = _scaffold(repo_root, workdir, seeded=False)
    if root is None:
        rep.defect("selftest", "newnovel refused to scaffold - the dry run cannot start")
        for f in screp.findings:
            rep.findings.append(f)
        return steps, None
    created = sum(len(lines) for h, lines in screp.sections if h.startswith("created"))
    steps.append(Step("newnovel", True, note="%d files scaffolded, %d filled"
                                             % (created, filled)))

    novel = Novel(root)
    if not novel.exists():
        rep.defect("selftest", "the scaffolded novel has no novel.md at %s" % root)
        return steps, None

    try:
        text = cmd_readset.build(novel, 4, ["Wren", "Maro"], ["The Tidehouse"], want_society=True)
    except Exception as exc:                                   # noqa: BLE001 - reported, not raised
        rep.defect("selftest", "readset raised %s: %s" % (type(exc).__name__, exc))
        text = ""
    ok = bool(text) and "=C0003=" in text and "Wren" in text
    steps.append(Step("readset -c 4", ok,
                      note="%d bytes, blocks 1-3 and the speaker rows present" % len(text)))
    if not ok:
        rep.defect("selftest", "the read-set for chapter 4 is empty or is missing the blocks "
                               "and cast rows it is defined as carrying")

    for name, fn in (("lint --all", lambda: cmd_lint.run(novel, None)),
                     ("cast", lambda: cmd_cast.run(novel)),
                     ("curve", lambda: cmd_curve.run(novel)),
                     ("state", lambda: cmd_state.run(novel)),
                     ("status", lambda: cmd_status.run(novel)),
                     ("arc -a 1", lambda: cmd_arc.run(novel, 1)),
                     ("history", lambda: cmd_history.run(novel)[0])):
        steps.append(_graded(name, fn, rep))

    # stamp is the one command that writes. The counts were measured at build time, so a
    # correct stamp writes nothing at all - which is the assertion.
    strep, wrote = cmd_write.stamp(novel, 6)
    steps.append(Step("stamp -c 6", not wrote and strep.exit_code == 0,
                      strep.count("defect"), strep.count("warn"),
                      "wrote nothing" if not wrote else "REWROTE a correct file"))
    if wrote:
        rep.defect("selftest", "stamp rewrote chapter 6, whose word count was already correct - "
                               "a bookkeeping command that writes when nothing changed will "
                               "churn every chapter in the book")
    return steps, novel


def _graded(name, fn, rep):
    try:
        sub = fn()
    except Exception as exc:                                   # noqa: BLE001
        rep.defect("selftest", "%s raised %s: %s" % (name, type(exc).__name__, exc))
        return Step(name, False, note="raised %s" % type(exc).__name__)
    d, w = sub.count("defect"), sub.count("warn")
    if d:
        rep.defect("selftest", "%s reports %d defect(s) against the clean sample novel: %s"
                   % (name, d, ", ".join(sorted({f.check for f in sub.findings
                                                 if f.level == "defect"}))))
    if w:
        rep.warn("selftest", "%s reports %d warning(s) against the clean sample novel: %s"
                 % (name, w, ", ".join(sorted({f.check for f in sub.findings
                                               if f.level == "warn"}))))
    return Step(name, d == 0, d, w)


def _control_pass(repo_root, workdir, rep):
    """The same novel with named defects in it. Each must be caught by the check that owns it."""
    root, _screp, _n = _scaffold(repo_root, workdir, seeded=True)
    if root is None:
        rep.defect("selftest", "the seeded novel could not be scaffolded")
        return []
    novel = Novel(root)
    caught = set()
    for fn in (lambda: cmd_lint.run(novel, None), lambda: cmd_cast.run(novel),
               lambda: cmd_curve.run(novel), lambda: cmd_state.run(novel)):
        try:
            sub = fn()
        except Exception as exc:                               # noqa: BLE001
            rep.defect("selftest", "a command raised on the seeded novel: %s: %s"
                       % (type(exc).__name__, exc))
            continue
        caught.update((f.check, f.level) for f in sub.findings
                      if f.level in ("defect", "warn"))

    rows = []
    for check, where, what, level in sample.SEEDED:
        hit = (check, level) in caught
        rows.append((check, where, "%s (%s)" % (what, level), hit))
        if not hit:
            rep.defect("control",
                       "planted `%s` in %s (%s) and no command reported it - the check is dead, "
                       "and a dead check does not look like a broken parser, it looks like a "
                       "clean chapter" % (check, where, what))
    extra = sorted(c for c, lv in caught
                   if lv == "defect" and c not in {r[0] for r in sample.SEEDED})
    if extra:
        rep.warn("control", "the seeded novel also raised %s - a seed with a side effect makes "
                            "the control less exact than it reads" % ", ".join(extra))
    return rows


def run(repo_root, keep=None, transcript_root=None):
    rep = Report("selftest - %s" % os.path.basename(os.path.abspath(repo_root)))
    workdir = keep or tempfile.mkdtemp(prefix="sw-selftest-")
    control_dir = os.path.join(workdir, "control")
    clean_dir = os.path.join(workdir, "clean")
    os.makedirs(clean_dir)
    os.makedirs(control_dir)
    failed = False
    try:
        steps, _novel = _clean_pass(repo_root, clean_dir, rep)
        rows = _control_pass(repo_root, control_dir, rep)

        hrep = cmd_health.run(repo_root, commands=None)
        steps.append(Step("health", hrep.exit_code == 0, hrep.count("defect"),
                          hrep.count("warn"), "audits this repo, not the sample"))
        if hrep.count("defect"):
            rep.defect("selftest", "health reports %d defect(s) against this repo - run "
                                   "`sw health` for the list" % hrep.count("defect"))

        # The empty path: a config root with no transcripts must report nothing and not raise.
        empty = os.path.join(workdir, "no-transcripts")
        os.makedirs(empty)
        try:
            trep, tdata = cmd_trace.run(repo_root, transcript_root=transcript_root or empty)
            ok = trep.exit_code == 0 and not tdata.get("sessions")
            steps.append(Step("trace (empty root)", ok, note="reported nothing, exit 0"))
            if not ok:
                rep.defect("selftest", "trace against an empty transcript root did not come "
                                       "back empty and clean")
        except Exception as exc:                               # noqa: BLE001
            rep.defect("selftest", "trace raised on an empty transcript root: %s: %s"
                       % (type(exc).__name__, exc))
            steps.append(Step("trace (empty root)", False, note="raised"))

        _render(rep, steps, rows, workdir, keep)
        failed = rep.exit_code != 0
    finally:
        if keep is None and not failed:
            shutil.rmtree(workdir, ignore_errors=True)
    return rep


def _render(rep, steps, rows, workdir, keep):
    lines = ["   %-20s %-6s %8s %7s  %s" % ("step", "result", "defects", "warns", "note")]
    for s in steps:
        lines.append("   %-20s %-6s %8s %7s  %s"
                     % (s.name, "ok" if s.ok else "FAIL",
                        "-" if s.defects is None else s.defects,
                        "-" if s.warns is None else s.warns, s.note))
    rep.info("pipeline, against a clean novel built from the shipped template", lines)

    if rows:
        ctl = ["   %-16s %-26s %-8s %s" % ("check", "planted in", "caught", "what was planted")]
        for check, where, what, hit in rows:
            ctl.append("   %-16s %-26s %-8s %s"
                       % (check, where, "yes" if hit else "NO", what))
        ctl.append("   Every row must say yes. A `no` means that check is dead, and a dead check")
        ctl.append("   reads exactly like a clean novel.")
        rep.info("positive control, against the same novel with defects planted in it", ctl)

    where = workdir.replace(os.sep, "/")
    rep.info("workspace", [
        "   %s" % where,
        "   %s" % ("kept, because --keep was given" if keep else
                   ("kept, because the run failed" if rep.exit_code else "removed")),
        "   Nothing outside it was written. `health` read this repo and wrote nothing.",
    ])
