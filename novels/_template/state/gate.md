# Gate hand-back — the chapter the gate last passed

One hand-back, overwritten every chapter. The gate (`revision-pass`, Phase C of `write-chapter`)
writes it here before it returns, and the coordinator relays the same text to the drafter. Step 5
copies the block's `z4>` from it and carries every `For design:` item into the report's `Bible:`
line, instead of remembering them.

**Why it is a file and not only a message.** Every other hand-off in the loop leaves a mark on disk
— the brief's `status:`, the chapter's `status:`, the CCS block. The hand-back did not, so it lived
only in two conversations, and when the drafter holding it died mid-state-write, its successor
rebuilt the block from the ledger and lost a design item nobody could recover. On a resume at
step 5, `sw readset` says whether the hand-back on file is this chapter's.

It is a scratch file, not a ledger, and it is the gate's alone: the drafter copies from it and
never edits it. Keep the fenced block opening on `Ch <n> — gate hand-back`, which is the line the
read-set matches against the chapter being written. Delete the placeholder below when the first
hand-back is written.

```
(no hand-back on file yet)
```
