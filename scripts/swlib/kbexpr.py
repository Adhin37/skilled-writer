"""The trigger language: when a knowledge-base card applies.

Every card in `.claude/skills/*/references/` declares a `when:` in its frontmatter, and this
module decides whether it fires for a given novel and chapter. The conditions it replaces were
prose in two dispatcher tables - "chapter <= `opening.contract_by_ch + 2`", "`scaling.shape` is
not `none`" - typed by hand in both directions and readable only by a model.

The grammar is the smallest one that covers those conditions:

    expr    := "always" | "never" | or
    or      := and ("or" and)*
    and     := atom ("and" atom)*
    atom    := path | path "is" ("set"|"unset") | path op operand
    op      := "==" | "!=" | "<=" | ">=" | "<" | ">" | "in"
    operand := int | word | "[" word ("," word)* "]" | path | path ("+"|"-") int
    path    := ident ("." ident)*

`and` binds tighter than `or`. There are no parentheses: a trigger that needs them is answering
two questions and the card should be split. `or` exists because the genre modules genuinely need
it - `power-system` is on when the *genre or the subgenre* is fantasy, scifi or progression, and
`cmd_readset.active_modules` has always tested both. Nothing is passed to `eval` or `exec`.

A right-hand identifier containing a `.` is a path; one without is a literal. That is unambiguous
for this vocabulary - `none`, `true`, `climb`, `on` never contain a dot - and `sw health` rejects
a `when:` naming a config key that does not exist.

**Two consumers, opposite strictness, and that is the safety story.** A condition that cannot be
evaluated returns UNKNOWN rather than False. `sw readset` and `sw kb cards` treat UNKNOWN as
*include*, because a card wrongly opened costs tokens and a card wrongly skipped costs a defect
in the chapter. `sw health` treats UNKNOWN as a defect, so the maintainer fixes it. The same rule
governs `sw health` (strict, our own corpus) against `sw kb validate --okf` (permissive, OKF
section 11, somebody else's bundle).
"""

import re

# Kleene three-valued logic. These must be combined with k_and/k_or/k_not and never with Python's
# own operators: `UNKNOWN and FALSE` evaluates to None rather than False, which would turn a
# broken trigger into a silently disabled card - the fail-dangerous direction.
TRUE, FALSE, UNKNOWN = True, False, None


def k_and(a, b):
    if a is FALSE or b is FALSE:
        return FALSE
    return UNKNOWN if (a is UNKNOWN or b is UNKNOWN) else TRUE


def k_or(a, b):
    if a is TRUE or b is TRUE:
        return TRUE
    return UNKNOWN if (a is UNKNOWN or b is UNKNOWN) else FALSE


_TOKEN = re.compile(r"""
      (?P<list>\[[^\]]*\])
    | (?P<op><=|>=|==|!=|<|>)
    | (?P<sign>[+-](?=\s*\d))
    | (?P<num>\d+)
    | (?P<word>[A-Za-z_][A-Za-z0-9_.-]*)
    | (?P<ws>\s+)
""", re.X)


class ExprError(ValueError):
    """A `when:` that does not parse. Raised at load time, never swallowed."""


def _tokenise(text):
    out, pos = [], 0
    while pos < len(text):
        m = _TOKEN.match(text, pos)
        if not m:
            raise ExprError("cannot read %r at offset %d" % (text[pos:pos + 12], pos))
        pos = m.end()
        if m.lastgroup != "ws":
            out.append((m.lastgroup, m.group(0)))
    return out


def _split(tokens, keyword):
    groups, cur = [], []
    for kind, tok in tokens:
        if kind == "word" and tok == keyword:
            if not cur:
                raise ExprError("`%s` with nothing before it" % keyword)
            groups.append(cur)
            cur = []
        else:
            cur.append((kind, tok))
    if not cur:
        raise ExprError("`%s` with nothing after it" % keyword)
    groups.append(cur)
    return groups


def parse(text):
    """Parse a `when:` into [[atom, ...], ...] - an OR of ANDs. Raises ExprError."""
    text = (text or "").strip()
    if not text:
        raise ExprError("empty condition - write `always` if it is unconditional")
    tokens = _tokenise(text)
    if [t for _, t in tokens] == ["always"]:
        return [[{"kind": "always", "text": "always"}]]
    if [t for _, t in tokens] == ["never"]:
        return [[{"kind": "never", "text": "never"}]]
    return [[_atom(a, text) for a in _split(clause, "and")]
            for clause in _split(tokens, "or")]


def _atom(toks, whole):
    kinds = [k for k, _ in toks]
    words = [t for _, t in toks]
    if not toks:
        raise ExprError("empty term in %r" % whole)
    if kinds[0] != "word":
        raise ExprError("expected a config path at the start of %r" % " ".join(words))

    if len(toks) == 1:
        return {"kind": "truthy", "path": words[0], "text": words[0]}

    if len(toks) == 3 and words[1] == "is" and words[2] in ("set", "unset"):
        return {"kind": words[2], "path": words[0], "text": " ".join(words)}

    if kinds[1] == "op" or words[1] == "in":
        return {"kind": "compare", "path": words[0], "op": words[1],
                "value": _operand(toks[2:], whole), "text": " ".join(words)}

    raise ExprError("cannot read the term %r in %r" % (" ".join(words), whole))


def _operand(toks, whole):
    if not toks:
        raise ExprError("nothing on the right of the operator in %r" % whole)
    kind, tok = toks[0]

    if kind == "list":
        items = [i.strip().lower() for i in tok[1:-1].split(",") if i.strip()]
        if not items:
            raise ExprError("empty list in %r" % whole)
        return {"kind": "list", "items": items}

    if kind == "num":
        return {"kind": "number", "value": int(tok)}

    if kind == "word":
        # `path + N` / `path - N`, the only arithmetic the grammar has. The sign must be spaced
        # or the tokeniser reads it as part of a kebab-case identifier, which is what makes
        # `optional.no-harem` lex as one word.
        if len(toks) == 3 and toks[1][0] == "sign" and toks[2][0] == "num":
            if "." not in tok:
                raise ExprError("`%s` needs a config path on its left, in %r"
                                % (toks[1][1], whole))
            off = int(toks[2][1])
            return {"kind": "path_offset", "path": tok,
                    "offset": -off if toks[1][1] == "-" else off}
        if len(toks) != 1:
            raise ExprError("unexpected %r after %r in %r" % (toks[1][1], tok, whole))
        if "." in tok:
            return {"kind": "path", "path": tok}
        return {"kind": "literal", "value": tok.lower()}

    raise ExprError("cannot read the value %r in %r" % (tok, whole))


def paths(text):
    """Every config path a condition names. `sw health` checks these against the template."""
    found = set()
    for clause in parse(text):
        for atom in clause:
            if atom["kind"] in ("always", "never"):
                continue
            found.add(atom["path"])
            val = atom.get("value") or {}
            if val.get("kind") in ("path", "path_offset"):
                found.add(val["path"])
    return found


# --------------------------------------------------------------------------- resolution

# Where a config key has a default, the default lives on `novelio.Novel` and this routes to it.
# It is a routing table to the existing owner, not a second copy: getting this wrong is the
# highest-consequence bug in the module. `pov.mode != single` against a novel with no `pov.mode`
# resolves to "none" != "single" -> TRUE, which switches `pov-switch` on for every novel that
# never configured POV. Every entry here exists to stop that class of error.
_PROPS = {
    "scaling.shape":          lambda n: n.scaling_shape,
    "mc.foreknowledge":       lambda n: n.has_foreknowledge,
    "mc.form_locked":         lambda n: n.form_locked,
    "chapters.arc_length":    lambda n: n.arc_length,
    "opening.contract_by_ch": lambda n: n.get("opening.contract_by_ch", 3),
    "pov.mode":               lambda n: n.get("pov.mode", "single"),
    "content.romance":        lambda n: n.get("content.romance", "none"),
}

MISSING = object()


class Context(object):
    """Resolves a path for one novel and one chapter.

    Three namespaces: bare paths are `novel.md` config (through `_PROPS` where a default
    exists), `optional.<name>` goes to `Novel.optional_on`, and the builtins below are computed
    by the caller - `chapter` from the -c argument, `speakers` from the read-set's resolved
    characters, `draft.*` from the drafted chapter at gate time.
    """

    BUILTINS = ("chapter", "speakers", "arc")

    def __init__(self, novel=None, **builtins):
        self.novel = novel
        self.builtins = {k: v for k, v in builtins.items() if v is not None}

    def get(self, path):
        if path in self.builtins:
            return self.builtins[path]
        if path in self.BUILTINS or path.startswith("draft."):
            return MISSING
        if self.novel is None:
            return MISSING
        if path.startswith("optional."):
            return "on" if self.novel.optional_on(path.split(".", 1)[1]) else "off"
        if path in _PROPS:
            return _PROPS[path](self.novel)
        val = self.novel.get(path, MISSING)
        return MISSING if val == "" else val


_OFF = ("none", "", "-", "off", "false", "no", "null")


def _norm(value):
    """Everything compares as a lowercase string, and the on/off families collapse.

    `mdio` coerces `true`/`false` to bool but leaves `on`/`off`/`none` as strings, so a card
    written `optional.no-harem == on` has to match a file that says either `on` or `true`.
    """
    if value is MISSING or value is None:
        return "none"
    if isinstance(value, bool):
        return "on" if value else "off"
    s = str(value).strip().lower()
    if s in ("true", "yes"):
        return "on"
    if s in ("false", "no"):
        return "off"
    return "none" if s in ("", "null", "~") else s


def _as_int(value):
    if isinstance(value, bool) or value is MISSING or value is None:
        return None
    if isinstance(value, int):
        return value
    m = re.search(r"-?\d+", str(value))
    return int(m.group(0)) if m else None


def evaluate(text, ctx):
    """Return (TRUE|FALSE|UNKNOWN, [explanation, ...]). Never raises on a parsed expression.

    The explanations are the point of the second value: the read-set prints why a card was
    skipped, so a trigger that is quietly wrong is visible rather than merely absent.
    """
    try:
        clauses = parse(text)
    except ExprError as exc:
        return UNKNOWN, ["cannot parse %r: %s" % (text, exc)]
    result, why = FALSE, []
    for clause in clauses:
        got = TRUE
        for atom in clause:
            ok, line = _run(atom, ctx)
            why.append(line)
            got = k_and(got, ok)
        result = k_or(result, got)
    return result, why


def _run(atom, ctx):
    kind = atom["kind"]
    if kind == "always":
        return TRUE, "always"
    if kind == "never":
        return FALSE, "never"

    raw = ctx.get(atom["path"])

    if kind in ("set", "unset", "truthy"):
        present = _norm(raw) not in _OFF
        ok = (not present) if kind == "unset" else present
        return (TRUE if ok else FALSE), "%s -> %s" % (atom["text"], "yes" if present else "no")

    op, val = atom["op"], atom["value"]

    if val["kind"] == "list":
        if op not in ("in", "==", "!="):
            return UNKNOWN, "%s -> `%s` does not take a list" % (atom["text"], op)
        hit = _norm(raw) in val["items"]
        ok = (not hit) if op == "!=" else hit
        return (TRUE if ok else FALSE), "%s -> %s %s [%s] = %s" % (
            atom["text"], _norm(raw), op, ", ".join(val["items"]), _yn(ok))

    if val["kind"] == "path":
        right = ctx.get(val["path"])
    elif val["kind"] == "path_offset":
        base = _as_int(ctx.get(val["path"]))
        if base is None:
            return UNKNOWN, "%s -> %s is not a number" % (atom["text"], val["path"])
        right = base + val["offset"]
    else:
        right = val["value"]

    if op in ("==", "!="):
        hit = _norm(raw) == _norm(right)
        ok = (not hit) if op == "!=" else hit
        return (TRUE if ok else FALSE), "%s -> %s %s %s = %s" % (
            atom["text"], _norm(raw), op, _norm(right), _yn(ok))
    if op == "in":
        return UNKNOWN, "%s -> `in` needs a list on the right" % atom["text"]

    # Ordering needs two numbers on purpose. A silent lexicographic compare on a typo'd
    # `opening.contract_by_ch` is worse than saying the trigger could not be evaluated.
    li, ri = _as_int(raw), _as_int(right)
    if li is None or ri is None:
        return UNKNOWN, "%s -> not a number (%s %s %s)" % (
            atom["text"], _norm(raw), op, _norm(right))
    ok = {"<": li < ri, "<=": li <= ri, ">": li > ri, ">=": li >= ri}[op]
    return (TRUE if ok else FALSE), "%s -> %d %s %d = %s" % (atom["text"], li, op, ri, _yn(ok))


def _yn(ok):
    return "true" if ok else "false"
