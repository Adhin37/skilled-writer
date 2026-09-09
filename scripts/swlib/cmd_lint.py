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
    rep = rep or Report()
    p = ch.path
    body = ch.body
    outside = ch.outside_speech

    _frontmatter(novel, ch, rep)
    _channels(novel, ch, rep)
    _texture(ch, rep)
    _speech_window(novel, ch, rep)
    _phrases(ch, rep)
    _rhythm(ch, rep)
    _anchor(novel, ch, rep)
    _ledger(novel, ch, rep)
    return rep


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

    status = str(ch.meta.get("status", "")).strip()
    if status and status not in VALID_STATUS:
        rep.warn("frontmatter", "status `%s` is not one of %s"
                 % (status, "/".join(VALID_STATUS)), path=p, line=1)

    num = ch.meta.get("number")
    fname = re.match(r"^(\d+)", ch.name)
    if isinstance(num, int) and fname and int(fname.group(1)) != num:
        rep.defect("frontmatter", "number: %d but the filename says %s"
                   % (num, fname.group(1)), path=p, line=1)


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
               runs, longest, ch.narration_between_speech)])
        lint_chapter(novel, ch, rep)
    return rep
