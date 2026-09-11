"""`sw lint` - the mechanical sweep over one chapter's prose and frontmatter.

Covers revision-pass Pass 7 (MTL), the countable half of Pass 8 (prose), Pass 10 (mechanics
and the four channels), the default-gesture sweep inside Pass 2, and the anchor-vocabulary
count inside Pass 9b. It cannot judge whether a chapter delivers, whether a cast sounds
alike, or whether a fact has a provenance - those stay with the model, and the skills say so.
"""

import re

from . import rules
from .report import Report

VALID_STATUS = ("planned", "drafted", "revised", "published")
SCENE_BREAK = re.compile(r"^\*(\s+\*)+$")
# Benchmark run #2, F3: the old check enumerated the wrong forms (`***`, `---`, `~~~`, `===`,
# `* * * *`) and so missed a lone `*` - the malformation the writing agent actually produced,
# three times. Enumerating wrong answers cannot be complete; match anything break-shaped
# instead and compare it against the one right answer.
BREAK_LINE = re.compile(r"^[ \t]*[*\-_~=·•][ \t*\-_~=·•]*$", re.M)
WELL_FORMED_BREAK = "* * *"


def lint_chapter(novel, ch, rep=None):
    """Every check that is about **this chapter alone**.

    Strictly per-chapter, because `cmd_history` calls this once for every chapter to build its
    trend table. A novel-level verdict evaluated here would be counted once per chapter and then
    reported as a habit firing on the whole book - one finding wearing N hats. Those live in
    `run()`, which is the command layer and is invoked once.
    """
    rep = rep or Report()
    p = ch.path
    body = ch.body
    outside = ch.outside_speech

    _frontmatter(novel, ch, rep)
    _channels(novel, ch, rep)
    _texture(ch, rep)
    _pacing(ch, rep)
    _phrases(ch, rep)
    _house_style(ch, rep)
    _register(novel, ch, rep)
    _rhythm(ch, rep)
    _anchor(novel, ch, rep)
    _ledger(novel, ch, rep)
    return rep



def check_counts(novel, ch):
    """Which checks fired on one chapter, and how many findings each raised.

    Shared by `sw history` (defects over time) and `sw readset` (the WATCH row), both of which
    want the check *names* rather than the rendered text. Counting, not judging: a check that
    fired is a place to look.
    """
    sub = Report()
    lint_chapter(novel, ch, sub)
    counts = {"defect": 0, "warn": 0, "checks": {}}
    for f in sub.findings:
        if f.level in counts:
            counts[f.level] += 1
        if f.level in ("defect", "warn"):
            counts["checks"][f.check] = counts["checks"].get(f.check, 0) + 1
    return counts


# --------------------------------------------------------------- Pass 10


def _frontmatter(novel, ch, rep):
    p = ch.path
    if not ch.frontmatter_text:
        rep.defect("frontmatter", "no YAML frontmatter at all", path=p, line=1)
        return
    for field in rules.REQUIRED_FRONTMATTER:
        val = ch.meta.get(field)
        if val is None or (isinstance(val, str) and not val.strip()):
            rep.defect("frontmatter", "`%s:` missing or empty" % field, path=p, line=1)

    measured = ch.words
    recorded = ch.meta.get("wordcount")
    if isinstance(recorded, int) and recorded != measured:
        rep.defect(
            "wordcount",
            "frontmatter says %d, body measures %d - a stale count propagates into "
            "state/continuity.md (run `sw stamp`)" % (recorded, measured),
            path=p, line=1)

    _event_field(ch, rep)

    status = str(ch.meta.get("status", "")).strip()
    if status and status not in VALID_STATUS:
        rep.warn("frontmatter", "status `%s` is not one of %s"
                 % (status, "/".join(VALID_STATUS)), path=p, line=1)

    num = ch.meta.get("number")
    fname = re.match(r"^(\d+)", ch.name)
    if isinstance(num, int) and fname and int(fname.group(1)) != num:
        rep.defect("frontmatter", "number: %d but the filename says %s"
                   % (num, fname.group(1)), path=p, line=1)


def _clause_at(ch, off, span=95):
    """The readable run of text around an offset, for quoting back in a finding."""
    text = re.sub(r"\s+", " ", ch.body[max(0, off - 10):off + span]).strip()
    return text[:span]


def _event_field(ch, rep):
    """`event:` is the concrete half of the delivery gate.

    `delivers:` asks for a difference and gets one - benchmark run #2 wrote five of them and
    every single one described a shift in somebody's interior state ("proximity that isn't
    refused", "attention has moved one level up"). A gate phrased in abstractions is satisfied
    by abstractions. `event:` asks instead for the thing a reader would retell, in one clause,
    with a verb and a target.
    """
    p = ch.path
    ev = str(ch.meta.get("event", "")).strip()
    if not ev:
        return                      # _frontmatter already defected on the missing field
    n = len(ev.split())
    if n > rules.EVENT_MAX_WORDS:
        rep.warn("event", "`event:` runs %d words; the cap is %d. If it will not fit in a "
                 "clause it is a summary of the chapter, not the thing that happened"
                 % (n, rules.EVENT_MAX_WORDS), path=p, line=1)
    for _off, hit, label in rules.scan(ev, rules.EVENT_ABSTRACT):
        rep.defect("event", "`event:` contains %s: `%s`" % (label, hit), path=p, line=1,
                   detail='"%s" - name what happened, not what it did to anyone. '
                          '"She lies to the Hokage about the recovery list" is an event; '
                          '"trust deepens" is that event\'s effect.' % ev[:90])


def _house_style(ch, rep):
    """The register this model defaults to once the MTL cut-list is already clean.

    Individually every construction below is good writing, so every hit is a note and the only
    finding that carries weight is the aggregate rate. The disease is uniformity: run #2's five
    chapters never once let a sentence just deliver information, and that - not any banned
    phrase - is what makes them read as machine-made.
    """
    p = ch.path
    hits = ch.house_style_hits()
    for off, label in hits:
        rep.note("house-style", label, path=p, line=ch.line_of(off))
    # A rate needs a denominator worth dividing by. One antithesis in a 200-word chapter is
    # 5 per 1000 words and means nothing; the finding is density, so it needs enough hits to be
    # a density. Same guard `_pacing` uses on the summary markers.
    if ch.house_style_rate > rules.HOUSE_RATE_WARN and len(hits) >= rules.HOUSE_MIN_HITS:
        rep.warn("house-style",
                 "%d house-register constructions (%.1f per 1000 words, over %.0f) - the "
                 "narrator has one setting. Vary it: let some sentences carry information and "
                 "nothing else"
                 % (len(hits), ch.house_style_rate, rules.HOUSE_RATE_WARN), path=p,
                 detail="; ".join(sorted({l for _o, l in hits}))[:160])
    if ch.emdash_rate > rules.EMDASH_RATE_WARN and ch.words >= rules.RATE_MIN_WORDS:
        rep.warn("em-dash", "%.1f em-dashes per 1000 words of narration (over %.0f) - the "
                 "appositive that re-explains the clause before it is this narrator's tic"
                 % (ch.emdash_rate, rules.EMDASH_RATE_WARN), path=p)


def _register(novel, ch, rep):
    """The declared temperature and hook shape for this chapter, checked against the vocabulary.

    Distribution is `sw arc`'s job - one chapter cannot be too `quiet`. This only checks that the
    plan row said something, and said something legal.
    """
    if ch.number is None:
        return
    row = novel.plan_row(ch.number)
    if row is None:
        return
    p = novel.path("plan", "chapters.md")
    for field, vocab in (("temp", rules.TEMPS), ("hooktype", rules.HOOKTYPES)):
        val = row.get(field, "").strip().lower()
        if not val:
            rep.warn("register", "plan row %d has no `%s` - set it before drafting, so the "
                     "chapter is written to a temperature instead of inheriting the last one"
                     % (ch.number, field), path=p, line=row.line_no)
        elif val not in vocab:
            rep.warn("register", "plan row %d `%s: %s` is not one of %s"
                     % (ch.number, field, val, " ".join(vocab)), path=p, line=row.line_no)


def _channels(novel, ch, rep):
    p = ch.path
    share = ch.speech_share
    if share < rules.SPEECH_FLOOR:
        # A warn, not a defect. The defect is `speech-starvation`, measured over a window:
        # see _speech_window.
        rep.warn("speech-share",
                 "%.1f%% spoken aloud, under the %.0f%% floor - allowed as a deliberate, "
                 "occasional chapter, not as a habit (target %.0f-%.0f%%)"
                 % (share, rules.SPEECH_FLOOR, rules.SPEECH_TARGET_LOW,
                    rules.SPEECH_TARGET_HIGH), path=p)
    elif share < rules.SPEECH_TARGET_LOW:
        rep.warn("speech-share", "%.1f%% spoken aloud, below the %.0f-%.0f%% target"
                 % (share, rules.SPEECH_TARGET_LOW, rules.SPEECH_TARGET_HIGH), path=p)
    elif share > rules.SPEECH_TARGET_HIGH:
        rep.warn("speech-share", "%.1f%% spoken aloud, above the %.0f%% target - check for "
                 "talking heads" % (share, rules.SPEECH_TARGET_HIGH), path=p)

    thoughts = ch.thoughts()
    if len(thoughts) > rules.THOUGHT_BUDGET:
        rep.defect("thought-budget",
                   "%d direct-thought marks; the budget is %d. Convert the surplus back to "
                   "free indirect discourse" % (len(thoughts), rules.THOUGHT_BUDGET),
                   path=p, line=ch.line_of(thoughts[rules.THOUGHT_BUDGET].start()))

    for line_no, text in ch.unterminated_thoughts():
        rep.defect("channel-collision",
                   "thought mark opens and never closes on this line - an apostrophe read as "
                   "a thought mark", path=p, line=line_no,
                   detail=text[:110])

    paras = ch.paragraphs()
    if paras and re.search(r"\[[^\]\n]*\]", paras[0][1]):
        rep.warn("meta-channel", "the chapter opens on a `[...]` meta block", path=p,
                 line=ch.line_of(paras[0][0]))
    prev_meta = False
    for off, text in paras:
        is_meta = bool(re.match(r"^\[[^\]]*\]$", text.strip()))
        if is_meta and prev_meta:
            rep.warn("meta-channel", "two `[...]` meta blocks run consecutively",
                     path=p, line=ch.line_of(off))
        prev_meta = is_meta

    for off, text in paras:
        if BREAK_LINE.match(text.strip()) or SCENE_BREAK.match(text.strip()):
            continue          # a break, well formed or not; _scene_breaks owns it
        for rx, label in rules.STRAY_MARKUP:
            m = rx.search(text)
            if m:
                rep.defect("markup", "%s - nothing but the four channels belongs in a prose "
                           "body" % label, path=p, line=ch.line_of(off),
                           detail=m.group(0).strip()[:80])
                break

    _scene_breaks(ch, rep)


def _scene_breaks(ch, rep):
    """Any line that is nothing but break punctuation, held against the one correct form."""
    for m in BREAK_LINE.finditer(ch.body):
        text = m.group(0).strip()
        if text != WELL_FORMED_BREAK:
            rep.warn("scene-break", "scene break is not `%s`" % WELL_FORMED_BREAK,
                     path=ch.path, line=ch.line_of(m.start()), detail=text)


def _texture(ch, rep):
    """How the dialogue sounds, as far as counting can reach.

    Benchmark run #2 shipped five chapters at a healthy 25% share that a reader called stiff and
    unnatural: complete grammatical sentences, nobody interrupting, every line carrying
    exposition. Share cannot see any of that.

    Every finding here is a **note**. They are diagnostics for a human or a revising model to
    weigh, not a gate - `speech-share` was made a defect once and was optimised to 0.2 points
    above it within five chapters. The judgement stays in `dialogue-voice`.
    """
    lines = ch.speech_line_lengths
    if len(lines) < 4:
        return
    p = ch.path
    if ch.speech_fragment_share < 15.0:
        rep.note("texture", "%.0f%% of spoken lines are fragments - real speech breaks off, "
                 "answers in two words, and does not always reach a full stop"
                 % ch.speech_fragment_share, path=p)
    if ch.speech_contraction_rate < 3.0:
        rep.note("texture", "%.1f contractions per 100 spoken words - a cast that never says "
                 "`don't` reads as translated or as written to be read"
                 % ch.speech_contraction_rate, path=p)
    if ch.speech_interruptions == 0:
        rep.note("texture", "nobody is cut off or trails away anywhere in the chapter", path=p)
    _runs, longest = ch.speech_exchange_runs
    if longest < 3:
        rep.note("texture", "longest unbroken exchange is %d line(s) - lines separated by "
                 "narration are a POV character thinking with quotes attached, not a "
                 "conversation" % longest, path=p)
    if ch.narration_between_speech > 45:
        rep.note("texture", "%.0f words of narration between spoken lines on average - the "
                 "dialogue is carrying exposition rather than the scene"
                 % ch.narration_between_speech, path=p)


def _pacing(ch, rep):
    """Where a turn may have been reported instead of played.

    story-craft owns the judgement. These are notes and they settle nothing: a chapter can skip its
    most important beat without one marker, by starting after it. They are printed so a reviser
    knows where to look first, and they are deliberately not gates - two numeric gates in this repo
    have already been optimised rather than satisfied.
    """
    p = ch.path
    marks = ch.summary_markers()

    # The campaign clause gets its own finding, at warn, regardless of the rate.
    #
    # CLAUDE.md section 5 bans this construction and quotes "She had spent three weeks making it
    # true" as the example. That exact sentence is in benchmark run #2's chapter 1, which shipped
    # `status: revised` through all sixteen revision passes - and this file counted it, then
    # printed the count inside a statistics line where nothing had to answer for it. A rule that
    # is measured but never surfaced is not a rule. Warn, not defect, because ordinary past
    # perfect is how English orders two past events; the marker list is already narrowed to verbs
    # that carry a campaign across elapsed time.
    for off, label in marks:
        if not label.startswith("had <verb>"):
            continue
        rep.warn("campaign-clause",
                 "an event reported inside a past-perfect clause - the reader never watched it "
                 "happen (CLAUDE.md section 5)", path=p, line=ch.line_of(off),
                 detail='"%s" - if it matters, it is a scene; if it does not, cut it'
                        % _clause_at(ch, off))

    if ch.summary_marker_rate > 2.5 and len(marks) >= 3:
        rep.note("pacing", "%d reported-event constructions (%.1f per 1000 words) - check whether "
                 "a turn is happening inside one of them"
                 % (len(marks), ch.summary_marker_rate),
                 path=p, line=ch.line_of(marks[0][0]),
                 detail="; ".join(sorted({lbl for _off, lbl in marks}))[:150])
    if ch.speech_ranges and ch.words_before_first_scene > 600:
        rep.note("pacing", "%d words before anyone speaks - the chapter may be summarising its way "
                 "to the scene" % ch.words_before_first_scene, path=p)


def _speech_window(novel, ch, rep):
    """Dialogue starvation is distributional: one quiet chapter is a choice, five is a cast that
    has become scenery.

    Benchmark run #2: a per-chapter floor raised as a defect is a number that decides whether a
    chapter ships, and it was optimised to 0.2 points above the gate within five chapters - the
    writing agent retrofitted a muttering habit onto the MC to clear it. That is finding 6's
    signature on a new metric. Measuring the mean over a window leaves no single-chapter number
    to write toward while still catching the thing the floor exists to catch.
    """
    if ch.number is None:
        return
    window = [c for c in novel.chapters()
              if c.number is not None
              and ch.number - rules.SPEECH_WINDOW < c.number <= ch.number]
    if len(window) < rules.SPEECH_WINDOW:
        return
    shares = [c.speech_share for c in window]
    mean = sum(shares) / len(shares)
    if mean < rules.SPEECH_FLOOR:
        rep.defect("speech-starvation",
                   "chapters %d-%d average %.1f%% spoken aloud, under the %.0f%% floor "
                   "(%s) - the cast has become scenery and every voice check no-ops"
                   % (window[0].number, ch.number, mean, rules.SPEECH_FLOOR,
                      ", ".join("%.1f" % sh for sh in shares)),
                   path=ch.path)


def _closer_window(novel, ch, rep):
    """How the chapter ends, measured over a window rather than per chapter.

    Benchmark run #2 closed four of five chapters on a short line of narration with nobody
    speaking - "The gate hung open." / "The small hand found hers, tighter, in her sleep." /
    "Neither did Enko." / "The door stayed shut, this time, and nobody was watching it." Each is
    a good last line. Four in a row is a tic, and a reader registers it as sameness long before
    they could say what is repeating.

    Distributional for the same reason `speech-share` is: a per-chapter rule here would be
    satisfied by appending a sentence, which is not the change anybody wants.
    """
    if ch.number is None:
        return
    window = [c for c in novel.chapters()
              if c.number is not None
              and ch.number - rules.CLOSER_WINDOW < c.number <= ch.number]
    if len(window) < rules.CLOSER_WINDOW:
        return
    short = [c for c in window if c.closes_on_short_beat]
    if len(short) > rules.CLOSER_WINDOW_MAX:
        rep.warn("closer-sameness",
                 "%d of the last %d chapters end on a short withheld beat with nobody speaking "
                 "- vary the shape (hook-and-pacing, the eight hook types)"
                 % (len(short), len(window)),
                 path=ch.path,
                 detail="\n         ".join("ch%s: %s" % (c.number, c.closing_sentence[:72])
                                           for c in short))


# ---------------------------------------------------------- Pass 7 and Pass 8

def _phrases(ch, rep):
    p = ch.path
    for off, hit, label in rules.scan(ch.body, rules.MTL_BANNED):
        rep.defect("mtl", "banned phrase: %s" % label, path=p, line=ch.line_of(off),
                   detail='"%s" - rewrite the sentence, do not swap a synonym' % hit)

    for off, hit, label in rules.scan(ch.body, rules.AI_DEFAULT):
        rep.defect("ai-default", "cut-list phrase: %s" % label, path=p,
                   line=ch.line_of(off),
                   detail='"%s" - rewrite it, or if it is deliberate (a register being '
                          'quoted, a character\'s own words) say so in the revision report'
                          % hit)

    bangs = [m for m in re.finditer(r"!", ch.outside_speech)]
    for m in bangs:
        rep.defect("narration-bang", "exclamation mark outside dialogue", path=p,
                   line=ch.line_of(m.start()))

    qs = [m for m in re.finditer(r"\?", ch.outside_speech)]
    if qs:
        rep.warn("rhetorical-q",
                 "%d question mark(s) in narration - mtl-detox allows one per ten chapters, "
                 "and only as genuine deep-distance thought" % len(qs),
                 path=p, line=ch.line_of(qs[0].start()))

    for off, hit, label in rules.scan(ch.outside_speech, rules.GESTURES):
        rep.warn("gesture", "default gesture set: %s - a beat that identifies nobody is stage "
                 "business" % label, path=p, line=ch.line_of(off))

    for off, hit, label in rules.scan(ch.outside_speech, rules.FILTER_VERBS):
        rep.note("filter-verb", "filter verb `%s`" % hit, path=p, line=ch.line_of(off))

    for off, hit, label in rules.scan(ch.outside_speech, rules.WEASEL):
        rep.note("weasel", "`%s`" % hit, path=p, line=ch.line_of(off))


def _rhythm(ch, rep):
    p = ch.path
    paras = ch.paragraphs()

    prev_word = None
    for off, text in paras:
        first = re.sub(r"^[^\w]*", "", text).split(" ")[0].strip(".,;:!?\"'").lower()
        if first and first == prev_word:
            rep.warn("para-opening", "paragraph opens on the same word as the one before "
                     "it (`%s`)" % first, path=p, line=ch.line_of(off))
        prev_word = first

    for off, text in paras:
        n = len(text.split())
        if n > 100 and not re.search(r'^[“"]', text.strip()):
            rep.warn("phone-legibility",
                     "%d-word paragraph - over about six lines on a laptop is a wall on a "
                     "phone" % n, path=p, line=ch.line_of(off))

    sents = ch.narration_sentences()
    run, run_start = [], None
    for off, text in sents:
        n = len(text.split())
        if not run:
            run, run_start = [n], off
            continue
        if abs(n - (sum(run) / float(len(run)))) <= 2.0:
            run.append(n)
        else:
            if len(run) >= 5:
                rep.warn("sentence-rhythm",
                         "%d consecutive narration sentences of near-identical length (~%d "
                         "words)" % (len(run), int(sum(run) / len(run))),
                         path=p, line=ch.line_of(run_start))
            run, run_start = [n], off
    if len(run) >= 5:
        rep.warn("sentence-rhythm",
                 "%d consecutive narration sentences of near-identical length (~%d words)"
                 % (len(run), int(sum(run) / len(run))), path=p, line=ch.line_of(run_start))


# --------------------------------------------------------------- Pass 9b

def _anchor(novel, ch, rep):
    if ch.number is None or ch.number > novel.opening_last_ch:
        return
    terms = novel.anchor_terms()
    if not terms:
        rep.warn("anchor", "no anchor terms declared - add an `anchor?` column to "
                 "bible/lexicon.md", path=novel.path("bible", "lexicon.md"))
        return
    hits, found = 0, []
    for display, rx in terms:
        n = len(rx.findall(ch.body))
        if n:
            hits += n
            found.append("%s x%d" % (display, n))
    if hits == 0:
        rep.defect("anchor",
                   "zero anchor-vocabulary hits inside the opening arc (ch <= %d) - a reader "
                   "cannot place this chapter" % novel.opening_last_ch, path=ch.path)
    else:
        rep.info("anchor vocabulary (ch %s)" % ch.number, ["   %d hits: %s" % (hits, ", ".join(found))])


# ----------------------------------------------------------- ledger agreement

def _ledger(novel, ch, rep):
    if ch.number is None:
        return
    block = novel.block(ch.number)
    if block is None:
        rep.defect("ledger", "no `=C%04d=` block in state/continuity.md - a chapter written "
                   "without its CCS block is a bug" % ch.number,
                   path=novel.path("state", "continuity.md"))
        return
    if block.wc is not None and block.wc != ch.words:
        rep.defect("ledger", "CCS block says wc:%d, body measures %d"
                   % (block.wc, ch.words), path=novel.path("state", "continuity.md"),
                   line=block.line_no)
    ev_ch = str(ch.meta.get("event", "")).strip().lower()
    ev_bl = block.get("ev").strip().lower()
    if ev_ch and ev_bl:
        # The event has to be one of the things the ledger says happened. Compare on content
        # words, because `ev>` is a slash-separated list of clauses and the frontmatter is one.
        stop = {"the", "a", "an", "to", "of", "and", "her", "his", "their", "in", "on", "at",
                "for", "with", "about", "it", "she", "he", "they", "them", "that", "from"}
        want = {w for w in re.findall(r"[a-z']{3,}", ev_ch) if w not in stop}
        have = {w for w in re.findall(r"[a-z']{3,}", ev_bl) if w not in stop}
        if want and len(want & have) * 2 < len(want):
            rep.warn("ledger", "`event:` is not recognisable in the block's `ev>` line - the "
                     "chapter's headline event should be one of the things the ledger records",
                     path=novel.path("state", "continuity.md"), line=block.line_no,
                     detail="fm:  %s\n         ccs: %s" % (ev_ch[:80], ev_bl[:80]))

    dlv_ch = str(ch.meta.get("delivers", "")).strip().lower().rstrip(".")
    dlv_bl = block.get("dlv").strip().lower().rstrip(".")
    if dlv_ch and dlv_bl and dlv_ch[:40] != dlv_bl[:40]:
        rep.warn("ledger", "`delivers:` and the block's `dlv>` do not match",
                 path=novel.path("state", "continuity.md"), line=block.line_no,
                 detail="fm:  %s\n         ccs: %s" % (dlv_ch[:80], dlv_bl[:80]))


def run(novel, numbers=None):
    rep = Report("lint - %s" % novel.title)
    chapters = novel.chapters()
    if numbers:
        chapters = [c for c in chapters if c.number in numbers]
        if not chapters:
            rep.defect("usage", "no chapter file for %s"
                       % ", ".join(str(n) for n in sorted(numbers)))
            return rep
    for ch in chapters:
        runs, longest = ch.speech_exchange_runs
        rep.info(ch.name, [
            "   %d words | speech %.0f%% | thought %d/%d | meta %d | breaks %d"
            % (ch.words, ch.speech_share, len(ch.thoughts()), rules.THOUGHT_BUDGET,
               len(ch.metas()), ch.scene_breaks()),
            "   dialogue texture: %d lines, mean %.1f words (spread %.1f) | contractions "
            "%.1f/100 | fragments %.0f%% | cut off %d | exchanges %d, longest %d | narration "
            "between %.0f words"
            % (len(ch.speech_line_lengths), ch.speech_line_mean, ch.speech_line_spread,
               ch.speech_contraction_rate, ch.speech_fragment_share, ch.speech_interruptions,
               runs, longest, ch.narration_between_speech),
            "   pacing: %d summary marker(s), %.1f per 1000 words | %d words before the first "
            "scene"
            % (len(ch.summary_markers()), ch.summary_marker_rate,
               ch.words_before_first_scene)])
        lint_chapter(novel, ch, rep)
    # Novel-level, so evaluated once for the last chapter in the requested set rather than once
    # per chapter. `sw lint -c 7` asks about the window ending at 7; `--all` asks about the book.
    _speech_window(novel, chapters[-1], rep)
    _closer_window(novel, chapters[-1], rep)
    return rep
