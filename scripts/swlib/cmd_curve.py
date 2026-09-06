"""`sw curve` - the shape of the MC's power curve, and whether it is still entertaining.

power-scaling owns the distance between the MC and the opposition. This module finds the
countable half of that: a gain bigger than one tier, a gain missing one of its four
requirements, a boost whose debt was never paid, a stretch with no variation, a pressure value
that disagrees with the ledger. It cannot tell whether a gain was earned on the page or whether
an opponent is a person rather than a number; those stay in the audit card.
"""

import os
import re

from .report import Report

BLANK = ("", "-", "—", "–", "n/a", "tbd", "?", "none")
MONOTONY_WINDOW = 10
BANDS = [(2, "hopeless"), (1, "outmatched"), (0, "even"), (-1, "favoured"), (-2, "trivial")]


def _blank(val):
    return str(val).strip().strip("*").lower() in BLANK


def _int(val, default=None):
    m = re.search(r"-?\d+", str(val))
    return int(m.group(0)) if m else default


def _band(p):
    if p >= 2:
        return "hopeless"
    if p <= -2:
        return "trivial"
    return {1: "outmatched", 0: "even", -1: "favoured"}[p]


def _yes(val):
    return str(val).strip().strip("*").lower() in ("yes", "y", "true", "x", "✓")


def run(novel):
    rep = Report("curve - %s" % novel.title)
    if not novel.has_scaling:
        rep.note("curve", "scaling.shape is `none` - power-scaling is off for this novel")
        return rep

    ppath = novel.path("state", "power.md")
    if not os.path.isfile(ppath):
        rep.defect("curve-files", "scaling.shape is `%s` but state/power.md is missing - the "
                   "curve cannot be tracked without it" % novel.scaling_shape,
                   path=novel.path("novel.md"))
        return rep

    last_ch = max([c.number for c in novel.chapters() if c.number] or [0])
    _config(novel, rep)
    gains = _gains(novel, rep, ppath)
    _boosts(novel, rep, ppath, last_ch)
    _pressure(novel, rep, ppath, gains, last_ch)
    return rep


def _config(novel, rep):
    """The frontmatter contradictions, which cost nothing to find and shape everything."""
    npath = novel.path("novel.md")
    shape = novel.scaling_shape
    start = novel.scaling_int("start_tier", 1)
    tiers = novel.scaling_int("tiers", 7)
    ceiling = novel.scaling_int("ceiling_tier", tiers)

    if shape == "climb" and start > 2:
        rep.defect("curve-config", "scaling.shape is `climb` but start_tier is %d - a reader "
                   "will not invest in a climb that has already happened. Lower it, or the "
                   "shape is `inverted` or `plateau-late`" % start, path=npath)
    if shape == "inverted" and _blank(novel.get("scaling.substitute_tension", "")):
        rep.defect("curve-config", "scaling.shape is `inverted` but substitute_tension is empty "
                   "- an unbeatable MC is a valid book only when you have written down what the "
                   "story runs on instead", path=npath)
    if _blank(novel.get("scaling.endgame", "")):
        rep.warn("curve-config", "scaling.endgame is empty - a ladder with no top is how the "
                 "escalating sky starts. Name the final opposition and its tier", path=npath)

    edge = novel.scaling_int("edge_worth", 1)
    if edge > 1:
        rep.defect("curve-config", "scaling.edge_worth is %d - the edge closes a gap of at most "
                   "1. Above that it is a tier, not an advantage" % edge, path=npath)
    if edge > 0 and _blank(novel.get("scaling.edge_price", "")):
        rep.defect("curve-config", "edge_worth is %d but edge_price is empty - an advantage that "
                   "closes a tier for free flattens the ladder" % edge, path=npath)

    first_win = novel.get("opening.first_win_by_ch")
    first_limit = novel.scaling_int("first_limit_by_ch", 8)
    if isinstance(first_win, int) and first_limit <= first_win:
        rep.defect("curve-config", "first_limit_by_ch (%d) is not after opening.first_win_by_ch "
                   "(%d) - the advantage must work legibly before it hits a wall, or the reader "
                   "was promised something the book never showed them"
                   % (first_limit, first_win), path=npath)
    if ceiling > tiers:
        rep.defect("curve-config", "ceiling_tier (%d) is above the ladder (tiers: %d)"
                   % (ceiling, tiers), path=npath)


def _gains(novel, rep, ppath):
    """The step rule: +1 at most, and all four requirements present."""
    rows = novel.gain_rows()
    tiers = novel.scaling_int("tiers", 7)
    ceiling = novel.scaling_int("ceiling_tier", tiers)
    gap_min = novel.scaling_int("gain_gap_min", 15)
    seen = []

    for r in rows:
        ch = _int(r.first())
        if ch is None:
            continue
        move = r.get("from → to") or r.get("from to") or r.get("fromto")
        nums = re.findall(r"\d+", move)
        if len(nums) >= 2:
            frm, to = int(nums[0]), int(nums[1])
            if to - frm > 1:
                rep.defect("curve-gain", "ch %d advances %d tiers (%d to %d) - a permanent gain "
                           "is +1. Split it across arcs, or make it a boost with an expiry and "
                           "a debt" % (ch, to - frm, frm, to), path=ppath, line=r.line_no)
            if to > ceiling:
                rep.warn("curve-gain", "ch %d reaches tier %d, above ceiling_tier %d"
                         % (ch, to, ceiling), path=ppath, line=r.line_no)
            seen.append((ch, to))
        else:
            rep.warn("curve-gain", "ch %d has no readable `from → to` tiers" % ch,
                     path=ppath, line=r.line_no)

        for col, why in (("source", "nothing is found in a cave by luck"),
                         ("price paid (ch)", "paid after, it is a receipt"),
                         ("set up in ch", "a capability introduced where it is needed is a "
                                          "deus ex machina"),
                         ("new problem", "if it only solves things, do not grant it")):
            if _blank(r.get(col)):
                rep.defect("curve-gain", "ch %d gain has no `%s` - %s" % (ch, col, why),
                           path=ppath, line=r.line_no)

        paid = _int(r.get("price paid (ch)"))
        if paid is not None and paid > ch:
            rep.defect("curve-gain", "ch %d gain records its price paid in ch %d, after the gain "
                       "landed - the price comes first or it is not a decision" % (ch, paid),
                       path=ppath, line=r.line_no)
        setup = _int(r.get("set up in ch"))
        lead = novel.scaling_int("setup_lead", 3)
        if setup is not None and ch - setup < lead:
            rep.defect("curve-gain", "ch %d gain was set up in ch %d, %d chapter(s) ahead; "
                       "setup_lead is %d" % (ch, setup, ch - setup, lead),
                       path=ppath, line=r.line_no)

    seen.sort()
    for i in range(1, len(seen)):
        gap = seen[i][0] - seen[i - 1][0]
        if gap < gap_min:
            rep.warn("curve-gain", "gains at ch %d and ch %d are %d chapters apart; gain_gap_min "
                     "is %d - gains this close stop registering"
                     % (seen[i - 1][0], seen[i][0], gap, gap_min), path=ppath)
    return seen


def _boosts(novel, rep, ppath, last_ch):
    """Plot armour is allowed. Free plot armour is not."""
    rows = novel.boost_rows()
    due_window = novel.scaling_int("boost_debt_due", 5)
    climaxes = []

    for r in rows:
        ch = _int(r.first())
        if ch is None:
            continue
        for col in ("above tier by", "expires ch", "the debt", "due ch"):
            if _blank(r.get(col)):
                rep.defect("curve-boost", "ch %d boost has no `%s` - a boost decided after it "
                           "is used is plot armour" % (ch, col), path=ppath, line=r.line_no)
        due = _int(r.get("due ch"))
        if due is not None and due - ch > due_window:
            rep.warn("curve-boost", "ch %d boost's debt is due at ch %d, %d chapters out; "
                     "boost_debt_due is %d" % (ch, due, due - ch, due_window),
                     path=ppath, line=r.line_no)
        if due is not None and due < last_ch and not _yes(r.get("paid?")):
            rep.defect("curve-boost", "ch %d boost's debt was due at ch %d and is still unpaid "
                       "at ch %d - the novel spent the reader's trust and did not settle up"
                       % (ch, due, last_ch), path=ppath, line=r.line_no)
        if _yes(r.get("climax?")):
            climaxes.append((ch, r))

    if len(climaxes) > 1:
        first = climaxes[0][0]
        for ch, r in climaxes[1:]:
            rep.defect("curve-boost", "ch %d is a second boost resolving an arc climax (the "
                       "first was ch %d) - the reader has now learned that arc endings are not "
                       "decided by anything they were shown" % (ch, first),
                       path=ppath, line=r.line_no)


def _pressure(novel, rep, ppath, gains, last_ch):
    """The gap itself: does it vary, and does the ledger agree with the CCS blocks?"""
    rows = novel.pressure_rows()
    lpath = novel.path("state", "continuity.md")
    series = []

    for r in rows:
        ch = _int(r.first())
        p = _int(r.get("P"))
        if ch is None or p is None:
            continue
        their = _int(r.get("their tier"))
        mine = _int(r.get("MC tier"))
        if their is not None and mine is not None and their - mine != p:
            rep.defect("curve-pressure", "ch %d records P=%d but its tiers give %d"
                       % (ch, p, their - mine), path=ppath, line=r.line_no)
        if p >= 1 and _blank(r.get("what it cost")):
            rep.defect("curve-pressure", "ch %d is at P=%+d with no recorded cost - a win when "
                       "outmatched costs something that is still costing at the end of the "
                       "chapter" % (ch, p), path=ppath, line=r.line_no)
        series.append((ch, p))

    _ccs_agreement(novel, rep, lpath, dict(series))

    if not series:
        return
    series.sort()

    trivial_per_arc = novel.scaling_int("trivial_per_arc", 2)
    arc_len = novel.arc_length
    by_arc = {}
    for ch, p in series:
        if p <= -2:
            by_arc.setdefault((ch - 1) // arc_len + 1, []).append(ch)
    for arc, chs in sorted(by_arc.items()):
        if len(chs) > trivial_per_arc:
            rep.warn("curve-pressure", "arc %d has %d confrontations at P <= -2 (ch %s); "
                     "trivial_per_arc is %d - this is the face-slap treadmill"
                     % (arc, len(chs), ", ".join(str(c) for c in chs), trivial_per_arc),
                     path=ppath)

    window = series[-MONOTONY_WINDOW:]
    if len(window) >= MONOTONY_WINDOW and len({_band(p) for _, p in window}) == 1:
        rep.warn("curve-pressure", "the last %d confrontations are all in the `%s` band - the "
                 "fights have become a texture. The range is the entertainment"
                 % (len(window), _band(window[0][1])), path=ppath)

    _flat(novel, rep, ppath, series, gains, last_ch)
    _drift(rep, ppath, series, gains)
    rep.info("curve", _render(series, gains))


def _ccs_agreement(novel, rep, lpath, by_ch):
    """The `pwr>` line and the ledger must agree, the way `wc:` and the body must."""
    for b in novel.blocks():
        keys = b.keys()
        if "pwr" not in keys:
            rep.warn("curve-ccs", "block =C%04d= has no `pwr>` line, but scaling.shape is `%s` "
                     "- record the pressure, or record that nothing was contested"
                     % (b.number, novel.scaling_shape), path=lpath, line=b.line_no)
            continue
        m = re.search(r"\bP\s*=?\s*([+-]?\d+)", " ".join(keys["pwr"]))
        if not m:
            continue
        p = int(m.group(1))
        if b.number in by_ch and by_ch[b.number] != p:
            rep.defect("curve-ccs", "block =C%04d= records P=%+d, state/power.md records P=%+d"
                       % (b.number, p, by_ch[b.number]), path=lpath, line=b.line_no)
        elif b.number not in by_ch:
            rep.warn("curve-ccs", "block =C%04d= records P=%+d but has no row in state/power.md "
                     "section 3" % (b.number, p), path=lpath, line=b.line_no)


def _flat(novel, rep, ppath, series, gains, last_ch):
    """No tier movement AND no pressure variation - the progression reader's exit point.

    A run ends at a gain or at a change of band. The tail is measured against the last chapter
    on disk rather than the last logged row, because a long stretch with no confrontations at
    all is the flat middle in its purest form.
    """
    flat_max = novel.scaling_int("flat_max", 12)
    gain_chs = {ch for ch, _ in gains}
    run_start, run_bands = series[0][0], set()

    def flag(start, end):
        rep.warn("curve-flat", "ch %d-%d: no tier movement and no pressure variation across %d "
                 "chapters; flat_max is %d - vary the pressure rather than granting a gain"
                 % (start, end, end - start, flat_max), path=ppath)

    for ch, p in series:
        if ch in gain_chs or (run_bands and _band(p) not in run_bands):
            run_start, run_bands = ch, {_band(p)}
            continue
        run_bands.add(_band(p))
        if ch - run_start >= flat_max:
            flag(run_start, ch)
            run_start, run_bands = ch, {_band(p)}
    if last_ch - run_start >= flat_max:
        flag(run_start, last_ch)


def _drift(rep, ppath, series, gains):
    """Tier rising while pressure falls. This is power creep, measured."""
    if len(series) < 6 or len(gains) < 2:
        return
    half = len(series) // 2
    early = sum(p for _, p in series[:half]) / float(half)
    late = sum(p for _, p in series[half:]) / float(len(series) - half)
    tier_early, tier_late = gains[0][1], gains[-1][1]
    if tier_late > tier_early and late < early - 0.5:
        rep.warn("curve-drift", "the MC climbed from tier %d to tier %d while average pressure "
                 "fell from %+.1f to %+.1f - power has outrun the story. Raise the opposition "
                 "with the plan, not after the fact"
                 % (tier_early, tier_late, early, late), path=ppath)


def _render(series, gains):
    """The curve, so a human can see the shape the checks are describing."""
    tier_at, cur = {}, None
    for ch, to in gains:
        tier_at[ch] = to
    out = ["   %-7s %-6s %-11s %s" % ("ch", "P", "band", "gain")]
    for ch, p in series:
        if ch in tier_at:
            cur = tier_at[ch]
        out.append("   %-7d %-+6d %-11s %s"
                   % (ch, p, _band(p), "-> tier %d" % cur if ch in tier_at else ""))
    return out
