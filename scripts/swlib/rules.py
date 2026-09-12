"""The searchable rule sets.

Every entry here comes from a skill file and cites it, so a hit is a named QC-gate failure
rather than a matter of taste. Anything requiring judgement is deliberately absent: this
module can only find strings, and pretending otherwise is how a checklist becomes a
substitute for the skill it summarises (revision-pass, "Before you start").
"""

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
CLAUDE_REGISTER = _compile([
    (r",\s+not\s+(?!to\b|be\b|have\b|only\b|just\b|yet\b)\w+", "X, not Y antithesis"),
    (r",\s+never\s+(?:a|an|the)\b", ", never a - antithesis"),
    (r"(?:^|(?<=[.!?]\s))Not\s+\w+\.", "`Not X.` fragment negation"),
    (r"\bA beat\.", "`A beat.` - a stage direction, not prose"),
    (r"\bthe kind of \w+ (?:that|who|a|an|you|one|people)\b", "the kind of X that"),
    (r"\bthe way (?:you|one|people)\b", "the way you/one/people - generalising aside"),
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
))
SITUATION_NOTE_CHECKS = frozenset((
    "group-scene",      # three or more speakers present - a category, not a defect
))

EVENT_MAX_WORDS = 14
EMDASH_RATE_WARN = 6.0          # per 1,000 words; run #2 chapter 1 ran 11.4
HOUSE_RATE_WARN = 6.0           # CLAUDE_REGISTER hits per 1,000 words...
HOUSE_MIN_HITS = 4              # ...and never on fewer hits than this: a rate needs a density
RATE_MIN_WORDS = 400            # below this, per-1,000-word rates are noise
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
