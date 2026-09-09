"""`sw curve` - the power curve checks.

The defects these pin are the ones a reader reports as "the MC got too strong too fast" and
"nothing has been at stake for thirty chapters", neither of which any earlier check could see:
the escalation budget lived in `bible/`, which the read-set never loads and no script validated.
Everything here is countable. The judged half - whether a gain was earned on the page - stays in
power-scaling's audit card, deliberately.
"""

import unittest

from fixtures import NovelFixture, NOVEL_MD

from swlib import cmd_curve


def checks(rep):
    return {f.check for f in rep.findings}


def messages(rep):
    return " | ".join(f.message for f in rep.findings)


def power_md(pressure="", gains="", boosts="", standing=""):
    """A minimal state/power.md carrying only the tables under test."""
    return """# Power curve

## 1. CURRENT STANDING

| character | tier | since ch | the edge | what the edge cannot buy | active boost? |
|---|---|---|---|---|---|
%s

## 2. THE LADDER

| tier | what it lets you do | what it still cannot do | how many alive | who the reader has met |
|---|---|---|---|---|
| 1 | walk away from one man | walk away from three | many | the toll clerk |

## 3. THE PRESSURE LOG

| ch | opposition | their tier | MC tier | P | outcome | what it cost |
|---|---|---|---|---|---|---|
%s

## 4. THE GAIN LOG

| ch | from → to | source | price paid (ch) | set up in ch | what it obsoletes | new problem |
|---|---|---|---|---|---|---|
%s

## 5. ACTIVE BOOSTS

| ch | boost | above tier by | expires ch | the debt | due ch | paid? | climax? |
|---|---|---|---|---|---|---|---|
%s

## 6. THE CURVE PLAN

| arc | chapters | MC tier entry → exit | top opposition | pressure band | the gain, and where |
|---|---|---|---|---|---|
""" % (standing, pressure, gains, boosts)


SCALING = """
scaling:
  shape: %s
  tiers: 7
  start_tier: %d
  ceiling_tier: 6
  endgame: "the Archivist, tier 6"
  edge_worth: %d
  edge_price: "%s"
  substitute_tension: "%s"
  first_limit_by_ch: %d
  gain_gap_min: 15
  setup_lead: 3
  flat_max: 12
  trivial_per_arc: 2
  boost_debt_due: 5
"""


def novel_md(shape="climb", start=1, edge=1, price="a day of memory",
             substitute="", first_limit=8):
    block = SCALING % (shape, start, edge, price, substitute, first_limit)
    return NOVEL_MD.replace("\n---\n\n# Hook", block + "---\n\n# Hook")


def build(fx, **kw):
    fx.write("novel.md", novel_md(**kw))
    return cmd_curve.run(fx.novel())


class TestConfig(unittest.TestCase):
    """power-scaling section 4 - the shape and its requirements."""

    def test_a_climb_that_starts_near_the_top_is_a_defect(self):
        with NovelFixture() as fx:
            fx.write("state/power.md", power_md())
            rep = build(fx, start=5)
            self.assertIn("curve-config", checks(rep))
            self.assertIn("start_tier is 5", messages(rep))

    def test_a_low_start_is_clean(self):
        with NovelFixture() as fx:
            fx.write("state/power.md", power_md())
            self.assertNotIn("start_tier", messages(build(fx, start=2)))

    def test_inverted_without_a_substitute_tension_is_a_defect(self):
        with NovelFixture() as fx:
            fx.write("state/power.md", power_md())
            rep = build(fx, shape="inverted", start=6)
            self.assertIn("substitute_tension is empty", messages(rep))

    def test_inverted_with_one_is_allowed_and_skips_the_start_tier_rule(self):
        with NovelFixture() as fx:
            fx.write("state/power.md", power_md())
            rep = build(fx, shape="inverted", start=6, substitute="nobody believes him")
            self.assertNotIn("substitute_tension", messages(rep))
            self.assertNotIn("start_tier", messages(rep))

    def test_an_edge_worth_two_tiers_is_a_defect(self):
        with NovelFixture() as fx:
            fx.write("state/power.md", power_md())
            self.assertIn("at most", messages(build(fx, edge=2)))

    def test_a_free_edge_is_a_defect(self):
        with NovelFixture() as fx:
            fx.write("state/power.md", power_md())
            self.assertIn("edge_price is empty", messages(build(fx, price="")))

    def test_the_first_limit_must_come_after_the_first_win(self):
        with NovelFixture() as fx:
            fx.write("state/power.md", power_md())
            # the fixture's opening.first_win_by_ch is absent, so set the collision explicitly
            fx.write("novel.md", novel_md(first_limit=4).replace(
                "  contract_by_ch: 3", "  contract_by_ch: 3\n  first_win_by_ch: 5"))
            self.assertIn("is not after", messages(cmd_curve.run(fx.novel())))

    def test_shape_none_turns_everything_off(self):
        with NovelFixture() as fx:
            fx.write("state/power.md", power_md(gains="| 5 | 1 → 6 | a cave | | | | |"))
            rep = build(fx, shape="none")
            self.assertEqual(rep.count("defect"), 0)


class TestStepRule(unittest.TestCase):
    """power-scaling section 3 - no cannon fodder to god in one step."""

    GOOD = "| 20 | 1 → 2 | Master Oyo, who wants a favour | 18 | 4 | the old form | Oyo can call it in |"

    def test_a_gain_of_more_than_one_tier_is_a_defect(self):
        with NovelFixture() as fx:
            fx.write("state/power.md", power_md(
                gains="| 20 | 1 → 4 | Oyo | 18 | 4 | the old form | a debt |"))
            rep = build(fx)
            self.assertIn("curve-gain", checks(rep))
            self.assertIn("advances 3 tiers", messages(rep))

    def test_a_complete_plus_one_gain_is_clean(self):
        with NovelFixture() as fx:
            fx.write("state/power.md", power_md(gains=self.GOOD))
            self.assertEqual(build(fx).count("defect"), 0)

    def test_each_missing_requirement_is_its_own_defect(self):
        with NovelFixture() as fx:
            fx.write("state/power.md", power_md(gains="| 20 | 1 → 2 | | | | | |"))
            msg = messages(build(fx))
            for col in ("source", "price paid (ch)", "set up in ch", "new problem"):
                self.assertIn("no `%s`" % col, msg)

    def test_a_price_paid_after_the_gain_is_a_defect(self):
        with NovelFixture() as fx:
            fx.write("state/power.md", power_md(
                gains="| 20 | 1 → 2 | Oyo | 24 | 4 | the old form | a debt |"))
            self.assertIn("after the gain", messages(build(fx)))

    def test_a_setup_inside_the_lead_window_is_a_defect(self):
        with NovelFixture() as fx:
            fx.write("state/power.md", power_md(
                gains="| 20 | 1 → 2 | Oyo | 18 | 19 | the old form | a debt |"))
            self.assertIn("set up in ch 19", messages(build(fx)))

    def test_gains_closer_than_the_cadence_warn(self):
        with NovelFixture() as fx:
            fx.write("state/power.md", power_md(gains=self.GOOD + "\n" +
                     "| 24 | 2 → 3 | Oyo | 22 | 4 | the old form | a debt |"))
            rep = build(fx)
            self.assertIn("4 chapters apart", messages(rep))
            self.assertEqual(rep.count("defect"), 0)


class TestBoosts(unittest.TestCase):
    """power-scaling section 3 - plot armour is allowed; free plot armour is not."""

    def test_a_debt_overdue_and_unpaid_is_a_defect(self):
        with NovelFixture() as fx:
            fx.add_chapter(20, "word " * 10)
            fx.write("state/power.md", power_md(
                boosts="| 6 | the talisman | 2 | 7 | a year of growth | 9 | | |"))
            self.assertIn("still unpaid", messages(build(fx)))

    def test_a_paid_debt_is_clean(self):
        with NovelFixture() as fx:
            fx.add_chapter(20, "word " * 10)
            fx.write("state/power.md", power_md(
                boosts="| 6 | the talisman | 2 | 7 | a year of growth | 9 | yes | |"))
            self.assertEqual(build(fx).count("defect"), 0)

    def test_a_boost_missing_its_terms_is_a_defect(self):
        with NovelFixture() as fx:
            fx.write("state/power.md", power_md(boosts="| 6 | the talisman | | | | | | |"))
            msg = messages(build(fx))
            for col in ("above tier by", "expires ch", "the debt", "due ch"):
                self.assertIn("no `%s`" % col, msg)

    def test_a_second_climax_boost_is_a_defect(self):
        with NovelFixture() as fx:
            fx.add_chapter(30, "word " * 10)
            fx.write("state/power.md", power_md(boosts="\n".join([
                "| 6 | the talisman | 2 | 7 | a year | 9 | yes | yes |",
                "| 26 | the other one | 2 | 27 | a year | 29 | yes | yes |"])))
            rep = build(fx)
            self.assertIn("second boost resolving an arc climax", messages(rep))

    def test_one_climax_boost_is_allowed(self):
        with NovelFixture() as fx:
            fx.add_chapter(30, "word " * 10)
            fx.write("state/power.md", power_md(
                boosts="| 6 | the talisman | 2 | 7 | a year | 9 | yes | yes |"))
            self.assertEqual(build(fx).count("defect"), 0)


class TestPressure(unittest.TestCase):
    """power-scaling section 1 - the gap is the thing that is monitored."""

    def test_a_p_that_disagrees_with_its_tiers_is_a_defect(self):
        with NovelFixture() as fx:
            fx.write("state/power.md", power_md(
                pressure="| 4 | the Warden | 5 | 3 | +9 | lost | a hand |"))
            self.assertIn("its tiers give 2", messages(build(fx)))

    def test_a_win_while_outmatched_must_record_a_cost(self):
        with NovelFixture() as fx:
            fx.write("state/power.md", power_md(
                pressure="| 4 | the Warden | 4 | 3 | +1 | won | |"))
            self.assertIn("no recorded cost", messages(build(fx)))

    def test_too_many_trivial_fights_in_one_arc_warn(self):
        with NovelFixture() as fx:
            rows = "\n".join("| %d | thug | 1 | 3 | -2 | won | |" % i for i in range(1, 6))
            fx.write("state/power.md", power_md(pressure=rows))
            self.assertIn("face-slap treadmill", messages(build(fx)))

    def test_ten_fights_in_one_band_warn(self):
        with NovelFixture() as fx:
            rows = "\n".join("| %d | a rival | 3 | 3 | 0 | won | |" % i for i in range(1, 12))
            fx.write("state/power.md", power_md(pressure=rows))
            self.assertIn("have become a texture", messages(build(fx)))

    def test_a_varied_curve_is_clean(self):
        with NovelFixture() as fx:
            ps = [1, 0, -1, 1, 0, 2, 1, 0, -1, 1, 0]
            rows = "\n".join(
                "| %d | a rival | %d | 3 | %+d | won | a favour |" % (i + 1, 3 + p, p)
                for i, p in enumerate(ps))
            fx.write("state/power.md", power_md(pressure=rows))
            rep = build(fx)
            self.assertEqual(rep.count("defect"), 0)
            self.assertNotIn("curve-flat", checks(rep))

    def test_a_long_stretch_with_no_variation_warns(self):
        with NovelFixture() as fx:
            fx.add_chapter(40, "word " * 10)
            rows = "\n".join("| %d | a rival | 3 | 3 | 0 | won | |" % i
                             for i in (1, 8, 16, 24, 32))
            fx.write("state/power.md", power_md(pressure=rows))
            self.assertIn("curve-flat", checks(build(fx)))

    def test_a_long_tail_with_no_confrontations_at_all_warns(self):
        with NovelFixture() as fx:
            fx.add_chapter(40, "word " * 10)
            fx.write("state/power.md", power_md(
                pressure="| 2 | a rival | 3 | 3 | 0 | won | |"))
            self.assertIn("curve-flat", checks(build(fx)))


class TestArcBucketing(unittest.TestCase):
    """The trivial budget is per arc, and the ledger's `arc:` field decides which arc that is.

    Arcs do not reliably land on `chapters.arc_length` boundaries. Bucketing arithmetically puts
    a confrontation in the wrong arc's budget, and disagrees with what `sw arc` reports.
    """

    def _ledger(self, chs, arc):
        return "\n".join(
            "=C%04d= pov:Rin | loc:x | t:D1 | wc:3 | arc:%d\n"
            "dlv> x\nev> x\nchg> Rin: a->b\npwr> P=-2\nkno> Rin+{x}\nthr> ~T01(x)\n"
            "obj> x\nwld> x\nhook> x\n" % (c, arc) for c in chs)

    def test_the_ledger_arc_field_overrides_the_arithmetic(self):
        # arc_length is 25, so ch 1-5 look arithmetically like arc 1 - but the ledger says
        # they are arc 2, and a per-arc budget must follow the ledger.
        with NovelFixture() as fx:
            chs = list(range(1, 6))
            fx.write("state/continuity.md", self._ledger(chs, 2))
            rows = "\n".join("| %d | thug | 1 | 3 | -2 | won | |" % c for c in chs)
            fx.write("state/power.md", power_md(pressure=rows))
            msg = messages(build(fx))
            self.assertIn("arc 2 has 5 confrontations", msg)
            self.assertNotIn("arc 1 has", msg)

    def test_chapters_with_no_block_fall_back_to_the_arithmetic(self):
        with NovelFixture() as fx:
            rows = "\n".join("| %d | thug | 1 | 3 | -2 | won | |" % c for c in range(1, 6))
            fx.write("state/power.md", power_md(pressure=rows))
            self.assertIn("arc 1 has 5 confrontations", messages(build(fx)))


class TestLedgerAgreement(unittest.TestCase):
    """The `pwr>` line and state/power.md must agree, the way `wc:` and the body must."""

    BLOCK = ("=C0004= pov:Rin | loc:x | t:D1 | wc:3 | arc:1\n"
             "dlv> x\nev> x\nchg> Rin: a->b\npwr> %s\n"
             "kno> Rin+{x}\nthr> ~T01(x)\nobj> x\nwld> x\nhook> x\n")

    def test_a_disagreement_is_a_defect(self):
        with NovelFixture() as fx:
            fx.write("state/continuity.md", self.BLOCK % "P=-2 easy")
            fx.write("state/power.md", power_md(
                pressure="| 4 | the Warden | 5 | 3 | +2 | survived | ribs |"))
            self.assertIn("state/power.md records P=+2", messages(build(fx)))

    def test_agreement_is_clean(self):
        with NovelFixture() as fx:
            fx.write("state/continuity.md", self.BLOCK % "P=+2 survived")
            fx.write("state/power.md", power_md(
                pressure="| 4 | the Warden | 5 | 3 | +2 | survived | ribs |"))
            rep = build(fx)
            self.assertEqual(rep.count("defect"), 0)

    def test_a_block_with_no_pwr_line_warns(self):
        with NovelFixture() as fx:
            fx.write("state/continuity.md", self.BLOCK.replace("pwr> %s\n", ""))
            fx.write("state/power.md", power_md())
            self.assertIn("has no `pwr>` line", messages(build(fx)))


class TestFileGate(unittest.TestCase):
    """The conditional-state-file contract, the same one body.md and foreknowledge.md use."""

    def test_a_missing_ledger_is_a_defect_while_scaling_is_on(self):
        with NovelFixture() as fx:
            import os
            os.remove(fx.path("state", "power.md"))
            rep = build(fx)
            self.assertIn("curve-files", checks(rep))

    def test_a_missing_ledger_is_fine_when_shape_is_none(self):
        with NovelFixture() as fx:
            import os
            os.remove(fx.path("state", "power.md"))
            self.assertEqual(build(fx, shape="none").count("defect"), 0)


if __name__ == "__main__":
    unittest.main()


class TestEmptyPressureLog(unittest.TestCase):
    """Benchmark run #2, F2. `curve` printed its header and nothing else.

    Its only `rep.info` sat inside `_pressure`, after `if not series: return`, so a novel whose
    arc runs on institutional pressure rather than confrontations got a permanently clean curve —
    and `_flat`, the enforcement of hard rule 11, never ran either. A command that says nothing
    when it has nothing to complain about cannot be told from one whose parser is broken.
    """

    STANDING = "| Wren | 2 | 1 | a ledger nobody audits | a fight | no |"

    def _run(self, chapters):
        with NovelFixture(novel_md=novel_md()) as fx:
            fx.write("state/power.md", power_md(standing=self.STANDING))
            for n in range(1, chapters + 1):
                fx.add_chapter(n, "She counted the sacks again.\n")
            return cmd_curve.run(fx.novel())

    def test_it_prints_a_position_section_with_no_pressure_rows(self):
        """Was: header, `0 defect(s)`, and not one line between them."""
        rep = self._run(3)
        headings = [h for h, _ in rep.sections]
        self.assertIn("standing", headings,
                      "curve printed nothing against a populated power.md")
        body = " ".join(l for _h, lines in rep.sections for l in lines)
        self.assertIn("Wren", body)

    def test_an_empty_log_past_the_horizon_is_a_finding(self):
        """Was: silence. 300 chapters logging nothing read exactly like a healthy curve."""
        self.assertIn("curve-empty", checks(self._run(14)))

    def test_an_empty_log_early_is_not_yet_a_finding(self):
        self.assertNotIn("curve-empty", checks(self._run(3)))
