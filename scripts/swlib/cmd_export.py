"""`sw export --okf` - project a novel into an Open Knowledge Format bundle.

An export target, never the working format. `novels/<slug>/` stays exactly as it is, because
`sw readset` hands a chapter its *slices* - blocks N-5..N-1, the matrix rows for this chapter's
speakers - and OKF has no concept of a slice. Handing an agent whole files is the cost the
read-set exists to avoid, and that argument is unchanged by anything here.

What the bundle is for is everything outside this repo: another vendor's agent, a wiki, a
teammate's tooling. It is knowledge *about* the novel - cast, world, threads, state, and what
each chapter delivered - not a copy of the prose. Every document carries a `resource:` naming the
repo file it was projected from, so the bundle says where it came from rather than pretending to
be the original.

The projection rule: a table row becomes its own document when it has a stable identity that the
read-set already slices on, because that slicing is the existing proof the row is individually
addressable. Threads have ids; locations are resolved per chapter; CCS blocks are pulled by
number. Voice and competence rows do not - their identity is the character, so they become
sections inside that character's document.

This is the one command that writes more than chapter frontmatter, and it writes only into a
directory that does not yet exist. CLAUDE.md section 4 names it explicitly.
"""

import datetime
import os

from . import mdio
from .report import Report

OKF_VERSION = "0.2"
GENERATED_BY = "skilled-writer/sw-export"


def _now():
    return datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _slug(text):
    out = "".join(c.lower() if c.isalnum() else "-" for c in str(text).strip())
    while "--" in out:
        out = out.replace("--", "-")
    return out.strip("-") or "untitled"


def _yaml(value):
    text = " ".join(str(value or "").split())
    return '"%s"' % text.replace("\\", "\\\\").replace('"', '\\"')


class Bundle(object):
    """Collects documents in memory, then writes them all at once.

    Nothing reaches disk until the whole projection has succeeded, so a failure halfway through
    leaves no half-bundle behind.
    """

    def __init__(self, root, novel):
        self.root, self.novel = root, novel
        self.docs = []

    def add(self, path, kind, title, body, description="", resource=None, extra=None):
        lines = ["---", "type: %s" % kind, "title: %s" % _yaml(title)]
        if description:
            lines.append("description: %s" % _yaml(description))
        if resource:
            lines.append("resource: %s" % _yaml(resource))
        for key, val in sorted((extra or {}).items()):
            lines.append("%s: %s" % (key, _yaml(val)))
        lines.append("generated: {by: %s, at: %s}" % (GENERATED_BY, _now()))
        lines += ["---", "", body.rstrip(), ""]
        self.docs.append((path, "\n".join(lines)))

    def write(self):
        for path, text in self.docs:
            full = os.path.join(self.root, path)
            d = os.path.dirname(full)
            if d and not os.path.isdir(d):
                os.makedirs(d)
            with open(full, "w", encoding="utf-8") as fh:
                fh.write(text)
        return len(self.docs)


def _rel(novel, *parts):
    return os.path.join("novels", os.path.basename(novel.path()), *parts).replace(os.sep, "/")


def build(novel, root):
    b = Bundle(root, novel)
    _novel_doc(b, novel)
    _cast(b, novel)
    _locations(b, novel)
    _threads(b, novel)
    _chapters(b, novel)
    _state(b, novel)
    _index(b, novel)
    _log(b, novel)
    return b


def _novel_doc(b, novel):
    cfg = novel.cfg
    rows = ["| field | value |", "|---|---|"]
    for key in ("genre", "subgenre", "narration.person", "narration.tense", "pov.mode",
                "mc.name", "mc.intel_tier", "scaling.shape", "theme.controlling_idea",
                "ending.contract"):
        val = novel.get(key, "")
        if val not in ("", None):
            rows.append("| `%s` | %s |" % (key, str(val).replace("|", "\\|")))
    body = "\n".join(rows) + "\n\n" + (novel.blurb or "")
    b.add("novel.md", "Novel", novel.title, body,
          description=str(cfg.get("premise") or novel.blurb or "")[:200],
          resource=_rel(novel, "novel.md"))


def _cast(b, novel):
    """One document per named character, with their voice and competence rows folded in."""
    voices = {str(r.first()).strip(): r for r in novel.voice_rows()}
    comps = {}
    for r in novel.competence_rows():
        comps.setdefault(str(r.first()).strip(), []).append(r)
    names = set(voices) | set(comps)
    for path in novel.cast_files():
        names.add(os.path.splitext(os.path.basename(path))[0].replace("-", " ").title())
    for name in sorted(n for n in names if n and not n.startswith("-")):
        parts = []
        if name in voices:
            parts.append("# Voice\n\n%s" % voices[name].raw.strip())
        if name in comps:
            parts.append("# Competence\n\n%s"
                         % "\n".join(r.raw.strip() for r in comps[name]))
        b.add("cast/%s.md" % _slug(name), "Character", name,
              "\n\n".join(parts) or "(no matrix row)",
              description="cast member of %s" % novel.title,
              resource=_rel(novel, "bible", "cast"))


def _locations(b, novel):
    for r in novel.location_rows():
        name = str(r.first()).strip()
        if not name:
            continue
        b.add("world/locations/%s.md" % _slug(name), "Location", name, r.raw.strip(),
              resource=_rel(novel, "bible", "world.md"))


def _threads(b, novel):
    for r in novel.threads():
        tid = str(r.first()).strip()
        if not tid:
            continue
        b.add("threads/%s.md" % _slug(tid), "Thread", tid, r.raw.strip(),
              description=str(r.get("thread") or ""),
              resource=_rel(novel, "state", "threads.md"),
              extra={"status": str(r.get("status") or "")})


def _chapters(b, novel):
    """Frontmatter and what the chapter delivered - deliberately not the prose.

    The bundle is knowledge about the novel. Copying the prose in would make it a second copy of
    the book, and `resource:` already says where the real one is.
    """
    blocks = {blk.number: blk for blk in novel.blocks()}
    for ch in novel.chapters():
        if not ch.number:
            continue
        meta = ch.meta
        rows = ["| field | value |", "|---|---|"]
        for key in ("pov", "arc", "event", "delivers", "wordcount", "status"):
            if meta.get(key) not in (None, ""):
                rows.append("| %s | %s |" % (key, str(meta[key]).replace("|", "\\|")))
        body = "\n".join(rows)
        blk = blocks.get(ch.number)
        if blk:
            body += "\n\n# Continuity\n\n```\n%s\n```" % blk.text.strip()
        links = ["[%s](/threads/%s.md)" % (t, _slug(t)) for t in _thread_ids(blk)]
        if links:
            body += "\n\n# Threads\n\n%s" % ", ".join(links)
        b.add("chapters/%04d.md" % ch.number, "Chapter",
              str(meta.get("title") or "Chapter %d" % ch.number), body,
              description=str(meta.get("delivers") or ""),
              resource=_rel(novel, "chapters", os.path.basename(ch.path)),
              extra={"status": "stable" if str(meta.get("status")) in ("revised", "published")
                     else "draft"})


def _thread_ids(blk):
    import re
    if blk is None:
        return []
    return sorted(set(re.findall(r"\bT\d+", " ".join(blk.keys().get("thr", [])))))


_LEDGERS = (("state/power.md", "Power Ledger", "power.md"),
            ("state/growth.md", "Arc Ladder", "growth.md"),
            ("state/foreknowledge.md", "Foreknowledge Ledger", "foreknowledge.md"),
            ("state/body.md", "Form Ledger", "body.md"),
            ("state/timeline.md", "World Clock", "timeline.md"),
            ("bible/world.md", "World Fact", "world.md"),
            ("bible/society.md", "World Fact", "society.md"),
            ("bible/lexicon.md", "Glossary", "lexicon.md"),
            ("bible/canon.md", "Canon", "canon.md"),
            ("bible/power-system.md", "World Fact", "power-system.md"),
            ("plan/arcs.md", "Plan", "arcs.md"),
            ("plan/chapters.md", "Plan", "chapters.md"),
            ("plan/timeline.md", "Timeline", "timeline.md"))


def _state(b, novel):
    for rel, kind, name in _LEDGERS:
        text = mdio.read_text(os.path.join(novel.path(), rel))
        if not text.strip():
            continue
        out = rel.replace("bible/", "world/").replace("plan/", "plan/")
        b.add(out, kind, name, mdio.split_frontmatter(text)[1] or text,
              resource=_rel(novel, *rel.split("/")))


def _index(b, novel):
    groups = {}
    for path, text in b.docs:
        groups.setdefault(path.split("/")[0] if "/" in path else ".", []).append((path, text))
    lines = ["---", 'okf_version: "%s"' % OKF_VERSION, "---", "",
             "# %s" % novel.title, "",
             "Projected from `%s` by `sw export --okf`. Knowledge about the novel, not the prose."
             % _rel(novel), ""]
    for group in sorted(groups):
        lines.append("## %s" % (group if group != "." else "root"))
        lines.append("")
        for path, text in sorted(groups[group]):
            title = ""
            fm = mdio.parse_yaml(mdio.split_frontmatter(text)[0])
            title = str(fm.get("title") or path)
            desc = str(fm.get("description") or "")
            lines.append("* [%s](/%s)%s" % (title, path, (" - %s" % desc) if desc else ""))
        lines.append("")
    b.docs.append(("index.md", "\n".join(lines)))


def _log(b, novel):
    day = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d")
    b.docs.append(("log.md", "\n".join([
        "# Export log", "", "## %s" % day, "",
        "* **Export**: %d document(s) projected from `%s`." % (len(b.docs), _rel(novel)), ""])))


def run(novel, out_dir):
    rep = Report("export --okf - %s" % novel.title)
    bundle = build(novel, out_dir)
    count = bundle.write()
    kinds = {}
    for path, text in bundle.docs:
        fm = mdio.parse_yaml(mdio.split_frontmatter(text)[0])
        kinds[str(fm.get("type") or "index/log")] = kinds.get(
            str(fm.get("type") or "index/log"), 0) + 1
    rep.info("bundle", ["   %s" % os.path.abspath(out_dir),
                        "   %d document(s), OKF v%s" % (count, OKF_VERSION)]
             + ["   %-18s %d" % (k, v) for k, v in sorted(kinds.items())])
    rep.info("note", ["   An export target, not the working format: `novels/` is unchanged, and",
                      "   `sw readset` still slices it. Validate with `sw kb validate <dir>`."])
    return rep
