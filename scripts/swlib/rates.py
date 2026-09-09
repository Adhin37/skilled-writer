"""Model prices, and the arithmetic that turns a token count into a dollar figure.

The transcripts carry no cost field, so cost here is **computed, never read**. That makes the
rate table an assumption, and an assumption a reader cannot see is the failure mode this whole
toolkit is written against - so every report that prints a dollar figure also prints the table it
used, and `--rates <file>` replaces it.

Rates are US dollars per million tokens, from Anthropic's published API pricing. Cache is priced
off the model's own input rate by three standard multipliers: a 5-minute cache write costs 1.25x
input, a 1-hour write 2x, and a cache read 0.1x - except on Fable 5.1, where a read is 0.025x
($0.25/MTok), which is why the read rate is stored per model rather than derived at the call site.
"""

import json

MILLION = 1000000.0

# input, output, cache-read - dollars per million tokens.
_BASE = {
    "claude-fable-5-1":   (10.00, 50.00, 0.25),
    "claude-mythos-5-1":  (10.00, 50.00, 1.00),
    "claude-fable-5":     (10.00, 50.00, 1.00),
    "claude-opus-5":      (5.00, 25.00, 0.50),
    "claude-opus-4-8":    (5.00, 25.00, 0.50),
    "claude-opus-4-7":    (5.00, 25.00, 0.50),
    "claude-opus-4-6":    (5.00, 25.00, 0.50),
    "claude-sonnet-5":    (2.00, 10.00, 0.20),
    "claude-sonnet-4-6":  (3.00, 15.00, 0.30),
    "claude-haiku-4-5":   (1.00, 5.00, 0.10),
}

WRITE_5M_MULTIPLIER = 1.25
WRITE_1H_MULTIPLIER = 2.00

# Anything unrecognised. Named rather than guessed at, so an unpriced model is visible in the
# report instead of quietly costing whatever the last model cost.
UNKNOWN = "(unpriced)"


class Rates(object):
    """A price list. `Rates()` is the published table; `Rates.load(path)` is the user's."""

    def __init__(self, table=None, source="built-in published rates"):
        self.table = dict(_BASE)
        if table:
            for model, spec in table.items():
                self.table[model] = _coerce(spec)
        self.source = source
        self.unpriced = set()

    @classmethod
    def load(cls, path):
        with open(path, encoding="utf-8") as fh:
            data = json.load(fh)
        if not isinstance(data, dict):
            raise ValueError("a rates file must be a JSON object of model -> rates")
        return cls(data, source=path)

    def known(self, model):
        return _canon(model) in self.table

    def row(self, model):
        return self.table.get(_canon(model))

    def cost(self, model, input_tokens=0, cache_write_5m=0, cache_write_1h=0,
             cache_read=0, output_tokens=0):
        """Dollars for one model's usage. An unpriced model contributes 0 and is recorded."""
        row = self.row(model)
        if row is None:
            self.unpriced.add(model or "(unknown)")
            return 0.0
        rin, rout, rread = row
        return (input_tokens * rin
                + cache_write_5m * rin * WRITE_5M_MULTIPLIER
                + cache_write_1h * rin * WRITE_1H_MULTIPLIER
                + cache_read * rread
                + output_tokens * rout) / MILLION

    def describe(self, models=None):
        """The table as report lines, restricted to the models actually seen."""
        names = sorted(models) if models else sorted(self.table)
        out = ["   $/million tokens, from %s" % self.source,
               "   %-20s %8s %8s %10s %10s %10s"
               % ("model", "input", "output", "read", "write 5m", "write 1h")]
        for name in names:
            row = self.row(name)
            if row is None:
                out.append("   %-20s %8s   %s" % (name[:20], UNKNOWN,
                                                  "not in the table - costs 0 below"))
                continue
            rin, rout, rread = row
            out.append("   %-20s %8.2f %8.2f %10.2f %10.2f %10.2f"
                       % (name[:20], rin, rout, rread,
                          rin * WRITE_5M_MULTIPLIER, rin * WRITE_1H_MULTIPLIER))
        out.append("   if your rates differ, every dollar figure scales linearly")
        return out


def _canon(model):
    return str(model or "").strip()


def _coerce(spec):
    """Accept either [in, out, read] or {\"input\": .., \"output\": .., \"cache_read\": ..}."""
    if isinstance(spec, dict):
        return (float(spec.get("input", 0)), float(spec.get("output", 0)),
                float(spec.get("cache_read", spec.get("input", 0) * 0.1)))
    seq = list(spec)
    if len(seq) == 2:
        seq.append(float(seq[0]) * 0.1)
    return (float(seq[0]), float(seq[1]), float(seq[2]))


def total_cost(rates, per_model):
    """Sum cost across {model: usage-dict}. Usage keys match `transcripts` field names."""
    total = 0.0
    for model, u in per_model.items():
        total += rates.cost(
            model,
            input_tokens=u.get("input_tokens", 0),
            cache_write_5m=u.get("cache_write_5m", 0),
            cache_write_1h=u.get("cache_write_1h", 0),
            cache_read=u.get("cache_read_input_tokens", 0),
            output_tokens=u.get("output_tokens", 0))
    return total
