"""`sw kb` - query the craft knowledge base.

The counterpart to `sw readset`. That command answers "what does this chapter need to know about
the story"; this one answers "what does it need to know about the craft" - which concept belongs
to which skill, what teaches it, and which cards apply to the chapter in hand.

It finds and resolves; it does not judge. `search` has no ranking, because a ranked search is a
judging tool and this toolkit does not have those. Nothing here writes a file: `--json` goes to
stdout, and the index itself is derived on every call rather than stored.
"""

import json
import os
import re

from . import kb, kbexpr, mdio
from .report import Report

ACTIONS = ("owner", "show", "list", "search", "cards", "passes", "validate")


def run(repo_root, args, novel=None):
    action = args.action
    if action == "owner":
        return _owner(repo_root, args)
    if action == "show":
        return _show(repo_root, args)
    if action == "list":
        return _list(repo_root, args)
    if action == "search":
        return _search(repo_root, args)
    if action in ("cards", "passes"):
        return _cards(repo_root, args, novel)
    return _validate(repo_root, args)


def _need(args, what):
    if not args.args:
        print("sw kb %s needs %s" % (args.action, what))
        return None
    return args.args[0]


# ------------------------------------------------------------------- lookups


def _owner(repo_root, args):
    slug = _need(args, "a concept slug")
    if slug is None:
        return 2
    idx = kb.index(repo_root)
    owner = idx.owners.get(slug)
    if not owner:
        near = sorted(s for s in idx.owners if slug in s or s in slug)
        print("no skill owns `%s`%s" % (slug, ("  (did you mean: %s)" % ", ".join(near[:5]))
                                        if near else ""))
        return 1
    print("%s -> %s  (%s)" % (slug, owner,
                              os.path.relpath(idx.skills[owner].path, repo_root)))
    return 0


def _show(repo_root, args):
    slug = _need(args, "a concept slug")
    if slug is None:
        return 2
    idx = kb.index(repo_root)
    if slug not in idx.owners:
        print("no skill owns `%s`" % slug)
        return 1
    print("%s\n%s" % (slug, "=" * len(slug)))
    print("owner: %s" % idx.owners[slug])
    carriers = idx.carrying(slug)
    print("\nwhat teaches it:")
    for c in carriers:
        if isinstance(c, kb.SkillEntry):
            print("  %-14s %s" % ("SKILL.md", os.path.relpath(c.path, repo_root)))
        else:
            print("  %-14s %s%s" % (c.type, c.rel,
                                    ("  - %s" % c.description) if c.description else ""))
    cites = sorted(s.name for s in idx.skills.values()
                   if s.name != idx.owners[slug] and _mentions(s, slug))
    if cites:
        print("\ncited by: %s" % ", ".join(cites))
    return 0


def _mentions(skill, slug):
    from . import mdio
    return slug in mdio.read_text(skill.path)


def _list(repo_root, args):
    idx = kb.index(repo_root)
    want = getattr(args, "type", None)
    if args.json:
        data = {
            "skills": [{"name": s.name, "owns": s.owns, "tier": s.tier, "when": s.when,
                        "path": os.path.relpath(s.path, repo_root)}
                       for s in sorted(idx.skills.values(), key=lambda x: x.name)],
            "files": [{"path": f.rel, "type": f.type, "owner": f.owner,
                       "dispatcher": f.dispatcher, "phase": f.phase, "pass": f.pass_,
                       "order": f.order, "when": f.when, "concepts": f.concepts,
                       "description": f.description}
                      for f in idx.files if not want or f.type == want],
            "owners": idx.owners,
        }
        print(json.dumps(data, indent=2, sort_keys=True, default=str))
        return 0

    if not want or want == "skill":
        print("-- skills (%d)" % len(idx.skills))
        for s in sorted(idx.skills.values(), key=lambda x: x.name):
            print("   %-24s %-9s %s" % (s.name, s.tier or "-", ", ".join(s.owns)))
    for kind in kb.TYPES[1:]:
        if want and want != kind:
            continue
        rows = idx.by_type(kind)
        if not rows:
            continue
        print("\n-- %s (%d)" % (kind, len(rows)))
        for f in sorted(rows, key=lambda x: x.rel):
            print("   %-24s %-9s %s" % (f.owner, f.phase or f.pass_ or "-",
                                        f.when or f.description or ""))
    print("\n%d skills, %d files, %d concepts" % (len(idx.skills), len(idx.files),
                                                  len(idx.owners)))
    return 0


def _search(repo_root, args):
    if not args.args:
        print("sw kb search needs a term")
        return 2
    hits = kb.search(repo_root, args.args)
    for h in hits:
        print("%s\n    %s%s\n    %s" % (h["path"],
                                        ("§%s  " % h["heading"]) if h["heading"] else "",
                                        "[%s, %s]" % (h["type"], h["owner"]),
                                        h["line"][:110]))
    print("\n%d hit(s)" % len(hits))
    return 0 if hits else 1


# ------------------------------------------------------------- card resolution


def _cards(repo_root, args, novel):
    """The resolved card set for one chapter. This is what replaces the dispatcher tables."""
    idx = kb.index(repo_root)
    kind = "draft-card" if args.action == "cards" else "audit-card"
    number = args.chapter
    ctx = kbexpr.Context(novel, chapter=number, speakers=_speakers(novel, number))
    fired, skipped = idx.cards(kind, ctx, phase=getattr(args, "phase", None))

    total = len(idx.by_type(kind))
    label = "phase %s" % args.phase if getattr(args, "phase", None) else kind
    print("# CARDS - %s, chapter %s. Open these in order, and no others." % (label, number))
    if not fired and not skipped:
        print("  (no %s declares a trigger yet)" % kind)
        return 0
    for f, state, why in fired:
        mark = " ?" if state is kbexpr.UNKNOWN else ""
        cond = ("  [%s]" % f.when) if f.when and f.when != "always" else ""
        print("  %-22s %s%s%s" % (f.owner, f.rel, cond, mark))
        if f.description:
            print("  %-22s %s" % ("", f.description))
        if state is kbexpr.UNKNOWN:
            print("  %-22s ? could not resolve: %s" % ("", "; ".join(why)))
    if skipped:
        print("\n# NOT OPENED (condition false for this novel and chapter)")
        for f, why in skipped:
            print("  %-22s %s" % (f.owner, "; ".join(why)))
    print("\n%d of %d applied." % (len(fired), total))
    return 0


def _speakers(novel, number):
    """Speaker count for `speakers >= N`, from the same resolver the read-set uses."""
    if novel is None:
        return None
    try:
        from . import cmd_readset
        names, _why = cmd_readset.resolve_characters(novel, number)
        return len(names)
    except Exception:
        return None


# ---------------------------------------------------------------- validation


RESERVED = ("index.md", "log.md")


def _validate_bundle(path, args):
    """OKF section 11 conformance, applied to a bundle this repo did not necessarily write.

    Permissive on purpose, and the permissiveness is the spec's, not a shrug: section 11 says a
    consumer MUST NOT reject a bundle for a missing optional field, an unknown `type`, an unknown
    extra key, a broken cross-link or a missing `index.md`. Only two things are hard requirements
    - parseable frontmatter, and a non-empty `type` - so only those are defects here.

    `sw health` is the other half and does not work this way. It audits *this repo's own* corpus,
    where the whole value is a contract a low-effort model cannot wriggle out of, and it defects
    freely. Strict at authoring, permissive at consumption; the two are not in tension.
    """
    rep = Report("kb validate --okf - %s" % os.path.basename(os.path.abspath(path)))
    if not os.path.isdir(path):
        rep.defect("okf", "%s is not a directory" % path)
        print(rep.render(show=getattr(args, "show", "warn")))
        return 1

    docs, targets = [], set()
    for sub, _dirs, files in os.walk(path):
        for fname in sorted(files):
            if not fname.endswith(".md"):
                continue
            full = os.path.join(sub, fname)
            rel = os.path.relpath(full, path).replace(os.sep, "/")
            targets.add("/" + rel)
            if fname in RESERVED:
                continue
            text = mdio.read_text(full)
            fm, body = mdio.split_frontmatter(text)
            if not fm:
                rep.defect("okf", "%s has no YAML frontmatter - section 11 requires it" % rel,
                           path=full)
                continue
            cfg = mdio.parse_yaml(fm)
            if not str(cfg.get("type") or "").strip():
                rep.defect("okf", "%s has no non-empty `type` - the one universally required "
                                  "field" % rel, path=full)
            docs.append((rel, full, cfg, body))

    root_index = os.path.join(path, "index.md")
    if not os.path.isfile(root_index):
        rep.note("okf", "no bundle-root index.md - optional, and a consumer may synthesize one")
    else:
        fm = mdio.parse_yaml(mdio.split_frontmatter(mdio.read_text(root_index))[0])
        if not fm.get("okf_version"):
            rep.note("okf", "index.md declares no `okf_version` - optional")

    broken = 0
    for rel, full, _cfg, body in docs:
        for target in re.findall(r"\]\((/[^)\s]+\.md)\)", body):
            if target not in targets:
                broken += 1
                rep.warn("okf-link", "%s links to %s, which is not in the bundle - section 11 "
                                     "says a consumer tolerates this" % (rel, target), path=full)
    kinds = {}
    for _rel, _full, cfg, _body in docs:
        k = str(cfg.get("type") or "?")
        kinds[k] = kinds.get(k, 0) + 1
    rep.info("bundle", ["   %d concept document(s), %d reserved"
                        % (len(docs), len(targets) - len(docs))]
             + ["   %-20s %d" % (k, v) for k, v in sorted(kinds.items())])
    print(rep.render(show=getattr(args, "show", "warn")))
    return 1 if any(f.level == "defect" for f in rep.findings) else 0


def _validate(repo_root, args):
    if args.args:
        return _validate_bundle(args.args[0], args)
    rep = Report("kb validate")
    idx = kb.index(repo_root)
    for problem in idx.problems:
        rep.defect("kb-scope", problem)
    validate(idx, rep)
    rep.info("scope", ["   %d skills, %d files, %d concepts"
                       % (len(idx.skills), len(idx.files), len(idx.owners)),
             "   Structure only. It says nothing about whether the advice is any good."])
    print(rep.render(show=getattr(args, "show", "warn")))
    return 1 if rep.findings and any(f.level == "defect" for f in rep.findings) else 0


def validate(idx, rep):
    """The structural checks, shared with `sw health`.

    Kept permissive about `type` on purpose: OKF section 11 says a consumer must not reject a
    document for an unknown type, and that is right here too - a new kind of reference should
    not break the build. Everything that would make a card unreachable is a defect.
    """
    known_skills = set(idx.skills)
    for f in idx.files:
        if f.type not in kb.TYPES:
            rep.warn("kb-type", "%s declares type `%s`, which is not one of %s"
                     % (f.rel, f.type, ", ".join(kb.TYPES)), path=f.path)
        if f.owner not in known_skills:
            rep.defect("kb-owner", "%s names owner `%s`, which is not a skill"
                       % (f.rel, f.owner), path=f.path)
        if f.dispatcher and f.dispatcher not in known_skills:
            rep.defect("kb-dispatch", "%s names dispatcher `%s`, which is not a skill"
                       % (f.rel, f.dispatcher), path=f.path)
        for slug in f.concepts:
            owner = idx.owners.get(slug)
            if owner is None:
                rep.defect("kb-concept", "%s carries concept `%s`, which no skill owns"
                           % (f.rel, slug), path=f.path)
            elif owner != f.owner:
                rep.defect("kb-concept", "%s carries `%s`, which %s owns - a file teaches only "
                                         "its own skill's concepts" % (f.rel, slug, owner),
                           path=f.path)
        if f.when:
            _check_expr(f.when, f.rel, f.path, rep)
    for s in idx.skills.values():
        if s.when:
            _check_expr(s.when, "%s/SKILL.md" % s.name, s.path, rep)


def _check_expr(expr, rel, path, rep):
    try:
        kbexpr.parse(expr)
    except kbexpr.ExprError as exc:
        rep.defect("kb-trigger", "%s has an unreadable `when:` - %s" % (rel, exc), path=path)
