---
name: comedy-levity
description: Optional (default off). Place humour deliberately - character-sourced, rhythm-aware, never at the cost of stakes. Use only while this skill is enabled.
metadata:
  type: skill
  tier: optional
  force: stylistic
  when: optional.comedy-levity == on
  owns: [humour-placement]
---

# comedy-levity

**Gate.** Applies only if `novel.md` → `optional.comedy-levity` is `on`. When `off`, wit that
belongs to a character's fingerprint is still fine — this skill governs *scheduled* levity, not
voice.

**Who is allowed to be funny is not decided here.** The `wit` axis in `bible/cast/_voices.md`
decides that, on or off: at most two of the recurring cast have wit other than `none`, each with a
named register (dry, warm, clowning, cruel) and a named pressure that triggers it
(`voice-separation` §1). This skill places the comic beats; it never hands a joke to a character
whose axis says `none`, and it never lets a scene make everyone funny because the scene had room.
A cast where anyone can land the line is a cast with one voice in it.

---

## Where humour comes from

**Character, not narration.** The narrator making jokes about the story undercuts it. A character
making jokes tells you who they are. Humour is a fingerprint field (`dialogue-voice`): who is
funny, in what register, and — most revealingly — *what they use it to avoid*.

**Sources that work in serials:**

| source | shape |
|---|---|
| Competence mismatch | someone excellent at the wrong thing for this situation |
| Deflection | a character who jokes precisely when they should not |
| Deadpan under absurdity | treating the impossible as a scheduling problem |
| Specificity | the wrong detail, delivered flatly. Specificity is most of comedy |
| Bureaucracy meeting mortal peril | forms, fees, and procedure at the worst moment |
| Two agendas that never align | both people leaving the conversation satisfied and wrong |

**Sources to avoid:** cruelty to a character the story does not respect · anything at the expense
of a group (`bias-guard` — humour is the most common vector) · pop-culture reference in secondary
worlds · the narrator winking at the reader · sustained slapstick, which does not survive prose ·
a character whose only function is comic relief.

## Rhythm

**Levity works as contrast.** A funny beat immediately before a hard one sharpens both; a chapter
of unbroken jokes flattens.

Placement that works:
- Early in a chapter, before the pressure builds
- After a heavy chapter, as the reader exhales — but with the cost still visible underneath
- Inside tension, as a character's coping mechanism, which *raises* tension rather than releasing it

Placement that fails:
- During the climax
- Immediately after a death or a real loss
- As the chapter's hook, unless the joke is also a threat

**Never puncture stakes.** If a joke makes the danger feel unreal, cut it. The test: after the
funny beat, does the reader still believe the MC could lose?

## Craft

- **Undersell.** The narration never signals that a line was funny. No character laughing to cue
  the reader.
- **The last word is the funny word.** Sentence order does most of the work.
- **Do not explain.** The beat after the joke moves on.
- **Comic characters get real arcs.** A character who is only funny is furniture.
- **Frequency**: in a `grounded` or `bleak` tone, a few beats per chapter at most. In a `wry`
  tone, humour is the voice and this skill governs its restraint instead.


## When to break these — `force: stylistic`

Placement rules here are **defaults, not gates**. The one that is not a default is the last line
of the self-check, which is `bias-guard`'s and is absolute.

Break the placement rules when the joke is doing something the rule cannot see:

- **A joke during the climax**, when it is a character's panic reaching for the only thing that
  works for them. The rule assumes levity releases tension; a badly-timed joke from a frightened
  person raises it.
- **A joke immediately after a loss**, when it is grief arriving wrong — which is how grief
  usually arrives, and is a far stronger beat than the paragraph of mourning it replaces.
- **The narrator being funny**, once, when the book's register is genuinely comic and the user
  asked for that. Then it is voice, not commentary, and `style.read_like` should say so.

The rule that does not bend: the stakes test. If the reader stops believing the MC could lose,
cut the beat whatever it was doing.

## Self-check

- [ ] Every funny beat belongs to a character, not the narrator
- [ ] Nothing is funny at the expense of a group
- [ ] Stakes survive the joke
- [ ] No joke during the climax or immediately after a real loss
- [ ] Nothing signals that a line was a joke
- [ ] Any comic character has a want and an arc
