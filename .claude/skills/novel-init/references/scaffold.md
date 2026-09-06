# novel-init — the scaffold procedure, defaults and failure modes

Open this at Step 3, when the interview is done and the workspace is about to be written — and the defaults table whenever the user declines to decide something.

---

## Step 3 — Scaffold

Copy the scaffold. Use paths relative to the repo root, never absolute ones — this repo is used
on both Windows and Linux.

```bash
python3 scripts/sw.py newnovel <slug>
```

This is the portable form: it needs no shell, refuses to overwrite an existing novel, rejects a
slug that is not kebab-case, and prints the tree it created. Failing that:

```bash
cp -r novels/_template novels/<slug>          # macOS / Linux / Git Bash
```

If neither is available, create the directories and write each template file out instead; the
tree is small and the file list is in `CLAUDE.md` §6. Do not rely on any one shell being present.

**Copy first, then read.** Do not read the template files before copying them — copy the tree, then
open only the file you are about to fill, one at a time. Reading all eleven up front costs a turn
each and teaches you nothing the copy did not already put on disk.

The copy step must be permitted. If the shell refuses it, say so rather than silently falling
back — a denied copy is a settings problem, not a reason to hand-write the tree.

Slug is the one `title-craft` derived in Step 2b — kebab-case, 4–5 words. **It is permanent.**
The title may change at a later arc boundary; the directory every path hangs off does not.
Never scaffold under `untitled`: if Step 2b was skipped, go back and run it.

Note for the user, once, at the end: `novels/` is gitignored except the template, so their book
is not committed to the toolkit repo by default.

Then fill in, in this order:

1. **`novel.md`** — every frontmatter field. No field left as a placeholder. `title`,
   `title_alternates` and `slug` come from Step 2b; paste the blurb `title-craft` wrote into
   `# Hook (platform blurb)` rather than writing a second one. Write the premise, tone
   references, themes and the ending target. Delete the `fanfic:` block for non-fanfic.
2. **`bible/world.md`** via `story-bible`. Enough to write 25 chapters, not a gazetteer.
3. **`bible/lexicon.md`** — names and terms invented so far, plus house style decisions.
4. **`bible/power-system.md`** via `power-system` (fantasy/scifi) or **`bible/canon.md`** via
   `fanfic-canon`. Delete the file that does not apply.
4b. **`bible/society.md`** via `social-fabric` — **after** step 4, never before: the six
   questions, and one propagation test taking the most important rule down into institution,
   market and household. This is the step that stops a spectacular magic system from sitting on
   top of generic medieval wallpaper. Keep it under 1,000 words; write only the social layer
   arc 1 actually enters.
5. **`bible/cast/`** — the MC's profile first, via `mc-design` + `character-profile`. Then the
   love interest via `lead-interest`, if there is one. Then 3–5 other characters who appear in
   arc 1, **each at its tier**: full profiles only for principals, the short file for supporting
   characters, and nothing at all for people arc 1 merely walks past — they get sketched when
   they are written. Keep `_character-template.md`, `_supporting-template.md` and the empty
   `_extras.md` in place; they are the references for future characters.
5b. **`bible/cast/_voices.md`** via `voice-separation` — a matrix row for every character written
   in step 5, filled in **together, as a table**, not one at a time. Then run
   `python3 scripts/sw.py cast novels/<slug>`, which checks both this file and step 5c's, or run
   the three checks in §2 of that file by hand: the cast straddles the MC's intel tier, at most two characters have wit, and no
   two rows share intel + articulacy + wit. This is the step that decides the book will not be one
   voice in several costumes, and it is far cheaper here than in chapter 40. Delete §5 (Mirrors) if
   nothing in the novel duplicates a person.
5c. **`bible/cast/_competence.md`** via `competence-map` — the same move for knowledge. A row per
   character: domain, level, and **where the edge is**, plus a referral each, and §3, *what nobody
   in this cast knows*. Fill it as a grid so the distribution is visible: does anyone read, who is
   the only one who can fight, what would this cast have to buy? Unlisted is `none`, which is what
   gives arc 1 its errands and its wrong answers. Fill §4 only if the book contains gods, immortals,
   cultivators or artificial minds — their boundary and their access bound are required fields, not
   decoration, because an unbounded oracle dissolves every mystery you have planned.
6. **`plan/timeline.md`** via `timeline-engine` — the drivers with their reaction profiles, the
   world track for arcs 1–3, standing clocks, and the point-of-no-return watch. For fanfic, the
   canon track and the first deliberate divergence. Keep this coarse for original fiction: the
   antagonist's plan plus two or three clocks is enough.
7. **`plan/arcs.md`** via `chapter-plan` — arc 1 in full, arcs 2–3 in one line each.
8. **`plan/chapters.md`** via `chapter-plan` — the first 12 rows, fully specified.
9. **`state/`** — initialise `continuity.md` book digest, seed `threads.md` with the threads
   arc 1 opens (including the romance thread if there is one), seed `growth.md` with every tier-A
   character at rung 1 and every tier-B at `B1`, set the calendar in `timeline.md`. If `mc.form_locked` is true, fill in
   `body.md` completely — every stage, its limits and its transition chapter — before chapter 1 is
   written. If nothing in the novel changes form, delete `body.md`. If `mc.foreknowledge` is set,
   fill `foreknowledge.md` — the grain, the inventory of what the MC believes, and §5's arc of the
   advantage with the inventory scene, the first win and the first failure placed **in that
   order**. If nobody knows the future, delete `foreknowledge.md`.

## Defaults when the user won't decide

| field | default | why |
|---|---|---|
| pov.mode | `single` | Cheapest to keep consistent, strongest reader attachment. |
| mc.intel_tier | `3` | Smart enough to be satisfying, no plot-engineering burden. |
| chapters.length_band | `1500-2600` | A printer's note, never a gate. Do not raise it as a question. |
| opening.anchor_by_ch | `1` | The reader is oriented before they are threatened. |
| mc.foreknowledge_grain | `major-beats` | If the MC knows the future at all. Precise enough to plan on, loose enough to be wrong. |
| arc_length | `25` | Roughly a month of daily releases. |
| narration | third-limited, past, close | Widest tolerance, easiest voice to hold. |
| mc.origin | `native` | No form ledger, no foreknowledge decay; the MC learns as the reader does. |
| mc.golden_finger | `none` | An advantage is easy to add at chapter 30; removing one is not. |
| romance.configuration | `undecided` | A lead chosen from the existing cast at chapter 20 is almost always better than one designed cold. |
| timeline.reactivity | `3` | The world notices and adapts without becoming a grind. |
| ending.tone | `hopeful` | Never default the *contract* — ask for it in the user's words. |
| title | never defaulted | Always show three screened candidates. `"Untitled"` reaching the scaffold is a bug. |
| optional | only `no-harem` and `combat-choreography` on | Adding mechanics later is easy; removing them mid-serial is not. |

Never default `mc.gender` — ask it. Never infer `romance.lead_gender` from the MC's gender without
offering every configuration.

## Failure modes

- **Don't** interrogate. If the user gives short answers, stop asking and start building; they
  will correct a draft far more readily than they will fill in a form.
- **Don't** accept "make it like <popular novel>" as a spec. Ask which single element they want
  borrowed, and write that element down in tone references.
- **Don't** invent a 5000-word bible. Everything in `bible/` must be needed by arc 1 or by a
  decision you have already made.
- **Don't** ship a world whose central rule changed nothing about how people live. One
  propagation test at init is the minimum (`social-fabric` §2), and it costs six lines.
- **Don't** leave `blind_spots` empty. Two minimum, or `mc-intel-meter` cannot do its job.
- **Don't** build a starting cast where everyone is as quick and as articulate as the MC. Fill
  `_voices.md` as a table and check the three rules in §2 — somebody below the MC's tier, at most
  two funny people, no duplicate intel/articulacy/wit triples. Left undone at init, this defect is
  invisible for twenty chapters and then permanent.
- **Don't** scaffold before the book has a name. The slug is derived from the title and is
  permanent; a workspace built under `untitled` is a directory rename later for no reader-visible
  gain. And **don't** ship a fanfic whose title omits the source work — it is the search term.
- **Don't** give anyone an open-ended competence. Three domains for the MC, two for a principal,
  one for a supporting character, and everything unlisted is `none`. A cast where everyone can
  answer everything has no errands, no referrals and no reason for half its members to exist.
