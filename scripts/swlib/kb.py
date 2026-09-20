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

from . import kbexpr, mdio, rules

SKILLS_REL = os.path.join(".claude", "skills")

# The role trees live at the repo root: the point of a physical split is that the roles are
# visible at `ls` and `.claude/` goes back to meaning harness config. `.claude/skills/`
# stays the design tree and Claude Code's discovery root - the bare names in an agent's
# `skills:` frontmatter resolve through it, so the 44 bodies cannot move.
ROLES_REL = "roles"

# Every layout the role trees have ever had, longest first so the alternation below can never
# match a suffix of a longer one. `CITATION` and the transcript scanners are built from this
# rather than spelling a path of their own, because that is precisely how they drifted before:
# the constant and the regex were two independent copies of one string, and `Index.resolve()`
# answers None *silently* when they disagree - so a desync surfaces as a clean run, not an error.
#
# The old form stays recognised deliberately and permanently. A citation written before a move
# still names a real file on the day of the move, which is what lets the migration find the text
# it has to rewrite. Resolving is not the same as being correct, and the check that insists the
# text actually be rewritten is `test_corpus.py::test_every_referenced_file_exists`, which asks
# the filesystem rather than the index.
ROLES_DIRS = (".claude/roles", "roles")
_ROLES_ALT = "(?:%s)" % "|".join(re.escape(d) for d in ROLES_DIRS)

# Made to agree here rather than by convention, because the failure is silent either way.
assert ROLES_REL.replace(os.sep, "/") in ROLES_DIRS, \
    "ROLES_REL=%r is not one of the layouts CITATION can match" % (ROLES_REL,)

# `shared` states the property rather than the membership: opened by more than one role. Design
# reads every bucket, because a body still cites its own notes wherever they now sit - so
# `design` is where a note lands that NO card and NO dispatcher body reaches, not where the
# architect's reading stops.
#
# The closure that sorts a note into one of these must seed from the dispatcher bodies as well as
# from the cards. `draft` and `gate` each open exactly one body - their dispatcher, preloaded by
# the harness and named in the Read guard - so what those bodies cite is reachable by that role.
# A card-only closure files `revision-pass.owned-passes.md` as design, and that file carries six
# of the gate's passes.
BUCKETS = ("draft", "gate", "shared", "design")

# The one body each writing role opens. Not an exemption: these are preloaded through `skills:`,
# and naming them here is what keeps the bucket closure agreeing with what the role can reach.
DISPATCHER_BODIES = {"draft": ("write-chapter", "continuity-summary"),
                     "gate": ("revision-pass",)}

# The reserved card filenames, and the dispatcher each one answers to. A card is opened by its
# dispatcher rather than cited by its own skill, which is why it is the one inversion in the
# corpus and why `type` can be inferred from the name before any migration has happened.
CARD_KINDS = {"draft-card.md": ("draft-card", "write-chapter"),
              "audit-card.md": ("audit-card", "revision-pass")}

TYPES = ("skill", "draft-card", "audit-card", "reference")

# Every shape in which one corpus file names another. One regex, because there were three copies
# of it - here, in `cmd_health._references`, and in `test_corpus` - and three copies of a pattern
# is three chances to teach the corpus a citation form that only two of them accept.
#
#   references/x.md                     this skill's own
#   other-skill/references/x.md         another skill's
#   .claude/skills/other/references/x.md  the same, written out
#   roles/<bucket>/owner.x.md          the post-move form, resolved by path
#   x.md                                bare, meaning "mine" - four of these exist
#
# Deliberately NOT a general `*.md` matcher: `CLAUDE.md`, `state/threads.md` and `novel.md` are
# named all over the corpus and none of them is a citation of a knowledge file. The bare form is
# the reason `resolve()` may return None WITHOUT that being a dangling pointer - a bare `.md`
# is a citation only if the owner actually has a file by that name, and `novel.md` never will.
# `prose-quality`'s audit card is the one card that cites this way, and a closure that could not
# see it filed `ai-default-tells.md` as unreachable by the gate that opens it.
CITATION = re.compile(
    r"(?:\.claude/skills/)?(?:(?P<skill>[a-z][a-z0-9]*(?:-[a-z0-9]+)*)/)?"
    r"references/(?P<ref>[A-Za-z0-9._-]+\.md)"
    r"|(?<![\w/-])(?P<rel>" + _ROLES_ALT + r"/[a-z]+/(?P<rolefile>[A-Za-z0-9._-]+\.md))"
    r"|(?<![/\w-])(?P<bare>[a-z][a-z0-9-]*\.md)\b")

_CACHE = {}


def skills_dir(repo_root):
    return os.path.join(repo_root, SKILLS_REL)


def roles_dir(repo_root):
    return os.path.join(repo_root, ROLES_REL)


# How hard a skill's rules bind. The corpus was written with no way to say this, so the
# essentialism ban and a note about em-dash density read identically - and a model obeys both at
# the same anxiety level, which is paid for entirely by the stylistic rules. See
# `docs/creative-latitude.md`.
FORCE = ("absolute", "structural", "stylistic")

# Which agent may open a skill. A role is a *view* over the corpus, never a location in it: 23 of
# the 32 card-carrying skills serve both the draft and the gate, so splitting the corpus into
# per-role folders would have to duplicate them - the defect class `metadata.owns:` exists to
# remove. The axis routes; it moves nothing.
ROLES = ("design", "draft", "gate", "review", "coordinate")

# `review` carries no corpus, deliberately. A cold read is only worth having from someone who has
# not read the rubric, so the role is defined by what it is denied rather than what it is given -
# and that is the one isolation Claude Code can actually enforce, because a reader needs no
# `Skill` tool at all. See roles/review/reader-review.md.
ROLES_WITHOUT_CORPUS = ("review",)

# A card's kind already names the role that opens it; `dispatcher:` was the proto-role axis.
CARD_ROLES = {"draft-card": "draft", "audit-card": "gate"}
_CARD_KIND_BY_ROLE = dict((role, kind) for kind, role in CARD_ROLES.items())


class SkillEntry(object):
    __slots__ = ("name", "path", "description", "owns", "tier", "force", "when", "meta", "role")

    def __init__(self, name, path, description, owns, tier, when, meta, force=None, role=None):
        self.name, self.path, self.description = name, path, description
        self.owns, self.tier, self.when, self.meta = owns, tier, when, meta
        self.force = force
        self.role = role or []

    def __repr__(self):
        return "<skill %s owns=%d>" % (self.name, len(self.owns))


class FileEntry(object):
    __slots__ = ("path", "rel", "type", "owner", "dispatcher", "phase", "pass_",
                 "order", "description", "when", "concepts", "bucket", "cite", "provenance")

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
        self.shortfalls = []
        self._by_rel = {}
        self._by_owner_file = {}
        self._build()
        self._floor()

    # ------------------------------------------------------------------ build

    def _build(self):
        root = skills_dir(self.repo_root)
        if os.path.isdir(root):
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
        self._build_roles()

    def _build_roles(self):
        """The role trees, where every file is named `<owner>.<stem>.md`.

        The prefix is a checksum, never a second source: `owner:` in frontmatter stays
        authoritative, and a disagreement between the two is a `problems` entry rather than a
        silent preference for one of them. The prefix earns its place anyway - `failure-modes.md`
        exists under three different skills, two of which land in the same bucket.

        The stem after the first dot is what the rest of the corpus cites the file by, so
        `references/mirror-clause.md` and `roles/shared/voice-separation.mirror-clause.md`
        resolve to one entry. Owner names contain no dots, which is what makes the split safe.
        """
        root = roles_dir(self.repo_root)
        if not os.path.isdir(root):
            return
        for bucket in BUCKETS:
            bdir = os.path.join(root, bucket)
            if not os.path.isdir(bdir):
                continue
            for fname in sorted(os.listdir(bdir)):
                if not fname.endswith(".md"):
                    continue
                prefix, _, stem = fname.partition(".")
                if not stem:
                    self.problems.append("%s/%s is not `<owner>.<stem>.md`" % (bucket, fname))
                    continue
                self._add_reference(prefix, bdir, fname, bucket=bucket, cite=stem)

    def _floor(self):
        """The check that fires when the corpus is SMALLER than it has ever been.

        `_build` above skips any directory without a `SKILL.md`, so a half-finished move returns
        an empty index - and every other number in this toolkit is a ceiling, which an empty
        corpus satisfies perfectly. `sw health` reports clean, `sw load` prints a row of zeros,
        both card budgets pass. A *clean run* is what a broken index looks like today.

        Kept out of `problems` on purpose: `problems` is per-file (a slug claimed twice, an
        owner that is not a skill) and every consumer renders it the same way. A shortfall is a
        statement about the corpus as a whole, and it is reported once, first, by whoever asked.
        See `rules.CORPUS_FLOOR` for why the numbers sit well under today's figures.
        """
        if not rules.corpus_floor_applies(self.repo_root):
            return
        have = {"skill": len(self.skills)}
        for kind in ("draft-card", "audit-card", "reference"):
            have[kind] = len(self.by_type(kind))
        for kind, floor in sorted(rules.CORPUS_FLOOR.items()):
            if have.get(kind, 0) < floor:
                self.shortfalls.append(
                    "%d %s file(s) reachable, against a floor of %d - the corpus is smaller "
                    "than it has ever been, which is what a half-finished move looks like "
                    "from the inside" % (have.get(kind, 0), kind, floor))

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
                           role=_as_list(meta.get("role")),
                           meta=meta)
        self.skills[name] = entry
        for slug in owns:
            if slug in self.owners and self.owners[slug] != name:
                self.problems.append("`%s` is claimed by both %s and %s"
                                     % (slug, self.owners[slug], name))
            self.owners[slug] = name

    def _add_reference(self, skill, refdir, fname, bucket=None, cite=None):
        path = os.path.join(refdir, fname)
        cfg = mdio.parse_yaml(mdio.split_frontmatter(mdio.read_text(path))[0])
        cite = cite or fname
        kind, dispatcher = CARD_KINDS.get(cite, ("reference", None))
        if bucket is None:
            rel = os.path.join(SKILLS_REL, skill, "references", fname)
        else:
            rel = os.path.join(ROLES_REL, bucket, fname)
        self.files.append(FileEntry(
            path=path,
            rel=rel.replace(os.sep, "/"),
            bucket=bucket,
            cite=cite,
            type=str(cfg.get("type") or kind).strip(),
            owner=str(cfg.get("owner") or skill).strip(),
            dispatcher=str(cfg.get("dispatcher") or dispatcher or "").strip() or None,
            phase=str(cfg.get("phase") or "").strip() or None,
            pass_=str(cfg.get("pass") or "").strip() or None,
            order=cfg.get("order"),
            description=str(cfg.get("description") or "").strip(),
            when=str(cfg.get("when") or "").strip() or None,
            provenance=str(cfg.get("provenance") or "").strip() or None,
            concepts=_as_list(cfg.get("concepts"))))
        entry = self.files[-1]
        self._by_rel[entry.rel] = entry
        self._by_owner_file[(entry.owner, entry.cite)] = entry
        if bucket is not None and entry.owner != skill:
            self.problems.append(
                "%s is filed under the prefix `%s` but declares `owner: %s`"
                % (entry.rel, skill, entry.owner))

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

    def owned_files(self, skill):
        """Every path this skill owns - its body first, then its files, wherever they sit.

        The one answer to "what is a skill's corpus?". It used to be `os.walk` of the skill's
        directory, in four places, which silently means "whatever happens to be filed here" -
        so a note misfiled under the wrong directory was attributed to the directory rather
        than to the owner it declares, and moving a file out of the tree would have stopped
        the duplication checks comparing it without any of them noticing.

        Sorted by `cite` - the stem the rest of the corpus names the file by - rather than by
        basename. The two agree before the move and after it, but only `cite` agrees *during*
        it: a half-moved skill has `channels.md` beside `narrator-voice.audit-card.md`, and
        sorting those by basename silently reorders the concatenation. That matters because a
        10-word run can span the join between two files, so a reorder perturbs the duplication
        check for reasons that have nothing to do with the text.
        """
        out = []
        s = self.skills.get(skill)
        if s is not None:
            out.append(s.path)
        out.extend(f.path for f in
                   sorted((f for f in self.files if f.owner == skill),
                          key=lambda f: f.cite or os.path.basename(f.path)))
        return out

    def reachable(self, role):
        """Every corpus file a writing role can arrive at, as a set of `rel` paths.

        The transitive closure of citation, seeded from what the harness hands that role without
        it asking: its cards, resolved by the dispatcher at run time, and the **one body** it
        opens - named in `DISPATCHER_BODIES`, preloaded through `skills:`, and granted by path in
        the Read guard. Finds files; judges nothing. `cmd_health._partition()` is what turns a
        disagreement between this and the on-disk bucket into a defect.

        Seeding from cards alone is the mistake that has now been made twice, and it fails
        quietly both times: `revision-pass.owned-passes.md` is cited thirteen times and every one
        of them is from `revision-pass/SKILL.md`, so a card-only closure sees no citation at all
        and files six of the gate's own passes as unreachable. Nothing errors - the gate simply
        stops opening them.
        """
        seeds = [f for f in self.files if f.type == _CARD_KIND_BY_ROLE.get(role)]
        work = [(f.path, f.owner, f.rel) for f in seeds]
        work += [(self.skills[n].path, n, "SKILL:%s" % n)
                 for n in DISPATCHER_BODIES.get(role, ()) if n in self.skills]
        seen = set()
        while work:
            path, owner, rel = work.pop()
            if rel in seen:
                continue
            seen.add(rel)
            for m in CITATION.finditer(mdio.read_text(path)):
                target = self.resolve(m, owner)
                if target is not None and target.rel not in seen:
                    work.append((target.path, target.owner, target.rel))
        return seen

    def bucket_for(self, rel, reach):
        """Where a file belongs, given `{role: reachable(role)}`. The partition's whole rule.

        `shared` states a property rather than a membership - opened by more than one role - and
        `design` is the residue: a note no card and no dispatcher body reaches. Design reads
        every bucket, so this is never a claim about where the architect stops looking.
        """
        roles = sorted(r for r in CARD_ROLES.values() if rel in reach.get(r, ()))
        if len(roles) > 1:
            return "shared"
        return roles[0] if roles else "design"

    def resolve(self, match, citing=None):
        """The file a `CITATION` match names, or None. Finds a file; judges nothing.

        `citing` is the skill whose text the citation was found in - it supplies the owner for
        the bare `references/x.md` form, which means "my own".
        """
        if match.group("rolefile"):
            return self._by_rel.get(match.group("rel"))
        if match.group("bare"):
            return self._by_owner_file.get((citing, match.group("bare")))
        owner = match.group("skill") or citing
        return self._by_owner_file.get((owner, match.group("ref")))

    def entry(self, skill):
        """The cheapest correct entry point: the draft card if there is one, else the body.

        Finds a path; judges nothing. Moved here from `cmd_readset._module_entry` so the
        read-set and the card resolver cannot disagree about where a module starts.
        """
        for f in self.files:
            if f.owner == skill and f.type == "draft-card":
                return f.rel
        s = self.skills.get(skill)
        if s is not None:
            return os.path.relpath(s.path, self.repo_root).replace(os.sep, "/")
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

    def view(self, role, ctx=None, phase=None):
        """One role's slice of the corpus: ([SkillEntry], [(FileEntry, state, why)]).

        What an agent for this role may open, and nothing else. When `ctx` is given the card set
        is resolved against that novel, so the answer is this run's, not the corpus's.

        A role with no corpus returns two empty lists, and that is an answer rather than a miss -
        see `ROLES_WITHOUT_CORPUS`.
        """
        skills = [s for _, s in sorted(self.skills.items()) if role in s.role]
        kind = None
        for card_kind, card_role in CARD_ROLES.items():
            if card_role == role:
                kind = card_kind
        if kind is None or ctx is None:
            return skills, []
        fired, _skipped = self.cards(kind, ctx, phase=phase)
        return skills, fired

    def roleless(self):
        """Skills declaring no role. A skill no agent may open is a skill nothing reaches."""
        return sorted(n for n, s in self.skills.items() if not s.role)

    def bad_roles(self):
        """(skill, role) pairs naming a role that does not exist. Catches a typo, which would
        otherwise present as a skill quietly vanishing from a view."""
        return sorted((n, r) for n, s in self.skills.items()
                      for r in s.role if r not in ROLES)

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
