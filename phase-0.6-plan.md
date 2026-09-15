# Phase 0.6: Line the pipeline up with the style reference

Paste this into a fresh session. It stands on its own.

## Read first, in this order

1. `joshua_study_style_reference.md`. This is the artifact contract, and it wins every disagreement. The sections that matter here: §2 (root identity), §3 (the hard contract), §4 (components), §5 (Hebrew in English), §7 (checklist), §8 (worked example).
2. `CLAUDE.md`. It says how the repo behaves today. It has ⚠ banners on the sections this phase replaces.
3. `PLAN.md`, Phase 0.6.
4. `Projects/Hebrew/pipeline/transliterate.py`, the module docstring, plus `verify_transliterate.py`. This is the "parser project" the style reference cites. It already has vocal/silent sheva rules, holam-vav/shuruq/hiriq-yod matres, and furtive patach. **Port its rules, not its alphabet.** It uses ASCII and models b/k/p spirantization, and Joshua must not do either.
5. The session-context files: `session_index.md`, `improvements_log.md`, `session_summary_2026-09-14.md`.

## Ground rules

- **Never hand-type Hebrew. Pull by word id from `Joshua-words.tsv`** (style reference §2). This applies to test fixtures and expected values too.
- `pipeline/test_hebrew.py` is the scheme's authoritative definition. This time, work each expected value out by hand from the word's actual codepoints and the documented rules, the way `Projects/Hebrew/pipeline/verify_transliterate.py` does. Don't copy the generator's output and "review" it; that was the weaker discipline used last time.
- `data/threads.json` and `data/roots.json` are Lane's policy files. Nothing in the pipeline writes their content, so keep them empty.
- Ask Lane before guessing on design or scope. Batch the §A questions at the start.
- Update `improvements_log.md` and `session_index.md` as you go. Write a `session_summary_<date>.md` at the end.

## Current state, measured 2026-09-14 (don't re-derive; spot-check if in doubt)

What `hebrew.py` produces today, by real word id:

| word id | ref | today | the style reference wants | cause |
|---|---|---|---|---|
| 06b5Q | 2:3 | `melekhe` | `melek` | spirantized kaf, and word-final sheva spoken |
| 062oS | 9:1 | `ha-melakhiym` | `hammelakim` (maybe hyphenated, see §A2) | no dagesh-forte doubling, spirantized kaf, hiriq-yod read as `iy` |
| 06K9n | 6:15 | `ka-mišepaṭ` | `mishpaṭ` stem | sheva always spoken as "e", shin comes out `š` instead of `sh` |
| 06aPd | 1:1 | `yehošuʿ̲a` | `yehoshuaʿ` | no furtive patach, shin as `š` |
| 06LeN | 1:3 | `netatiy-w` | hiriq-yod should read `i` | yod after hiriq is read as a consonant |
| 06k5P | 1:1 | `Yahweh` | `YHWH` | override output. "Yahweh" belongs in `translation-choices.md`, not in the transliteration |

- Vowels already come out **without** length marks (a e i o u). `PLAN.md` and `CLAUDE.md` briefly said otherwise; that has been corrected.
- Lemma fields carry trailing letters `a` (×1400), `b` (×331), `d` (×71), `c` (×27), `e` (×2). Keep them in the data and strip them at query time (§2). There are 1,223 distinct lemma ids.
- Lemma segments **don't** line up 1:1 with surface morphemes. Pronoun suffixes have a morph segment (`Sp3fs`) but no lemma segment. Example: 06XSi `בֵיתָ/הּ` has lemma `1004 b` and morph `HNcmsc/Sp3fs`.
- There are 32 Ketiv/Qere pairs. Both rows carry ids, and `Joshua-reading.txt` shows the Qere.

## A. Decisions to get from Lane first (ask all at once)

1. **Tsadi**: `ts` or `ṣ`? §5's rule is "a diacritic only where the plain letter is already claimed," and that doesn't settle it. (Shin = `sh` and sin = `ś` are settled by §5's own examples.)
2. **Morpheme boundaries**: keep the hyphen (`ha-melek`, `u-`) or join (`hammelek`)? §5 writes `hammelek` but also `u-`.
3. **Aleph/ayin distinction.** Today a combining underline is baked into ayin. §5 says to distinguish them "in a legend or gloss" by something other than the mark alone. Keep the underline, or leave transliteration as plain ʾ/ʿ and handle the distinction in legend markup?
4. **Ketiv/Qere**: which word id does an artifact tag, and which does the audit count? Recommendation: the Qere id, since it matches the reading text.
5. **One id in two roots**: hard fail, or allowed with a note?
6. **Local (non-thread) roots**: does `roots.json` hold them too, or only tracked threads? §2 says "a root is a hand-curated set of Strong's ids in roots.json", but local-root spans need no `data-w`.
7. **Override API.** Recommendation: a word-level call with the lemma id (`transliterate_word(surface, lemma)`), plus a verse-level call (`transliterate_ref("Josh 1:1")`) that pulls words and lemmas from the TSV. The bare-text `transliterate(text)` stays as a fallback with no overrides.
8. **`pipeline/thread-stems.json`**: delete it (recommended) or archive it?

## B. `pipeline/hebrew.py`: fix the scheme (independent of C–F)

1. **Alphabet**: ʾ b g d h w z ḥ ṭ y k l m n s ʿ p (tsadi per A1) q r sh ś t.
   - No spirantization: bet, kaf, and pe always come out b, k, p. Drop the kh/v/f branches.
   - Het is `ḥ`. No kaf form collides with it anymore.
2. **Sheva**:
   - Port the parser project's rules: word-final sheva is silent; word-initial sheva is spoken; of two in a row, the first is silent and the second spoken; otherwise silent after a short vowel.
   - Add what that project skipped: sheva under a doubled consonant is spoken (§5: `hammelakim`, not `hamlakim`).
   - A spoken sheva comes out `e`.
3. **Dagesh forte doubles the consonant.** Tell forte apart from lene:
   - In a non-begadkefat letter, a dagesh is forte. The exceptions are shuruq in vav and mappiq in a final he.
   - In a begadkefat letter, a dagesh right after a vowel is forte. At the start of a word or morpheme, or after a silent sheva, it's lene.
   - The article's gemination doubles into the next morpheme (`hammelek`).
4. **Matres lectionis**:
   - Keep the holam-vav fix (a real bug fixed earlier; about 12% of words hit it).
   - Keep shuruq.
   - Add hiriq-yod → `i` and tsere-yod → `e`.
   - Final he after a vowel stays `h` (`torah`). A mappiq he is `h`.
5. **Furtive patach** on a word-final ḥet, ʿayin, or mappiq he: the vowel comes out before the consonant (`yehoshuaʿ`).
6. **Overrides keyed on lemma id**, not on the consonant skeleton (§5):
   - Seed 3068/3069 → `YHWH`, 3389 → Yerushalayim (confirm the spelling against A1 and A2), 3605 → `kol`.
   - Build the API from A7. Line lemma segments up with surface morphemes by walking the morph segments and skipping `S…` suffix segments.
   - **Check that alignment over all 10,083 rows before relying on it**, and report every mismatch.
7. **Keep**:
   - `unicodedata.combining()` for spotting marks.
   - Phrase handling that keeps spaces.
   - Word-initial shuruq `u` (hyphen per A2).
   - `hebrew_words()` / `hebrew_morphemes()`, if anything still uses them.
8. **Tests: rebuild `pipeline/test_hebrew.py`** with hand-derived expected values, pulled by id.
   - Cover every row of the table above, plus 06XR4 (kol), 06YgF and 06sZv (Jerusalem, bare and prefixed), 06KZG (qum), 068w5 (ḥerem), 06cpb (shuruq plus sin).
   - Add a Ketiv/Qere pair: 06x72 and 06FYV.
   - Keep a full-verse phrase case (Josh 1:1) that asserts the word count is unchanged, and a maqqef case.
   - Add a **full-corpus sweep**: all 10,083 words transliterate without raising, the output is never empty, and the output uses only the allowed alphabet plus `-` and space.
9. Rewrite the `hebrew.py` docstring as a summary that points at the test file.

## C. `data/roots.json`: identity by id (independent of B)

1. **Schema**, still empty:
   ```json
   { "_note": "...", "version": 1,
     "roots": { "<slug>": { "ids": ["2763a", "2764a"], "note": "why these ids are one root" } } }
   ```
   Keep it flat: no `kind`/`members` (§1). Every slug matches `[a-z0-9-]+`.
2. **New `pipeline/roots.py`** loader:
   - Normalize ids by stripping the trailing letter for queries.
   - Every id must exist as a lemma in `Joshua-words.tsv`.
   - Enforce the A5 rule.
   - Every tracked thread's `root` in `threads.json` must exist in `roots.json`.
3. **Test file.** Build synthetic roots from real ids pulled from the TSV. Cover: an unknown id fails, a bad slug fails, a lettered id normalizes, and a thread whose root is missing fails.

## D. `pipeline/audit_thread_coverage.py`: set arithmetic over `data-w` (needs C)

1. **Source side.** For a root, collect every `word_id` in `Joshua-words.tsv` whose numeric lemma segments (letter stripped) intersect the root's id set. Key each by its ref, then apply A4.
2. **Fragment side.** Parse `data-root` and `data-w` from built unit HTML. A tracked-thread span with no `data-w` is a hard error.
3. **Report**:
   - **gap**: an id that is in the source within the unit's passage but untagged.
   - **wrong id**: a tagged id whose lemma isn't in the root's set.
   - **stray**: a tagged id that is outside the unit's passage or doesn't exist.
   - Keep the per-verse view for local roots.
4. **Remove** `_compile_stems`, `hebrew_hits`, `strip_prefixes`, and `HEBREW_PREFIX_LETTERS`. Remove `strip_accents` too if nothing else needs it.
5. **Keep**: the book-field source lookup and its self-check, the CLI shape (`--unit`, `--stub`), and `coverage_for_unit`/`coverage_for_fragment` for the Phase 3 porter.
6. **Replace `--forms` with `--ids <root>`.** It lists every surface form, ref, and count that a root's id set pulls in. That's the review step before Lane commits an id set.
7. Beth-el is two tagged words that share one id (§6), so count by word id, not by lemma occurrence.

## E. `pipeline/verify_thread_coverage.py`: rewrite (needs C, D)

1. Re-derive source id sets on its own. Parse the TSV a different way (the `csv` module, not `split`), don't import the audit's functions, and compare the results.
2. Retire the checks that no longer apply: the final-letter fold, and the kol/Caleb stem over-match. Replace them with a regression pulled from the TSV at check time: the id set {3605} yields exactly as many word ids as there are TSV rows with lemma 3605, and none with 3612 (Caleb).
3. Synthetic fragment fixtures (Hebrew pulled from the TSV, never typed) must catch each of these:
   - a gap
   - a wrong-lemma id
   - a missing `data-w` on a tracked span
   - an id outside the unit's passage
   - a nonexistent id

## F. `pipeline/unit_meta.py`: match the contract (§3, §4, §7)

1. `ALLOWED_TOP_LEVEL_KEYS` = unit, slug, passage, title, movement, roots, threads. **Remove `descriptor` and `discourse`** (§3 table; port analysis §7.5).
2. `threads` must hold all four sub-keys (opens, payoffs, candidates, retro), each a list.
3. `opens`/`payoffs` entries require a `note` (checklist 4).
4. `candidates[]` = `{root, why, ids?, refs?}`.
   - `ids` are strings matching `^\d+[a-z]?$`; `refs` are `C:V` strings.
   - Reject `stems` and `exclude`.
5. `roots[]`: reject `kind`/`members` again. Matthew's validator had this check, and the fork dropped it.
6. **No-Hebrew check: remove the `candidates[].stems` exemption.** Checklist 12 says "no exceptions, attribute values included." Flip the matching test in `test_unit_meta.py` to must-fail.
7. Add the cheap fragment checks:
   - Every `data-root` resolves to `threads.json` or this artifact's `roots[]` (checklist 6).
   - Every tracked-thread span has a `data-w` (checklist 7).
   - `h3.pericope` contains a `· C:V` range (checklist 9).
   - No inline `style=` and no `--c-*` vars (checklist 13).
   - `class="rl"` inside a `.v` block raises a warning (§4).
8. **Defer** the `.gloss`/`.compare` sibling/nesting check (checklist 10) to Phase 3, together with the porter. The same goes for any `aside.echo` check, which ships only if unit 1 wants echo.
9. `REQUIRED_COMPONENT_CLASSES`: the legend is `section.block.legend`, so require both `block` and `legend`.

## G. `css/styles.css`: whitelist scaffold

- Add the classes §4 and §8 use: `mast`, `kicker`, `block`, `legend`, `notes`, `pericope`, `v`, `n`, `r`, `rl`, `gloss`, `compare`, `en`, `unit`.
- Leave `echo` out until it's decided.
- **Acceptance**: a new test reads the §8 worked example **straight out of `joshua_study_style_reference.md`** (extract the fenced html block at test time; don't copy it). Run `validate()` and `validate_fragment()` on it against a threads/roots fixture that declares `devote` and `give`. It must pass clean. This test is the contract between the style reference and the validator; if either drifts, it fails.

## H. Docs and cleanup (last)

- `CLAUDE.md`: remove the ⚠ banners, rewrite the Transliteration and Thread-coverage sections to describe the new behavior, and update the repo layout.
- `PLAN.md`: mark Phase 0.6 done and record the §A answers.
- `pipeline/threads_digest.py` prose: replace the mentions of `thread-stems.json` and "consonant-skeleton stems/exclude" with `roots.json` ids/refs. Regenerate `threads-digest.md`.
- Delete or archive `thread-stems.json` per A8. Grep for leftover references in `pipeline/`, `CLAUDE.md`, `PLAN.md`, and `project-side/README.md`.
- `project-side/README.md`: add `data/roots.json` if Lane wants the research project to see id sets (ask).
- Logs: `improvements_log.md`, `session_index.md`, and a new `session_summary_<date>.md`.

## Order

A → (B ‖ C) → D → E → F → G → H

B and C–F don't depend on each other. F's "`data-root` resolves" check can use C's loader once it exists.

## Done when

- `test_hebrew.py`, the roots test, `verify_thread_coverage.py`, and `test_unit_meta.py` all pass. That includes the §8 worked-example test and the full-corpus transliteration sweep.
- `audit_thread_coverage.py` runs clean against the empty data.
- No file still references stems, `strip_prefixes`, or the skeleton-keyed overrides.
- `CLAUDE.md` has no ⚠ banners left.

## Out of scope

- Populating `units.json` (Phase 1).
- Porting `port_artifact.py` / `scan_occurrences.py` / `build.py` (Phase 3).
- The app shell (Phase 4).
- `resources.md`. It's still missing and Lane-authored; mention it, don't write it.
