"""`sw arc` - the distributional pass, run at an arc boundary.

Every defect this format actually suffers is distributional. Dialogue starvation, word-count
clustering, voice convergence, an unpaid promise, a foreknowledge advantage that never wins,
the same delivery twice - none of them is visible in the chapter you are holding, and
`revision-pass` only ever holds one. All five high-severity findings from benchmark run #1 were
of this kind, and all five were found by lining five chapters up next to each other.

So this command lines them up. It prints trends, spreads, rotations and ages, and it hands the
model a short list of places to look. It does not score the arc, and it must not: the strongest
off-the-shelf judges agree with human preference on creative writing about 73% of the time, and
a number attached to a chapter is a number the next chapter gets written toward.

Two things it prints and never judges: word counts, and the delivery of any individual chapter.
"""

import re

from . import mdio, rules
from .report import Report

# Two `delivers:` this similar in one arc usually means the second chapter re-delivered the
# first one's change rather than making a new one.
DUP_DELIVERS_RATIO = 0.6


def _norm(text):
    return set(re.findall(r"[a-z']+", str(text).lower()))


def _similar(a, b):
    wa, wb = _norm(a), _norm(b)
    if len(wa) < 3 or len(wb) < 3:
        return 0.0
    return len(wa & wb) * 2.0 / (len(wa) + len(wb))


def _cluster(items, threshold):
    """Group (number, text) pairs into near-duplicate clusters.

    Reported as groups rather than pairs: twenty identical hooks are one finding a reader can
    act on, not a hundred and ninety.
    """
    groups = []
    for num, text in items:
        for g in groups:
            if _similar(g[0][1], text) >= threshold:
                g.append((num, text))
                break
        else:
            groups.append([(num, text)])
    return [g for g in groups if len(g) > 1]


def _arc_range(novel, arc):
    """Chapters belonging to an arc.

    The ledger's `arc:` field is the authority, but the range is widened to the arithmetic arc
    as well: a chapter written without its CCS block has no `arc:` anywhere, and narrowing to
    the ledger would make exactly that chapter invisible to the pass that exists to find it.
    """
    n = novel.arc_length
    lo, hi = (arc - 1) * n + 1, arc * n
    numbered = [b.number for b in novel.blocks()
                if b.number is not None and b.arc == arc]
    if numbered:
        lo, hi = min(lo, min(numbered)), max(hi, max(numbered))
    written = [c.number for c in novel.chapters() if c.number and lo <= c.number <= hi]
    if written:
        hi = max(hi, max(written))
    return lo, hi


def _pick_arc(novel, requested):
    if requested:
        return requested
    arcs = [b.arc for b in novel.blocks() if b.arc is not None]
    if arcs:
        return max(arcs)
    numbers = [c.number for c in novel.chapters() if c.number]
    return ((max(numbers) - 1) // novel.arc_length + 1) if numbers else 1


def run(novel, arc=None):
    arc = _pick_arc(novel, arc)
    lo, hi = _arc_range(novel, arc)
    rep = Report("arc %d (ch %d-%d) - %s" % (arc, lo, hi, novel.title))

    chapters = [c for c in novel.chapters() if c.number and lo <= c.number <= hi]
    blocks = [b for b in novel.blocks() if b.number and lo <= b.number <= hi]
    if not chapters:
        rep.defect("arc", "no chapters in range %d-%d" % (lo, hi))
        return rep

    _shape(novel, rep, arc, chapters, blocks)
    _register(novel, rep, chapters)
    _delivery(rep, chapters)
    _cast(novel, rep, blocks)
    _hooks(rep, blocks)
    _threads(novel, rep, blocks, lo, hi)
    _foreknowledge(novel, rep, blocks)
    _curve(novel, rep, lo, hi)
    _judged(novel, rep, arc)
    return rep


def _shape(novel, rep, arc, chapters, blocks):
    """The per-chapter table. Length is printed as a fact and scored on nothing."""
    lines = ["   %-5s %7s %8s %7s %6s %s" % ("ch", "words", "dialogue", "anchor", "block", "pov")]
    have = {b.number for b in blocks}
    shares = []
    for c in chapters:
        share = c.speech_share
        shares.append(share)
        anchors = sum(1 for _t, rx in novel.anchor_terms() if rx.search(c.body))
        lines.append("   %-5s %7d %7.1f%% %7d %6s %s"
                     % (c.number, c.words, share, anchors,
                        "yes" if c.number in have else "MISSING",
                        c.meta.get("pov", "-")))
    rep.info("chapters", lines)

    missing = sorted(c.number for c in chapters if c.number not in have)
    if missing:
        rep.defect("arc-ledger", "no CCS block for chapter(s) %s - a chapter written without its "
                   "block is a bug" % ", ".join(str(m) for m in missing),
                   path=novel.path("state", "continuity.md"))

    if shares:
        lo_s, hi_s = min(shares), max(shares)
        starved = [c.number for c, s in zip(chapters, shares) if s < 10.0]
        rep.info("dialogue", [
            "   share across the arc: %.1f%% - %.1f%% (mean %.1f%%)"
            % (lo_s, hi_s, sum(shares) / len(shares)),
            "   a whole arc under 25% is the defect run #1 shipped five times",
        ])
        if starved:
            rep.defect("arc-dialogue", "chapter(s) %s are under 10%% spoken - on a silent cast "
                       "every voice check in the toolkit silently no-ops"
                       % ", ".join(str(s) for s in starved))
        elif sum(shares) / len(shares) < 25.0:
            rep.warn("arc-dialogue", "arc mean dialogue share is %.1f%%, under the 25-40%% band"
                     % (sum(shares) / len(shares)))

    words = sorted(c.words for c in chapters)
    if len(words) >= 5:
        spread = words[-1] - words[0]
        rep.info("length", [
            "   %d-%d words, median %d, spread %d" % (words[0], words[-1],
                                                      words[len(words) // 2], spread),
            "   reported, never scored. A tight spread is a style; a spread of under 100 words",
            "   across five chapters is a model writing to a number - check nothing is being",
            "   padded or cut to land there.",
        ])

    # Shrinkage, as a signal about event density rather than about length.
    #
    # docs/design-notes.md is right that any number gating a chapter gets optimised, and no
    # number here gates anything. But run #2 ran 1938 -> 1457 -> 1323 -> 1213 -> 1151, and a
    # chapter that is 41% shorter than chapter 1 while the state files grow is usually a chapter
    # with less happening in it, not a tighter one. Print the slide; let the model look.
    seq = [(c.number, c.words) for c in chapters]
    run_len, start = 1, 0
    for i in range(1, len(seq)):
        if seq[i][1] < seq[i - 1][1]:
            run_len += 1
        else:
            run_len, start = 1, i
        if run_len > rules.DECLINE_RUN:
            drop = 100.0 * (seq[start][1] - seq[i][1]) / float(seq[start][1] or 1)
            rep.warn("arc-shrinkage",
                     "chapters %d-%d get shorter every chapter (%d -> %d words, -%.0f%%) - "
                     "not a length problem in itself, but check the events are not thinning "
                     "with them"
                     % (seq[start][0], seq[i][0], seq[start][1], seq[i][1], drop))
            break


def _register(novel, rep, chapters):
    """Temperature and hook shape across the arc.

    Nothing in this toolkit tracked register before, which is why run #2 did not have one: five
    chapters, one temperature, one hook shape, and prose that a reader flagged as machine-made
    without being able to point at a sentence. Sameness is invisible from inside a single
    chapter and obvious from four feet away, so it belongs here with the other distributional
    checks rather than in `revision-pass`.

    Declared at plan time, checked as a distribution, scored never.
    """
    rows = [(c.number, novel.plan_row(c.number)) for c in chapters]
    got = [(n, r.get("temp", "").strip().lower(), r.get("hooktype", "").strip().lower())
           for n, r in rows if r is not None]
    if not any(t or h for _n, t, h in got):
        rep.note("register", "no `temp` / `hooktype` columns filled in plan/chapters.md for this "
                 "arc - the register ledger is how the arc avoids one temperature",
                 path=novel.path("plan", "chapters.md"))
        return

    rep.info("register", ["   %-5s %-11s %s" % ("ch", "temp", "hooktype")]
             + ["   %-5s %-11s %s" % (n, t or "-", h or "-") for n, t, h in got])

    temps = [t for _n, t, _h in got if t]
    hooks = [h for _n, _t, h in got if h]

    run_val, run_len, run_at = None, 0, None
    for n, t, _h in got:
        if t and t == run_val:
            run_len += 1
        else:
            run_val, run_len, run_at = t, 1, n
        if t and run_len > rules.TEMP_RUN_MAX:
            rep.warn("arc-register",
                     "`%s` runs %d chapters straight from ch %d - three chapters at one "
                     "temperature is where a reader starts skimming" % (t, run_len, run_at))
            break

    for i in range(len(got) - rules.HOOK_WINDOW + 1):
        window = [h for _n, _t, h in got[i:i + rules.HOOK_WINDOW] if h]
        if not window:
            continue
        for shape in set(window):
            if window.count(shape) > rules.HOOK_WINDOW_MAX:
                rep.warn("arc-register",
                         "hook shape `%s` used %d times in chapters %d-%d - the eight shapes "
                         "exist so the reader cannot predict the last line"
                         % (shape, window.count(shape), got[i][0],
                            got[i + rules.HOOK_WINDOW - 1][0]))
                break
        else:
            continue
        break

    if len(chapters) >= rules.ARC_MIN_DISTINCT:
        if temps and len(set(temps)) < rules.ARC_MIN_DISTINCT:
            rep.warn("arc-register", "only %d distinct temperature(s) across the arc (%s) - "
                     "aim for %d. A quiet chapter is earned by a loud one"
                     % (len(set(temps)), ", ".join(sorted(set(temps))), rules.ARC_MIN_DISTINCT))
        if hooks and len(set(hooks)) < rules.ARC_MIN_DISTINCT:
            rep.warn("arc-register", "only %d distinct hook shape(s) across the arc (%s) - "
                     "aim for %d"
                     % (len(set(hooks)), ", ".join(sorted(set(hooks))), rules.ARC_MIN_DISTINCT))


def _delivery(rep, chapters):
    """`delivers:` present, and no two chapters delivering the same thing twice."""
    missing = [c.number for c in chapters if not str(c.meta.get("delivers", "")).strip()]
    if missing:
        rep.defect("arc-delivers", "chapter(s) %s have no `delivers:` - the Pass 9 gate was "
                   "never written down" % ", ".join(str(m) for m in missing))

    have = [(c.number, str(c.meta.get("delivers", ""))) for c in chapters
            if str(c.meta.get("delivers", "")).strip()]
    for group in _cluster(have, DUP_DELIVERS_RATIO):
        nums = ", ".join(str(n) for n, _t in group)
        rep.warn("arc-delivers", "chapters %s deliver nearly the same thing - after the first, "
                 "these may have re-delivered a change already made rather than making a new "
                 "one: %r" % (nums, group[0][1][:60]))


def _cast(novel, rep, blocks):
    """Who actually appeared. A matrix row nobody used is a character the arc forgot."""
    seen = {}
    for b in blocks:
        names = [b.pov] if b.pov else []
        for line in b.keys().get("chg", []):
            for part in line.split(";"):
                m = re.match(r"\s*([A-Z][\w'\-]*(?:\s+[A-Z][\w'\-]*)?)\s*:", part)
                if m:
                    names.append(m.group(1).strip())
        for n in names:
            if n:
                seen[n.lower()] = max(seen.get(n.lower(), 0), b.number)

    rows = novel.voice_rows()
    if not rows:
        return
    absent, present = [], []
    for r in rows:
        name = r.first().strip().strip("*")
        (present if name.lower() in seen else absent).append(name)
    rep.info("cast rotation", [
        "   on the page this arc: %s" % (", ".join(sorted(present)) or "nobody"),
        "   matrix rows absent:   %s" % (", ".join(sorted(absent)) or "none"),
    ])
    if len(present) == 1 and len(rows) > 1:
        rep.warn("arc-cast", "only one matrix character appears in the whole arc - the cast is "
                 "not being rotated, and voice separation has nothing to separate")


def _hooks(rep, blocks):
    """Hook rotation. The script shows them; whether they repeat in kind is a reading."""
    hooks = [(b.number, b.get("hook")) for b in blocks if b.get("hook")]
    if not hooks:
        return
    shown = hooks[:15]
    lines = ["   %-5d %s" % (n, h[:80]) for n, h in shown]
    if len(hooks) > len(shown):
        lines.append("   ... %d more" % (len(hooks) - len(shown)))
    lines += ["   rotation is a judgement: three cliffhangers running reads as a tic, and a",
              "   run of quiet closings reads as a stall."]
    rep.info("hooks", lines)
    for group in _cluster(hooks, 0.7):
        rep.warn("arc-hooks", "hooks on chapters %s are near-identical: %r"
                 % (", ".join(str(n) for n, _h in group), group[0][1][:60]))


def _threads(novel, rep, blocks, lo, hi):
    ops = {"~": [], "^": [], "v": [], "x": []}
    for b in blocks:
        for line in b.keys().get("thr", []):
            for op, tid in re.findall(r"([~^vx])(T\d+)", line):
                ops[op].append("%s@%d" % (tid, b.number))
    rep.info("threads this arc", [
        "   opened:    %s" % (", ".join(ops["~"]) or "none"),
        "   advanced:  %s" % (", ".join(ops["^"]) or "none"),
        "   paid:      %s" % (", ".join(ops["v"]) or "none"),
        "   abandoned: %s" % (", ".join(ops["x"]) or "none"),
    ])
    if not ops["v"] and not ops["x"]:
        # An arc still being written has not failed to pay off; it has not finished. Run at
        # chapter 1 this fired as a DEFECT on a 25-chapter arc. Benchmark run #2, F6.
        drafted = max([c.number for c in novel.chapters() if c.number] or [0])
        msg = ("chapters %d-%d opened %d thread(s) and closed none - perpetual deferral is the "
               "complaint readers drop long serials over (plot-threads section Ageing)"
               % (lo, hi, len(ops["~"])))
        path = novel.path("state", "threads.md")
        if drafted < hi:
            rep.note("arc-payoff", "%s. The arc is %d of %d chapters in, so this is a position, "
                     "not yet a verdict" % (msg, max(drafted - lo + 1, 0), hi - lo + 1), path=path)
        else:
            rep.defect("arc-payoff", msg, path=path)


def _foreknowledge(novel, rep, blocks):
    if not novel.has_foreknowledge:
        return
    spent = [b.number for b in blocks if b.has("fk")]
    win = novel.get("mc.foreknowledge_first_win_ch")
    fails = novel.get("mc.foreknowledge_fails_ch")
    lines = ["   fk> lines in this arc: %s" % (", ".join(str(s) for s in spent) or "none"),
             "   first_win_ch %s / fails_ch %s" % (win, fails)]
    rep.info("foreknowledge", lines)
    if not spent:
        rep.warn("arc-foreknowledge", "the MC knows the future and spent none of it across the "
                 "whole arc - an MC who never refers to knowing what is coming has wasted the "
                 "premise (meta-knowledge section 2)")
    if isinstance(win, int) and isinstance(fails, int) and win >= fails:
        rep.defect("arc-foreknowledge", "foreknowledge_first_win_ch (%d) is not before "
                   "foreknowledge_fails_ch (%d) - the advantage is scheduled to be corrected "
                   "before it has ever worked" % (win, fails),
                   path=novel.path("novel.md"))


def _curve(novel, rep, lo, hi):
    """The arc's power trend. `sw curve` judges the whole book; this is the slice."""
    if not novel.has_scaling:
        return
    rows = []
    for r in novel.pressure_rows():
        ch = _first_int(r)
        p = _first_int(r, "P")
        if ch is not None and p is not None and lo <= ch <= hi:
            rows.append((ch, p))
    gains = [(_first_int(r), r.get("from → to")) for r in novel.gain_rows()
             if _first_int(r) is not None and lo <= _first_int(r) <= hi]

    if not rows:
        rep.info("power curve", ["   no confrontations logged in this arc"])
        return
    ps = [p for _, p in rows]
    rep.info("power curve", [
        "   confrontations: %d   pressure %+d..%+d   mean %+.1f"
        % (len(ps), min(ps), max(ps), sum(ps) / float(len(ps))),
        "   gains this arc: %s" % (", ".join("ch %d %s" % (c, m.strip()) for c, m in gains)
                                   or "none"),
    ])
    if len(set(ps)) == 1:
        rep.warn("arc-curve", "every confrontation in this arc sat at P=%+d - the arc has one "
                 "gear (power-scaling section 1)" % ps[0])
    if not gains and len(rows) >= 4 and max(ps) <= 0:
        rep.warn("arc-curve", "no tier advance and nothing above P=0 across the arc - a "
                 "progression reader has no reason to start the next one")


def _first_int(row, column=None):
    text = row.get(column) if column else row.first()
    m = re.search(r"[+-]?\d+", str(text))
    return int(m.group(0)) if m else None


def _judged(novel, rep, arc):
    """The half a script cannot do. Named, so it is not quietly skipped."""
    items = [
        "   Open these and answer them by reading. Nothing above settles any of them:",
        "",
        "   1. Did the arc answer its dramatic question in plan/arcs.md - or move it?",
        "   2. Consistency across the arc: timeline, who knew what when, world rules,",
        "      established facts, and whether the narrating voice drifted.",
        "   3. Voice drift: read the first and last chapter's dialogue side by side. Has",
        "      anyone converged on the MC? (bible/cast/_voices.md, voice-separation)",
        "   4. Does the blurb still describe this book? (novel.md, the Hook section)",
        "   5. Tension shape: where did the arc turn, and does the shape have a middle -",
        "      or is it flat until the last two chapters?",
        "   6. Could a reader have predicted this arc's ending from its first chapter?",
    ]
    if novel.get("theme.controlling_idea"):
        items.append("   7. Did a choice test theme.controlling_idea, and did the counter-case")
        items.append("      get the better of an argument anywhere in it?")
    items += [
        "",
        "   Report what you found. Do not score the arc: judged scores on prose are ~73%",
        "   agreement with human preference at best, and a scored arc is an arc the next",
        "   one gets written toward.",
    ]
    rep.info("the judged half", items)
