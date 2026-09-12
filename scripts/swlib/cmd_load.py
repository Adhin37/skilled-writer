"""`sw load` - what the toolkit hands a drafter before a word of story state.

Every other command measures the novel. This one measures the *instructions*, and it exists
because nothing did: the corpus grew to 118 files and 3,942 negations with no number anywhere
that anyone had to answer for. `docs/creative-latitude.md` is the measurement that prompted it.

It counts four things per phase, resolved against this novel and chapter so the answer is the
real load rather than the corpus total:

    cards        how many files the dispatcher opens
    words        how much procedure that is
    checkboxes   how many compliance items are live at once
    negations    how much of the text is a prohibition

**A maintainer number, never a chapter gate.** Nothing here says a chapter is good or bad, and
no drafting decision may cite it. The one place it is enforced is `sw health`, against the corpus
rather than against any novel - see `rules.CARD_BUDGET` for the count and
`rules.CARD_WORD_BUDGET` for the words, which is the number a drafter actually pays.
"""

import os
import re

from . import kb, kbexpr, rules
from .report import Report

# The prohibition vocabulary. Deliberately plain and deliberately fixed: this is a trend line,
# and a list that grows every time somebody thinks of another negative word measures the list
# rather than the corpus.
NEGATION = re.compile(
    r"\b(never|no|not|nothing|nobody|ban|bans|banned|forbidden|defect|fail|fails|failed|failure"
    r"|avoid|cannot|wrong|violation|prohibited)\b", re.I)
CHECKBOX = re.compile(r"^\s*- \[ \]", re.M)
FRONTMATTER = re.compile(r"^---\n.*?\n---\n", re.S)


def measure(path):
    """(words, checkboxes, negations) for one knowledge file, frontmatter excluded."""
    try:
        with open(path, encoding="utf-8") as fh:
            body = FRONTMATTER.sub("", fh.read())
    except (IOError, OSError):
        return 0, 0, 0
    return len(body.split()), len(CHECKBOX.findall(body)), len(NEGATION.findall(body))


def _phase(idx, ctx, kind, phase=None):
    fired, skipped = idx.cards(kind, ctx, phase=phase)
    rows, totals = [], [0, 0, 0]
    for f, _state, _why in fired:
        w, b, n = measure(f.path)
        rows.append((f.owner, w, b, n))
        totals = [totals[0] + w, totals[1] + b, totals[2] + n]
    return rows, totals, len(skipped)


def run(novel, number, repo_root="."):
    rep = Report("load - %s, chapter %s" % (novel.title, number))
    idx = kb.index(repo_root)
    ctx = kbexpr.Context(novel, chapter=number, speakers=0)

    grand = [0, 0, 0, 0]
    for label, kind, phase in (("A  the brief", "draft-card", "A"),
                               ("B  the draft", "draft-card", "B"),
                               ("C  the gate", "audit-card", None)):
        rows, totals, skipped = _phase(idx, ctx, kind, phase)
        if not rows:
            continue
        grand = [grand[0] + len(rows), grand[1] + totals[0],
                 grand[2] + totals[1], grand[3] + totals[2]]
        lines = ["   %-24s %6s %6s %6s" % ("card", "words", "boxes", "negs")]
        for owner, w, b, n in sorted(rows, key=lambda r: -r[1]):
            lines.append("   %-24s %6d %6d %6d" % (owner[:24], w, b, n))
        lines.append("   %-24s %6d %6d %6d" % ("-- total", totals[0], totals[1], totals[2]))
        rep.info("phase %s - %d cards, %d not opened" % (label, len(rows), skipped), lines)

    rep.info("the whole chapter", [
        "   %d cards | %d words of instruction | %d checkboxes | %d negations"
        % tuple(grand),
        "   Reached before any story state. A maintainer number: nothing here scores a chapter,",
        "   and no drafting decision may cite it (docs/creative-latitude.md)."])

    # The corpus-level budget, reported here as context rather than enforced. `sw health` owns
    # the enforcement, because the budget is a property of the corpus and not of this novel.
    always = _always_counts(idx)
    lines = ["   %-12s %6s %7s %8s %8s" % ("kind", "cards", "budget", "words", "wbudget")]
    for kind in ("draft-card", "audit-card"):
        count, words = always[kind]
        lines.append("   %-12s %6d %7d %8d %8d"
                     % (kind, count, rules.CARD_BUDGET[kind], words,
                        rules.CARD_WORD_BUDGET[kind]))
    lines += [
        "   Both are bounded now. The count budget forced seven merges and the load rose",
        "   anyway - 16,359 words to 16,550 - because a merged card costs what its two",
        "   halves cost separately, so the ratchet was on the wrong number. The word",
        "   budget is a ceiling to lower, never a target to fill",
        "   (docs/creative-latitude.md item 6).",
    ]
    rep.info("the unconditional set - what every novel pays, every chapter", lines)

    over = [(k, v[0], rules.CARD_BUDGET[k])
            for k, v in always.items() if v[0] > rules.CARD_BUDGET[k]]
    if over:
        rep.warn("card-budget",
                 "%s - past the budget, a new card must merge with an existing one rather than "
                 "join the queue" % "; ".join(
                     "%s carries %d always-on cards against a budget of %d" % (k, v, cap)
                     for k, v, cap in over))
    return rep


def _always_counts(idx):
    """Unconditional cards by kind - what *every* novel pays, which is what the budget bounds.

    Returns (count, words). The count is the enforced number; the words are recorded beside it
    because the count is what the budget moved and the words are what a chapter actually pays.
    """
    out = {}
    for kind in ("draft-card", "audit-card"):
        live = [f for f in idx.by_type(kind) if not f.when or f.when.strip() == "always"]
        out[kind] = (len(live), sum(measure(f.path)[0] for f in live))
    return out
