---
name: mtl-detox
description: Strip machine-translation artifacts and structural cliches - stock phrases, crowd reactions, the face-slap loop, rank recitals. Use on every chapter inside revision-pass, and while drafting.
metadata:
  type: skill
  tier: craft
  force: stylistic
  when: always
  owns: [banned-phrase-list, translationese]
---

# mtl-detox

Most serialized fiction in the training corpus arrived through machine translation from Chinese
web platforms. That corpus supplies the format's genuine strengths — momentum, hooks, visible
progression, generous chapter counts — and also a set of defects that read as "AI wrote this" to
an English-language audience.

This skill keeps the engine and removes the residue. It is **not** a judgement about a culture or
its literature: the defects here are artifacts of *bulk machine translation and web-serial
incentive structures*, not of Chinese fiction, which at its best has none of them. What we are
stripping is the translationese and the treadmill.

Run on every chapter. Not optional.

---

## What lives in `references/`

| file | open it when |
|---|---|
| `references/catalogues.md` | `sw lint` is unavailable, or a phrase feels like an artifact and you want the full banned-phrase and structural-cliché lists |

`sw lint` searches both catalogues on every chapter. Open the file when it cannot run, or when
you are deciding whether a hit is a defect — which is the half it does not do.

## Part 3 — Detox pass procedure

Run over the drafted chapter:

```bash
python3 scripts/sw.py lint novels/<slug> -c <n>
```

Steps 1-3 are that command: it holds the whole banned list above, counts exclamation marks and
question marks outside dialogue, and reports each with its line. Steps 4-8 are structural and
are yours — no script can see a crowd-reaction block or price a confrontation. Without Python,
search for each phrase by hand.

1. Search the draft for each banned phrase. Rewrite, don't substitute. The linter finds the
   string; **you** rewrite the sentence, because swapping a synonym is the failure this list
   exists to prevent.
2. Count exclamation marks outside dialogue. Target zero.
3. Count rhetorical questions in narration. Target zero, ceiling one.
4. Find every paragraph describing a group reacting to the POV character. Delete or individuate.
5. Find every passage explaining the power system. Is it in a character's mouth, with a reason,
   under 60 words? If not, cut it.
6. For every confrontation: name what it cost the winner. If nothing, apply a replacement above.
7. For every antagonist present: name what they want and what they are good at. If you cannot,
   fix the character before the sentence.
8. Read the chapter's last 200 words aloud. Translationese hides in the rhythm — flat
   subject-verb-object chains of uniform length. Vary or rewrite.


## When to break these — `force: stylistic`

The banned list is a **default, not a gate**, and it may be broken without owing the report a
reason.

A banned phrase is legitimate when it is **somebody's, on purpose**: a character who talks in
stock phrases is a characterisation, a narrator who does is the defect. Dialogue is the ordinary
case — people do say *you dare* — and the test is whether a different character in the same scene
would say it differently. In-world documents, proclamations and translated texts get the same
latitude for the same reason.

What has no latitude is the **structural** half: the face-slap loop, the crowd narrating how
impressive somebody was, the rank recital as narration, the paragraph saying one thing three
ways. Those are not phrasings, they are shapes, and a chapter built out of them is not fixed by
rewording. That half binds as `structural` regardless of this skill's declared force.

And the standing warning from `CLAUDE.md` §5: no phrase list is ever finished. Ban a tic and the
model's own register fills the hole with a new one, which is why `sw lint`'s echo check looks for
*repeated constructions* and not for words.

## Self-check

- [ ] Zero banned phrases
- [ ] Zero narration exclamation marks
- [ ] No crowd-reaction block
- [ ] No rank recital
- [ ] Every confrontation has a cost
- [ ] Every antagonist on the page wants something and is good at something
- [ ] No paragraph says the same thing three ways
