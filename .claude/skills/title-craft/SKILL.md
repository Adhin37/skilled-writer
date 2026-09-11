---
name: title-craft
description: Name the book and write the platform blurb. Use once during novel-init, and again only at an arc boundary when the story has outgrown its name.
metadata:
  type: skill
  tier: core
  when: always
  owns: [title, blurb, slug]
---

# title-craft

Runs inside `novel-init`, **after Round F and before the scaffold** — the slug is derived from the
title, and there is no rename path: `sw.py newnovel` refuses to overwrite an existing directory,
and renaming afterwards means moving the tree by hand and fixing every path that points at it.

Output: `title:` and `title_alternates:` in `novel.md`, the **slug** the whole workspace is built
under, and the `# Hook (platform blurb)` body section of `novel.md`.

**Why this is a skill and not a line in the interview.** `story-opening` exists because chapter 1
is a conversion event — about 60% of readers who open it reach chapter 2. The title and the blurb
sit one step earlier in the same funnel and are read by *everyone who never opened chapter 1 at
all*. A reader in a library grid gives the title about two seconds and the blurb about fifteen. A
book with a good chapter 1 and a noun-stack title is a book nobody clicks, and no amount of
revision downstream recovers it.

The order is fixed: **title, then blurb, then slug.** The blurb is written against the title so
the two promise the same book; the slug is derived last so it is derived from something final.

---

## What lives in `references/`

| file | open it when |
|---|---|
| `references/listing-kit.md` | the listing step: tags, cover brief, cadence, launch stock — and again when a secondary element becomes prominent enough to earn its tag |
| `references/fanfic-and-renaming.md` | the novel is fan fiction (the source-in-title rule is mandatory there), or an arc boundary has left the title naming a state the story has left |

## The three jobs

Every candidate is judged on all three. A title that does two is a rename waiting to happen.

| job | the reader's question | how it is answered |
|---|---|---|
| **Shelf** | what kind of book is this? | one word carrying genre freight — *Shinobi*, *Dungeon*, *Necromancer*, *Ledger*, *Void* |
| **Promise** | what pleasure am I being offered? | the specific thing, not the category: *levelling up* is a shelf, *levelling up alone* is a promise |
| **Hook** | why this one and not the four beside it? | a contradiction, a refusal, an incongruity, or a destination stated too boldly |

*He Who Fights With Monsters* does all three in six words. *Shadow Blade Chronicles* does none in
three.

## Step 1 — Assemble the ingredients

**Ask nothing.** Everything needed already exists by the end of Round F. Pull it and write it
down before generating anything:

- the premise in the user's own words (Step 1 of `novel-init`)
- `genre` and `subgenre` — the shelf word comes from here
- `mc.origin` and `mc.golden_finger` — the incongruity usually lives in one of these
- `opening.promise` — the contract the title must not contradict
- `ending.contract` — where this is going, which is where an escalation title points
- `content.tone` — a wry book must not get a portentous title
- `fanfic.source`, if this is fan fiction — see Step 3, it is mandatory

`opening.promise` is written in Round D from the premise, so it always exists by the time you run.
The blurb you write in Step 5 is the *later* artifact, and `novel-init` re-checks the promise
against it before the scaffold. If the two promise different books, the blurb changes: the user
confirmed the promise out loud and has not yet seen the blurb.

## Step 2 — Five candidates, five strategies

Generate **five**, one per strategy. This is the anti-collapse rule: asked for five titles
without constraint, a model produces five rewordings of the same idea, and the user picks the
least bad rather than choosing between real alternatives.

| # | strategy | shape | example |
|---|---|---|---|
| 1 | **Role + fracture** | the MC's function, broken by one word that shouldn't be there | *The Necromancer Who Buried Nothing* |
| 2 | **First-person claim** | the MC states an intent, a refusal, or a flat fact | *I Refuse to Feed the Dragon* |
| 3 | **The mechanism** | the story's central rule or object, as a noun phrase | *The Ledger of Small Debts* |
| 4 | **Understated flat** | one or two plain words, dry, confident, no ornament | *Delve* · *Rangemaster* |
| 5 | **The destination** | the thing the reader is being promised they will reach | *The New God of Shinobi* |

Two hard constraints on the set:

- **No two candidates share a strategy.** Five of row 1 is not five candidates.
- **No two candidates share their first noun.** The first two words carry the click in a grid;
  if all five open on *Shadow*, the user is choosing a suffix.

Strategy 4 will feel too small every time. Generate it anyway — understated titles outperform
their apparent confidence, and it is the only row that reliably survives the truncation test.

## Step 4 — Screen the five

Run every candidate through all seven. A candidate failing 4 or 6 is dead; the others are
negotiable and the failure is reported to the user rather than silently fixed.

| # | test | how | fail looks like |
|---|---|---|---|
| 0 | **Length** | count the characters | over 60 for the whole line, or over 40 after a fandom prefix — the grid will not give them back |
| 1 | **Truncation** | cut it at 30 characters | *Shadow Blade Chronicles: Lega…* — the surviving half says nothing |
| 2 | **Say it aloud** | could a reader recommend it in a sentence and could the friend spell it into a search box? | apostrophes, invented spellings, three-word abstract nouns |
| 3 | **Collision** | name three existing works you would confuse it with | naming three easily is a fail |
| 4 | **Promise match** | read it beside `opening.promise` | a title promising a different book than the page delivers — the worst failure here, because it converts and then loses the reader at chapter 2 feeling lied to |
| 5 | **Survives the arc** | is it still true at chapter 100? | a title naming a state the MC leaves at chapter 30 |
| 6 | **Noun-stack** | delete *Chronicles · Saga · Legacy of · Rise of · Ascendant · Eternal · of Destiny* | if nothing was lost, they were filler and the title underneath is the real candidate |

Keep the three that survive best. If fewer than three survive, generate again — do not present a
failed candidate as a courtesy option.

## Step 5 — The blurb

Written **after** the title is chosen, against it. 60–120 words, three moves, and it ends on a
threat or a question — never on a summary.

1. **Anchor** — who, where, and what kind of world, in the first sentence. Same rule as
   `story-opening`: the reader is oriented before they are threatened. For fanfic, the sentence
   also says *which story and roughly when*, and the divergence point is named by the end.
2. **Want and obstruction** — what the MC is after and the specific thing in the way. One
   concrete thing, not a faction and a prophecy and an ancient evil.
3. **Turn** — the cost, the trap, or the question. This is the last line and it is the only one
   most readers finish.

Hard rules:

- **At most two proper nouns beyond the MC's name.** A blurb naming six invented things is a
  glossary, and a reader who cannot pronounce a name will not carry it into chapter 1.
- **No rank ladder.** Not *"the nine Sundering Tiers"*, not *"from Mortal to Ascendant"*. Power
  reaches a reader as cost, here as much as on the page.
- **No `mtl-detox` stock phrasing.** *little did he know* · *unbeknownst to* · *little did they
  realise* · *but fate had other plans* · *his life would never be the same*. Full list in
  `mtl-detox`; the blurb is where they cluster worst because it is the most marketing-shaped text
  in the repo.
- **No rhetorical question stack.** One question can end a blurb. Three is a shrug.
- **No tag brackets.** `[LitRPG] [Progression] [Weak to Strong]` belongs in the platform's tag
  field, not the prose. Say what they mean or leave them out.
- **Promise only what the first ten chapters deliver.** The blurb is `opening.promise` in retail
  form, and `plot-threads` holds the page to it by `promise_touched_by_ch`.
- `bias-guard` applies here exactly as it does to prose. A blurb is the most-read text in the
  novel; a lazy villain shorthand in it is the most-read defect in the novel.

## Step 6 — Present, pick, record

Show the user **three titles**, each with one line naming what it promises and what it costs —
the same shape `mc-design` uses for "Surprise me", and for the reason it gives there. Lead with
your recommendation.

```
1. Naruto: The New God of Shinobi   (Recommended)
   Promises the destination hard and early. Searchable, and the escalation is the draw.
   Costs you: you now owe the reader that ending, and the title spoils the shape of the arc.

2. Naruto: The Ledger of Small Debts
   Promises a quieter, mechanism-led story about what favours cost in a shinobi village.
   Costs you: a smaller shelf. Readers browsing for power fantasy will scroll past it.

3. Naruto: Refuse the Will of Fire
   Promises a refusal — the reader knows immediately what the MC is against.
   Costs you: it reads as edgy if the book is not actually about that argument.
```

Then the blurb underneath, once, in full. The user reacts to a written blurb; they do not react
to an offer to write one.

They may also write their own title. If they do, run it through Step 4 anyway and **report any
failures without overriding them** — it is their book. The one exception is the fanfic source
rule in Step 3, which is a discoverability fact rather than a taste question: say plainly that
the title will not be found by fandom search, then do as they ask.

Record:

```yaml
title: "Naruto: The New God of Shinobi"
title_alternates:                     # the runners-up, kept for a rename at an arc boundary
  - "Naruto: The Ledger of Small Debts"
  - "Naruto: Refuse the Will of Fire"
slug: "naruto-new-god-of-shinobi"
```

And write the blurb into the `# Hook (platform blurb)` section of `novel.md`.

## The slug is permanent, the title is not

The slug names the directory every path in the workspace hangs off. Once chapters exist, renaming
it means moving the tree and rewriting whatever referenced it, and it buys nothing a reader ever
sees. **The slug is decided once, here, and never changes.**

Derive it: kebab-case of the title, articles and prepositions dropped, **4–5 words maximum**.

| title | slug |
|---|---|
| *Naruto: The New God of Shinobi* | `naruto-new-god-of-shinobi` |
| *The Necromancer Who Buried Nothing* | `necromancer-buried-nothing` |
| *Delve* | `delve` |

Keep the fandom prefix in a fanfic slug — it is what makes a workspace legible at a glance when
several novels sit side by side.

## Self-check

- [ ] Five candidates generated, one per strategy, no two sharing a strategy or a first noun
- [ ] All five screened on all seven tests; the three presented are the survivors
- [ ] Test 4 run explicitly against `opening.promise` — title and promise describe one book
- [ ] If `genre: fanfic`: `fanfic.source` is in the title line, in its most-searched form
- [ ] Whole title ≤ 60 characters; the part after a fandom prefix ≤ 40
- [ ] Three options presented with what each promises **and** what each costs
- [ ] Blurb written after the title, 60–120 words, anchors before it threatens, ends on threat or question
- [ ] Blurb: ≤ 2 proper nouns beyond the MC, no rank ladder, no tag brackets, no stock phrases
- [ ] Blurb promises only what the first ten chapters deliver
- [ ] `title`, `title_alternates` and `slug` recorded in `novel.md`; blurb in `# Hook`
- [ ] Slug is 4–5 words, kebab-case, and understood to be permanent
