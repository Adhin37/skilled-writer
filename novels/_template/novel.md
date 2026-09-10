---
# ── IDENTITY ─────────────────────────────────────────────────────────────────
# Filled by title-craft, once, before the scaffold exists.
title: "Untitled"         # fanfic: the source work goes in the title line —
                          #   "Naruto: The New God of Shinobi"
title_alternates: []      # screened runners-up, kept for a rename at an arc boundary
slug: "untitled"          # kebab-case, 4-5 words. PERMANENT: the title may change,
                          #   the directory every path hangs off does not
genre: fantasy            # fantasy | scifi | fanfic
subgenre: ""              # progression | cultivation | space-opera | cyberpunk | isekai | ...
status: planning          # planning | drafting | hiatus | complete
language: en

# ── NARRATION ────────────────────────────────────────────────────────────────
narration:
  person: third-limited   # first | third-limited | third-objective
  tense: past             # past | present
  distance: close         # close | medium | cool   (see narrator-voice)
  interiority: high       # high | medium | low
  voice_notes: ""         # e.g. "dry, understated, short sentences under stress"

# ── STYLE TARGET ─────────────────────────────────────────────────────────────
# The single cheapest lever on register, and the only one that works by imitation rather
# than by prohibition. A model matches an example far more reliably than it obeys a rule,
# and the failure this exists to prevent is not slop — it is the model's own literary
# default filling the space where slop was banned: every sentence loaded, every scene
# closed on an aphorism, one temperature for the whole book.
#
# `read_like` names 1–2 real comparison works whose *register* this novel wants — not its
# plot. `sample` is optional: 3–6 sentences, either written by the user or drafted at init
# and approved, that the drafter re-reads each chapter and writes toward.
style:
  read_like: []           # e.g. ["Joe Abercrombie — The Blade Itself", "Mother of Learning"]
  sample: ""              # 3–6 sentences of target register. Optional but worth the tokens.
  avoid: ""               # registers this novel must not drift into

# ── POINT OF VIEW ────────────────────────────────────────────────────────────
pov:
  mode: single            # single | dual | rotating | ensemble   (see pov-switch)
  switch_granularity: chapter   # chapter | scene | never
  pov_characters: []      # ordered; first is primary
  label_switches: true    # print the POV name under the chapter title on switch
  antagonist_pov: never   # never | rare | scheduled

# ── MAIN CHARACTER ───────────────────────────────────────────────────────────
# Filled by mc-design. Run it before any other cast work.
mc:
  name: ""
  gender: ""              # any value; drives lead-interest defaults, nothing else
  pronouns: ""            # she/her | he/him | they/them — fixed for the whole novel
  intel_tier: 3           # 1 ordinary | 2 sharp | 3 smart | 4 brilliant | 5 genius
  competence_domains: []  # where the tier applies at full strength
  blind_spots: []         # where it does not — required, minimum two
  development_rate: 5     # MC is always 5 (see character-development)
  appearance_note: ""     # how the world reads them, in one line — not an inventory
  core_wound: ""
  core_want: ""           # what they pursue
  core_need: ""           # what they actually require, usually in conflict with want

  # origin: native | reincarnator | transmigrator | regressor | isekai | revenant
  origin: native
  # ── FOREKNOWLEDGE ── any MC who knows what happens next. See meta-knowledge.
  foreknowledge: ""       # what they know, in one sentence
  foreknowledge_grain: "" # episode-precise | major-beats | impressions | fandom-corrupted
  foreknowledge_first_win_ch: null  # where it first WORKS, on the page, legibly
  foreknowledge_fails_ch: null      # where it is first wrong. Must be > first_win_ch.
  foreknowledge_known_by: []        # who has guessed the MC knows things they shouldn't

  # the central advantage / golden finger — "none" is a valid, strong answer
  golden_finger: ""       # one sentence a reader could repeat
  gf_cost: ""             # what each use takes, measurable
  gf_limit: ""            # two sentences beginning "this can never…"
  gf_problem: ""          # the new problem it creates — mandatory
  gf_known_by: []         # who has guessed
  # where the MC starts relative to the world is scaling.start_tier, below.

  # form: set true if the MC does not start in their final body (reborn infant,
  # transmigrated, sealed, pre-evolution). Requires state/body.md. See mc-design.
  form_locked: false
  final_form_reached_ch: null

# ── POWER SCALING ────────────────────────────────────────────────────────────
# The distance between the MC and the opposition, and its shape over the whole book.
# Owned by power-scaling; the ledger is state/power.md. shape: none turns it all off.
scaling:
  shape: climb            # climb | inverted | regression | plateau-late | none
  tiers: 7                # size of the ladder in state/power.md section 2
  start_tier: 1           # where the MC starts. Must be <= 2 when shape: climb
  ceiling_tier: 6         # the highest tier the MC may reach
  endgame: ""             # the final opposition and its tier, in one line. Set at init.
  edge_worth: 1           # tiers the golden finger closes. 0 or 1. Never 2.
  edge_price: ""          # what closing that gap costs, every time
  substitute_tension: ""  # REQUIRED when shape: inverted - what the story runs on instead
  first_limit_by_ch: 8    # the advantage hits a wall. Must be > opening.first_win_by_ch
  gain_gap_min: 15        # minimum chapters between tier advances
  setup_lead: 3           # chapters a gain's mechanism must precede the gain
  flat_max: 12            # max chapters with no tier movement and no pressure variation
  trivial_per_arc: 2      # max confrontations at P <= -2 per arc
  boost_debt_due: 5       # chapters a boost's debt may go unpaid

# ── ROMANCE ──────────────────────────────────────────────────────────────────
# Filled by lead-interest, AFTER mc-design. Governed by content.romance below.
romance:
  configuration: undecided  # complementary | same-gender | other | none | undecided
  lead: ""                  # name of the primary love interest
  lead_gender: ""
  lead_introduced_ch: null

# ── CHAPTER ECONOMY ──────────────────────────────────────────────────────────
# A chapter is judged by what it DELIVERS, not by its length. See revision-pass Pass 9.
chapters:
  length_band: "1500-2600"  # a printer's note, not a quality gate. Flagged only outside.
  hook_required: true       # every chapter ends on a hook (see hook-and-pacing)
  arc_length: 25            # chapters per arc
  scenes_per_chapter: 2     # 1–3

# ── TEXT CHANNELS ────────────────────────────────────────────────────────────
# How the four kinds of text are marked on the page. Owned by narrator-voice.
# Set once, never varied. The full house style lives in bible/lexicon.md.
channels:
  speech: '"…"'             # anything said aloud
  thought: "'…'"            # DIRECT verbatim thought only — budget 1–3 per chapter
  meta: "[…]"               # system interfaces, in-world documents, narrative adjustments
  free_indirect: unmarked   # the default carrier of interiority — no marks at all

# ── THE OPENING ──────────────────────────────────────────────────────────────
# What the first chapters owe the reader, and when. See story-opening.
# The reader is oriented before they are threatened.
opening:
  promise: ""               # the blurb's central promise, in one sentence
  anchor_by_ch: 1           # reader knows what world, what place, what the MC wants
  contract_by_ch: 3         # subgenre unmistakable; reader can predict ch 10's pleasures
  promise_touched_by_ch: 3  # `promise` has reached the page, not just the blurb
  first_win_by_ch: 5        # the central advantage lands one legible win, before it fails
  stakes_ceiling: ""        # the worst thing allowed to happen before the frame is on the page

# ── THEME ────────────────────────────────────────────────────────────────────
# What the book argues, and the best argument against it. Both are for the author:
# the narrator never states either one. See revision-pass Pass 9d.
# Leave both empty for a book that is not arguing anything - the pass then skips.
theme:
  controlling_idea: ""      # one sentence. What this story turns out to be true about.
                            # "Loyalty you inherited is not loyalty you chose."
  counter_case: ""          # the strongest argument against it, which a character makes
                            # and wins with at least once. If nobody can, it is a sermon.
  tested_in_arcs: []        # arcs where a choice puts the idea under real pressure

# ── PLATFORM ─────────────────────────────────────────────────────────────────
# How the book is listed and released. See title-craft and hook-and-pacing.
platform:
  site: ""                  # royalroad | webnovel | scribblehub | other | none
  tags: []                  # 5-7. The primary genre tag from chapter 1; a secondary tag
                            # is added when that element actually becomes prominent.
  cadence: ""               # daily | 5x-week | 3x-week | 2x-week | weekly
  launch_stock: 0           # chapters banked before the first goes up
  cover_brief: ""           # one sentence an illustrator could work from

# ── WORLD CLOCK ──────────────────────────────────────────────────────────────
# How much the world runs on its own and reacts to the MC. See timeline-engine.
# The world track itself lives in plan/timeline.md.
timeline:
  reactivity: 3           # 1 inert | 2 ripples | 3 responsive | 4 adaptive | 5 predatory
  butterfly_horizon: 2    # how many arcs ahead a change may propagate before it is
                          # narrated as background rather than simulated
  escalation_ceiling: 1   # stake-rungs the world may climb per arc (conflict-engine ladder)
  crisis_cap: 3           # max simultaneous unresolved crises; never above 3

# ── ENDING CONTRACT ──────────────────────────────────────────────────────────
# The world is never allowed to make this unreachable. See timeline-engine.
ending:
  contract: ""            # what a satisfying ending looks like — IN THE USER'S OWN WORDS
  tone: hopeful           # hopeful | bittersweet | triumphant | quiet | earned-peace
  non_negotiables: []     # who must survive; what must be true at the end. Protected absolutely.

# ── CONTENT BOUNDARIES ───────────────────────────────────────────────────────
content:
  rating: teen            # teen | mature
  violence: moderate      # light | moderate | graphic
  profanity: light        # none | light | heavy
  romance: subplot        # none | subplot | central
  hard_limits: []         # anything the story must never depict

# ── OPTIONAL SKILLS ──────────────────────────────────────────────────────────
# Each key maps to .claude/skills/<key>/. `off` means the skill no-ops entirely.
optional:
  no-harem: on
  romance-arc: off
  combat-choreography: on
  litrpg-system: off
  mystery-clues: off
  comedy-levity: off
  grimdark-consequences: off
  slice-of-life-texture: off

# ── FANFIC ONLY ──────────────────────────────────────────────────────────────
fanfic:
  source: ""              # canon work
  canon_scope: ""         # which volumes/seasons are canon for this story
  divergence_point: ""    # the exact canon moment where this story departs
  ooc_budget: low         # low | medium | high (see fanfic-canon)
  oc_policy: supporting   # none | supporting | co-lead
  # how much the MC's mere existence perturbs canon — see timeline-engine
  footprint: self-insert  # self-insert | replaced-extra | oc-in-canon |
                          # canon-different-choices | canon-new-circumstance
---

# Premise

<!-- Three to five sentences. What the reader is promised. Written as a pitch, not a summary. -->

# Hook (platform blurb)

<!-- Written by title-craft, after the title and against it. 60–120 words. This is what appears
     on the novel's landing page. Anchor (who, where, what kind of world) before you threaten;
     one want and one concrete obstruction; ends on a question or a threat, never on a summary.
     At most two proper nouns beyond the MC. No rank ladder, no tag brackets, no stock phrases.
     Promise only what the first ten chapters deliver. -->

# Tone references

<!-- 2–4 works, with one line each on *what specifically* is borrowed. Not "like X" but
     "the interrogation-scene patience of X", "the cost-of-magic economy of Y". -->

# Themes

<!-- 1–3. Stated as a question the story argues with itself about, not as a noun. -->

# Ending target

<!-- Where this is going. One paragraph. May change; if it does, note the date and why. -->
