---
type: draft-card
owner: mystery-clues
dispatcher: write-chapter
phase: A
order: 25
description: Which clue moves this chapter, and which knowledge mode it runs in
when: optional.mystery-clues == on
---

# mystery-clues — draft card

Opened by `write-chapter` Phase A when the module is on. Two decisions, both recorded in the
chapter plan row.

**Produce two lines for the brief:**

```
mode     ahead - the reader saw the ledger's second page in ch 6; Halden did not
clue     C4 planted, disguised as a complaint about the delivery rota
```

## Decision 1 — the knowledge mode

| mode | reader vs. POV | what it produces |
|---|---|---|
| **behind** | reader knows less | curiosity |
| **level** | the same | participation |
| **ahead** | reader knows more | dread |

Rotate it deliberately across the arc. A whole novel in one mode exhausts or deflates.

**`ahead` has a hard constraint:** if the reader knows something the POV character does not, that
character must not have had access to it. Check the `kno>` line in the read-set. Someone failing
to notice what the reader watched them witness is an idiot-ball violation, and the repair is
always to change the information, never the intelligence (`mc-intel-meter`).

## Decision 2 — which clue moves, and how it is disguised

- **Disguise by function, not by obscurity.** A clue hides by doing another job — a complaint, a
  transaction, a joke, a piece of atmosphere — so the reader registers it without weighting it. A
  clue nobody notices was not planted; it was skimmed past.
- **Which plant is this?** Ambient, then noticed and dismissed, then loaded and unexplained. The
  decisive clue is planted early, while the reader is not yet suspicious.
- **One clue, two readings** is the strongest device available: a fact fully explained by the
  innocent interpretation and fully explained by the true one.
- Update the ledger in `state/threads.md`, both knowledge columns — the gap between them *is* the
  tension.

## If a reveal lands this chapter

Dramatise it: the answer arrives as something that happens *to* someone, under pressure, to
somebody who will act on it. Cite two or three plants briefly and trust the reader. Never explain
the foreshadowing. The answer costs something, and it opens a sharper question than it closed.
