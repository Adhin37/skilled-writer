"""Synthetic novels, built in a temp directory.

`novels/` holds the template and nothing else — no book is committed to this repo — so the
tests build what they need from the real `novels/_template` and fill in only the files under
test. Copying the shipped template rather than inventing a scaffold means a test fails when
the template drifts away from the parsers, which is the point.
"""

import os
import shutil
import sys
import tempfile

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCRIPTS = os.path.join(REPO, "scripts")
TEMPLATE = os.path.join(REPO, "novels", "_template")

if SCRIPTS not in sys.path:
    sys.path.insert(0, SCRIPTS)

from swlib.novelio import Novel  # noqa: E402


NOVEL_MD = """---
title: "The Test Book"
slug: "test-book"
genre: fantasy
status: drafting

narration:
  person: third-limited
  tense: past

pov:
  mode: single

mc:
  name: Rin
  intel_tier: 3
  foreknowledge: false
  form_locked: false

chapters:
  length_band: "1500-2600"
  arc_length: 25

channels:
  speech: '"…"'
  thought: "'…'"
  meta: "[…]"

opening:
  anchor_by_ch: 1
  contract_by_ch: 3
---

# Hook (platform blurb)

A test book.
"""

CHAPTER = """---
number: {number}
title: "{title}"
pov: Rin
arc: 1
event: "{event}"
delivers: "{delivers}"
wordcount: {wordcount}
status: drafted
---

{body}
"""

CCS_BLOCK = """=C{number:04d}= pov:Rin | loc:Ashfall Market | t:D1 dusk | wc:{wc} | arc:1
dlv> {dlv}
ev> walks to the market / argues with the clerk / leaves without the permit
chg> Rin: calm->rattled
kno> Rin+{{the clerk was told to refuse her}} ; reader+{{who told him}}
thr> ~T01(permit-refused)
obj> get the permit -> next: find who told the clerk
wld> the guild moves a file
hook> the clerk locks the door behind her
"""


class NovelFixture(object):
    """A throwaway novel on disk. Use as a context manager."""

    def __init__(self, slug="test-book", novel_md=NOVEL_MD):
        self.slug = slug
        self._novel_md = novel_md
        self._tmp = None
        self.root = None

    def __enter__(self):
        self._tmp = tempfile.mkdtemp(prefix="sw-test-")
        self.repo_root = self._tmp
        self.root = os.path.join(self._tmp, "novels", self.slug)
        shutil.copytree(TEMPLATE, self.root)
        # A usable repo root: `newnovel` and `resolve` both look for novels/_template.
        shutil.copytree(TEMPLATE, os.path.join(self._tmp, "novels", "_template"))
        self.write("novel.md", self._novel_md)
        return self

    def __exit__(self, *exc):
        shutil.rmtree(self._tmp, ignore_errors=True)
        return False

    # ----------------------------------------------------------------- writing

    def path(self, *parts):
        return os.path.join(self.root, *parts)

    def write(self, relpath, text, newline="\n", bom=False):
        full = self.path(*relpath.split("/"))
        parent = os.path.dirname(full)
        if not os.path.isdir(parent):
            os.makedirs(parent)
        data = text.replace("\n", newline) if newline != "\n" else text
        with open(full, "w", encoding="utf-8", newline="") as fh:
            if bom:
                fh.write("﻿")
            fh.write(data)
        return full

    def read_bytes(self, relpath):
        with open(self.path(*relpath.split("/")), "rb") as fh:
            return fh.read()

    def add_chapter(self, number, body, title=None, delivers="something changed",
                    wordcount=None, newline="\n", bom=False, frontmatter=None,
                    event="Rin argues with the clerk and leaves without the permit"):
        title = title or "Chapter %d" % number
        if wordcount is None:
            wordcount = len(body.split())
        text = frontmatter if frontmatter is not None else CHAPTER.format(
            number=number, title=title, event=event, delivers=delivers,
            wordcount=wordcount, body=body)
        return self.write("chapters/%04d-chapter.md" % number, text,
                          newline=newline, bom=bom)

    def add_ledger(self, numbers, wcs=None):
        """Append one CCS block per chapter number."""
        blocks = []
        for i, n in enumerate(numbers):
            wc = (wcs or {}).get(n, 100) if isinstance(wcs, dict) else (
                wcs[i] if wcs else 100)
            blocks.append(CCS_BLOCK.format(number=n, wc=wc,
                                           dlv="Rin cannot get the permit"))
        with open(self.path("state", "continuity.md"), encoding="utf-8") as fh:
            base = fh.read()
        self.write("state/continuity.md", base + "\n" + "\n".join(blocks))

    def novel(self):
        return Novel(self.root)


# ------------------------------------------------------------------ prose samples

# The standard English convention: a speech running over several paragraphs opens a quote on
# each paragraph and closes only on the last one.
MULTI_PARAGRAPH_SPEECH = '''"I was there when the levee went," she said.

"We waited three days for the water to drop. Nobody came up the road, and nobody was going to,
because the road was under eleven feet of it and the bridge had gone the same night.

"By the fourth day we walked out over the fields."

The rain had not stopped since.
'''
