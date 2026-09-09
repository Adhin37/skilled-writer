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
    _debuts(novel, rep, rows)
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
    _near_clash(rep, rows, vpath)


def _near_clash(rep, rows, vpath):
    """Two speakers alike on intel AND articulacy, differing only in wit.

    The three-way clash above is the rule as CLAUDE.md states it. This is the practical failure
    underneath it: wit is the weakest of the three axes - it is a label, and it can go a whole
    chapter without surfacing - while intel and articulacy decide how a line is built. Benchmark
    run #2 shipped a two-hander in which both speakers were intel 3 / artic 3 and a reader
    reported the dialogue as everyone sounding the same. `three-way-clash` passed it, correctly
    and uselessly.

    A warn, not a defect: two people can legitimately reason and speak at the same level, and a
    declared `mirror:` is exactly that. It wants a decision, not a gate.
    """
    pairs = {}
    for x in rows:
        key = (x["intel"], x["artic"])
        if None in key:
            continue
        pairs.setdefault(key, []).append(x)
    for (intel, artic), group in sorted(pairs.items()):
        if len(group) < 2:
            continue
        names = ", ".join(g["name"] for g in group)
        rep.warn("near-clash",
                 "%s share intel %s + artic %s and differ only in wit - wit is a label that can "
                 "go a chapter without surfacing, so on the page these are one voice. Separate "
                 "them on an axis that shapes a sentence, or declare a `mirror:`"
                 % (names, intel, artic), path=vpath, line=group[-1]["line"])


def _debuts(novel, rep, rows):
    """Where each character first appears, and how long the reader has before they speak.

    Benchmark run #2, reader report: "they are not even introduced. It feels like I should know
    them and everything in their life." Nothing in the toolkit looked at a character's *first*
    appearance - `cast` audits the matrix, `character-profile` owns the profile, `story-opening`
    owns the world anchor, and between them a named character can walk on with no placement at
    all and every check stays green. Chapter 1 of that run: "she went to find Enko before Enko
    found the discrepancy first", and four lines later Enko is in a loaded argument.

    This prints; it does not score. The `speaks after` column is the countable half of the
    complaint - a small number means a name arrived and started talking before the reader could
    place it. Whether that is a defect is a craft judgement and stays with the human.
    """
    chapters = [c for c in novel.chapters() if c.number]
    if not chapters:
        return
    world = _world_terms(novel)
    lines = ["   %-24s %-7s %-9s %-12s %-10s %s"
             % ("character", "debut", "at word", "speaks after", "matched",
                "the sentence they arrive in")]
    found = False
    for x in sorted(rows, key=lambda r: r["name"]):
        hit = _first_mention(chapters, x["name"], world)
        if not hit:
            continue
        found = True
        ch, off, sentence, gap, tok = hit
        lines.append("   %-24s ch %-4d %-9d %-12s %-10s %s"
                     % (x["name"][:24], ch.number, len(ch.body[:off].split()),
                        "-" if gap is None else "%d words" % gap, tok[:10], sentence[:46]))
    if found:
        lines.append("   `speaks after` is the words between a character's first mention and "
                     "their first line.")
        lines.append("   `matched` is the name token that was found - a clan name shared with "
                     "the world (`Uchiha`) can")
        lines.append("   match before the person does, and no counting rule separates the two. "
                     "Read it and discount it.")
        lines.append("   Printed, never scored: deferring a placement is a choice, and doing it "
                     "to everyone is a habit.")
        rep.info("debuts", lines)


def _world_terms(novel):
    """Capitalised nouns the world bible claims - clans, factions, places. Not people."""
    out = {}
    for parts in (("bible", "world.md"), ("bible", "lexicon.md")):
        try:
            with open(novel.path(*parts), encoding="utf-8") as fh:
                text = fh.read()
        except (IOError, OSError):
            continue
        for m in re.finditer(r"\b[A-Z][a-z]{2,}\b", text):
            key = m.group(0).lower()
            out[key] = out.get(key, 0) + 1
    return out


def _first_mention(chapters, name, world_terms=None):
    """(chapter, offset, sentence, words until they first speak) for a cast name."""
    world_terms = world_terms or {}
    tokens = [t for t in re.split(r"[^\w']+", name) if len(t) >= 2]
    if not tokens:
        return None
    # A clan or faction name is shared with the world: searching "Uchiha Tsumugi" on "Uchiha"
    # finds the compound wall in paragraph two and reports a debut the character is not in. Drop
    # the tokens the world bible already claims, then take the earliest of what is left - which
    # is the name the prose actually calls the person by.
    # Match on any token of the name, and report which one matched.
    #
    # Two cleverer rules were tried and both were silently wrong. Rarest-token picks `Kurogane`
    # over `Suzune` for a protagonist who is only ever called Suzune. Scoring by how hard the
    # world bible claims a token does not separate them either: in run #2 the bible claims
    # `Suzune` 26 times and the clan name `Uchiha` 8, so no threshold exists. A shared clan name
    # cannot be told from a protagonist by counting, and a debut ledger that is confidently wrong
    # is worse than one that shows its working. So the matched token is printed and the reader
    # discounts `Uchiha` for themselves.
    pattern = re.compile(r"\b(?:%s)\b" % "|".join(re.escape(t) for t in tokens))
    for ch in chapters:
        m = pattern.search(ch.body)
        if not m:
            continue
        start = ch.body.rfind("\n\n", 0, m.start()) + 1
        stop = ch.body.find("\n\n", m.end())
        para = ch.body[start:stop if stop != -1 else len(ch.body)]
        sentence = " ".join(para.split())
        gap = None
        for sp_start, _sp_end in ch.speech_ranges:
            if sp_start >= m.start():
                gap = len(ch.body[m.start():sp_start].split())
                break
        return (ch, m.start(), sentence, gap, m.group(0))
    return None


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
