---
type: audit-card
owner: pov-switch
dispatcher: revision-pass
pass: "2"
pass_kind: mechanical
description: The viewpoint held, and the switch was legal
when: pov.mode != single
---

# pov-switch — audit card

Opened by `revision-pass` **Pass 2** only when `pov.mode` is not `single`. In a single-POV novel
this card never opens and the one rule that still applies — nothing on the page exceeds the POV
character's knowledge — is audited by `narrator-voice`.

## The gate

> **Is there a paragraph that knows something this viewpoint cannot?**

Head-hopping is `narrator-voice`'s concept and its card catches the sentence-level version. This
gate is the chapter-level one: a scene that reports another character's feeling, intention or
private history as fact has changed viewpoint without saying so, and the reader feels it as the
prose going vague.

## Checks

- [ ] `novel.md` permits this switch at this granularity, and `label_switches` was honoured
- [ ] The switch passes at least one justification test — it is not here because the author
      wanted a scene the MC could not attend
- [ ] The new POV is identifiable from **voice** within two sentences, before any label
- [ ] What this character notices differs from what the previous POV would have noticed in the
      same room
- [ ] Their thought unit is not the MC's, and it is the source of this chapter's metaphors
      (`bible/cast/_voices.md` §3)
- [ ] No mid-scene switching anywhere in the chapter
- [ ] The MC has not been absent for more than two chapters
- [ ] If this is an antagonist POV, `pov.antagonist_pov` allows it and the chapter did not spend
      the tension the MC's ignorance was holding

## Where it fails most often

| symptom | what it actually is | go to |
|---|---|---|
| The switch was needed to show information | exposition wearing a viewpoint | give the ignorance to someone who has it, and keep the POV |
| The new POV narrates in the MC's rhythm | the thought unit was never set | `voice-separation` |
| Switches are getting more frequent | the novel is drifting toward ensemble without deciding to | `SKILL.md` §Choosing the mode — change the config or stop |

## What it looks like when it lands

The chapter opens in Maro's head and the reader knows inside two sentences, before the label,
because he is counting something. What he notices about the room is the rent on it. Wren noticed
the salt line.
