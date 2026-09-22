# Joshua

How this repo behaves. The artifact contract (fragment shape, meta schema,
components, transliteration scheme, checklist) lives in
`joshua_study_style_reference.md` and is authoritative over this file — this
file points there rather than restating it.

**State (2026-09-22):** Phases 0–5 done; units 1–4 built (Movement I complete);
20 tracked threads in `data/threads.json`/`data/roots.json` (every one carries an
`echo`). This repo is not migrating onto the shared core (`../g6-plan.md`, which is for future books); copy a core fix across only when it clearly helps.
`source-artifacts/` is current for all four units: edit there and re-port
rather than editing `units/` by hand. Tracked-thread colours are assigned
algorithmically (`port_artifact.assign_tracked_colors()`), same as local
roots — never hand-picked (Lane, 2026-09-22).

## Project documents

- **`joshua_study_style_reference.md`** — the artifact contract.
- **`Claude_ai_chat_side_instructions.md`** — the Claude.ai research project's
  workflow (four passes incl. the intertext pass, standing moves). Not in the
  synced mirror: Lane pastes it into the project's instructions by hand.
- **`joshua_literary_unit_map.md`** — 24 units, 4 movements, confirmed.
- **`PLAN.md`** — phase list and open questions.
- **`Port analysis.md`** — the Matthew-pipeline port audit. Guide, not gospel.
- **`translation-choices.md`** — English-rendering glossary. Update in the same
  turn as any wording decision.
- **`project-side/README.md`** — every file that round-trips with the Claude.ai
  project. Check there before hunting for a path.
- **`resources.md`** — lives only in the Claude.ai project, not the repo, by
  design. References to it are correct.

## Source data

- **`Joshua-reading.txt`** — pointed Hebrew, `Josh C:V<TAB>text`. Ketiv/Qere
  pairs use the pointed Qere.
- **`Joshua-words.tsv`** — one row per OSHB `<w>`:
  `word_id\tref\tsurface\tlemma\tmorph`. Ketiv and Qere each get a row, so
  10,083 rows, not 10,051.
- **`Joshua-english.txt`** — WEB classic (`eng-web`, "Yahweh", USA spelling;
  not `eng-webp`/`eng-webbe`), same line shape, footnotes stripped. A separate
  file rather than a third column, so the Hebrew file's shape stays stable.
  **Role: provenance only** (Lane, 2026-09-19). It is *not* the base text of
  the study translation, not a draft the chat side edits, and not a diff
  target — the style reference is explicit that the verse text is "not a
  polish of an existing English version". It is generated and pinned so the
  corpus is reproducible, and nothing in the workflow reads it. Its absence
  from `project-side/synced/` is deliberate, not a gap. (It is also not
  where the *Hebrew* comes from — that is morphhb, `pipeline/corpus/wlc/`.)
- **`candidate-boundaries.md`** — every petuhah/setumah marker, uninterpreted.
- Generators: `pipeline/build_reading.py` (from `pipeline/corpus/wlc/Josh.xml`)
  and `pipeline/build_english.py` (from WEB USFM; asserts verse count matches
  the Hebrew file).

### Corpus pin

- **morphhb 2.0.2** — `package.json`/lock, `--save-exact`. shasum
  `2ea8c8adc94ff7bd1b3ac3fdbcfd1a489a4c145a` (matches npm registry).
  `pipeline/corpus/wlc/Josh.xml` copied from `node_modules/morphhb/wlc/`.
- **HebrewLexicon @ `21c9add13bc727d3a951361778e97e3ff7afd1ce`** —
  `AugIndex.xml`, `LexicalIndex.xml`, `BrownDriverBriggs.xml`,
  `HebrewStrong.xml` in `pipeline/corpus/lexicon/`. Not yet consulted by any
  build.
- Both CC BY 4.0.
- **WEB classic** — `https://ebible.org/Scriptures/eng-web_usfm.zip`, book file
  `07-JOSeng-web.usfm`, in `pipeline/corpus/web/`. Public domain.

### Verification (against printed BHS)

Re-check against the file on disk rather than trusting prior numbers:

- 658 verses; chapter 21 has 45 (21:36–37 present, unmarked).
- 10,083 `<w>`: 10,051 running text + 32 Qere under
  `<note type="variant"><rdg type="x-qere">`.
- 52 petuhah + 42 setumah = 94 breaks.

If a count drifts on re-fetch, flag it loudly — it likely means the corpus is
wrong, but that needs eyes.

## Transliteration — `pipeline/hebrew.py`

Scheme rules: style reference §5. **`pipeline/test_hebrew.py` is the
authoritative definition** (real OSHB word ids, hand-derived expectations, plus
a full 10,083-word sweep); if prose disagrees, the test wins.

Repo-side notes not in the style reference:

- Tsadi is `ts`, shin `sh`, sin `ś`. Morpheme boundaries are hyphenated
  (`ha-melek`, `u-`). Matres: shuruq, holam-male (bare vav + holam is a vowel,
  ~12% of words), hiriq-yod → `i`, tsere-yod → `e`. Furtive patach glides
  before the final guttural.
- Ayin carries a baked-in combining low line (ʿ̲) so it survives TSV/terminal/
  HTML without CSS.
- Marks detected via `unicodedata.combining() != 0`, not codepoint ranges
  (which would catch maqqef/sof-pasuq/paseq).
- **Overrides key on lemma id** (3068/3069 → `YHWH`, 3389 → `Yerushalayim`,
  3605 → `kol`), so they apply only via `transliterate_word(surface, lemma,
  morph)` or `transliterate_ref("Josh C:V")`. Bare `transliterate(text)` is
  deterministic-only. `_align_lemma_to_surface()` maps lemma segments to
  surface morphemes; zero misalignments across the corpus.

## Roots and thread coverage

A root is a hand-curated set of lemma ids, never a Hebrew string (style
reference §2).

- **`data/roots.json`** — tracked threads only:
  `{"roots": {"<slug>": {"ids": [...], "note": "..."}}}`. Lane's policy.
- **`pipeline/roots.py`** — loader/validator: every id is a real lemma, no id
  in two roots, every thread's root has an entry. `bare_id()` strips the
  disambiguator letter and OSHB's `+` marker; `lemma_key()` keeps the letter
  and strips only `+`. Matching uses both via `split_ids()`: a bare id claims
  every lexeme under a number, a suffixed id claims exactly one — so `3885a`
  *lodge* and `3885b` *murmur* can be separate roots (style reference §2 has
  the three real cases). A suffixed id the corpus never carries is an error,
  since it would match nothing. `load_roots()` resolves its
  default path at call time — it used to bind at import, which silently
  ignored test monkeypatches.
- **`pipeline/audit_thread_coverage.py`** — set arithmetic over word ids.
  Reports **gap**, **wrong**, **stray**, and **missing_data_w**. Local roots get
  an informational per-verse view. Ketiv rows dropped by adjacency (same ref,
  unpointed then pointed — exactly 32 pairs). Only `class="r"` spans count;
  `rl` is excluded. `--ids <root>` lists every form/ref an id set pulls in.
- **`pipeline/verify_thread_coverage.py`** — independent re-derivation (own
  Ketiv detection, own bare-id parser, no shared matching code), with five
  synthetic failure fixtures.

### Thread promotion: book-wide vs. local (Lane, 2026-09-16)

Claude decides whether a `threads.candidates[]` root becomes a tracked thread,
**biased toward book-wide** — a local root that later pays off is worse than a
tracked one that doesn't. Ask Lane only when genuinely unsure (unit 1: `kol`,
236 occurrences, asked, kept local).

Its colour comes from `port_artifact.assign_tracked_colors()` (Lane,
2026-09-22: never hand-pick) — the tracked-thread counterpart to
`assign_hues()`, checked against every other tracked colour plus every local
root colour on record in `data/units.json`, globally. The `WELL` palette was
expanded from 20 to 65 colours the same day promoting three threads at once
exhausted the original well (see `pipeline/port_artifact.py`'s `WELL` comment
for the generation method) — if it runs short again, expand it the same way
rather than picking a colour by hand.

Promotion makes every occurrence in every built unit require `data-w`. Existing
artifacts usually already wrap the occurrences, so it's normally a
`retrofit-tags.json` `retag` pass, not new tagging.

**Retrofit recipe** (per promoted root, per unit):

1. Pull every occurrence from `Joshua-words.tsv` in the unit's passage —
   `audit_thread_coverage.source_hits_for_root(words, entry["ids"])` does
   exactly this. Keep `(ref, word_id, surface, morph)`. **In practice run
   `python pipeline/assign_data_w.py N` instead of steps 1–3 by hand; it does
   the zip and reports only the verses it cannot decide.**
2. Pull every `<span class="r" data-root="ROOT">` from the fragment, in order.
3. Zip the two lists per verse.
4. Where a verse's counts differ, look closer: one span over two Hebrew words
   (one `retag`, or split by hand), one Hebrew word as two spans (keep the
   span a reader recognizes as the root and `unwrap` the other — `rl` still
   picks up the root's colour, so demoting isn't enough; unit 1 v15 tags
   *rest*, not *gives*), or a truly untagged occurrence (`add`).
5. Same root + same text twice in a verse → `retag`'s `occ` (1-based).
6. One entry per occurrence: `{"unit", "verse", "from", "to", "text", "w"}`.
7. Re-run `python pipeline/port_artifact.py N` then
   `python pipeline/audit_thread_coverage.py`; every promoted root must report
   clean. Don't hand-wave a nonzero count.

## Canon leads — `pipeline/canon_leads.py`

The mechanical half of the project side's intertext pass (Lane, 2026-09-21):
Claude Code finds where words recur, the project side decides what matters.
Per unit, `canon-leads/canon-leads-unit-NN.md` lists rare words (≤ `--rare`
verses in the Hebrew Bible, default 20) and adjacent-lemma phrases shared
with the Torah (overlapping pairs merged), each with every hit,
transliterated. It reads the whole Hebrew Bible from
`node_modules/morphhb/wlc`. It is deliberately narrow: listing every word
would mean ~33,000 Torah verses for Joshua 2. Blind to common words, themes,
type-scenes and the New Testament. `build.py` regenerates it for every built
unit plus the next one, and `check_project_sync.TRACKED_FILES` globs the
folder into the synced mirror. `pipeline/test_canon_leads.py` pins real hits
(Gen 8:9, Exod 15:15–16, Deut 1:28, Gen 19:4).

Drafting cross-references here from memory is the thing this replaces. The
unit 1–2 echoes were written that way and are provisional until the project
side runs its pass on them.

## Fragment validation — `pipeline/unit_meta.py`

Implements style reference §3, §4, §7. Rules live there; repo-side notes:

- `ALLOWED_TOP_LEVEL_KEYS` passing only means `validate()` won't reject a key —
  `generate()` must separately round-trip it or it's dropped on regen.
- `validate_fragment()` hard checks: component whitelist (grep-diff against
  `css/styles.css`, `block` + `legend` required), endnote pairing, zero Hebrew
  script (U+0590–U+05FF, attributes included), `data-root` resolves,
  tracked spans have `data-w`, pericope ranges, no inline style.
- `warnings_for_fragment()` is a separate non-fatal channel (`rl` inside `.v`).
- `pipeline/test_unit_meta.py` includes an acceptance test that regex-extracts
  the style reference's `## 8. Worked example` html fence at test time — keep
  that heading and fence intact.

## Porting a unit — `pipeline/port_artifact.py`

    python pipeline/port_artifact.py 6              # port source-artifacts/joshua_06_translation.html
    python pipeline/port_artifact.py 6 --dry        # preview, write nothing
    python pipeline/port_artifact.py 6 --src X.html # dry-run a practice file
    python pipeline/port_artifact.py 1 --force      # re-port an already-built unit

**Re-porting a built unit needs `--force`.** A re-port replaces the fragment
wholesale with the source artifact. `7af1a59` (the unit 2 port) re-ported
unit 1 from a source artifact a day staler than the fragment, and silently
lost four local roots, the anonymous-voice notes and the C7 markup. Fixed
2026-09-21 by making the source artifact current and adding the guard.

Deliberately slimmer than Matthew's:

- No `extract_units.py` cleanup — artifacts arrive in contract shape.
  `to_fragment()` only strips the meta block and prefixes endnote ids
  (`n1` → `u06-n1`).
- No `--backfill`.
- Candidate preview runs proposed `ids` through
  `audit_thread_coverage.source_hits_for_root()`, so preview and audit agree.
- `merge_units_json()` carries a local root's optional `example`/`echo` into
  `data/units.json`. It used to write only `{color, translit, gloss}`, so
  `generate()` dropped both on regen.
- Only `unit_meta.validate()` on the meta dict blocks the write;
  `validate_fragment()` findings are reported, and the fragment is still
  written for browser review.
- Local roots get a colour from Joshua's own `WELL` palette via
  `assign_hues()` (CIE-Lab distance, avoiding the unit's other local hues and
  every tracked thread's colour). Tracked-thread colours live only in
  `data/threads.json` — that file itself is still edited by hand (nothing
  writes it automatically), but its colour *values* come from
  `assign_tracked_colors()`, the same algorithm, never picked by eye
  (Lane, 2026-09-22).
- Retro entries are dry-checked via `apply_retrofit.FNS[op]` and merged into
  generated `pipeline/retro-tags.json`, separate from hand-authored
  `pipeline/retrofit-tags.json`.

Supporting scripts:

- `apply_retrofit.py` — `add`/`retag` accept optional `w` (inject/update
  `data-w`); `retag` accepts `occ`. `retag_word` deliberately doesn't take `w`
  (bulk reclassification changes the root, not the word).
- `scan_occurrences.py` — unchanged from Matthew.
- `verify_occurrences.py` — narrower than Matthew's: colour-resolution and
  colour-collision checks dropped (`unit_meta` already checks resolution).
- `refresh_meta.py`, `build.py` — near-unchanged; `build.py` adds a
  `roots.py` step between `verify_occurrences.py` and `threads_digest.py`.
- `test_port_artifact.py` runs end to end against a scratch copy of `data/`,
  `units/`, `pipeline/out` using the §8 worked example; the subprocess step is
  stubbed (those scripts have their own tests).

## App shell (Phase 4)

`index.html` + `app/*.js` + `css/styles.css`, forked from Matthew. No
discourse layer (movements only), a Matthew-style book map.

- `app/threads.js` is Matthew's plus `example` and `echo` fields on resolved
  roots (`echo` renders as a "cf." line in the root popover, `.rp-echo`); originally just `example` (the change that exposed the module cache-busting bug in `main.js`); `app/search.js` near-unchanged (storage key
  `joshua.search.q`); `app/spotlight.js` has `.gloss` and `aside.echo`
  (compare/synoptic paths deleted) — both are verse-sibling asides
  collapsed behind one shared per-verse toggle.
- `app/main.js` reads `movements[]` as `{n, name, span, units}` (the
  `data/units.json` shape). `normalizeSectionHeadings()` dropped.
  **`hoistStructureBlocks()` skips `.notes` as well as `.legend`** — Joshua's
  endnotes carry `block`, so an unchanged port would hoist them above the text.
- `css/styles.css` — Joshua's own theme, not Matthew's: sun-bleached ground,
  clay (verse numbers, endnotes), bronze (headings, chrome), Jordan teal
  (placement). Cinzel display, Frank Ruhl Libre body. No `.compare`, no
  Matthew-only components. `aside.echo` (cross-book echo) built 2026-09-21,
  before unit 2 — same shape as `.gloss` (verse sibling, never nested,
  always closed), collapsed behind the same toggle in `app/spotlight.js`,
  Jordan teal + "cf." prefix once open. `pipeline/unit_meta.check_echo()`
  enforces the `data-anchor="C:V"` match and the nesting-depth check the
  style reference calls for (§4, checklist 11).
- Preview via `.claude/launch.json` (static file server).

## Repo layout

```
CLAUDE.md                        this file
PLAN.md                          phase list, open questions
Port analysis.md                 Matthew port audit
Claude_ai_chat_side_instructions.md  research-project workflow
joshua_study_style_reference.md  the artifact contract (authoritative)
joshua_literary_unit_map.md      24 units / 4 movements
translation-choices.md           English-rendering glossary
threads-digest.md                generated from data/threads.json -- never hand-edit
project-side/README.md           index of files round-tripping with the research project
project-side/sync-state.json     fallback hash state for check_project_sync.py
project-side/synced/             generated mirror for GitHub-connector sync -- never hand-edit
Joshua-reading.txt, Joshua-words.tsv, Joshua-english.txt, candidate-boundaries.md   generated source data
source-artifacts/                incoming research artifacts (joshua_NN_translation.html)
canon-leads/                     generated intertext reading lists, one per unit (synced)
units/                           ported fragments (unit-NN.html)
data/units.json                  24-unit / 4-movement registry
data/threads.json                tracked threads (Lane's policy)
data/roots.json                  tracked-thread id sets (Lane's policy)
data/occurrences.json            generated by scan_occurrences.py
index.html, app/*.js, css/styles.css   app shell
.claude/launch.json              local static server for previewing
pipeline/build_reading.py        Hebrew generator
pipeline/build_english.py        English generator
pipeline/hebrew.py               transliteration (test_hebrew.py is authoritative)
pipeline/roots.py                roots.json loader/validator
pipeline/audit_thread_coverage.py   id-based coverage audit
pipeline/verify_thread_coverage.py  independent re-derivation of the audit
pipeline/unit_meta.py            meta parse/validate/generate + fragment checks
pipeline/threads_digest.py       threads.json -> threads-digest.md
pipeline/port_artifact.py        port a research artifact into the site
pipeline/canon_leads.py          unit -> canon-leads/ (rare words + Torah phrases, whole Hebrew Bible)
pipeline/apply_retrofit.py       idempotent fragment-edit ops, replayed by build.py
pipeline/retrofit-tags.json      hand-authored fragment edits
pipeline/retro-tags.json         generated retro fixes (created on first merged retro)
pipeline/scan_occurrences.py     units/*.html -> data/occurrences.json
pipeline/verify_occurrences.py   independent count re-derivation + tagged-flag check
pipeline/refresh_meta.py         regenerate every fragment's meta block
pipeline/build.py                re-derive everything downstream of fragments
pipeline/sync_to_github.py       primary project-side sync (mirror + push)
pipeline/check_project_sync.py   fallback: which project-side files need re-pasting
pipeline/test_*.py               hebrew, roots, unit_meta, apply_retrofit, scan_occurrences, verify_occurrences, port_artifact, canon_leads
pipeline/corpus/{wlc,lexicon,web}/   pinned sources
package.json                     morphhb pin
```
