---
type: reference
owner: social-fabric
description: money at the scale of a scene - wages, prices, debt - so that a stake can have a number on it
---

# social-fabric — prices, wages and stakes with numbers

Open this when a scene turns on what something costs, when the MC acquires or loses money, or
when the stakes in an arc are financial and keep coming out vague.

Question 2 of the six answers what wealth is *made of*. This file answers what things **cost**,
which is a different question and the one a scene needs. A story where money is mentioned but
never quantified has no economic stakes, only economic atmosphere — and readers can tell, because
nothing the characters buy ever prevents them buying something else.

---

## The anchor wage

**Set one number and derive everything from it.** One line in `bible/society.md`:

```
anchor   a labourer earns 8 coppers a day; 100 coppers = 1 silver; 20 silver = 1 gold
```

Then every price in the novel is expressible in **days of ordinary work**, which is the unit a
reader actually feels. *Two silver* means nothing. *Three weeks' wages* means everything, and it
means the same thing in every culture a reader has ever lived in.

Fill in six prices once, and only these six. Adding a twenty-row table is worldbuilding for its
own sake, and `world-texture`'s budget will never let most of it onto the page anyway.

| thing | in days of work | why this one |
|---|---|---|
| a day's food | ~0.3 | the floor; makes hunger arithmetic |
| a night's lodging | ~0.5 | the commonest transaction a travelling character makes |
| the tool of the MC's trade | 20–60 | what losing it costs, in a number |
| a month's rent or its equivalent | 8–12 | the recurring pressure |
| the cheapest thing from the power system | 100+ | this is what makes the system *scarce* |
| a bribe that works | 30–90 | the price of the shortcut, every time it is offered |

The last two are the ones that do plot work. If the cheapest healing costs a year's wages, the
reader understands the world's cruelty without a word of narration — and every scene where
somebody is hurt now has a second question in it.

## The three rules that make it load-bearing

**Prices are stable, or the change is a plot event.** A loaf that costs differently in chapter 40
because the scene needed it is the economic version of a rule bending for one scene. If a price
moves, somebody caused it and somebody profits.

**Everyone knows the price of their own life and nobody knows anyone else's.** A character
quoting the cost of something outside their world is a competence violation wearing a purse
(`competence-map`). The noble does not know what bread costs. That is characterisation, and it is
free.

**Money is a way of losing, not only of having.** The stakes come from debt, obligation, and the
thing that must be sold. What a character *cannot* buy is the useful number.

## Debt is better than poverty

Poverty is a condition and it is static. **Debt is a deadline with a person attached**, and it
gives you a creditor who wants something legible, a date, an escalation ladder and a reason the
MC cannot simply leave. Where a story needs financial pressure, an obligation to a named person
outperforms a low balance every time (`conflict-engine` owns the ladder it climbs).

Record the terms: to whom, how much in days of work, by when, and what happens on the day it is
not paid. That last one is the plot.

## Reaching the page

Almost none of this is narrated. It arrives as:

- **A refusal.** Somebody cannot afford the thing, and says so in a way that prices it.
- **A comparison.** *He had not seen a gold coin since the funeral.*
- **A substitution.** The cheap version, the borrowed one, the one that is the wrong size.
- **An argument about a small sum**, which is how readers learn what a small sum is.
- **What somebody does for money** that they would rather not (`character-profile`).

One priced detail per chapter is plenty, and fewer as the book goes on — see §The curve. The
table exists so that the one is consistent with the last forty, not so that the reader learns
the currency.

## The curve — money stops deciding things

`means.shape: fades` is the default because it is what the genre does. A protagonist who begins
with nothing is blocked by prices constantly in the first arc and barely notices them by the
fifth, and the part worth getting right is that **the prices did not move** — the rule above
forbids that. What moved is the MC.

So `means.background_by_arc` does not change how often money appears. It changes what money is
allowed to *do*:

| where | what a price may do | on the page |
|---|---|---|
| before the arc named | stop the MC getting what they want | she counted it twice and walked past the door anyway |
| after it | cost them something they no longer feel | she paid the man at the door without looking at her hand |

The coin has not left the book. It has stopped being the obstacle, and the obstacle has moved up
the ladder `conflict-engine` owns — what the MC stands to lose is no longer a thing they own. A
chapter still solving its problem with a purse late in the book owes the reader a climb it never
wrote.

`flat` is a real answer for a story about staying poor, `inverts` for one where the MC acquires
enough to be ruined by it, and `none` for a book in which nobody ever counts.

## When money eats the book

The opposite failure, and the likelier one once a writer has been told that money matters. Four
signatures:

- **Every scene is a transaction.** Somebody buys, sells, haggles or is charged in all of them.
- **The arc's goal is a number going up.** A target sum is a quest marker wearing a stake's coat.
- **The narrator converts.** Everything gets valued, including what nobody present would price.
- **A win is reported as a balance.** The chapter ends richer and that is the news.

Said in the positive, which is the useful direction: **money is what stops a scene, not what
drives one.** Someone who wants the thing and cannot pay is a scene. Someone who wants money is an
errand.

Unless the book is about the errand. A merchant story, a heist, a debt-bondage plot — there the
acquiring *is* the plot, and everything above describes the genre rather than a defect in it.

## Who understands money

Financial sense is a domain like any other and belongs in the grid at `bible/cast/_competence.md`,
declared with an edge, and absent where the character does not have it — `competence-map` owns
that grid and the rule that an omission is not a blank cheque. Give the MC a row. An MC who prices
everything correctly in a world they reached last week has been handed a competence nobody sold
them.

The viewpoint half is already an axis. `_voices.md` records a `thought unit` per POV character and
`money` is one of its values (`voice-separation`). A narrator who thinks in prices reaches for
what a thing cost; one who does not will describe the same object and never raise it. That one
field does more than a paragraph about where they grew up.

## When the central rule is the economy

If the power system is *itself* scarce and tradeable — spirit stones, mana crystals, credits — it
is a currency, and it obeys everything above plus one more rule: **name who issues it and who
would lose by its value changing.** A resource everybody wants, with no issuer and no interested
party, is a game item. The propagation test in §2 of the skill body is where that gets worked out.
