# Craft sources

What was researched for this toolkit, where it came from, and which rule it produced. Provenance
only — nothing here is loaded at runtime. The runtime knowledge lives in
`.claude/skills/story-craft/references/`, because a file no dispatcher names never enters context
(benchmark finding 9).

Researched 2026-09-09, prompted by a reader report that the generated novel "goes fast to the
finish line", with no build-up of world or character.

## The finding that shaped everything

Machine-written fiction fails pacing **in one direction**: it gives the important beat to summary.
That asymmetry is why the rules added here guard one direction and leave over-elaboration to
`world-texture`'s existing description budget.

| source | what it established | what it produced |
|---|---|---|
| [CONCOCT, arXiv:2311.04459](https://arxiv.org/abs/2311.04459) | LLM story systems "gloss over important events or over-elaborate on insignificant details"; pacing is the distribution of **concrete detail** across events | `story-craft` §The one decision; the past-perfect tell; `CLAUDE.md` §4 rule 4 corollary |
| [arXiv:2407.13248](https://arxiv.org/pdf/2407.13248) | Models pace *setup* correctly but rush the major setback and climax; human stories carry higher suspense, the gap widening from the midpoint | `references/why-ai-rushes.md`; the note that the failure concentrates in the second half, not the opening |
| Dwight Swain, *Techniques of the Selling Writer* (1965) · [Wikipedia](https://en.wikipedia.org/wiki/Scene_and_sequel) · [Ingermanson](https://www.advancedfictionwriting.com/articles/writing-the-perfect-scene/) | scene = goal/conflict/disaster; sequel = reaction/dilemma/decision; MRUs; **sequel length is the pacing dial** | `references/scene-and-summary.md`; the follow-through note in the draft card |
| [Center for Fiction](https://centerforfiction.org/writing-tools/scenes-summary/) · [Write It Scared](https://www.writeitscared.co/blog-3/narrativedistance) | scene vs summary allocation; narrative distance; pull to scene as stakes rise | `references/scene-and-summary.md` §When summary is right |
| [Go Teen Writers](https://goteenwriters.com/2013/07/30/try-fail-cycles-the-yes-but-or-no-and-method-to-creating-plot-twists/) · [Karen Woodward](https://blog.karenwoodward.org/2014/04/parts-of-story-try-fail-cycles.html) | try/fail cycles; "yes, but" / "no, and"; failure is what makes a win feel earned | `references/story-structure.md` §Try/fail; `CLAUDE.md` §5 "a win costs a failure the reader watched" |
| [StudioBinder](https://www.studiobinder.com/blog/three-act-structure/) · [Helping Writers Become Authors](https://www.helpingwritersbecomeauthors.com/understanding-the-normal-world-of-a-storys-first-act/) | 25/50/25 as function not target; the ordinary world before the inciting incident | `references/story-structure.md` §Three acts; `chapter-plan`'s arc-1 shape table |
| [Royal Road forums: retention](https://www.royalroad.com/forums/thread/111699) · [slow burn](https://www.royalroad.com/forums/thread/143611) · [tension pacing](https://www.royalroad.com/forums/thread/131403) | ~50% drop after chapter 1; three pacing layers (chapter/arc/novel); slow burn works on *deposits*, not on lower density | `references/serial-pacing.md`; the "build-up is deposits" note in `hook-and-pacing/references/arc-rhythm.md` |

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

## What is measured, and what is deliberately not

`sw lint` prints reported-event markers, words before the first scene, and the dialogue-texture
line; `sw history` trends marker density across the book. **All notes.** There is a test asserting
the pacing findings can never be raised to a defect.

This project has twice built a number that decided whether a chapter shipped — word count, then
dialogue share — and both were optimised rather than satisfied, the second within five chapters.
Concreteness is the quantity that matters and it is not reliably countable; the markers only say
where to look.
