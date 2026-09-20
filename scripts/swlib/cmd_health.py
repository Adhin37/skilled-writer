"""`sw health` - does the toolkit itself still hang together?

Every check here used to exist only as an assertion inside `tests/`, which means somebody who
clones the repo, edits a skill and breaks a pointer finds out by reading a stack trace, if at
all. These are the same checks as a report. `tests/test_template_wiring.py` imports the tables
below and asserts this command finds nothing, so the two cannot drift apart.

It audits the repo, never a novel. Nothing here reads a chapter.
"""

import json
import os
import re

from . import cmd_load, kb, mdio, rules
from .novelio import Novel
from .report import Report

# Every table a parser selects by column name, and the columns it selects on. `plan_rows()`
# selected on a `delivers` column the shipped `plan/chapters.md` did not have, and returned []
# against every real novel for the life of the repo while every test passed.
TABLE_ACCESSORS = [
    ("threads",         ("state", "threads.md"),            ("id", "thread", "status")),
    ("growth_rows",     ("state", "growth.md"),              ("character", "rung")),
    ("skill_rows",      ("state", "growth.md"),              ("character", "skill", "stage")),
    ("standing_rows",   ("state", "power.md"),               ("character", "tier", "the edge")),
    ("ladder_rows",     ("state", "power.md"),               ("tier", "how many alive")),
    ("pressure_rows",   ("state", "power.md"),               ("ch", "opposition", "p")),
    ("gain_rows",       ("state", "power.md"),               ("ch", "source", "new problem")),
    ("boost_rows",      ("state", "power.md"),               ("ch", "boost", "the debt")),
    ("curve_plan_rows", ("state", "power.md"),               ("arc", "pressure band")),
    ("divergence_rows", ("state", "timeline.md"),            ("ch", "mc action", "effect")),
    ("plan_rows",       ("plan", "chapters.md"),             ("#", "title", "delivers")),
    ("voice_rows",      ("bible", "cast", "_voices.md"),     ("character", "intel", "artic",
                                                              "wit")),
    ("competence_rows", ("bible", "cast", "_competence.md"), ("character", "domain", "level")),
]

SECTION_LOOKUPS = rules.SECTION_LOOKUPS


# Axes a skill requires every character to carry. The template is where a new novel gets its
# slots, so an axis the corpus mandates and the template does not offer is an axis no novel will
# ever have: `cadence` was added to `voice-separation` section 3 and to CLAUDE.md section 4 and
# reached neither template file, and `eq` reached the matrix but not the profile the matrix says
# is its source of truth. `_orphan_keys` already checks config-key -> owner; this is the other
# direction, owner -> template slot.
TEMPLATE_AXES = [
    ("eq",      "social-perception", [("bible", "cast", "_voices.md"),
                                      ("bible", "cast", "_character-template.md")]),
    ("cadence", "voice-separation",  [("bible", "cast", "_voices.md"),
                                      ("bible", "cast", "_character-template.md")]),
    ("lasting harm", "character-development", [("state", "growth.md")]),
]

# A card is written by the skill that owns the defect and opened by the dispatcher that needs
# the answer, so it is dispatched from there rather than cited from its own body. CLAUDE.md
# section 8. The edge used to be checked by looking for the card's path as a literal string in
# the dispatcher's body, which only ever proved that a copy of the list existed there; the list
# is data now, and `_cards` checks the edge structurally instead.
CARD_OWNERS = {"draft-card.md": "write-chapter", "audit-card.md": "revision-pass"}

# `hook-and-pacing:38-39` rots the moment a paragraph is added above it, and rots silently.
LINE_CITATION = re.compile(
    r"`?\b([a-z][a-z0-9]*(?:-[a-z0-9]+)+|[A-Za-z0-9_./-]+\.md):(\d+)(?:-(\d+))?\b`?")


def skills_dir(repo_root):
    """`kb`'s, not a second one. Two private copies of a path is two things to move."""
    return kb.skills_dir(repo_root)


def skill_dirs(repo_root):
    """Every directory under the skills tree, loadable or not. `_skills` needs the failures."""
    d = skills_dir(repo_root)
    if not os.path.isdir(d):
        return []
    return sorted(n for n in os.listdir(d)
                  if os.path.isdir(os.path.join(d, n)) and not n.startswith("."))


def skill_names(repo_root):
    """The skills that actually LOAD - a directory with a `SKILL.md` in it.

    The requirement used to be absent, so a directory left behind by a half-finished move
    counted as a skill everywhere downstream and every check ran against a body that was not
    there. `_skills` still reports the directory that has no `SKILL.md`; nothing else has to.
    """
    d = skills_dir(repo_root)
    return [n for n in skill_dirs(repo_root)
            if os.path.isfile(os.path.join(d, n, "SKILL.md"))]


def run(repo_root, commands=None):
    """`commands` is the dispatcher's own subcommand list, passed in to avoid importing sw.py."""
    rep = Report("health - %s" % os.path.basename(os.path.abspath(repo_root)))
    for name in skill_dirs(repo_root):
        if not os.path.isfile(os.path.join(skills_dir(repo_root), name, "SKILL.md")):
            rep.defect("skill-frontmatter", "%s/ has no SKILL.md - the skill cannot load" % name,
                       path=os.path.join(skills_dir(repo_root), name, "SKILL.md"))
    names = skill_names(repo_root)
    if not names:
        # Present-but-empty and absent-entirely are different failures and the message used to
        # report both as the second. They arrive by different routes - an empty tree is what a
        # move that deleted before it copied leaves behind - and the fix is not the same.
        where = os.path.abspath(repo_root).replace(os.sep, "/")
        rep.defect("skills",
                   "%s/.claude/skills/ is empty - no skill is reachable" % where
                   if os.path.isdir(skills_dir(repo_root))
                   else "no .claude/skills/ directory under %s" % where)
        return rep

    _corpus_floor(repo_root, rep)
    _skills(repo_root, names, rep)
    _registry(repo_root, names, rep)
    _template(repo_root, rep)
    _commands(repo_root, commands, rep)
    _slash_commands(repo_root, rep)
    _uncited(repo_root, names, _owns_map(repo_root, names, rep), rep)
    _overlap(repo_root, names, rep)
    _kb(repo_root, rep)
    _force(repo_root, rep)
    _role(repo_root, rep)
    _partition(repo_root, rep)
    _agents(repo_root, rep)
    _settings_hooks(repo_root, rep)
    _card_budget(repo_root, rep)
    _card_scope(repo_root, rep)
    rep.info("scope", [
        "   %d skills, %d roles, %d template accessors, %d template sections, %d template "
        "axes checked"
        % (len(names), len(kb.ROLES), len(TABLE_ACCESSORS), len(SECTION_LOOKUPS),
           len(TEMPLATE_AXES)),
        "   This is wiring only. It says nothing about whether a skill's advice is any good.",
    ])
    return rep


# ---------------------------------------------------------------------- floor

def _corpus_floor(repo_root, rep):
    """Everything else here is a ceiling. This is the floor, and it runs first.

    Every budget in this toolkit bounds the corpus from above, and an empty corpus satisfies all
    of them: `kb.Index._build()` skips a directory with no `SKILL.md`, so a half-finished move
    returns nothing and `sw health` reports 0/0/0 against a corpus no agent can reach. A clean
    run is what the worst failure looks like, which is why this is the first check in the file
    rather than one more in the list.

    `rules.CORPUS_FLOOR` holds the numbers and `kb.Index._floor()` does the counting, so the
    same shortfall reaches `sw kb validate` and `sw load` without being computed three times.
    """
    idx = kb.index(repo_root, refresh=True)
    for shortfall in idx.shortfalls:
        rep.defect("corpus-floor", shortfall,
                   detail="rules.CORPUS_FLOOR. Check that .claude/skills/ and roles/ "
                          "are both present before trusting any other line of this report.")


# --------------------------------------------------------------------- skills

def _skills(repo_root, names, rep):
    root = skills_dir(repo_root)
    bodies = {}
    for name in names:
        path = os.path.join(root, name, "SKILL.md")
        text = mdio.read_text(path)
        bodies[name] = text
        fm, body = mdio.split_frontmatter(text)
        if not fm:
            rep.defect("skill-frontmatter", "%s/SKILL.md has no YAML frontmatter" % name,
                       path=path, line=1)
            continue
        meta = mdio.parse_yaml(fm)
        declared = str(meta.get("name", "") or "").strip()
        if not declared:
            rep.defect("skill-frontmatter", "%s/SKILL.md declares no `name:`" % name,
                       path=path, line=1)
        elif declared != name:
            rep.defect("skill-frontmatter",
                       "%s/SKILL.md declares `name: %s` - it must match the directory"
                       % (name, declared), path=path, line=1)
        if not str(meta.get("description", "") or "").strip():
            rep.defect("skill-frontmatter",
                       "%s/SKILL.md declares no `description:` - the dispatcher picks skills "
                       "by description alone" % name, path=path, line=1)

    idx = kb.index(repo_root, refresh=True)
    _references(idx, names, rep)
    _line_citations(idx, names, rep)


def _references(idx, names, rep):
    """Two jobs, and they are opposite: nothing orphaned, nothing dangling.

    **J1, anti-orphan.** A `type: reference` file is cited by at least one file with the same
    owner - the body, the draft card or the audit card. Stated that way it is a claim about
    OWNERSHIP rather than about directories, so it survives the file moving to another tree,
    and it is the invariant the repo actually means: a pointer without a trigger is not read.

    **J2, anti-dangling.** Every citation resolves to a file that exists. This subsumes the old
    `_dangling_cards`, which was the same check narrowed to cards and written with its own
    third copy of the citation regex. One regex now, `kb.CITATION`, and one resolver.
    """
    # J1 - every reference is cited by something its own owner wrote. Asked through the
    # resolver, not by looking for the basename in the owner's text: a role file is
    # `<owner>.<stem>.md` on disk and is legally cited by either its full path or its bare stem,
    # and a substring test sees only the first. So the old form reported a live pointer as an
    # orphan - the same string-matching heuristic this check was rewritten to stop using, left
    # behind in the one place it still decided something. Same resolver as J2, one call each.
    cited = set()
    for name in names:
        for path in idx.owned_files(name):
            for m in kb.CITATION.finditer(mdio.read_text(path)):
                target = idx.resolve(m, name)
                if target is not None:
                    cited.add((name, target.rel))
    for f in idx.files:
        if f.type != "reference":
            continue
        if (f.owner, f.rel) not in cited:
            rep.defect("skill-reference",
                       "%s is never cited by anything %s owns - a pointer without a trigger is "
                       "not read" % (f.rel, f.owner), path=f.path)

    # A card is the one inversion in the corpus: it is opened by its dispatcher rather than
    # cited by its own skill, so J1 cannot reach it. Check the edge it does have instead.
    for f in idx.files:
        if f.type in ("draft-card", "audit-card") and f.dispatcher not in idx.skills:
            rep.defect("skill-card", "%s exists but its dispatcher `%s` is missing"
                       % (f.rel, f.dispatcher), path=f.path)

    # J2 - and every pointer lands on a real file, from anywhere in the corpus.
    scanned = [(None, os.path.join(idx.repo_root, "CLAUDE.md"))]
    for name in names:
        scanned += [(name, p) for p in idx.owned_files(name)]
    for citing, path in scanned:
        if not os.path.isfile(path):
            continue
        text = mdio.read_text(path)
        seen = set()
        for m in kb.CITATION.finditer(text):
            raw = m.group(0)
            if raw in seen:
                continue
            seen.add(raw)
            if idx.resolve(m, citing) is not None:
                continue
            # A BARE `x.md` is a citation only when the owner has a file by that name -
            # `novel.md`, `state/threads.md` and `CLAUDE.md` are named all over the corpus and
            # none is a pointer at a knowledge file. Reporting those would make the check
            # unusable, which is how a check gets switched off. The qualified forms carry
            # `references/` or a role path, so an unresolved one is unambiguously broken.
            if m.group("bare"):
                continue
            # A role path the index cannot resolve but which **exists on disk** is not broken.
            # `roles/review/` is the case: the reader carries no corpus, so `kb.BUCKETS` does not
            # list it and `resolve()` answers None for two files that open perfectly well. The
            # defect this check raises is about openability, so the filesystem is the right
            # oracle for it - the index is the right one for everything above.
            if m.group("rel") and os.path.isfile(os.path.join(idx.repo_root, m.group("rel"))):
                continue
            rep.defect("skill-reference",
                       "cites `%s`, which does not exist - the reader is sent to a file "
                       "that never opens" % raw, path=path)


def _line_citations(idx, names, rep):
    for name in names:
        for path in idx.owned_files(name):
            text = mdio.read_text(path)
            for i, line in enumerate(text.split("\n"), 1):
                    m = LINE_CITATION.search(line)
                    if not m:
                        continue
                    rep.defect("line-citation",
                               "cites `%s` by line number - cite the section instead, because "
                               "a line number rots silently when a paragraph is added above it"
                               % m.group(0).strip("`"), path=path, line=i)
                    break


# ------------------------------------------------------------------ registry

def _registry(repo_root, names, rep):
    claude = os.path.join(repo_root, "CLAUDE.md")
    if not os.path.isfile(claude):
        rep.warn("skill-registry", "no CLAUDE.md at the repo root - cannot check the registry")
        return
    text = mdio.read_text(claude)
    registry = mdio.section(text, "Skill registry") or text

    for name in names:
        if ("`%s`" % name) not in registry:
            rep.defect("skill-registry",
                       "`%s` exists on disk but section 3 never names it - the registry is the "
                       "contract, and a skill missing from it is a skill nobody dispatches"
                       % name, path=claude)

    listed = set()
    for table in mdio.parse_tables(registry):
        for row in table.rows:
            m = re.match(r"^`([a-z][a-z0-9-]*)`$", row.first().strip())
            if m:
                listed.add(m.group(1))
    for name in sorted(listed - set(names)):
        rep.defect("skill-registry",
                   "section 3 lists `%s`, which has no .claude/skills/%s/ directory"
                   % (name, name), path=claude)
    _dispatched(repo_root, registry, rep)


def _dispatched(repo_root, registry, rep):
    """A registry row that names a dispatcher must be named back by that dispatcher.

    The check above this one is card-anchored: it asks whether every card that exists is opened
    by its dispatcher. That leaves a blind spot for a skill with no card at all, and benchmark
    run #2 fell into it - CLAUDE.md section 3 says `mtl-detox` runs "Inside `revision-pass`",
    `revision-pass/SKILL.md` never mentioned it, and the skill loaded zero times in a real run
    while `health` reported no defects. This is the converse, skill-anchored check.
    """
    for table in mdio.parse_tables(registry):
        for row in table.rows:
            m = re.match(r"^`([a-z][a-z0-9-]*)`$", row.first().strip())
            if not m:
                continue
            name = m.group(1)
            for dispatcher in sorted(set(CARD_OWNERS.values())):
                if ("`%s`" % dispatcher) not in row.raw:
                    continue
                path = os.path.join(skills_dir(repo_root), dispatcher, "SKILL.md")
                if not os.path.isfile(path):
                    continue
                if name not in mdio.read_text(path):
                    rep.defect("skill-dispatch",
                               "section 3 says `%s` runs inside `%s`, but %s/SKILL.md never "
                               "names it - a skill its dispatcher does not name is a skill that "
                               "never enters context" % (name, dispatcher, dispatcher),
                               path=path)


# ------------------------------------------------------------------ template

def _template(repo_root, rep):
    tpl = os.path.join(repo_root, "novels", "_template")
    if not os.path.isdir(tpl):
        rep.defect("template", "novels/_template is missing - `newnovel` has nothing to copy")
        return
    novel = Novel(tpl)

    for accessor, parts, cols in TABLE_ACCESSORS:
        text = novel._text(*parts)
        if novel._table_by_headers(text, *cols) is None:
            have = [t.headers for t in mdio.parse_tables(text)]
            rep.defect("template-table",
                       "`Novel.%s()` selects on %s, which %s does not have - it returns [] "
                       "against every real novel"
                       % (accessor, list(cols), "/".join(parts)),
                       path=novel.path(*parts),
                       detail="template has: %s" % (have or "no tables at all"))

    for parts, heading in SECTION_LOOKUPS:
        got = mdio.section(novel._text(*parts), heading)
        if not (got and got.strip()):
            rep.defect("template-section",
                       "%s has no non-empty `%s` section - the read-set slices it by that "
                       "heading and silently drops it" % ("/".join(parts), heading),
                       path=novel.path(*parts))

    missing = [k for k in (novel.cfg.get("optional") or {})
               if not os.path.isdir(os.path.join(skills_dir(repo_root), k))]
    for key in missing:
        rep.defect("optional-toggle",
                   "`optional: %s` has no .claude/skills/%s/ behind it - it never no-ops, it is "
                   "simply never read" % (key, key), path=novel.path("novel.md"))

    _template_axes(novel, rep)
    _orphan_keys(repo_root, novel, rep)


def _template_axes(novel, rep):
    """An axis the corpus mandates that the template offers no slot for.

    A new novel is scaffolded from `novels/_template`, so a slot missing here is a field that
    never gets filled in any book. The failure is silent in both directions: the drafter has
    nowhere to write the value, and the rule that needs it reads as satisfied because nothing
    contradicts it.
    """
    for axis, owner, targets in TEMPLATE_AXES:
        word = re.compile(r"\b%s\b" % re.escape(axis), re.I)
        for parts in targets:
            if not word.search(novel._text(*parts)):
                rep.defect("template-axis",
                           "`%s` owns the `%s` axis and %s offers no slot for it - a novel "
                           "scaffolded from this template can never carry it"
                           % (owner, axis, "/".join(parts)),
                           path=novel.path(*parts))


def _orphan_keys(repo_root, novel, rep):
    """A novel.md key nothing names is a question asked at init whose answer goes nowhere.

    `docs/` is excluded deliberately: a key named only in a post-mortem is not a key with an
    owner.
    """
    corpus = []
    for rel in ("CLAUDE.md",):
        p = os.path.join(repo_root, rel)
        if os.path.isfile(p):
            corpus.append(mdio.read_text(p))
    for top in (".claude", "scripts"):
        for dirpath, dirs, files in os.walk(os.path.join(repo_root, top)):
            dirs[:] = [d for d in dirs if d != "__pycache__"]
            for f in files:
                if f.endswith((".md", ".py")):
                    corpus.append(mdio.read_text(os.path.join(dirpath, f)))
    text = "\n".join(corpus)

    for key in sorted(_flatten(novel.cfg)):
        leaf = key.split(".")[-1]
        if key in text or re.search(r"\b%s\b" % re.escape(leaf), text):
            continue
        rep.defect("config-owner",
                   "novel.md declares `%s` but no skill names it and no script reads it - wire "
                   "it to an owner or drop it" % key, path=novel.path("novel.md"))


def _flatten(data, prefix=""):
    out = []
    for k, v in (data or {}).items():
        key = "%s.%s" % (prefix, k) if prefix else k
        out += _flatten(v, key) if isinstance(v, dict) else [key]
    return out


# ------------------------------------------------------------------ ownership

# Passages every skill is expected to share: the card and reference-table templates. They are
# structure, not duplicated craft advice, so the overlap detector skips anything containing one.
BOILERPLATE = (
    "written here rather than summarised there",
    "opened by",
    "this file does not carry other skills",
    "cite them so the gaps",
    "when its trigger fires",
    "section numbers are stable",
    # Card scaffolding. Every audit card closes on the same three-column triage table; the
    # header is structure, not advice, and a skill that writes one has copied a form rather
    # than somebody else's rule. Kept to the single canonical wording on purpose - a second
    # accepted spelling of the same header is how the exemption grows into a hole.
    "where it fails most often symptom what it actually is go to",
    # The card rows in a skill's own reference table. Every skill that owns a card writes the
    # same disclaimer, and it is an instruction about who opens the file rather than advice.
    "never by you",
    # The merged-card header. Four cards now carry two owners' decisions because the card budget
    # forbids a new file, and each says so in the same words on purpose: the reader has to be
    # able to tell a merge from a land-grab at a glance.
    "one card two owners",
    "the card budget is why they share a file",
    "and each half names its owner",
    # The boundary heading a reference opens when it sits next to somebody else's rule. Three
    # files carry it and more will, because "cite the owner and stop" is the rule rather than a
    # style. Only the heading is exempt: its table's column names differ file to file, one of
    # them is used once, and exempting a header on one file's evidence is how this tuple grows
    # into a hole.
    "where this is not the right file",
)

OVERLAP_RUN = 10        # words, normalised, before a shared passage counts
OVERLAP_MAX = 2         # distinct shared runs a pair of skills may have


def _owns_map(repo_root, names, rep):
    """`metadata.owns` in frontmatter is the scope declaration. One concept, one owner.

    Without it the toolkit has no answer to "whose rule is this?", and the measured consequence
    is two skills carrying the same advice until the copies drift apart.

    It lives under `metadata:` because that is the only place the Agent Skills spec sanctions for
    custom keys - a top-level `owns:` works in Claude Code but hard-errors when the toolkit is
    packaged or uploaded. The top-level form is still read, so a skill written before the move is
    not silently treated as declaring nothing.
    """
    owners = {}
    for name in names:
        path = os.path.join(skills_dir(repo_root), name, "SKILL.md")
        if not os.path.isfile(path):
            continue
        fm, _ = mdio.split_frontmatter(mdio.read_text(path))
        cfg = mdio.parse_yaml(fm) if fm else {}
        meta = cfg.get("metadata")
        owns = (meta.get("owns") if isinstance(meta, dict) else None)
        if owns is None:
            owns = cfg.get("owns")
        if not isinstance(owns, list) or not owns:
            rep.defect("skill-scope", "%s declares no `owns:` - every skill states the concepts "
                                      "it is the only authority on" % name, path=path, line=1)
            continue
        for slug in owns:
            slug = str(slug).strip()
            if not re.match(r"^[a-z][a-z0-9-]*$", slug):
                rep.defect("skill-scope", "%s owns `%s` - concept slugs are kebab-case"
                           % (name, slug), path=path, line=1)
                continue
            if slug in owners:
                rep.defect("skill-scope", "`%s` is claimed by both %s and %s - a concept has one "
                                          "owner, and the other skill cites it"
                           % (slug, owners[slug], name), path=path, line=1)
            else:
                owners[slug] = name
    return owners


def _normalise(text):
    text = re.sub(r"`[^`]*`", " ", text)                    # citations live in code spans
    text = re.sub(r"\[[^\]]*\]\([^)]*\)", " ", text)
    text = re.sub(r"[^a-z0-9 ]", " ", text.lower())
    return re.sub(r"\s+", " ", text).strip().split()


def _runs(words):
    """Every OVERLAP_RUN-word window, with the shared template text cut out first.

    Boilerplate is *removed* rather than filtered window-by-window. Filtering only suppresses a
    window that contains a whole marker, so the windows straddling a marker's edge survived and
    the template tripped the check it was exempted from.
    """
    text = " ".join(words)
    for phrase in BOILERPLATE:
        text = text.replace(phrase, "\x00")
    out = set()
    for segment in text.split("\x00"):
        w = segment.split()
        for i in range(len(w) - OVERLAP_RUN + 1):
            out.add(" ".join(w[i:i + OVERLAP_RUN]))
    return out


UNCITED_MIN = 2         # mentions of another skill's concept before silence is a finding


def _uncited(repo_root, names, owners, rep):
    """A skill that discusses someone else's concept and never names the owner.

    The overlap check finds copied text. This finds the case it cannot: a skill that states a
    rule in its own words, so no passage matches, and leaves the reader no route to the authority.
    Two copies of an idea drift the same way whether or not they share a sentence.

    Only multi-word concepts are checked. A single word like `title` or `pressure` is ordinary
    vocabulary, and flagging it would train people to sprinkle citations rather than mean them.
    """
    idx = kb.index(repo_root, refresh=True)
    raw, words = {}, {}
    for name in names:
        raw[name] = _skill_corpus(idx, name)
        words[name] = " ".join(_normalise(raw[name]))

    for slug, owner in sorted(owners.items()):
        phrase = slug.replace("-", " ")
        if " " not in phrase:
            continue
        for name in names:
            if name == owner or name not in words:
                continue
            seen = words[name].count(phrase)
            if seen >= UNCITED_MIN and owner not in raw[name]:
                rep.warn("skill-scope", "%s discusses `%s` %d times and never names %s, which owns "
                                        "it - cite the owner or drop the passage"
                         % (name, slug, seen, owner),
                         path=os.path.join(skills_dir(repo_root), name, "SKILL.md"))


def _skill_corpus(idx, name):
    """Every `.md` body under a skill, frontmatter stripped.

    Frontmatter is structure, not craft advice, and stripping it protects both duplication
    checks from the knowledge-base layer in opposite directions. `_overlap` would otherwise see
    the uniform `type:`/`owner:`/`dispatcher:` block that every card carries as a shared 10-word
    passage and warn on all 171 pairs of draft cards - the same reason BOILERPLATE is cut out
    before comparison. `_uncited` would otherwise be *cleared* by a frontmatter field: a card
    that says `dispatcher: write-chapter` has not cited write-chapter, and only a real mention
    in the prose should count. One break is noisy and one is silent; the silent one is worse.
    """
    parts = []
    for path in idx.owned_files(name):
        _fm, body = mdio.split_frontmatter(mdio.read_text(path))
        parts.append(body)
    return "\n".join(parts)


def _overlap(repo_root, names, rep):
    """Long passages carried by two skills at once.

    It finds text, not meaning, so it cannot see a paraphrase - but every duplicate this repo
    actually grew was copied, and a copy is what drifts. Citing a concept is free: a code span is
    stripped before comparison, so pointing at an owner never trips this.
    """
    idx = kb.index(repo_root, refresh=True)
    shingles = {}
    for name in names:
        shingles[name] = _runs(_normalise(_skill_corpus(idx, name)))

    for i, a in enumerate(names):
        for b in names[i + 1:]:
            both = shingles.get(a, set()) & shingles.get(b, set())
            if len(both) > OVERLAP_MAX:
                sample = sorted(both)[0]
                rep.warn("skill-overlap", "%s and %s share %d passages of %d+ words - one of them "
                                          "owns this and the other should cite it. e.g. \"%s...\""
                         % (a, b, len(both), OVERLAP_RUN, sample[:70]),
                         path=os.path.join(skills_dir(repo_root), a, "SKILL.md"))


# ------------------------------------------------------------------ commands

def _kb(repo_root, rep):
    """The knowledge-base layer: frontmatter, the dispatch edges, and every trigger.

    This replaces the old string-presence card check. That one asked whether the dispatcher's
    body contained the card's path as literal text, which proved only that a copy of the list
    lived there - and the copy was the thing the list being data was meant to remove. The edge
    is now checked from both ends: a card declares the dispatcher that opens it, and the
    dispatcher has to resolve to exactly the cards that declare it.
    """
    from . import cmd_kb, kb
    idx = kb.index(repo_root, refresh=True)
    for problem in idx.problems:
        rep.defect("skill-scope", problem)
    cmd_kb.validate(idx, rep)

    for kind, dispatcher in (("draft-card", "write-chapter"), ("audit-card", "revision-pass")):
        cards = idx.by_type(kind)
        on_disk = {f.owner for f in cards}
        declared = {f.owner for f in cards if f.dispatcher == dispatcher}
        for owner in sorted(on_disk - declared):
            rep.defect("skill-card", "%s's %s does not declare `dispatcher: %s` - a card no "
                                     "dispatcher claims is a file nobody opens"
                       % (owner, kind, dispatcher))
        for f in cards:
            if kind == "draft-card" and not f.phase:
                rep.defect("skill-card", "%s declares no `phase:` - the dispatcher cannot place "
                                         "it" % f.rel, path=f.path)
            if kind == "audit-card" and not f.pass_:
                rep.defect("skill-card", "%s declares no `pass:` - the dispatcher cannot place "
                                         "it" % f.rel, path=f.path)
            if not f.description:
                rep.warn("skill-card", "%s declares no `description:` - the dispatcher prints it "
                                       "in place of the table it replaced" % f.rel, path=f.path)


def _force(repo_root, rep):
    """Every skill declares how hard its rules bind.

    Without it the corpus states the essentialism ban and a note about em-dash density in the
    same register, in the same kind of list, with the same weight - so a model obeys both at the
    same anxiety level, and the whole cost of that is paid by the stylistic rules, which are
    exactly the ones a good chapter sometimes needs to break. `docs/creative-latitude.md`.
    """
    idx = kb.index(repo_root, refresh=True)
    for name in sorted(idx.skills):
        skill = idx.skills[name]
        path = os.path.join(skills_dir(repo_root), name, "SKILL.md")
        if not skill.force:
            rep.defect("skill-force",
                       "`%s` declares no `metadata.force:` - a rule whose weight is not stated "
                       "is obeyed at the same anxiety level as every other" % name, path=path)
        elif skill.force not in kb.FORCE:
            rep.defect("skill-force",
                       "`%s` declares force `%s`, which is not one of %s"
                       % (name, skill.force, ", ".join(kb.FORCE)), path=path)


def _role(repo_root, rep):
    """Every skill declares which agent may open it.

    A role is a view over the corpus, not a location in it - 23 of the 32 card-carrying skills
    serve both the draft and the gate, so a per-role folder split would have to duplicate them.
    A skill with no role is a skill no agent reaches; a misspelled role is worse, because it
    presents as a skill quietly missing from a view rather than as an error.

    The card budget is *not* re-checked here. `CARD_BUDGET` bounds the unconditional card set by
    kind, `_card_budget` below already enforces it, and draft-card/audit-card map one-to-one onto
    the draft and gate roles - so a per-role check would be the same check under a second name.
    """
    idx = kb.index(repo_root, refresh=True)
    for name in idx.roleless():
        rep.defect("skill-role",
                   "`%s` declares no `metadata.role:` - no agent's view contains it, so nothing "
                   "reaches it" % name,
                   path=os.path.join(skills_dir(repo_root), name, "SKILL.md"))
    for name, role in idx.bad_roles():
        rep.defect("skill-role",
                   "`%s` declares role `%s`, which is not one of %s"
                   % (name, role, ", ".join(kb.ROLES)),
                   path=os.path.join(skills_dir(repo_root), name, "SKILL.md"))
    for role in kb.ROLES:
        if role in kb.ROLES_WITHOUT_CORPUS:
            continue
        if not idx.view(role)[0]:
            rep.warn("skill-role",
                     "no skill declares role `%s` - the role resolves to an empty view" % role)


# `<owner>.<stem>.md`, and owner names contain no dots - which is what makes the split safe.
ROLE_FILE = re.compile(r"^[a-z][a-z0-9-]*\.[a-z0-9-]+\.md$")


def _partition(repo_root, rep):
    """The role trees are a partition, and this is the check that replaces a prose rule.

    Five assertions, one per way the layout can go wrong. They are what makes "a drafting agent
    never opens a `SKILL.md`" unfalsifiable rather than obeyed: there is no body in the tree to
    open, and a file in the wrong bucket is a visibly wrong path rather than a subtly wrong file.

    **A sixth assertion from Part 7 is deliberately absent** - *no `draft/` file is reachable
    from an audit card, and none in `gate/` from a draft card*. It is the special case of the
    closure assertion below where the disagreement is a card's, so implementing it would be a
    second copy of a check under a different name, which is the defect class this repo exists to
    remove. `kb.Index.reachable()` computes both closures once and the bucket comparison catches
    it: a `draft/` file the gate reaches wants `shared`, and wanting `shared` while sitting in
    `draft/` is already a defect.

    A missing `roles/` is **not** reported here. `_corpus_floor` owns "the corpus vanished", it
    runs first, and it is anchored to this repo - so a two-skill fixture that never writes a role
    file is silent here rather than being asked to have a partition it has no reason to.
    """
    root = kb.roles_dir(repo_root)
    if not os.path.isdir(root):
        return
    idx = kb.index(repo_root, refresh=True)

    # 1 - no body in a role tree. The whole point, and the one that needs no index.
    # 2 - one bucket deep, `.md` only, named `<owner>.<stem>.md`.
    known = set(kb.BUCKETS) | set(kb.ROLES_WITHOUT_CORPUS)
    for name in sorted(os.listdir(root)):
        path = os.path.join(root, name)
        if not os.path.isdir(path):
            rep.defect("partition",
                       "roles/%s is a file at the root of the role trees - every corpus file "
                       "belongs to exactly one bucket" % name, path=path)
            continue
        if name not in known:
            rep.defect("partition",
                       "roles/%s/ is not a bucket - the buckets are %s"
                       % (name, ", ".join(sorted(known))), path=path)
            continue
        for fname in sorted(os.listdir(path)):
            fpath = os.path.join(path, fname)
            if fname == "SKILL.md":
                rep.defect("partition",
                           "roles/%s/SKILL.md is a skill body inside a role tree - a body is "
                           "for designing the thing, a card for deciding it" % name, path=fpath)
            elif os.path.isdir(fpath):
                rep.defect("partition",
                           "roles/%s/%s/ is a subdirectory - a bucket is flat, so a path can "
                           "go straight to Read with no resolution step" % (name, fname),
                           path=fpath)
            elif not fname.endswith(".md"):
                rep.defect("partition", "roles/%s/%s is not a `.md` file" % (name, fname),
                           path=fpath)
            elif name not in kb.ROLES_WITHOUT_CORPUS and not ROLE_FILE.match(fname):
                # `review` is exempt: the reader carries no corpus, so its two files are
                # documents rather than owned notes and neither declares an owner to prefix.
                rep.defect("partition",
                           "roles/%s/%s is not `<owner>.<stem>.md` - the prefix is the checksum "
                           "on the declared owner" % (name, fname), path=fpath)

    # 3 - the closure agrees with the shelf. The one with teeth: it is what tells you a NEW
    #     note cited from both sides belongs in `shared/`, before either role is refused it.
    reach = dict((role, idx.reachable(role)) for role in kb.CARD_ROLES.values())
    for f in idx.files:
        want = idx.bucket_for(f.rel, reach)
        if f.bucket is None:
            rep.defect("partition",
                       "%s is a corpus file outside the role trees - it belongs in "
                       "roles/%s/" % (f.rel, want), path=f.path)
        elif f.bucket != want:
            rep.defect("partition",
                       "%s sits in roles/%s/ but is reached by %s - it belongs in roles/%s/"
                       % (f.rel, f.bucket, _reached_by(f.rel, reach) or "neither role", want),
                       path=f.path)

    # 4 - and a skill that writes a card declares the role that opens it. A warn, not a defect:
    #     the card is the evidence and `metadata.role:` is the declaration, so a disagreement is
    #     a stale declaration far more often than it is a misfiled card.
    #
    #     Scoped to CARDS, not to every file the skill owns, and the wider form was tried first
    #     and is wrong. A note's bucket is a property of the citation GRAPH - who cites it -
    #     while `metadata.role:` is a property of the SKILL, and the two legitimately diverge
    #     wherever a merged card names a second owner: `roles/draft/character-development.ladders.md`
    #     sits in the drafter's tree because `voice-separation`'s draft card cites it, and the
    #     drafter still never opens `character-development/SKILL.md`. The wide form fired on six
    #     such cases here, which is how a warn stops being read.
    for f in idx.files:
        role = kb.CARD_ROLES.get(f.type)
        skill = idx.skills.get(f.owner)
        if role and skill is not None and role not in (skill.role or []):
            rep.warn("partition",
                     "`%s` owns %s but does not declare `metadata.role: %s` - the role that "
                     "opens the card does not have the skill in its view"
                     % (f.owner, f.rel, role), path=skill.path)

    # 5 - and nothing in a writing role's tree sends it into `docs/`. `design` is exempt, being
    #     the one role that is not denied it; every other bucket, `review` included, is bound.
    #     Maintainer-facing rationale belongs in `provenance:`, where it costs no body words and
    #     cannot read as an instruction. Without this the ban is a sentence in `AGENTS.md`.
    for bucket in sorted(known - {"design"}):
        bdir = os.path.join(root, bucket)
        if not os.path.isdir(bdir):
            continue
        for fname in sorted(os.listdir(bdir)):
            if not fname.endswith(".md"):
                continue
            fpath = os.path.join(bdir, fname)
            body = mdio.split_frontmatter(mdio.read_text(fpath))[1]
            for i, line in enumerate(body.split("\n"), 1):
                m = DOCS_CITATION.search(line)
                if m:
                    rep.defect("partition",
                               "roles/%s/%s cites `%s`, which its own role may not open - move "
                               "maintainer rationale to `provenance:` in the frontmatter"
                               % (bucket, fname, m.group(0)), path=fpath, line=i)
                    break


DOCS_CITATION = re.compile(r"\bdocs/[A-Za-z0-9._-]+\.md")


def _reached_by(rel, reach):
    return ", ".join(sorted(r for r in reach if rel in reach[r]))


AGENTS_REL = os.path.join(".claude", "agents")


def _agents(repo_root, rep):
    """Role agents: the frontmatter parses, the name matches, and the hooks point at real files.

    A hook whose script has moved does not fail loudly - Claude Code logs it and runs the agent
    anyway, so the isolation quietly stops existing while every test still passes. That is the
    same failure shape as a card whose dispatcher was renamed, and it is checked here for the
    same reason.

    Nothing here judges an agent's prompt. This is wiring.
    """
    root = os.path.join(repo_root, AGENTS_REL)
    if not os.path.isdir(root):
        return
    names = []
    for fname in sorted(os.listdir(root)):
        if not fname.endswith(".md"):
            continue
        path = os.path.join(root, fname)
        stem = fname[:-3]
        names.append(stem)
        raw = mdio.split_frontmatter(mdio.read_text(path))[0]
        if not raw.strip():
            rep.defect("agent-frontmatter",
                       "%s has no YAML frontmatter - it cannot load as an agent" % fname,
                       path=path)
            continue
        cfg = mdio.parse_yaml(raw)
        declared = str(cfg.get("name") or "").strip()
        if declared != stem:
            rep.defect("agent-frontmatter",
                       "%s declares `name: %s` - it must match the filename"
                       % (fname, declared or "(none)"), path=path)
        if not str(cfg.get("description") or "").strip():
            rep.defect("agent-frontmatter",
                       "%s declares no `description:` - nothing can route to it" % fname,
                       path=path)
        for written, script in _hook_scripts(mdio.read_text(path)):
            _check_hook(repo_root, rep, "agent-hook", fname, written, script, path,
                        "the agent runs unguarded")
    if names:
        rep.info("agents", ["   %s" % ", ".join(names)])


_HOOK_CMD = re.compile(r"""command:\s*['"]?(?:python3?|sh|bash)\s+(\S.*?)['"]?\s*$""", re.M)
_PROJECT_DIR = re.compile(r"""\$\{?CLAUDE_PROJECT_DIR\}?""")


def _hook_scripts(text):
    """Script paths named by a frontmatter hook, as (as written, resolved against the repo) pairs.

    Deliberately shallow: it reads the raw file rather than the parsed YAML, because the nested
    hook shape is three levels deep and a half-parsed one would report nothing rather than report
    a problem.

    `${CLAUDE_PROJECT_DIR}` is the documented way to name a script that must resolve whatever the
    cwd is, and it has to be resolved here rather than matched around: a pattern that only reads
    bare relative paths finds nothing in the recommended form, so adopting the recommendation
    would silently retire the check that the script exists.
    """
    out = []
    for rest in _HOOK_CMD.findall(text):
        pair = _script_from_command(rest)
        if pair:
            out.append(pair)
    return out


_INTERPRETERS = ("python3", "python", "py", "sh", "bash")


def _script_from_command(cmd):
    """`python3 "${CLAUDE_PROJECT_DIR}"/a/b.py --flag` -> (as written, resolved against the repo).

    Tolerates the interpreter already having been eaten by the caller's pattern, because the two
    callers arrive from different directions: `_HOOK_CMD` consumes it, JSON does not.
    """
    parts = [x for x in cmd.split() if x]
    while parts and parts[0].rsplit("/", 1)[-1] in _INTERPRETERS:
        parts.pop(0)
    if not parts:
        return None
    written = parts[0]
    resolved = _PROJECT_DIR.sub("", written).replace('"', "").replace("'", "").lstrip("/")
    return (written, resolved) if resolved else None


def _check_hook(repo_root, rep, check, where, written, script, path, consequence):
    """One hook command, checked twice: the script is there, and the path survives a changed cwd."""
    if not os.path.isfile(os.path.join(repo_root, script)):
        rep.defect(check, "%s wires a hook to `%s`, which does not exist - the hook is skipped "
                          "and %s" % (where, script, consequence), path=path)
    elif "CLAUDE_PROJECT_DIR" not in written and not written.startswith("/"):
        rep.warn(check, "%s wires a hook to the relative path `%s`. Hooks run in the current "
                        "directory, which follows a worktree or a cd and is not pinned to the "
                        "project root, so this resolves only when the cwd happens to be right - "
                        "and when it is not, the hook is skipped and %s. "
                        'Use "${CLAUDE_PROJECT_DIR}"/%s'
                        % (where, written, consequence, script), path=path)


SETTINGS_REL = os.path.join(".claude", "settings.json")


def _settings_hooks(repo_root, rep):
    """The same wiring check for `.claude/settings.json`, which is not an agent file.

    A guard that dispatches on which agent is calling can only be registered here, because the
    coordinator is the main session and has no agent file to carry frontmatter. So the one hook
    whose whole job is to catch the role that cannot be caught elsewhere is the one hook `_agents`
    cannot see, and its path rots in silence the same way.

    Parsed as JSON rather than pattern-matched: unlike the three-deep YAML in agent frontmatter,
    this shape parses reliably, and a settings file that does not parse is a defect on its own.
    """
    path = os.path.join(repo_root, SETTINGS_REL)
    if not os.path.isfile(path):
        return
    try:
        cfg = json.loads(mdio.read_text(path))
    except ValueError as exc:
        rep.defect("settings-hook",
                   "settings.json does not parse as JSON (%s) - every hook and permission in it "
                   "is being ignored" % exc, path=path)
        return
    hooks = cfg.get("hooks")
    if not isinstance(hooks, dict):
        return
    for event in sorted(hooks):
        for entry in hooks.get(event) or []:
            if not isinstance(entry, dict):
                continue
            for hook in entry.get("hooks") or []:
                if not isinstance(hook, dict):
                    continue
                pair = _script_from_command(str(hook.get("command") or ""))
                if pair:
                    _check_hook(repo_root, rep, "settings-hook",
                                "settings.json %s" % event, pair[0], pair[1], path,
                                "every role it guards runs unguarded")


def _card_budget(repo_root, rep):
    """How many cards EVERY novel pays for, against the budget in `rules`.

    The corpus has one growth mechanism - adding a rule - and adding a rule has always meant
    adding a file. Nothing anywhere counted the result, so it reached nineteen draft cards and
    twenty-three audit cards for a single chapter, which is the load `write-chapter` itself
    blames for "short, defensive and eventless" chapters. `docs/creative-latitude.md`.

    Conditional cards are excluded on purpose. A module that fires for one novel in ten is not
    what makes the loop heavy; the unconditional set is, because it is what every chapter of
    every book carries.
    """
    idx = kb.index(repo_root, refresh=True)
    for kind, cap in sorted(rules.CARD_BUDGET.items()):
        cards = [f for f in idx.by_type(kind)
                 if not f.when or f.when.strip() == "always"]
        live = sorted(f.owner for f in cards)
        if len(live) > cap:
            rep.defect("card-budget",
                       "%d unconditional %ss against a budget of %d (%s) - merge one into the "
                       "card that already owns its neighbourhood; a new file is not an option "
                       "past the budget"
                       % (len(live), kind, cap, ", ".join(live)))

        # And the words, which is the number a drafter actually pays. The count budget forced
        # merges, and a merged card costs exactly what its two halves cost separately - the
        # count fell 42 -> 35 while the load rose 16,359 -> 16,550 words and nothing objected.
        wcap = rules.CARD_WORD_BUDGET.get(kind)
        words = sum(cmd_load.measure(f.path)[0] for f in cards)
        if wcap and words > wcap:
            fattest = sorted(((cmd_load.measure(f.path)[0], f.owner) for f in cards),
                             reverse=True)[:3]
            rep.defect("card-words",
                       "%d words across the unconditional %ss, against a budget of %d - a "
                       "merge does not pay for itself, so something has to be cut. Heaviest: %s"
                       % (words, kind, wcap,
                          ", ".join("%s (%d)" % (o, w) for w, o in fattest)),
                       detail="docs/creative-latitude.md item 6. The budget is a ceiling to "
                              "lower, never a target to fill.")


def _norm_when(value):
    """`when:` as a comparable string. Absent and `always` are the same condition."""
    text = str(value or "").strip()
    return "always" if not text or text.lower() == "always" else text


def _card_scope(repo_root, rep):
    """A card may be narrower than the skill that owns it, never broader.

    `pov-switch` is the case. The skill and its audit card both carried
    `when: pov.mode != single`; the draft card carried `when: always`, so every single-POV novel
    ever written opened a card for a decision it does not have - one of twelve unconditional
    draft-card budget slots, spent on nothing. Nothing compared the two, because `_cards` checks
    that a card names a dispatcher and `kb` evaluates each `when:` on its own.
    """
    idx = kb.index(repo_root, refresh=True)
    for kind in ("draft-card", "audit-card"):
        for f in idx.by_type(kind):
            skill = idx.skills.get(f.owner)
            if skill is None:
                continue
            owner_when, card_when = _norm_when(skill.when), _norm_when(f.when)
            if owner_when != "always" and card_when == "always":
                rep.defect("card-scope",
                           "%s is `when: always` but `%s` it belongs to is `when: %s` - the card "
                           "fires for novels the skill is switched off for"
                           % (f.rel, f.owner, owner_when),
                           path=f.path, line=1)


def _commands(repo_root, commands, rep):
    if not commands:
        return
    have = set(commands)
    for rel, heading in (("CLAUDE.md", "mechanical toolkit"), ("scripts/README.md", "Commands")):
        path = os.path.join(repo_root, *rel.split("/"))
        if not os.path.isfile(path):
            continue
        text = mdio.read_text(path)
        section = mdio.section(text, heading) or text
        named = set()
        for table in mdio.parse_tables(section):
            for row in table.rows:
                m = re.match(r"^`(?:sw(?:\.py)?\s+)?([a-z]+)\b", row.first().strip())
                if m:
                    named.add(m.group(1))
        for name in sorted(named - have):
            rep.defect("command-doc", "%s documents `%s`, which sw.py does not implement"
                       % (rel, name), path=path)
        for name in sorted(have - named):
            rep.warn("command-doc", "sw.py implements `%s`, which %s does not document"
                     % (name, rel), path=path)


def _slash_commands(repo_root, rep):
    """CLAUDE.md section 7 against `.claude/commands/`, in both directions.

    The same wiring check `_commands` runs for sw.py subcommands. It exists because section 7 is
    the only place a user finds out a command is there: a command file with no entry is invisible,
    and an entry with no file is worse - it is an instruction to type something that does nothing.
    """
    d = os.path.join(repo_root, ".claude", "commands")
    claude = os.path.join(repo_root, "CLAUDE.md")
    if not os.path.isdir(d) or not os.path.isfile(claude):
        return
    have = set(f[:-3] for f in os.listdir(d) if f.endswith(".md"))
    section = mdio.section(mdio.read_text(claude), "Slash commands")
    if not section:
        rep.warn("slash-command", "CLAUDE.md has no slash-commands section to check "
                                  "`.claude/commands/` against", path=claude)
        return
    named = set(re.findall(r"`/([a-z][a-z0-9-]*)`", section))
    for name in sorted(named - have):
        rep.defect("slash-command", "CLAUDE.md section 7 lists `/%s`, which has no file in "
                                    ".claude/commands/" % name, path=claude)
    for name in sorted(have - named):
        rep.warn("slash-command", ".claude/commands/%s.md exists but CLAUDE.md section 7 does "
                                  "not list it - an undocumented command is an unused one"
                 % name, path=os.path.join(d, name + ".md"))
