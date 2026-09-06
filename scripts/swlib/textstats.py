"""Chapter body analysis: the four channels, paragraphs, sentences, offsets.

The channel regexes are ported verbatim from docs/check-chapters.sh, which had them right:
a thought mark opens at a word boundary and closes before punctuation or space, so bare
contractions (don't, she'd) and plural possessives (the boys' room) can never match, and a
word-internal apostrophe is allowed inside a thought so 'Start with what you're sure of.'
parses as one thought and not zero. Speech spans are stripped before thought and meta are
counted, because a '...' inside a "..." is a nested quotation and not thought.
"""

import os
import re

from . import mdio

SPEECH = re.compile(r'[“"][^”"]*[”"]')
META = re.compile(r"\[[^\]\n]*\]")
THOUGHT = re.compile(
    r"(?:(?<=^)|(?<=[\s(\"“—–]))"
    r"'((?:[^'\n]|(?<=\w)'(?=\w))+?)'"
    r"(?=[\s.,;:!?)\"”—–]|$)",
    re.M,
)
SENTENCE_END = re.compile(r"[.!?]+[\"”')\]]*(?:\s+|$)")


def _blank(match):
    """Replace a span with spaces so downstream offsets stay valid."""
    return " " * (match.end() - match.start())


class Chapter(object):
    def __init__(self, path):
        self.path = path
        self.name = os.path.basename(path)
        text = mdio.read_text(path)
        fm_text, body = mdio.split_frontmatter(text)
        self.frontmatter_text = fm_text
        self.meta = mdio.parse_yaml(fm_text) if fm_text else {}
        self.body = body
        # line number in the file at which the body starts (1-based)
        self.body_start_line = text[: len(text) - len(body)].count("\n") + 1
        self._line_starts = None

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
            starts, pos = [0], 0
            for ch in self.body:
                pos += 1
                if ch == "\n":
                    starts.append(pos)
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
    def speech_spans(self):
        return SPEECH.findall(self.body)

    @property
    def speech_words(self):
        return sum(len(s.split()) for s in self.speech_spans)

    @property
    def speech_share(self):
        total = self.words
        return (self.speech_words * 100.0 / total) if total else 0.0

    @property
    def outside_speech(self):
        """Body with speech spans blanked out, offsets preserved."""
        return SPEECH.sub(_blank, self.body)

    def thoughts(self):
        return list(THOUGHT.finditer(self.outside_speech))

    def metas(self):
        return list(META.finditer(self.outside_speech))

    def unterminated_thoughts(self):
        """Lines that open a thought mark at a word boundary and never close it."""
        out = []
        for i, line in enumerate(self.outside_speech.split("\n")):
            if re.search(r"(^|[\s(\[\-])'[^']{2,}$", line):
                out.append((self.body_start_line + i, line.strip()))
        return out

    def nested_thought_in_speech(self):
        """`'...'` pairs living inside a `"..."` span - legal, but worth counting."""
        n = 0
        for span in self.speech_spans:
            n += len(THOUGHT.findall(span))
        return n

    # -------------------------------------------------------------- structure

    def paragraphs(self):
        """(offset, text) for every non-empty paragraph."""
        out, pos = [], 0
        for chunk in self.body.split("\n\n"):
            if chunk.strip():
                out.append((pos + len(chunk) - len(chunk.lstrip()), chunk.strip()))
            pos += len(chunk) + 2
        return out

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
        """Sentences with no speech in them at all."""
        return [(o, s) for o, s in self.sentences() if not SPEECH.search(s)]

    def scene_breaks(self):
        return len(re.findall(r"^\s*\*\s\*\s\*\s*$", self.body, re.M))


def load_chapters(chapters_dir):
    """Every NNNN-*.md chapter in a directory, ordered by number."""
    if not os.path.isdir(chapters_dir):
        return []
    out = []
    for name in sorted(os.listdir(chapters_dir)):
        if re.match(r"^\d+.*\.md$", name):
            out.append(Chapter(os.path.join(chapters_dir, name)))
    return out
