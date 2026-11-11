# Session summary — 2026-09-19 — platform review G1

## Scope

Lane added `platform-design-review.md` (a menu of items A–H across Joshua and
Matthew) and asked what implementing **G1–G3** would look like. After the
scoping answers below, G1 was implemented in full. G2 and G3 were not started.

## Decisions Lane made this session

- **A2** — add the `opens.note` slot (rather than dropping the requirement).
- **A3** — Claude's call. Lane's steer: "a local root being tracked beyond its
  chapter is much less a problem than a tracked root being kept local when it
  shouldn't be." (That bias is about *promotion*, A18/A19; it does not by
  itself settle what `roots[]` means — see below.)
- **A5** — Claude's call, "too technical."
- **C10** — ʿeved → **slave**, matching Matthew's doulos rule. *Not yet
  applied; belongs to G3.*
- **Scope** — do it whichever way is most efficient.

## Correction issued

Lane believed WEB was where both the Hebrew and English texts came from. The
Hebrew is morphhb 2.0.2 (`pipeline/corpus/wlc/Josh.xml`); WEB is an
independent public-domain English translation. So **A21 — "what is
`Joshua-english.txt` actually for?" — is still an open question**, deferred to
G3 rather than answered by assumption.

## What shipped (G1)

See `improvements_log.md` 2026-09-19 for the itemised record. Headline:

1. **A1/A2** — `generate()` did not round-trip the `note` that `validate()`
   requires, so every `build.py` run silently wrote `units/unit-01.html` into
   a shape the project's own validator rejected (10 errors). Fixed for both
   `opens` and `payoffs`.
2. **A3 decided: `roots[]` is local roots only.** Grounded in
   `app/threads.js` `resolveUnit()`, which resolves a tracked `data-root`
   from `threads.json` directly — so re-declaring tracked threads in
   `roots[]` would buy nothing and go stale. Style reference §1 amended.
3. **A4** — worse than the review reported. Collision avoidance was blind to
   *every* tracked colour, and its exhaustion fallback emitted exact
   duplicates of tracked-thread colours. Both fixed.
4. **A20** — new `pipeline/validate_units.py`, a hard build step over
   `units/*.html`. Contract breaches fail; colour distance warns.
5. **A9, A17, A18, A22** — stale text, transliteration overrides in reports,
   promotion authority aligned, repo-move residue committed.
6. **Test gap closed** — the A1 regression test passed only because its
   fixture had zero threads. New test covers opens *and* payoffs;
   mutation-checked. 37 → 44 checks.

Verified: full suite green, `build.py` green, coverage 0/0/0/0, browser render
clean (16 roots, 69 spans, 16 swatches, no console errors).

## Open question for Lane — thread density vs. palette

**Unit 1 tags 16 distinct roots. The 20-colour `WELL` yields only 13 mutually
distinguishable at dE≥12.** The unit is over-subscribed; the best achievable
leaves three pairs at dE 11.0–11.5, and two of them (*yarash*/*gibbor ḥayil*,
*naḥal*/*shabar*) are visibly similar in the rendered legend. This is review
item **H11** arriving at unit 1 instead of later. Options, none taken:

- widen `WELL` with hues that hold Joshua's theme (clay / bronze / Jordan teal);
- lower `DE_MIN` from 12 to 10 (16 roots fit exactly — no headroom for unit 2);
- tag fewer roots per unit (editorial, Lane's call).

Deliberately left as a build *warning*, so it is said out loud every build
without blocking work.

## Next

- **G2** — the `data-w` assigner (A5), then the chat/contract reconciliation
  (A6). The largest per-unit manual cost.
- **G3** — apply C10 (slave), decide C12 (shamayim) before unit 2's Rahab,
  answer A21, add the A13 declined-candidates ledger.
- **A7** (unverified) — OSHB letter suffixes are treated as opaque; 12 bare
  ids in Joshua carry more than one. Worth checking against
  `LexicalIndex.xml` before more roots are committed under that policy.
- The canon conventions file (D15/F20) is **deferred to G6**: Joshua and
  Matthew are sibling repos with no shared parent, so it has no real home yet.
