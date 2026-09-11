"""The trigger language.

Every expression the migration will write is exercised here against real novels, because a
trigger that is silently false disables a card and nothing else in the toolkit would notice.
"""

import unittest

from fixtures import TEMPLATE

from swlib import kbexpr
from swlib.kbexpr import TRUE, FALSE, UNKNOWN, Context, ExprError


class FakeNovel(object):
    """Only the surface `kbexpr.Context` touches: get, optional_on and the defaulted properties."""

    def __init__(self, cfg):
        self.cfg = cfg

    def get(self, key, default=None):
        return self.cfg.get(key, default)

    def optional_on(self, name):
        return str(self.cfg.get("optional.%s" % name, "off")).lower() in ("on", "true")

    @property
    def scaling_shape(self):
        s = str(self.cfg.get("scaling.shape", "climb") or "climb").strip().lower()
        return s if s in ("climb", "inverted", "regression", "plateau-late", "none") else "climb"

    @property
    def has_foreknowledge(self):
        return bool(self.cfg.get("mc.foreknowledge"))

    @property
    def form_locked(self):
        return bool(self.cfg.get("mc.form_locked"))

    @property
    def arc_length(self):
        n = self.cfg.get("chapters.arc_length", 25)
        return n if isinstance(n, int) and n > 0 else 25


def ev(expr, cfg=None, **builtins):
    return kbexpr.evaluate(expr, Context(FakeNovel(cfg or {}), **builtins))[0]


class TestMissingKeyDefaults(unittest.TestCase):
    """The highest-consequence bug class: an absent key must not switch a module ON.

    `pov.mode != single` against a novel with no `pov.mode` resolves "none" != "single" -> TRUE
    unless the path is routed through the Novel's own default. That would activate `pov-switch`
    on every novel that never configured POV.
    """

    def test_absent_pov_mode_does_not_enable_pov_switch(self):
        self.assertIs(ev("pov.mode != single", {}), FALSE)

    def test_declared_pov_mode_still_works(self):
        self.assertIs(ev("pov.mode != single", {"pov.mode": "dual"}), TRUE)
        self.assertIs(ev("pov.mode != single", {"pov.mode": "single"}), FALSE)

    def test_absent_romance_does_not_enable_lead_interest(self):
        self.assertIs(ev("content.romance != none", {}), FALSE)
        self.assertIs(ev("content.romance != none", {"content.romance": "subplot"}), TRUE)

    def test_absent_scaling_shape_defaults_to_climb(self):
        # scaling.shape defaults to climb, so power-scaling is ON by default - the opposite
        # default from pov.mode, and both come from novelio rather than from this module.
        self.assertIs(ev("scaling.shape != none", {}), TRUE)
        self.assertIs(ev("scaling.shape != none", {"scaling.shape": "none"}), FALSE)

    def test_absent_contract_by_ch_defaults_to_three(self):
        self.assertIs(ev("chapter <= opening.contract_by_ch + 2", {}, chapter=5), TRUE)
        self.assertIs(ev("chapter <= opening.contract_by_ch + 2", {}, chapter=6), FALSE)


class TestRealConditions(unittest.TestCase):
    """Every condition the two dispatcher tables carry today, in its migrated form."""

    def test_always(self):
        self.assertIs(ev("always"), TRUE)
        self.assertIs(ev("never"), FALSE)

    def test_story_opening_window(self):
        e = "chapter <= opening.contract_by_ch + 2"
        cfg = {"opening.contract_by_ch": 3}
        self.assertIs(ev(e, cfg, chapter=1), TRUE)
        self.assertIs(ev(e, cfg, chapter=5), TRUE)
        self.assertIs(ev(e, cfg, chapter=6), FALSE)

    def test_foreknowledge_is_set(self):
        self.assertIs(ev("mc.foreknowledge is set", {"mc.foreknowledge": "knows the war"}), TRUE)
        self.assertIs(ev("mc.foreknowledge is set", {"mc.foreknowledge": ""}), FALSE)
        self.assertIs(ev("mc.foreknowledge is set", {}), FALSE)

    def test_form_locked(self):
        self.assertIs(ev("mc.form_locked == true", {"mc.form_locked": True}), TRUE)
        self.assertIs(ev("mc.form_locked == true", {"mc.form_locked": False}), FALSE)
        self.assertIs(ev("mc.form_locked == true", {}), FALSE)

    def test_speakers(self):
        self.assertIs(ev("speakers >= 2", {}, speakers=3), TRUE)
        self.assertIs(ev("speakers >= 2", {}, speakers=1), FALSE)

    def test_optional_module_accepts_on_or_true(self):
        self.assertIs(ev("optional.no-harem == on", {"optional.no-harem": "on"}), TRUE)
        self.assertIs(ev("optional.no-harem == on", {"optional.no-harem": True}), TRUE)
        self.assertIs(ev("optional.no-harem == on", {"optional.no-harem": "off"}), FALSE)
        self.assertIs(ev("optional.no-harem == on", {}), FALSE)

    def test_genre_module_needs_or_across_two_paths(self):
        """`power-system` is on when the genre OR the subgenre matches - the reason `or` exists."""
        e = "genre in [fantasy, scifi, progression] or subgenre in [fantasy, scifi, progression]"
        self.assertIs(ev(e, {"genre": "fantasy"}), TRUE)
        self.assertIs(ev(e, {"genre": "fanfic", "subgenre": "progression"}), TRUE)
        self.assertIs(ev(e, {"genre": "fanfic", "subgenre": "reincarnation"}), FALSE)

    def test_and_binds_tighter_than_or(self):
        # TRUE and FALSE or TRUE  ==  (TRUE and FALSE) or TRUE  ==  TRUE
        self.assertIs(ev("genre == fanfic and chapter > 5 or speakers >= 2",
                         {"genre": "fanfic"}, chapter=1, speakers=3), TRUE)
        self.assertIs(ev("genre == fanfic and chapter > 5 or speakers >= 2",
                         {"genre": "fanfic"}, chapter=1, speakers=1), FALSE)


class TestKleene(unittest.TestCase):
    """UNKNOWN is include-at-runtime and defect-at-health, so it must not collapse to False."""

    def test_unknown_and_false_is_false(self):
        self.assertIs(kbexpr.k_and(UNKNOWN, FALSE), FALSE)

    def test_unknown_and_true_is_unknown(self):
        self.assertIs(kbexpr.k_and(UNKNOWN, TRUE), UNKNOWN)

    def test_unknown_or_true_is_true(self):
        self.assertIs(kbexpr.k_or(UNKNOWN, TRUE), TRUE)

    def test_unknown_or_false_is_unknown(self):
        self.assertIs(kbexpr.k_or(UNKNOWN, FALSE), UNKNOWN)

    def test_unevaluable_ordering_is_unknown_not_false(self):
        """A card whose trigger cannot be read must be opened, not silently skipped."""
        self.assertIs(ev("chapter <= opening.contract_by_ch + 2", {}), UNKNOWN)

    def test_unparseable_expression_is_unknown(self):
        self.assertIs(kbexpr.evaluate("chapter <=", Context(None))[0], UNKNOWN)


class TestParsing(unittest.TestCase):

    def test_kebab_path_is_one_word(self):
        """`optional.no-harem` must not lex as a subtraction."""
        self.assertEqual(kbexpr.paths("optional.no-harem == on"), {"optional.no-harem"})

    def test_offset_paths_are_reported(self):
        self.assertEqual(kbexpr.paths("chapter <= opening.contract_by_ch + 2"),
                         {"chapter", "opening.contract_by_ch"})

    def test_or_paths_are_reported(self):
        self.assertEqual(kbexpr.paths("genre in [a] or subgenre in [b]"), {"genre", "subgenre"})

    def test_empty_condition_is_an_error(self):
        self.assertRaises(ExprError, kbexpr.parse, "")
        self.assertRaises(ExprError, kbexpr.parse, "   ")

    def test_dangling_connective_is_an_error(self):
        self.assertRaises(ExprError, kbexpr.parse, "chapter > 1 and")
        self.assertRaises(ExprError, kbexpr.parse, "or chapter > 1")

    def test_explanations_name_the_term(self):
        _, why = kbexpr.evaluate("scaling.shape != none",
                                 Context(FakeNovel({"scaling.shape": "none"})))
        self.assertIn("scaling.shape != none", why[0])


class TestAgainstTheShippedTemplate(unittest.TestCase):
    """The template is half of every parser, so the triggers are checked against it too."""

    def test_every_path_exists_in_the_template(self):
        from swlib import novelio
        novel = novelio.Novel(TEMPLATE)
        flat = set(_flatten(novel.cfg))
        used = set()
        for expr in ("scaling.shape != none", "mc.foreknowledge is set",
                     "mc.form_locked == true", "chapter <= opening.contract_by_ch + 2",
                     "pov.mode != single", "content.romance != none",
                     "optional.no-harem == on",
                     "genre in [fanfic] or subgenre in [fanfic]"):
            used |= kbexpr.paths(expr)
        builtins = set(Context.BUILTINS)
        missing = sorted(p for p in used if p not in flat and p not in builtins)
        self.assertEqual(missing, [], "trigger paths absent from novels/_template/novel.md")

    def test_template_resolves_every_real_trigger(self):
        from swlib import novelio
        ctx = Context(novelio.Novel(TEMPLATE), chapter=1, speakers=2)
        for expr in ("always", "scaling.shape != none", "mc.form_locked == true",
                     "chapter <= opening.contract_by_ch + 2", "pov.mode != single",
                     "optional.no-harem == on"):
            got, why = kbexpr.evaluate(expr, ctx)
            self.assertIsNot(got, UNKNOWN, "%s did not resolve against the template: %s"
                             % (expr, why))


def _flatten(cfg, prefix=""):
    for key, val in (cfg or {}).items():
        path = "%s%s" % (prefix, key)
        yield path
        if isinstance(val, dict):
            for sub in _flatten(val, path + "."):
                yield sub


if __name__ == "__main__":
    unittest.main()
