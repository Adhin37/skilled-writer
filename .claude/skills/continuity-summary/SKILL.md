---
name: continuity-summary
description: Maintain and read the compressed machine-only continuity ledger (CCS) that tells the writing model what the current chapter must be about, given prior chapters and planned ones. Use before drafting any chapter (to assemble the read-set) and after drafting (to append the chapter block). Also use to compact old chapters into arc digests.
---

# continuity-summary

The ledger in `state/continuity.md` is **context fuel, not a recap**. It is optimised for a
model's recall, not a human's comfort. Terseness is correctness here: it is what lets chapter 250
be written for the same cost as chapter 5.

Never apologise for it being unreadable. Never expand it into prose. If a human asks what
happened, generate a summary for them separately — do not soften the ledger.

---

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
10. `state/body.md` §1 and §2 — **whenever any character in this chapter has `form_locked: true`.**
    No description of their body, reach, voice or capability may be written without it.
11. `plan/timeline.md` §4 (scheduled for this arc) — always. It is short, and it is how the
    chapter knows what the world is doing behind the MC's back.

If the read-set exceeds what you can hold, drop items 4 and 3-oldest first. Never drop 1, 5, 6, 9,
10.

---

## CCS block format

One block per chapter. Fixed key order. Lowercase keys, `>` separator, ` / ` between items,
` ; ` between characters.

```
=C0042= pov:Rin | loc:Ashfall Market>Guild undercroft | t:D12 dusk | wc:1840 | arc:2
ev> buys forged map / spots guild seal is a fake / tails the forger / hides in undercroft
chg> Rin: wary->suspicious(Guild) ; Dael: admits debt, -2 trust w/Rin
pwr> Rin: Echo-step x2 (nosebleed, 6h lock) / limit shown: fails indoors
kno> Rin+{seal forged} Rin-{who paid} ; reader+{Dael paid} ; Dael-{Rin saw him}
thr> ~T14(forged-seal) ^T03(father-debt) vT09(oath to Mira: she forgives him)
obj> get the buyer's name -> next: read the Guild ledger
bod> Rin: F2 juvenile, unchanged / could not reach the top shelf, stacked crates instead
wld> Vesh: opens a file on Rin (institution, latency 10, fires ~ch52) / W04 grain levy unmoved
set> undercroft: wet chalk smell, one lamp / Rin owns Dael's coat now
hook> the ledger's first line is her father's name
open> who paid the forger / why the Guild tolerates it
```

### Line reference

| key | contents | required |
|---|---|---|
| `=CNNNN=` | header: chapter no, `pov`, `loc` (`>` for movement), `t` in-world time, `wc`, `arc` | yes |
| `ev>` | events, in order, as verb phrases. Max 6. Only what changed the situation. | yes |
| `chg>` | per-character state change: emotional, positional, relational. `->` for transitions, `±n` for trust/standing deltas | yes |
| `pwr>` | abilities used, cost paid, limits demonstrated. Omit line if genre has no power system | genre |
| `kno>` | **the most valuable line.** Who knows what now. `+{}` gained, `-{}` still lacks. Track `reader` as an entity. | yes |
| `thr>` | thread ops: `~` opened, `^` advanced, `v` paid, `x` abandoned. Ids from `threads.md` | yes |
| `obj>` | current objective, and the next concrete step | yes |
| `bod>` | form state for any `form_locked` character: current stage, whether it changed this chapter, and any limit the chapter ran into. On a transition, record what it now enables and what it costs. Omit only if nobody is locked | conditional |
| `wld>` | **the offstage question**: what the world did this chapter that the POV character does not know about. Driver moves, world-track events fired or moved, clocks advancing. See `timeline-engine`. Omit only if genuinely nothing moved | yes |
| `set>` | new world/possession facts introduced. Feeds `bible/` later. Omit if none | no |
| `hook>` | the chapter's final beat | yes |
| `open>` | questions the chapter deliberately left unanswered | no |

### Notation legend

```
->     transition            +{x}   now knows x
±n     delta on a scale      -{x}   still does not know x
~      opened                >      movement / sequence
^      advanced              x      abandoned
v      paid off              ()     parenthetical cost or qualifier
```

### Hard rules for writing a block

1. **No adjectives of quality.** `ev> a brutal, desperate fight` is wrong. `ev> fights Karth to a
   draw / breaks two ribs` is right. Record facts, not impressions.
2. **No prose sentences.** No articles where they can be dropped. No "then", "and then".
3. **Never omit `kno>`.** Dramatic irony, reveals and idiot-ball prevention all run off it.
   `mc-intel-meter` reads this line to check the MC is not acting on information they lack.
4. **Costs go in parentheses** attached to what caused them.
5. **Names exactly as in `lexicon.md`.** No pronouns. No "the protagonist".
6. **One block per chapter, appended.** Do not rewrite history to make it tidier.
7. **`chg>` is for tier A and B.** A walk-on earns a `chg>` entry only if they died, or did
   something that changed the situation — in which case they are being promoted anyway. Extras
   who merely appeared belong in the roster, not in the ledger.

## Arc digest format

```
=ARC2= ch26-50 | q:can Rin buy back her father's name? | a:no, she burns it instead
ev> guild ledger names father / Rin trades the map to Vesh / undercroft raid / Dael dies
chg> Rin: rung2->rung4 (stops asking permission) ; Vesh: ally->creditor
kno> Rin+{father sold the seal willingly} ; reader+{Vesh ordered the raid}
thr> paid:T03,T09 open:T14,T21 new:T27(Vesh's claim on Rin)
cost> Dael dead / Rin's name blacklisted in Ashfall / left hand scarred
end> Rin leaves Ashfall owing Vesh a favour she cannot define
```

## Book digest format

```
prem> one sentence
mc> Rin | tier3 | want:clear father's name | need:stop defining herself by it | wound:abandoned at 9
world> three lines max: the constraint, the power, the scarcity
arc> 1:<six words> 2:<six words> 3:<six words>
open> the standing questions, ids only
done> the things that can never be undone
```

---

## Procedure — before drafting (read mode)

1. Assemble the read-set above.
2. Produce a **chapter brief** — internal, ≤10 lines, not written to disk:
   - what the reader knows entering this chapter that the POV character does not, and vice versa
   - which threads are due
   - which characters must sound different than they did last time (from `growth.md`)
   - the one fact from the last five chapters this chapter must not contradict
3. Hand the brief to `write-chapter`.

## Procedure — after drafting (write mode)

1. Append the CCS block to §3 of `state/continuity.md`.
2. Update `state/threads.md` for every `thr>` operation.
3. Update `state/growth.md` for every rung change in `chg>`.
4. Append to `state/timeline.md` if in-world time advanced. If time advanced enough to age a
   `form_locked` character, check `state/body.md` §3 — a stage may be due.
5. If a form changed, update `state/body.md` §1, §2 and §4, and log any masking slip in §5.
6. Move any `set>` facts that will recur into `bible/world.md` or `bible/lexicon.md`.
7. Update `bible/cast/_extras.md`: a roster line for each new walk-on, an appended chapter number
   for each returning one, a row in **Dead** for any who died. Promote anyone at a third
   appearance or who changed the plot (`character-profile`), and add every named person to
   `lexicon.md`.

## Procedure — arc rollup

Triggered when a chapter completes an arc.

1. Write the ARC DIGEST from that arc's chapter blocks.
2. Compress the arc digest that is now two arcs old down to 40 words.
3. Rewrite the BOOK DIGEST.
4. Leave the chapter blocks in place — they are cheap and occasionally needed. Do not delete.

## Self-check

- [ ] Every block has `kno>` and `hook>`
- [ ] No block exceeds 13 lines
- [ ] No adjectives of quality anywhere in the ledger
- [ ] Thread ids in the ledger all exist in `threads.md`
- [ ] Names match `lexicon.md` exactly
