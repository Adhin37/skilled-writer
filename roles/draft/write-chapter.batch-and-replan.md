---
type: reference
owner: write-chapter
description: "the user asks for more than one chapter, or the chapter you drafted is not the chapter the plan row described"
---

# write-chapter — batches, and when the draft leaves the plan behind

Open this when the user asks for more than one chapter, or when the chapter you drafted is not the
chapter the plan row described.

## Running a batch

Run the **full loop per chapter — including the Phase C gate and the state write-back — before
starting the next.** Never
draft three chapters and then reconcile state: the second chapter has to be written against the
first chapter's consequences, and a batch that defers the ledger is a batch that invents them
twice.

The check-in after every **5 chapters** is the coordinator's, which runs the loop; your part is
the step 6 report that ends each chapter, with its one question about what comes next. Long
unsupervised runs drift, and the drift is cheapest to correct early.

A long batch is also large enough to hit a session limit partway through. Finishing each chapter
completely means an interruption leaves whole chapters behind it, never a half-written one — and
"completely" includes the gate. A chapter left at `status: drafted` is an unfinished chapter, and
`sw readset` will refuse to be quiet about it when the batch resumes.

## Cost discipline across a batch

Per-chapter cost climbs with conversation length rather than with the novel's length — measured on
run #1, cache reads rose about 34% across three chapters inside one session while the read-set
stayed the same size. The read-set is bounded; the session is not. Nothing is lost by starting
over: the whole point of the state files is that chapter N is writable from `novels/<slug>/` alone.

## After an interruption, re-enter through the read-set

**A chapter resumed mid-flight starts again at step 0.** Do not continue from where you stopped.
Re-run `sw readset`, re-resolve the card set with `sw kb cards`, and open the cards the phase
names — even if you were four hundred words into the draft and the brief is still above you in the
conversation.

**Then resume where the read-set's RESUME line says**, which it reads off the disk rather than
off your memory: a proposed brief is presented again, an approved one is drafted from, a
`drafted` chapter goes back as `READY FOR GATE`, a `gated` one goes to the state write. Step 0
again is not Phase A again.

The reason is measured. Run #4 read a warm agent five chapters deep opening 5 of ~36 resolved
cards against a cold agent's 33 and concluded that a long session rations the contract away. Run
#5 found the sharper edge: the same warm agent, in the same conversation, opened **twenty-nine**
cards for one chapter and **one** for the chapter a rate limit had landed in. Length was not what
did it. The contract is re-derived per chapter and lives in the run-up to the draft, so an
interruption anywhere in that run-up loses it silently — the draft continues, the cards do not,
and every check downstream stays green because nothing counts what you opened.

This costs one read-set call. Continuing without it costs the gate.

## When the plan and the draft disagree

The draft wins if it is better, but the plan is updated, not ignored — by the architect, since
`plan/` is design's:

1. Write what the chapter actually became.
2. Put `replan` in your report's `Bible:` line, naming the row and what it should now say. The
   fold amends it and re-checks the following three rows.
3. Say it in the report too: *"chapter went somewhere else — row 43 needs replanning, 44–45
   checked by the fold."*

If the divergence changes what the arc is about rather than how it gets there, that is a
`chapter-plan` job, not an edit: the arc's dramatic question moved, and the rows after it were
built to answer the old one.
