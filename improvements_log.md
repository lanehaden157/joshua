# Improvements Log

## 2026-09-12
- Created `dozeman_vol1_fixed.txt` from the vol 1 .txt inside `Downloads\AYBC - 6.1. Iosue 1–12 (Thomas B. Dozeman, 2015) Yale.zip`. Mapped 10 private-use digit glyphs (U+F639, U+F63A–F641, U+F6DC) to 0–9. 108,870 glyphs replaced, 0 left.
- Vol 2 (`AYBC - 6.2`) text checked: no private-use glyphs, no fix needed.

## 2026-09-14
- Wrote `CLAUDE.md` (didn't exist before). Pinned morphhb 2.0.2 fresh in this repo (`npm install morphhb@2.0.2 --save-exact`) and HebrewLexicon @ `21c9add13bc727d3a951361778e97e3ff7afd1ce`; nothing was pinned here before this — the earlier morphhb pin from session history lives in `Projects\Hebrew`, not here.
- Verified `pipeline/corpus/wlc/Josh.xml` (copied from the pinned package) against printed BHS: 658 verses, ch. 21 = 45 verses (21:36–37 present, unmarked), 10,083 `<w>` elements (10,051 main text + 32 Qere alternates), 52 petuhah + 42 setumah.
- Generated `Joshua-reading.txt` (pointed Hebrew, `Josh C:V<TAB>text`, Qere substituted at the 32 Ketiv/Qere slots), `Joshua-words.tsv` (one row per `<w>`, Ketiv and Qere each keep their own id), and `candidate-boundaries.md` (94 petuhah/setumah markers, unclustered) via `pipeline/build_reading.py`.
- Generated `Joshua-english.txt` (WEB classic/WEBUS, `eng-web` from eBible.org, "Yahweh" not "LORD") via `pipeline/build_english.py`, from USFM pinned at `pipeline/corpus/web/07-JOSeng-web.usfm`. Stripped footnote markers and Strong's-number word wrappers. 658 lines, asserted equal to `Joshua-reading.txt`'s verse count (it is). Kept as a separate file rather than a third column on `Joshua-reading.txt`, since the Hebrew file's two-column shape is already read elsewhere.

## 2026-09-14 (part 2)
- Built `pipeline/hebrew.py`, the Hebrew sibling to `Projects/Matthew/pipeline/greek.py`. Niqqud/cantillation detection via `unicodedata.combining() != 0` (not a hand-rolled range check, which would also catch maqqef/sof-pasuq). Handles phrases without losing spaces; word-initial shuruq renders `u-` not `w-`; `OVERRIDES` table (keyed by bare consonant skeleton) covers YHWH, Jerusalem (both spellings), and kol; ayin gets a trailing combining low line so it's distinguishable from alef in plain text, not just via a wrapping HTML span.
- `pipeline/test_hebrew.py`: 30 word-level cases pulled by id from `Joshua-words.tsv` (YHWH x2, kol bare/prefixed x3, Jerusalem bare/prefixed, Ketiv/Qere pair, word-initial shuruq, begadkefat and shin/sin-dot minimal pairs, heavy niqqud/cantillation stacking), plus a full-verse phrase case (Josh 1:1, proves spaces survive) and an isolated maqqef case. All 32 checks pass. This test file, not `hebrew.py`'s docstring, is the scheme's authoritative definition.
- **Bug fix, caught in review**: bare vav+holam (plene "o" spelling, holam male) was rendering as consonant "w" + vowel "o" instead of vowel "o" alone -- Yehoshuaʿ's own name came out `yehwošuʿ̲a`. Not an edge case: 1,191 of 10,083 words in Joshua (~12%) carry this pattern. Fixed by giving holam male the same vowel-only treatment as shuruq; all 32 test cases updated to the corrected output. Also checked (not assumed) whether the skeleton-keyed override table risks homograph collisions: scanned all 469 skeleton matches in Joshua's actual vocabulary against their lemmas -- zero mismatches for the three current entries (kol 236, YHWH 224, Jerusalem 9).


## 2026-09-14 (part 3)
- Forked `pipeline/audit_thread_coverage.py` from `Projects/Matthew/pipeline/audit_thread_coverage.py` for Hebrew. Added `hebrew_words()`/`hebrew_morphemes()` to `hebrew.py` (reusable tokenizer, also used by `transliterate()` now). `strip_accents()` folds Hebrew final letters to medial (ך/ם/ן/ף/ץ) -- without it the *singular* lexical citation form (מֶלֶךְ, melek) fails to match, not an edge case. Matching is per-morpheme (splitting OSHB's `/` boundaries) rather than per whole surface word. Source filename/line-prefix now read from `data/units.json`'s `book` field instead of hardcoded, with a loud self-check against the file's own first line.
- `pipeline/thread-stems.json` documents `stems`/`exclude`/`strip_prefixes` together in a `_schema` field from the start. Confirmed live on real text (not hypothetical): anchored stem `^כל` for kol over-matches Caleb + כלה/כלי roots (251 raw hits, 236 real + 15 homographs) -- exactly the over-match risk the design doc warned about, reproduced and locked into `verify_thread_coverage.py` as a regression check.
- Wrote `pipeline/verify_thread_coverage.py` *before* any thread generator exists for this project (per house rule: Matthew's worst silent bug shipped across seven files before a verifier existed for it). Independently re-implements `strip_accents` and the morpheme tokenizer (not imported) and checks them against real word ids from `Joshua-words.tsv` and all 658 verses of `Joshua-reading.txt` -- same anti-hand-typing discipline as `test_hebrew.py`. All checks pass.
- Added empty scaffolding (`data/units.json` with `book: "Joshua"`, `data/threads.json`, `pipeline/thread-stems.json`) so both scripts actually run today -- no fabricated thread/unit content, just an accurate empty state.

## 2026-09-14 (part 4)
- Forked `pipeline/unit_meta.py` from Matthew's, hardening `validate()`/adding `validate_fragment()` with four checks Matthew didn't have until after the cost was paid: (1) unknown top-level meta-block keys are a hard failure (`ALLOWED_TOP_LEVEL_KEYS`) -- this is the check that would have caught Matthew's "descriptor"/"discourse" silently-dropped-across-eleven-units bug; (2) component whitelist -- every fragment `class=` must be defined in `css/styles.css` (grep-diff), and `legend` must be present; (3) endnote id/href sets must match exactly; (4) zero native Hebrew script (U+0590-U+05FF) anywhere in a fragment except `threads.candidates[].stems` -- `exclude` is explicitly NOT exempt, stated in the failure message.
- Added `css/styles.css` as a starter scaffold (mirrors Matthew's `.unit`/`.legend`/`.v`/`.n`/`.translit` naming) so the component-whitelist check has something real to diff against.
- `pipeline/test_unit_meta.py`: 12 checks against synthetic fragment fixtures (no real units exist yet), proving each of the four hardened checks fires on the right failure and stays quiet on a clean fragment. Hebrew text in the fixtures is still pulled live from `Joshua-reading.txt`, not hand-typed. All pass.

## 2026-09-14 (part 5)
- Lane added `Port analysis.md` (full Matthew-pipeline port audit: ~85% directly reusable, ~10% new module, ~5% param changes -- §7's ranked gap list matches items 1-8 already closed this session) and `joshua_literary_unit_map.md` (24 units, 4 movements, chs. 1-9 checked against Masoretic petuhah/setumah, 10-24 scholarship-grounded/draft).
- Wrote `PLAN.md`: phase list grounded in the port analysis's reuse assessment and the literary unit map's content backbone, carrying forward its §7 findings (1-8 done, 9 open -- Joshua's compare-box shape undecided, 10-11 done this pass).
- Seeded `data/roots.json` (empty, flat `{root,translit,gloss}` shape only -- Matthew built and reverted a richer kind/motif taxonomy the same day it shipped, Port analysis.md §3.5, not repeating that).
- Refined `data/threads.json`'s `_note` to document the real per-thread shape (id/root/translit/gloss/color/status/tagged/opens/payoffs/note, matching Matthew's actual schema) and added `version: 1`.
- `translation-choices.md`: seeded at unit 1, not unit 10 (Matthew's arrived late and cost a retroactive reconciliation pass, Port analysis.md §7.10). One seeded row (divine name -> Yahweh, matching `hebrew.py`'s `OVERRIDES`), six open TODO rows with no default filled in (herem, hesed, nachalah, goel, nefesh, y'all-for-2pl) -- Hebrew citation forms pulled from `Joshua-words.tsv` by real word id, not hand-typed.
- Ported `pipeline/threads_digest.py` (threads.json -> threads-digest.md) from Matthew's, unchanged in structure per Port analysis.md §1.8 (pure generic-schema logic). Ran it against the real empty `threads.json` (round-trips clean, 0 threads) and separately against a synthetic populated one (table + notes render correctly) to prove both code paths before unit 1.
- Fixed `session_index.md`'s header to match Matthew's day-one convention ("Read this first. 3 lines max per session.").

## 2026-09-14 (part 6)
- Lane added `joshua_study_style_reference.md` (the artifact contract) and `instructions.md` (renamed from `project side instructions.md` to match Matthew's plain filename convention).
- **Found a real divergence between the style reference and this session's earlier work, not just an extension of it:**
  - Style reference §2 measures substring-stem matching against real OSHB Joshua and rejects it: *natan* 42% recall, *qum* 24%, *nakah* 3%, **Yehoshuaʿ 0%**. Design is id-based instead -- `data/roots.json` holds curated Strong's-id sets, tagged spans carry `data-w="<word id>"`, the audit does set arithmetic. This obsoletes `pipeline/thread-stems.json`'s approach and most of `audit_thread_coverage.py`'s matching logic (`_compile_stems`, `hebrew_hits`, `strip_prefixes`).
  - `hebrew.py`'s scheme has three corrections needed: no vowel length (`mishpaṭ` not `mišpāṭ` -- currently uses ā/ē/ō macrons), no spirantization (`melek` not `melekh` -- currently alternates bet/kaf/pe stop/fricative by dagesh), and YHWH should transliterate as bare `YHWH` (currently bakes "Yahweh" directly into `OVERRIDES`; "Yahweh" is a `translation-choices.md` decision, not a transliteration output). Dagesh-forte gemination and vocal-sheva-under-doubling aren't implemented at all yet.
  - `unit_meta.py`'s `threads.candidates[]` shape needs to change from `{root, why, stems?, exclude?}` to `{root, why, ids?, refs?}` to match.
  - Logged as `PLAN.md`'s new Phase 0.6 (blocks Phase 1), not started -- confirming scope with Lane first since it touches most of Phase 0's engineering. `CLAUDE.md` got inline warnings at both affected sections rather than being silently left to describe superseded behavior as current.
- Built `project-side/README.md`: a pointer index (paths + direction + update cadence) for every file that round-trips with the Claude.ai research project, not a folder of duplicated copies -- `instructions.md` itself warns against that exact mistake ("Matthew's contract lived in three places and drifted").
- Resolved PLAN.md's two open questions: no Matthew-style compare box (style reference's narrower `aside.echo` instead, ship only if unit 1 needs it); Literary Unit Map units 10-24 confirmed as-is by Lane.

## 2026-09-14 (part 7)
- Wrote `phase-0.6-plan.md`: self-contained rework plan for a fresh session (decisions to ask Lane first, then hebrew.py scheme, roots.json id-sets, id-based audit, verify rewrite, unit_meta.py contract alignment, css whitelist, docs), grounded in measured current output by word id.
- **Correction to part 6**: `hebrew.py` does NOT use macrons -- its vowels are already plain a/e/i/o/u. The real scheme gaps are spirantization, sheva always voiced, shin as `š`, no dagesh-forte doubling, no furtive patach, hiriq-yod as `iy`, skeleton-keyed overrides, and YHWH output. Fixed the wrong claim in `PLAN.md` and `CLAUDE.md`.
- Found further `unit_meta.py` divergences from the style reference while planning: `descriptor`/`discourse` still allowed (§3 excludes them), the `candidates[].stems` no-Hebrew exemption contradicts checklist 12 ("no exceptions"), `kind`/`members` rejection was dropped in the fork, and opens/payoffs `note` isn't required. All folded into the plan's §F.

## 2026-09-14 (part 8) -- Phase 0.6 begins
- Batched and got answers to all 8 phase-0.6-plan.md §A decisions from Lane: tsadi = `ts` digraph, morpheme boundaries hyphenated (`ha-melek`), keep the ayin combining-underline convention, Ketiv/Qere tag the Qere id, one-id-in-two-roots is a hard fail, `data/roots.json` holds tracked threads only (not local roots), override API is word-level (`transliterate_word`) + verse-level (`transliterate_ref`) + a no-override bare fallback, `pipeline/thread-stems.json` gets deleted (not archived).
- **Rewrote `pipeline/hebrew.py`** per §B: no spirantization (bet/kaf/pe always b/k/p), sheva na/nach rules ported from `Projects/Hebrew/pipeline/transliterate.py` plus the added "vocal under a doubled consonant" case, dagesh-forte doubling (lene/forte distinguished for begadkefat letters by whether the dagesh follows an audible vowel; non-begadkefat letters' dagesh is always forte except vav-shuruq/he-mappiq), tsere-yod mater added alongside hiriq-yod, furtive patach (vowel-before-consonant reorder), tsadi as `ts`, sin as `ś` (shin stays the `sh` digraph, distinct from `ś`), overrides re-keyed on lemma id (YHWH/Jerusalem/kol) instead of consonant skeleton, and bare `YHWH` output (no more baked-in "Yahweh" — that's `translation-choices.md`'s job). Added `transliterate_word(surface, lemma, morph)` and `transliterate_ref("Josh C:V")`; overrides now only apply through these two, not bare `transliterate()`. `_align_lemma_to_surface()` lines up OSHB's lemma segments (which skip pronoun-suffix morphs) with surface morphemes by walking `morph`'s segments — validated over all 10,083 rows via the corpus sweep test, zero misalignments.
- **Rebuilt `pipeline/test_hebrew.py`** with every expected value hand-derived from dumped Unicode codepoints and the documented rules (not copied from the generator's output) — caught two of my own transcription slips this way (missed a dagesh on shin in 06bjL, missed a final mem in 06VdU) by re-deriving rather than trusting the first pass. 33 word cases (covers the plan's whole measured-output table plus dagesh-forte doubling, both consecutive-shva-pair cases, lene-vs-forte, furtive patach, tsere-yod, a Ketiv/Qere pair, word-initial shuruq), 3 `transliterate_ref`-vs-`transliterate_word` agreement cases, 1 phrase case, 1 maqqef case, and a full 10,083-word corpus sweep (0 failures — no crashes, no empty output, alphabet-only output). 10,120 checks total, all passing.
- Found and fixed a real bug during self-verification (not in review after the fact): `_CONSONANTS` was missing a plain "w" entry for vav, so any word with a genuinely consonantal (non-mater) vav crashed with `KeyError`. Caught by the very first hand-derived-case run, before any test file was written.

## 2026-09-14 (part 9) -- Phase 0.6 continued (C, D, E)
- **`data/roots.json`** reshaped per §C: from the old flat `{root,translit,gloss}` scaffold to the id-based `{ids, note}` registry (tracked threads only, per §A6 -- local roots stay in a unit's own `unit-meta` `roots[]`). New `pipeline/roots.py` loader/validator: slug format, non-empty `ids`+required `note`, every id's bare form must exist as a lemma in `Joshua-words.tsv`, an id claimed by two roots is a hard failure (§A5), `kind`/`members`/`translit`/`gloss`/`color` are all rejected (wrong file for those), and every `threads.json` thread's `root` must resolve to an entry here. `pipeline/test_roots.py`: 11 checks against synthetic fixtures built from real ids (3068/3389/3605, already confirmed live in the corpus via hebrew.py's overrides) -- unknown id, bad slug, lettered-id normalization, id-in-two-roots, missing note, kind/members rejection, translit/gloss rejection, thread-with-missing-root, thread-with-present-root. All pass. Also had to extend the id-parsing regex mid-build: found 67 real lemma segments in Joshua-words.tsv ending in a bare `+` (OSHB's own marker for a lemma continuing into an adjacent word as part of a multi-word proper name, e.g. "Bet-" + "-el"), not just the documented space+letter form -- caught by running roots.py's `known_lemma_ids()` over the real file rather than assuming the two documented forms were exhaustive.
- **Rewrote `pipeline/audit_thread_coverage.py`** per §D: set arithmetic over word ids, not substring-stem matching. `load_words()` drops Ketiv rows (detected by an adjacency pattern -- same ref, an unpointed row immediately followed by a pointed one -- verified against the whole corpus to find exactly the documented 32 pairs, zero exceptions, zero lone unpointed rows elsewhere) so the audit tags/counts the Qere id per §A4. `source_hits_for_root()` matches a word into a root by checking whether ANY of its lemma segments' bare ids intersect the root's id set (so a prefixed word like "we-kol" still counts as one whole-word occurrence, matching how `data-w` tags the whole surface word). `coverage_for_fragment()` now reports three categories per tracked thread -- **gap** (source id in-range, untagged), **wrong** (tagged id whose lemma isn't in the root's set), **stray** (tagged id that's out of range or doesn't exist) -- plus a hard `missing_data_w` count for any tracked-thread span lacking the attribute entirely. Local (non-thread) roots keep the old per-verse `tagged_map()` view, informationally, since they have no id set to audit against. Removed `_compile_stems`/`hebrew_hits`/`strip_prefixes`/`HEBREW_PREFIX_LETTERS`/`strip_accents` entirely. `--forms` replaced with `--ids <root>` (lists every surface form + ref a root's id set pulls in, counted by word id per §6's Beth-el note). Kept the book-field source lookup + self-check, `--unit`/`--stub`, `coverage_for_unit`/`coverage_for_fragment`. Runs clean (0/0/0/0) against the current empty threads.json/roots.json.
- **Rewrote `pipeline/verify_thread_coverage.py`** per §E, written before any real unit/thread exists. Re-derives source-id matching independently (own Ketiv detection, own bare-id parser, `csv.reader` + manual header-index lookup rather than `DictReader`, no import of `roots.py`'s or `audit_thread_coverage.py`'s matching functions) and cross-checks it against the real `audit_thread_coverage.source_hits_for_root()` for kol/YHWH -- would catch a divergence in either implementation. Retired the old final-letter-fold and kol/Caleb stem-over-match checks (neither applies to id-based matching); replaced with a live regression pulled from the TSV at check time (the `{3605}` id set's hit count never exceeds the raw row count, and never includes Caleb's `3612`). Five synthetic fragment fixtures, built from real word ids (06XR4 kol, 06k5P YHWH, 06yw4 we-kol), each isolating exactly one of the required failure shapes: gap, wrong-lemma id, missing data-w, stray-outside-passage, nonexistent id -- plus a clean-fragment case. 10/10 checks pass.
- Deleted `pipeline/thread-stems.json` per §A8 (nothing in the pipeline reads it anymore; prose mentions elsewhere -- `unit_meta.py`, `threads_digest.py`, `CLAUDE.md`, `PLAN.md` -- are Phase F/H cleanup, not yet done).

## 2026-09-14 (part 10) -- Phase 0.6 continued (F, G)
- **Reworked `pipeline/unit_meta.py`** per §F to match `joshua_study_style_reference.md` exactly: `ALLOWED_TOP_LEVEL_KEYS` drops `descriptor`/`discourse` entirely (§3's table has no such keys); `threads` now requires all four sub-keys present (`opens`/`payoffs`/`candidates`/`retro`, empty lists fine) instead of only type-checking whichever happen to be there; `opens`/`payoffs` entries require a `note` (checklist 4); `roots[]` now also rejects `kind`/`members` (this fork had dropped that check somewhere along the way); `threads.candidates[]` reshaped from `{root, why, stems?, exclude?}` to `{root, why, ids?, refs?}` -- `stems`/`exclude` are now a hard rejection, `why` is now required (wasn't checked before), `ids` must match `^\d+[a-z]?$`, `refs` must match `C:V`. Removed the `candidates[].stems` Hebrew-script exemption entirely -- checklist 12 says "no exceptions, attribute values included," and the exemption's own field doesn't exist in the schema anymore anyway. Added the four cheap fragment checks the plan asked for: `check_data_root_resolves` (checklist 6), `check_tracked_spans_have_data_w` (checklist 7), `check_pericope_headings` (checklist 9), `check_no_inline_style` (checklist 13, also catches `--c-*` vars) -- all folded into `validate_fragment()`. Added `warnings_for_fragment()` as a separate, non-fatal channel for `class="rl"` inside a `.v` block (§4: valid outside verse blocks, only mislabels intent inside one -- a warning, not a hard failure, kept structurally distinct from `validate_fragment()`'s hard-error list). `REQUIRED_COMPONENT_CLASSES` is now `{block, legend}` (the legend is `section.block.legend`, both tokens required).
- **`pipeline/test_unit_meta.py`** rewritten alongside it: 37 checks (was 12), covering every one of the above plus the flipped Hebrew-in-candidates test (used to assert exemption, now asserts no exemption) and a **new acceptance test**: pulls the §8 worked example's fenced ```html``` block straight out of `joshua_study_style_reference.md` at test time (regex-extracted, never copied) and runs it through `validate()` + `validate_fragment()` against a synthetic `devote`/`give` threads.json fixture -- passes with zero errors. This is the contract test between the style reference and the validator; if either ever drifts, it fails.
- **`css/styles.css`** (§G): replaced the old Matthew-mirrored placeholder vocabulary (`.legend`, `.endnotes .en`, `.translit`, `.foot`) with the real style-reference component set -- `mast`, `kicker`, `pericope`, `block` (+`.block.legend`, `.block.notes`), `v`/`n`, `r`/`rl`, `gloss`, `compare`, `en`. Left `echo` out on purpose (§4: ship it only if unit 1 actually wants it, with its nesting-depth check in the same commit). This had to happen now, not after Phase F alone, because the rewritten `test_unit_meta.py`'s fragments use the real component names (`h3.pericope`, `section.block.legend`, `section.block.notes`) instead of the old placeholder ones, and the component-whitelist check needs a stylesheet that actually defines them.
- Full suite re-run together after F/G: `test_hebrew.py` (10,120), `test_roots.py` (11), `test_unit_meta.py` (37), `verify_thread_coverage.py` (10), and `audit_thread_coverage.py` against the real empty data (0/0/0/0) -- all clean.

## 2026-09-15 (part 11) -- Phase 0.6 complete (H)
- **`CLAUDE.md`**: removed both ⚠ banners. Rewrote the Transliteration section (new alphabet/sheva/dagesh-forte/matres/furtive-patach/override rules), renamed and rewrote "Thread coverage" to "Root identity and thread coverage" (id-based design, `roots.py`, the rewritten audit/verify scripts, Ketiv/Qere handling), rewrote the Fragment metadata section (new `unit_meta.py` contract, all hardened checks, the §8 acceptance test), and updated the repo layout table (added `roots.py`/`test_roots.py`, dropped `thread-stems.json`, updated `css/styles.css`'s description).
- **`PLAN.md`**: Phase 0.6 marked ✅ DONE, all 8 §A decisions recorded inline. Condensed the old future-tense rework-item list (now stale) into a short "landed" summary pointing at `CLAUDE.md`/`improvements_log.md`. Updated the "Design decisions" section's root-registry description (no longer "shape superseded, see Phase 0.6" — states the actual id-set shape). Cleared the "Open questions for Lane" section (Phase 0.6's scope question is resolved).
- **`pipeline/threads_digest.py`**: prose rewritten to describe `data-w` tagging and `data/roots.json` id sets instead of `thread-stems.json`/consonant-skeleton `stems`/`exclude`. Regenerated `threads-digest.md` (still 0 threads, round-trip still clean).
- **`data/threads.json`**'s `_note` updated: a thread's coverage-audit prerequisite is now a `data/roots.json` entry, not a `pipeline/thread-stems.json` entry.
- Grepped `pipeline/`, `CLAUDE.md`, `PLAN.md`, `project-side/README.md`, and `data/` for leftover `thread-stems`/`strip_prefixes`/`_compile_stems`/`hebrew_hits`/skeleton-keyed-override references — the only survivors are explanatory ("this used to work this way, here's why it changed") or explicit "deleted" notes, not live dependencies.
- Asked Lane whether `data/roots.json` should join `project-side/README.md`'s sync index (the plan flagged this as a real decision, not a default). Answer: yes — added as a `repo → project` row.
- Full suite re-run one final time after all doc edits: `test_hebrew.py` (10,120), `test_roots.py` (11), `test_unit_meta.py` (37), `verify_thread_coverage.py` (10), `audit_thread_coverage.py` against real empty data (0/0/0/0), `roots.py` and `threads_digest.py` standalone — all clean. **Phase 0.6 is done**; Phase 1 (populate `units.json` from the Literary Unit Map) is next.

## 2026-09-15 (part 12) -- Phase 1 + cleanup pass
- **Phase 1**: transcribed `joshua_literary_unit_map.md`'s 24 units / 4 movements into `data/units.json` (`n`, `slug`, `passage`, `title`, `movement`, `built: false` on every row; `movements[]` array added with each movement's name/span/unit-list). Verified all 24 rows against the pipeline, not just by eye: `audit_thread_coverage.parse_range()` on every `passage` string produces the exact chapter:verse bounds the unit map states, including both off-grid breaks (unit 8's 8:30–9:2, unit 24's 24:29–33); `unit_meta.generate()` + `validate()` run clean for every unit number.
- That check caught a real bug: `unit_meta.generate()` never emitted `threads.retro`, so its own output failed `validate()`'s (correct, Phase F) requirement that all four threads sub-keys be present. Fixed `generate()` to include `"retro": []`, and added `test_generate_output_validates_clean()` to `test_unit_meta.py` (38 checks now) so this specific regression — a generator whose own output doesn't pass its own validator — can't come back silently.
- **Cleanup pass** (prompted: "always clean vestigial and useless things up as you go"): removed `pipeline/__pycache__` and added a `.gitignore` (none existed) so it doesn't recur. Removed `hebrew_words()`/`hebrew_morphemes()` from `hebrew.py` — dead since the Phase 0.6 audit rewrite stopped re-tokenizing raw Hebrew text and started working entirely off `Joshua-words.tsv` rows; confirmed via grep that nothing else called them. Checked `data/units.json`'s top-level `discourses` field before touching it — NOT vestigial, it's Matthew's real `manifest.discourses` (consumed by `app/main.js`'s `discourseOf()`, per `Port analysis.md` §6.2), distinct from the per-unit `discourse` flag that Phase F correctly rejects; left it alone, empty until Phase 4's app shell exists to populate it.
- Found a more serious gap this same pass: `audit_thread_coverage.py`'s `tagged_map`/`load_hebrew`/`hebrew_index`/`verse_text` were all defined but **never actually called** anywhere in the rewritten module — meaning the "local roots keep a per-verse informational view" claim in `CLAUDE.md` was false as shipped, not just an unused-code nit. Wired it in for real: new `local_root_verses()` builds `{root: [(ch,v),...]}` for every `data-root` in a fragment that isn't a tracked thread, folded into `coverage_for_fragment()`'s return (`"local"` key) and printed in `audit()`'s report. Also wired `verse_text()` into the GAP report (English context per gap, matching what the old stem-based version showed). Added `test_local_root_verse_view()` to `verify_thread_coverage.py` (11 checks now). Full suite re-verified clean after both fixes.

## 2026-09-15 (part 13) -- Phase 3: port the reusable pipeline
- Fixed three real bugs in `joshua_study_style_reference.md`'s §8 worked example, found by cross-checking its ids against `Joshua-words.tsv` while planning the port: `data-w="06Qzf"` appeared twice (once as "devoted," once as "given") but `06Qzf` is actually "unto" (אֶל) at 1:1, not either word -- fixed to `068w5` (the real ḥerem noun at 6:17) and `06Fu4` (the real natan verb at 6:2). Its retro entry also had `"verse": 13` when the word it names ("commander," שַׂר) only occurs at 5:14, and was missing the newly-required `w` field entirely -- fixed to `"verse": 14, "w": "06UrB"`.
- **Schema addition**: `threads.retro[]` entries now carry an optional `w` (OSHB word id), required by `unit_meta.validate()` when `op` is `add`/`retag`/`retag_word` and the target root is a tracked thread -- that op creates or repoints a `data-root` span, and a tracked-thread span needs `data-w` same as any other (checklist 7). Local-root retro fixes need none. `pipeline/test_unit_meta.py` grew 5 checks for this (43 total).
- **Ported `pipeline/apply_retrofit.py`** (genuinely language-neutral, Port analysis.md §1.3) with one real addition: `add`/`retag` accept an optional `w` and inject/update `data-w` on the span they produce; `retag_word` deliberately does not (a bulk reclassification changes root, not word-id, so any existing `data-w` on a matched span is left alone). 19 tests, including idempotency and the new data-w injection/update paths.
- **Ported `scan_occurrences.py`** unchanged (pure generic-markup logic). 4 tests.
- **Ported `verify_occurrences.py` narrower than Matthew's, not straight** -- kept the independent count-mismatch re-derivation (a separate line-oriented tokeniser, not scan_occurrences' regex) and the threads.json tagged-flag sanity check; dropped the colour-resolution and perceptual-distance collision checks entirely, since `unit_meta.check_data_root_resolves()` already does resolution more rigorously (as part of every `validate_fragment()` call) and collision-checking needs real hex colours that don't exist until Phase 4. 5 tests.
- **Ported `refresh_meta.py` and `build.py`** essentially unchanged; `build.py`'s step list gained a step Matthew never needed -- `pipeline/roots.py`, validating `data/roots.json` integrity between `verify_occurrences.py` and `threads_digest.py`.
- **Built `pipeline/port_artifact.py` deliberately slimmer than Matthew's**, not a straight port: dropped `extract_units.py`'s whole ~400-line cleanup pipeline (Greek-title parsing, script stripping, palette extraction, verse normalization) since Joshua's `source-artifacts/` already arrive in the style-reference fragment shape from unit 1 -- `to_fragment()` is a 20-line function (strip any existing meta block, prefix endnote ids) instead. Dropped `--backfill` (no legacy units). Dropped the WELL-palette/`assign_hues()`/colour-collision system per Lane's call -- local roots merge into `data/units.json` as `{translit, gloss}` only, colour deferred to Phase 4. Candidate preview (`_append_candidate_preview`) runs proposed `ids` through `audit_thread_coverage.source_hits_for_root()` instead of a Hebrew stem preview. Coverage reporting uses gap/wrong/stray/missing-data-w (Phase 0.6's shape) instead of gap/over. Fragment-level findings from `unit_meta.validate_fragment()` are reported in the thread-delta, not a hard gate -- only `validate()` on the meta dict blocks the write, matching Matthew's own "warn, still write" philosophy for its narrower set of structure checks.
- **`pipeline/test_port_artifact.py`**: a real end-to-end test, not mocked -- runs the actual `port_artifact.port_one()` against a scratch copy of `data/`/`units/`/`pipeline/out` (multiple modules' path globals monkeypatched and restored: `port_artifact`, `unit_meta`, `audit_thread_coverage`, `roots` -- `ROOT`/`Joshua-words.tsv` intentionally left real so word-id lookups stay genuine), using the style reference's own now-fixed §8 worked example as the incoming artifact. Covers dry-run (writes nothing), a real port (fragment written, units.json merged, fragment validates clean), the retro fix merging onto a scratch unit-05 fragment (with the real word id `06UrB`), local roots getting no colour, thread-delta report content (candidate preview, clean coverage, the merged retro line), and two hard-error paths (no meta block, invalid meta). 8/8 passing on the first real run against actual logic -- caught nothing to fix, which is itself informative given how much surface area the test covers.
- The subprocess-based `run_retrofit_and_scan()` step is stubbed out in the end-to-end test (a real subprocess re-imports those modules fresh and reads their own path globals from their own file location, not the test's monkeypatched scratch ones -- would silently read/write the real repo's files instead of the scratch tree). Not a gap: `apply_retrofit`/`scan_occurrences`/`verify_occurrences` already have their own direct-logic tests.
- Cleanup along the way: removed an unused `import re` from `verify_occurrences.py`, removed `pipeline/__pycache__` again.
- Full suite re-run clean end to end: `test_hebrew.py` (10,120), `test_roots.py` (11), `test_unit_meta.py` (43), `test_apply_retrofit.py` (19), `test_scan_occurrences.py` (4), `test_verify_occurrences.py` (5), `test_port_artifact.py` (8), `verify_thread_coverage.py` (11), `audit_thread_coverage.py` clean, `build.py` runs end to end. **Phase 3 is done.** Phase 4 (the app shell) is next.

## 2026-09-15 (part 14) -- Wrote phase-4-5-plan.md
- Read the real `Projects/Matthew/app/*.js` + `index.html` (not just `Port analysis.md`'s earlier assessment) to measure what actually ports vs. needs rework for Phase 4. Found `Port analysis.md` §1.11's "essentially wholesale portable" claim is true for `index.html`/`search.js`/`threads.js` but not the whole shell: `spotlight.js` handles two component kinds (`.compare`, `aside.synoptic`) Joshua's style reference doesn't have (no compare box; `aside.echo` undecided) and needs real trimming, not adaptation; `main.js` has a genuine ~1/3-of-file rework around Matthew's "discourse" overlay (`discourseOf()`, book-map brackets, masthead placement text) which has no confirmed Joshua equivalent, plus a field-name mismatch already baked in (`units.json`'s `movements[]` is `{n,name,span,units}` from this project's own Phase 1 work; Matthew's `main.js` expects `{id,label}`).
- Found the real blocker for Phase 4's visual result: colour assignment was deliberately deferred in Phase 3 (Lane's own call), but `threads.js`'s `injectPalette()`/`rebuildLegend()` both key off a `color` field that doesn't exist anywhere in Joshua's data yet -- the JS ports fine, the site would just render colourless. Framed as an open question (three options, no recommendation -- genuine design-taste call) rather than deciding it here.
- Wrote `phase-4-5-plan.md`: self-contained plan for a fresh session, same pattern as `phase-0.6-plan.md` -- read-first list, ground rules, measured current state, §A decisions to get from Lane first (discourse-equivalent or not, colour timing, book-map visual scope, search hint text), a per-file port-vs-rework table with line counts and specific function names, and Phase 5 (Unit 1) folded in since Phase 4's shell needs real content to prove itself against. Linked from `PLAN.md`'s Phase 4/5 entries and its Open Questions section.

## 2026-09-15 (part 15) -- Phase 4: the app shell
- Got the §A decisions batched in `phase-4-5-plan.md` from Lane: no discourse-equivalent overlay (movements only), assign root/thread colours now rather than deferring to Phase 5, a rich Matthew-style book map (not a plain chip list). Mid-session, Lane also asked for the visual theme to be distinguishable from Matthew's -- "old testament theme joshua theme, similar but unique" -- not a straight recolour of the same design.
- Ported `index.html`, `app/threads.js` (unchanged -- entirely data-driven, no Matthew-specific logic), `app/search.js` (near-unchanged -- `fold()`'s NFD diacritic-stripping already works for `ḥerem`/`naḥalah`; only the storage key and hint text/examples changed), `app/spotlight.js` (trimmed to the `.gloss`-only path -- Matthew's `.compare`/`aside.synoptic` handling deleted, not disabled, since Joshua has neither component).
- Reworked `app/main.js`: removed `discourseOf()` and both discourse-drawing code paths entirely (not adapted). Reconciled the field-name mismatch flagged in the plan by reading `movements[]` as `data/units.json`'s own `{n, name, span, units}` shape rather than changing the data to match Matthew's `{id, label}`. Dropped `normalizeSectionHeadings()` outright (not simplified) -- it exists in Matthew to clean up legacy pre-contract heading markup from artifacts migrated before the style reference existed, and Joshua's artifacts arrive in the `h3.pericope` shape from unit 1, so there's nothing for it to normalize.
- **Caught a real behavioral bug while porting, not just adapting cosmetically**: Matthew's `hoistStructureBlocks()` skips only `section.block.legend` when moving structural blocks to the top of a unit -- safe there because Matthew's endnotes are a bare `.notes` section, not `.block`. Joshua's endnotes are `<section class="block notes">` (style reference §4, carrying `block` too), so an unchanged port would have hoisted every unit's endnotes above its translation on every single build. Fixed by also skipping `.notes` in the hoist loop, with a comment explaining why (so it doesn't get "simplified" back to Matthew's version later).
- `css/styles.css`: the real design pass, not a recolour of Matthew's. Sun-bleached wilderness ground, clay/terracotta for verse numbers and endnote markers, bronze for pericope headings and active chrome, a new Jordan-valley teal-indigo for movement-placement text (no Matthew equivalent slot). Display type Cinzel (carved-inscription capitals) in place of Cormorant Garamond; body serif Frank Ruhl Libre in place of EB Garamond. Component vocabulary kept to exactly the style reference's §4 list -- `.compare` removed from the whitelist (Phase 2 already resolved no compare box) rather than left in unused, and Matthew-only content components with no Joshua analogue (`.structure`/`.frame`/`.triads`/`.mirror`/`.gem` genealogy box, `.prayer`, `.itin`, `table.exod`) were never ported at all.
- `pipeline/port_artifact.py` gained Matthew's hue-assignment system (`WELL`, `assign_hues()`, `_lab`/`_de` CIE-Lab perceptual-distance collision avoidance), ported near-verbatim except for `WELL` itself: a new ~20-hue desert/Jordan-valley palette sharing no hex values with Matthew's crimson-and-gold-leaning one. `merge_units_json()` now assigns a genuinely local (non-tracked) root a real colour on port, avoiding collisions with the unit's own existing local hues and with the colour of every tracked thread the unit also uses -- colour timing was the one thing Phase 3 deliberately deferred, now resolved.
- Updated `pipeline/test_port_artifact.py`: renamed the old "local roots have no colour" test to reflect what it actually demonstrates now (tracked roots produce no local-roots entry at all, since their colour lives in `threads.json`) and added `test_real_port_local_root_gets_a_colour`, a new fixture with one genuinely local root ("shout"), asserting it gets a colour from `port_artifact.WELL` plus its translit/gloss. 9 checks now (was 8).
- Smoke-tested in a real browser (local `python -m http.server` via a new `.claude/launch.json`) against the still-empty `data/*.json`: nav renders 24 unit chips correctly grouped under 4 movements marked "not yet built," the book map renders with roman-numeral movement groups (I-IV) and no discourse brackets, search renders with the updated hint text and no results, no console errors, works cleanly at 375px mobile width.
- Full suite re-verified clean before and after: `test_hebrew.py` (10,120), `test_roots.py` (11), `test_unit_meta.py` (43), `test_apply_retrofit.py` (19), `test_scan_occurrences.py` (4), `test_verify_occurrences.py` (5), `test_port_artifact.py` (9), `build.py` end to end. This phase didn't need to touch pipeline *logic*, only `port_artifact.py`'s colour assignment, matching the plan's own "worth a pause to ask why" bar for pipeline changes. Updated `CLAUDE.md` (new "The app shell" section) and `PLAN.md` (Phase 4 marked done, Open Questions section cleared). **Phase 4 is done.** Phase 5 (Unit 1) is next, blocked on Lane producing the research artifact via the Claude.ai project workflow.

## 2026-09-17 -- repo move
- Moved repo root from `Projects\Joshua` to `Projects\Bible\Joshua` (Matthew moved to `Projects\Bible\Matthew` too, same session). Updated the hardcoded absolute `SRC`/`OUT` paths in `pipeline/build_reading.py` and `pipeline/build_english.py` to match. Git remote (`github.com/lanehaden157/joshua`) and `pipeline/sync_to_github.py` are unaffected since they're not path-dependent.

## 2026-09-17 — doc trim
- `joshua_study_style_reference.md` trimmed 4,120 → ~2,140 words: every rule and all 16 checklist items kept, section numbers and §8 worked example unchanged (tests extract it), `(learned)` stories cut to one clause + commit hash, `.compare` references dropped (no compare box), §9 TODO replaced with pointer to the unit map. Added a "Translation philosophy" paragraph to §5.
- `Claude_ai_chat_side_instructions.md` trimmed 1,014 → ~460 words: pass 3's duplicated artifact rules (voice, local-root tagging, translation philosophy) replaced with a pointer to the style reference; three-pass flow, standing moves, scope, and working style kept.
- `CLAUDE.md` trimmed 5,230 → ~1,590 words: restatements of the style reference (key table, checklist, transliteration rules) replaced with pointers; kept pins, BHS counts, the retrofit recipe, port/app-shell deviations from Matthew, and known gotchas. Fixed stale state (unit 1 built, 10 threads/roots, source-artifacts exists) and flagged resources.md as missing. Full suite + build.py clean.
- `PLAN.md`: Phase 5 (unit 1) marked done with a short record of what it changed; Phase 6 = units 2–24; `resources.md` listed as the one open question. `CLAUDE.md` retrofit recipe step 4 corrected to match `b5bcee5` (unwrap the extra span rather than demote to `rl`).

## 2026-09-19 -- platform review G1 (Joshua correctness pass)

Worked the G1 group from `platform-design-review.md`. Every item verified by
running code, not by reading prose.

- **A2 `opens.note` now has a home.** Added `note` to `threads.json`'s `opens`
  object, seeded on all 10 threads from each thread's prose `note` (every
  thread opens in unit 1, so those notes already *were* the unit-1 opening
  beats). `port_artifact.thread_delta()` now emits a paste-ready
  `` `id`.opens: {...} `` entry the way it already did for payoffs, instead of
  printing the note with nowhere to put it.
- **A1 fixed.** `_threads_touching()` built `{id, ref}` while `validate()`
  required `note` on both opens and payoffs, so *every* `build.py` run wrote
  `units/unit-01.html` into a shape the project's own validator rejected --
  10 errors, silently, on every build. Now carries `note` through for both.
  Payoffs had the identical bug; unit 1 just has no payoffs yet to expose it.
- **A3 decided: `roots[]` is local roots only.** Confirmed from
  `app/threads.js` `resolveUnit()`, which unions `roots[]` with the occurrence
  counts and prefers the *thread's* colour/translit/gloss whenever
  `threads.byRoot` has the root -- so a tracked thread renders correctly
  without appearing in `roots[]` at all. Re-declaring one there would only
  duplicate `threads.json` per-unit and go stale. Style reference §1 amended;
  the code already behaved this way.
- **A4 fixed, and it was worse than the review thought.** `assign_hues()`
  seeded `taken` from `meta.roots`, which under the A3 decision contains *no*
  tracked threads -- so collision avoidance was blind to every tracked colour
  in the unit. Now seeded from the fragment's actual `data-root` spans
  (`roots_in_fragment()`). Separately, the `pick is None` fallback was
  `WELL[len(used) % len(WELL)]`, which ignored collisions outright and handed
  out *exact duplicates* of tracked-thread colours; it now picks the colour
  furthest from what is taken.
- **Density finding (review H11, arriving at unit 1).** Unit 1 tags 16
  distinct roots; the 20-colour `WELL` yields only 13 mutually distinct at
  dE>=12. The palette cannot separate this unit at the current threshold.
  Best achievable is dE 11.0-11.5 on three pairs. Left for Lane -- widening
  the well, lowering the threshold, and tagging less are all live.
- **A20: `pipeline/validate_units.py`, a new hard build step.** Re-validates
  every fragment on disk (meta + `validate_fragment`) rather than only the
  incoming artifact at port time. Contract breaches fail the build; colour
  distance warns, since that is a tunable aesthetic judgement rather than a
  contract violation. Wired into `build.py` `STEPS` after `refresh_meta.py`.
- **Closed the test gap that hid A1.** `test_generate_output_validates_clean`
  passed only because its fixture used `{"threads": []}` -- zero entries, so
  zero notes to get wrong. Added
  `test_generate_round_trips_opens_and_payoffs_notes` with threads that
  actually touch the unit, covering both opens and payoffs. Mutation-checked:
  reverting the fix fails it. Suite 37 -> 44 checks.
- **A17.** Reports called bare `transliterate()`, which is deterministic-only,
  so lemma-keyed `OVERRIDES` never fired and kol rendered `kal`. Added
  `audit_thread_coverage._translit_row()` (uses the row's lemma + morph);
  the `--ids` report and the porter's candidate preview both go through it.
- **A18.** Promotion authority said three different things. Aligned
  `threads_digest.py` (and so `threads-digest.md`), `unit_meta.py`'s docstring
  and style reference §3 to the 2026-09-16 decision: Claude decides, biased
  book-wide, ask Lane only when genuinely unsure.
- **A9.** `units.json` `_note` no longer claims "No units built yet";
  `CLAUDE.md` no longer calls `app/threads.js` unchanged from Matthew (it has
  the `example` field); style reference §5's open-questions line now reflects
  naḥalah and y'all being locked 2026-09-16, with four still open.
- **A22.** Committed the repo-move path residue and moved a misplaced
  `improvements_log.md` heading that had orphaned a hebrew.py bug-fix bullet.

Full suite green (44 checks in `test_unit_meta.py`), `build.py` green, thread
coverage 0 gap / 0 wrong / 0 stray / 0 missing-data-w. Verified in the browser:
16 roots, 69 tagged spans, 16 legend swatches, all distinct, no console errors.

## 2026-09-19 (part 2) -- platform review G2 (data-w assigner + contract reconciliation)

- **A5: `pipeline/assign_data_w.py`.** Turns CLAUDE.md's seven-step retrofit
  recipe into one command. Per verse, per tracked root: zip the id-set's
  source hits (in `Joshua-words.tsv` order) against that verse's
  `<span class="r" data-root=...>` spans in document order. Counts agree ->
  assign. Counts disagree -> assign *nothing* in that verse and say why. A
  wrong `data-w` is worse than a missing one: missing is a hard error the
  audit already catches, wrong silently points a reader's popover at the
  wrong Hebrew word. Never overwrites an existing `data-w`; a conflicting
  one is reported, not replaced.
- **Validated against the real hand-tagged unit.** Stripping every `data-w`
  from `units/unit-01.html` and re-running the assigner reproduces the file
  **byte-identically** -- all 38 tracked spans, zero mismatches.
- **Validated against the untagged source artifact** (which has 0 `data-w`):
  37 of 38 assigned automatically, and the single verse it refused to guess
  is `rest 1:15` -- exactly the documented ambiguity where one Hebrew word
  (*yaniaḥ*) is rendered as two English words, the subject of `b5bcee5` and
  a named example in CLAUDE.md's recipe step 4. The tool independently
  rediscovered the one verse that genuinely needed a human. Per-unit cost
  goes from 38 hand-placements to 1 decision.
- `pipeline/test_assign_data_w.py`: the round-trip against real data, plus
  the refusal cases (count mismatch, conflicting existing `data-w`,
  idempotence on a tagged file, chapter defaulting and rollover).
- **A6: contract reconciled.** The chat side was told "mark roots with
  data-root only; don't hand-chase data-w ids" while the contract required
  `w` in two places -- unsatisfiable from that end. `w` is now explicitly
  optional in the incoming artifact and filled by the porter; the guarantee
  moves to the built fragment, where `check_tracked_spans_have_data_w()`
  already enforced it. Updated style reference §7 items 6 and 8,
  `Claude_ai_chat_side_instructions.md` pass 3, and `unit_meta.validate()`
  (a malformed `w` is still an error; a missing one is not). Two tests that
  encoded the old rule were rewritten to the new one rather than deleted.
- `port_artifact.py` runs the assigner right after `to_fragment()`, printing
  what it assigned and what needs eyes.

Full suite green (8 files), `build.py` green, `units/unit-01.html` unchanged.

## 2026-09-19 (part 3) -- platform review G3 (the wording decisions)

Decisions that are cheap now and a retroactive pass at unit 10 (Matthew's
lesson) later.

- **C10 -- ʿeved renders "slave"** (Lane). Applied to unit 1, all 5
  occurrences (1:1, 1:2, 1:7, 1:13, 1:15), via a `text` op in
  `retrofit-tags.json` matching `>servant</span>` rather than bare
  "servant" -- the bare form would also have rewritten `data-root="servant"`
  and the meta block's thread id. The thread *slug* stays `servant`: it is an
  internal identifier, never shown to a reader, and renaming it would mean
  retagging every span (review H7). Thread gloss updated to match. The 5
  existing `retag` entries carrying the data-w injection had to be retargeted
  from "servant" to "slave" or they would have silently MISSed on any future
  re-port -- caught because apply_retrofit reported it.
- **C12 -- shamayim renders "sky / skies"** everywhere (Lane), matching
  Matthew's ouranos rule. Decided before unit 2 because Rahab's 2:11 is the
  first hit. **Correction to the review:** C12 lists the occurrences as
  2:11, 8:20, 10:11, 11:4 -- 11:4 does not contain shamayim; the fourth is
  **10:13**. The four split by sense (2:11 and 8:20 cosmological, 10:11 and
  10:13 physical; WEB itself renders the first pair "heaven" and the second
  "sky"), and rendering them alike is the deliberate choice.
- **A21 -- WEB is provenance only** (Lane). Not the base text, not a draft
  the chat side edits, not a diff target. Generated and pinned for
  reproducibility; nothing in the workflow reads it; its absence from
  `project-side/synced/` is deliberate, not a gap. Written down in
  `CLAUDE.md` beside the file, with the note that it is also *not* where the
  Hebrew comes from (that is morphhb) -- the belief that prompted the item.
- **A13 -- declined-candidate ledger.** `data/roots.json` gains `declined`
  (slug -> {why, date, unit?, ids?}), seeded with `all`/kol and the actual
  2026-09-16 reasoning, which until now lived only in a session log.
  `roots.py` validates it (`why` and `date` required -- a bare "no" gets
  re-litigated -- and a slug may not be both declined and tracked).
  `threads_digest.py` renders a "Considered and kept local" section, so the
  chat side reads it. `port_artifact.py` flags a re-proposal against the
  original reasoning and asks what changed. Verified end to end by feeding
  the porter an artifact that re-proposes `all`: the flag fires.
- **D15/F20 (canon conventions file) deliberately NOT done.** Joshua and
  Matthew are sibling repos with no shared parent, so a "shared" file today
  means duplicating it or inventing a third location nothing reads. The
  decisions are what is expensive to defer, and they are recorded; the file
  waits for G6, when D1/D2 give it a real home.

Full suite green, `build.py` green, coverage 0/0/0/0. Browser-verified: all 5
prose spans read "slave", the legend reads "ʿeved — slave (Moses' title,
'slave of Yahweh') 5×", no "servant" remains in the rendered text, no console
errors. `units/unit-01.html` diff is exactly 5 lines, `data-root`/`data-w`
untouched.

## 2026-09-19 (part 4) -- A7: OSHB letter suffixes are not opaque

Ran the lexicon check the review flagged as not done (`AugIndex.xml` +
`LexicalIndex.xml`), and the "opaque" rule in style reference §2 turned out
to be wrong. The letters separate genuinely distinct lexemes:

| id | split | in Joshua |
|---|---|---|
| 3885 | a *lodge* / b *murmur* | 4x lodge (3:1, 4:3, 6:11, 8:9) vs 1x murmur (9:18) |
| 2416 | a *alive* / e *life* | "living God" (3:10, 8:23) vs "days of your life" (1:5, 4:14) |
| 6924 | a *front* / b *eastward* | 7:2 vs the boundary formula (15:5, 18:20, 19:12, 19:13) |

Elsewhere the letters are inflectional, not lexical (834a-d are all *ʾăšer*
with different prefixes; 859a-e all *ʾattâ* by person/number), so a bare id
covers them correctly.

Two counting corrections to the review's A7: it says 12 bare ids carry more
than one suffix, which is right *only* if you separate letter suffixes from
the `+` marker. `bare_id()` strips both; the other 67 collisions are all `+`
(Beth-el as `1008` vs `1008+`), the same lexeme with a compound-name flag,
correctly stripped.

**Change:** matching now honours what is written. A bare id (`"2416"`) claims
every lexeme under the number; a suffixed id (`"2416e"`) claims exactly one.

- `roots.py` gains `lemma_key()` (keeps the letter, strips `+`) and
  `split_ids()`. `_ID_RE` now captures the marker.
- `source_hits_for_root(words, ids)` takes the root's **raw id list** instead
  of a pre-stripped bare set, and matches bare-vs-exact itself. All six call
  sites simplified accordingly.
- The "no id in two roots" check understands the asymmetry: `3885a` and
  `3885b` may sit in different roots, but a bare `3885` collides with either.
- A suffixed id the corpus never carries is now a hard error -- under the new
  semantics it would match *nothing*, and a silent zero is worse than a loud
  failure. This reverses `test_lettered_id_normalizes`'s old assumption, which
  was safe only while the letter was being stripped; that test was rewritten
  rather than deleted, and two new ones cover the lodge/murmur split.

**No existing root's coverage moved** -- all ten still report 89, 81, 32, 59,
6, 8, 5, 9, 27, 23 occurrences, identical to before. The change is purely
additive: precision is opt-in.

Style reference §2 rewritten with the three real cases; `CLAUDE.md` updated,
including pointing the retrofit recipe at `assign_data_w.py` instead of the
by-hand steps 1-3.

## 2026-09-21 -- G4 prep: the wording decisions and aside.echo, before unit 2

### ḥesed and nefesh (translation-choices.md)

- **ḥesed** locked to left-untranslated ("ḥesed") with a gloss. Two
  occurrences, both Rahab (2:12), a reciprocal covenant-loyalty exchange
  paired with "a sign of truth" -- not the word's usual divine-to-human
  register, which made every single-word English option (steadfast love /
  kindness / loyalty) lose something specific. Same pattern already in use
  for `torah`.
- **nefesh** locked to a two-rule split, not left open-ended. Pulled all 16
  occurrences and their morphology first: **Rule A** (self/address, 6
  occurrences: 2:13, 2:14, 9:24, 22:5, 23:11, 23:14) follows Matthew's
  psychē mechanism exactly -- Hebrew singular -> "life", Hebrew plural ->
  "being(s)", never "soul". **Rule B** (10 occurrences: the ḥerem
  battle-report formula 10:28-11:11, and the cities-of-refuge law 20:3/20:9)
  is a documented exception: "person". Both are Hebrew-grammatical-singular
  uses, generic/distributive ("every person," "a person"), and Matthew's
  psychē has no occurrence in that register to borrow from -- "he struck
  the life/being with the sword" is not idiomatic English and miscounts
  what's being described. Neither decision is applied to prose yet; unit 1
  contains neither word (both start at 2:12/2:13).

### aside.echo built (style reference §4, review A15)

Was spec'd but genuinely unbuilt: not in the CSS class whitelist, no
validator, no nesting-depth check, `app/spotlight.js`'s own header comment
flagged it as a known gap. Built before unit 2 (Lane's call):

- `css/styles.css` -- `.unit aside.echo` and its `.verse-note` variant,
  modelled on `.gloss`'s box shape but Jordan-teal left border + a
  CSS-generated "cf. " prefix, so the two are visually distinct once open.
- `pipeline/unit_meta.py` `check_echo()` -- new, wired into
  `validate_fragment()`. Three things: `data-anchor="C:V"` present and
  well-formed; the anchor matches the verse the echo actually follows in the
  fragment (drift between position and anchor would be invisible to a
  reader and to a diff); and the nesting-depth check the style reference
  calls for -- no `<aside class="echo">` starts inside an unclosed `.gloss`
  span, which is the literal `67b2712` bug, not a hypothetical one. Modelled
  the check the way a naive renderer actually behaves (nearest `</span>`
  closes a gloss, whether or not it was meant to) rather than assuming
  well-formed input, since that mismatch *is* the failure mode.
- `app/spotlight.js` -- extended to mount `.echo` alongside `.gloss` under
  the same per-verse toggle (one "is there more here" control, not two).
- 8 new tests in `test_unit_meta.py` (44 -> 52): a clean pass, missing
  anchor, malformed anchor, anchor/verse mismatch, the 67b2712 nesting
  case, bare-verse-number chapter rollover, unclosed `<aside>`, and that
  `echo` is a real CSS class (so `check_component_whitelist` doesn't reject
  a fragment that uses it). Mutation-tested the nesting check by disabling
  it: the regression test fails, confirming it isn't a coincidence.
- Verified live: injected a real echo into a scratch copy of unit-01.html
  (never committed), confirmed it validates clean through the actual
  pipeline, rendered it in the browser, clicked the toggle open, screenshot
  confirmed the teal "cf." styling and correct box mounting alongside the
  existing gloss. Reverted the test content -- `unit-01.html`'s committed
  diff is zero.
- Style reference §4 and checklist item 11 updated to describe the built
  component instead of the unbuilt spec; `CLAUDE.md`'s app-shell section and
  its now-stale "`app/spotlight.js` has only `.gloss`" line updated too.

Full suite green (`test_unit_meta.py` 52 checks), `build.py` green, coverage
0/0/0/0, `units/unit-01.html` unchanged.


## 2026-09-21 — C7 resolved (platform-design-review.md)
- Matthew's `<div class="notes">` won the cross-project decision (zero retrofit there vs.
  this repo's single unit). `units/unit-01.html`: `<section class="block notes">` ->
  `<div class="notes">`. `css/styles.css`: replaced the `.block.notes` rules (which
  borrowed their frame from the generic `.block` panel style) with a plain top-divider
  `.notes` rule, matching Matthew's shape. `pipeline/build.py` green after.

## 2026-09-21 (part 2) — Unit 2 ported
- Ported `source-artifacts/joshua_02_translation.html` -> `units/unit-02.html` via
  `pipeline/port_artifact.py 2`. `assign_data_w.py` placed all 9 spans by alignment,
  no human intervention needed.
- Thread promotions (Claude's call, biased book-wide per CLAUDE.md policy):
  promoted `devote` (haram, 2763a), `swear` (shavaʿ̲/shevuʿ̲ah, 7650+7621),
  `blood` (dam, 1818), `melt` (masas, 4549) to tracked threads in
  `data/roots.json` + `data/threads.json`. Declined widening `cross`'s id set to
  cover maʿ̲berot "fords" (4569b, distinct lemma, single occurrence) -- logged
  in `roots.json`'s `declined` ledger instead.
- `swear`'s first occurrence is actually 1:6 (Yahweh's oath to the fathers),
  untagged when unit 1 was built -- retro'd via a new `add` op in
  `pipeline/retrofit-tags.json` (word `06LJh`, text "swore"), applied by
  re-running `port_artifact.py 1`.
- Accepted 5 of the porter's proposed payoffs onto existing threads: `send`
  (2:1), `give` (2:9, 2:24), `cross` (2:10, 2:23) -- none closed the thread.
- `audit_thread_coverage.py`: 0 gap/wrong/stray/missing-data-w across all 14
  tracked threads. `verify_thread_coverage.py`: 11/11. Full `build.py` clean.
- Fixed a stale hardcoded count in `test_assign_data_w.py` (asserted exactly
  38 tracked spans in unit 1; now 39 after the swear retro) -- now derives
  the expected count from the file instead of hardcoding it.
- Smoke-tested unit 2 live (static server, `#/unit-02`): threads panel,
  local-root list, and all 24 verses render clean; no console errors.

## 2026-09-21 (part 3) — Unit 2 wording review
- `translation-choices.md`: ḥerem locked (Lane, ahead of unit 5) to
  "devote(d) to destruction" -- kept as an English phrase, not
  transliterated like ḥesed/torah, since the verb form dominates the early
  occurrences and a transliterated verb reads far worse than a
  transliterated noun. Yam Suf (2:10) locked to "Reed Sea" over the
  traditional "Red Sea". Both already matched what `unit-02.html` actually
  rendered -- no fragment changes needed, glossary only.
- Fixed a real glossary bug: the ḥesed row said "two occurrences, both at
  2:12" -- `Joshua-words.tsv` has three (lemma 2617a: 2:12 ×2, 2:14 ×1).
  `unit-02.html`'s tagging was already correct (3 spans); only the
  glossary row was wrong.
- Checked unit 2's plural-possessive usage ("y'all's God", "y'all's way")
  against unit 1's convention -- already consistent, no fix needed.

## 2026-09-21 (part 4) — questions[] artifact field
- Lane's ask: wording/data questions the chat side has for him were getting
  asked (and answered) on the project side after the artifact was already
  handed off -- he wants them surfaced here instead, with choices, at port
  time. New artifact-contract field: `questions[]` (`{topic, note,
  options?}`), style reference §3a.
- `pipeline/unit_meta.py`: added `questions` to `ALLOWED_TOP_LEVEL_KEYS`,
  validated (topic/note required strings, options optional string list).
  Deliberately NOT round-tripped by `generate()` -- consumed and dropped
  exactly like `threads.candidates`/`threads.retro`, so a regenerated
  fragment never carries stale questions.
- `pipeline/port_artifact.py`: new `print_questions()` prints every
  question straight to stdout right after meta validation (both `--dry`
  and real-write paths) -- the copy meant to actually get read, in the
  terminal, not buried in a report file. `thread_delta()` also gets an
  "## Open questions for Lane" section for the written record.
- `Claude_ai_chat_side_instructions.md`: fifth standing move added --
  wording/data calls go in `questions[]`, not asked in chat; pass-3
  artifact-skeleton description updated to match.
- 5 new `test_unit_meta.py` checks (schema validation + generate() never
  re-adding the key) + 2 new `test_port_artifact.py` checks (thread-delta
  section, stdout printing). Full suite + `build.py` still clean.
