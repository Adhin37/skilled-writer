# Brief — the chapter in progress

One brief, overwritten every chapter. `write-chapter` Phase A writes it here **before** it stops
for approval, under `status: proposed`, and flips that line to `status: approved` when the answer
comes back; Phase B drafts from it, and step 5 copies its `cand` and `gives` lines into the CCS
block's `cand>` and `gav>` instead of remembering them.

**Why it is a file and not only a message.** Everything else the loop decides lands in `bible/`,
`plan/` or `state/`. The brief did not, so it was the one decision that a compaction, an
interruption or a dead session could take outright — benchmark run #5 lost a chapter's candidates
that way and its ledger reads `cand> unrecorded`. On a resume `sw readset` finds a brief whose
chapter matches the one being drafted and hands it back at the top of the read-set.

It is a scratch file, not a ledger. Nothing is appended, nothing is kept, and nothing is scored on
it. The block below is replaced wholesale each chapter; once the chapter is stamped and its CCS
block is written, what is here has already been copied into `state/continuity.md` and this file is
only waiting to be overwritten.

Keep the `status:` line on its own line above the block, and the fenced block as the brief's own
thirteen lines, opening on `Ch <n> — "<title>"`, which is the line the read-set matches against
the chapter being drafted. A proposed brief is never drafted from: on a resume the read-set hands
it back to be presented again. Delete the placeholder below when the first brief is written.

```
(no brief on file yet)
```
