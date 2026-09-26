---
type: reference
owner: novel-init
description: "the end of Round D, when Round A's style question came back thin: no style target, or one named and nothing written. Five original sample paragraphs to pick from and edit into style.sample"
---

# novel-init — register presets

Open this at the **end of Round D**, when Round A's style question came back thin: the user
shrugged, or named two books and left `style.sample` empty. Not in Round A itself, because the pair
you show is chosen by `tone.register`, which Round D asks. Do not open it when they paste their own paragraphs — theirs
are better than these by definition, because they are what that person actually wants to read.

`style.sample` is the cheapest lever on register in the whole toolkit and the only one that works
by imitation rather than by prohibition (`novels/_template/novel.md` §STYLE TARGET says why). It is
also the field most likely to be left blank, and a blank one hands the register back to the model's
own default — which is where every benchmark run's monotony came from.

**How to use these.** Show two, not five: pick the pair nearest the `tone.register` answer from
Round D. Ask which is closer, then **edit the winner with the user** until it is about their book —
swap the names, the props and the world, keep the sentence shapes. Ten minutes here is worth more
than any rule downstream. Write the edited version into `style.sample`, never the preset verbatim:
an unedited preset is a fifth house style, which is the problem, not the fix.

These are written for this file and are nobody's published work. `style.read_like` is where real
books get named — by title, as comparison points, never quoted.

---

## 1. Plain and procedural — `grounded`

> The lock was a Verrin four-pin, which meant it was older than the door it sat in. Sera set the
> lamp on the step where it would not throw her shadow across the keyhole. She had picked three of
> these in the last year and all three had taken longer than the book said. This one took eleven
> minutes. She did not feel clever when it opened; she felt cold, and aware that she had been
> kneeling on stone.

Competence shown by method. Sentences that carry information and stop. The feeling arrives last and
undramatised.

## 2. Warm and peopled — `adventurous`

> Dov had saved her the seat by the fire and was pretending he had not. He had also, she noticed,
> moved the wet boots off the hearth and put hers there instead, which was the kind of thing he
> would deny under questioning.
>
> "You're late."
>
> "I'm on time. You're early, which isn't the same as me being late."
>
> "It is from here." He passed her the cup without being asked, and she drank it without saying
> thank you, because thanking him would have made it a favour instead of a Tuesday.

Affection carried by what people do and refuse to say about it. The joke includes the other person.
Nothing is undercut at the end.

## 3. Dry and sharp — `wry`

> The Ministry of Roads had sent four men to inspect a bridge that everyone in the valley knew had
> fallen down in spring. They inspected it thoroughly. They filed a report recommending an
> inspection. Mira watched from the bank with her cart and her dying horse and thought about how
> long it would take to walk to Halstead, which was the sort of thought that kept a person warm.

The humour is in the arrangement of facts, not in a joke. The narrator has an attitude and does not
announce it.

## 4. Close and hurt — `grounded`, high interiority

> She had been fine in the corridor. She had been fine on the stairs. It was the smell of the
> landing that did it — someone two floors down was frying onions, the way her mother had, and Kess
> had to stand with her hand flat on the wall until it passed. Onions. Eleven years of not crying
> at funerals and she was going to be undone by somebody's dinner.

Free indirect discourse doing the work. The trigger is specific and small. No naming of the emotion.

## 5. Cold and wide — `bleak`

> By the second week the camp had stopped burying them properly. There was a procedure for it,
> written down, and the procedure assumed a number that the winter had exceeded in four days. Vosk
> kept the ledger anyway. He wrote each name in the same careful hand, because the hand was the
> last part of the job that still worked.

The cost is stated flatly and never editorialised. Even here, one thing is held onto — which is
what keeps it readable (`conflict-engine` §What the chapter gives back).

---

**A note on the pairing.** `tone.warmth` and these presets are not the same question. Preset 5 with
`warmth: measured` is a bleak book that still lets something matter; preset 2 with `warmth: cold` is
a book whose warmth is there to be taken away. Both are coherent. Ask for both answers.
