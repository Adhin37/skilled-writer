"""Markdown and YAML-frontmatter readers.

Stdlib only. The formats in this repo are regular enough that a real parser is short and a
shell pipeline is not: pipe tables with fixed columns, `key>` ledger lines, and a YAML
frontmatter block that nests two levels deep and uses multi-line quoted scalars.
"""

import os
import re

# --------------------------------------------------------------------------- files


def read_text(path):
    """Read a file as UTF-8 with normalised newlines. Returns '' if it does not exist."""
    if not os.path.isfile(path):
        return ""
    with open(path, encoding="utf-8", errors="replace") as fh:
        return fh.read().replace("\r\n", "\n").replace("\r", "\n")


def read_lines(path):
    text = read_text(path)
    return text.split("\n") if text else []


# --------------------------------------------------------------- frontmatter + YAML

_FM = re.compile(r"\A---\n(.*?)\n---\n?", re.S)


def split_frontmatter(text):
    """Return (frontmatter_text, body). No frontmatter -> ('', text)."""
    m = _FM.match(text)
    if not m:
        return "", text
    return m.group(1), text[m.end():]


def _strip_comment(s):
    """Remove a trailing # comment that is not inside quotes."""
    quote = None
    for i, ch in enumerate(s):
        if quote:
            if ch == quote and (i == 0 or s[i - 1] != "\\"):
                quote = None
        elif ch in "\"'":
            quote = ch
        elif ch == "#" and (i == 0 or s[i - 1] in " \t"):
            return s[:i]
    return s


def _scalar(v):
    """Coerce a YAML scalar to str/int/bool/None."""
    v = v.strip()
    if not v:
        return ""
    if len(v) > 1 and v[0] == v[-1] and v[0] in "\"'":
        return v[1:-1]
    low = v.lower()
    if low in ("true", "yes", "on"):
        return True if low == "true" else v
    if low in ("false", "no", "off"):
        return False if low == "false" else v
    if low in ("null", "~", "none"):
        return None if low != "none" else v
    if re.fullmatch(r"-?\d+", v):
        return int(v)
    if re.fullmatch(r"-?\d+\.\d+", v):
        return float(v)
    if v.startswith("[") and v.endswith("]"):
        inner = v[1:-1].strip()
        if not inner:
            return []
        return [_scalar(x) for x in _split_inline(inner)]
    return v


def _split_inline(s):
    """Split a bracketed inline list on commas that are not inside quotes."""
    out, buf, quote = [], "", None
    for ch in s:
        if quote:
            if ch == quote:
                quote = None
            buf += ch
        elif ch in "\"'":
            quote = ch
            buf += ch
        elif ch == ",":
            out.append(buf)
            buf = ""
        else:
            buf += ch
    if buf.strip():
        out.append(buf)
    return out


def _unterminated_quote(v):
    """True if v opens a quoted scalar that does not close on this line."""
    v = v.strip()
    if not v or v[0] not in "\"'":
        return False
    q = v[0]
    return not (len(v) > 1 and v.rstrip().endswith(q))


def parse_yaml(text):
    """Minimal YAML reader for this repo's frontmatter.

    Handles nested maps, `- ` lists, inline `[a, b]` lists, `#` comments outside quotes, and
    multi-line double/single quoted scalars (which novel.md uses for prose fields). It does
    not handle anchors, block scalars or flow maps, none of which appear here.
    """
    root = {}
    # stack of (indent, container)
    stack = [(-1, root)]
    lines = text.split("\n")
    i = 0
    while i < len(lines):
        raw = lines[i]
        i += 1
        if not raw.strip() or raw.lstrip().startswith("#"):
            continue
        indent = len(raw) - len(raw.lstrip(" "))
        line = _strip_comment(raw).rstrip()
        if not line.strip():
            continue
        stripped = line.strip()

        while stack and indent <= stack[-1][0] and len(stack) > 1:
            stack.pop()
        container = stack[-1][1]

        if stripped.startswith("- "):
            val = stripped[2:].strip()
            if isinstance(container, list):
                while _unterminated_quote(val) and i < len(lines):
                    val = val + " " + lines[i].strip()
                    i += 1
                container.append(_scalar(val))
            continue

        m = re.match(r"^([A-Za-z0-9_.\-]+):\s*(.*)$", stripped)
        if not m:
            continue
        key, val = m.group(1), m.group(2)

        if val == "":
            # peek: list or map?
            nxt = None
            for j in range(i, len(lines)):
                if lines[j].strip() and not lines[j].lstrip().startswith("#"):
                    nxt = lines[j]
                    break
            child = [] if (nxt and nxt.strip().startswith("- ")) else {}
            container[key] = child
            stack.append((indent, child))
            continue

        while _unterminated_quote(val) and i < len(lines):
            val = val + " " + _strip_comment(lines[i]).strip()
            i += 1
        container[key] = _scalar(val)
    return root


def dig(data, path, default=None):
    """dig(cfg, 'mc.foreknowledge') -> value or default."""
    cur = data
    for part in path.split("."):
        if not isinstance(cur, dict) or part not in cur:
            return default
        cur = cur[part]
    return cur


# ------------------------------------------------------------------- pipe tables


class Row(object):
    __slots__ = ("cells", "line_no", "raw", "_headers")

    def __init__(self, cells, line_no, raw, headers):
        self.cells = cells
        self.line_no = line_no
        self.raw = raw
        self._headers = headers

    def get(self, name, default=""):
        """Fetch a cell by header name (case-insensitive, ignores ** and spaces)."""
        want = _norm_header(name)
        for idx, h in enumerate(self._headers):
            if _norm_header(h) == want:
                return self.cells[idx] if idx < len(self.cells) else default
        return default

    def first(self):
        return self.cells[0] if self.cells else ""

    def __repr__(self):
        return "Row(%r)" % (self.cells,)


class Table(object):
    def __init__(self, headers, rows, start_line, heading):
        self.headers = headers
        self.rows = rows
        self.start_line = start_line
        self.heading = heading

    def __len__(self):
        return len(self.rows)


def _norm_header(h):
    return re.sub(r"[^a-z0-9]", "", h.lower())


def _cells(line):
    s = line.strip()
    if s.startswith("|"):
        s = s[1:]
    if s.endswith("|"):
        s = s[:-1]
    return [c.strip() for c in s.split("|")]


_SEP = re.compile(r"^\|?[\s:\-|]+\|[\s:\-|]*$")


def parse_tables(text):
    """Every pipe table in the document, tagged with its nearest preceding heading."""
    tables = []
    lines = text.split("\n")
    heading = ""
    i = 0
    while i < len(lines):
        line = lines[i]
        if line.lstrip().startswith("#"):
            heading = line.lstrip("# ").strip()
            i += 1
            continue
        if line.strip().startswith("|") and i + 1 < len(lines) and _SEP.match(lines[i + 1].strip()):
            headers = _cells(line)
            start = i + 1
            i += 2
            rows = []
            while i < len(lines) and lines[i].strip().startswith("|"):
                if not _SEP.match(lines[i].strip()):
                    rows.append(Row(_cells(lines[i]), i + 1, lines[i], headers))
                i += 1
            tables.append(Table(headers, rows, start, heading))
            continue
        i += 1
    return tables


def tables_under(text, heading_substr):
    """Tables whose nearest preceding heading contains heading_substr (case-insensitive)."""
    want = heading_substr.lower()
    return [t for t in parse_tables(text) if want in t.heading.lower()]


def section(text, heading_substr, level=None):
    """Return the body of the first heading containing heading_substr, up to the next
    heading of the same or shallower level. Empty string if not found."""
    want = heading_substr.lower()
    lines = text.split("\n")
    start = None
    start_level = 0
    for idx, line in enumerate(lines):
        m = re.match(r"^(#{1,6})\s+(.*)$", line)
        if not m:
            continue
        lv, title = len(m.group(1)), m.group(2)
        if start is None:
            if want in title.lower() and (level is None or lv == level):
                start, start_level = idx, lv
        elif lv <= start_level:
            return "\n".join(lines[start:idx]).rstrip()
    if start is None:
        return ""
    return "\n".join(lines[start:]).rstrip()
