# Cast voice matrix

Maintained by `voice-separation`. **One screen. Load it before any scene with two or more
speakers.**

Sameness is a property of a *cast*, not of a character — you cannot see that two people sound
alike by reading their profiles one at a time. That is what this file is for. The values here are
copies of fields in each profile; the profile is the source of truth, this is the comparison.

| axis | values |
|---|---|
| **intel** | 1 ordinary · 2 sharp · 3 smart · 4 brilliant · 5 genius (the `mc-intel-meter` ladder) |
| **artic** | 1 points, cannot explain · 2 facts, no reasons · 3 ordinary · 4 fluent · 5 persuasive at will |
| **wit** | none · dry · warm · clowning · cruel — plus the pressure that triggers it |
| **heat** | flat · banked · quick · volatile |
| **turn** | default words per speaking turn. A number. Hold it |
| **hands** | the one thing their hands do |
| **pressure** | still · bigger · smaller · busy · closer · leaves |
| **first move** | what they reach for or look at first when the situation changes |
| **stance** | what they do about what this society expects of their gender: conforms-benefits · conforms-resents · exploits · defies-openly · defies-quietly · oblivious · enforces. Any character takes any value; two of the same gender should differ (`social-fabric/references/gendered-experience.md`) |

---

## 1. THE MATRIX

Tier A and tier B only. Tier C walk-ons get one off-default axis in `_extras.md` and no row here.

| character | tier | intel | artic | wit | heat | turn | hands | pressure | first move |
|---|---|---|---|---|---|---|---|---|---|

**The MC's row is the calibration point, not the ceiling.** Read down each column before adding
anyone. If a new character's row already exists under another name, change it.

## 2. THE THREE CHECKS

Run these against the table above, not against a chapter.

- **Straddle** — at least one character above the MC's intel tier, at least one below.
- **Wit budget** — at most two characters with wit other than `none`.
- **No duplicate triples** — no two characters sharing intel + artic + wit.

## 3. POV THOUGHT FIELDS

Only for `pov_eligible: true` characters. The thought unit is also the metaphor source that
`narrator-voice` draws on, so two POV characters sharing one will narrate identically however
different their dialogue is.

| character | thought unit | thought speed | facing an unknown |
|---|---|---|---|

`thought unit`: images · words · numbers · bodies · rules · people · money
`thought speed`: ahead of the scene · with it · one beat behind
`facing an unknown`: test it · avoid it · name it · ask someone · assume the worst

## 4. CONVERSATIONAL BLIND SPOTS

One per recurring character: the thing they cannot do that the MC does easily.

| character | cannot |
|---|---|

## 5. MIRRORS

Clones, avatars, doubles — the characters **exempt** from the separation rules. Empty in most
novels; delete the section if nothing in this book duplicates a person.

| character | mirror of | kind | convergence | diverged ch | the tell | who could notice |
|---|---|---|---|---|---|---|

`kind`: clone · avatar · projection · doppelganger · body-snatch · split-self · time-double ·
copy-mind · shapeshifter
`convergence`: identical · drifting · inverted

**the tell** — the one thing that does not copy, and therefore the plot device. If nothing fails to
copy, write `none — deliberate` so it is a decision rather than an oversight.

Divergence starts at `diverged ch` and accumulates at the duplicate's own `development_rate`. A
double who sounds identical after thirty chapters of a separate life is a puppet, and somebody on
the page should notice that it never learned anything.

## 6. DRIFT LOG

Once per arc: one recent line from each recurring character, read side by side. If the axes have
compressed toward the MC's, restore them and log it.

| arc | who drifted | toward what | restored how |
|---|---|---|---|
