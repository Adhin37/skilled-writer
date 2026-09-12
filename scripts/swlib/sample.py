"""The novel `sw selftest` builds: complete, small, and written to pass every audit.

It exists so a fresh clone can be proved working without a model, an interview, a network or an
API key. The content is filled into a copy of the **shipped** `novels/_template`, the way
`tests/fixtures.py` does, so the selftest fails when the template drifts away from the parsers
rather than quietly testing a private scaffold.

Two variants:

* `build(root)` - the clean novel. Every command must exit 0 against it.
* `build(root, seeded=True)` - the same novel with `SEEDED` defects planted in it, each one
  named by the check that has to catch it. A selftest that only asserts "no defects" passes
  just as happily when every parser is dead; this is the positive control.

Word counts are measured at build time and written into the frontmatter and the ledger, because
a fixture that hardcodes them starts failing the moment somebody fixes a typo in the prose.
"""

import os
import re

SLUG = "salt-and-ledger"

# Each entry: (check, where, what was planted, the level it must be reported at). The selftest
# asserts every one is found. The level is part of the row because a check that reports a `warn`
# is just as dead when it stops firing, and a control that only collects defects cannot see it.
SEEDED = [
    ("mtl", "chapters/0002", "a banned MTL phrase in narration", "defect"),
    ("narration-bang", "chapters/0003", "an exclamation mark outside dialogue", "defect"),
    ("wordcount", "chapters/0004", "frontmatter wordcount that disagrees with the body", "defect"),
    ("scene-break", "chapters/0005", "a scene break written as a lone `*`", "warn"),
    ("markup", "chapters/0006", "a phrase italicised in a prose body", "defect"),
    ("ccs", "state/continuity.md", "mc.foreknowledge set with no `fk>` line on any block", "defect"),
    ("curve-pressure", "state/power.md", "a P value that disagrees with its own tiers", "defect"),
    ("straddle", "bible/cast/_voices.md", "nobody left below the MC's intel tier", "defect"),
]


# --------------------------------------------------------------------- chapters

CHAPTERS = [
    dict(
        title="The Line on the Stone",
        delivers="Wren finds her own name against a draw she did not make",
        event="Wren reads her own name in the salt line at the Tidehouse",
        ev="reads the salt line at the Tidehouse / counts it twice / Maro names the debtor",
        chg="Wren: steady -> cornered ; Maro: amused -> attentive",
        kno="Wren+{her name is on the draw} ; reader+{the Ledger can be written into}",
        thr="~T01(name-on-the-draw)",
        obj="find out who drew against the harbour -> next: get the clerks to open the book",
        wld="the Tidehouse clerks move the bell an hour later",
        hook="the name under the draw is hers, in a hand she does not know",
        pwr="P=+1 vs the Tidehouse clerks",
        prose='''The tide had turned an hour before Wren reached the Tidehouse, and the salt line on
the steps stood a hand higher than the Ledger allowed.

She counted the courses twice. Both times the stone gave her the same wrong answer.

"You are early," Maro said from the doorway. He had six coins stacked on the rail beside him and
he did not look up from them. "The clerks do not open the book until the bell."

"The book is already open." Wren put two fingers against the salt. "Somebody drew against the
harbour last night."

"Somebody draws against the harbour every night. That is what a harbour is for."

"Not four fathoms of it."

The seventh coin stopped halfway to the stack. Maro set it down flat instead, which was how she
knew she had his attention, and he came down the steps without hurrying, because Maro never
hurried where anyone could see him do it.

He looked at the line for a long moment. "Four is a barge," he said. "Four is somebody moving
grain out of Ashfall before the levy lands."

"Four is somebody who does not care that the whole quay reads this stone every morning."

"Or somebody who wanted it read." He wiped the salt off his thumb. "Whose name is under it?"

Wren had been standing so that her body covered that part of the step. She moved.

The clerks had written the draw in the small square hand they used for everything, the letters
tipped left, and under it, where the debtor signs, somebody had put her name. Not a copy of her
name. Hers, with the crooked W she had never managed to straighten out of it, the one her master
still corrected on the tally slips.

Maro read it. Then he read it again, which he did not do with things.

"You did not sign that," he said. It was not a question, and Wren was grateful for it in a way
she could not have explained without sounding young.

"I was in the counting room until the second bell. Ossian saw me leave."

"Then somebody wrote you into a debt of four fathoms." He straightened. "Wren. A saltwright with
a draw against her cannot hold a licence. They will take the seal by the end of the month."

The bell rang, an hour late, and the clerks came out to open the book on a draw that already had
a debtor.''',
    ),
    dict(
        title="What the Clerks Will Say",
        delivers="the manifest that authorised the draw has a signature nobody will read out",
        event="The clerks produce the manifest with the signature covered",
        ev="Wren petitions the clerks / the manifest is produced / the signature is covered",
        chg="Wren: cornered -> looking for the hand",
        kno="Wren+{a manifest exists} ; reader+{somebody senior signed it}",
        thr="^T01(name-on-the-draw) ~T02(who-signed-the-manifest) ~T04(which-barge)",
        obj="read the manifest -> next: find who had the seal that night",
        wld="the levy office posts a second collection date",
        hook="the clerk turns the manifest so the bottom third stays under his hand",
        pwr="P=0 vs the clerks",
        prose='''The counting room at the Tidehouse smelled of wet rope and the lamp oil the clerks bought
too cheap, and it had exactly one chair, which was not for petitioners.

She had stood in it perhaps forty times and had never once been offered the chair. That was not
rudeness. The office simply had no category for a petitioner who also worked there.

"A draw is a draw," the senior clerk said. He was a narrow man named Hesk with ink to the second
knuckle. "The stone records it. The book records the stone."

"The book records a debtor," Wren said. "I am the debtor. I did not draw."

"Then the book is wrong, and the book is not wrong."

"Show me the manifest."

Hesk looked up for the first time. Behind him two juniors had stopped copying, in the particular
way people stop when they want to be seen to be working.

"There is a manifest," Wren said. "Four fathoms does not come off the harbour on somebody's word.
A saltwright signs the draw and a factor signs the manifest and the clerks match the two. That is
the whole of your office."

"You know the office."

"I am three years in it."

He went to the shelf. He was gone long enough that Maro, who had come in behind her and said
nothing at all, put his back against the door frame and stayed there.

The manifest came out in a grey sleeve. Hesk laid it on the desk, turned it so the head of it
faced her, and left his hand flat across the bottom third.

Most of it was ordinary. Four fathoms, drawn against the Ashfall harbour ledger, dated the night
before, consigned to a barge she did not know. The body listed grain, which was what everybody
said it would list.

She read the whole of it twice anyway, at the speed she used on the steps. The head of a manifest
is the part people forge badly, because it is the part that has to look right from across a room.
The body is where the care goes. This one had care in it.

"The signature," Wren said.

Hesk's hand stayed flat. Under the desk his other hand had found the edge of the shelf and stayed
there too.

"The signature is a matter for the office."

She kept her voice where she kept it for counting, which was low and slightly bored, and which had
never once failed to make a clerk finish a sentence he had not meant to start.

"It is a matter for the person whose name is on the stone."

Hesk did not move his hand. "You may lodge a counter-claim," he said. "A counter-claim is heard
at the quarter. Until the quarter you are a saltwright with a draw against her, and I would not
present myself at the Tidehouse in that condition if I were you."

Maro spoke from the door. "She is not asking you to read it out. She is asking you to move your
hand."

"I am aware of what she is asking."

Nobody moved for a while. Then Hesk slid the manifest back into its sleeve, and Wren went out
into the light with nothing except the shape of a signature she had not been allowed to see, and
the certainty that Hesk had known exactly whose it was.''',
    ),
    dict(
        title="Bread and the Second Oven",
        delivers="Bel trades what she knows about the barge for help she cannot ask for",
        event="Bel names the barge and takes the licence as her price",
        ev="Wren goes to the bakehouse / Bel names the barge / the licence is the price",
        chg="Wren: alone -> in somebody's debt ; Bel: wary -> committed",
        kno="Wren+{the barge is the Corun} ; Bel+{Wren is under a draw}",
        thr="^T01(name-on-the-draw) ~T03(bels-oven-licence) vT04(the Corun, read at the waterline)",
        obj="learn the barge -> next: reach the dock crew who loaded it",
        wld="the bakehouse row loses its second water ration of the month",
        hook="Bel puts the licence on the table between them and does not let go of it",
        pwr="P=-1 vs the bakehouse row",
        prose='''Bel had the second oven open and both arms in it to the elbow, and the bakehouse was hot
enough that the salt in the mortar had gone soft.

The row had one water ration between nine families and two ovens, and every household on it could
have told you to the bucket how much of that went into Bel's second oven and how much came back
out as bread. Wren had grown up four doors along. She could still read the state of the row off
the heat coming through the door.

"You look like the stone," Bel said, without turning round. "Grey and written on."

"I need the name of a barge."

Bel laid the peel across the mouth of the oven.

"I need a water ration and a clerk who can count. We are both going to be disappointed." She
pulled the tray, banged it flat on the board, and only then looked at Wren properly. Whatever she
found there made her put the cloth down. "Sit."

"Bel—"

"Sit down, Wren."

Wren sat. The stool was too low, the way it had been since they were twelve, and sitting on it put
her at the height of the board, which was where Bel put people she intended to feed.

Through the wall came the sound of the row going about its morning: a bucket set down, somebody
counting children, the long scrape of the other oven's door. Nine families. It was a number Wren
had been carrying around all week without once saying it out loud.

"The barge is the Corun," Bel said. "Out on the ebb, low in the water, and nobody on the row
slept through the loading because they did it with the lamps hooded." She began cutting the loaf
without looking at it. "Grain, they said. Grain does not need hooded lamps. Grain does not need
six men who are not dock crew."

"You are certain about the name."

"It was painted out and painted over. You can read the ghost of it at the waterline when the
light is low." Bel pushed half the loaf across. "Eat that. You have the face you get."

The row had no reason to watch a barge load. That was the thing worth carrying out of the
bakehouse. Nine families had stood at their windows in the middle of the night over hooded lamps,
which meant the lamps had been wrong enough to be worth losing sleep over.

Wren ate, because Bel would not go on until she did, and because the bread was warm and she had
not stopped moving since the bell.

The paint, she thought. That was the piece that mattered. A barge running a legitimate draw does
not paint out its name, and a barge running an illegitimate one does not paint it back on badly
enough to be read at the waterline. Somebody had done both, which meant somebody had changed their
mind partway through the night about whether this was going to be a secret.

"Now," Bel said. "What is it costing you."

"The seal, if the counter-claim fails."

"And if it does not fail?"

"Then somebody senior at the Tidehouse loses a great deal more than a seal, and I have to be
right in front of the whole quarter about a signature I have never been shown."

Bel wiped her palms down her apron, once, and reached under the board. What she brought up was a
folded square of Tidehouse paper, soft at the creases from being carried.

"My oven licence," she said. "Lapsed the first of the month. Hesk has been sitting on the renewal
since spring because the row will not pay him what the row does not have."

She laid it on the table between them and kept two fingers on the corner.

"You take that to the counter-claim," Bel said, "and you make the quarter look at it, and Hesk
has to explain two pieces of paper instead of one. But if you lose, I lose the oven, and the row
loses its bread, and that is nine families, Wren, and I will have handed it to you myself."

Wren looked at the fingers on the corner of the paper.

"Then do not hand it to me yet," she said.''',
    ),
    dict(
        title="The Crew That Was Not There",
        delivers="Ossian refuses her, and the refusal tells her who the six men answered to",
        event="Ossian refuses to name the six men on the quay",
        ev="Wren finds Ossian on the quay / he will not name the six / his refusal names them",
        chg="Wren: asking -> deducing ; Ossian: neutral -> exposed",
        kno="Wren+{the six were levy men} ; Ossian+{Wren is close to the manifest}",
        thr="^T02(who-signed-the-manifest)",
        obj="name the six men -> next: put the levy office at the loading",
        wld="the levy office moves its own men off the night roster",
        hook="Ossian tells her which question will get her hurt, which is the question",
        pwr="P=+1 vs the levy office",
        prose='''Ossian worked the Ashfall quay the way other men worked a rope, hand over hand, never
looking at the whole length of it, and he had a ring he tapped against the bollard when he wanted
somebody to stop talking.

He was tapping it before Wren finished the first sentence.

"No," he said.

The quay was working around them, which was the point of having the conversation there. Two berths
down a crew was arguing about a pallet in the flat, unhurried way of men who would still be
arguing about it at noon.

"I have not asked yet."

"You have asked six people this morning and I have heard about five of them." Tap. "The answer is
no, and you should take it from me rather than from the man who tells you next."

Wren put her back against the bollard so that they were shoulder to shoulder and both facing the
water, which was how you had a conversation on the quay that nobody wrote down.

"Six men loaded the Corun," she said. "They were not dock crew. Dock crew is your roster. If they
were not on your roster then somebody put them on a roster of their own, and there are not many
offices in Ashfall that keep one."

"I am not going to name them."

Wren had expected that, and had come anyway, which was the part he had not accounted for.

"I know."

"Then why are you standing here."

"Because you not naming them is worth almost as much."

The ring stopped against the bollard.

She had worked this out on the way down, walking the long side of the harbour so she would have
time to be wrong about it. Ossian had a roster. A roster is a list of men who may be on the quay
at night, and its whole purpose is that anyone not on it is a trespasser. Six men had loaded a
barge under hooded lamps and nobody had called them trespassers. Either they were on his roster,
or they were on somebody else's, and there were not many offices in Ashfall that kept one.

"You could have said you did not know," Wren said. "You could have said it was a crew out of the
south quay and I would have gone and wasted three days on the south quay. You did not, because
you will not lie to me, and you will not name them, and the only men in this town who buy that
particular silence are men who can take your roster away."

Ossian looked at the water for a while. A gull came down on the next bollard and left again.

The tide was three-quarters out. From here the Tidehouse steps were a pale band above the mud, and
the line she had counted at dawn was still on them, four courses higher than it had any business
being, legible to the whole of Ashfall and disputed by nobody at all.

He put his weight on the other foot.

"The levy office keeps a night roster," he said, to nobody. "It is not a secret. It is written up
in the same room as everything else."

"And the six?"

"I said I am not going to name them." He turned round, and up close he was older than the quay
made him look. "Wren. Listen to me, because I have known your master twenty years and I would
rather do this once. There is a question you are three days from asking. When you ask it out loud,
in front of the quarter, with Hesk in the room, you will have made it impossible for anybody to
give you a small answer."

Wren looked out at the water instead of at him, because he had earned that much.

"I am already in a draw for four fathoms."

"That is the small answer." The ring went back into his pocket. "Ask a different one and they can
still let you keep the seal. Ask that one and they cannot."

He went back down the quay hand over hand, stopping twice for things that did not need him, and
Wren stayed at the bollard with the water going out in front of her.

Two questions, then. One of them got the draw lifted and left the office intact, and she could
probably still be a saltwright at the end of it. The other one put the levy office at a loading it
denied attending for nine days running, and there was no version of asking it that ended with
anybody handing her back a seal.

She did the arithmetic twice, the way she did everything twice, and both times it came out the
same, and both times she disliked the answer for exactly as long as it took her to accept it.''',
    ),
    dict(
        title="The Ghost at the Waterline",
        delivers="Maro gets her the manifest, and the hand on it is the one that trained her",
        event="Maro brings the sleeve and the signature is her master's hand",
        ev="Maro trades a debt for the sleeve / Wren reads the signature / the hand is her master's",
        chg="Wren: deducing -> unwilling to believe it ; Maro: careful -> spent",
        kno="Wren+{her master signed the manifest} ; Maro+{what the counter-claim will cost her}",
        thr="^T01(name-on-the-draw) ^T02(who-signed-the-manifest)",
        obj="read the signature -> next: decide whether to lodge the counter-claim",
        wld="the quarter session is brought forward by nine days",
        hook="the crooked W on the manifest is not hers, and she knows exactly whose it is",
        pwr="P=+2 vs the Tidehouse office",
        prose='''Maro came to the counting room at the hour when the lamps were lit and the clerks had gone,
and he put the grey sleeve on the table without any ceremony at all.

"That is not yours," Wren said.

"It is not anybody's for about a quarter of an hour."

"What did it cost."

"A thing I was owed." He sat down on the corner of the desk. "Do not ask me by whom. If the
quarter puts you under oath I would like the true answer to be short."

Wren undid the tie. Her hands were steady, which surprised her, and the paper came out of the
sleeve with the small dry sound that Tidehouse stock always made.

She read the head again, because she wanted the ordinary part to last.

Four fathoms. Ashfall harbour ledger. The barge unnamed in the body and named in the endorsement,
and the endorsement said Corun, and Bel had been right about the paint.

Then the bottom third, which Hesk had covered with his hand.

The factor's signature was there. It was small, and it was tipped left, and the last letter ran
down and away as though the writer had been interrupted, and it was not a hand she had to think
about, because she had been copying it onto tally slips for three years to learn the shape of a
good one.

"Wren."

"The W," she said.

"What about it."

"It is crooked." She put her finger next to it without touching the ink. "Mine is crooked because
I learned it from his. He tells the room it is the one fault he never got out of me. He tells the
room that once a season, Maro, the same way, and everybody laughs, and I have been standing there
laughing with them."

Maro was quiet for a moment. Out on the harbour somebody was working a winch, and the sound came
up through the floor of the counting room the way it had every evening of her apprenticeship.

"So he wrote your name on the stone," he said, "in his own hand, which is close enough to yours
that no clerk in Ashfall would look at it twice."

"And signed the manifest above it. So that if it ever came apart, it came apart onto me."

"Yes."

Wren put the paper down flat and made herself look at the whole of it at once instead of the
signature.

"He needs the seal," she said slowly. "Not mine. His. A factor under a draw cannot sign anything,
so the draw had to sit on somebody, and the somebody had to be near enough to him that the hand
matched. That is not spite. That is arithmetic."

"It is both."

Wren turned the manifest a quarter turn on the desk, the way she turned a tally slip when the
figures stopped agreeing, as though the fault might be in the angle she was holding it at.

"It is arithmetic," Wren said, "and I can do arithmetic."

She rolled the manifest and gave it back, and her hands were still steady, and she found that she
minded that more than anything else in the room.''',
    ),
    dict(
        title="Counter-Claim",
        delivers="Wren lodges the counter-claim and loses the apprenticeship to do it",
        event="Wren files the counter-claim and is put out of the house",
        ev="Wren files at the quarter / names the manifest without naming her master / is put out of the house",
        chg="Wren: unwilling -> committed and homeless",
        kno="quarter+{a manifest exists} ; Hesk+{Wren has read it} ; reader+{her master knows she knows}",
        thr="^T01(name-on-the-draw) ^T02(who-signed-the-manifest) ^T03(bels-oven-licence)",
        obj="get the draw lifted -> next: survive the quarter with no house behind her",
        wld="the levy lands nine days early and the row pays it first",
        hook="her master signs the dismissal in the small hand, tipped left, and hands her the pen",
        pwr="P=0 vs the quarter",
        prose='''The quarter sat in the long room above the Tidehouse, and it took Wren four minutes to
say what nine days of reading had turned up.

She did not name her master. She named the manifest, and the endorsement, and the hooded lamps,
and the six men who were on no dock roster, and she put Bel's lapsed licence on the table beside
the draw and asked the quarter to look at the two pieces of paper together and tell her which
office had been holding both.

Hesk objected twice. The second time, the presiding factor told him to sit.

"You are asking us to open the manifest," the factor said.

"I am asking you to open both of them," Wren said. "A draw with no readable manifest is not a
debt. It is a claim. I am not asking the quarter to say who signed it. I am asking the quarter to
say that somebody has to."

"And if the manifest is opened and your name is on it in your own hand?"

"Then the seal is yours to take and I will not be here to argue."

It went to the clerks. The clerks would take until the next quarter, which was the answer Wren
had come for and not the answer she had wanted, and the draw stood against her name until they
were done.

Her master was waiting in the counting room.

He had the dismissal already written. That was the part she was not ready for, that it was written
before she had said a word upstairs, in the small square hand tipped left, with the whole of the
reason given as a failure to maintain the standards of the house.

"Sign it," he said, "and the house will not be asked about your draw."

"And if I do not sign it?"

"Then the house will be asked, and the house will answer, and the answer will be worse for you
than for me. You know that. You have always been good at knowing that."

Wren looked at the page for a long time.

Then she took the pen, and she signed it with the crooked W, large, and pressed hard enough that
the nib caught, so that every clerk who ever pulled the dismissal out of the shelf would see
exactly which of the two of them had written that letter last.

"Keep the copy," she said, and put the pen down on his side of the desk.

Outside, the tide was going out, and the salt line on the Tidehouse steps still stood a hand
higher than the Ledger allowed, and now there was nobody at all whose job it was to correct it.''',
    ),
]


# ----------------------------------------------------------------- config + bible

NOVEL_MD = '''---
title: "Salt and Ledger"
title_alternates: ["The Line on the Stone", "Four Fathoms"]
slug: "salt-and-ledger"
genre: fantasy
subgenre: ""
status: drafting
language: en

narration:
  person: third-limited
  tense: past
  distance: close
  interiority: high
  voice_notes: "dry, procedural, short under pressure"

pov:
  mode: single
  switch_granularity: never
  pov_characters: ["Wren"]
  label_switches: false
  antagonist_pov: never

mc:
  name: Wren
  gender: female
  pronouns: she/her
  intel_tier: 3
  eq_tier: 2
  competence_domains: ["salt-ledger arithmetic", "Tidehouse procedure"]
  blind_spots: ["reading people who are fond of her", "anything involving a boat"]
  development_rate: 5
  appearance_note: "reads as somebody's clerk until she opens her mouth"
  core_wound: "was taught by a man who was already using her"
  core_want: "to keep the seal she earned"
  core_need: "to stop measuring herself against his hand"
  origin: native
  foreknowledge: ""
  foreknowledge_grain: ""
  foreknowledge_first_win_ch: null
  foreknowledge_fails_ch: null
  foreknowledge_known_by: []
  golden_finger: "she can read a salt line to the quarter-fathom by eye"
  gf_cost: "an hour of the tide, and she has to be standing on the stone"
  gf_limit: "this can never tell her who drew. It can never work on a written record."
  gf_problem: "it makes her the only witness, which makes her the obvious debtor"
  gf_known_by: ["Maro", "her master"]
  form_locked: false
  final_form_reached_ch: null

scaling:
  shape: climb
  tiers: 7
  start_tier: 2
  ceiling_tier: 6
  endgame: "the factor who trained her, at tier 5, with the quarter behind him"
  edge_worth: 1
  edge_price: "she has to be present, in daylight, where anybody can see her counting"
  substitute_tension: ""
  first_limit_by_ch: 8
  gain_gap_min: 15
  setup_lead: 3
  flat_max: 12
  trivial_per_arc: 2
  boost_debt_due: 5

romance:
  configuration: undecided
  lead: ""
  lead_gender: ""
  lead_introduced_ch: null

chapters:
  length_band: "1500-2600"
  hook_required: true
  arc_length: 25
  scenes_per_chapter: 2

channels:
  speech: '"…"'
  thought: "'…'"
  meta: "[…]"
  free_indirect: unmarked

opening:
  promise: "a clerk with one useless gift has to prove a debt was forged before it takes her trade"
  anchor_by_ch: 1
  contract_by_ch: 3
  promise_touched_by_ch: 3
  first_win_by_ch: 5
  stakes_ceiling: "Wren can be ruined on paper, but nobody may lay a hand on her until the reader has watched the office ruin somebody else first"

theme:
  controlling_idea: "A debt you did not make is still yours to answer."
  counter_case: "Some debts are only paid by the people who cannot refuse them, and refusing is the whole of the work."
  tested_in_arcs: [1, 2]

platform:
  site: royalroad
  tags: ["fantasy", "low magic", "mystery", "female lead", "slow burn"]
  cadence: 3x-week
  launch_stock: 6
  cover_brief: "a salt-crusted stone step with a name written on it in a stranger's hand"

timeline:
  reactivity: 3
  butterfly_horizon: 2
  escalation_ceiling: 1
  crisis_cap: 3

ending:
  contract: "Wren keeps the seal, and the office that forged the draw has to answer for it in front of the quarter."
  tone: earned-peace
  non_negotiables: ["Bel keeps the oven", "Wren never becomes her master"]

content:
  rating: teen
  violence: light
  profanity: light
  romance: none
  hard_limits: []

optional:
  no-harem: on
  romance-arc: off
  combat-choreography: off
  litrpg-system: off
  mystery-clues: on
  comedy-levity: off
  grimdark-consequences: off
  slice-of-life-texture: off

fanfic:
  source: ""
  canon_scope: ""
  divergence_point: ""
  ooc_budget: low
  oc_policy: supporting
  footprint: self-insert
---

# Premise

Wren is three years into a saltwright apprenticeship in Ashfall, a harbour town that runs on a
public ledger cut into stone. She can read a salt line to the quarter-fathom by eye, which is a
small gift and the only one she has. One morning the line is wrong by four fathoms and her own
name is written underneath it in a hand she does not recognise.

# Hook (platform blurb)

Ashfall keeps its accounts in salt. Every draw against the harbour is cut into the Tidehouse
steps where the whole quay can read it, and Wren, three years an apprentice, can read it better
than anyone alive. That is why she is the first to see that last night somebody took four fathoms
out of the harbour and signed her name to it. The clerks will not open the manifest. Her master
will not meet her eye. She has until the quarter session to prove a debt was forged, and the only
evidence is a signature she has been copying since she was fifteen.

# Tone references

- The procedural patience of a good courtroom novel: the paperwork is the weapon.
- The small-town economy of a fishing-village mystery, where everyone's livelihood touches.

# Themes

Is a debt you did not make still yours to answer?

# Ending target

Wren keeps the seal and the office answers for the forgery, but she does it by becoming the kind
of person who reads the room the way her master does, and she has to decide what to do with that.
'''

WORLD_MD = '''# World

Ashfall is a harbour town on a cold coast, running on salt, grain and a public ledger.

## Places

| place | what it is | why it matters to the plot | sensory signature |
|---|---|---|---|
| The Tidehouse | the office that keeps the harbour ledger | the draw is cut into its steps | wet rope, cheap lamp oil, salt gone soft |
| The Ashfall quay | working dock, six berths | where the Corun was loaded under hooded lamps | gull noise, tar, the knock of hulls |
| The bakehouse row | nine families, two ovens, one water ration | Bel's licence is the second piece of paper | flour dust and a heat you can lean on |
| The long room | where the quarter session sits | the counter-claim is heard here | chalk, cold stone, a window nobody opens |

## Factions

| faction | wants | method | fears | current posture toward MC |
|---|---|---|---|---|
| The Tidehouse office | to keep the ledger unquestioned | procedure, delay, the quarter calendar | an opened manifest | obstructive, not yet hostile |
| The levy office | to collect before the harvest moves | night rosters and its own men | being placed at a loading | watching |
| The bakehouse row | water, and a licence renewed | collective refusal to pay | losing the second oven | owes her nothing, helps anyway |

## Open questions

| question | may be answered by ch | currently implied |
|---|---|---|
| Who moved the bell an hour late | 12 | somebody wanted the draw read before the book opened |
| What was actually on the Corun | 18 | not grain |
'''

SOCIETY_MD = '''# Society

The central rule: **the harbour ledger is public and physical.** Every draw is cut into the
Tidehouse steps in salt, where anyone may read it, and the written book only records the stone.

## Labour

Saltwrights read and cut the stone. It is a licensed trade, three years apprenticed, and a
saltwright under a draw cannot hold a seal - which makes the trade unusually easy to destroy on
paper and unusually hard to buy.

## Money

Debt is denominated in fathoms of harbour draw. Because the ledger is public, credit in Ashfall
is a matter of who has been seen to pay, not of who has coin.

## Law

The quarter session hears counter-claims. Between the lodging and the hearing the claim stands,
which means an accusation costs the accused a season of trade whether or not it is true.

## Knowledge

Reading the stone is a skill, not a secret. Reading it to the quarter-fathom by eye is rare
enough that Wren is the only witness to her own accusation.

## Belief

The row holds that a debt cut in salt washes out if it was never owed. The office holds that the
stone is the record and the sea has no standing.

## Mobility

A seal moves a person between quays. Losing one puts them back on the row they came from.
'''

LEXICON_MD = '''# Lexicon

## Names

| canonical | pronunciation hint | who/what | never write as |
|---|---|---|---|
| Wren | as the bird | the MC, saltwright apprentice | Wrenn |
| Maro | MAH-ro | factor's runner, keeps his own accounts | Marro |
| Bel | as in bell | baker, second oven, bakehouse row | Belle |
| Ossian | OSH-un | quay foreman, keeps the dock roster | Osian |
| Hesk | rhymes with desk | senior clerk at the Tidehouse | Hesque |

## Terms

| term | capitalized? | italicized on first use? | plain-English meaning | anchor? | first appears |
|---|---|---|---|---|---|
| Ashfall | yes | no | the harbour town this is all in | yes | 1 |
| the Tidehouse | yes | no | the office that keeps the harbour ledger | yes | 1 |
| saltwright | no | no | licensed reader and cutter of the salt ledger | yes | 1 |
| the Ledger | yes | no | the public account cut into the Tidehouse steps | yes | 1 |
| fathom | no | no | the unit a draw is measured in | no | 1 |
| draw | no | no | an authorised withdrawal against the harbour | no | 1 |

## Address

| speaker → target | form | when it changes |
|---|---|---|
| Wren → her master | "sir", never his name | she uses the name in ch 6 and does not go back |
| Bel → Wren | "Wren", flat | never |

## Units

| unit | equals | used by |
|---|---|---|
| fathom | one course of salt on the Tidehouse steps | everyone |
| quarter | the session, every ninety days | the office |
'''

VOICES_MD = '''# Cast voice matrix

One row per speaker. The MC is the calibration point; everybody else is placed against her.

| character | tier | intel | eq | artic | wit | heat | turn | hands | pressure | first move |
|---|---|---|---|---|---|---|---|---|---|---|
| Wren | MC | 3 | 2 | 3 | none | banked | 12 | picks at the seam of her cuff | goes quieter and more exact | states the measurement |
| Maro | A | 4 | 4 | 4 | dry | flat | 22 | stacks coins into towers | stops moving his hands | asks the question under the question |
| Bel | B | 2 | 3 | 2 | none | quick | 6 | wipes her palms down her apron | gets louder and shorter | tells you to sit down |
| Ossian | A | 4 | 1 | 2 | none | volatile | 30 | taps a ring against wood | says no before you finish | refuses, then explains the refusal |

## POV THOUGHT

Direct thought is Wren's only, in single quotes, one to three a chapter. Everything else in her
head is unmarked free indirect discourse.

## MIRROR

No declared mirrors. Nobody in this cast shares all three of intel, articulacy and wit, and no
two share intel and eq. Wren reasons better than she reads people; Bel is the other way round.
'''

COMPETENCE_MD = '''# Competence grid

An unlisted domain is `none`.

| character | domain | level | where the edge is |
|---|---|---|---|
| Wren | salt-ledger arithmetic | professional | cannot tell who cut a line, only that it was cut |
| Wren | Tidehouse procedure | apprentice | knows the forms, not which of them can be waived |
| Maro | contracts and endorsements | exceptional | reads paper; will not read a room he is inside |
| Maro | who owes whom in Ashfall | professional | stops at the levy office door |
| Bel | ovens and grain quality | professional | cannot read a manifest at all |
| Ossian | dock labour and rosters | professional | knows the men, not the offices that hire them |
| Ossian | Tidehouse procedure | apprentice | has watched it, never worked it |

## Who they ask

| character | outside their domain, they go to | what asking costs them |
|---|---|---|
| Wren | Maro | he keeps a running account of it |
| Maro | Ossian | has to be seen on the quay, which he avoids |
| Bel | Wren | she does not like owing the trade |
| Ossian | nobody | it is why his refusals are so informative |

## What nobody knows

| gap | who in the world does know | what it would cost to reach them |
|---|---|---|
| what was actually loaded onto the Corun | the six men on the night roster | the levy office would have to be named |
| who moved the Tidehouse bell | a junior clerk | he would lose the post |
'''

EXTRAS_MD = '''# Extras roster

Tier-C walk-ons. One line each. Never a profile.

```
Hesk — senior clerk, Tidehouse counting room — ch 2, 6 — recurring obstruction
The presiding factor — chairs the quarter session — ch 6 — one scene
```
'''

# ------------------------------------------------------------------------- plan

# hook-and-pacing: the declared temperature and last-beat shape per chapter. Varied on purpose -
# this fixture is a positive control, so it has to be the shape a passing novel actually has.
REGISTER = [
    ("tense", "reveal"),      ("procedural", "decision"), ("warm", "quiet"),
    ("tense", "reversal"),    ("bleak", "reveal"),        ("loud", "decision"),
    ("quiet", "arrival"),     ("fast", "threat"),         ("fast", "reversal"),
    ("procedural", "question"), ("warm", "quiet"),        ("tense", "threat"),
    ("bleak", "reveal"),      ("loud", "cliff"),          ("tense", "decision"),
    ("fast", "reversal"),
]

PLAN_ROWS = [
    (1, "The Line on the Stone", "read the wrong line", "the clerks will not open early",
     "her own name is under the draw", "Wren finds her own name against a draw she did not make",
     "she is a saltwright under a draw", "~T01", "the hand is not hers", "revised"),
    (2, "What the Clerks Will Say", "read the manifest", "Hesk covers the signature",
     "she is offered a counter-claim instead", "the manifest that authorised the draw has a signature nobody will read out",
     "a season of trade if she lodges", "^T01 ~T02 ~T04", "his hand does not move", "revised"),
    (3, "Bread and the Second Oven", "name the barge", "Bel wants something first",
     "the price is nine families", "Bel trades what she knows about the barge for help she cannot ask for",
     "she is now in Bel's debt", "^T01 ~T03 vT04", "the licence stays under Bel's fingers", "revised"),
    (4, "The Crew That Was Not There", "name the six men", "Ossian refuses",
     "the refusal identifies them", "Ossian refuses her, and the refusal tells her who the six men answered to",
     "the question she can afford narrows", "^T02", "the dangerous question is the right one", "revised"),
    (5, "The Ghost at the Waterline", "read the signature", "the manifest is not hers to hold",
     "the hand is her master's", "Maro gets her the manifest, and the hand on it is the one that trained her",
     "Maro spends a debt he was owed", "^T01 ^T02", "the crooked W is his", "revised"),
    (6, "Counter-Claim", "get the draw lifted", "the office delays to the next quarter",
     "she signs her own dismissal", "Wren lodges the counter-claim and loses the apprenticeship to do it",
     "the apprenticeship and the house", "^T01 ^T02 ^T03", "he hands her the pen", "revised"),
    (7, "No House Behind Her", "find a bed and a bench", "nobody will take a seal under a draw",
     "the row takes her in on Bel's word", "Wren is housed by the people whose licence she risked",
     "she owes the row publicly", "^T03", "the row expects a return", "planned"),
    (8, "The Junior Clerk", "learn who moved the bell", "he will lose the post if he speaks",
     "he asks her to take the risk with him", "the bell was moved on a written instruction",
     "a second person is exposed", "~T04", "the instruction is initialled", "planned"),
    (9, "The Night Roster", "place the levy office at the loading", "the roster is kept in the same room as everything else",
     "Ossian gives her the room, not the names", "the levy office is placed at the Corun loading",
     "Ossian's roster is taken from him", "^T02 ^T04", "the roster page is missing", "planned"),
    (10, "Four Fathoms of Grain", "find what the Corun carried", "the barge is out of reach",
     "the cargo was never grain", "the cargo manifest and the endorsement disagree",
     "she has to admit what she cannot prove", "^T02", "the endorsement is dated wrong", "planned"),
    (11, "The Water Ration", "keep the row fed", "the levy lands early",
     "Bel spends the oven to do it", "the row pays the levy first and the oven goes cold",
     "Bel's licence lapses in fact as well as on paper", "^T03", "the second oven is bricked", "planned"),
    (12, "A Small Answer", "accept a settlement", "the settlement requires her silence",
     "she refuses it in front of witnesses", "Wren refuses the settlement that would have saved the seal",
     "the seal, for certain now", "^T01 ^T02", "the offer is withdrawn publicly", "planned"),
    (13, "What Maro Is Owed", "collect on Maro's account", "his creditor is the levy office",
     "he pays instead of collecting", "Maro's ledger of favours is called in against him",
     "Maro loses his standing on the quay", "~T05", "his coins are not stacked", "planned"),
    (14, "The Second Quarter", "get the manifest opened", "the office moves the session",
     "the presiding factor recuses himself", "the manifest is ordered opened and the factor steps down",
     "the session is delayed again", "^T02 ^T04", "the recusal is not explained", "planned"),
    (15, "Her Master's Hand", "confront him directly", "he has already prepared the room",
     "he offers her the factorship", "her master offers her the thing he forged the draw to keep",
     "she has to want it out loud", "^T01 ^T05", "he is not lying about wanting her to have it", "planned"),
    (16, "The Stone Is the Record", "cut a line herself", "cutting without a seal is a crime",
     "the quay reads it before the office can wash it", "Wren cuts an unlicensed line and the quay reads it",
     "she is now provably outside the trade", "vT02 ^T05", "the office sends men to the steps", "planned"),
]

ARCS_MD = '''# Arcs

## Arc 1 - The Draw (ch 1-25)

| field | value |
|---|---|
| premise | a forged debt takes Wren's trade before she can prove it was forged |
| opposition | the Tidehouse office, procedurally, and her master personally |
| MC tier entry to exit | 2 to 2 |
| what closes | T01 - the draw is lifted or she is out of the trade |
| what opens | T05 - what Maro is owed, and by whom |
| cost | the apprenticeship, the house, and Bel's licence in fact |
'''

TIMELINE_PLAN_MD = '''# World track

What happens whether or not the MC acts.

## SCHEDULED FOR THIS ARC

| when | driver | event | reaches the MC as |
|---|---|---|---|
| ch 2 | the levy office | posts a second collection date | a queue outside the bakehouse |
| ch 5 | the Tidehouse | brings the quarter forward nine days | less time than she planned for |
| ch 6 | the levy | lands early; the row pays first | Bel's oven goes cold in ch 11 |
| ch 9 | the levy office | pulls its men off the night roster | Ossian loses the page |

## Drivers

| driver | wants | reacts at reactivity 3 by |
|---|---|---|
| the Tidehouse office | the ledger unquestioned | using the calendar, never force |
| the levy office | collection before the harvest moves | removing its own traces |
'''


# ------------------------------------------------------------------------ state

# ch -> (opposition, their tier, MC tier, P, outcome, what it cost)
PRESSURE = [
    (1, "the Tidehouse clerks and their calendar", 3, 2, 1, "held", "an hour she needed"),
    (2, "Hesk, procedurally", 2, 2, 0, "stalemate", "-"),
    (3, "the bakehouse row's own shortage", 1, 2, -1, "won", "-"),
    (4, "the levy office, through Ossian's silence", 3, 2, 1, "learned", "the safe question"),
    (5, "the Tidehouse office and her master together", 4, 2, 2, "read it anyway", "Maro's credit"),
    (6, "the quarter session", 2, 2, 0, "deferred", "-"),
]

THREADS_MD = '''# Thread ledger

| id | thread | opened | type | tension | due | carried | status | payoff |
|---|---|---|---|---|---|---|---|---|
| T01 | Wren's name is under a draw she did not make | 1 | promise | hot | 18 | | open | the draw is lifted, or she is out of the trade |
| T02 | who signed the manifest that authorised the draw | 2 | mystery | warm | 20 | | open | the signature is read out in the long room |
| T03 | Bel's oven licence has lapsed and Hesk is sitting on it | 3 | promise | cold | 24 | | open | the row gets its licence or loses the oven |
| T04 | which barge the four fathoms actually went onto | 2 | mystery | hot | 8 | | paid | Bel reads the painted-out name at the waterline: the Corun |
'''

GROWTH_MD = '''# Growth ledger

| character | rate | rung | since ch | next trigger | voice delta so far |
|---|---|---|---|---|---|
| Wren | 5 | 2 | 6 | naming her master out loud | shorter sentences, no hedges under pressure |
| Maro | 3 | 1 | 5 | his account being called in | has stopped narrating his own cleverness |
| Bel | 2 | 1 | 3 | the oven going cold | says "we" where she used to say "the row" |
| Ossian | 2 | 1 | 4 | losing the roster page | explains a refusal he would once have left bare |

## Skill ladders

| character | skill | stage | since ch | source of the last advance | what practice is costing |
|---|---|---|---|---|---|
| Wren | reading a forged hand | unreliable | 5 | copying her master's signature for three years | she cannot unsee it on old slips |
| Wren | quarter-session procedure | fails knowingly | 6 | one hearing, badly handled | a season of trade |

## What was taken

| ch | what was taken | from whom | still unhealed? |
|---|---|---|---|
| 6 | the apprenticeship and the house | Wren | yes |
| 6 | a debt he was owed | Maro | yes |
'''

POWER_MD_HEAD = '''# Power ledger

## CURRENT STANDING

| character | tier | since ch | the edge | what the edge cannot buy | active boost? |
|---|---|---|---|---|---|
| Wren | 2 | 1 | reads a salt line to the quarter-fathom by eye | it cannot tell her who cut it | no |
| Her master | 5 | 1 | a factor's seal and the office's habit of believing him | it cannot survive an opened manifest | no |
| Hesk | 3 | 1 | the quarter calendar | it cannot make the stone say something else | no |

## THE LADDER

| tier | what it lets you do | what it still cannot do | how many alive | who the reader has met |
|---|---|---|---|---|
| 1 | work a trade under somebody | lodge anything | most of Ashfall | Bel |
| 2 | hold an apprentice seal | sign a manifest | some dozens | Wren |
| 3 | clerk a ledger, set a calendar | overturn a factor | a dozen | Hesk, Maro |
| 4 | run a roster or an office floor | open a sealed manifest | six | Ossian |
| 5 | sign a manifest, carry a factor's seal | write the stone | three | her master |
| 6 | chair the quarter | leave Ashfall unwatched | one | not yet |
| 7 | rewrite what the ledger is for | - | none living | not yet |

## 3. PRESSURE LOG

| ch | opposition | their tier | MC tier | P | outcome | what it cost |
|---|---|---|---|---|---|---|
'''

POWER_MD_TAIL = '''
## GAIN LOG

| ch | from → to | source | price paid (ch) | set up in ch | what it obsoletes | new problem |
|---|---|---|---|---|---|---|

## ACTIVE BOOSTS

| ch | boost | above tier by | expires ch | the debt | due ch | paid? | climax? |
|---|---|---|---|---|---|---|---|

## CURVE PLAN

| arc | chapters | MC tier entry → exit | top opposition | pressure band | the gain, and where |
|---|---|---|---|---|---|
| 1 | 1-25 | 2 → 2 | her master, tier 5 | outmatched to hopeless | none - arc 1 is the gap, not a climb |
| 2 | 26-50 | 2 → 3 | the levy office, tier 4 | outmatched | ch 34, a seal of her own, paid for in ch 31 |
'''

CONTINUITY_HEAD = '''# Continuity ledger (CCS)

**Machine-only. Do not prettify. Do not write prose here.** Format spec and legend live in
`.claude/skills/continuity-summary/SKILL.md`. Newest chapter blocks go at the bottom of section 3.

---

## 1. BOOK DIGEST

```
prem> Ashfall keeps its accounts in salt; a forged draw puts Wren's name under a debt she did not make
mc> name=Wren | tier=3 | want=keep the seal she earned | need=stop measuring herself against his hand | wound=taught by a man already using her
world> harbour town, public stone ledger, quarter sessions, a levy landing early
open> T01 the forged draw | T02 the covered signature | T03 Bel's lapsed licence
done> ch 1-6 drafted: the draw found, the manifest half-read, the barge named, the six men placed, the hand identified as her master's, the counter-claim lodged at the cost of the apprenticeship
```

## 2. ARC DIGESTS

<!-- One per completed arc. Arc 1 is in progress. -->

## 3. CHAPTER BLOCKS

'''


# ------------------------------------------------------------------------ build

def _words(text):
    return len(text.split())


def _chapter_file(index, entry, wordcount):
    return (
        "---\n"
        "number: %d\n"
        'title: "%s"\n'
        "pov: Wren\n"
        "arc: 1\n"
        'event: "%s"\n'
        'delivers: "%s"\n'
        "wordcount: %d\n"
        "status: revised\n"
        "---\n"
        "\n"
        "%s\n" % (index, entry["title"], entry["event"], entry["delivers"], wordcount,
                   entry["prose"].strip()))


# What phase C had to fix, on the chapters where it found anything. Two of six, because a
# `gate>` on every block would be a habit rather than a record - and an absent line is the
# clean signal the format is built around.
SAMPLE_GATE = {
    3: "campaign-clause x2, speech-share 19%",
    5: "closer-sameness, Pass Z redraft of scene 2",
}


def _block(index, entry, wordcount):
    gate = SAMPLE_GATE.get(index)
    return (
        "=C%04d= pov:Wren | loc:Ashfall | t:D%d | wc:%d | arc:1\n"
        "dlv> %s\n"
        "ev> %s\n"
        "chg> %s\n"
        "kno> %s\n"
        "thr> %s\n"
        "obj> %s\n"
        "wld> %s\n"
        "pwr> %s\n"
        "hook> %s\n"
        % (index, index, wordcount, entry["delivers"], entry["ev"], entry["chg"], entry["kno"],
           entry["thr"], entry["obj"], entry["wld"], entry["pwr"], entry["hook"])
        + ("gate> %s\n" % gate if gate else ""))


def _plan_md():
    head = ("# Chapter construction list\n\n"
            "| # | title | pov | arc | temp | hooktype | goal | obstacle | turn | delivers | "
            "cost | threads | hook | status |\n"
            "|---|---|---|---|---|---|---|---|---|---|---|---|---|---|\n")
    rows = []
    for i, (num, title, goal, obstacle, turn, delivers, cost, threads, hook,
            status) in enumerate(PLAN_ROWS):
        temp, hooktype = REGISTER[i]
        rows.append("| %d | %s | Wren | 1 | %s | %s | %s | %s | %s | %s | %s | %s | %s | %s |"
                    % (num, title, temp, hooktype, goal, obstacle, turn, delivers, cost,
                       threads, hook, status))
    return head + "\n".join(rows) + "\n"


def _power_md():
    rows = []
    for ch, opp, their, mine, p, outcome, cost in PRESSURE:
        rows.append("| %d | %s | %d | %d | %+d | %s | %s |"
                    % (ch, opp, their, mine, p, outcome, cost))
    return POWER_MD_HEAD + "\n".join(rows) + "\n" + POWER_MD_TAIL


def _write(root, relpath, text):
    full = os.path.join(root, *relpath.split("/"))
    parent = os.path.dirname(full)
    if parent and not os.path.isdir(parent):
        os.makedirs(parent)
    with open(full, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(text)
    return full


def _read(root, relpath):
    with open(os.path.join(root, *relpath.split("/")), encoding="utf-8") as fh:
        return fh.read()


def build(root, seeded=False):
    """Fill a scaffolded novel directory. Returns the list of files written."""
    written = []

    def put(rel, text):
        written.append(_write(root, rel, text))

    put("novel.md", NOVEL_MD)
    put("bible/world.md", WORLD_MD)
    put("bible/society.md", SOCIETY_MD)
    put("bible/lexicon.md", LEXICON_MD)
    put("bible/cast/_voices.md", VOICES_MD)
    put("bible/cast/_competence.md", COMPETENCE_MD)
    put("bible/cast/_extras.md", EXTRAS_MD)
    put("plan/arcs.md", ARCS_MD)
    put("plan/chapters.md", _plan_md())
    put("plan/timeline.md", TIMELINE_PLAN_MD)
    put("state/threads.md", THREADS_MD)
    put("state/growth.md", GROWTH_MD)
    put("state/power.md", _power_md())

    # Measured, never asserted: a fixture that hardcodes a word count starts lying the moment
    # somebody fixes a typo in the prose.
    blocks = []
    for i, entry in enumerate(CHAPTERS, 1):
        body = entry["prose"].strip() + "\n"
        count = _words(body)
        put("chapters/%04d-%s.md" % (i, _slugify(entry["title"])),
            _chapter_file(i, entry, count))
        blocks.append(_block(i, entry, count))
    put("state/continuity.md", CONTINUITY_HEAD + "\n".join(blocks))

    if seeded:
        _seed(root)
    return written


def _slugify(title):
    return re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")


def _seed(root):
    """Plant one defect per SEEDED row. Each must be caught by the check it names."""
    # mtl - a banned phrase, in narration where no exemption can apply.
    text = _read(root, "chapters/0002-what-the-clerks-will-say.md")
    # Word-for-word the same length as what it replaces (7 words for 7). A seed that changes
    # the body also trips `wordcount` and `ledger`, and then the control no longer isolates
    # the check it claims to test.
    text = text.replace("Hesk looked up for the first time.",
                        "His expression changed drastically all at once.")
    _write(root, "chapters/0002-what-the-clerks-will-say.md", text)

    # narration-bang - an exclamation mark outside dialogue.
    text = _read(root, "chapters/0003-bread-and-the-second-oven.md")
    text = text.replace("Wren sat. The stool was too low",
                        "Wren sat! The stool was too low")
    _write(root, "chapters/0003-bread-and-the-second-oven.md", text)

    # wordcount - frontmatter that disagrees with the body it describes.
    rel = "chapters/0004-the-crew-that-was-not-there.md"
    text = _read(root, rel)
    text = re.sub(r"(?m)^wordcount: \d+$", "wordcount: 4242", text)
    _write(root, rel, text)

    # ccs - foreknowledge declared, and not one block records a spend.
    text = _read(root, "novel.md")
    text = text.replace('  foreknowledge: ""',
                        '  foreknowledge: "she has read the next four quarter calendars"')
    _write(root, "novel.md", text)

    # curve-pressure - a P that its own tiers contradict.
    text = _read(root, "state/power.md")
    # Their tier moves, not P: P still agrees with the CCS block, so only the row's internal
    # arithmetic is wrong and `curve-ccs` stays quiet.
    text = text.replace("| 2 | Hesk, procedurally | 2 | 2 | +0 |",
                        "| 2 | Hesk, procedurally | 4 | 2 | +0 |")
    _write(root, "state/power.md", text)

    # scene-break - a lone `*` where the one correct form is `* * *`. Word-for-word neutral: a
    # word is removed and the `*` replaces it, so `wordcount` and `ledger` stay out of it.
    rel = "chapters/0005-the-ghost-at-the-waterline.md"
    text = _read(root, rel)
    text = text.replace("without any ceremony at all.", "without any ceremony\n\n*\n\nall.")
    _write(root, rel, text)

    # markup - italics in a prose body. `*word*` is one whitespace token, exactly like the word
    # it replaces, so nothing downstream of the word count moves.
    rel = "chapters/0006-counter-claim.md"
    text = _read(root, rel)
    text = text.replace("what nine days of reading had turned up",
                        "what nine *days* of reading had turned up")
    _write(root, rel, text)

    # straddle - lift the only character below the MC up to her tier. Her eq moves with it,
    # so the plant stays a pure straddle failure rather than also tripping `eq-clash`.
    text = _read(root, "bible/cast/_voices.md")
    text = text.replace("| Bel | B | 2 | 3 | 2 |", "| Bel | B | 3 | 5 | 2 |")
    _write(root, "bible/cast/_voices.md", text)
