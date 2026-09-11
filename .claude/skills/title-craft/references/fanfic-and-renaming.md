---
type: reference
owner: title-craft
description: the novel is fan fiction (the source-in-title rule is mandatory there), or an arc boundary has left the title naming a state the story has left
---

# title-craft — the fanfic rule, renaming, and failure modes

Open the fanfic rule for any fan fiction — it is mandatory there. Open renaming only at an arc boundary, when the title names a state the story has left.

---

## Step 3 — The fanfic rule

**If `genre: fanfic`, the title must carry `fanfic.source`. This is not optional and not a style
preference.** Readers browse fan fiction *by fandom*: the source name is the search term, the
filter, and the entire reason a stranger stops scrolling. A fanfic whose title omits it is
invisible to the only audience it has.

Default form — **prefix, colon, title**:

```
Naruto: The New God of Shinobi
```

| form | when | example |
|---|---|---|
| **Prefix + colon** *(default)* | almost always | *Naruto: The New God of Shinobi* |
| **Embedded** | only when a canon proper noun sits naturally inside the title *and* is as searchable as the source name | *The Hokage Who Stayed Dead* · *Reborn in Konoha* |
| **Prefix + embedded** | never — it stutters | ~~*Naruto: Reborn in Konoha*~~ |

Choose embedded only if you can name the search term a reader would type and point to it in the
title. *Konoha* qualifies. *Hogwarts* qualifies. A minor character's name does not.

Use the **source's most-searched name**, not its most correct one — the form on the anime/manga
cover a reader would recognise, matching `fanfic.source`. If the work is known by two names, use
the one the fandom types.

Keep the whole line short: the prefix eats characters that the grid will not give back. Aim for
**≤ 40 characters after the colon.**

## Renaming later

`title:` may change. This is a one-time skill by default, but a serial that has found itself at
chapter 40 sometimes needs a name that fits the book it actually became.

Re-run **only at an arc boundary**, and only when the current title fails test 5 — it names a
state the story has left. Then: pick from `title_alternates` or generate a fresh five, update
`title:`, add the old name to `title_alternates`, rewrite the blurb against the new title, and
**leave the slug alone.** Say once that published platforms treat a rename as a discoverability
reset, so it is worth doing early or not at all.

## Failure modes

| pattern | example | why it fails |
|---|---|---|
| **The noun-stack** | *Shadow Blade Chronicles: Legacy of the Eternal Flame* | interchangeable with four hundred others; every word is genre wallpaper |
| **The abstract** | *Ascension* · *Requiem* · *Legacy* | no shelf, no promise, and unsearchable — a reader cannot find it again |
| **The MTL literal** | *The Strongest Big Boss Villain's Runaway Wife* | the corpus artifact `mtl-detox` exists to strip; it signals a translation, not a book |
| **The spoiler** | naming the twist, the betrayal, or the final form | sells one surprise and spends it before chapter 1 |
| **The in-joke** | a term the story invents at chapter 40 | means nothing at the only moment it has to work |
| **The bait** | a grimdark title on a cosy book | converts, then loses the reader at chapter 2 feeling lied to — worse than a dull title, and it earns reviews that say so |
| **The unsayable** | apostrophes, invented orthography, four abstract nouns | cannot be recommended out loud, which is how serials actually spread |
| **The untitled** | `title: "Untitled"` reaching the scaffold | shipping this is the bug this skill exists to prevent |
