# voice-separation — the mirror clause

Open this only when a clone, avatar, double or body-snatch is on the page. It is the one exemption from the separation rules.

---

## 7. The mirror clause — clones, avatars, doubles

Copies of a person are **exempt** from §3. A duplicate is permitted to share the original's
fingerprint, body idiom and thought unit, in whole or in part — that is the premise, not a defect.

**Declaring one.** In the duplicate's profile frontmatter:

```yaml
mirror: rin              # the source character's slug
mirror_kind: clone       # clone | avatar | projection | doppelganger | body-snatch |
                         # split-self | time-double | copy-mind | shapeshifter
convergence: drifting    # identical | drifting | inverted
diverged_ch: 47          # the chapter they became separate people
```

Add a row to the mirrors block of `bible/cast/_voices.md`. If the double has a different body, they
are also `form_locked: true` with a stage row in `state/body.md` (`mc-design`).

| convergence | speech | body | thought | use for |
|---|---|---|---|---|
| `identical` | exact | exact | exact | a projection the original drives directly; a copy in its first chapters; an impostor who has not yet slipped |
| `drifting` | same fingerprint, diverging vocabulary and deltas | same idiom, new habits from a different life | same unit, different conclusions | any duplicate that has lived independently for more than a few chapters |
| `inverted` | the fingerprint pushed to an extreme the original never reaches | the same body used differently | same unit, opposite values | the evil twin; the self the MC refused to become |

### The four rules that make a double interesting

1. **Divergence starts at separation.** From `diverged_ch`, two copies accumulate different
   experiences, and different experiences produce different people. They drift at the duplicate's
   own `development_rate`. A duplicate who sounds identical after thirty chapters of a different
   life is a puppet — legitimate *if the story says so* (a driven avatar, a mind with no
   independent memory), and then say so on the page: someone notices that it never learned
   anything.
2. **Name the tell.** If the duplicate is meant to pass as the original, decide the one thing that
   does not copy — a reflex, a piece of knowledge, a habit acquired after the split, the way they
   handle being touched — and decide **who could notice it**. That is a plot device, and it should
   be planted before it is needed (`plot-threads`). If nothing fails to copy, state that
   deliberately: the horror is that there is no test.
3. **Keep them legible in a shared scene.** When two mirrors are on the page together, the reader
   must be able to tell which is speaking, from a physical tag, position, or a POV anchor — *or*
   the confusion is the intended effect and a character on the page is confused too. Never let it
   be an accident.
4. **The exemption is exactly this wide.** It covers characters with a `mirror:` field, on the
   channels their convergence level names, and nothing else. It does not license an ally, a
   student, a sibling or a rival to share the MC's voice. "He's like a younger version of me" is
   not a mirror; it is a cast with two of the same person in it.

---
