# write-chapter — batches, and when the draft leaves the plan behind

Open this when the user asks for more than one chapter, or when the chapter you drafted is not the
chapter the plan row described.

## Running a batch

Run the **full loop per chapter — including the Phase C gate and the state write-back — before
starting the next.** Never
draft three chapters and then reconcile state: the second chapter has to be written against the
first chapter's consequences, and a batch that defers the ledger is a batch that invents them
twice.

Pause and check in after every **5 chapters** with a one-paragraph status and one question about
direction. Long unsupervised runs drift, and the drift is cheapest to correct early.

A long batch is also large enough to hit a session limit partway through. Finishing each chapter
completely means an interruption leaves whole chapters behind it, never a half-written one — and
"completely" includes the gate. A chapter left at `status: drafted` is an unfinished chapter, and
`sw readset` will refuse to be quiet about it when the batch resumes.

## Cost discipline across a batch

Per-chapter cost climbs with conversation length rather than with the novel's length — measured on
run #1, cache reads rose about 34% across three chapters inside one session while the read-set
stayed the same size. The read-set is bounded; the session is not. For a long run, start a fresh
session every few chapters. Nothing is lost: the whole point of the state files is that chapter N
is writable from `novels/<slug>/` alone.

## When the plan and the draft disagree

The draft wins if it is better, but the plan is updated, not ignored:

1. Write what the chapter actually became.
2. Amend that row in `plan/chapters.md`.
3. Re-check the following three rows for ones that no longer follow, and fix them.
4. Tell the user in the report line: *"chapter went somewhere else — replanned 43–45."*

If the divergence changes what the arc is about rather than how it gets there, that is a
`chapter-plan` job, not an edit: the arc's dramatic question moved, and the rows after it were
built to answer the old one.
