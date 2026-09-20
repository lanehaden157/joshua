# Session summary — 2026-09-19 — platform review G1, G2, G3

Continues `session_summary_2026-09-19_g1-correctness.md` (G1). This covers
the colour rework, G2 and G3.

## Colour checks (Lane's steer: don't over-engineer this)

Swapped to CIEDE2000 for both `assign_hues()` and `validate_units.py`, added
a book-wide "no two threads share a hex" assertion, and a ranked closest-pairs
line printed whether or not anything crosses the threshold. All warnings, never
failures. It earned its keep immediately: CIE76 rated `send`/`strong` as clear,
CIEDE2000 puts them at 7.3. One recolour pass moved the worst pair 5.0 → 6.9
and it was left there — unit 1 tags 16 roots against a palette that separates
about 13, and that is a ceiling to see coming, not a build to redden.

## G2 — the `data-w` assigner

`pipeline/assign_data_w.py`. Per verse, per tracked root: zip the id-set's
source hits against that verse's spans in document order. Counts agree →
assign; counts disagree → assign nothing there and say why. Never overwrites
an existing `data-w`. The bias is deliberate: a wrong `data-w` silently points
a reader's popover at the wrong Hebrew word, while a missing one is a hard
error the audit already catches.

Validated against real data both directions:

- Stripping every `data-w` from `units/unit-01.html` and re-running rebuilds
  the file **byte-identically** — all 38 spans, zero mismatches.
- On the source artifact (which has zero `data-w`): 37 of 38 assigned, and the
  one verse it refused is `rest 1:15` — the *yaniaḥ* case where one Hebrew word
  is rendered as two English words, subject of `b5bcee5` and a named example in
  CLAUDE.md's recipe step 4. It found the only genuinely ambiguous verse by
  itself.

**Per-unit cost: 38 hand-placements → 1 decision.**

A6 followed: `w` is optional in the incoming artifact and filled by the porter,
so "don't hand-chase word ids" and the contract stop contradicting each other.
The guarantee moved to the built fragment, where it was already enforced.

## G3 — the wording decisions

- **C10** ʿeved → **"slave"**, applied to unit 1's 5 occurrences. Slug stays
  `servant` (identifier, not reader-facing).
- **C12** shamayim → **"sky / skies"** everywhere, matching Matthew.
- **A21** WEB is **provenance only**, written down in `CLAUDE.md`.
- **A13** declined-candidate ledger in `roots.json`, validated, surfaced in
  the digest, and flagged by the porter on re-proposal.
- **D15/F20** canon conventions file deliberately deferred to G6.

## Corrections issued this session

1. WEB is not where the Hebrew comes from (morphhb is). This was the belief
   behind A21, so it changed what got written down.
2. The review's C12 verse list is wrong: 11:4 has no shamayim; the fourth
   occurrence is **10:13**.
3. A4 was worse than the review reported — the hue fallback emitted exact
   duplicates, not just near-collisions.

## Open / next

- **Needs Lane by hand:** `Claude_ai_chat_side_instructions.md` is out of the
  sync loop by design (2026-09-16), so the A6 edit to pass 3 will not reach the
  Claude.ai project on its own. Paste it, or unit 2 arrives under the old
  contract. Same for the style reference's §7 items 6 and 8 if the project
  holds its own copy.
- **A7** still unverified: OSHB letter suffixes are treated as opaque, 12 bare
  ids in Joshua carry more than one. Worth checking against `LexicalIndex.xml`
  before more roots are committed under that policy.
- **G4** is the next roadmap group: ship units 2–4, tracking every "I wish the
  contract said…" for D1.
- Four glossary entries still open: ḥerem, ḥesed, goel, nefesh.
