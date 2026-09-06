# story-opening — audit card

Opened by `revision-pass` **Pass 9b**, on chapters up to `opening.contract_by_ch + 2`. Skip
entirely outside that range.

Two of these are judgement calls a checklist cannot make, and this is exactly the pass that
silently no-ops when it is worked from a summary. If the anchor test or the ceiling is close,
open `SKILL.md` §1 and §3.

- [ ] **The anchor test.** Could a stranger reading only this chapter say what kind of story this
      is, where and when it happens, and what the POV character wants? Three shrugs is a fail
- [ ] For fanfic or transmigration: does the reader know **which** story they are in, and roughly
      **when** in it?
- [ ] Anchor-vocabulary count for this chapter is not zero — the `anchor? yes` terms in
      `bible/lexicon.md`. Across chapters 1–5 collectively, zero is a hard failure. `sw lint`
      prints the count and the terms it matched; a low but non-zero count is still a judgement call
- [ ] **The stakes ceiling.** Has any consequence escalated past the reader's ability to price it?
      Before a threat is dangerous, its mechanism must have been on the page — not in the bible.
      A threat the reader cannot price reads as somebody being arbitrarily strict
- [ ] `opening.promise` has been touched by `promise_touched_by_ch`
- [ ] The central advantage lands a legible win by `first_win_by_ch`, before any failure
- [ ] Chapter 1 only: the MC **acts**. They are not delivered through the chapter by other people

**The genre contract.** By `opening.contract_by_ch`, a reader can say what kind of pleasure this
book is offering, and the page has delivered a sample of it rather than a promise of it.
