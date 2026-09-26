"""`sw cast` - the distributional audits on the two cast tables.

voice-separation section 3 and competence-map section 2 are arithmetic over a table: whether
the cast straddles the MC's tier, how many people are funny, whether two rows are the same
person twice, and whether anyone has quietly accumulated expertise past their budget. Those
are exactly the defects a per-chapter read cannot see and a script can settle outright.

What it cannot do: decide whether the drafted dialogue honours the row. The script says the
matrix is well-formed; the model still says the chapter is.
"""

import os
import re

from . import textstats
from .report import Report

# competence-map: deep-expertise budget, by cast tier.
DEEP_LEVELS = ("exceptional", "best alive")
DEEP_BUDGET = {"mc": 3, "a": 2, "b": 1, "c": 1}

# Attributed turns before a per-speaker measurement is worth printing. Attribution is a floor
# rather than a census, so a speaker with three tagged lines is an anecdote.
MIN_ATTRIBUTED_TURNS = 4


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
            "eq": _int(r.get("eq")),
            "artic": _int(r.get("artic")),
            "wit": _wit(r.get("wit")),
            "turn": _int(r.get("turn")),
            "hands": str(r.get("hands", "")).strip().lower(),
            "line": r.line_no,
        })

    rep.info("voice matrix (%d rows)" % len(rows), [
        "   %-12s tier %-2s intel %-4s eq %-4s artic %-4s wit %-10s turn %s"
        % (x["name"], x["tier"], x["intel"], x["eq"], x["artic"], x["wit"] or "none", x["turn"])
        for x in rows])

    _mc_row(rep, rows, mc_name, mc_tier, vpath)
    _straddle(rep, rows, mc_name, mc_tier, vpath)
    _eq(rep, novel, rows, mc_name, vpath)
    _debuts(novel, rep, rows)
    _turn_lengths(novel, rep, rows)
    _wit_cap(rep, rows, vpath)
    _clash(rep, rows, vpath)
    _turns_and_hands(rep, rows, vpath)
    _competence(rep, novel, rows, comps, cpath)
    _names_elsewhere(novel, rep)
    return rep


def _name_tokens(novel):
    """Capitalised words of three letters or more in every name the novel declares - the voice
    matrix, the walk-on roster, the profile files, and the lexicon, which names the absent and
    the dead that no matrix row carries."""
    names = [r.first() for r in novel.voice_rows()] + [e["name"] for e in novel.roster()]
    names += [re.sub(r"[-_]+", " ", k).title() for k in novel.cast_files()]
    names += novel.lexicon_names()
    out = {}
    for name in names:
        for t in re.findall(r"\b[A-Z][a-z'\-]{2,}\b", name):
            if t.lower() not in _NOT_NAMES:
                out.setdefault(t, name)
    return out


# Institutions and titles every fantasy has: two books sharing a guild share nothing.
_NOT_NAMES = frozenset(
    "the guild house order council crown church temple court hall office city river lord lady "
    "king queen prince princess master mistress warden captain deputy sir dame elder high".split())


def _names_elsewhere(novel, rep):
    """A name this cast shares with another novel in the same repo.

    Benchmark runs #5 and #6 were two original fantasies with nothing in common but the model:
    the first's MC and the second's vanished mentor shared a surname, and three names in all sat
    on both sides of the two casts. Nothing in the corpus names any of them, so it is the model's
    default reaching the page. A note - two novels may share a name on purpose - and
    `character-profile`'s to decide. The other novel's name is printed, never its cast.
    """
    from .novelio import Novel
    parent = os.path.dirname(novel.root)
    mine = _name_tokens(novel)
    if not mine or not os.path.isdir(parent):
        return
    for slug in sorted(os.listdir(parent)):
        other_root = os.path.join(parent, slug)
        if slug.startswith("_") or other_root == novel.root or not os.path.isdir(other_root):
            continue
        theirs = _name_tokens(Novel(other_root))
        shared = sorted(set(mine) & set(theirs))
        if shared:
            rep.note("cast-names",
                     "%s also name%s a character in `%s` - a name two unrelated books share is "
                     "usually the model's default rather than either book's choice "
                     "(character-profile)" % (", ".join("`%s`" % t for t in shared),
                                             "" if len(shared) > 1 else "s", slug),
                     path=novel.path("bible", "cast", "_voices.md"))


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


def _eq(rep, novel, rows, mc_name, vpath):
    """social-perception: the EQ axis, its agreement with novel.md, and the intel+eq pair.

    A cast whose rows all read `intel == eq` has one kind of mind in it wearing different names,
    and the defect is invisible per chapter for the same reason the straddle rule is: you cannot
    see it by reading one profile. Everything here is a warn rather than a defect - a novel may
    legitimately not use the axis yet, and the drafter is told so once rather than blocked.
    """
    declared = _int(novel.get("mc.eq_tier"), None)
    scored = [x for x in rows if x["eq"] is not None]
    if not scored:
        rep.warn("eq", "no `eq` values in the matrix - every character reads people exactly as "
                 "well as the author does, which is one mind with several names. Add the column "
                 "(`social-perception`)", path=vpath)
        return

    mc = [x for x in scored if x["name"].lower() == (mc_name or "").lower()]
    if mc and declared is not None and mc[0]["eq"] != declared:
        rep.defect("eq", "matrix gives %s eq %s, novel.md declares eq_tier %s"
                   % (mc[0]["name"], mc[0]["eq"], declared), path=vpath, line=mc[0]["line"])

    mc_eq = mc[0]["eq"] if mc else declared
    if mc_eq is not None:
        others = [x for x in scored if x["name"].lower() != (mc_name or "").lower()]
        if others and not [x for x in others if x["eq"] > mc_eq]:
            rep.warn("eq-straddle",
                     "nobody reads people better than the MC (eq %d) - somebody in the cast "
                     "should see what the MC misses, and act on it first" % mc_eq, path=vpath)

    flat = [x for x in scored if x["intel"] is not None and x["intel"] == x["eq"]]
    if len(flat) == len(scored) and len(scored) > 2:
        rep.warn("eq-flat",
                 "every character has eq equal to intel (%s) - the gap between the two axes is "
                 "where a character lives, and a cast without one has a single kind of mind in "
                 "it" % ", ".join(x["name"] for x in flat), path=vpath)

    seen = {}
    for x in scored:
        key = (x["intel"], x["eq"])
        if None in key:
            continue
        if key in seen:
            rep.warn("eq-clash",
                     "%s and %s share intel %s + eq %s - those two decide what a character "
                     "concludes about a scene, so these reach the same judgement about "
                     "everyone. Move one"
                     % (seen[key], x["name"], x["intel"], x["eq"]), path=vpath, line=x["line"])
        else:
            seen[key] = x["name"]


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
    declared = novel.cast_frontmatter()
    lines = ["   %-24s %-7s %-9s %-12s %-10s %s"
             % ("character", "debut", "at word", "speaks after", "matched",
                "the sentence they arrive in")]
    found, stale = False, []
    for x in sorted(rows, key=lambda r: r["name"]):
        hit = _first_mention(chapters, x["name"], world)
        if not hit:
            continue
        found = True
        ch, off, sentence, gap, tok = hit
        lines.append("   %-24s ch %-4d %-9d %-12s %-10s %s"
                     % (x["name"][:24], ch.number, len(ch.body[:off].split()),
                        "-" if gap is None else "%d words" % gap, tok[:10], sentence[:46]))
        says = _int((declared.get(x["name"]) or {}).get("first_appears"))
        if says and says != ch.number:
            stale.append("%s says %d, reads ch %d" % (x["name"], says, ch.number))
    if stale:
        # A note, because a character may legitimately be named before they appear and the match
        # is a token match - the `matched` column exists because a house name shared with the
        # world can hit before the person does. What a note cannot be is absent: this field was
        # in both cast templates from the start, read by nothing, and wrong in two of run #5's
        # seven files by chapter 4.
        rep.note("first-appears",
                 "%s - `first_appears:` disagrees with where the name first reaches the page. "
                 "A name may be spoken of before it walks on, so read it; a field nothing reads "
                 "is a field that drifts" % "; ".join(stale),
                 path=novel.path("bible", "cast"))
    if found:
        lines.append("   `speaks after` is the words between a character's first mention and "
                     "their first line.")
        lines.append("   `matched` is the name token that was found - a clan or house name "
                     "shared with the world can")
        lines.append("   match before the person does, and no counting rule separates the two. "
                     "Read it and discount it.")
        lines.append("   Printed, never scored: deferring a placement is a choice, and doing it "
                     "to everyone is a habit.")
        rep.info("debuts", lines)


def _cadence(rep, spoken):
    """How each speaker BUILDS a turn, as far as counting reaches. Printed, never scored.

    `voice-separation` section 3's cadence test has no script by design - cadence is a shape and the
    matrix axes are numbers - and the writing agent in benchmark run #3 named that as the one
    repair it had no mechanical backstop for over a long run. This does not replace the judgement;
    it puts the three countable shadows of cadence side by side so two speakers can be compared
    at an arc rollup without re-reading every scene.

    `sent` mean words per sentence inside their turns
    `frag` share of their sentences that never reach a full stop
    `fall` share of their multi-sentence turns that END on a sentence well under their own
           average - the long-balanced-then-short-flat landing that made run #3's mother and
           her six-year-old daughter read as one person on two different matrix rows
    """
    sig = {}
    for name, turns in spoken.items():
        sents, falls, multi = [], 0, 0
        for turn in turns:
            parts = [p.strip() for p in re.split(r"(?<=[.!?])\s+", turn) if p.strip()]
            lens = [len(p.split()) for p in parts]
            if not lens:
                continue
            sents.extend(lens)
            if len(lens) >= 2:
                multi += 1
                if lens[-1] < 0.6 * (sum(lens) / float(len(lens))):
                    falls += 1
        if len(sents) < 4:
            continue
        frag = sum(1 for p in turns for q in [p] if not q.rstrip().endswith((".", "!", "?")))
        sig[name] = (sum(sents) / float(len(sents)),
                     frag * 100.0 / len(turns),
                     (falls * 100.0 / multi) if multi else 0.0)
    if len(sig) < 2:
        return
    lines = ["   %-24s %-7s %-7s %-7s" % ("character", "sent", "frag%", "fall%")]
    for name in sorted(sig):
        a, b, c = sig[name]
        lines.append("   %-24s %-7.1f %-7.0f %-7.0f" % (name[:24], a, b, c))
    lines.append("   Printed, never scored - cadence is a shape and these are its shadows.")
    lines.append("   Two speakers close on all three are worth reading side by side")
    lines.append("   (voice-separation section 3, the cadence test).")
    rep.info("cadence, as far as counting reaches", lines)


def _alternate(ch, paragraphs, names):
    """Fill unattributed turns in two-speaker scenes, where the convention verifies itself.

    Benchmark run #5, O14: the better the dialogue, the less the voice checks can see. Attribution
    needs a cast name in the narration around the line, so a well-written untagged two-hander -
    the scene a writer is *supposed* to be able to leave untagged - scored 4 of 52 lines. Below
    four sentences `_cadence` bails, so run #3's cadence test never ran, on a chapter where two
    characters demonstrably shared a cadence. The instrument went blind exactly where the prose
    got good.

    This recovers turns without loosening the conservatism anywhere else, because it never
    *assumes* alternation - it checks it. Inside one scene, with exactly two speakers attributed,
    an unattributed run is filled only when it is bracketed at both ends by attributed turns whose
    parity agrees: if the ends are the same speaker the gap must be even, if they differ it must be
    odd. A run whose ends disagree with the count between them is a scene that is not strictly
    alternating, and it stays unattributed. So does anything before the first tag or after the
    last, which has no second bracket to check against.

    Recovered turns are counted separately from directly attributed ones and printed that way, so
    a reader can always tell how much of the number is inference.
    """
    filled = list(names)
    for start, end in ch.scene_bounds():
        idx = [i for i, p in enumerate(paragraphs) if p[0] >= start and p[1] <= end]
        cast = {names[i] for i in idx if names[i]}
        if len(cast) != 2:
            continue
        anchors = [i for i in idx if names[i]]
        for a, b in zip(anchors, anchors[1:]):
            gap = idx.index(b) - idx.index(a)
            if gap < 2:
                continue
            same = names[a] == names[b]
            if same != (gap % 2 == 0):
                continue                    # the scene does not alternate across this run
            other = next(n for n in cast if n != names[a])
            for step in range(1, gap):
                filled[idx[idx.index(a) + step]] = names[a] if step % 2 == 0 else other
    return filled


def _turn_lengths(novel, rep, rows):
    """Each speaker's measured turn length against the one their own row declares.

    The revising agent in benchmark run #2 found this by hand and named it as the reason the
    defect survived several `revision-pass` cycles: `sw lint`'s texture line is a mean across
    **all** speakers in a chapter, so one character's turns can double while the chapter average
    stays healthy. There the MC declared `turn: 14` and ran to 23.4 words in the two
    highest-pressure scenes in the arc - a person narrating an essay about her own honesty.

    Attribution is deliberately conservative: a line counts for a speaker only when exactly one
    cast name appears in the narration around it. Coverage is printed so the number can be
    weighed. Printed, never scored.
    """
    chapters = [c for c in novel.chapters() if c.number]
    declared = {}
    for x in rows:
        turn = _int(x.get("turn"))
        if turn:
            declared[x["name"]] = turn
    if not chapters or not declared:
        return
    world = _world_terms(novel)
    tokens = {}
    for name in declared:
        toks = [t for t in re.split(r"[^\w']+", name) if len(t) >= 2]
        tokens[name] = [t for t in toks if world.get(t.lower(), 0) < 3] or toks

    # One paragraph is one TURN, and every `"…"` span inside it counts together. Run #3, T4: this
    # loop used to measure each span on its own, so `"…," she said. "…"` - the ordinary way to
    # punctuate a long speech - halved the speaker's measured turn length. The bug was fixed in
    # `textstats.speech_line_lengths` for the chapter mean and survived here, in the per-speaker
    # view, which is the one that exists precisely to catch what a chapter mean hides.
    measured, spoken, attributed, recovered, total = {}, {}, 0, 0, 0
    for ch in chapters:
        body = ch.body
        # One paragraph with speech in it is one turn, and `around` is the narration outside the
        # quotes. Both come from `textstats.Chapter.speech_paragraphs`, which `cmd_lint`'s
        # group-scene check shares so the two cannot drift apart again.
        paragraphs = ch.speech_paragraphs()
        names = []
        for _para_start, _para_end, spans, around in paragraphs:
            total += 1
            hits = [n for n, toks in tokens.items()
                    if any(re.search(r"\b%s\b" % re.escape(t), around) for t in toks)]
            names.append(hits[0] if len(hits) == 1 else None)
        attributed += sum(1 for n in names if n)
        filled = _alternate(ch, paragraphs, names)
        recovered += sum(1 for a, b in zip(names, filled) if b and not a)
        for (_para_start, _para_end, spans, _around), name in zip(paragraphs, filled):
            words = sum(len(body[s:e].split()) for s, e in spans)
            if not words or not name:
                continue
            measured.setdefault(name, []).append(words)
            spoken.setdefault(name, []).append(
                " ".join(body[s:e].strip('\"\u201c\u201d') for s, e in spans))

    lines = ["   %-24s %-9s %-9s %-7s %s"
             % ("character", "declared", "measured", "lines", "")]
    flagged = []
    for name in sorted(measured):
        got = measured[name]
        mean = sum(got) / float(len(got))
        want = declared[name]
        off = ""
        if len(got) >= MIN_ATTRIBUTED_TURNS and want and abs(mean - want) / float(want) > 0.4:
            off = "%+.0f%% against their own row" % ((mean - want) * 100.0 / want)
            flagged.append(name)
        lines.append("   %-24s %-9d %-9.1f %-7d %s" % (name[:24], want, mean, len(got), off))
    if len(lines) == 1:
        return
    lines.append("   %d of %d spoken lines attributed to exactly one speaker. A line counts only "
                 "when one" % (attributed, total))
    lines.append("   cast name appears around it, so an unattributed line is silence here, not a "
                 "short turn.")
    if recovered:
        lines.append("   %d more recovered by alternation inside two-speaker scenes, bracketed at "
                     "both ends." % recovered)
    rep.info("turn length, declared vs measured", lines)
    _cadence(rep, spoken)
    _contractions(novel, rep, spoken)
    if flagged:
        rep.note("turn-drift", "%s speak at more than 40%% off their declared turn length - a "
                 "chapter mean hides this, which is how it survived several revision passes in "
                 "benchmark run #2" % ", ".join(flagged), path=novel.path("bible", "cast",
                                                                         "_voices.md"))


def _contractions(novel, rep, spoken):
    """Each speaker's measured contraction rate against the cell their own file declares.

    `sw lint` measures contractions one way only: pooled across every speaker in the chapter, and
    flagged only when there are too *few* ("a cast that never says…"). So a character whose
    §Speech fingerprint says `contractions: never` and who contracts in every line is invisible
    twice over. Benchmark run #5, chapter 4: the guild master's file declares `never`, his dialogue
    carried ten, and the only thing in the toolkit that noticed was the drafter reading its own
    cast file during Pass 10.

    A note, never a gate, and the reason is the repo's most-repeated lesson: a number a chapter has
    to clear is a number somebody writes toward. A character may break his own fingerprint because
    the scene is better for it - the note says what it saw and the drafter decides. `never` and
    `always` are the only two cells this reads; anything conditional ("drops them when lying") is a
    judgement and is left alone.
    """
    fingerprints = novel.fingerprints()
    if not fingerprints:
        return
    flagged = []
    for name in sorted(spoken):
        declared = str((fingerprints.get(name) or {}).get("contractions", "")).strip().lower()
        if declared not in ("never", "always"):
            continue
        turns = spoken[name]
        if len(turns) < MIN_ATTRIBUTED_TURNS:
            continue
        text = " ".join(turns)
        words = len(text.split())
        if not words:
            continue
        hits = len(textstats.CONTRACTION_RE.findall(text))
        if declared == "never" and hits:
            flagged.append("%s declares `never` and contracts %.1f times per 100 spoken words "
                           "(%d in %d attributed turns)"
                           % (name, hits * 100.0 / words, hits, len(turns)))
        elif declared == "always" and not hits:
            flagged.append("%s declares `always` and contracts nothing across %d attributed turns"
                           % (name, len(turns)))
    if flagged:
        rep.note("fingerprint", "a speech fingerprint and the page disagree: %s. The cell is in "
                 "the character's own file and no other check reads it - break it on purpose or "
                 "fix one of the two" % "; ".join(flagged),
                 path=novel.path("bible", "cast"))


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
