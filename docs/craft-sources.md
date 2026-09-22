# Craft sources

What was researched for this toolkit, where it came from, and which rule it produced. Provenance
only — nothing here is loaded at runtime. The runtime knowledge lives in
`roles/draft/story-craft.*`, because a file no dispatcher names never enters context
(benchmark finding 9).

Researched 2026-09-09, prompted by a reader report that the generated novel "goes fast to the
finish line", with no build-up of world or character. Extended 2026-09-13 with the world half.
Extended again 2026-09-22 with **why readers stay** — prompted by a report that readers were
dropping the novels after two chapters, and by the observation that neither earlier pass contains
a single source on character appeal, humour or emotional payoff.

## The finding that shaped everything

Machine-written fiction fails pacing **in one direction**: it gives the important beat to summary.
That asymmetry is why the rules added here guard one direction and leave over-elaboration to
`world-texture`'s existing description budget.

| source | what it established | what it produced |
|---|---|---|
| [CONCOCT, arXiv:2311.04459](https://arxiv.org/abs/2311.04459) | LLM story systems "gloss over important events or over-elaborate on insignificant details"; pacing is the distribution of **concrete detail** across events | `story-craft` §The one decision; the past-perfect tell; `CLAUDE.md` §4 rule 4 corollary |
| [arXiv:2407.13248](https://arxiv.org/pdf/2407.13248) | Models pace *setup* correctly but rush the major setback and climax; human stories carry higher suspense, the gap widening from the midpoint | `roles/design/story-craft.why-ai-rushes.md`; the note that the failure concentrates in the second half, not the opening |
| Dwight Swain, *Techniques of the Selling Writer* (1965) · [Wikipedia](https://en.wikipedia.org/wiki/Scene_and_sequel) · [Ingermanson](https://www.advancedfictionwriting.com/articles/writing-the-perfect-scene/) | scene = goal/conflict/disaster; sequel = reaction/dilemma/decision; MRUs; **sequel length is the pacing dial** | `roles/shared/story-craft.scene-and-summary.md`; the follow-through note in the draft card |
| [Center for Fiction](https://centerforfiction.org/writing-tools/scenes-summary/) · [Write It Scared](https://www.writeitscared.co/blog-3/narrativedistance) | scene vs summary allocation; narrative distance; pull to scene as stakes rise | `roles/shared/story-craft.scene-and-summary.md` §When summary is right |
| [Go Teen Writers](https://goteenwriters.com/2013/07/30/try-fail-cycles-the-yes-but-or-no-and-method-to-creating-plot-twists/) · [Karen Woodward](https://blog.karenwoodward.org/2014/04/parts-of-story-try-fail-cycles.html) | try/fail cycles; "yes, but" / "no, and"; failure is what makes a win feel earned | `roles/design/story-craft.story-structure.md` §Try/fail; `CLAUDE.md` §5 "a win costs a failure the reader watched" |
| [StudioBinder](https://www.studiobinder.com/blog/three-act-structure/) · [Helping Writers Become Authors](https://www.helpingwritersbecomeauthors.com/understanding-the-normal-world-of-a-storys-first-act/) | 25/50/25 as function not target; the ordinary world before the inciting incident | `roles/design/story-craft.story-structure.md` §Three acts; `chapter-plan`'s arc-1 shape table |
| [Royal Road forums: retention](https://www.royalroad.com/forums/thread/111699) · [slow burn](https://www.royalroad.com/forums/thread/143611) · [tension pacing](https://www.royalroad.com/forums/thread/131403) | ~50% drop after chapter 1; three pacing layers (chapter/arc/novel); slow burn works on *deposits*, not on lower density | `roles/design/story-craft.serial-pacing.md`; the "build-up is deposits" note in `roles/shared/hook-and-pacing.arc-rhythm.md` |

## The contradictions this surfaced in our own rules

Researching build-up showed the toolkit was arguing against itself. All six are now resolved; the
detail is in each skill.

| # | was | now |
|---|---|---|
| C1 | `CLAUDE.md` §5 "Enter scenes in motion", unconditional, with zero lines protecting orientation | qualified: it bans a *mode of telling*, never the build-up |
| C2 | `story-opening` §3 gave chapter 1 danger "none" while its own `chapter-one.md` demanded something already wrong plus a cliffhanger | "low external, full internal", plus a new §Orientation is not build-up |
| C3 | `chapter-plan` switched its only shape table off for arc 1 rows 1–5 and replaced it with four deadlines and no temperature | rows 1–5 now carry a temperature and a scene-intent column |
| C4 | `chapter-one.md` gave world ~35% of chapter 1; `world-texture` capped description at ≤8% | stated: 35% is share of *attention*, 8% governs channel 4 only |
| C5 | `story-bible` "introduce constraints when they bind" made a setup phase illegal | scoped to *explanation*; a constraint may be shown working before it binds |
| C6 | "story velocity is read as competence" read as a licence to compress | qualified: cut bridges, never summarise beats |
| C7 | `world-texture` capped **direct description** at ≤8% — the one mode models already match — while the mode they overproduce was unbudgeted, and is what `narrator-voice`'s free-indirect default produces | the budget still governs volume; §1 now governs **mode**, and the third failure is named *Atmospheric* (second pass, below) |

## The second pass, 2026-09-13 — how the world arrives

The first pass was about **events**: which beats get played. It said so itself, in
`why-ai-rushes.md` implication 3 — *the failure concentrates in the second half, not the opening*.
That is correct and it is why the opening had no pacing guard. This pass is about the **world**,
and it lands in the opposite place.

**The finding: models do not skip world-building, they deliver it in the wrong mode.** Human
fiction grounds a storyworld in space characters *move through and act on*; machine fiction
produces atmosphere — space that is sensed, moody, and never handled.

| source | what it established | what it produced |
|---|---|---|
| [How LLMs Build Fictional Worlds, arXiv:2609.02482](https://arxiv.org/abs/2609.02482) | five kinds of narrative space after Rohrbacher (2025); human text runs on **action space**, all four models tested overproduce **perceived space** — openings 0.47 against a human 0.19, whole chapters 0.17–0.33 against 0.083, two to three times human even at their within-chapter low; stable across narrative time, present from chapter 1, peaking at every chapter boundary; **descriptive space is the category models match most closely** | `roles/draft/world-texture.narrative-space.md`; the *Atmospheric* failure row and the handled-noun test in §1; C7 above |
| [WebNovelBench, arXiv:2505.14818](https://arxiv.org/abs/2505.14818) | scores LLM novelists against the web-novel distribution — this toolkit's exact genre — and names *Richness of Sensory Detail* a weak dimension for mid-tier models | supporting evidence for keeping `world-texture`'s 2–4 per scene as a floor, not only a ceiling |
| [Lost in Stories / ConStory-Bench, arXiv:2603.05890](https://arxiv.org/html/2603.05890v1) | *World-building & Setting* is a first-class consistency-error category beside plot and character | supports `story-bible` and the `set>` line; no new rule |
| [Royal Road: slow burn](https://www.royalroad.com/forums/thread/143611) · practitioner writing on serial pacing | the opening is a **tempo promise**; readers choose a serial on the rate the first chapters set, and breaking it late reads as betrayal — *"plot, promise, progression, and payoff, is how a slow burn keeps its heat"* | `opening.pace_contract`; `story-opening` §2 and its `pace-contract` slug |

**Why it hits us harder than it hits the paper's subjects.** The authors note that each chapter was
prompted separately, so every chapter start behaves like an opening and perceived space peaks at
the boundaries. They treat that as an artifact. For us it is the production model — run #4 of the
benchmark established a fresh session per chapter as the quality fix — so the peak is not an
artifact, it is our steady state.

**The caveat, kept deliberately.** The paper measures a textual divergence from human fiction and
explicitly declines to say what it means for a reader; it notes that readers in one study rated AI
stories as *more* absorbing. So this is grounds for a craft default, not for a gate — which is the
same conclusion the first pass reached by a different road.

**No check was written for it, and that is a decision.** Telling action space from perceived space
needed fine-tuned BERT classifiers at macro-F1 0.82. A regex would be guessing, and a check that
guesses is a number somebody writes toward (`docs/coverage-map.md`).

## What is measured, and what is deliberately not

`sw lint` prints reported-event markers, words before the first scene, and the dialogue-texture
line; `sw history` trends marker density across the book. **All notes.** There is a test asserting
the pacing findings can never be raised to a defect.

This project has twice built a number that decided whether a chapter shipped — word count, then
dialogue share — and both were optimised rather than satisfied, the second within five chapters.
Concreteness is the quantity that matters and it is not reliably countable; the markers only say
where to look.

---

# Third pass — why readers stay (2026-09-22)

Prompted by a user report: readers drop after two chapters. Three candidate causes were offered —
the light-novel format not being respected, missing craft knowledge, and a tone that is relentlessly
cold. This pass covers the second and third. The first turned out not to be a knowledge gap: the
toolkit has no light-novel register because it was built as a literary-craft toolkit pointed at
webnovel platforms, which is a register decision rather than a missing source.

## The finding that shaped this pass

The two earlier passes are both about **structure** — where the beat goes, how the world arrives.
Neither asks why a reader would want to spend an evening with these people. The corpus had the same
shape: measured at 118 checkboxes demanding a cost against roughly 9 on the relief side, and a
prohibition-to-generation ratio of 18.8 : 1 (`docs/creative-latitude.md`). A toolkit with a cost
ledger and no reward ledger produces books that are well made and that nobody finishes.

| source | what it established | what it produced |
|---|---|---|
| [Royal Road: ch1→ch2 retention](https://www.royalroad.com/forums/thread/134345) · [Reader drop rate](https://www.royalroad.com/forums/thread/111699) | the first three chapters are where readers settle in, see what the story is, and **gauge whether they like the characters**; authors treat sub-25% chapter-2 retention as a problem and disagree on the good band (>50% vs >70%) | confirms character appeal as an early-retention factor rather than a late one; `mc-design` §Good company |
| [Jane Friedman, connecting readers to characters](https://janefriedman.com/connect-characters/) · [Writers Helping Writers: attachment](https://writershelpingwriters.net/2018/12/goal-oriented-storytelling-attachment/) · [Nathan Bransford](https://nathanbransford.com/blog/2019/10/5-ways-to-make-a-character-more-sympathetic) | attachment is built from **many small moments**, not one big one — the "glue" of empathy. Named levers: show them caring about something concrete; **social validation** (other characters value them, so the reader does); vulnerability; competence shown while trying; goal specificity | `mc-design` §Good company, both fields. The social-validation lever was absent from the toolkit entirely: nothing anywhere asked whether anyone in the cast likes the POV character |
| [Green & Appel, *Narrative Transportation* (2024)](https://www.mcm.uni-wuerzburg.de/fileadmin/06110300/2024/Pdfs/Green___Appel__2024__Advances_Preprint.pdf) · [Bal & Veltkamp, PLOS One](https://journals.plos.org/plosone/article?id=10.1371%2Fjournal.pone.0055341) | transportation = focused attention + **emotional engagement** + mental imagery + cognitive detachment; it is the *emotional* component specifically that produces identification and liking | grounds the axis in something other than taste: the component that makes a reader stay is the one the corpus had no rule for |
| [Writer's Digest, pacing for emotional impact](https://www.writersdigest.com/pacing-for-emotional-impact-in-fiction-building-tension-and-release-in-a-novel) · [Hunger Mountain, idiosyncratic tone](https://hungermtn.org/idiosyncratic-tone-in-the-novel/) · [comic relief](https://en.wikipedia.org/wiki/Comic_relief) | a book in one tone becomes monotonous regardless of execution quality; grimdark fatigue is distinct from boredom — the story keeps asking for emotional attention without repaying it; relief is a structural device, not a lapse | `hook-and-pacing` §The temperature ledger: `bleak` and `tense` are now earned on the same terms `warm` and `quiet` always were |
| [Progression fantasy](https://en.wikipedia.org/wiki/Progression_fantasy) · [Cozy fantasy](https://en.wikipedia.org/wiki/Cozy_fantasy) | in this toolkit's own target genres, warmth is **load-bearing appeal** rather than a concession: banter and slice-of-life beside the training arcs are named reread drivers, and an adjacent genre is built entirely on community and friendship | settles the question of whether warmth is a genre-neutral default. It is, for these genres; `tone.warmth: cold` is the opt-out for the ones where it is not |

## What it produced in the corpus

| finding | change |
|---|---|
| the author's declared tone was discarded — `novel-init` Round D asked for it and no field existed | `tone.register` / `tone.warmth` in the template, in `CONFIG_KEYS`, owned by `narrator-voice` §The tone axis |
| the cost rule had no counterpart | `conflict-engine` gains `chapter-reward`, merged into its existing Phase A and Pass 4 cards |
| dialogue had no shape for people on the same side | `dialogue-voice` gains `rapport`; `roles/draft/dialogue-voice.same-side.md` |
| the one always-on tone gate ran anti-warmth | the microtension card regains the relief valve its own skill always had |
| nothing asked whether anyone likes the POV character | `mc-design` §Good company; a slot in the character template |
| the negative register was measured only by a maintainer's grep | `negation-density`, a habit note that reaches the WATCH row |

## The caveats, kept deliberately

**The Royal Road threads 403 on automated fetch.** Those figures come from search summaries, not
from reading the threads. They agree with the ~50% first-chapter drop the first pass already
established from the same forums, which is why they were used at all — but a human should open
them before anything is leaned on harder than "character appeal matters early".

**The craft sources are practitioner advice, not measurement.** The attachment levers are what
working editors and novelists say works. They are not evidence in the sense the transportation
papers are, and they are used here the way the first pass used Swain: as a source of craft
defaults, never of gates.

**The absorption caveat from the second pass still stands and cuts against this one.** Readers in
one study rated AI stories as *more* absorbing. Transportation is not a complete account of why
these novels get dropped, and nothing here should be read as one.

**Nothing became a ship gate.** `negation-density` is a note and is in `HABIT_NOTE_CHECKS`; the
emotional-direction finding is a note on `sw arc`. This project has three times built a number that
decided whether a chapter shipped — word count, dialogue share, `SPEECH_TARGET_LOW` — and all three
were optimised rather than satisfied. Warmth is a licence in this toolkit, never a quota, and no
chapter is scored on it.
