#!/usr/bin/env python3
"""skilled-writer mechanical toolkit.

    python3 scripts/sw.py <command> [novel] [options]

Does the countable work the skills would otherwise spell out by hand: slicing the read-set,
sweeping a chapter for banned strings and channel mechanics, auditing the cast tables,
checking the ledger against the chapters, and stamping a measured word count.

It is an optimisation and never a dependency. Every skill that names a command here keeps
its manual checklist underneath, because the toolkit has to work with nothing installed.

Exit codes: 0 clean - 1 findings that need a decision - 2 bad usage or missing files.
"""

import argparse
import os
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from swlib import (cmd_arc, cmd_cast, cmd_curve, cmd_health, cmd_load,  # noqa: E402
                   cmd_history, cmd_kb, cmd_lint, cmd_readset, cmd_selftest,
                   cmd_export, cmd_state, cmd_status, cmd_trace, cmd_write, kb)
from swlib.novelio import Novel, resolve  # noqa: E402
from swlib.rates import Rates  # noqa: E402
from swlib.report import Report  # noqa: E402

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
USAGE_ERROR = 2

# Named once, so `sw health` can check the docs against the implementation rather than against
# a second list that drifts.
COMMANDS = ("readset", "lint", "arc", "cast", "curve", "state", "status", "stamp", "audit",
            "newnovel", "doctor", "trace", "history", "health", "selftest", "kb", "export",
            "load")


def _novel(args):
    n = resolve(getattr(args, "novel", None), REPO_ROOT)
    if n is None:
        target = getattr(args, "novel", None)
        if target:
            sys.stderr.write("no novel at %r (looked for novel.md there, under the repo root, "
                             "and under novels/)\n" % target)
        else:
            sys.stderr.write("could not pick a novel: name one, e.g. "
                             "`sw %s novels/<slug>`\n" % args.command)
        sys.exit(USAGE_ERROR)
    return n


def _emit(rep, args):
    show = "defect" if getattr(args, "quiet", False) else getattr(args, "show", "warn")
    print(rep.render(show=show))
    # A file or chapter that does not exist is bad usage, not a finding about the novel.
    if any(f.check == "usage" for f in rep.findings):
        return USAGE_ERROR
    return rep.exit_code


# --------------------------------------------------------------------- commands

def _checked_out_dir(target):
    """Where `sw export --out` may write: a directory that does not yet exist.

    The sibling of `_checked_out_path`, and the reason CLAUDE.md section 4 names the export
    explicitly rather than letting it quietly widen "scripts write only chapter frontmatter, a
    CCS `wc:` field and a fresh scaffold". A fresh directory is the scaffold case; an existing
    one is somebody's work.
    """
    dest = os.path.abspath(target)
    allowed = [os.path.abspath(REPO_ROOT), os.path.abspath(tempfile.gettempdir())]
    if not any(dest == root or dest.startswith(root + os.sep) for root in allowed):
        sys.stderr.write("--out must be inside the repo or the system temp directory; "
                         "%s is neither\n" % dest)
        sys.exit(USAGE_ERROR)
    if os.path.exists(dest):
        sys.stderr.write("--out refuses to write into an existing directory: %s\n" % dest)
        sys.exit(USAGE_ERROR)
    parent = os.path.dirname(dest) or "."
    if not os.path.isdir(parent):
        sys.stderr.write("--out parent directory does not exist: %s\n" % parent)
        sys.exit(USAGE_ERROR)
    return dest


def _checked_out_path(target):
    """Where `--out` is allowed to write: under the repo, or under the system temp dir.

    This is the only command that takes a destination from the caller, and it is documented as
    writing nothing. An unconstrained path with no overwrite guard is how a read-only tool ends
    up truncating a chapter.
    """
    dest = os.path.abspath(target)
    allowed = [os.path.abspath(REPO_ROOT), os.path.abspath(tempfile.gettempdir())]
    if not any(dest == root or dest.startswith(root + os.sep) for root in allowed):
        sys.stderr.write("--out must be inside the repo or the system temp directory; "
                         "%s is neither\n" % dest)
        sys.exit(USAGE_ERROR)
    if os.path.exists(dest):
        sys.stderr.write("--out refuses to overwrite an existing file: %s\n" % dest)
        sys.exit(USAGE_ERROR)
    parent = os.path.dirname(dest) or "."
    if not os.path.isdir(parent):
        sys.stderr.write("--out directory does not exist: %s\n" % parent)
        sys.exit(USAGE_ERROR)
    return dest


def do_readset(args):
    novel = _novel(args)
    chars = args.chars.split(",") if args.chars else None
    locs = args.locs.split(",") if args.locs else None
    text = cmd_readset.build(novel, args.chapter, chars, locs, want_society=args.society)
    if args.out:
        dest = _checked_out_path(args.out)
        with open(dest, "w", encoding="utf-8", newline="\n") as fh:
            fh.write(text)
        print("read-set for chapter %d written to %s (%d bytes)"
              % (args.chapter, args.out, len(text)))
    else:
        sys.stdout.write(text)
    return 0


def do_lint(args):
    novel = _novel(args)
    numbers = None
    if args.chapter is not None:
        numbers = [args.chapter]
    else:
        chs = [c.number for c in novel.chapters() if c.number]
        if not chs:
            sys.stderr.write("no chapters to lint in %s\n" % novel.path("chapters"))
            return USAGE_ERROR
        if not args.all:
            numbers = [max(chs)]
    return _emit(cmd_lint.run(novel, numbers), args)


def do_arc(args):
    return _emit(cmd_arc.run(_novel(args), args.arc), args)


def do_cast(args):
    return _emit(cmd_cast.run(_novel(args)), args)


def do_curve(args):
    return _emit(cmd_curve.run(_novel(args)), args)


def do_state(args):
    return _emit(cmd_state.run(_novel(args)), args)


def do_status(args):
    return _emit(cmd_status.run(_novel(args)), args)


def do_stamp(args):
    novel = _novel(args)
    number = args.chapter
    if number is None:
        chs = [c.number for c in novel.chapters() if c.number]
        if not chs:
            sys.stderr.write("no chapters to stamp\n")
            return USAGE_ERROR
        number = max(chs)
    rep, _wrote = cmd_write.stamp(novel, number, args.status, args.ledger)
    return _emit(rep, args)


def do_newnovel(args):
    rep, _ok = cmd_write.newnovel(args.slug, REPO_ROOT)
    return _emit(rep, args)


def do_audit(args):
    """The independent whole-novel pass. Replaces docs/check-chapters.sh."""
    novel = _novel(args)
    rep = Report("audit - %s" % novel.title)
    chapters = novel.chapters()
    if not chapters:
        rep.defect("audit", "no chapters yet in %s" % novel.path("chapters"))
        return _emit(rep, args)

    inv = ["   %-38s %7s %7s %-9s %s" % ("file", "words", "fm_wc", "status", "delivers")]
    total = 0
    for c in chapters:
        total += c.words
        inv.append("   %-38s %7d %7s %-9s %s"
                   % (c.name, c.words, c.meta.get("wordcount", "-"),
                      c.meta.get("status", "-"), str(c.meta.get("delivers", ""))[:48]))
    inv.append("   %d chapters, %d body words. Word count is a fact here and is scored on"
               % (len(chapters), total))
    inv.append("   nothing - only whether the recorded number is true.")
    rep.info("inventory", inv)

    rep.extend(cmd_lint.run(novel, None))
    rep.extend(cmd_cast.run(novel))
    rep.extend(cmd_state.run(novel))
    rep.extend(cmd_curve.run(novel))
    # Benchmark run #3: the writing agent reported "`sw audit` returns 0 defects" as its evidence
    # the novel was clean, on a novel where `campaign-clause` was firing on 4 of 5 chapters and
    # `sw history` said so. Every check here was per-chapter, and a habit is by definition not
    # visible in one chapter - so the gate people actually run could not see the one class of
    # defect that most needs a whole-novel view. Only the cross-chapter findings are added;
    # history's per-chapter trends come from the same `lint` already run above.
    hist, _data = cmd_history.run(novel)
    rep.findings.extend(f for f in hist.findings
                        if f.check in ("history-dialogue", "history-habit"))
    return _emit(rep, args)


def _json_dump(data, args):
    """`--json` prints the same content the report renders, for anything downstream."""
    import json
    print(json.dumps(data, indent=2, sort_keys=True, default=str))


def do_trace(args):
    rates = Rates()
    if args.rates:
        try:
            rates = Rates.load(args.rates)
        except (IOError, OSError, ValueError) as exc:
            sys.stderr.write("could not read --rates %s: %s\n" % (args.rates, exc))
            return USAGE_ERROR
    novel = resolve(getattr(args, "novel", None), REPO_ROOT)
    rep, data = cmd_trace.run(REPO_ROOT, novel=novel, rates=rates,
                              transcript_root=args.transcripts,
                              since=args.since, until=args.until,
                              session=args.session)
    if args.json:
        _json_dump(data, args)
        return 0
    return _emit(rep, args)


def do_history(args):
    rep, data = cmd_history.run(_novel(args))
    if args.json:
        _json_dump(data, args)
        return 0
    return _emit(rep, args)


def do_health(args):
    return _emit(cmd_health.run(REPO_ROOT, commands=sorted(COMMANDS)), args)


def do_selftest(args):
    keep = _checked_out_path(args.keep) if args.keep else None
    if keep:
        os.makedirs(keep)
    return _emit(cmd_selftest.run(REPO_ROOT, keep=keep), args)


def do_doctor(args):
    rep = Report("doctor")
    ok = sys.version_info >= (3, 8)
    rep.info("environment", [
        "   python %d.%d.%d at %s" % (sys.version_info[0], sys.version_info[1],
                                      sys.version_info[2], sys.executable),
        "   repo root %s" % REPO_ROOT.replace(os.sep, "/"),
        "   %s" % ("stdlib only, no dependencies to install" if ok else "NEEDS Python 3.8+"),
    ])
    if not ok:
        rep.defect("environment", "Python 3.8 or newer is required")

    tpl = os.path.join(REPO_ROOT, "novels", "_template")
    if not os.path.isdir(tpl):
        rep.defect("scaffold", "novels/_template is missing")

    nd = os.path.join(REPO_ROOT, "novels")
    found = []
    if os.path.isdir(nd):
        for name in sorted(os.listdir(nd)):
            p = os.path.join(nd, name)
            if name.startswith("_") or not os.path.isdir(p):
                continue
            n = Novel(p)
            if not n.exists():
                continue
            found.append("   %-28s %d chapters, %d CCS blocks%s%s"
                         % (name, len(n.chapters()), len(n.blocks()),
                            ", foreknowledge" if n.has_foreknowledge else "",
                            ", form-locked" if n.form_locked else ""))
    rep.info("novels", found or ["   none yet - run `sw newnovel <slug>`"])
    return _emit(rep, args)


def do_export(args):
    novel = _novel(args)
    if not args.okf:
        sys.stderr.write("sw export needs --okf (the only format there is)\n")
        sys.exit(USAGE_ERROR)
    out = _checked_out_dir(args.out or os.path.join(REPO_ROOT, "export-%s" % novel.slug))
    return _emit(cmd_export.run(novel, out), args)


def do_load(args):
    """What the toolkit hands the drafter for this chapter. Measures instructions, not prose."""
    novel = _novel(args)
    if args.chapter is None:
        sys.stderr.write("sw load needs --chapter/-c\n")
        sys.exit(USAGE_ERROR)
    return _emit(cmd_load.run(novel, args.chapter, REPO_ROOT), args)


def do_kb(args):
    """Query the craft knowledge base.

    Only `cards` and `passes` take a novel. The rest are repo-only, and must not go through
    `_novel()`, which exits 2 when no novel resolves - that would make `sw kb owner` unusable
    from anywhere but a novel directory.
    """
    novel = None
    if args.action in ("cards", "passes"):
        # `args` is nargs="*" and `novel` is the nargs="?" after it, so argparse gives the
        # greedy one everything and the novel slot stays empty - `sw kb cards novels/x -c 1`
        # never reached `novel` at all. It went unnoticed because with exactly one novel in
        # the repo `resolve(None)` picks it anyway; the documented form breaks on the second
        # book. Recover it here rather than reordering the positionals, which would change
        # the shape of every other kb action.
        if not getattr(args, "novel", None) and args.args:
            args.novel = args.args[-1]
        novel = _novel(args)
        if args.chapter is None:
            sys.stderr.write("sw kb %s needs --chapter/-c\n" % args.action)
            sys.exit(USAGE_ERROR)
    return cmd_kb.run(REPO_ROOT, args, novel)


# ---------------------------------------------------------------------- parsing

def build_parser():
    p = argparse.ArgumentParser(
        prog="sw", description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="command")

    def novel_arg(sp):
        sp.add_argument("novel", nargs="?",
                        help="path or slug; omit when only one novel exists")
        sp.add_argument("-q", "--quiet", action="store_true",
                        help="show defects only")
        sp.add_argument("--show", choices=["defect", "warn", "note"], default="warn",
                        help="lowest level to print (default: warn)")
        return sp

    sp = novel_arg(sub.add_parser("readset", help="assemble the bounded read-set for a chapter"))
    sp.add_argument("--chapter", "-c", type=int, required=True)
    sp.add_argument("--chars", help="comma-separated characters on the page this chapter")
    sp.add_argument("--locs", help="comma-separated locations this chapter")
    sp.add_argument("--society", action="store_true",
                    help="include bible/society.md (chapter turns on a social rule)")
    sp.add_argument("--out", help="write to a file instead of stdout")
    sp.set_defaults(func=do_readset)

    sp = novel_arg(sub.add_parser("lint", help="mechanical sweep over a chapter's prose"))
    sp.add_argument("--chapter", "-c", type=int, help="default: the latest chapter")
    sp.add_argument("--all", action="store_true", help="every chapter")
    sp.set_defaults(func=do_lint)

    sp = novel_arg(sub.add_parser("arc", help="the distributional pass over one arc"))
    sp.add_argument("--arc", "-a", type=int, help="default: the latest arc")
    sp.set_defaults(func=do_arc)

    novel_arg(sub.add_parser("cast", help="voice matrix and competence grid audits")
              ).set_defaults(func=do_cast)
    novel_arg(sub.add_parser("curve", help="power curve - step size, boosts, pressure")
              ).set_defaults(func=do_curve)
    lp = novel_arg(sub.add_parser(
        "load", help="what the toolkit hands the drafter - cards, words, boxes, negations"))
    lp.add_argument("--chapter", "-c", type=int, required=True)
    lp.set_defaults(func=do_load)
    novel_arg(sub.add_parser("state", help="ledger, threads, plan and roster integrity")
              ).set_defaults(func=do_state)
    novel_arg(sub.add_parser("status", help="progress aggregation for /novel-status")
              ).set_defaults(func=do_status)

    sp = novel_arg(sub.add_parser("stamp", help="measure the body, write wordcount/status"))
    sp.add_argument("--chapter", "-c", type=int, help="default: the latest chapter")
    sp.add_argument("--status", choices=list(cmd_lint.VALID_STATUS))
    sp.add_argument("--ledger", action="store_true",
                    help="also correct wc: in the chapter's CCS block")
    sp.set_defaults(func=do_stamp)

    novel_arg(sub.add_parser("audit", help="independent whole-novel pass")
              ).set_defaults(func=do_audit)

    sp = sub.add_parser("newnovel", help="copy novels/_template to novels/<slug>")
    sp.add_argument("slug")
    sp.add_argument("-q", "--quiet", action="store_true")
    sp.add_argument("--show", choices=["defect", "warn", "note"], default="note")
    sp.set_defaults(func=do_newnovel)

    sp = novel_arg(sub.add_parser("export", help="project a novel into an OKF bundle"))
    sp.add_argument("--okf", action="store_true", help="Open Knowledge Format v0.2")
    sp.add_argument("--out", help="destination directory; must not already exist")
    sp.set_defaults(func=do_export)

    sp = sub.add_parser("kb", help="query the craft knowledge base - owners, cards, concepts")
    sp.add_argument("action", choices=list(cmd_kb.ACTIONS))
    sp.add_argument("args", nargs="*", help="a concept slug, or search terms")
    sp.add_argument("novel", nargs="?", help="cards/passes only: path or slug")
    sp.add_argument("--chapter", "-c", type=int, help="cards/passes only")
    sp.add_argument("--phase", choices=["A", "B", "C"], help="cards only")
    sp.add_argument("--type", choices=list(kb.TYPES), help="list only")
    sp.add_argument("--json", action="store_true", help="list only: machine-readable, to stdout")
    sp.add_argument("-q", "--quiet", action="store_true")
    sp.add_argument("--show", choices=["defect", "warn", "note"], default="warn")
    sp.set_defaults(func=do_kb)

    sp = novel_arg(sub.add_parser("trace", help="what the run cost, and which skills it opened"))
    sp.add_argument("--transcripts", help="Claude Code config root (default: $CLAUDE_CONFIG_DIR "
                                          "or ~/.claude)")
    sp.add_argument("--rates", help="JSON file of model -> rates, overriding the built-in table")
    sp.add_argument("--since", help="ISO 8601 lower bound, e.g. 2026-09-09 - scope one run "
                                    "instead of every session ever run in this repo")
    sp.add_argument("--until", help="ISO 8601 upper bound")
    sp.add_argument("--session", help="one transcript only, by session id, agent id or path "
                                      "fragment - a time window alone still includes the "
                                      "session that drove the agent")
    sp.add_argument("--json", action="store_true", help="emit the measurements as JSON")
    sp.set_defaults(func=do_trace)

    sp = novel_arg(sub.add_parser("history", help="the whole book as a series, not one chapter"))
    sp.add_argument("--json", action="store_true", help="emit the per-chapter rows as JSON")
    sp.set_defaults(func=do_history)

    sp = sub.add_parser("health", help="the toolkit's own wiring: skills, cards, template, docs")
    sp.add_argument("-q", "--quiet", action="store_true")
    sp.add_argument("--show", choices=["defect", "warn", "note"], default="warn")
    sp.set_defaults(func=do_health)

    sp = sub.add_parser("selftest", help="dry-run the whole pipeline on a throwaway novel")
    sp.add_argument("--keep", help="build into this directory and leave it there")
    sp.add_argument("-q", "--quiet", action="store_true")
    sp.add_argument("--show", choices=["defect", "warn", "note"], default="warn")
    sp.set_defaults(func=do_selftest)

    sp = sub.add_parser("doctor", help="environment and workspace check")
    sp.add_argument("-q", "--quiet", action="store_true")
    sp.add_argument("--show", choices=["defect", "warn", "note"], default="warn")
    sp.set_defaults(func=do_doctor)
    return p


def _force_utf8():
    """Windows consoles default to a legacy code page; novel prose is full of em-dashes and
    curly quotes, and printing one to cp1252 raises UnicodeEncodeError. Python 3.7+ can
    retag the stream in place."""
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8", errors="replace")
        except (AttributeError, ValueError):
            pass


def main(argv=None):
    _force_utf8()
    parser = build_parser()
    args = parser.parse_args(argv)
    if not getattr(args, "command", None):
        parser.print_help()
        return USAGE_ERROR
    return args.func(args) or 0


if __name__ == "__main__":
    sys.exit(main())
