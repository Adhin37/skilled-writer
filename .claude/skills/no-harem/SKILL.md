---
name: no-harem
description: Optional (default on). Keep love interests people with their own goals, and romantic attention reciprocal and reversible. Use on any romantic or attracted-to dynamic while enabled.
metadata:
  type: skill
  tier: optional
  when: optional.no-harem == on
  owns: [reciprocity]
---

# no-harem

**Gate.** Applies only if `novel.md` → `optional.no-harem` is `on`. If `off`, this skill does
nothing — but `bias-guard` still applies in full, and it is not toggleable.

On by default. The harem configuration is the corpus's most reflexive romantic default, and a
model will reach for it unprompted: characters accumulate around the protagonist, their arcs
collapse into wanting him, and nobody ever chooses anyone else.

---

## The rules

1. **At most one active romantic line at a time.** A previous one may be unresolved; it is not
   also active. Two women in love with the MC simultaneously is a plot only if the story is
   *about* that, and then it resolves rather than persists.

2. **Attraction is motivated and stated.** Name what draws each party, specifically. "She is
   beautiful" and "he is strong" are not motivations. "He is the only person who has ever told her
   the number instead of a comforting version of the number" is.

3. **Attraction is reciprocal or it is a subplot about rejection.** Unrequited attention that goes
   nowhere and is never addressed is set dressing for the MC's desirability. Either it is
   returned, or someone deals with the fact that it is not.

4. **Rejection is real and it sticks.** Characters may decline the MC. That decision holds. It
   does not soften over twenty chapters into acceptance.

5. **Every love interest passes the agency test** (`bias-guard`): she wants something that is not
   the MC and pursues it on the page. Ideally her goal costs her something to pursue alongside the
   relationship.

6. **Nobody is a reward.** Not for winning, not for power, not for kindness. A relationship is not
   an item acquired at the end of an arc.

7. **The MC is not universally attractive.** People are indifferent to him. Some dislike him for
   defensible reasons. Attention from everyone is not romance, it is wish-fulfilment scaffolding.

8. **Rivals are people.** A romantic rival wants the same person for their own reasons and is not
   thereby a villain, an idiot, or someone the plot will conveniently remove.

9. **No collection dynamics.** No character is added to the MC's orbit and then kept there
   inactive, appearing occasionally to demonstrate continued devotion.

## Detection — what this catches in a draft

- Two or more characters whose scenes exist mainly to register feelings about the MC
- A character introduced with an appearance inventory and a blush in the same chapter
- Any character whose want, stated in `bible/cast/`, is only about the MC
- A rejected character still orbiting fifteen chapters later with no arc of their own
- A cast where every named woman is romantically available and no named man is
- Jealousy scenes between characters that resolve without either of them changing

## If the user turns this off

They may want a genuine polyamorous or harem-structured story, and that is a legitimate choice.
It changes rules 1, 3 and 4 only. Rules 2, 5, 6, 7, 8 and 9 still hold, because those are
`bias-guard` requirements in romantic clothing: everyone involved has goals, agency, interiority
and the ability to leave. A well-written multi-partner story is *harder*, not easier — each
relationship needs its own reason to exist, and the arrangement itself needs to be examined rather
than assumed.

## Self-check

- [ ] One active romantic line, or a clearly-named reason there are more
- [ ] Each party's attraction is specific and stated
- [ ] Every love interest has an on-page goal unrelated to the MC
- [ ] No rejection has quietly reversed
- [ ] Nobody was awarded to anyone
- [ ] Somebody in this novel is indifferent to the MC
