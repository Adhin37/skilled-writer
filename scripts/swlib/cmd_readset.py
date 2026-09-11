"""`sw readset` - assemble the bounded read-set for one chapter.

continuity-summary specifies the read-set as slices: the matrix rows for *this chapter's*
speakers, the location rows for *this chapter's* locations, chapter blocks N-5 to N-1. A
model cannot read half a file, so in practice it reads all of them and the cost grows with
the ledger. This emits the slices, and nothing else.

The bundle ends with a NOT LOADED list, so what was left out is visible rather than silently
absent - the read-set is bounded on purpose, and the model has to be able to ask for more.
"""

import os
import re

from . import cmd_lint, kb, kbexpr, mdio, rules

HOT_BLOCK_CAP = 3

# The WATCH row. Distributional by construction: a check has to have fired in at least
# WATCH_MIN of the last WATCH_WINDOW chapters before it is named, and only WATCH_CAP items
# are printed. One chapter is never scored on it - the row says what has *recurred*, which
# is the only thing a per-chapter gate cannot see about itself.
WATCH_WINDOW = 5
WATCH_MIN = 2
WATCH_CAP = 3

CONFIG_KEYS = [
    "genre", "subgenre",
    "narration.person", "narration.tense", "narration.distance", "narration.interiority",
    "narration.voice_notes",
    "style.read_like", "style.avoid",
    "pov.mode", "pov.switch_granularity", "pov.label_switches",
    "mc.name", "mc.intel_tier", "mc.origin", "mc.form_locked",
    "mc.foreknowledge_grain", "mc.foreknowledge_first_win_ch", "mc.foreknowledge_fails_ch",
    "chapters.length_band", "chapters.hook_required", "chapters.arc_length",
    "chapters.scenes_per_chapter",
    "opening.anchor_by_ch", "opening.contract_by_ch", "opening.promise_touched_by_ch",
    "opening.first_win_by_ch", "opening.promise", "opening.stakes_ceiling",
    "scaling.shape", "scaling.tiers", "scaling.ceiling_tier", "scaling.endgame",
    "scaling.edge_worth", "scaling.edge_price", "scaling.substitute_tension",
    "scaling.first_limit_by_ch", "scaling.trivial_per_arc", "scaling.boost_debt_due",
    "theme.controlling_idea", "theme.counter_case",
    "timeline.reactivity", "timeline.crisis_cap",
    "content.rating", "content.romance",
    "ending.contract",
]


SKILLS_REL = os.path.join(".claude", "skills")
_REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def _module_entry(name):
    """The cheapest correct entry point for a module: its draft card, else its body.

    Finds a path; judges nothing. Delegates to the index so the read-set and `sw kb` cannot
    disagree about where a module starts.
    """
    return kb.index(_REPO).entry(name)


def active_modules(novel):
    """The optional and genre modules switched on for this novel, as (name, entry) pairs.

    write-chapter step 0.2 opens these and no others: a module absent from this list is off
    for this novel and costs nothing to skip.

    Which modules exist and what switches each one on is declared in the skills' own frontmatter
    and read by `kb`, rather than restated here. The config-gated skills are deliberately not in
    this list: it has always been the optional and genre modules, and widening it is a change to
    what the read-set tells a drafter rather than a refactor.
    """
    return [(name, entry)
            for name, entry, _state in kb.index(_REPO).active(novel,
                                                              tiers=("optional", "genre"))]


def _cards_section(add, novel, number, characters):
    """The phase A card set, resolved against this novel and this chapter.

    This replaces the table `write-chapter` used to carry, and the replacement is not only a
    move. The table listed twenty-two rows with four conditions written in English, which the
    model had to evaluate for itself every chapter; these are the cards that actually apply,
    with each card's own statement of what it decides.

    The cards that did NOT fire are printed too, with the reason. A condition that is quietly
    wrong is otherwise indistinguishable from a card that was never meant to apply - and the
    whole point of moving the conditions into data was to make them checkable.
    """
    idx = kb.index(_REPO)
    ctx = kbexpr.Context(novel, chapter=number, speakers=len(characters or []))
    fired, skipped = idx.cards("draft-card", ctx, phase="A")
    if not fired and not skipped:
        return
    add("\n### CARDS - phase A, resolved. Open these in order, and no others.")
    width = max(len(f.owner) for f, _s, _w in fired) if fired else 10
    for f, state, why in fired:
        cond = ("  [%s]" % f.when) if f.when and f.when != "always" else ""
        mark = "  ?" if state is kbexpr.UNKNOWN else ""
        add("%-*s -> %s%s%s" % (width, f.owner, f.rel, cond, mark))
        if f.description:
            add("%-*s    %s" % (width, "", f.description))
        if state is kbexpr.UNKNOWN:
            add("%-*s    ? trigger could not be resolved: %s" % (width, "", "; ".join(why)))
    if skipped:
        add("\n### CARDS NOT OPENED - the condition is false for this novel and chapter")
        w2 = max(len(f.owner) for f, _w in skipped)
        for f, why in skipped:
            add("%-*s    %s" % (w2, f.owner, "; ".join(why)))


def _recent_pressure(novel, number, window=5):
    """The last few pressure rows. The whole log would grow without bound; the shape does not."""
    rows = [r for r in novel.pressure_rows()
            if _first_int(r) is not None and _first_int(r) < number]
    rows.sort(key=_first_int)
    if not rows:
        return "### THE PRESSURE LOG (recent)\n(no confrontations logged yet)"
    tail = rows[-window:]
    return "### THE PRESSURE LOG (last %d)\n%s" % (
        len(tail), _table_block(tail[0]._headers, tail))


def _first_int(row):
    m = re.search(r"\d+", row.first())
    return int(m.group(0)) if m else None


def _names_from_chg(block):
    out = []
    for line in block.keys().get("chg", []):
        for part in line.split(";"):
            m = re.match(r"\s*([A-Z][\w'\-]*(?:\s+[A-Z][\w'\-]*)?)\s*:", part)
            if m:
                out.append(m.group(1).strip())
    return out


def resolve_characters(novel, number, explicit=None):
    """Explicit list wins; otherwise the plan row's POV plus everyone who changed recently."""
    if explicit:
        return [c.strip() for c in explicit if c.strip()], "given on the command line"
    names, why = [], "plan row POV + `chg>` names from blocks %d-%d" % (max(1, number - 3), number - 1)
    row = novel.plan_row(number)
    if row:
        pov = row.get("pov").strip()
        if pov:
            names.extend(p.strip() for p in re.split(r"[/,+&]| and ", pov) if p.strip())
    for b in novel.blocks():
        if b.number is not None and number - 3 <= b.number <= number - 1:
            names.extend(_names_from_chg(b))
            if b.pov:
                names.append(b.pov)
    seen, out = set(), []
    for n in names:
        if n.lower() not in seen:
            seen.add(n.lower())
            out.append(n)
    return out, why


def resolve_locations(novel, number, explicit=None):
    if explicit:
        return [l.strip() for l in explicit if l.strip()]
    hay = ""
    prev = novel.block(number - 1)
    if prev:
        hay += prev.header_field("loc") + " " + prev.get("set")
    row = novel.plan_row(number)
    if row:
        hay += " " + " ".join(row.cells)
    out = []
    for r in novel.location_rows():
        place = r.first().strip()
        bare = re.sub(r"^(?:the|a|an)\s+", "", place, flags=re.I)
        if bare and re.search(r"\b%s\b" % re.escape(bare), hay, re.I):
            out.append(place)
    return out


def _match(rows, names):
    low = [n.lower() for n in names]
    return [r for r in rows if any(r.first().strip().lower() == n for n in low)]


def _table_block(headers, rows):
    if not rows:
        return None
    out = ["| " + " | ".join(headers) + " |",
           "|" + "|".join(["---"] * len(headers)) + "|"]
    out.extend(r.raw.strip() for r in rows)
    return "\n".join(out)


def regate_target(numbers):
    """How to name a set of ungated chapters back to the user.

    A range only when the run is unbroken: `1-4` where chapters 1 and 4 are ungated but 2 and 3
    are not would send the user to re-gate two chapters that already passed.
    """
    nums = sorted(numbers)
    if len(nums) == 1:
        return "`/novel-write %d`" % nums[0]
    if nums == list(range(nums[0], nums[-1] + 1)):
        return "`/novel-write %d-%d`" % (nums[0], nums[-1])
    shown = ", ".join(str(n) for n in nums[:6])
    return "ch %s%s, one at a time" % (shown, "" if len(nums) <= 6 else
                                       " and %d more" % (len(nums) - 6))


def watch_row(novel, number):
    """Checks that fired in WATCH_MIN or more of the last WATCH_WINDOW chapters.

    The countable half of what the gate keeps fixing. The judgement half is in the `gate>`
    lines, which this prints beside the row rather than trying to parse - no script can tell
    that two differently worded gate notes are the same defect.
    """
    lo = max(1, number - WATCH_WINDOW)
    chapters = [c for c in novel.chapters()
                if c.number is not None and lo <= c.number <= number - 1]
    if not chapters:
        return [], []
    hits = {}
    for c in chapters:
        for check in cmd_lint.check_counts(novel, c)["checks"]:
            hits[check] = hits.get(check, 0) + 1
    named = sorted(((v, k) for k, v in hits.items() if v >= WATCH_MIN),
                   key=lambda vk: (-vk[0], vk[1]))
    row = ["%s (%d of last %d)" % (k, v, len(chapters)) for v, k in named[:WATCH_CAP]]
    notes = []
    for b in novel.blocks():
        if b.number is not None and lo <= b.number <= number - 1 and b.has("gate"):
            notes.append("c%d %s" % (b.number, b.get("gate")))
    return row, notes


def build(novel, number, chars=None, locs=None, want_society=False):
    cfg_lines = []
    for key in CONFIG_KEYS:
        val = novel.get(key)
        if val not in (None, "", [], {}):
            cfg_lines.append("%s: %s" % (key, val))
    modules = active_modules(novel)

    characters, why = resolve_characters(novel, number, chars)
    locations = resolve_locations(novel, number, locs)

    out = []
    add = out.append
    add("# READ-SET - %s - chapter %d" % (novel.title, number))
    add("# Assembled by `sw readset`. This is the whole read-set: do not open the source")
    add("# files for anything listed here. See NOT LOADED at the foot for what is missing")
    add("# on purpose and how to ask for it.")
    add("# characters resolved: %s  (%s)" % (", ".join(characters) or "none", why))
    add("# locations resolved:  %s" % (", ".join(locations) or "none"))

    stale = novel.ungated_chapters(below=number)
    row, notes = watch_row(novel, number)
    if stale or row or notes:
        add("\n## GATE (write-chapter phase C - what it left behind)")
    if stale:
        add("DEFECT ch %d is `status: %s` - the phase C gate never ran on it%s."
            % (stale[0].number, str(stale[0].meta.get("status", "")).strip() or "?",
               "" if len(stale) == 1 else " (%d ungated below %d)" % (len(stale), number)))
        add("       Re-gate before drafting: %s. A chapter is not finished at `drafted`,"
            % regate_target(c.number for c in stale))
        add("       and the defects it kept are the ones this chapter inherits.")
    if row:
        add("WATCH  %s" % " | ".join(row))
        add("       What the gate keeps having to fix. Write against it in phase B. It is a")
        add("       pointer at the owning skill, never a phrase ban, and no chapter is scored")
        add("       on it - three items at most, and only what recurred.")
    if notes:
        add("gate>  " + "\n       ".join(notes))

    add("\n## 0. CONFIG (novel.md, the fields that gate a chapter)")
    add("\n".join(cfg_lines))

    sample = novel.get("style.sample")
    if sample:
        add("\n### STYLE TARGET - write toward this register")
        add(str(sample).strip())
        add("(imitation, not transcription: match the density and the variety, not the words)")

    add("\n### active modules - open these and no others")
    if modules:
        width = max(len(n) for n, _ in modules)
        add("\n".join("%-*s -> %s" % (width, n, path) for n, path in modules))
    else:
        add("(none - no optional module is on and the genre switches none on)")

    _cards_section(add, novel, number, characters)

    add("\n## 1. BOOK DIGEST")
    add(novel.book_digest() or "(empty)")

    digests = novel.arc_digests()
    if digests:
        cur = max(digests)
        add("\n## 2. ARC DIGESTS (current + previous)")
        for a in sorted(d for d in digests if d >= cur - 1):
            add(digests[a])
    else:
        add("\n## 2. ARC DIGESTS")
        add("(none yet - the current arc has not closed)")

    add("\n## 3. CHAPTER BLOCKS %d-%d" % (max(1, number - 5), number - 1))
    blocks = [b for b in novel.blocks()
              if b.number is not None and max(1, number - 5) <= b.number <= number - 1]
    add("\n\n".join(b.text for b in blocks) or "(no prior chapters)")

    # Read-set item 4. continuity-summary says this is the first thing to drop when the
    # set gets too big, so it is capped: without a cap it grows with every hot thread the
    # novel accumulates, which is exactly the cost curve this command exists to flatten.
    hot_cited = []
    for r in novel.threads():
        if str(r.get("tension", "")).lower().strip() == "hot":
            opened = re.sub(r"\D", "", str(r.get("opened", "")))
            if opened and int(opened) < max(1, number - 5):
                b = novel.block(int(opened))
                if b:
                    hot_cited.append((r.first().strip(), b))
    hot_cited.sort(key=lambda x: x[1].number, reverse=True)
    dropped = hot_cited[HOT_BLOCK_CAP:]
    hot_cited = hot_cited[:HOT_BLOCK_CAP]
    if hot_cited:
        add("\n## 3b. BLOCKS CITED BY A HOT THREAD (outside the window)")
        add("\n\n".join("# cited by %s\n%s" % (tid, b.text) for tid, b in hot_cited))
    if dropped:
        add("# also cited, not loaded (cap %d): %s - ask by chapter number if needed"
            % (HOT_BLOCK_CAP, ", ".join("%s@ch%d" % (t, b.number) for t, b in dropped)))

    add("\n## 4. PLAN ROWS %d-%d" % (max(1, number - 1), number + 2))
    prows = [r for r in novel.plan_rows()
             if re.sub(r"\D", "", r.first()).isdigit()
             and max(1, number - 1) <= int(re.sub(r"\D", "", r.first())) <= number + 2]
    add(_table_block(novel.plan_rows()[0]._headers if novel.plan_rows() else [], prows)
        or "(no plan rows in range - run chapter-plan before drafting)")

    add("\n## 5. THREADS (open / escalated)")
    trows = [r for r in novel.threads()
             if str(r.get("status", "")).strip().lower() in ("open", "escalated")]
    add(_table_block(novel.threads()[0]._headers if novel.threads() else [], trows)
        or "(none open)")

    add("\n## 6. GROWTH (this chapter's characters)")
    grows = _match(novel.growth_rows(), characters)
    add(_table_block(novel.growth_rows()[0]._headers if novel.growth_rows() else [], grows)
        or "(no rows for these characters)")
    srows = _match(novel.skill_rows(), characters)
    if srows:
        add("\n### skill ladders")
        add(_table_block(novel.skill_rows()[0]._headers, srows))

    add("\n## 7. VOICE MATRIX (this chapter's speakers)")
    vrows = _match(novel.voice_rows(), characters)
    add(_table_block(novel.voice_rows()[0]._headers if novel.voice_rows() else [], vrows)
        or "(no matrix rows for these characters - voice-separation section 1)")
    vtext = novel._text("bible", "cast", "_voices.md")
    thought = mdio.section(vtext, "POV THOUGHT")
    if thought:
        add("\n" + thought)
    mirrors = mdio.section(vtext, "MIRROR")
    if mirrors and not re.search(r"\bnone\b|\(delete", mirrors, re.I):
        add("\n" + mirrors)

    add("\n## 8. COMPETENCE (this chapter's characters)")
    crows = _match(novel.competence_rows(), characters)
    add(_table_block(novel.competence_rows()[0]._headers if novel.competence_rows() else [],
                     crows) or "(no grid rows - an unlisted domain is `none`)")
    rrows = _match(novel.referral_rows(), characters)
    if rrows:
        add("\n### referrals")
        add(_table_block(novel.referral_rows()[0]._headers, rrows))

    add("\n## 9. LEXICON (whole - it is small and prevents the most common defect)")
    add(novel._text("bible", "lexicon.md").strip() or "(empty)")

    sched = mdio.section(novel._text("plan", "timeline.md"), "SCHEDULED FOR THIS ARC")
    add("\n## 10. WORLD TRACK - scheduled for this arc")
    add(sched or "(nothing scheduled)")

    if novel.form_locked:
        btext = novel._text("state", "body.md")
        add("\n## 11. BODY LEDGER (a character is form_locked)")
        add(mdio.section(btext, "CURRENT FORM") or "(missing)")
        add(mdio.section(btext, "ABSOLUTE LIMITS") or "")

    if novel.has_foreknowledge:
        ftext = novel._text("state", "foreknowledge.md")
        add("\n## 12. FOREKNOWLEDGE")
        add(mdio.section(ftext, "THE GRAIN") or "")
        add(mdio.section(ftext, "THE INVENTORY") or "")
        add(mdio.section(ftext, "THE SPEND LOG") or "")

    if locations:
        add("\n## 13. LOCATIONS (sensory signatures, this chapter only)")
        lrows = [r for r in novel.location_rows()
                 if r.first().strip().lower() in [l.lower() for l in locations]]
        add(_table_block(novel.location_rows()[0]._headers, lrows) or "(none matched)")

    if want_society:
        add("\n## 14. SOCIETY")
        add(novel._text("bible", "society.md").strip())

    if novel.has_scaling:
        ptext = novel._text("state", "power.md")
        add("\n## 15. POWER CURVE (scaling.shape is %s)" % novel.scaling_shape)
        add(mdio.section(ptext, "CURRENT STANDING") or "(missing)")
        add(mdio.section(ptext, "THE LADDER") or "")
        add(_recent_pressure(novel, number))
        add(mdio.section(ptext, "ACTIVE BOOSTS") or "")

    add("\n## NOT LOADED (deliberately - ask for these by name if the chapter needs them)")
    missing = [
        "bible/world.md beyond the location rows above",
        "bible/cast/<char>.md full profiles - the matrix and competence rows are the summary",
        "bible/cast/_extras.md - load the roster line when a walk-on returns",
        "CCS blocks before %d, and arc digests older than the previous arc" % max(1, number - 5),
        "plan/arcs.md, plan/timeline.md sections 1-3 and 5-6",
        "every chapter file - never read past prose unless the user asks for a specific one",
    ]
    if not want_society:
        missing.insert(1, "bible/society.md - pass --society if the chapter turns on a social rule")
    if novel.has_foreknowledge:
        missing.append("state/foreknowledge.md sections 4-6 (observer paradox, arc, who suspects)")
    if novel.has_scaling:
        missing.append("state/power.md section 4 (the gain log) and section 6 (the curve plan) - "
                       "the arc's band is in plan/arcs.md")
    add("\n".join("- " + m for m in missing))
    return "\n".join(out) + "\n"
