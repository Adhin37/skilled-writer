# power-scaling — how a curve dies

Open this when the curve is not landing and you need the named shape of what went wrong. Continues
`SKILL.md`'s section numbering. Each entry: the symptom as a reader experiences it, the mechanical
cause, and the fix that does not require rewriting the last thirty chapters.

## 8. The seven failures

### The god-step

**Symptom.** A chapter ends with the MC categorically stronger than they were at its start, and the
next arc has to be rebuilt around it.

**Cause.** A gain of +2 or more, almost always granted to solve a problem the author had written
themselves into. The tell is that the gain arrives *during* the crisis rather than before it.

**Fix.** Split it. A +3 gain is three gain rows across three arcs, and the two you have not written
yet become the next two arcs' spines — which is a better plan than the one you had. If the chapter
is already published, demote the gain to a **boost** retroactively: give it an expiry and a debt in
§5, and pay the debt in the next arc. A boost that turns out to be temporary is a scene; a tier that
turns out to be wrong is a continuity break.

### The treadmill

**Symptom.** Every arc introduces a stronger opponent, the MC gains to match, and the reader has
stopped tracking magnitudes by arc four.

**Cause.** Escalating on the tier axis instead of the stake axis. Pressure is held constant at +1
by moving *both* numbers up, which is arithmetically a working curve and dramatically nothing —
because a reader does not experience tier, only pressure, and the pressure never changed.

**Fix.** This is `conflict-engine`'s ladder, not this skill's. Hold the tier still for an arc and
escalate what is *lost*. A rung-5 stake at P=0 beats a rung-1 stake at P=+2 every time. If three
consecutive arcs each raised the MC's tier, one of them was a treadmill arc.

### The silent nerf

**Symptom.** The MC struggles with something they handled easily eleven chapters ago, and nothing
in the text acknowledges it.

**Cause.** The opposition was placed by feel rather than from §2, so the same task got two
different tiers. This is the most common defect the ledger catches and the one readers report as
"inconsistent power levels" — it damages trust faster than an overpowered MC does, because it reads
as the author not remembering their own book.

**Fix.** The ledger, used in the order §1 gives: pressure first, opponent second. Where it has
already happened, the cheapest repair is almost always to make it *diegetic* — the MC is injured,
exhausted, holding back, or the task is genuinely harder for a named reason. One clause. But do it
in the chapter, not in a later explanation.

### The escalating sky

**Symptom.** Around chapter 80 a new tier is revealed above the one everybody thought was the top.
Then another.

**Cause.** `ceiling_tier` and `endgame` were never set, so the ladder had no top and the only way to
generate pressure was to add one. Each addition retroactively shrinks everything the MC has already
achieved, which is why long serials feel like they are deflating.

**Fix.** Set `endgame` now, even mid-novel, and make the revealed tier the last one. Then move the
conflict off the ladder — this is what `plateau-late` exists for (`curve-shapes.md` §6). A ladder
that stops is a story that can end.

### The unpaid boost

**Symptom.** The MC won a fight they should have lost, and the reader is not sure why it was
allowed.

**Cause.** A boost with no debt, or a debt logged in §5 and never paid. The novel spent the reader's
trust and did not settle up.

**Fix.** Pay it late rather than not at all — a debt paid twelve chapters after it was incurred
still works, and often works better, because the reader has stopped expecting it. What does not
work is a second unpaid boost. The `climax?` flag exists to make the second one visible before it
is written.

### The flat middle

**Symptom.** Chapters 40–70 are competent and nobody is reading them.

**Cause.** No tier movement and no pressure variation for a long stretch — `scaling.flat_max`
exists to catch exactly this. It usually happens during a stretch of good character work, which is
why it survives revision: every individual chapter is fine.

**Fix.** Not a gain — a gain here rewards the wrong thing and starts a treadmill. Vary the
*pressure* instead: one P=+2 chapter the MC survives rather than wins, immediately after a P=−1
chapter, teaches the reader the range again in two chapters. The range is the entertainment; the
absolute value never was.

### The invisible ceiling

**Symptom.** The MC's advantage has never failed, and the reader has quietly stopped worrying about
anything.

**Cause.** `scaling.first_limit_by_ch` passed without the limit landing, or the limit landed
offstage. Every subsequent threat is uninsurable — the reader cannot price it, because they have
never seen the price paid (`story-opening` §3, from the other direction).

**Fix.** The wall, on the page, at the earliest honest opportunity. It does not have to be a defeat:
the advantage working and *not being enough* is stronger than the advantage failing, because it
keeps the promise while closing the loophole.

## The one-line diagnostic

Run `sw curve` first — five of the seven are countable. If it comes back clean and the curve still
feels wrong, the question is almost always: **what was the pressure eleven chapters ago, and what is
it now?** If the answer is the same number, the problem is monotony. If the tier rose and the
pressure fell, the problem is creep. If neither moved, the problem is the flat middle.
