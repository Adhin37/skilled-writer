# Why machine-written stories rush, measured

Open this when a draft is compressed and you want the reason rather than the symptom, or when you
are editing this toolkit's pacing rules and need to know which failure they are guarding against.

This file exists because the failure is **specific and asymmetric**, and a rule written against the
general idea of "bad pacing" will guard the wrong direction.

## What the research finds

**The failure is glossing, not padding.** CONCOCT (Wang et al., 2023) states it directly: LLM
systems for long-form stories "frequently suffer from unnatural pacing, whether glossing over
important events or over-elaborating on insignificant details". Their fix is a **concreteness
evaluator** — a judgement about how low-level-detailed an event is — used to expand the vaguest
parts of an outline first. Pacing, in their formulation, *is* the distribution of concrete detail
across events. That is the same quantity this skill calls scene-versus-summary.

**Setup is fine; the turns are rushed.** Work on human-level narrative generation finds that models
grasp the correct pacing to establish the initial setup and introduce the main goal, but fail to
unfold the crucial junctures — the **major setback and the climax**. Introduced briefly and resolved
quickly, both flatten the arc.

**Suspense is measurably lower.** Human stories carry consistently higher suspense, and the gap
widens from the midpoint to the end — exactly where the machine version has already discharged its
tension.

**Length is not the problem.** Where models do hit a target length, they tend to tell most of the
story early and leave little for the rest. Practitioners writing full-length books with LLMs report
the same shape: some chapters read as a slog, while the model "breezes right over big important
moments with a summary".

## What it implies for this toolkit

1. **Guard one direction.** Our rules should make skipping an important beat expensive and leave
   over-elaboration to the existing description budget in `world-texture`. Symmetric rules waste
   attention on a failure we do not have.
2. **The lever is concreteness, not word count.** Length gating was removed from this repo twice for
   being gameable. Concreteness is the quantity that actually matters, and its countable proxy is
   whether a turn sits inside a past-perfect clause.
3. **Watch the second half hardest.** The measured failure concentrates at the setback and the
   climax, which in a 25-chapter arc is `chapter-plan`'s rows 12–14 and 23–24 — not the opening.
   The opening complaint and this one have the same cause and different locations.
4. **A model told only "be concise" will comply.** Every rule in `CLAUDE.md` §5 that bans padding is
   correct and none of them says what to spend words *on*. That asymmetry is why §5 now carries the
   build-up counterweight.

## Sources

- [Improving Pacing in Long-Form Story Planning (CONCOCT), arXiv:2311.04459](https://arxiv.org/abs/2311.04459)
- [Are Large Language Models Capable of Generating Human-Level Narratives?, arXiv:2407.13248](https://arxiv.org/pdf/2407.13248)
