# prose-quality — the house style

Open this when `sw lint` reports `house-style`, `em-dash` or `closer-sameness`, when a chapter
reads as machine-made and no banned phrase explains why, or before revising the first chapter of
a new novel.

---

## What this file is for

The cut list below used to be a list of stock phrases. It stayed, at the bottom, because those
phrases are still worth cutting — but they are not what makes this toolkit's output read as
AI-written, and an earlier version of this file already named two of the real tells and was
ignored anyway.

Benchmark run #2 is the evidence. Five chapters, 7,302 words, `status: revised`, zero MTL hits,
zero cut-list phrases — and a reader flagged the novel as AI-generated inside a page and priced
it at one star. The problem was never slop. **Ban xianxia cliché and what fills the vacuum is
this model's own literary default**, which is a narrower and more recognisable fingerprint than
the cliché was, because every model of this family writes it.

So the disease has one name: **uniform density.** Every sentence carries subtext. Every scene
ends on a small ironic withholding. Nothing is ever allowed to just say a thing. The individual
constructions below are *good writing* — that is exactly why they survive revision, and exactly
why they are dangerous. What kills a chapter is that there is no third gear.

---

## The seven tells, measured

Counts are from run #2 unless stated. `sw lint` reports each as a **note** and the aggregate rate
as a warn; none is a defect, because any one instance is fine.

| tell | what it looks like | run #2 |
|---|---|---|
| **The antithesis** | *"It was weather, not prophecy."* · *"Not relief."* · *"this one was confirmation, not ease"* | 18 in 7.3k words |
| **The em-dash appositive** | A clause, then a dash, then a noun phrase re-explaining it: *"took Suzune's slip first, the small, automatic courtesy of a captain who still remembered which of her people didn't waste her time."* | 62 dashes; 11.4/1k in ch1 |
| **The aphoristic close** | A scene ends on a portable generalisation: *"A promise kept was one data point. It was not yet a pattern."* | nearly every scene break |
| **The abstract as object** | *"turning eight years of careful, controlled arithmetic over in her hands"* | recurring |
| **The stage direction** | *"A beat."* written into the prose as if it were a script | 4× in ch5 alone |
| **The triple hedge** | *"she did not hear — could not have heard, and did not need to —"* | ch4's closing line |
| **The repeated tag** | *"in the same flat register she told herself everything in now"*, reused across chapters as a substitute for characterisation | 3 chapters |

### Why they cluster

They are all the same instinct: **refusing to commit.** The antithesis defines by exclusion, the
appositive qualifies what was just said, the aphorism converts a moment into a lesson, the hedge
takes back the claim inside the sentence that makes it. A narrator who never commits is a
narrator with one attitude, and one attitude for 7,000 words reads as a machine.

---

## The fix is positive, and it is the only one that works

Cutting tells makes prose *emptier*, not better. A chapter that removes 18 antitheses and adds
nothing has the same problem with fewer commas.

**Write plainly on purpose, in the same chapter.** Some sentences must carry information and
nothing else. Somebody says a thing and means it. Something is described because it is there.

> *The rice was untouched. The blanket was still folded on the bed.*

That is run #2's own prose, and it is the best writing in chapter 5, because for two sentences
the narrator stops performing. The chapter needed forty more like it.

A rough working shape, not a quota to hit:

- **A third of the chapter should be plain.** No dash, no reversal, no irony, no lesson.
- **One scene per chapter closes flat** — on an action or a line of speech, not on a reflection.
- **The narrator is allowed to be wrong, blunt, or bored.** Range is what an author has and a
  register does not.

There is no script for this and there will not be one. The first version of `sw lint` scored the
share of syntactically simple sentences and rated *"It was not yet a pattern."* as plain — the
house aphorism is short and simple, so shape cannot see it. This one is yours to judge.

---

## Checking your own draft

1. Read the last line of every scene. If more than one is a short withheld beat, rewrite the
   others. (`sw lint` flags this across chapters as `closer-sameness`.)
2. Find three sentences that exist only to deliver information. If there are none, that is the
   finding.
3. Count dashes in one page. Over about four per thousand words the appositive has become the
   default connector.
4. Read one page aloud. If every sentence lands with the same small click, the pitch is flat.

---

## The old cut list — still true, still worth a sweep

*a mix of X and Y* · *a testament to* · *something shifted in the air* · *the weight of X settled
over* · *a moment that stretched* · *she couldn't shake the feeling* · *little did she know* ·
*for the first time in a long time* · *a silence stretched between them* · *emotions warred within
her* · *the air was thick with tension* · *a chill ran down his spine* · *time seemed to slow* ·
*he let out a breath he didn't know he was holding* · *this changes everything*

| shape | example | fix |
|---|---|---|
| The tricolon habit | "It was cold, it was quiet, and it was wrong." | Two items, or four. Three is the model's default cadence. |
| Sentence-length monotony | Five clauses of eleven words in a row | `sw lint` reports it as `sentence-rhythm`. |
| Every paragraph opening on the subject | "She did… She turned… She waited…" | Reported as `para-opening`. |
