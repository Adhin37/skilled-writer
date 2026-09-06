# voice-separation — the body and thought channels

Open this while drafting a scene: how a character's body identifies them, and how a non-POV mind is shown without entering it.

---

## 4. The body channel

The most under-used identifier and the cheapest. A reader who has learned a body can tell who
entered a room before anyone speaks.

Three decisions per tier-A character, two for tier B, recorded once and reused:

| field | choose one |
|---|---|
| **default state** | still · restless · occupied (always holding something) · arranged (posed) |
| **the hands** | the one thing their hands do — the single highest-value field |
| **pressure move** | goes still · gets bigger · gets smaller · gets busy · closes distance · leaves |

Plus, for tier A only: **distance** — how close they stand by habit, and what they do when someone
crosses it.

### Rules

**The beat must be theirs.** An action beat any character could perform is dead weight
(`prose-quality` bans it as stage business; here it fails as identification too). Banned as
identifiers, all of them:

*nodded · shrugged · sighed · raised an eyebrow · crossed their arms · ran a hand through their
hair · clenched their jaw · let out a breath · looked away · smiled slightly*

These are the model's default gesture set. They identify nobody. Replace with the character's
hand-habit or cut the beat entirely — a line with no beat is better than a line with a generic one.

**Body contradicts speech.** The most useful thing a beat can do is disagree with the words. *"I'm
not angry," she said, and put the cup down where it had been, exactly, twice.*

**The body is class and culture, not just personality.** Who stands, who sits without being told,
who keeps their hands visible, who does not turn their back — these come from `bible/society.md`
(`social-fabric`), and a servant and a magistrate who share a body idiom have flattened the world
as well as the cast.

**Under a locked form, the ledger wins.** If a character has `form_locked: true`, their body idiom
is expressed within the current stage's limits in `state/body.md`. A reborn child has the habit,
not the reach.

---

## 5. The thought channel

Interiority is restricted by tier — walk-ons never get any (`character-profile`) — so this channel
splits in two.

### POV-eligible characters

Three fields, in the profile, used by `narrator-voice` and `pov-switch`:

| field | values |
|---|---|
| **thought unit** | images · words · numbers · bodies · rules · people · money |
| **thought speed** | ahead of the scene · with it · one beat behind |
| **facing an unknown** | test it · avoid it · name it · ask someone · assume the worst |

The thought unit is also the **metaphor source** (`narrator-voice`): a character who thinks in
money does not reach for a tide simile. Two POV characters who think in the same unit will produce
identical narration however different their dialogue is — that is the head-hopping smell readers
notice without being able to name.

### Everyone else — the first move

No interiority. A non-POV character's mind reaches the page through **what they reach for, look at,
or say first** when the situation changes. One line in their profile: *Karth checks the door.
Dael checks the room's faces. Mira checks the exit she came in by.*

Three characters, one entrance, three minds, zero interiority. This is how the cast thinks
differently inside a single POV.

### Marked thought belongs to the POV character alone

The direct-thought channel (`'…'`, `narrator-voice` §The four channels) does not create an
exception to any of the above. **A non-POV character never gets one** — that is head-hopping with
punctuation on it, and it is more conspicuous than the prose version, not less.

When the POV character does get one, it obeys their matrix row like any other line they produce:
their turn length, their articulacy, their register. A character whose spoken articulacy is 2 does
not think in balanced clauses because the marks make it look like a caption. And the budget is a
separation tool in its own right — at one to three per chapter, a marked thought is the most
emphatic thing on the page, so it should be the sentence only *this* character would form.

---
