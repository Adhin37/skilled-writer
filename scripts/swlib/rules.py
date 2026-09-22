"""The searchable rule sets.

Every entry here comes from a skill file and cites it, so a hit is a named QC-gate failure
rather than a matter of taste. Anything requiring judgement is deliberately absent: this
module can only find strings, and pretending otherwise is how a checklist becomes a
substitute for the skill it summarises (revision-pass, "Before you start").
"""

import os
import re


def _compile(pairs):
    return [(re.compile(pat, re.I), label) for pat, label in pairs]


# mtl-detox Part 1, "Banned phrases". Target zero.
MTL_BANNED = _compile([
    (r"\bexpressions? changed drastically\b", "expression changed drastically"),
    (r"\bas expected of\b", "as expected of"),
    (r"\bunexpectedly\b", "unexpectedly"),
    (r"\bto (?:his|her|their|its) surprise\b", "to X's surprise"),
    (r"\bin the next (?:instant|moment)\b", "in the next instant/moment"),
    (r"\blittle did (?:he|she|they|we|i) know\b", "little did X know"),
    (r"\bcould ?n[o']t help but\b", "couldn't help but"),
    (r"\bcould not help but\b", "could not help but"),
    (r"\bflashed (?:through|across) (?:his|her|their) eyes\b", "X flashed through his eyes"),
    (r"\btrash!", "trash!"),
    (r"\byou dare\b", "you dare"),
    (r"\bcourt death\b", "court death"),
    (r"\bdo you know who i am\b", "do you know who I am"),
    (r"\bat (?:this|that) moment\b", "at this/that moment"),
    (r"\bat that time\b", "at that time"),
    (r"\bnot simple\b", "not simple (meaning formidable)"),
    (r"\bheart trembled\b", "heart trembled"),
    (r"\bscalp went numb\b", "scalp went numb"),
    (r"\bhow could this be possible\b", "how could this be possible"),
    (r"\b(?:was|were) speechless\b", "was/were speechless"),
])

# prose-quality, "The AI-default tells". Target zero.
AI_DEFAULT = _compile([
    (r"\ba mix of \w+ and\b", "a mix of X and Y"),
    (r"\ba testament to\b", "a testament to"),
    (r"\bsomething shifted in the air\b", "something shifted in the air"),
    (r"\bthe weight of .{1,30} settled\b", "the weight of X settled over"),
    (r"\ba moment that stretched\b", "a moment that stretched"),
    (r"\bcould ?n[o']t shake the feeling\b", "couldn't shake the feeling"),
    (r"\bfor the first time in a long time\b", "for the first time in a long time"),
    (r"\b(?:a )?silence stretched between\b", "a silence stretched between them"),
    (r"\bemotions warred\b", "emotions warred within her"),
    (r"\bair was thick with tension\b", "the air was thick with tension"),
    (r"\bchill ran down (?:his|her|their|the)\b", "a chill ran down his spine"),
    (r"\btime seemed to slow\b", "time seemed to slow"),
    (r"\bbreath (?:he|she|they) did ?n[o']t know\b", "a breath they didn't know they were holding"),
    (r"\bthis changes everything\b", "this changes everything"),
])

# prose-quality, "Filter verbs and telling". Remove unless perceiving is the point.
FILTER_VERBS = _compile([
    (r"\b(?:saw|heard|felt|noticed|realis?ed|watched|wondered|seemed to|decided to)\b",
     "filter verb"),
])

# voice-separation section 4 / prose-quality: the default gesture set.
GESTURES = _compile([
    (r"\bnodd(?:ed|ing)\b", "nodded"),
    (r"\bshrugg(?:ed|ing)\b", "shrugged"),
    (r"\bsigh(?:ed|ing)\b", "sighed"),
    (r"\braised? (?:an|his|her|their) eyebrows?\b", "raised an eyebrow"),
    (r"\bcrossed (?:his|her|their) arms\b", "crossed their arms"),
    (r"\blet out a (?:breath|sigh)\b", "let out a breath"),
    (r"\bran a hand through (?:his|her|their) hair\b", "ran a hand through their hair"),
    (r"\bclenched (?:his|her|their) jaw\b", "clenched their jaw"),
    (r"\bsmiled slightly\b", "smiled slightly"),
])

# prose-quality, "Word-level".
WEASEL = _compile([
    (r"\bvery\b", "very"),
    (r"\breally\b", "really"),
    (r"\bquite\b", "quite"),
    (r"\bsomewhat\b", "somewhat"),
    (r"\brather\b(?! than)", "rather"),
    (r"\bslightly\b", "slightly"),
    (r"\bsuddenly\b", "suddenly"),
    (r"\b(?:began|started|proceeded) to\b", "began to / started to"),
])

# revision-pass Pass 10: nothing else in a prose body is markup.
STRAY_MARKUP = _compile([
    (r"^\s{0,3}#{1,6}\s", "markdown heading in prose body"),
    (r"^\s{0,3}[-*+]\s+\S", "list bullet in prose body"),
    (r"^\s{0,3}\d+\.\s+\S", "numbered list in prose body"),
    (r"\*\*[^*\n]+\*\*", "bold in prose body"),
    # Benchmark run #2, F3: there was a rule for bold and none for italics, so an italicised
    # direct thought - the exact hard-rule-7 violation the four channels exist to prevent -
    # passed silently. The look-arounds keep `**bold**` on the rule above, leave `3 * 4` and
    # snake_case identifiers alone, and never reach `* * *` (skipped as a scene break first).
    (r"(?<!\*)\*(?!\s)[^*\n]+(?<!\s)\*(?!\*)", "italics in prose body"),
    (r"(?<![\w_])_(?!\s)[^_\n]+(?<!\s)_(?![\w_])", "italics in prose body"),
    (r"\[[^\]\n]*\]\([^)\n]*\)", "markdown link in prose body"),
    (r"^\s{0,3}>\s", "blockquote in prose body"),
    (r"^\s{0,3}```", "code fence in prose body"),
])

# story-craft: a turn reported instead of played. The signature is a plot event inside a
# past-perfect clause or a span of compressed time. Ordinary past-perfect is how English orders two
# past events and is NOT listed here - only constructions that carry an event across elapsed time.
SUMMARY_MARKERS = _compile([
    (r"\bhad (?:spent|made|been making|arranged|built|learned|practi[sc]ed|trained|"
     r"prepared|planned|managed|persuaded|convinced|negotiated)\b", "had <verb> - an event reported"),
    (r"\bover the (?:next|following|past|course of)\b", "over the next - time compressed"),
    (r"\b(?:weeks|months|days|years) (?:passed|later|of)\b", "elapsed time"),
    (r"\bby the time\b", "by the time - the event happened offstage"),
    (r"\b(?:every|each) (?:day|night|morning|week) for\b", "a routine reported"),
    (r"\b(?:four|five|six|seven|eight|nine|ten|dozens? of|several) times in\b",
     "repeated attempts reported"),
    (r"\bin the (?:weeks|months|days) (?:that|after|before|since)\b", "time compressed"),
])

# prose-quality, "The house style". The tells this model produces when the MTL cut-list is
# already clean - measured off benchmark run #2, whose five chapters carried 62 em-dashes and 18
# antitheses in 7,302 words and read as machine-made without tripping a single banned phrase.
#
# Every hit here is a NOTE, never a defect, and that is deliberate. Each construction below is
# good writing in isolation; the disease is density, so the gate is the aggregate rate in
# `_house_style`, not any one line. A rule that defects on ", not " would ban a legitimate
# sentence and teach the drafter to write around the checker instead of varying its register.
# The fragment negation, widened after benchmark run #5. The original `Not\s+\w+\.` matched
# exactly one shape - `Not yet.` - and nothing longer, never covered `No`, and required the
# sentence to open after `[.!?]` plus one space, which a paragraph break is not. Run #5 wrote
# eleven of these across three chapters and the detector caught none, so what the drafter cleared
# was the measurement. Three things keep the widening honest:
#   * it stays a FRAGMENT test - a span carrying a finite auxiliary or copula is a sentence that
#     happens to begin with a negator, and the lookahead refuses it;
#   * no commas, so `No, he said.` and `Not knowing what else to do, he waited.` stay out;
#   * five words at most, because past that a negation is doing work rather than posturing;
#   * a sentence starts at `[.!?]` or a PARAGRAPH break, never at any newline - the sample novel
#     is hard-wrapped and `she had\nnot stopped moving since the bell.` is not a fragment.
# Widening a regex adds no prohibition to any card, which is why this is the cheap half of the
# fix - and why CLAUDE.md section 5's thesis stands: the next register fills the hole anyway.
_FRAGMENT_NEGATION = (
    r"(?:^|(?<=[.!?])|(?<=\n\n))[\"“”\s]*(?:Not|No)\b"
    r"(?![^.!?\n]*\b(?:is|are|was|were|am|be|been|being|has|have|had|do|does|did|will|"
    r"would|can|could|shall|should|may|might|must)\b)"
    r"(?:\s+[\w'’-]+){0,5}\s*[.!?]"
)

CLAUDE_REGISTER = _compile([
    (r",\s+not\s+(?!to\b|be\b|have\b|only\b|just\b|yet\b)\w+", "X, not Y antithesis"),
    (r",\s+never\s+(?:a|an|the)\b", ", never a - antithesis"),
    (_FRAGMENT_NEGATION, "`Not X.` fragment negation"),
    (r"\bA beat\.", "`A beat.` - a stage direction, not prose"),
    (r"\bthe kind of \w+ (?:that|who|a|an|you|one|people)\b", "the kind of X that"),
    (r"\bthe way (?:you|one|people|he|she|they|it|we|i|an?|the|his|her|their|its|every|"
     r"(?-i:[A-Z][a-z]+))\b", "the way X does Y - generalising aside"),
    (r"\bnot (?:because|out of|from)\b[^.;]{2,40}\bbut (?:because|out of|from)\b",
     "not because X but because Y"),
    (r"\bfor (?:exactly )?as long as (?:an?|the) \w+ would\b", "for exactly as long as X would"),
    (r"\bsomething (?:in|about) (?:his|her|their|the) (?:face|eyes|voice|expression)\b",
     "something in her face"),
    (r"\bthe same \w+ (?:register|voice|tone|hand)\b", "the same flat register - a repeated tag"),
    (r"\b(?:turning|holding|carrying|weighing|folding)\b[^.]{0,40}\b(?:years?|arithmetic|"
     r"silence|grief|doubt|history|guilt|memory|arithmetic)\b[^.]{0,25}\bin (?:his|her|their) "
     r"hands\b", "an abstract noun handled as an object"),
])

# The abstract-state nouns that turn `event:` back into `delivers:`. An event is something a
# reader could retell; "trust deepens" is not an event, it is a description of an event's effect.
EVENT_ABSTRACT = _compile([
    (r"\b(?:trust|proximity|attention|awareness|understanding|relationship|tension|doubt|"
     r"realisation|realization|suspicion|connection|intimacy|rapport|resolve|acceptance|"
     r"dynamic|bond)\b", "an abstract state, not an event"),
    (r"\b(?:becomes|is now|has become|begins to)\b", "a state change, not an event"),
])

# hook-and-pacing: the declared temperature of a chapter, and the shape of its last beat.
# Set at plan time in plan/chapters.md, checked distributionally by `sw arc` - never scored
# per chapter, because a number that decides whether one chapter ships gets optimised
# (docs/design-notes.md, "Why the gate is delivery, not length").
TEMPS = ("fast", "tense", "loud", "warm", "funny", "bleak", "procedural", "quiet")
# The eight are hook-and-pacing's own taxonomy, verbatim. Inventing a second vocabulary here
# would give the skill and the script different words for the same thing, and the skill's list
# was already thought through - including the rule that `cliff` is rationed to once per 8-10
# chapters, which this module cannot check and does not try to.
HOOKTYPES = ("reveal", "arrival", "decision", "question", "threat", "reversal", "cliff", "quiet")

# --------------------------------------------------------------- the note tier
#
# Note-level checks come in two kinds, and only one of them is a habit.
#
# A HABIT note fires on something that is fine once and is a fingerprint at density - one
# antithesis is good writing, one filter verb is nothing, a scene where nobody interrupts is a
# scene. That is exactly why each is a note per chapter, and exactly why a *recurrence* is a
# finding worth putting in front of the next draft. Benchmark run #4 shipped five of six
# chapters with `house-style` firing and the drafter was never told once.
#
# A SITUATION note reports a fact about what the chapter contains, so the reader can apply the
# right craft - `group-scene` names a scene with three or more speakers and its own message
# ends "Read it and discount it". A book with group scenes in every chapter has group scenes.
# It is not a habit and it must never reach the WATCH row, which says what the gate keeps
# having to fix.
#
# The habit set is an allowlist on purpose: a new note check is a situation note until somebody
# decides otherwise, and `tests/test_cmds.py` fails if a note check appears in neither set.
HABIT_NOTE_CHECKS = frozenset((
    "house-style",      # the antithesis and the rest of the one-attitude narrator
    "filter-verb",      # she felt / she saw / she heard
    "weasel",           # hedges and intensifiers
    "texture",          # the dialogue floors: no interruption, no contraction, over-long turns
    "pacing",           # reported-event constructions, and summarising toward the scene
    "thought-budget",   # the floor only - the ceiling is a defect and never reaches here
    "speech-share",     # the target band only - the floor is still a warn, and a habit of
                        # sitting under the band is what the window defect is for
    "thought-person",   # narration in thought marks - one is a slip, a run of them is the
                        # drafter using the channel as emphasis
    "negation-density", # the density only - one negative construction is a good sentence, and
                        # a narrator who defines everything by what it isn't is a habit
))
SITUATION_NOTE_CHECKS = frozenset((
    "group-scene",      # three or more speakers present - a category, not a defect
))

# narrator-voice, the four channels. A direct thought is the POV character's own voice in their
# own present tense; free indirect discourse is the narrator's voice carrying the character's
# slant, and it is the default carrier of interiority precisely because it does not need marks.
# Rule 7 was enforced on COUNT only, so benchmark run #5 put `'He'd made more of it than it was.'`
# inside thought marks in a third-person past novel - narration wearing the marks - and lint
# counted it as one of the legal one to three. That is rule 9's silence clause in a third place:
# a rule checked on one axis is satisfied on that axis.
#
# The screen is deliberately narrow, because the interesting half of this is a judgement.
# `'She's lying.'` is a perfectly good thought about somebody else, so a present-tense marker
# ends the check; `'I should have known.'` is the POV character's own voice, so a first- or
# second-person pronoun ends it too. What is left is a span with no speaker in it, in the
# narrator's tense - and a possessive `'s` reads as present here, which errs toward silence.
FIRST_SECOND_PERSON = re.compile(
    r"\b(?:i|me|my|mine|myself|we|us|our|ours|ourselves|you|your|yours|yourself|yourselves)\b"
    r"|\b(?:i|we|you)['’](?:m|re|ve|ll|d)\b", re.I)
PRESENT_MARKERS = re.compile(
    r"\b(?:is|are|am|has|have|do|does|can|shall|will)\b|['’](?:s|re|m|ve|ll)\b", re.I)
PAST_MARKERS = re.compile(
    r"\b(?:was|were|had|been|did|would|could|should)\b|['’]d\b", re.I)

# ------------------------------------------------------------------ thread ids
# `plot-threads` owns the format and documents it as `T01`, `T02`. Five commands parsed it with
# their own copy of `T\d+`, so benchmark run #5 - which numbered its threads `TH01` - had every
# thread check in `sw state` go quiet while `sw status` went on counting nine open threads from
# the same file. A check that falls silent reads exactly like a check that passed, which is the
# failure this repo keeps re-learning. One pattern, read loosely; `THREAD_ID_CANON` is what
# `cmd_state` warns against so the drift announces itself instead of disabling the suite.
THREAD_ID = re.compile(r"^T[A-Z]{0,3}\d+$")
THREAD_ID_CANON = re.compile(r"^T\d+$")
THREAD_ID_IN_TEXT = re.compile(r"[~^vx]?\b(T[A-Z]{0,3}\d+)\b")
THREAD_OP_IN_TEXT = re.compile(r"([~^vx])(T[A-Z]{0,3}\d+)\b")

# prose-quality "Range before polish", and run #5's cold read, which counted 235 of these in
# 7,700 words and called it a narrator who defines everything by what it isn't: things arriving
# as "not agreement", "no answer at all", "which was also not the answer". The measure lived as a
# grep recipe in the review tree and could only ever be run by hand on a finished novel; here it
# recurs across chapters and reaches the WATCH row.
#
# One instance is good writing - defining by exclusion is a real move - so this is a NOTE and the
# only thing that carries weight is the density. Never promote it: a per-chapter number that
# decides whether a chapter ships is a number the next chapter gets written toward, and this repo
# has done that three times already (word count, dialogue share, SPEECH_TARGET_LOW).
NEGATION_WORDS = re.compile(
    r"\b(?:not|never|nothing|nobody|none|nor|neither|no|"
    r"cannot|can't|won't|wasn't|isn't|didn't|doesn't|don't|hadn't|hasn't|haven't|"
    r"wouldn't|couldn't|shouldn't|aren't|weren't)\b", re.I)

EVENT_MAX_WORDS = 14
EMDASH_RATE_WARN = 6.0          # per 1,000 words; run #2 chapter 1 ran 11.4
HOUSE_RATE_WARN = 6.0           # CLAUDE_REGISTER hits per 1,000 words...
HOUSE_MIN_HITS = 4              # ...and never on fewer hits than this: a rate needs a density
RATE_MIN_WORDS = 400            # below this, per-1,000-word rates are noise
NEGATION_RATE_NOTE = 22.0       # negations per 1,000 NARRATION words. Calibrated on run #5,
NEGATION_MIN_HITS = 12          # ...which ran 20.9-28.1 across five chapters and was read cold
                                # as "a narrator who defines everything by what it isn't". This
                                # fires on four of those five; chapter 5, the one the benchmark
                                # singled out for the one warm beat that landed, sits under it
CLOSER_SHORT_WORDS = 12         # a chapter-ending line this short, with nobody speaking
CLOSER_WINDOW = 5               # ...in this many consecutive chapters...
CLOSER_WINDOW_MAX = 2           # ...more than this often is a tic, not a choice
TEMP_RUN_MAX = 2                # same temperature in a row
HOOK_WINDOW = 5                 # rolling window for hooktype repeats
HOOK_WINDOW_MAX = 2
ARC_MIN_DISTINCT = 4            # distinct temps and hooktypes required across an arc
DECLINE_RUN = 3                 # consecutive shrinking chapters before it is a signal


# The three module registries that used to live here - GENRE_MODULES, OPTIONAL_MODULES and
# CONFIG_GATED_MODULES - are gone. They were a second copy of CLAUDE.md section 3 maintained by
# hand, and all three answered one question: is this skill live for this novel? Each skill now
# answers it in its own frontmatter, as `metadata.when`, and `swlib/kb.py` reads it. The reason
# it had to be a copy at all was that the skill layer had no machine-readable form; it has one.


# The frontmatter revision-pass Pass 10 requires.
REQUIRED_FRONTMATTER = ["number", "title", "pov", "arc", "event", "delivers", "wordcount",
                        "status"]

# continuity-summary: CCS lines that are required on every block.
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

REQUIRED_CCS = ["dlv", "ev", "chg", "kno", "thr", "obj", "hook"]

# Raised 15 -> 17 when `cand>` and `z4>` arrived. Every block of the heaviest live novel sat at
# exactly 15, so the two new lines needed the room. The cap exists to keep a block compressed
# enough that five of them are cheap in a read-set, and it still does: a full block is header
# plus at most sixteen keys, and most chapters write far fewer.
CCS_MAX_LINES = 17
THOUGHT_FLOOR = 1               # ...and a floor, because only the ceiling was ever checked
THOUGHT_BUDGET = 3
SPEECH_FLOOR = 10.0
SPEECH_WINDOW = 5
SPEECH_TARGET_LOW = 25.0
SPEECH_TARGET_HIGH = 40.0

# Words in a single spoken TURN (every `"…"` span in one paragraph) past which the line has
# stopped being talk. Benchmark run #3: a six-year-old delivered a 73-word turn and her mother a
# 107-word one, both inside a texture line that read as healthy, because length was measured per
# span and a dialogue tag split the turn in two. `dialogue-voice` owns the judgement - a deliberate
# monologue is a real thing - so this prints a note naming the turn and gates nothing.
TURN_CEILING = 45

# A repeated CONSTRUCTION, caught without a phrase list. Benchmark run #3: the redraft removed the
# `the way a person …` simile (11 uses in one chapter) and grew `its own kind of …` in the same
# pass - 4 uses in the same chapter, 7 across five. That is CLAUDE.md section 5's thesis happening
# live: ban a tic and the model's default register fills the hole with another one, so no list of
# banned phrases can ever be finished. A word-length window of 4 at 3 occurrences found the tic
# with no false positives on this novel and two genuine ones on run #2's.
ECHO_WINDOW = 4                 # words per phrase compared
ECHO_MIN = 3                    # occurrences in ONE chapter before it is worth a look
ECHO_WARN = 4                   # ...and past this it is the chapter's signature, so it
                                # rises to a warn and reaches the next chapter's WATCH row


def scan(text, ruleset, offset_of=None):
    """Yield (offset, matched_text, label) for every rule hit in text."""
    for rx, label in ruleset:
        for m in rx.finditer(text):
            yield m.start(), m.group(0), label


# How many UNCONDITIONAL cards the dispatchers may carry - the cards every novel pays for,
# every chapter, whatever it is about.
#
# The corpus reached 118 files and 3,942 negations with no number anywhere that anybody had to
# answer for, and the expansion that measured it had itself added ten audit cards without
# anything objecting. `docs/creative-latitude.md` has the arithmetic: nineteen draft cards and
# twenty-three audit cards resolved for one chapter of a live novel - 16,359 words of
# instruction and 596 prohibitions before a line of story state.
#
# The budget is not a claim that the twelfth card is worth more than the thirteenth. It is a
# forcing function: past it a new rule has to MERGE with the card that already owns its
# neighbourhood rather than open a new file, which is the discipline that was missing. Enforced
# by `sw health` against the corpus, never against a novel and never against a chapter.
CARD_BUDGET = {"draft-card": 12, "audit-card": 15}

# And the same bound on WORDS, which is the number that actually costs a drafter anything.
#
# `CARD_BUDGET` bounds the count, and the merges it forced moved four draft cards and three
# audit cards into the card that already owned their neighbourhood. The count fell 42 -> 35 and
# the instruction load went 16,359 -> 16,550 words, because a merged card costs a drafter
# exactly what its two halves cost separately and nothing, anywhere, objected. That is the hole
# this closes: the ratchet was on the wrong number.
#
# Raised 2026-09-13: 6400 -> 7600 and 6800 -> 8000. It had been set a hair above the measured
# figure, and the hair turned out to be one word - the draft cards stood at 6399/6400 and the
# audit cards at 6775/6800, so a wording fix had to be paid for with a cut somewhere else and
# the ceiling was bounding rephrasing rather than growth. The harness now compresses context by
# default, subagents included, so what a card costs to CARRY stopped being scarce. What a
# drafter holds open at once did not, which is why `CARD_BUDGET` above does not move.
#
# The raise is sized as ONE WORKED EXAMPLE PER CARD, ~110 words, and that is what it is for.
# `CLAUDE.md` section 8 makes the spend asymmetric: length spent on an example is a better card,
# length spent on another prohibition is the failure this was built against. The number to watch
# on a card is its count of things you must not do, never its word count.
#
# Still a CEILING to be lowered, never a target to fill: the maintenance task is to cut toward
# it and then lower it again. `docs/creative-latitude.md` item 6 is the standing work.
#
# What it does NOT license is cutting advice to hit a number. The two obvious cuts named in that
# plan are already spent - `sw health`'s duplication rule means there is not one checkbox text
# shared between any two skills, and the boxes that merely restated a `sw lint` finding were
# taken in the same pass. What is left is prose, and prose is where the advice lives.
CARD_WORD_BUDGET = {"draft-card": 7600, "audit-card": 8000}


# The counter-check to every budget above, and the only number in this file that fails DOWNWARD.
#
# `CARD_BUDGET` and `CARD_WORD_BUDGET` are ceilings, and a ceiling cannot catch a corpus that
# vanished: `kb.Index._build()` skips any directory without a `SKILL.md`, so a half-finished
# move returns an EMPTY index and every check in the toolkit passes at zero. `sw health` reports
# clean, `sw load` prints a row of zeros, both budgets are satisfied. A clean run is exactly what
# a broken index produces, which is the worst shape a failure can take.
#
# So: the minimum the corpus may shrink to before something is wrong. Set well under today's
# figures (44 / 26 / 29 / 59) because this is a tripwire for a corpus that DISAPPEARED, not a
# ratchet on one that shrank - losing six draft cards still clears twenty, and the detector for
# that is the `sw load` word total, which moves the moment a file stops being reachable.
CORPUS_FLOOR = {"skill": 40, "draft-card": 20, "audit-card": 20, "reference": 50}


def corpus_floor_applies(repo_root):
    """Whether `CORPUS_FLOOR` binds this directory.

    The floor is measured against THIS toolkit's corpus, not against any directory that happens
    to hold a `.claude/skills/`. It is anchored on the file that declares it: a repo shipping
    `scripts/swlib/rules.py` is the repo these numbers came from. A test fixture with two skills
    in it is not, and a floor that fired on fixtures would be switched off inside a week.
    """
    return os.path.isfile(os.path.join(repo_root, "scripts", "swlib", "rules.py"))


# Which `## N.` sections of `CLAUDE.md` a role is NOT bound by. Everything else is included, and
# the asymmetry is deliberate: a rule wrongly carried costs a few hundred words of a role's
# attention, and one wrongly dropped costs a chapter. So a section added next month reaches every
# role until somebody writes it into this table on purpose.
#
#   7   the slash commands - the user's interface to the coordinator, not a role's own procedure
#   8   how to author a skill file - the maintainer's job. A drafter that reads it may try to do it
#  10   the role table and the guards - each agent's own scope is in its agent file, stated once
#
# Measured before it was built: this drops 1,574 of 7,583 words for each of the three. It is not
# sold as a token saving - see `CARD_WORD_BUDGET` for why this repo does not buy those - but as
# three fewer things competing for attention with the chapter, two of which describe work the
# role does not do.
CONTRACT_EXCLUDES = {
    "draft": ("7", "8", "10"),
    "gate": ("7", "8", "10"),
    "design": ("7", "8", "10"),
}
