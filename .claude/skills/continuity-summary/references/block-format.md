---
type: reference
owner: continuity-summary
description: writing a block or a digest. The line reference, the notation legend and the hard rules
---

# continuity-summary — the CCS block, arc digest and book digest formats

Open this when writing a block or a digest. It is the format spec: the line reference, the notation legend, and the hard rules.

---

## CCS block format

One block per chapter. Fixed key order. Lowercase keys, `>` separator, ` / ` between items,
` ; ` between characters.

```
=C0042= pov:Rin | loc:Ashfall Market>Guild undercroft | t:D12 dusk | wc:1840 | arc:2
dlv> Rin can no longer use the Guild archive, and knows who closed it to him
ev> buys forged map / spots guild seal is a fake / tails the forger / hides in undercroft
chg> Rin: wary->suspicious(Guild) ; Dael: admits debt, -2 trust w/Rin
pwr> P=+1 vs the Warden's man (T4 vs Rin T3) survived, ribs / Echo-step x2 (nosebleed, 6h lock) / limit shown: fails indoors
kno> Rin+{seal forged} Rin-{who paid} ; reader+{Dael paid} ; Dael-{Rin saw him}
thr> ~T14(forged-seal) ^T03(father-debt) vT09(oath to Mira: she forgives him)
obj> get the buyer's name -> next: read the Guild ledger
bod> Rin: F2 juvenile, unchanged / could not reach the top shelf, stacked crates instead
wld> Vesh: opens a file on Rin (institution, latency 10, fires ~ch52) / W04 grain levy unmoved
fk> spent K3(forger's name) to place himself in the undercroft -> K3 spent ; K7,K9 now suspect (she was never there in the remembered version)
set> undercroft: wet chalk smell, one lamp / Rin owns Dael's coat now
cand> 2:Rin reports the seal to the Guild 3:Rin sells the forger's name to Vesh -> took 3, the other two leave him with nothing to trade
z4> the forger is the one who warns him, and does it for free, which costs Rin more than a price would have
hook> the ledger's first line is his father's name
open> who paid the forger / why the Guild tolerates it
```

### Line reference

| key | contents | required |
|---|---|---|
| `=CNNNN=` | header: chapter no, `pov`, `loc` (`>` for movement), `t` in-world time, `wc` (a measured fact, never a target), `arc` | yes |
| `dlv>` | **what is materially different at the end.** One clause, a difference and not a summary of events. Mirrors the chapter's `delivers:` frontmatter and is what `revision-pass` Pass 9 gated on | yes |
| `ev>` | events, in order, as verb phrases. Max 6. Only what changed the situation. | yes |
| `chg>` | per-character state change: emotional, positional, relational. `->` for transitions, `±n` for trust/standing deltas | yes |
| `pwr>` | **`P=±n` first**, with both tiers and the outcome, then abilities used, cost paid, limits demonstrated. The `P` value must match `state/power.md` §3 for this chapter — `sw curve` compares them. Omit only if `scaling.shape` is `none`; a chapter with no confrontation still records the abilities it spent | conditional |
| `kno>` | **the most valuable line.** Who knows what now. `+{}` gained, `-{}` still lacks. Track `reader` as an entity. | yes |
| `thr>` | thread ops: `~` opened, `^` advanced, `v` paid, `x` abandoned. Ids from `threads.md` | yes |
| `obj>` | current objective, and the next concrete step | yes |
| `bod>` | form state for any `form_locked` character: current stage, whether it changed this chapter, and any limit the chapter ran into. On a transition, record what it now enables and what it costs. Omit only if nobody is locked | conditional |
| `wld>` | **the offstage question**: what the world did this chapter that the POV character does not know about. Driver moves, world-track events fired or moved, clocks advancing. See `timeline-engine`. Omit only if genuinely nothing moved | yes |
| `set>` | new world/possession facts introduced — location anchors, social facts, what a thing costs. Feeds `bible/world.md` and `bible/society.md` later. Omit if none | no |
| `fk>` | foreknowledge spent this chapter, what it cost, and which other items it invalidated. Omit only if `mc.foreknowledge` is unset. See `meta-knowledge` §5 | conditional |
| `hook>` | the chapter's final beat | yes |
| `cand>` | **the candidates Phase A did not take**, numbered as the draft card numbers them, then `-> took N` and a clause saying why. `story-craft`'s draft card owns the step; this line is the only place its output survives the conversation. Omit only if the chapter was drafted without the step, which is itself the thing worth seeing | no |
| `z4>` | **the answer to Pass Z4** — the thing here a competent hack would not have written — or the literal `none`. `none` is a legitimate entry and is the point of the line: one is a chapter, a run of them is a habit, and `sw history` counts them | no |
| `gate>` | **what Phase C had to fix** - check names where they have them, a dozen words at most. Omit the line entirely when the gate found nothing: an absent `gate>` is the clean signal, and a run of them is worth more than a run of `gate> clean`. `sw readset` reads the last five back to build the next chapter's WATCH row | no |
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
   **Never omit `dlv>` either** — a block whose `dlv>` restates its `ev>` is recording a chapter
   that did not change anything, and that is a defect worth seeing in the ledger.
   `mc-intel-meter` reads this line to check the MC is not acting on information they lack.
4. **Costs go in parentheses** attached to what caused them.
5. **Names exactly as in `lexicon.md`.** No pronouns. No "the protagonist".
6. **One block per chapter, appended.** Do not rewrite history to make it tidier.
7. **`chg>` is for tier A and B.** A walk-on earns a `chg>` entry only if they died, or did
   something that changed the situation — in which case they are being promoted anyway. Extras
   who merely appeared belong in the roster, not in the ledger.

## Arc digest format

```
=ARC2= ch26-50 | q:can Rin buy back his father's name? | a:no, he burns it instead
ev> guild ledger names father / Rin trades the map to Vesh / undercroft raid / Dael dies
chg> Rin: rung2->rung4 (stops asking permission) ; Vesh: ally->creditor
kno> Rin+{father sold the seal willingly} ; reader+{Vesh ordered the raid}
thr> paid:T03,T09 open:T14,T21 new:T27(Vesh's claim on Rin)
cost> Dael dead / Rin's name blacklisted in Ashfall / left hand scarred
end> Rin leaves Ashfall owing Vesh a favour he cannot define
```

## Book digest format

```
prem> one sentence
mc> Rin | tier3 | want:clear father's name | need:stop defining himself by it | wound:abandoned at 9
world> three lines max: the constraint, the power, the scarcity
arc> 1:<six words> 2:<six words> 3:<six words>
open> the standing questions, ids only
done> the things that can never be undone
```

**The book digest goes stale silently, and it is the most expensive file to have wrong** — it is
read first and trusted most. Two rules:

- **`done>` is updated in the same pass as any chapter that makes something irreversible.** A
  digest still reading `(none — no chapters drafted yet)` after five drafted chapters is not a
  cosmetic lapse; every later read-set inherits it, and a model assembling context from it will
  believe the book has not started.
- **Re-read the digest against reality at every arc rollup.** `prem>`, `mc>` and `world>` are
  written once and then quietly diverge from what the novel actually became.

---
