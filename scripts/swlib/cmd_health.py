"""`sw health` - does the toolkit itself still hang together?

Every check here used to exist only as an assertion inside `tests/`, which means somebody who
clones the repo, edits a skill and breaks a pointer finds out by reading a stack trace, if at
all. These are the same checks as a report. `tests/test_template_wiring.py` imports the tables
below and asserts this command finds nothing, so the two cannot drift apart.

It audits the repo, never a novel. Nothing here reads a chapter.
"""

import os
import re

from . import kb, mdio, rules
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
    ("plan_rows",       ("plan", "chapters.md"),             ("#", "title", "delivers")),
    ("voice_rows",      ("bible", "cast", "_voices.md"),     ("character", "intel", "artic",
                                                              "wit")),
    ("competence_rows", ("bible", "cast", "_competence.md"), ("character", "domain", "level")),
]

# Every section a parser slices out by heading text. A renamed heading drops it silently.
SECTION_LOOKUPS = [
    (("bible", "cast", "_voices.md"),    "POV THOUGHT"),
    (("bible", "cast", "_voices.md"),    "MIRROR"),
    (("plan", "timeline.md"),            "SCHEDULED FOR THIS ARC"),
    (("state", "body.md"),               "CURRENT FORM"),
    (("state", "body.md"),               "ABSOLUTE LIMITS"),
    (("state", "foreknowledge.md"),      "THE GRAIN"),
    (("state", "foreknowledge.md"),      "THE INVENTORY"),
    (("state", "foreknowledge.md"),      "THE SPEND LOG"),
    (("state", "power.md"),              "CURRENT STANDING"),
    (("state", "power.md"),              "THE LADDER"),
    (("state", "power.md"),              "ACTIVE BOOSTS"),
    (("state", "continuity.md"),         "BOOK DIGEST"),
    (("state", "continuity.md"),         "ARC DIGEST"),
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
    return os.path.join(repo_root, ".claude", "skills")


def skill_names(repo_root):
    d = skills_dir(repo_root)
    if not os.path.isdir(d):
        return []
    return sorted(n for n in os.listdir(d)
                  if os.path.isdir(os.path.join(d, n)) and not n.startswith("."))


def run(repo_root, commands=None):
    """`commands` is the dispatcher's own subcommand list, passed in to avoid importing sw.py."""
    rep = Report("health - %s" % os.path.basename(os.path.abspath(repo_root)))
    names = skill_names(repo_root)
    if not names:
        rep.defect("skills", "no .claude/skills/ directory under %s"
                   % os.path.abspath(repo_root).replace(os.sep, "/"))
        return rep

    _skills(repo_root, names, rep)
    _registry(repo_root, names, rep)
    _template(repo_root, rep)
    _commands(repo_root, commands, rep)
    _slash_commands(repo_root, rep)
    _uncited(repo_root, names, _owns_map(repo_root, names, rep), rep)
    _overlap(repo_root, names, rep)
    _kb(repo_root, rep)
    _force(repo_root, rep)
    _card_budget(repo_root, rep)
    rep.info("scope", [
        "   %d skills, %d template accessors, %d template sections checked"
        % (len(names), len(TABLE_ACCESSORS), len(SECTION_LOOKUPS)),
        "   This is wiring only. It says nothing about whether a skill's advice is any good.",
    ])
    return rep


# --------------------------------------------------------------------- skills

def _skills(repo_root, names, rep):
    root = skills_dir(repo_root)
    bodies = {}
    for name in names:
        path = os.path.join(root, name, "SKILL.md")
        if not os.path.isfile(path):
            rep.defect("skill-frontmatter", "%s/ has no SKILL.md - the skill cannot load" % name,
                       path=path)
            continue
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

    _references(root, names, bodies, rep)
    _line_citations(root, names, rep)


def _references(root, names, bodies, rep):
    for name in names:
        refdir = os.path.join(root, name, "references")
        body = bodies.get(name, "")
        present = []
        if os.path.isdir(refdir):
            present = sorted(f for f in os.listdir(refdir) if f.endswith(".md"))

        for fname in present:
            owner = CARD_OWNERS.get(fname)
            if owner:
                token = "%s/references/%s" % (name, fname)
                if owner not in bodies:
                    rep.defect("skill-card", "%s exists but its dispatcher `%s` is missing"
                               % (token, owner))
                continue
            if ("references/%s" % fname) not in body:
                rep.defect("skill-reference",
                           "%s/references/%s is never cited by its own SKILL.md - a pointer "
                           "without a trigger is not read" % (name, fname),
                           path=os.path.join(refdir, fname))

        # A citation is `references/x.md` for this skill's own, or `other/references/x.md` for
        # another skill's. Reading the tail alone turns every cross-skill pointer into a false
        # "does not exist" against the citing skill.
        cites = re.findall(r"(?:([a-z][a-z0-9-]*)/)?references/([A-Za-z0-9._-]+\.md)", body)
        for owner, cited in sorted(set(cites)):
            target_skill = owner or name
            path = os.path.join(root, target_skill, "references", cited)
            if os.path.isfile(path):
                continue
            where = ("%s/references/%s" % (owner, cited)) if owner else ("references/%s" % cited)
            rep.defect("skill-reference",
                       "%s/SKILL.md cites %s, which does not exist" % (name, where),
                       path=os.path.join(root, name, "SKILL.md"))


def _line_citations(root, names, rep):
    for name in names:
        for dirpath, _dirs, files in os.walk(os.path.join(root, name)):
            for fname in sorted(f for f in files if f.endswith(".md")):
                path = os.path.join(dirpath, fname)
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

    _orphan_keys(repo_root, novel, rep)


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
    root = skills_dir(repo_root)
    raw, words = {}, {}
    for name in names:
        raw[name] = _skill_corpus(root, name)
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
                         path=os.path.join(root, name, "SKILL.md"))


def _skill_corpus(root, name):
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
    for sub, _dirs, files in os.walk(os.path.join(root, name)):
        for f in sorted(files):
            if f.endswith(".md"):
                _fm, body = mdio.split_frontmatter(mdio.read_text(os.path.join(sub, f)))
                parts.append(body)
    return "\n".join(parts)


def _overlap(repo_root, names, rep):
    """Long passages carried by two skills at once.

    It finds text, not meaning, so it cannot see a paraphrase - but every duplicate this repo
    actually grew was copied, and a copy is what drifts. Citing a concept is free: a code span is
    stripped before comparison, so pointing at an owner never trips this.
    """
    root = skills_dir(repo_root)
    shingles = {}
    for name in names:
        shingles[name] = _runs(_normalise(_skill_corpus(root, name)))

    for i, a in enumerate(names):
        for b in names[i + 1:]:
            both = shingles.get(a, set()) & shingles.get(b, set())
            if len(both) > OVERLAP_MAX:
                sample = sorted(both)[0]
                rep.warn("skill-overlap", "%s and %s share %d passages of %d+ words - one of them "
                                          "owns this and the other should cite it. e.g. \"%s...\""
                         % (a, b, len(both), OVERLAP_RUN, sample[:70]),
                         path=os.path.join(root, a, "SKILL.md"))


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
        live = sorted(f.owner for f in idx.by_type(kind)
                      if not f.when or f.when.strip() == "always")
        if len(live) > cap:
            rep.defect("card-budget",
                       "%d unconditional %ss against a budget of %d (%s) - merge one into the "
                       "card that already owns its neighbourhood; a new file is not an option "
                       "past the budget"
                       % (len(live), kind, cap, ", ".join(live)))


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
