---
name: scene-craft
description: Build scenes with a goal, obstacle, turn and changed exit, and apply the want/friction/change delivery test. Use when structuring any chapter, and when a draft reads as 'things happened'.
---

# scene-craft

A chapter is one to three scenes. A scene is not a location or a conversation — it is **a unit in
which someone wants something, is opposed, and leaves changed.** If a passage has no want, it is
not a scene; it is a transition, and it should be a sentence.

---

**The boundary.** This skill owns what happens *inside* a scene. Whether a beat should be a scene
at all — rather than a line of summary — belongs to `story-craft`, and it is the decision that
controls pacing. A passage with no want is not a scene and should be a sentence; a *turn* with no
scene is a skipped chapter.

## The scene unit

| element | test |
|---|---|
| **POV** | whose head, and why theirs |
| **Goal** | what they are trying to get, concretely, in this scene |
| **Stakes** | what happens if they don't get it — must be knowable to the reader now |
| **Obstacle** | who or what opposes, with its own reason |
| **Turn** | the thing that isn't what they expected |
| **Exit state** | how the situation differs from the entry state |
| **Cost** | what this scene took |

Exit state has four legal values:

- **Yes, but** — they got it, and it created a problem. *The workhorse.*
- **No, and** — they failed, and it got worse. *The escalator.*
- **Yes, and** — they got it and more. Use rarely; it drains tension.
- **No, but** — they failed but salvaged something. Good after a hard blow.

Never **plain yes**. A scene the POV character simply wins is a scene the reader skims.

### The chapter-level version: want, friction, change

The scene table above, collapsed to the level a whole chapter is judged at. Same three ideas —
`goal` becomes **want**, `obstacle` becomes **friction**, and `exit state` becomes **change** —
and it is the exact test `revision-pass` Pass 9 runs on the finished draft, so build to it:

| | the question | fails when |
|---|---|---|
| **Want** | what the POV character is after in this chapter | the answer is "to react to things" |
| **Friction** | the person, rule or scarcity in the way | the only obstacle is the MC's own hesitation, twice running |
| **Change** | **what is materially different at the end** | the exit state equals the entry state |
| **Cost** | what was paid, and by whom | nothing — see `conflict-engine` |
| **Next** | what the reader now needs to see | the hook asks something the chapter already answered |

**Change is the load-bearing one, and it is not a summary of events.** *"She asks about the
recount"* is events. *"She is now someone the matron watches on purpose"* is a change. The
difference is whether you could state it without narrating the chapter — and a chapter that cannot
be stated that way is one a reader could skip.

This is what the toolkit gates on. Chapter **length is not a quality signal** and is not checked:
a short chapter that moves a relationship is finished, and a long one where everybody talks and
nothing shifts is not.

**Repeats must escalate.** If a beat recurs — a second refusal, a second interrogation, a second
failed attempt — the second must cost more than the first. A repeat that does not build is
repetition, and one of the two instances gets cut.

## The follow-through

After a hard scene, a short passage of reaction → dilemma → decision. This is where readers
metabolise what happened, and where character work happens. Keep it short in a
serialized chapter — long enough to feel the cost, short enough to keep the page turning. It ends
on a **decision**, which is the next scene's goal.

Skipping it entirely makes a chapter feel like a highlight reel. Overrunning it makes it feel
like the story has stopped.

## Chapter assembly

Default two-scene chapter:

```
cold open      in motion, no throat-clearing              ~7%
scene 1        goal → obstacle → turn                     ~40%
follow-through reaction → dilemma → decision              ~8%
* * *
scene 2        the decision acted on; the cost lands      ~40%   ← the change lands here
hook           final beat                                  ~5%
```

Proportions, not word counts — the chapter is as long as its material, and no longer.

One-scene chapters suit sustained pressure — an interrogation, a duel, a negotiation.
Three-scene chapters suit parallel lines converging; keep each scene short and do not switch POV
more than once (see `pov-switch`).

## Entering and leaving

**Enter late.** Start at the first moment something is at stake. Not the walk to the meeting —
the meeting, already going wrong.

**Leave early.** Cut at the turn, or one beat after. The reader does not need the goodbye, the
walk home, or the character reflecting on what just happened for four paragraphs.

Test: delete your first paragraph and your last paragraph. If the scene is better, they were
throat-clearing. This is true more often than it is comfortable.

## Grounding

Every scene needs, in its first 100 words: **where, who, and what is wrong**. Not as a list —
woven in. Then sensory details from that location's signature in `bible/world.md` — `world-texture`
owns how many and which. Reuse the same signature details across visits; that is how a reader
learns a place.

Keep bodies in space. In any scene with more than two people, the reader must be able to draw the
room. One spatial anchor per paragraph in action; one every three exchanges in dialogue.

## Scene types and their traps

| type | trap | fix |
|---|---|---|
| Conversation | two people exchanging information | give each a different want, and let one lie |
| Fight | choreography without stakes | decide before writing what is lost by the end. See `combat-choreography` |
| Travel | a montage of distance | either something happens on the road, or it is one sentence |
| Training | a montage of competence | show the cost and the failure, not the progression. One stage of the ladder per scene at most, and only when a stage actually turns over — practice between stages is a clause, not a scene (`competence-map/references/acquisition-ladder.md`) |
| Discovery | a lecture | the POV character wants something *else*; discovery interrupts it |
| Aftermath | drifting reflection | make it a decision scene: what will they do now |
| Political | names and titles the reader can't hold | ground in one concrete thing on the table |

## Transitions

- **Scene break `* * *`** for a jump in time, place or POV.
- **In-line time skip**: a sentence that carries the elapsed time and a fact. *By the time the
  gate opened, she had counted every guard twice.*
- **Never** a paragraph summarising what happened between scenes. If it mattered, it was a scene.

## Flashbacks

Expensive in serials: readers are dipping in weekly and a flashback breaks the forward line.

- Not before chapter 10.
- Never longer than 400 words.
- Must be triggered by something in the present scene and must answer a question the reader is
  actively asking.
- Prefer a single line of memory inside the present scene. Nine times in ten it is enough.

## Self-check

- [ ] Every scene has a goal, an obstacle, a turn and a cost
- [ ] No scene exits on a plain yes
- [ ] Every scene enters late and leaves early
- [ ] Where/who/what's wrong established in the first 100 words
- [ ] Bodies locatable in space
- [ ] Sensory details drawn from the location's signature, at `world-texture`'s budget
- [ ] The follow-through ends on a decision
- [ ] The chapter answers want / friction / **change** / cost / next
- [ ] `delivers:` names a difference, not a summary of events
- [ ] Any repeated beat escalated on its second appearance
