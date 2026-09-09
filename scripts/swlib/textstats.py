"""Chapter body analysis: the four channels, paragraphs, sentences, offsets.

Three properties of English prose the first version of this file got wrong, all of which made
the gate quieter rather than louder:

1. **Multi-paragraph speech.** A speech running over several paragraphs opens a quote on each
   one and closes only on the last. A regex pairing quote marks greedily reads paragraph two as
   narration, so its dialogue is counted as narration words *and* swept for narration defects.
   Spans are therefore found by a scan that is bounded to a paragraph: an unclosed quote runs to
   the end of its paragraph and no further.
2. **Curly marks.** `'` and `‘…’` are the same channel to a reader and different characters to a
   regex. Each channel owns an *open set* and a *close set* covering both, so a chapter typed in
   a word processor measures the same as one typed in vim.
3. **Leading-apostrophe elisions.** `'twas`, `'em` and `'99` are ordinary serial-fiction voice
   and are not unterminated thoughts.

The marks themselves come from `novel.md` → `channels:` rather than from literals here, so
changing that block changes what the linter measures. A word-internal apostrophe is still
allowed inside a thought, so `'Start with what you're sure of.'` is one thought and not zero.
"""

import os
import re

from . import mdio

# Quote families. A channel declares one character; the reader sees the whole family.
_DOUBLE_OPEN = ('"', "“")
_DOUBLE_CLOSE = ('"', "”")
_SINGLE_OPEN = ("'", "‘")
_SINGLE_CLOSE = ("'", "’")

# Leading-apostrophe elisions that are words, not opened thought marks.
_ELISIONS = (
    "twas", "tis", "twere", "em", "im", "er", "n", "cause", "bout", "round",
    "til", "till", "tween", "neath", "gainst", "fore", "way", "kay", "nother",
)
_ELISION_RE = re.compile(
    r"^(?:%s)\b" % "|".join(_ELISIONS) + r"|^\d{2}\b",
    re.I,
)

# An apostrophe with a letter on both sides is a contraction wherever it appears - the same rule
# that keeps `'Start with what you're sure of.'` from breaking the thought parser.
_CONTRACTION_RE = re.compile(r"\b\w+[\u2019']\w+\b")

_PARA_SPLIT = re.compile(r"\n[ \t]*\n")
SENTENCE_END = re.compile(r"[.!?]+[\"”'’)\]]*(?:\s+|$)")


def _family(ch, opening):
    """Expand one declared mark character into the set a reader would accept."""
    if ch in _DOUBLE_OPEN or ch in _DOUBLE_CLOSE:
        return set(_DOUBLE_OPEN if opening else _DOUBLE_CLOSE)
    if ch in _SINGLE_OPEN or ch in _SINGLE_CLOSE:
        return set(_SINGLE_OPEN if opening else _SINGLE_CLOSE)
    return {ch}


def _marks(spec, default_open, default_close):
    """('"…"', '"', '"') -> ({'"', '“'}, {'"', '”'}). Junk falls back to the defaults."""
    s = str(spec or "").strip()
    if s[:1] in ("'", '"') and s[-1:] == s[:1] and len(s) > 2:
        s = s[1:-1].strip()          # the config value may itself be quoted
    if len(s) < 2:
        return _family(default_open, True), _family(default_close, False)
    return _family(s[0], True), _family(s[-1], False)


def _cls(chars):
    return "[%s]" % "".join(sorted(re.escape(c) for c in chars))


class Channels(object):
    """The four text channels, as the marks that carry them."""

    def __init__(self, speech=None, thought=None, meta=None):
        self.speech_open, self.speech_close = _marks(speech, '"', '"')
        self.thought_open, self.thought_close = _marks(thought, "'", "'")
        self.meta_open, self.meta_close = _marks(meta, "[", "]")
        self.speech_marks = self.speech_open | self.speech_close
        self._thought_re = None
        self._meta_re = None
        self._unterminated_re = None

    @classmethod
    def from_novel(cls, novel):
        if novel is None:
            return cls()
        return cls(
            speech=novel.get("channels.speech"),
            thought=novel.get("channels.thought"),
            meta=novel.get("channels.meta"),
        )

    @property
    def thought_re(self):
        """Open at a boundary, close before punctuation or space, allow word-internal marks."""
        if self._thought_re is None:
            opens, closes = _cls(self.thought_open), _cls(self.thought_close)
            lead = _cls(set(" \t(") | self.speech_open | {"—", "–"})
            trail = _cls(set(" \t.,;:!?)") | self.speech_close | {"—", "–"})
            self._thought_re = re.compile(
                r"(?:(?<=^)|(?<=%s))" % lead
                + opens
                + r"((?:[^%s\n]|(?<=\w)%s(?=\w))+?)" % (
                    "".join(sorted(re.escape(c) for c in self.thought_close)), closes)
                + closes
                + r"(?=%s|$)" % trail,
                re.M,
            )
        return self._thought_re

    @property
    def meta_re(self):
        if self._meta_re is None:
            self._meta_re = re.compile(
                _cls(self.meta_open)
                + r"[^%s\n]*" % "".join(sorted(re.escape(c) for c in self.meta_close))
                + _cls(self.meta_close)
            )
        return self._meta_re

    @property
    def unterminated_re(self):
        """A thought mark opened at a boundary with no close before end of line."""
        if self._unterminated_re is None:
            self._unterminated_re = re.compile(
                r"(?:^|[\s(\[\-])(%s)([^%s]{2,})$" % (
                    _cls(self.thought_open),
                    "".join(sorted(re.escape(c) for c in self.thought_close)),
                )
            )
        return self._unterminated_re


DEFAULT_CHANNELS = Channels()


def paragraph_ranges(text):
    """(start, end) for every paragraph, blank-line separated."""
    out, pos = [], 0
    for m in _PARA_SPLIT.finditer(text):
        out.append((pos, m.start()))
        pos = m.end()
    out.append((pos, len(text)))
    return out


def find_speech_spans(text, channels=DEFAULT_CHANNELS):
    """(start, end) for every speech span, never crossing a paragraph boundary.

    An unclosed quote runs to the end of its paragraph. That is the standard convention for a
    speech continuing over several paragraphs, and it is also the only safe reading of a typo.
    """
    opens, closes, marks = channels.speech_open, channels.speech_close, channels.speech_marks
    spans = []
    for pstart, pend in paragraph_ranges(text):
        start = None
        for i in range(pstart, pend):
            c = text[i]
            if c not in marks:
                continue
            if start is None:
                if c in closes and c not in opens:
                    continue                      # a stray closer opens nothing
                start = i
            elif c in opens and c not in closes:
                spans.append((start, i))          # a new opener; the last one never closed
                start = i
            else:
                spans.append((start, i + 1))
                start = None
        if start is not None:
            spans.append((start, pend))
    return spans


def blank_ranges(text, ranges):
    """Replace ranges with spaces, preserving offsets *and* newlines."""
    if not ranges:
        return text
    buf = list(text)
    for start, end in ranges:
        for i in range(start, end):
            if buf[i] != "\n":
                buf[i] = " "
    return "".join(buf)


class Chapter(object):
    def __init__(self, path, channels=None):
        self.path = path
        self.name = os.path.basename(path)
        self.channels = channels or DEFAULT_CHANNELS
        text = mdio.read_text(path)
        fm_text, body = mdio.split_frontmatter(text)
        self.frontmatter_text = fm_text
        self.meta = mdio.parse_yaml(fm_text) if fm_text else {}
        self.body = body
        # line number in the file at which the body starts (1-based)
        self.body_start_line = text[: len(text) - len(body)].count("\n") + 1
        self._line_starts = None
        self._spans = None
        self._outside = None
        self._paragraphs = None

    # ------------------------------------------------------------------ basics

    @property
    def number(self):
        n = self.meta.get("number")
        if isinstance(n, int):
            return n
        m = re.match(r"^(\d+)", self.name)
        return int(m.group(1)) if m else None

    @property
    def words(self):
        """Body word count. Matches `wc -w`."""
        return len(self.body.split())

    def line_of(self, offset):
        """File line number for a character offset into the body."""
        if self._line_starts is None:
            starts = [0]
            pos = self.body.find("\n")
            while pos != -1:
                starts.append(pos + 1)
                pos = self.body.find("\n", pos + 1)
            self._line_starts = starts
        lo, hi = 0, len(self._line_starts) - 1
        while lo < hi:
            mid = (lo + hi + 1) // 2
            if self._line_starts[mid] <= offset:
                lo = mid
            else:
                hi = mid - 1
        return self.body_start_line + lo

    # ---------------------------------------------------------------- channels

    @property
    def speech_ranges(self):
        if self._spans is None:
            self._spans = find_speech_spans(self.body, self.channels)
        return self._spans

    @property
    def speech_spans(self):
        return [self.body[s:e] for s, e in self.speech_ranges]

    @property
    def speech_words(self):
        return sum(len(s.split()) for s in self.speech_spans)

    @property
    def speech_share(self):
        total = self.words
        return (self.speech_words * 100.0 / total) if total else 0.0

    @property
    def outside_speech(self):
        """Body with speech spans blanked out, offsets and line breaks preserved."""
        if self._outside is None:
            self._outside = blank_ranges(self.body, self.speech_ranges)
        return self._outside

    def thoughts(self):
        return list(self.channels.thought_re.finditer(self.outside_speech))

    def metas(self):
        return list(self.channels.meta_re.finditer(self.outside_speech))

    def unterminated_thoughts(self):
        """Lines that open a thought mark at a word boundary and never close it.

        A leading-apostrophe elision (`'twas`, `'em`) or a year (`'99`) is a word, not an
        opened mark, and does not count.
        """
        out = []
        pattern = self.channels.unterminated_re
        for i, line in enumerate(self.outside_speech.split("\n")):
            m = pattern.search(line)
            if m and not _ELISION_RE.match(m.group(2)):
                out.append((self.body_start_line + i, line.strip()))
        return out

    # ------------------------------------------------------------ dialogue texture
    #
    # Benchmark run #2 shipped five chapters at a healthy 25% speech share that a reader
    # nonetheless called stiff and unnatural. Share says how MUCH the cast speaks and nothing
    # about whether it sounds like people. These are the countable halves of that: how long the
    # lines are, how uniform, whether anyone ever speaks in a fragment, whether anyone is ever
    # cut off, and how much narration sits between one line and the next.
    #
    # They are DIAGNOSTICS, printed as measurements. None of them is a gate. A number that
    # decides whether a chapter ships gets optimised - that lesson cost this repo two rewrites.

    @property
    def speech_line_lengths(self):
        return [len(s.split()) for s in self.speech_spans if s.split()]

    @property
    def speech_line_mean(self):
        lens = self.speech_line_lengths
        return (sum(lens) / float(len(lens))) if lens else 0.0

    @property
    def speech_line_spread(self):
        """Population standard deviation of line length. Uniform lines read as written, not said."""
        lens = self.speech_line_lengths
        if len(lens) < 2:
            return 0.0
        mean = sum(lens) / float(len(lens))
        return (sum((n - mean) ** 2 for n in lens) / float(len(lens))) ** 0.5

    @property
    def speech_contraction_rate(self):
        """Contractions per 100 spoken words. Formal registers cluster near zero."""
        words = self.speech_words
        if not words:
            return 0.0
        n = sum(len(_CONTRACTION_RE.findall(s)) for s in self.speech_spans)
        return n * 100.0 / words

    @property
    def speech_fragment_share(self):
        """Share of spoken lines that are not one or more complete sentences.

        A fragment is a line that does not end in terminal punctuation, or that has no verb-like
        run at all. Real speech is full of them; prose written to be read aloud is not.
        """
        spans = [s.strip() for s in self.speech_spans if s.strip()]
        if not spans:
            return 0.0
        frag = 0
        for s in spans:
            inner = s.strip('"\u201c\u201d\u2018\u2019\'').strip()
            if not inner:
                continue
            if not re.search(r"[.!?\u2026]$", inner) or len(inner.split()) <= 3:
                frag += 1
        return frag * 100.0 / len(spans)

    @property
    def speech_interruptions(self):
        """Lines that break off mid-thought - an em dash or ellipsis at the end."""
        n = 0
        for s in self.speech_spans:
            inner = s.strip().strip('"\u201c\u201d').strip()
            if re.search(r"[\u2014\u2013-]{1,2}$|\u2026$|\.\.\.$", inner):
                n += 1
        return n

    @property
    def speech_exchange_runs(self):
        """(runs, longest) over consecutive spoken lines with no paragraph of narration between.

        Two people talking is a run. A line, three paragraphs of analysis, another line is not an
        exchange - it is a POV character thinking with quotes attached.
        """
        marks = []
        for start, end in self.speech_ranges:
            marks.append((start, end))
        if not marks:
            return (0, 0)
        runs, longest, cur = 0, 0, 0
        prev_end = None
        for start, end in marks:
            if prev_end is None:
                cur = 1
            else:
                between = self.body[prev_end:start]
                cur = cur + 1 if len(between.split()) <= 25 else 1
            if cur == 2:
                runs += 1
            longest = max(longest, cur)
            prev_end = end
        return (runs, longest)

    @property
    def narration_between_speech(self):
        """Mean words of narration between one spoken line and the next."""
        gaps = []
        prev_end = None
        for start, end in self.speech_ranges:
            if prev_end is not None:
                gaps.append(len(self.body[prev_end:start].split()))
            prev_end = end
        return (sum(gaps) / float(len(gaps))) if gaps else 0.0

    # ------------------------------------------------------------------ pacing
    #
    # story-craft: pacing is the distribution of detail across events, and the failure this repo
    # has is one-directional - the important beat gets the summary. These locate where to look.
    # None of them judges: a chapter can skip its most important beat with no marker at all, by
    # starting after it.

    @property
    def words_before_first_scene(self):
        """Words before the first spoken line - a rough hand on how long the reader waits."""
        spans = self.speech_ranges
        if not spans:
            return self.words
        return len(self.body[:spans[0][0]].split())

    def summary_markers(self):
        """(offset, label) for each reported-event construction, outside speech."""
        from . import rules
        out = []
        for rx, label in rules.SUMMARY_MARKERS:
            for m in rx.finditer(self.outside_speech):
                out.append((m.start(), label))
        return sorted(out)

    @property
    def summary_marker_rate(self):
        """Markers per 1,000 body words."""
        words = self.words
        return (len(self.summary_markers()) * 1000.0 / words) if words else 0.0

    def nested_thought_in_speech(self):
        """`'...'` pairs living inside a `"..."` span - legal, but worth counting."""
        n = 0
        for span in self.speech_spans:
            n += len(self.channels.thought_re.findall(span))
        return n

    # -------------------------------------------------------------- structure

    def paragraphs(self):
        """(offset, text) for every non-empty paragraph."""
        if self._paragraphs is None:
            out = []
            for start, end in paragraph_ranges(self.body):
                chunk = self.body[start:end]
                if chunk.strip():
                    out.append((start + len(chunk) - len(chunk.lstrip()), chunk.strip()))
            self._paragraphs = out
        return self._paragraphs

    def sentences(self):
        """(offset, text) for every sentence in the body."""
        out, start = [], 0
        for m in SENTENCE_END.finditer(self.body):
            seg = self.body[start:m.end()].strip()
            if seg:
                out.append((start, seg))
            start = m.end()
        tail = self.body[start:].strip()
        if tail:
            out.append((start, tail))
        return out

    def narration_sentences(self):
        """Sentences carrying no speech at all, by offset rather than by re-matching."""
        ranges = self.speech_ranges
        out = []
        for off, seg in self.sentences():
            end = off + len(seg)
            if not any(s < end and off < e for s, e in ranges):
                out.append((off, seg))
        return out

    def scene_breaks(self):
        return len(re.findall(r"^\s*\*\s\*\s\*\s*$", self.body, re.M))


def load_chapters(chapters_dir, channels=None):
    """Every NNNN-*.md chapter in a directory, ordered by number."""
    if not os.path.isdir(chapters_dir):
        return []
    out = []
    for name in sorted(os.listdir(chapters_dir)):
        if re.match(r"^\d+.*\.md$", name):
            out.append(Chapter(os.path.join(chapters_dir, name), channels=channels))
    return out
