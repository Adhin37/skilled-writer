---
type: reference
owner: competence-map
description: "the character is a god, an immortal, a cultivator with centuries, or an artificial mind — knowledge_scope: broad"
---

# competence-map — the broad-knowledge clause

Open this only for a god, an immortal, a cultivator with centuries, or an artificial mind — anyone whose knowledge_scope is broad.

---

## 6. The broad-knowledge clause — gods, immortals, cultivators, ASI

Some settings contain minds that genuinely do know enormously more than a person, and §1 must not
flatten them into a blacksmith with a long memory. Declare it in the profile:

```yaml
knowledge_scope: broad      # narrow (default) | broad
scope_kind: domain-god      # domain-god | long-lived | artificial | borrowed
scope_shape: ""             # what is actually broad, in one sentence
scope_boundary: ""          # what still bites, in one sentence — required
```

**Even omniscience has a shape, and the shape is the character.**

| kind | what is genuinely broad | the boundary that still bites |
|---|---|---|
| **domain god** — of wisdom, war, the harvest, the sea | everything inside the domain, natively, without having learned it | outside it they are *worse* than a mortal, because they have never had to acquire anything and do not know how ignorance feels. A god of wisdom is not a god of people |
| **long-lived** — immortal, cultivator, elf, revenant | breadth accumulated across centuries | it is **era-locked**: they know the world of four hundred years ago in extraordinary detail and this one badly. They have also forgotten more than they kept, and they mistake the forgotten for the unimportant |
| **artificial** — ASI, oracle, system core | recall and inference at a scale no person matches | trained on what someone fed it. No embodied knowledge — it has never lifted anything. It interpolates confidently across its blank regions, and cannot tell those regions from the rest |
| **borrowed** — a system, a library, a bound spirit | access, not knowledge | it must be *queried*: that takes time, costs something, and returns what was asked rather than what was needed. The character's real skill is knowing what to ask |

### The three rules that still apply

1. **Breadth is not depth is not applicability.** Knowing everything recorded about metallurgy is
   not knowing which of these two smiths is lying to you. The gap between knowledge and judgement
   is where these characters are written.
2. **Bound the access, not the knowledge.** An unbounded oracle is a plot solvent — every mystery
   dies at its feet. So the god answers three questions a year; the immortal is asleep, or bored,
   or forbidden to intervene; the ASI is airgapped and speaks through a bad channel; the system
   charges. This is a `power-system` / `tech-plausibility` limit and it goes in that file too.
3. **They are still wrong about people.** `mc-intel-meter`'s tier-5 error profile applies with
   more force here: what cannot be modelled — grief, loyalty, spite, being loved — is where a mind
   like this fails, and failing there is the only thing that makes it a character rather than a
   reference work.

**Everyone else in that setting is still narrow.** A world with gods in it is not a world where the
farmers know cosmology. A cultivation sect with an 800-year-old patriarch still has disciples who
cannot read. The clause is per-character and does not leak downward — if anything, a setting with
broad-knowledge beings in it should be *more* stratified, because knowledge is a possession there
and possessions are guarded (`social-fabric`).
