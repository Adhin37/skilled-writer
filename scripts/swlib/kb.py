"""The knowledge-base index: what the craft corpus contains, and which of it applies today.

`novels/<slug>/` has had a query layer since `sw readset` - it hands a chapter its slices rather
than its files. The craft corpus never had one. Forty-two skills and seventy-five references were
reachable only through pointers typed by hand into two dispatcher tables, and `sw trace` measured
what that costs: `write-chapter` opened 38 times against `story-craft`, whose card the contract
calls "first, always", opened twice.

This module reads the frontmatter of every knowledge file and answers three questions:

    who owns this concept          -> Index.owners
    what teaches it                -> Index.carrying
    which cards apply right now    -> Index.cards / Index.active

**Derived at call time, never committed.** 117 files, frontmatter only, tens of milliseconds -
and a committed index would be a second copy of the corpus, which is the defect class this repo
exists to remove. Bodies are read only by `search`.

The index reads both the pre- and post-migration frontmatter shapes, so it can be built, tested
and diffed before a single file is rewritten. `owns:` is taken from `metadata.owns` where it
exists and from the top-level key otherwise.
"""

import os
import re

from . import kbexpr, mdio

SKILLS_REL = os.path.join(".claude", "skills")

# The reserved card filenames, and the dispatcher each one answers to. A card is opened by its
# dispatcher rather than cited by its own skill, which is why it is the one inversion in the
# corpus and why `type` can be inferred from the name before any migration has happened.
CARD_KINDS = {"draft-card.md": ("draft-card", "write-chapter"),
              "audit-card.md": ("audit-card", "revision-pass")}

TYPES = ("skill", "draft-card", "audit-card", "reference")

_CACHE = {}


def skills_dir(repo_root):
    return os.path.join(repo_root, SKILLS_REL)


# How hard a skill's rules bind. The corpus was written with no way to say this, so the
# essentialism ban and a note about em-dash density read identically - and a model obeys both at
# the same anxiety level, which is paid for entirely by the stylistic rules. See
# `docs/creative-latitude.md`.
FORCE = ("absolute", "structural", "stylistic")


class SkillEntry(object):
    __slots__ = ("name", "path", "description", "owns", "tier", "force", "when", "meta")

    def __init__(self, name, path, description, owns, tier, when, meta, force=None):
        self.name, self.path, self.description = name, path, description
        self.owns, self.tier, self.when, self.meta = owns, tier, when, meta
        self.force = force

    def __repr__(self):
        return "<skill %s owns=%d>" % (self.name, len(self.owns))


class FileEntry(object):
    __slots__ = ("path", "rel", "type", "owner", "dispatcher", "phase", "pass_",
                 "order", "description", "when", "concepts")

    def __init__(self, **kw):
        for slot in self.__slots__:
            setattr(self, slot, kw.get(slot))

    def __repr__(self):
        return "<%s %s>" % (self.type, self.rel)


def _as_list(value):
    """Accept a YAML list or a comma-separated string.

    `metadata:` is documented as a free-form map and lists parse today, but if a packaging path
    ever requires string values the fix belongs here rather than in every reader.
    """
    if value is None or value == "":
        return []
    if isinstance(value, (list, tuple)):
        return [str(v).strip() for v in value if str(v).strip()]
    return [v.strip() for v in str(value).strip("[]").split(",") if v.strip()]


class Index(object):
    """Everything the frontmatter of the craft corpus says, in one object."""

    def __init__(self, repo_root):
        self.repo_root = repo_root
        self.skills = {}
        self.files = []
        self.owners = {}
        self.problems = []
        self._build()

    # ------------------------------------------------------------------ build

    def _build(self):
        root = skills_dir(self.repo_root)
        if not os.path.isdir(root):
            return
        for name in sorted(os.listdir(root)):
            path = os.path.join(root, name, "SKILL.md")
            if not os.path.isfile(path):
                continue
            self._add_skill(name, path)
            refdir = os.path.join(root, name, "references")
            if os.path.isdir(refdir):
                for fname in sorted(os.listdir(refdir)):
                    if fname.endswith(".md"):
                        self._add_reference(name, refdir, fname)

    def _add_skill(self, name, path):
        cfg = mdio.parse_yaml(mdio.split_frontmatter(mdio.read_text(path))[0])
        meta = cfg.get("metadata") or {}
        if not isinstance(meta, dict):
            meta = {}
        # Post-migration the scope declaration lives under `metadata:`, which is the only place
        # the Agent Skills spec sanctions for custom keys. Pre-migration it is top level.
        owns = _as_list(meta.get("owns", cfg.get("owns")))
        entry = SkillEntry(name=name, path=path,
                           description=str(cfg.get("description") or "").strip(),
                           owns=owns,
                           tier=str(meta.get("tier") or "").strip() or None,
                           when=str(meta.get("when") or "").strip() or None,
                           force=str(meta.get("force") or "").strip() or None,
                           meta=meta)
        self.skills[name] = entry
        for slug in owns:
            if slug in self.owners and self.owners[slug] != name:
                self.problems.append("`%s` is claimed by both %s and %s"
                                     % (slug, self.owners[slug], name))
            self.owners[slug] = name

    def _add_reference(self, skill, refdir, fname):
        path = os.path.join(refdir, fname)
        cfg = mdio.parse_yaml(mdio.split_frontmatter(mdio.read_text(path))[0])
        kind, dispatcher = CARD_KINDS.get(fname, ("reference", None))
        self.files.append(FileEntry(
            path=path,
            rel=os.path.join(SKILLS_REL, skill, "references", fname).replace(os.sep, "/"),
            type=str(cfg.get("type") or kind).strip(),
            owner=str(cfg.get("owner") or skill).strip(),
            dispatcher=str(cfg.get("dispatcher") or dispatcher or "").strip() or None,
            phase=str(cfg.get("phase") or "").strip() or None,
            pass_=str(cfg.get("pass") or "").strip() or None,
            order=cfg.get("order"),
            description=str(cfg.get("description") or "").strip(),
            when=str(cfg.get("when") or "").strip() or None,
            concepts=_as_list(cfg.get("concepts"))))

    # ----------------------------------------------------------------- lookup

    def by_type(self, kind):
        return [f for f in self.files if f.type == kind]

    def carrying(self, slug):
        """Every file whose `concepts:` names a slug, owner's SKILL.md first."""
        owner = self.owners.get(slug)
        out = []
        if owner and owner in self.skills:
            out.append(self.skills[owner])
        out.extend(f for f in self.files if slug in f.concepts)
        return out

    def entry(self, skill):
        """The cheapest correct entry point: the draft card if there is one, else the body.

        Finds a path; judges nothing. Moved here from `cmd_readset._module_entry` so the
        read-set and the card resolver cannot disagree about where a module starts.
        """
        card = os.path.join(SKILLS_REL, skill, "references", "draft-card.md")
        if os.path.isfile(os.path.join(self.repo_root, card)):
            return card.replace(os.sep, "/")
        return os.path.join(SKILLS_REL, skill, "SKILL.md").replace(os.sep, "/")

    # ------------------------------------------------------------ resolution

    # `optional:` switches first, then the genre modules, then anything gated by config - the
    # order the read-set has always printed them in, kept because it groups by why a module is on.
    TIER_ORDER = ("optional", "genre", "gated")

    def active(self, novel, ctx=None, tiers=None):
        """The skills switched on for this novel, as (name, entry, state) triples.

        A skill with no declared `when:` is unconditional and always in play, so it is not a
        *module* and never appears here. UNKNOWN counts as on: a module wrongly listed costs a
        line, and one wrongly hidden costs a chapter.
        """
        ctx = ctx or kbexpr.Context(novel)
        want = tuple(tiers) if tiers else self.TIER_ORDER
        out = []
        for name in sorted(self.skills, key=lambda n: (_tier_rank(self.skills[n].tier), n)):
            skill = self.skills[name]
            if not skill.when or skill.when == "always":
                continue
            if skill.tier not in want:
                continue
            state, _why = kbexpr.evaluate(skill.when, ctx)
            if state is not kbexpr.FALSE:
                out.append((name, self.entry(name), state))
        return out

    def off_for(self, novel, ctx=None):
        """The modules this novel switches off. The converse of `active`, for `sw trace`.

        A module correctly switched off is not a skill the run failed to open, and reporting it
        as one teaches you to stop reading the findings.
        """
        ctx = ctx or kbexpr.Context(novel)
        off = []
        for name, skill in sorted(self.skills.items()):
            if not skill.when or skill.when == "always":
                continue
            if kbexpr.evaluate(skill.when, ctx)[0] is kbexpr.FALSE:
                off.append(name)
        return off

    def cards(self, kind, ctx, phase=None):
        """Resolve a card set. Returns ([(FileEntry, state, why)], [(FileEntry, why)]).

        The second list is the cards that did not fire, with the reason - the read-set prints it
        so a trigger that is quietly wrong is visible rather than merely absent.
        """
        fired, skipped = [], []
        for f in sorted(self.by_type(kind), key=_card_sort):
            if phase and f.phase and f.phase != phase:
                continue
            if not f.when:
                fired.append((f, kbexpr.TRUE, ["no condition declared"]))
                continue
            state, why = kbexpr.evaluate(f.when, ctx)
            if state is kbexpr.FALSE:
                skipped.append((f, why))
            else:
                fired.append((f, state, why))
        return fired, skipped


def _tier_rank(tier):
    return Index.TIER_ORDER.index(tier) if tier in Index.TIER_ORDER else len(Index.TIER_ORDER)


def _card_sort(f):
    """`order:` where declared, then owner name. Carries 'first, always' without a second list."""
    order = f.order if isinstance(f.order, int) else 999
    return (order, f.owner or "")


def index(repo_root, refresh=False):
    """Memoised per repo root. The corpus does not change inside one process run."""
    if refresh:
        _CACHE.pop(repo_root, None)
    if repo_root not in _CACHE:
        _CACHE[repo_root] = Index(repo_root)
    return _CACHE[repo_root]


# ------------------------------------------------------------------- search


def search(repo_root, terms):
    """Find, do not judge: substring hits with their heading, ordered by path.

    No ranking. A ranked search is a judging tool and this toolkit does not have those - the
    caller reads the hits and decides, which is the same contract every other command keeps.
    """
    idx = index(repo_root)
    needles = [t.lower() for t in terms if t.strip()]
    if not needles:
        return []
    hits = []
    paths = [(s.path, s.name, "skill") for s in idx.skills.values()]
    paths += [(f.path, f.owner, f.type) for f in idx.files]
    for path, owner, kind in sorted(paths):
        body = mdio.split_frontmatter(mdio.read_text(path))[1]
        heading = ""
        for line in body.split("\n"):
            m = re.match(r"^(#{1,6})\s+(.*)$", line)
            if m:
                heading = m.group(2).strip()
                continue
            low = line.lower()
            if all(n in low for n in needles):
                hits.append({"path": os.path.relpath(path, repo_root).replace(os.sep, "/"),
                             "owner": owner, "type": kind,
                             "heading": heading, "line": line.strip()})
    return hits
