"""`sw cast` - the distributional audits on the two cast tables.

voice-separation section 3 and competence-map section 2 are arithmetic over a table: whether
the cast straddles the MC's tier, how many people are funny, whether two rows are the same
person twice, and whether anyone has quietly accumulated expertise past their budget. Those
are exactly the defects a per-chapter read cannot see and a script can settle outright.

What it cannot do: decide whether the drafted dialogue honours the row. The script says the
matrix is well-formed; the model still says the chapter is.
"""

import re

from .report import Report

# competence-map: deep-expertise budget, by cast tier.
DEEP_LEVELS = ("exceptional", "best alive")
DEEP_BUDGET = {"mc": 3, "a": 2, "b": 1, "c": 1}


def _int(val, default=None):
    m = re.search(r"-?\d+", str(val))
    return int(m.group(0)) if m else default


def _wit(val):
    w = str(val).strip().lower()
    w = re.sub(r"\(.*?\)", "", w).strip()
    return "" if w in ("none", "-", "") else w


def run(novel):
    rep = Report("cast - %s" % novel.title)
    voices = novel.voice_rows()
    comps = novel.competence_rows()
    vpath = novel.path("bible", "cast", "_voices.md")
    cpath = novel.path("bible", "cast", "_competence.md")

    if not voices:
        rep.defect("voices", "no matrix rows found in bible/cast/_voices.md", path=vpath)
        return rep

    mc_name = str(novel.get("mc.name", "")).strip()
    mc_tier = _int(novel.get("mc.intel_tier"), None)

    rows = []
    for r in voices:
        rows.append({
            "name": r.first(),
            "tier": str(r.get("tier", "")).strip().upper(),
            "intel": _int(r.get("intel")),
            "artic": _int(r.get("artic")),
            "wit": _wit(r.get("wit")),
            "turn": _int(r.get("turn")),
            "hands": str(r.get("hands", "")).strip().lower(),
            "line": r.line_no,
        })

    rep.info("voice matrix (%d rows)" % len(rows), [
        "   %-12s tier %-2s intel %-4s artic %-4s wit %-10s turn %s"
        % (x["name"], x["tier"], x["intel"], x["artic"], x["wit"] or "none", x["turn"])
        for x in rows])

    _mc_row(rep, rows, mc_name, mc_tier, vpath)
    _straddle(rep, rows, mc_name, mc_tier, vpath)
    _wit_cap(rep, rows, vpath)
    _clash(rep, rows, vpath)
    _turns_and_hands(rep, rows, vpath)
    _competence(rep, novel, rows, comps, cpath)
    return rep


def _mc_row(rep, rows, mc_name, mc_tier, vpath):
    if not mc_name:
        return
    mc = [x for x in rows if x["name"].lower() == mc_name.lower()]
    if not mc:
        rep.defect("voices", "the MC (%s) has no row in the matrix - it is the calibration "
                   "point for every other row" % mc_name, path=vpath)
        return
    if mc_tier is not None and mc[0]["intel"] is not None and mc[0]["intel"] != mc_tier:
        rep.defect("voices", "matrix gives %s intel %s, novel.md declares intel_tier %s"
                   % (mc_name, mc[0]["intel"], mc_tier), path=vpath, line=mc[0]["line"])


def _straddle(rep, rows, mc_name, mc_tier, vpath):
    """voice-separation section 3: somebody above the MC, somebody below."""
    if mc_tier is None:
        return
    others = [x for x in rows if x["name"].lower() != mc_name.lower() and x["intel"] is not None]
    if not others:
        return
    above = [x["name"] for x in others if x["intel"] > mc_tier]
    below = [x["name"] for x in others if x["intel"] < mc_tier]
    if not above:
        rep.defect("straddle", "nobody in the cast is above the MC's intel tier (%d) - the "
                   "MC is the ceiling, which is how a cast becomes one mind" % mc_tier, path=vpath)
    if not below:
        rep.defect("straddle", "nobody in the cast is below the MC's intel tier (%d) - "
                   "somebody has to be slower and right about something anyway" % mc_tier,
                   path=vpath)
    if above and below:
        rep.info("straddle", ["   above the MC: %s | below: %s"
                             % (", ".join(above), ", ".join(below))])


def _wit_cap(rep, rows, vpath):
    """voice-separation: real wit for at most two of the recurring cast."""
    funny = [x for x in rows if x["wit"]]
    if len(funny) > 2:
        rep.defect("wit-cap", "%d characters have wit (%s) - the cap is two. If everyone is "
                   "funny, nobody is" % (len(funny), ", ".join(x["name"] for x in funny)),
                   path=vpath)


def _clash(rep, rows, vpath):
    """voice-separation: no two speakers share intel + artic + wit."""
    seen = {}
    for x in rows:
        key = (x["intel"], x["artic"], x["wit"])
        if None in key[:2]:
            continue
        if key in seen:
            rep.defect("three-way-clash",
                       "%s and %s share intel %s + artic %s + wit %s - one of them has no "
                       "reason to exist separately; re-cast or merge"
                       % (seen[key], x["name"], x["intel"], x["artic"], x["wit"] or "none"),
                       path=vpath, line=x["line"])
        else:
            seen[key] = x["name"]


def _turns_and_hands(rep, rows, vpath):
    turns = {}
    for x in rows:
        if x["turn"] is None:
            rep.warn("turn-length", "%s has no default turn length - it is the crudest "
                     "separator here and the most reliable" % x["name"],
                     path=vpath, line=x["line"])
            continue
        turns.setdefault(x["turn"], []).append(x["name"])
    for turn, names in sorted(turns.items()):
        if len(names) > 1:
            rep.warn("turn-length", "%s share a turn length of %d words"
                     % (" and ".join(names), turn), path=vpath)

    hands = {}
    for x in rows:
        if not x["hands"] or x["hands"] == "-":
            rep.defect("body-idiom", "%s has no hand-habit - that field is what does the "
                       "tag-free identification" % x["name"], path=vpath, line=x["line"])
            continue
        hands.setdefault(x["hands"], []).append(x["name"])
    for habit, names in hands.items():
        if len(names) > 1:
            rep.defect("body-idiom", "%s share the same hand-habit (%s)"
                       % (" and ".join(names), habit[:40]), path=vpath)


def _competence(rep, novel, vrows, comps, cpath):
    """competence-map section 2 (budget) and section 7 (distribution)."""
    if not comps:
        rep.defect("competence", "no grid rows found in bible/cast/_competence.md", path=cpath)
        return

    mc_name = str(novel.get("mc.name", "")).strip().lower()
    tiers = {x["name"].lower(): x["tier"] for x in vrows}

    per_char = {}
    for r in comps:
        name = r.first()
        level = str(r.get("level", "")).lower()
        deep = any(d in level for d in DEEP_LEVELS)
        rec = per_char.setdefault(name, {"domains": 0, "deep": 0, "line": r.line_no})
        rec["domains"] += 1
        if deep:
            rec["deep"] += 1

    lines = []
    for name in sorted(per_char):
        rec = per_char[name]
        key = "mc" if name.lower() == mc_name else tiers.get(name.lower(), "C").lower()
        budget = DEEP_BUDGET.get(key, 0)
        lines.append("   %-12s tier %-3s domains %d, above professional %d/%d"
                     % (name, key.upper(), rec["domains"], rec["deep"], budget))
        if rec["deep"] > budget:
            rep.defect("deep-budget",
                       "%s holds %d domains above professional; the budget for tier %s is %d"
                       % (name, rec["deep"], key.upper(), budget), path=cpath, line=rec["line"])
    rep.info("competence grid (%d rows)" % len(comps), lines)

    matrix_names = set(x["name"].lower() for x in vrows)
    grid_names = set(n.lower() for n in per_char)
    for missing in sorted(matrix_names - grid_names):
        rep.defect("competence", "%s is on the voice matrix but has no competence row - an "
                   "unlisted domain is `none`, so the row is what stops them answering "
                   "everything" % missing, path=cpath)
    for extra in sorted(grid_names - matrix_names):
        rep.warn("competence", "%s has competence rows but no voice-matrix row" % extra,
                 path=novel.path("bible", "cast", "_voices.md"))

    referrals = set(r.first().lower() for r in novel.referral_rows())
    for missing in sorted(matrix_names - referrals):
        rep.warn("referral", "%s has no referral - who they ask when it runs out is what "
                 "makes the edge produce a scene" % missing, path=cpath)

    if per_char:
        fewest = min(per_char.values(), key=lambda r: r["domains"])["domains"]
        thin = [n for n, r in per_char.items() if r["domains"] == fewest]
        rep.info("distribution", [
            "   thinnest maps: %s (%d domain(s) each)" % (", ".join(sorted(thin)), fewest),
            "   bias-guard section 7 asks whether the thin rows sort by gender, class or",
            "   people - that judgement is not scriptable; open bias-guard and make it."])
