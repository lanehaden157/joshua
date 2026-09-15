# Session Summary: 2026-09-14

## Done
- **Corpus**: pinned morphhb 2.0.2 and HebrewLexicon @ `21c9add` in this repo, starting from scratch, since the earlier pin lived only in `Projects/Hebrew`. Generated `Joshua-reading.txt`, `Joshua-words.tsv`, `candidate-boundaries.md`, and `Joshua-english.txt` (WEB classic). Checked against BHS: 658 verses, ch. 21 = 45, 10,083 `<w>` elements, 52 petuḥah + 42 setumah.
- **`pipeline/hebrew.py`** plus `test_hebrew.py`. A bug caught in review is fixed: holam-vav was rendering a spurious "w" in about 12% of words, including Yehoshuaʿ.
- **Forks from Matthew**:
  - `audit_thread_coverage.py`, with its verify step `verify_thread_coverage.py`
  - `unit_meta.py`, with a hardened `validate()` and `test_unit_meta.py`
  - `threads_digest.py`
- **Scaffolding and docs**:
  - Scaffolded `data/` (units, threads, roots), `css/styles.css`, and `translation-choices.md`
  - Wrote `PLAN.md` and `project-side/README.md` (a pointer index)
  - Renamed `instructions.md`
- Wrote `phase-0.6-plan.md` for the next session.

## Takeaways
- `joshua_study_style_reference.md` arrived late in the session and **supersedes** much of the day's engineering:
  - Id-based root identity replaces substring stems. The style reference measures 0% recall for Yehoshuaʿ under substring matching.
  - `hebrew.py`'s scheme needs rework: spirantization, sheva, shin, gemination, furtive patach, lemma-keyed overrides, and YHWH output.
  - The validator has several contract gaps.
  - All of this is itemized, with measured examples, in `phase-0.6-plan.md`.
- **Correction**: last session part I claimed `hebrew.py` used vowel macrons. It doesn't, and the docs are fixed.
- **Rules that held up all session**:
  - Pull Hebrew by word id; never hand-type it.
  - Write the verifier before the generator.
  - Check a claim against the corpus before stating it. The kol count (236) was confirmed three independent ways.

## Open
- Phase 0.6's §A decisions for Lane: tsadi, morpheme hyphens, how to distinguish aleph from ayin, Ketiv vs Qere id, one id in two roots, local roots in `roots.json`, override API, and whether to delete `thread-stems.json`.
- `resources.md` is referenced by `instructions.md` but not yet written (Lane's to author).
- No git repo exists for Joshua yet.
