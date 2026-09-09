"""`sw trace` - what the run cost, and which skills it actually opened.

The rest of the toolkit reviews the novel. This reviews the run: tokens, dollars, wall clock,
and the finding that motivated the command - `docs/benchmark.md` found that 21 of 37 skills were
never loaded, including four the contract calls non-optional, and had no way to check whether the
fix worked. This is that check, run against the transcripts Claude Code already writes.

It measures and does not score. There is no "good" number of skill loads and no target cost; the
one judgement it makes is that a skill `CLAUDE.md` section 3 lists as always in play, in a run
that opened skills at all, should have been opened.
"""

import os

from . import rules, transcripts
from .rates import Rates, total_cost
from .report import Report


def _skill_roster(repo_root):
    d = os.path.join(repo_root, ".claude", "skills")
    if not os.path.isdir(d):
        return []
    return sorted(name for name in os.listdir(d)
                  if os.path.isdir(os.path.join(d, name)) and not name.startswith("."))


def _classify(roster, novel):
    """Split the roster into (always-in-play, off-for-this-novel).

    Without a novel every module counts as in play: a module cannot be called switched off when
    nothing says which novel's switches to read.
    """
    off = set()
    if novel is not None:
        for name in rules.OPTIONAL_MODULES:
            if not novel.optional_on(name):
                off.add(name)
        genre = str(novel.get("genre", "") or "").lower()
        sub = str(novel.get("subgenre", "") or "").lower()
        for name, triggers in rules.GENRE_MODULES.items():
            if genre not in triggers and sub not in triggers:
                off.add(name)
    return [s for s in roster if s not in off], sorted(off & set(roster))


def _short(sess):
    """A transcript name that identifies it: the id, not the left-truncated path to it."""
    name = os.path.basename(sess.path)
    if name.endswith(".jsonl"):
        name = name[:-6]
    if sess.is_subagent:
        parent = os.path.basename(os.path.dirname(os.path.dirname(sess.path)))
        return "%s/%s" % (parent[:8], name)
    return name


def _hms(seconds):
    seconds = int(seconds or 0)
    if seconds < 60:
        return "%ds" % seconds
    if seconds < 3600:
        return "%dm %02ds" % (seconds // 60, seconds % 60)
    return "%dh %02dm" % (seconds // 3600, (seconds % 3600) // 60)


def _per_model(sessions):
    """{model: usage} so cost can be priced per model rather than blended."""
    out = {}
    for sess in sessions:
        for r in sess.responses:
            u = out.setdefault(r.model or "(unknown)", {
                "responses": 0, "input_tokens": 0, "cache_write_5m": 0,
                "cache_write_1h": 0, "cache_read_input_tokens": 0, "output_tokens": 0})
            u["responses"] += 1
            u["input_tokens"] += r.input_tokens
            u["cache_write_5m"] += r.cache_write_5m
            u["cache_write_1h"] += r.cache_write_1h
            u["cache_read_input_tokens"] += r.cache_read
            u["output_tokens"] += r.output_tokens
    return out


def run(repo_root, novel=None, rates=None, transcript_root=None, include_all=False,
        since=None, until=None, session=None):
    """Returns (Report, data). `data` is the same content, shaped for --json."""
    rates = rates or Rates()
    root = transcript_root or transcripts.default_root()
    rep = Report("trace - %s" % (novel.title if novel is not None else
                                 os.path.basename(os.path.abspath(repo_root))))
    data = {"transcript_root": root, "repo_root": os.path.abspath(repo_root)}

    if not os.path.isdir(root):
        rep.info("transcripts", [
            "   no transcript directory at %s" % root.replace(os.sep, "/"),
            "   nothing to measure - this is not a finding about the novel",
            "   set CLAUDE_CONFIG_DIR, or pass --transcripts <dir>",
        ])
        data["sessions"] = []
        return rep, data

    sessions = transcripts.sessions_for(repo_root, root, include_all=include_all,
                                        since=since, until=until, session=session)
    if not sessions:
        rep.info("transcripts", [
            "   searched %s" % root.replace(os.sep, "/"),
            "   no session reports a cwd inside %s" % os.path.abspath(repo_root).replace(os.sep, "/"),
            "   nothing to measure - this is not a finding about the novel",
        ])
        data["sessions"] = []
        return rep, data

    agg = transcripts.aggregate(sessions)
    per_model = _per_model(sessions)
    cost = total_cost(rates, per_model)
    data["totals"] = agg
    data["cost_usd"] = round(cost, 4)
    data["per_model"] = per_model

    _run_section(rep, sessions, agg)
    _token_section(rep, agg)
    _cost_section(rep, rates, per_model, cost, agg)
    _chapter_section(rep, sessions, rates, data, since)
    _skill_section(rep, repo_root, novel, agg, data)
    _tool_section(rep, agg)

    data["sessions"] = [{
        "file": s.rel, "kind": "subagent" if s.is_subagent else "session",
        "responses": len(s.responses), "rows": s.rows,
        "duration_s": s.duration_s, "first_ts": s.first_ts, "last_ts": s.last_ts,
        "totals": s.totals(), "naive": s.naive_totals,
        "skills": s.skills, "tools": s.tools,
    } for s in sessions]
    return rep, data


def _run_section(rep, sessions, agg):
    lines = ["   %-38s %-9s %6s %8s %9s" % ("transcript", "kind", "resp", "rows", "wall")]
    for s in sessions:
        lines.append("   %-38s %-9s %6d %8d %9s"
                     % (_short(s), "subagent" if s.is_subagent else "session",
                        len(s.responses), s.rows, _hms(s.duration_s)))
    lines.append("   %d session(s), %d API responses from %d transcript rows"
                 % (agg["sessions"], agg["responses"], agg["rows"]))
    worked = sum(s.duration_s for s in sessions)
    lines.append("   %s summed across sessions; %s from first row to last (they overlap, and "
                 "idle time between" % (_hms(worked), _hms(agg["duration_s"])))
    lines.append("   sessions counts in the second figure and not the first)")
    lines.append("   span %s -> %s" % (agg["first_ts"] or "?", agg["last_ts"] or "?"))
    lines.append("   models: %s" % (", ".join("%s x%d" % kv for kv in sorted(agg["models"].items()))
                                    or "none"))
    rep.info("run", lines)


def _token_section(rep, agg):
    naive = agg["naive"]
    rows = [
        ("input", agg["input_tokens"], naive["input_tokens"]),
        ("cache write", agg["cache_creation_input_tokens"], naive["cache_creation_input_tokens"]),
        ("  - 5m ttl", agg["cache_write_5m"], None),
        ("  - 1h ttl", agg["cache_write_1h"], None),
        ("cache read", agg["cache_read_input_tokens"], naive["cache_read_input_tokens"]),
        ("output", agg["output_tokens"], naive["output_tokens"]),
    ]
    lines = ["   %-14s %14s %14s %8s" % ("class", "tokens", "naive row-sum", "inflation")]
    for label, real, naive_v in rows:
        if naive_v is None:
            lines.append("   %-14s %14s" % (label, "{:,}".format(real)))
            continue
        ratio = ("%.2fx" % (naive_v / float(real))) if real else "-"
        lines.append("   %-14s %14s %14s %8s"
                     % (label, "{:,}".format(real), "{:,}".format(naive_v), ratio))
    lines.append("   Claude Code writes one row per content block and repeats `usage` on each,")
    lines.append("   so the naive column is what summing rows would have reported. It is shown")
    lines.append("   because benchmark run #1 was counted that way.")
    rep.info("tokens (one entry per API response)", lines)

    if agg["responses"] and agg["rows"]:
        inflate = naive["cache_read_input_tokens"] / float(agg["cache_read_input_tokens"] or 1)
        if inflate > 1.05:
            rep.note("accounting", "summing transcript rows would overstate cache reads by "
                                   "%.2fx here - %d rows carry %d responses"
                     % (inflate, agg["rows"], agg["responses"]))


def _cost_section(rep, rates, per_model, cost, agg):
    lines = []
    for model in sorted(per_model):
        u = per_model[model]
        lines.append("   %-20s %6d resp  $%8.2f"
                     % (model[:20], u["responses"], rates.cost(
                         model, input_tokens=u["input_tokens"],
                         cache_write_5m=u["cache_write_5m"],
                         cache_write_1h=u["cache_write_1h"],
                         cache_read=u["cache_read_input_tokens"],
                         output_tokens=u["output_tokens"])))
    lines.append("   %-20s %6s   $%8.2f total" % ("", "", cost))
    lines.append("")
    lines.extend(rates.describe(per_model.keys()))
    rep.info("cost (computed from tokens - the transcripts carry no cost field)", lines)
    for model in sorted(rates.unpriced):
        rep.warn("rates", "no published rate for model `%s` - it contributes $0.00 above; "
                          "add it with --rates" % model)


def _chapter_section(rep, sessions, rates, data, since=None):
    buckets = transcripts.by_chapter(sessions, since=since)
    data["by_chapter"] = buckets
    if not buckets:
        return
    lines = ["   %-20s %4s %6s %9s %13s %10s %9s  %s"
             % ("novel", "ch", "resp", "wall", "cache read", "output", "cost", "last write")]
    quick = []
    for b in buckets:
        b["cost_usd"] = round(total_cost(rates, b["by_model"]), 4)
        pre = b["chapter"] == 0
        lines.append("   %-20s %4s %6d %9s %13s %10s %9s  %s"
                     % (b["slug"][:20], "-" if pre else b["chapter"], b["responses"],
                        _hms(b["duration_s"]),
                        "{:,}".format(b["cache_read_input_tokens"]),
                        "{:,}".format(b["output_tokens"]),
                        "$%.2f" % b["cost_usd"], (b["until"] or "?")[:19]))
        if not pre and b["responses"] and b["duration_s"] < 30:
            quick.append(b["chapter"])
    lines.append("   Rows are in order of last write, which is not chapter order when a later")
    lines.append("   session revised an earlier chapter.")
    lines.append("   Attributed by the LAST write of each chapter file: a revision rewrites it,")
    lines.append("   and anchoring on the first would push revision cost into the next bucket.")
    lines.append("   The first chapter's row therefore absorbs the setup that preceded it.")
    if buckets and buckets[0]["chapter"] == 0:
        lines.append("   `(before --since)` is everything the window excludes, kept visible "
                     "rather than folded into chapter 1.")
    elif not since and len(sessions) > 1:
        lines.append("   No --since: every session ever run in this repo is in these numbers, "
                     "and the first chapter's bucket absorbs all of them.")
    rep.info("per chapter", lines)
    if quick:
        rep.warn("trace-attribution",
                 "chapter(s) %s hold under 30 seconds of work - attribution anchors on each "
                 "file's LAST write, so an end-of-run cleanup sweep across several chapters "
                 "moves their real cost into whichever chapter was touched before it"
                 % ", ".join(str(c) for c in quick),
                 detail="benchmark run #2, F5: five chapters resolved to $11.76/$6.30/$1.28/"
                        "$0.23/$0.11 this way. Only the run total was trustworthy.")


def _skill_section(rep, repo_root, novel, agg, data):
    roster = _skill_roster(repo_root)
    if not roster:
        rep.warn("skills", "no .claude/skills/ under %s - cannot tell which skills loaded"
                 % os.path.abspath(repo_root).replace(os.sep, "/"))
        return
    opened = agg["skills"]
    in_play, off = _classify(roster, novel)
    never = [s for s in in_play if s not in opened]
    data["skills"] = {"roster": roster, "opened": opened, "in_play": in_play,
                      "off_for_this_novel": off, "in_play_never_opened": never}

    known = set(roster)
    mine = dict((k, v) for k, v in opened.items() if k in known)
    foreign = dict((k, v) for k, v in opened.items() if k not in known)
    data["skills"]["opened_here"] = mine
    data["skills"]["opened_elsewhere"] = foreign

    lines = ["   %d of %d of this repo's skills opened" % (len(mine), len(roster))]
    if mine:
        hits = sorted(mine.items(), key=lambda kv: (-kv[1], kv[0]))
        lines.append("   opened: " + "  ".join("%s x%d" % (k, v) for k, v in hits))
    if foreign:
        # Bundled skills and slash commands come through the same `Skill` tool. They are not
        # this repo's and must not inflate the denominator.
        hits = sorted(foreign.items(), key=lambda kv: (-kv[1], kv[0]))
        lines.append("   not this repo's skills: "
                     + "  ".join("%s x%d" % (k, v) for k, v in hits))
    if off:
        lines.append("   off for this novel: " + "  ".join(off))
    if never:
        lines.append("   in play, never opened: " + "  ".join(never))
    rep.info("skills", lines)

    # Only a run that opened skills at all is evidence about which ones it skipped. A trace over
    # sessions that never wrote a chapter would otherwise report every skill as missing.
    if mine and never:
        rep.warn("skills", "%d skill(s) CLAUDE.md section 3 lists as always in play were never "
                           "opened in this run: %s" % (len(never), ", ".join(never[:8])),
                 detail="benchmark finding 9. A skill whose file never enters context contributes "
                        "only whatever another skill paraphrases of it.")


def _tool_section(rep, agg):
    tools = agg["tools"]
    if not tools:
        return
    rep.info("tools", ["   " + "  ".join("%s x%d" % kv for kv in
                                         sorted(tools.items(), key=lambda kv: (-kv[1], kv[0])))])
