---
type: draft-card
owner: mc-design
dispatcher: write-chapter
phase: A
order: 17
description: Which bodies are locked, and what they cannot do today
when: mc.form_locked == true
---

# mc-design — draft card

Opened by `write-chapter` **Step 1**, but **only when some character is `form_locked`** — a reborn
infant, a weakened body, a pre-evolution shape, a transmigrator in someone else's face. Skip it
entirely otherwise. Written here rather than summarised there, because the body on the page is a
per-chapter constraint, while the rest of this skill runs once at `novel-init`.

**Produce:** which bodies are locked this chapter, and what they cannot do today.

## The rule

> **The body on the page is the body in the ledger.** For any `form_locked` character, no sentence
> describes their body, reach, voice or capability except from the **CURRENT FORM** row of
> `state/body.md`.

Not the form they will have. Not the form they had. The row that is current on this chapter number.

## What the current row governs

| governs | the failure it prevents |
|---|---|
| **reach and height** | a four-year-old taking something off a shelf an adult put there |
| **strength and stamina** | a weakened form winning a fight the ledger says it cannot |
| **voice** | an infant's pitch, vocabulary and what adults hear when it speaks |
| **fine motor control** | handwriting, knots, blade work — usually the first thing a reborn adult forgets they have lost |
| **endurance** | how long before the body simply stops, which is a scene the mind cannot argue with |
| **how the world reads them** | who is allowed to speak to them, who ignores them, what a witness would report |

**The gap between the mind and the body is the material, not an obstacle to it.** A competent adult
in a child's body who reaches for a tool that is not there any more is a better beat than one who
adapts offscreen. The lever set being smaller than the knowledge is usually the scene.

## Before drafting

- Check the transition chapter. If a stage change fires here, it is a **scene** with a cost, and
  `state/body.md` is updated in Step 5 — a form change that only appears in the ledger is a bug.
- **No final-form detail may appear in an earlier stage's description**, however incidental.
- Appearance is *how the world reads them*, never an inventory (`bias-guard`).

Building or amending the ledger, and the stage table: `references/form-ledger.md`.
