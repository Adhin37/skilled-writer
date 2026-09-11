---
name: continuity-summary
description: Read and maintain the compressed continuity ledger (CCS). Use before drafting to assemble the read-set, after drafting to append the block, and to compact old arcs into digests.
---

# continuity-summary

The ledger in `state/continuity.md` is **context fuel, not a recap**. It is optimised for a
model's recall, not a human's comfort. Terseness is correctness here: it is what lets chapter 250
be written for the same cost as chapter 5.

Never apologise for it being unreadable. Never expand it into prose. If a human asks what
happened, generate a summary for them separately — do not soften the ledger.

---

## What lives in `references/`

| file | open it when |
|---|---|
| `references/block-format.md` | writing a block or a digest. The line reference, the notation legend and the hard rules |

## The three tiers

| tier | scope | cap | rewritten |
|---|---|---|---|
| BOOK DIGEST | whole novel | 200 words | at each arc boundary |
| ARC DIGEST | one arc | 120 words (40 once two arcs older) | when arc closes |
| CHAPTER BLOCK | one chapter | 13 lines | once, at drafting; never edited after the arc closes |

Compaction is the whole point. Chapter blocks are dense but numerous; arc digests replace them
for recall; the book digest replaces arcs. The read-set below stays roughly constant in size no
matter how long the novel gets.

## The read-set (what to load before writing chapter N)

```bash
python3 scripts/sw.py readset novels/<slug> -c <N>
```

**One command assembles the whole list below**, sliced rather than whole-file: the five recent
blocks and not the ledger, this chapter's matrix rows and not the matrix, this chapter's
locations and not the world bible. It resolves the characters from the plan row's POV and the
recent `chg>` lines, prints which ones it picked, and takes `--chars` when the chapter
introduces somebody it could not know about. Pass `--society` when the chapter turns on a
social rule, and `--locs` when it moves somewhere the plan row does not name.

It ends with a **NOT LOADED** list. That list is the point: the read-set is bounded on purpose,
and what is missing is missing deliberately. Ask for anything on it by name when the chapter
needs it — do not open the source files for anything the bundle already contains.

**If Python is unavailable**, load the list below by hand, in order, honouring every "rows
only" instruction. That is what the command is doing.

Load exactly this. Not more.

1. BOOK DIGEST
2. ARC DIGEST for the current arc, plus the immediately previous one
3. CHAPTER BLOCKS for chapters N−5 … N−1
4. Any chapter block cited by an open thread in `state/threads.md` with `tension: hot`
5. `plan/chapters.md` rows N−1, N, N+1, N+2
6. `state/threads.md` rows with status `open`/`escalated`
7. `state/growth.md` rows for characters appearing in row N
8. `bible/cast/<char>.md` for those characters only — **tier A and B files, and never a dormant
   one**. Walk-ons have no file: if one appears in row N, load their line from
   `bible/cast/_extras.md` (the relevant section only, if the roster is split)
9. `bible/lexicon.md` (always — it is small and prevents the most common defect)
9b. `bible/cast/_voices.md` §1 — **the matrix rows for this chapter's speakers, always**, plus §3
    for the POV character and §5 if a mirror is on the page. Profiles are read one at a time and
    sameness is only visible side by side; this is the file that keeps the cast from converging on
    the MC. It is a table, and it is cheap.
9c. `bible/cast/_competence.md` §1 and §2 — **the rows for this chapter's characters, always**, plus
    §4 if a broad-knowledge character is on the page. A few lines each, and they are what stop
    everyone in the chapter from answering every question. Load §3 (what nobody here knows) when
    the chapter turns on an expertise.
10. `state/body.md` §1 and §2 — **whenever any character in this chapter has `form_locked: true`.**
    No description of their body, reach, voice or capability may be written without it.
10b. `state/power.md` §1, §2 and §5 plus the last five §3 rows — **unless `scaling.shape` is
    `none`**. The chapter's opposition is derived from the arc's band, and no sentence may make
    anyone more or less capable than §1 and §2 say they are.
11. `plan/timeline.md` §4 (scheduled for this arc) — always. It is short, and it is how the
    chapter knows what the world is doing behind the MC's back.
12. `bible/world.md` — **the location rows for this chapter's locations only**, for their sensory
    signatures. Not the whole file. A chapter written without them re-invents the place.
13. `bible/society.md` — **only if the chapter turns on a social rule** (a licence, a debt, a
    court, a custom, who is allowed where). Load the relevant section, never the file.

If the read-set exceeds what you can hold, drop items 4 and 3-oldest first. Never drop 1, 5, 6, 9,
9b, 9c, 10, 10b, 12.

---

## Procedure — before drafting (read mode)

1. Assemble the read-set above — `sw readset novels/<slug> -c <N>`, or by hand.
2. Produce a **chapter brief** — internal, ≤10 lines, not written to disk:
   - what the reader knows entering this chapter that the POV character does not, and vice versa
   - which threads are due
   - which characters must sound different than they did last time (from `growth.md`)
   - the one fact from the last five chapters this chapter must not contradict
3. Hand the brief to `write-chapter`.

## Procedure — after drafting (write mode)

1. Append the CCS block to §3 of `state/continuity.md`. If Phase C had to fix something, the
   block carries a `gate>` line naming it in a dozen words or fewer — and no `gate>` line at all
   when the gate came back clean. `sw readset` reads the last five back to build the next
   chapter's WATCH row, so a defect recorded here is one the next draft is written against rather
   than one the gate fixes again in chapter 43.
2. Update `state/threads.md` for every `thr>` operation.
3. Update `state/growth.md` for every rung change in `chg>`.
4. Append to `state/timeline.md` if in-world time advanced. If time advanced enough to age a
   `form_locked` character, check `state/body.md` §3 — a stage may be due.
5. If a form changed, update `state/body.md` §1, §2 and §4, and log any masking slip in §5.
5b. Unless `scaling.shape` is `none`: a row in `state/power.md` §3 for every confrontation, with
    its `P` and — at P ≥ +1 — what the win cost; a row in §4 for a tier advance, with all four
    requirements, and §1 moved to match; a row in §5 for any boost, with its expiry, debt and due
    chapter. The `pwr>` line must agree with §3.
6. Move any `set>` facts that will recur into the right file: location anchors and world rules to
   `bible/world.md`, social facts (a price, a licence, who may testify, what a custom obliges) to
   the log at the foot of `bible/society.md`, names and terms to `bible/lexicon.md`. An anchor or
   a social fact invented on the page and left unrecorded is a contradiction waiting to happen.
7. Update `bible/cast/_extras.md`: a roster line for each new walk-on — including their one
   off-default axis — an appended chapter number for each returning one, a row in **Dead** for any
   who died. Promote anyone at a third appearance or who changed the plot (`character-profile`),
   and add every named person to `lexicon.md`.
8. Add a matrix row to `bible/cast/_voices.md` for anyone promoted this chapter, placed against the
   existing cast (`voice-separation` §1). Nothing else in that file changes per chapter — it is
   revised at arc rollup, not per chapter.
9. Log any **skill stage** that advanced in the skill-ladder table of `state/growth.md`, with what
   caused it (a teacher, a reference, a costly failure) and what the practice is costing. Add a
   competence row to `bible/cast/_competence.md` for anyone promoted, and for any domain a character
   genuinely acquired on the page. If the chapter needed an expertise nobody in the cast had, put it
   in §3 of that file — that is a person the story is missing (`competence-map`).

## Procedure — arc rollup

Triggered when a chapter completes an arc.

0. Run the **arc-boundary pass** before compressing anything, while the chapter blocks are still
   at full detail:

   ```bash
   python3 scripts/sw.py arc novels/<slug> --show note
   ```

   It lines the arc's chapters up next to each other and prints what only appears in aggregate:
   the dialogue trend, the length spread, hooks side by side, cast rotation, thread operations,
   repeated deliveries, and the foreknowledge ledger. Every high-severity finding in benchmark
   run #1 was of this kind — invisible in the chapter it appeared in, obvious across five. The
   command ends with the judged half it cannot do; answer those by reading, and **do not score
   the arc**. See `/novel-recap review`.

1. Write the ARC DIGEST from that arc's chapter blocks.
2. Compress the arc digest that is now two arcs old down to 40 words.
3. Rewrite the BOOK DIGEST.
3b. Run the **drift check** (`voice-separation` §6): one recent line from each recurring character,
    read side by side. If the axes have compressed toward the MC's, restore them and log it in §6
    of `bible/cast/_voices.md`. A serial converges slowly enough that only a periodic side-by-side
    catches it.
3c. Run the **competence audits** on `bible/cast/_competence.md`: has anyone quietly accumulated
    domains past their budget across the arc, and do the `none` rows sort by gender, class or
    people (`bias-guard`, `competence-map` §7)? Both defects arrive one convenient line at a time
    and are only visible in aggregate. Log the redeal in §5.
4. Leave the chapter blocks in place — they are cheap and occasionally needed. Do not delete.

## Self-check

```bash
python3 scripts/sw.py state novels/<slug>
```

Checks every box below that is countable — required lines, block length, `wc:` against the
measured body, thread ids against the board, the book digest's `done>` line — plus the plan
rows and the promotion trigger. The two it cannot check are the last two: whether `dlv>` names
a difference rather than a summary, and whether the ledger has drifted into adjectives of
quality. Read those yourself.

- [ ] Every block has `dlv>`, `kno>` and `hook>`
- [ ] `gate>` is present on every chapter Phase C had to change, and absent on every chapter
      it did not — `gate> clean` is not a value, it is a missing line
- [ ] `dlv>` names a difference, not a summary of events, and matches the chapter's `delivers:`
- [ ] `fk>` present on every chapter that spent foreknowledge, with what it invalidated
- [ ] `wc:` matches the chapter file's measured `wordcount:` — a stale number here corrupts
      every share computed from it later
- [ ] No block exceeds 15 lines
- [ ] No adjectives of quality anywhere in the ledger
- [ ] Thread ids in the ledger all exist in `threads.md`
- [ ] Names match `lexicon.md` exactly
- [ ] `fk>` is present on every block once `mc.foreknowledge` is set — including the chapters
      that spent nothing, which record that they spent nothing
