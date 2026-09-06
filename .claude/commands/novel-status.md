---
description: Where the novel stands — progress, open threads, character arcs, what's next
---

Report the state of the active novel. Read-only: change nothing.

```bash
python3 scripts/sw.py status novels/<slug>
python3 scripts/sw.py state novels/<slug>     # for section 9, the health check
python3 scripts/sw.py curve novels/<slug>     # for sections 5 and 9, the power curve
```

The first gathers everything sections 1-8 need: position, the last three `dlv>` lines, open
threads with how long each has gone untouched, growth rungs and skill ladders, the next planned
rows, the foreknowledge counters and the ending contract. The second finds what section 9 should
lead on. Neither writes anything.

Without Python, read `novel.md`, `state/continuity.md` (book digest + current arc digest + last 3
chapter blocks), `state/threads.md`, `state/growth.md`, and the plan rows around the draft line.

**Translate, do not paste.** The CCS is machine-only; section 2 is prose for a human.

Report, for a human, in this order:

1. **Position** — chapters written, current arc and its dramatic question, in-world day.
2. **Last three chapters** — one line each, in plain English (translate the CCS; do not paste it).
3. **Open threads** — id, promise, chapters open, `due`. Flag anything overdue or cold for 25+.
4. **Character arcs** — each tier-A character's rung and the one audible thing that has changed
   about them; tier-B characters as a line each with their shift done or pending; walk-ons as a
   count. Flag any principal stuck at rung 1 for two arcs, and any walk-on now past three
   appearances without a promotion.
5. **MC** — intel tier, current want, what the last arc cost them, what is unhealed. Then the
   **power curve**: their tier on `state/power.md` §2's ladder, what the edge is worth, the
   pressure range of the last arc, any boost debt still outstanding, and how far they are from
   `scaling.endgame`.
6. **The world** — reactivity dial, what each driver is currently doing that the MC doesn't know,
   which world-track events fire next, and how many world-track events this arc has moved. Flag
   an arc that has moved none. For fanfic, name the last canon decision the MC changed.
7. **Ending contract** — restate it, and confirm every non-negotiable is intact.
8. **Next** — the next three planned chapters, one line each.
9. **Health check** — the one thing most in need of attention, and why. Be specific and honest:
   a flat stretch, an overdue payoff, a cast imbalance, a thread count out of range, an inert
   world track, a crisis count over cap, an unpaid boost debt, a curve that has gone one-gear.

Keep it under 450 words. This is a dashboard, not a recap.
