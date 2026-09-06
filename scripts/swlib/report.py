"""Findings and their rendering.

One line per finding, `path:line: [check] message`, because the reader is usually a model
paying by the token to read it back.
"""

import os

DEFECT = "defect"
WARN = "warn"
NOTE = "note"

_ORDER = {DEFECT: 0, WARN: 1, NOTE: 2}
_LABEL = {DEFECT: "DEFECT", WARN: "warn", NOTE: "note"}


class Finding(object):
    __slots__ = ("level", "check", "path", "line", "message", "detail")

    def __init__(self, level, check, message, path=None, line=None, detail=None):
        self.level = level
        self.check = check
        self.message = message
        self.path = path
        self.line = line
        self.detail = detail

    def where(self):
        if not self.path:
            return "-"
        p = self.path.replace(os.sep, "/")
        return "%s:%d" % (p, self.line) if self.line else p

    def render(self):
        out = "%-6s %s: [%s] %s" % (_LABEL[self.level], self.where(), self.check, self.message)
        if self.detail:
            out += "\n         %s" % self.detail
        return out


class Report(object):
    def __init__(self, title=""):
        self.title = title
        self.findings = []
        self.sections = []      # (heading, [lines]) informational output

    # ------------------------------------------------------------- collecting

    def add(self, level, check, message, path=None, line=None, detail=None):
        self.findings.append(Finding(level, check, message, path, line, detail))

    def defect(self, check, message, **kw):
        self.add(DEFECT, check, message, **kw)

    def warn(self, check, message, **kw):
        self.add(WARN, check, message, **kw)

    def note(self, check, message, **kw):
        self.add(NOTE, check, message, **kw)

    def info(self, heading, lines):
        self.sections.append((heading, [l for l in lines]))

    def extend(self, other):
        self.findings.extend(other.findings)
        self.sections.extend(other.sections)

    # -------------------------------------------------------------- rendering

    def count(self, level):
        return sum(1 for f in self.findings if f.level == level)

    @property
    def exit_code(self):
        return 1 if self.count(DEFECT) else 0

    def render(self, show=NOTE, max_per_check=6):
        out = []
        if self.title:
            out.append(self.title)
            out.append("=" * len(self.title))
        for heading, lines in self.sections:
            out.append("")
            out.append("-- %s" % heading)
            out.extend(lines)
        limit = _ORDER[show]
        shown = [f for f in self.findings if _ORDER[f.level] <= limit]
        if shown:
            out.append("")
            out.append("-- findings")
            seen = {}
            for f in sorted(shown, key=lambda x: (_ORDER[x.level], x.check, x.path or "", x.line or 0)):
                seen[f.check] = seen.get(f.check, 0) + 1
                if seen[f.check] > max_per_check:
                    continue
                out.append(f.render())
            for check, n in sorted(seen.items()):
                if n > max_per_check:
                    out.append("       ... %d more [%s], %d shown" % (n - max_per_check, check, max_per_check))
        out.append("")
        out.append("%d defect(s), %d warning(s), %d note(s)"
                   % (self.count(DEFECT), self.count(WARN), self.count(NOTE)))
        return "\n".join(out)
