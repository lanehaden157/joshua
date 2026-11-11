# Session Summary — 2026-09-22 (part 2)

## What was done

Ported unit 3 (`source-artifacts/joshua_03_translation.html` → `units/unit-03.html`),
Joshua 3:1–4:24, "Crossing the Jordan."

The artifact carried 8 `questions[]` for Lane. Got all 8 answers before porting,
then hand-edited the source artifact to match (not left for a later pass):

- ʾaron → **"chest"**, not the artifact's drafted "ark" (Lane overrode the draft).
  Applied to all 17 verse occurrences + 5 endnote mentions + the 3:11 echo aside.
  "chest of the testimony" (4:16) kept as its own fixed phrase.
- berit → **"covenant"**, locked.
- qadash/hitqaddeshu (3:5) → **"set yourselves apart"**, not "make yourselves holy."
- ʾerets → **"land"** at 3:11, 3:13, 4:24 (not "earth" as drafted). Renamed the
  unit's local root slug `earth` → `land` to match.
- y'all-for-2pl **extended to possessives** ("Yahweh y'all's God," "y'all's
  children") — Lane chose full consistency over the artifact's drafted split
  (pronouns marked, possessives left plain).
- Widened two tracked threads onto real unit-3 occurrences: `rest` (5117 → add
  3240, the causative "lay down" at 4:3/4:8) and `strong` (2388 → add 2389, the
  adjective at 4:24). Both updated in `data/roots.json` and `data/threads.json`,
  with new spans tagged in the fragment.
- Kept the 4:22 Jacob/Gen 32:10 aside as drafted.
- Confirmed unit 1's "sole" slug is reused (both units already agreed).

New payoff entries added to `data/threads.json`: `possess` at 3:10, `rest` at
3:13, `cross` at 3:17.

## Promotion candidates — sole/lodge/fear promoted, this-day held back

The artifact proposed 4 candidates for promotion to book-wide tracked threads:
`sole`, `lodge`, `fear` (all well-evidenced, recurring across units 1–5+), and
`this-day` (228 word-hits book-wide — likely too frequent to carry signal, same
shape as the already-declined `kol`).

Initially held off promoting `sole`/`lodge`/`fear`, reading `data/threads.json`'s
"hand-authored" note as "Lane picks the colour by hand." Lane corrected this
mid-session: colours are never hand-picked, full stop — the local-root
algorithm (`assign_hues()`) just had no tracked-thread counterpart yet. Wrote
one (`assign_tracked_colors()`), which immediately surfaced a real problem:
the 20-colour `WELL` palette was almost exhausted (15 tracked threads + 18
local roots across units 1+3 already), and its fallback path had already
produced one exact colour collision before this session (`servant`/`devote`,
pre-existing, left alone). Lane's call: expand the palette (needs ≥60 colours)
rather than accept degraded near-duplicate colours or pick one by hand.
Generated 45 new colours (Lab-space sampled in the original palette's own
lightness/chroma/contrast range, not hand-picked), bringing `WELL` to 65.
Promoted all three with algorithmic colours, retrofitted `data-w` onto their
spans in units 1 and 3.

`this-day` stays a candidate, not promoted — it isn't tagged with spans in
the fragment yet, so nothing forces the decision, and at 228 word-hits
book-wide it's a strong candidate for staying local/untracked on frequency
grounds (same shape as the already-declined `kol`).

## Verification

- `pipeline/build.py` clean: 0 gap/wrong-id/stray/missing-data-w across all
  18 tracked threads (15 → 18 this session) over the 3 built units.
- `validate_units.py`'s colour-collision check (DE_MIN=10, CIEDE2000) passes
  for every built unit, including the 3 newly-promoted colours.
- All `pipeline/test_*.py` pass, no regressions.
- Smoke-tested unit 3 live in the browser twice (before and after the
  promotion): legend renders every root/thread with a resolved colour, verse
  text matches the locked wording exactly, notes render, no console errors.
- `translation-choices.md`: added ʾaron, berit, qadash/hitqaddeshu, ʾerets rows;
  extended the y'all row to cover possessives; logged the session.
- New feedback memory saved: thread colours are always algorithmic.

## Open questions for Lane

- `this-day` — worth tagging as a phrase-thread exception at all, given how
  common the formula is (228 hits book-wide)? No decision needed yet; not
  currently tagged anywhere in the fragment.

## Not yet done

- Sync to the Claude.ai project (`pipeline/sync_to_github.py`) — pending
  commit/push per standing instruction (commit or push implies sync).
