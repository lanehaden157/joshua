# Joshua

Phase 0.6 (the rework that lines this repo up with
`joshua_study_style_reference.md`) is done as of 2026-09-14. The sections
below now describe the reworked pipeline directly; see `PLAN.md`'s Phase
0.6 entry for the §A decisions that were locked in along the way.

## Project documents

- **`joshua_study_style_reference.md`** — the artifact contract (fragment
  shape, unit-meta schema, component whitelist, transliteration scheme,
  checklist). Authoritative over this file where they disagree.
- **`Claude_ai_chat_side_instructions.md`** — the research project's own operating
  instructions (persona, sourcing, three-pass workflow). Kept current in
  the Claude.ai project via `project-side/synced/` and its GitHub-connector
  sync (paste-sync is a fallback only); see `project-side/README.md`.
- **`joshua_literary_unit_map.md`** — 24 units, 4 movements, confirmed
  as-is by Lane (fulfills the style reference's §9 TODO).
- **`PLAN.md`** — phase list, open questions, and the Phase 0.6 rework
  list referenced above.
- **`Port analysis.md`** — the Matthew-pipeline port audit this whole
  structure was designed against. Guide, not gospel — read with `PLAN.md`
  for where its recommendations were followed vs. superseded.
- **`translation-choices.md`** — hand-maintained English-rendering
  glossary. Update in the same turn as any wording decision.
- **`project-side/README.md`** — index of every file that needs to
  round-trip with the Claude.ai research project (paths, direction,
  update cadence) — check there before hunting for a path.

## Source data

- **`Joshua-reading.txt`** — pointed Hebrew, one line per verse:
  `Josh C:V<TAB>text`. Where OSHB marks a Ketiv/Qere pair, the line uses the
  pointed Qere form (what is read aloud), not the unpointed Ketiv spelling.
- **`Joshua-words.tsv`** — one row per `<w>` element in the OSHB XML:
  `word_id\tref\tsurface\tlemma\tmorph`. Ketiv and Qere each keep their own
  OSHB id and get their own row (same `ref`), so this totals 10,083 rows,
  not 10,051 — see verification below.
- **`candidate-boundaries.md`** — every petuhah (`x-pe`) and setumah
  (`x-samekh`) marker in Joshua, in document order, unclustered. Raw
  material for a future literary-unit map; not interpreted here.
- **`Joshua-english.txt`** — World English Bible, classic/WEBUS edition
  (`eng-web` on eBible.org — USA spelling, "Yahweh" not "LORD"; *not*
  `eng-webp`/`eng-webbe`), public domain. Same shape as the Hebrew file:
  `Josh C:V<TAB>text`, footnote markers stripped. Kept as a **separate
  file** rather than a third column on `Joshua-reading.txt` — the Hebrew
  file's two-column shape is what the pipeline already reads, so adding a
  column there would be the more disruptive option; a parallel file with
  the same line shape is not.
- Generators: `pipeline/build_reading.py` (Hebrew, reads
  `pipeline/corpus/wlc/Josh.xml`) and `pipeline/build_english.py` (English,
  reads a WEB USFM source — see that file's docstring for the exact URL).
  `build_english.py` asserts its verse count matches
  `Joshua-reading.txt`'s and fails loudly on any mismatch, since Joshua's
  MT/LXX divergences are textual, not versification splits.

### Corpus pin

- **morphhb 2.0.2** — pinned via `package.json`/`package-lock.json`
  (`npm install morphhb@2.0.2 --save-exact`).
  shasum `2ea8c8adc94ff7bd1b3ac3fdbcfd1a489a4c145a` (verified against the npm
  registry's `dist.shasum` for this version — matches).
  `pipeline/corpus/wlc/Josh.xml` is copied from `node_modules/morphhb/wlc/Josh.xml`.
- **HebrewLexicon @ `21c9add13bc727d3a951361778e97e3ff7afd1ce`** (2019-09-02).
  `AugIndex.xml`, `LexicalIndex.xml`, `BrownDriverBriggs.xml`, `HebrewStrong.xml`
  copied into `pipeline/corpus/lexicon/` from that commit. Not currently
  consulted by `build_reading.py` (lemma/morph come straight off the WLC
  `<w>` tags) — pinned here for when a build needs gloss/POS lookups.
- Both licensed CC BY 4.0.
- **WEB classic (`eng-web`)** — USFM pulled from
  `https://ebible.org/Scriptures/eng-web_usfm.zip`, book file
  `07-JOSeng-web.usfm`, copied into `pipeline/corpus/web/`. Public domain.

### Verification (against printed BHS)

Checked directly against `pipeline/corpus/wlc/Josh.xml` after the fresh
install above — do not assume a prior session's numbers still hold without
re-checking against the file on disk:

- 658 verses total (`<verse osisID>` count) — matches BHS.
- Chapter 21 has 45 verses (`Josh.21.36` and `Josh.21.37` both present,
  unmarked) — matches BHS, where 21:36–37 are present.
- 10,083 `<w>` elements total: 10,051 in the main running text + 32 Qere
  alternates nested under `<note type="variant"><rdg type="x-qere">`.
- 52 petuhah + 42 setumah markers = 94 total paragraph breaks.

If any of these counts drift on a re-fetch, flag it loudly rather than
treating it as settled — it likely means the corpus, not BHS, is wrong, but
that needs eyes, not an assumption either way.

## Transliteration

`pipeline/hebrew.py` — deterministic Hebrew -> Latin transliteration, the
Hebrew sibling to `Projects/Matthew/pipeline/greek.py` (same role: one
small pure function, tested via its own `__main__` block). A new module,
not a parameterization of `greek.py`. Reworked in Phase 0.6 to match
`joshua_study_style_reference.md` §5 exactly — port `Projects/Hebrew/
pipeline/transliterate.py`'s sheva/matres/furtive-patach *rules*, not its
alphabet (that module models b/k/p spirantization for pronunciation,
which this project deliberately does not).

- **Alphabet**: `ʾ b g d h w z ḥ ṭ y k l m n s ʿ p ts q r sh ś t`. No
  vowel length. **No spirantization** — bet/kaf/pe are always `b`/`k`/`p`,
  never `v`/`kh`/`f`. Tsadi is the digraph `ts` (§A1: matches how shin was
  already a digraph rather than a diacritic), not `ṣ`. Shin (no sin dot)
  is `sh`; sin (sin dot) is `ś`, distinct from samekh's plain `s`.
- **Sheva (na/nach)**: word/morpheme-final silent, word/morpheme-initial
  vocal, first of a consecutive pair silent and the second vocal,
  otherwise silent — plus one the parser project didn't need: sheva under
  a dagesh-forte (doubled) consonant is vocal (`hammelakim`, not
  `hamlakim`).
- **Dagesh forte doubles the consonant.** A non-begadkefat letter's dagesh
  is always forte (doubled) except vav-shuruq and he-mappiq; a begadkefat
  letter's (bet/gimel/dalet/kaf/pe/tav) dagesh is forte only right after
  an audible vowel, otherwise lene (word-initial hardening, not doubled).
  Since spirantization is gone, lene vs. forte only ever changes whether
  the letter doubles.
- **Matres lectionis**: shuruq and holam-male (unchanged from before),
  plus **hiriq-yod → `i`** and **tsere-yod → `e`** (new — a vowelless bare
  yod right after a hiriq/tsere is absorbed, not also emitted as a
  consonant `y`).
- **Furtive patach**: a patach on a word/morpheme-final ḥet, ayin, or
  mappiq'd he glides in *before* the guttural (`yehoshuaʿ`, not
  `yehošuʿa`).
- Niqqud and cantillation are both identified via `unicodedata.combining()
  != 0`, not a hand-rolled codepoint-range check (that would also catch
  maqqef/sof-pasuq/paseq, which aren't combining marks). Meteg is dropped
  the same way.
- Handles full phrases without losing spaces — only Hebrew letters,
  combining marks, and the literal `/` morpheme-boundary marker get
  consumed into a "word"; everything else (including every space) passes
  through untouched.
- Word-initial shuruq renders `u-`, not `w-`. Morpheme boundaries are
  hyphenated (§A2: `ha-melek`, `u-`), not joined solid — including where
  gemination doubles a following morpheme's own first consonant
  (`ha-mmelek`, since OSHB already marks the article as its own `/`-split
  morpheme, so the doubling never has to cross the hyphen itself).
- **Overrides are keyed on LEMMA ID, not consonant skeleton** (§5, §A7):
  `OVERRIDES` covers `3068`/`3069` → bare `YHWH` (not `Yahweh` — that's
  `translation-choices.md`'s job), `3389` → `Yerushalayim` (the
  deterministic pass loses the word's second vowel: `yerushalam`), `3605`
  → `kol` (deterministic renders `kal` in most of its Joshua occurrences).
  Because an override now needs a lemma, it only applies through
  `transliterate_word(surface, lemma, morph)` or `transliterate_ref("Josh
  C:V")` (which pulls both from `Joshua-words.tsv`) — bare
  `transliterate(text)` stays a deterministic-only fallback with no
  overrides, same role it always had. `_align_lemma_to_surface()` lines up
  OSHB's lemma segments (which skip pronoun-suffix morphs) with surface
  morphemes by walking `morph`'s segments; validated over all 10,083 rows
  via `test_hebrew.py`'s corpus sweep, zero misalignments.
- Alef and ayin are visually near-identical at small sizes. Ayin always
  renders with a trailing combining low line (ʿ̲), baked into the
  returned string itself — not a wrapping `<span>` — so the distinction
  survives being copied into a TSV, a terminal, or HTML gloss text
  without depending on downstream CSS (§A3: kept, not replaced with plain
  `ʾ`/`ʿ` + markup).
- Holam male (bare vav + holam, no dagesh -- plene "o" spelling, e.g. the
  vav in Yehoshuaʿ or in môt) is treated as a vowel, not a consonant, the
  same way shuruq is. This was fixed after review caught it in Phase 0:
  the original code emitted a spurious "w" (Yehoshuaʿ itself came out
  `yehwošuʿ̲a`), and the pattern isn't rare -- it hits ~1,191 of 10,083
  words in Joshua (~12%).
- **`pipeline/test_hebrew.py` is the scheme's authoritative definition.**
  Its 33 word-level cases are real OSHB word ids pulled from
  `Joshua-words.tsv` (not hand-typed), each expected value hand-derived
  from the word's actual Unicode codepoints and the rules above — not
  copied from the generator's own output. Plus 3 `transliterate_ref`-vs-
  `transliterate_word` agreement cases, a full-verse phrase case, an
  isolated maqqef case, and a full 10,083-word corpus sweep (no crashes,
  no empty output, alphabet-only output). If this doc and that file ever
  disagree, the test file wins.

## Root identity and thread coverage (units/threads not built yet)

**A root is a hand-curated set of Strong's/lemma ids, not a Hebrew
string** (style reference §2). Measured against real OSHB Joshua,
substring-stem matching was bad enough on weak roots to be disqualifying
(*natan* 42% recall, *qum* 24%, *nakah* 3%, **Yehoshuaʿ 0%**) — Joshua's
load-bearing verbs are weak roots, so this isn't a hypothetical concern.
No Hebrew string is ever compared to another Hebrew string anywhere in
this project.

- **`data/roots.json`** — the global registry, tracked threads only
  (§A6; local, non-thread roots stay in a unit's own unit-meta `roots[]`,
  see below). Flat shape: `{"roots": {"<slug>": {"ids": [...], "note":
  "..."}}}` — no `kind`/`members`, no `translit`/`gloss`/`color` (those
  live with a thread's other data, not with its id-set). Lane's policy;
  nothing in the pipeline writes it.
- **`pipeline/roots.py`** — loader/validator. Every id must exist as a
  lemma in `Joshua-words.tsv`; an id claimed by two roots is a hard
  failure (§A5); every `threads.json` thread's `root` must resolve to an
  entry here. `bare_id()` strips the trailing disambiguator letter (and
  OSHB's own `+` continuation marker, e.g. `1007+` for "Beth-" of
  "Bethel") — opaque, not a homograph signal (style reference §2).
  `pipeline/test_roots.py`: 11 checks against synthetic fixtures built
  from real ids (3068/3389/3605).
- **`pipeline/audit_thread_coverage.py`** — Hebrew fork of
  `Projects/Matthew/pipeline/audit_thread_coverage.py`, rewritten for the
  id-based design: set arithmetic over word ids, not stem matching.
  - **Source side**: for a root, every non-Ketiv word in
    `Joshua-words.tsv` whose lemma has a bare id in the root's set — one
    hit per word id (§6: Beth-el is two tagged words sharing one id,
    counted as two occurrences by design).
  - **Fragment side**: `data-root`/`data-w` parsed from built unit HTML.
  - **Report**: **gap** (source id in-range, untagged), **wrong** (tagged
    id whose lemma isn't in the root's set), **stray** (tagged id out of
    range or nonexistent), plus a hard `missing_data_w` count for any
    tracked-thread span lacking the attribute at all. Local roots keep a
    per-verse informational view (`tagged_map`), since they have no id
    set to audit against.
  - **Ketiv/Qere (§A4)**: the artifact tags the Qere id, this audit
    counts it. `load_words()` drops Ketiv rows, detected by adjacency
    (same ref, an unpointed row immediately followed by a pointed one) —
    verified against the whole corpus to find exactly the documented 32
    pairs and zero exceptions.
  - Source filename and line-ref prefix are still read from
    `data/units.json`'s `book` field, self-checked against the file's own
    first line.
  - `--ids <root>` (was `--forms`) lists every surface form + ref a
    root's id set pulls in, counted by word id — the review step before
    Lane commits an id set to `data/roots.json`.
- **`pipeline/verify_thread_coverage.py`** — written *before* any thread
  generator exists for this project. Independently re-derives source-id
  matching (own Ketiv detection, own bare-id parser, `csv.reader` not
  `DictReader`, no import of `roots.py`'s or `audit_thread_coverage.py`'s
  matching functions), cross-checked against the real implementation.
  Retired the final-letter-fold and kol/Caleb stem-over-match checks
  (neither applies to id-based matching); replaced with a live regression
  pulled from the TSV at check time (`{3605}`'s hit count never exceeds
  the raw row count, never includes Caleb's `3612`). Five synthetic
  fragment fixtures, from real word ids, one per required failure shape:
  gap, wrong-lemma id, missing data-w, stray-outside-passage, nonexistent
  id.
- `pipeline/thread-stems.json` (the substring-stem spec file) is
  **deleted** (§A8) — nothing reads it anymore.
- `data/units.json` holds the real 24-unit / 4-movement registry (Phase
  1, transcribed from `joshua_literary_unit_map.md`), every row
  `built: false` — no units built yet. `data/threads.json` still holds no
  real threads — empty scaffolding so the audit and verify scripts are
  runnable today, not fabricated content.

## Fragment metadata / validation (no units built yet)

`pipeline/unit_meta.py` — Hebrew fork of
`Projects/Matthew/pipeline/unit_meta.py`: parse/strip/inject/generate for
the per-fragment `<script id="unit-meta">` JSON block, plus `validate()`
and `validate_fragment()`. Reworked in Phase 0.6 to match
`joshua_study_style_reference.md` (§3, §4, §7) exactly — this fork had
drifted from it on several points before the rework closed them:

- **`ALLOWED_TOP_LEVEL_KEYS`** = `unit, slug, passage, title, movement,
  roots, threads` — the complete, closed set (style reference §3's
  table). `descriptor`/`discourse` are **not** in it anymore (Matthew
  shipped them as documented-but-silently-dropped fields across eleven
  units before it added this check at all). Being in the set only means
  `validate()` won't reject the key — `generate()` still has to be taught
  to round-trip it separately, or it's dropped on regen.
- **`threads` requires all four sub-keys** (`opens`, `payoffs`,
  `candidates`, `retro`), each a list, empty lists fine — not just
  type-checked when present. `opens`/`payoffs` entries require a `note`
  (checklist 4, the popover prose for that beat).
- **`threads.candidates[]`** is `{root, why, ids?, refs?}` — `why` is
  required; `ids` must match `^\d+[a-z]?$`, `refs` must match `C:V`.
  `stems`/`exclude` (this fork's old, pre-style-reference shape) are now
  a hard rejection.
- **`roots[]`** rejects `color`/`colour` (the site assigns colours) and
  `kind`/`members` (that taxonomy was tried and reverted, style reference
  §1) — every entry is `{root, translit, gloss}`, nothing more.
- **Component whitelist** (`check_component_whitelist`): every `class=`
  used in a fragment must be defined in `css/styles.css` (grep-diff, not
  a full CSS parse), and `REQUIRED_COMPONENT_CLASSES` (`block`, `legend`
  — the legend is `section.block.legend`, both tokens required) must
  actually appear. `css/styles.css` now carries the real style-reference
  component vocabulary (`mast`, `kicker`, `pericope`, `block`, `v`/`n`,
  `r`/`rl`, `gloss`, `compare`, `en`) rather than a Matthew-mirrored
  placeholder set — `echo` deliberately left out until unit 1 decides it
  wants it (style reference §4).
- **Endnote integrity** (`check_endnote_integrity`): every `id="…n<N>"`
  and `href="#…n<N>"` in a fragment must pair up exactly.
- **Zero native Hebrew script** (`check_no_hebrew_script`): the whole
  Hebrew Unicode block (U+0590–U+05FF), anywhere in a fragment, **no
  exceptions, attribute values included** (checklist 12). This fork used
  to exempt `threads.candidates[].stems` — that field doesn't exist in
  the schema anymore (candidates carry `ids`/`refs` now), and the
  exemption contradicted checklist 12 regardless, so it's gone.
- **Four newer fragment checks**, all hard failures folded into
  `validate_fragment()`: `check_data_root_resolves` (every `data-root`
  must resolve to a `threads.json` thread's root or this fragment's own
  `roots[]`, checklist 6), `check_tracked_spans_have_data_w` (every
  tracked-thread span must carry `data-w`, checklist 7),
  `check_pericope_headings` (every `h3.pericope` must carry its `· C:V`
  range, checklist 9), `check_no_inline_style` (no inline `style=`, no
  `--c-*` colour vars, checklist 13).
- **`warnings_for_fragment()`** — a separate, non-fatal channel, kept
  structurally distinct from `validate_fragment()`'s hard errors:
  `class="rl"` inside a `.v` verse block (style reference §4: valid
  outside verse blocks, inside one it's counted anyway so it only
  mislabels intent — a warning, not a build failure).
- `pipeline/test_unit_meta.py`: 43 checks against synthetic fragment
  fixtures, plus one **acceptance test** that pulls the style reference's
  §8 worked example straight out of the file at test time (regex-
  extracted, never copied) and runs it through `validate()` +
  `validate_fragment()` against a synthetic `devote`/`give` threads.json
  fixture — passes clean. This is the contract between the style
  reference and the validator; if either drifts, it fails.
- **`threads.retro`'s `w` field** (Phase 3): a retro entry whose `op` is
  `add`/`retag`/`retag_word` and whose target root is a tracked thread
  must carry `w` (an OSHB word id) — that op creates or repoints a
  `data-root` span, and a tracked-thread span needs `data-w` same as any
  other (checklist 7). Local-root retro fixes need no `w`. Found and fixed
  while building the porter: the style reference's own §8 worked example
  had a retro entry missing both a correct verse number and a `w` — now
  fixed (verse 13 → 14, `w: "06UrB"`), along with two other wrong word ids
  the same example had (`06Qzf` was actually "unto" at 1:1, not "devoted"
  or "given" at 6:2/6:17 — now `068w5` and `06Fu4`).

## Porting a unit (Phase 3 — no units built yet)

Once a research artifact is saved as `source-artifacts/joshua_NN_translation.html`
(style reference §7's checklist, last step):

    python pipeline/port_artifact.py 6              # port it
    python pipeline/port_artifact.py 6 --dry        # preview, write nothing
    python pipeline/port_artifact.py 6 --src X.html  # dry-run against a practice file

`pipeline/port_artifact.py` — ported from `Projects/Matthew/pipeline/
port_artifact.py`, **deliberately slimmer**, not a straight port:

- **`extract_units.py`'s whole cleanup pipeline does not port.** Matthew's
  version existed to clean up older-format artifacts (Greek-title parsing,
  script stripping, local-palette extraction, verse/block normalization).
  Joshua's `source-artifacts/` arrive in the style-reference fragment
  shape from unit 1 (checklist 1: one `<article>`, nothing above or
  below) — there is nothing there to clean up. `to_fragment()` only
  strips any existing meta block and prefixes endnote ids
  (`id="n1"` → `id="u06-n1"`, keeps ids unique once every unit's fragment
  shares one page) — a 20-line function, not a 400-line module.
- **No `--backfill`.** Matthew's backfilled eight pre-existing units into
  the new contract. No such units exist here.
- **The colour/hue-assignment system does not port.** Matthew's `WELL`
  palette + `assign_hues()` + perceptual-distance collision avoidance
  needs real hex colours to avoid colliding with, and none are assigned
  in this project yet (deferred to Phase 4's design pass). Local
  (non-tracked) roots are merged into `data/units.json` as
  `{translit, gloss}` only — no `color` key — until then.
- **The new-thread candidate preview uses ids, not stems.** Matthew's
  version ran a candidate's proposed Hebrew stems against the Greek text.
  Joshua's `_append_candidate_preview()` runs the candidate's proposed
  `ids` through `audit_thread_coverage.source_hits_for_root()` instead —
  the same id-set matching the real coverage audit uses, so the preview
  and the eventual audit can't disagree.
- **Coverage reporting uses gap/wrong/stray/missing-data-w**, not
  Matthew's gap/over — matches `audit_thread_coverage.coverage_for_fragment()`'s
  Phase 0.6 shape.
- **Fragment-level findings (`unit_meta.validate_fragment()`) are
  reported, not a hard gate** — the port still writes the fragment for
  review in the browser; only `unit_meta.validate()` on the meta dict
  blocks the write (a malformed meta block can't even be merged into
  `units.json`/thread bookkeeping). Matthew's own `_append_structure` used
  the same "warn, still write" philosophy for its narrower set of checks.
- Retro-fix merging (`merge_retro`) is otherwise unchanged from Matthew's
  pattern: each `threads.retro` entry is dry-checked against its target
  fragment via `apply_retrofit.FNS[op]` before being merged into the
  generated `pipeline/retro-tags.json` (kept separate from the
  hand-authored `pipeline/retrofit-tags.json`, same split as Matthew).

`pipeline/apply_retrofit.py` — genuinely language-neutral (Port
analysis.md §1.3), ports with one real addition: `add` and `retag` accept
an optional `"w"` field and inject/update `data-w` on the span they
produce, since Joshua's tracked-thread spans need one and Matthew's never
did. `retag_word` (a whole-unit regex sweep over multiple spans at once)
deliberately does **not** accept `w` — a bulk reclassification changes
which root a span belongs to, not which word it points at, so whatever
`data-w` a matched span already carries is left untouched.

`pipeline/scan_occurrences.py` ports unchanged (pure generic-markup
logic, reads only English gloss text and `data-root` spans).

`pipeline/verify_occurrences.py` is **narrower than Matthew's**, not a
straight port: the count-mismatch re-derivation (independent
line-oriented tokeniser, not `scan_occurrences`' regex) and the
`threads.json` `tagged`-flag sanity check port as-is, but Matthew's
"every `data-root` resolves to a colour" and perceptual-colour-distance
collision checks are **dropped**, not adapted — `unit_meta.
check_data_root_resolves()` already does the resolution check, more
rigorously, as part of `validate_fragment()` on every build, and the
collision check needs real colour values that don't exist until Phase 4.
Re-checking mere resolution here would be exactly the kind of redundant
porting this rework is trying not to do.

`pipeline/refresh_meta.py` and `pipeline/build.py` port essentially
unchanged (pure generic orchestration) — `build.py`'s step list gets one
new step Matthew never needed: `pipeline/roots.py`, validating
`data/roots.json` integrity (every id resolves to a real lemma, no id
claimed by two roots, every tracked thread's root has an entry) between
`verify_occurrences.py` and `threads_digest.py`.

Tests: `pipeline/test_apply_retrofit.py` (21 — includes `retag`'s `occ`
param, added while retrofitting unit 1's newly-tracked roots, see below),
`pipeline/test_scan_occurrences.py` (4), `pipeline/test_verify_occurrences.py`
(5), and `pipeline/test_port_artifact.py` — a full end-to-end run of
`port_artifact.py` against a scratch copy of `data/`/`units/`/`pipeline/
out` (never the real registry), using the style reference's own §8 worked
example as the incoming artifact: dry-run, real port, fragment
validation, retro-merge onto an earlier unit, tracked roots produce no
local-roots entry, a genuinely local root gets a hue from `port_artifact.
py`'s `WELL` (Phase 4), and thread-delta report content (candidate
preview, real tracked-thread coverage gaps against the worked example's
deliberately-partial 2-verse excerpt, the merged retro fix) — 9 checks,
all passing on the real logic paths
(the subprocess-based `apply_retrofit`/`scan_occurrences`/
`verify_occurrences` step is stubbed out, since a real subprocess would
re-import those modules fresh and use their own path globals, not this
test's monkeypatched scratch ones — those three steps have their own
tests that exercise the real subprocess-free logic directly). Found while
building unit 1: `pipeline/roots.py`'s `load_roots()` used to bind its
default `path=ROOTS_JSON` at import time, so a test's `roots.ROOTS_JSON =
<scratch path>` monkeypatch was silently ignored on any no-arg call —
harmless while the real `data/roots.json` was empty (both looked like "no
entry"), but it would have masked real coverage-checking forever. Fixed
to resolve the default at call time.

### Thread promotion: book-wide vs. local (2026-09-16, Lane)

Every unit's artifact arrives with a `threads.candidates[]` list — each
one a **root that could go either way**: promoted to a tracked thread
(`data/roots.json` + `data/threads.json`, coloured and audited book-wide)
or left as a merely-local root (per-unit colour and gloss only, in
`units.json`, no id set, no cross-unit coverage guarantee). Lane's call:
**Claude decides this, not Lane** — biased toward book-wide, since a
thread kept local that turns out to have a real payoff later is a worse
outcome than one tracked book-wide that never pays off. Claude asks Lane
only when genuinely unsure (unit 1's example: `kol` "all," 236 book-wide
occurrences, flagged by the candidate's own `why` note as "probably too
frequent to colour usefully" — asked, kept local).

Promoting a candidate is not just a `data/roots.json`/`threads.json`
edit — it changes the coverage-audit contract for that root from
"informational, counted per verse" to "every occurrence in every built
unit's passage must carry `data-w`" (`audit_thread_coverage.py`'s
COVERAGE POLICY). An artifact written while a root was still expected to
stay local will usually already have every occurrence *wrapped* in a
span (the researcher tags what they notice), just without `data-w` (no
reason to look up a word id for a root that was never going to be
audited) — so promoting it after the fact is normally a `retrofit-tags.json`
`retag` pass (inject `data-w` into existing spans, one entry per
occurrence, cross-checked against `Joshua-words.tsv`), not new `add`
tagging. Watch for one English span covering what should be two separate
Hebrew occurrences, or two English spans covering one Hebrew occurrence
(unit 1: Hiphil *yaniaḥ* "gives ... rest" split across two words) — the
second case needs the secondary span demoted to `class="rl"` (`unwrap` +
`add` with `cls: "rl"`), since `rl` is what `audit_thread_coverage.py`
deliberately excludes from the count (its `SPAN_ATTRS` regex only matches
`class="r"`). Re-run `pipeline/audit_thread_coverage.py` after any
promotion-driven retrofit and confirm every promoted root reports clean
before committing.

**The retrofit recipe** (mechanical steps, not judgment calls — do this
per promoted root, per unit):

1. Pull every occurrence of the root's id(s) within the unit's chapter(s)
   straight from `Joshua-words.tsv`, in document order: filter rows whose
   `ref` falls in the unit's passage, split each `lemma` on `/`, keep
   digit-leading segments, bare them (`pipeline/roots.py`'s `bare_id()`),
   and match against the id set. Keep `(ref, word_id, surface, morph)` —
   this is the ground truth the fragment must match, not a re-derivation
   from English.
2. Pull every existing `<span class="r" data-root="ROOT">TEXT</span>` for
   that root out of the built unit's fragment, verse by verse, in
   document order.
3. Match the two lists 1:1 **in order, per verse** — the translation
   follows Hebrew word order closely enough that this works far more
   often than not. Where the counts match verse-by-verse, this is a
   straight ordered zip: occurrence *N* in the Hebrew list is span *N* in
   the English list.
4. Where a verse's counts *don't* match, that's the signal to look closer
   (not a bug to route around): one span wrapping two Hebrew words (write
   it as one `retag` covering both, or split the span by hand if the
   distinction matters to the thread), or one Hebrew word rendered as two
   English spans (demote the extra one to `class="rl"` per above), or a
   genuinely untagged occurrence (a real `add`, not `retag` — rare, since
   most candidates arrive already wrapped, see above).
5. Same root + same English text twice in one verse (e.g. "possess ...
   possess") needs `retag`'s `occ` (1-based, left to right) to tell the
   two spans apart — a bare text match can't.
6. Write one `retag` entry per matched occurrence: `{"unit", "verse",
   "from": root, "to": root, "text", "w": word_id}` (`occ` only when
   needed per #5). Batch them into `pipeline/retrofit-tags.json`.
7. Re-run `python pipeline/port_artifact.py N`, then
   `python pipeline/audit_thread_coverage.py` — expect every promoted
   root to report `clean`, 0 gap/wrong-id/stray/missing-data-w. Any
   remainder means a step-4 case was missed; don't hand-wave a nonzero
   count.

## The app shell (Phase 4)

`index.html` + `app/*.js` + `css/styles.css`, forked from `Projects/
Matthew/{index.html,app/*.js,css/styles.css}` per `phase-4-5-plan.md`'s §B
measurement (true "wholesale portable" only for part of it). Decisions
from Lane going in (§A): no discourse-equivalent overlay (movements only —
Joshua's literary unit map has no documented sub-movement grouping), root
colours assigned now rather than deferred to Phase 5, and a Matthew-style
rich book map (not a plain chip list).

- **`app/threads.js`** — ported unchanged. Entirely data-driven off
  `data/threads.json` + `units.json` roots + `data/occurrences.json`, no
  Matthew-specific logic anywhere in it.
- **`app/search.js`** — ported near-unchanged. `fold()`'s `NFD` +
  combining-mark strip is already diacritic-generic, so it works for
  `ḥerem`/`naḥalah` the same way it worked for `aphiēmi`. Only the
  storage key (`joshua.search.q`) and hint text/examples changed.
- **`app/spotlight.js`** — trimmed, not just adapted. Matthew's version
  handles three aside kinds (`.gloss`, `.compare`, `aside.synoptic`);
  Joshua has only `.gloss` (Phase 2: no compare box; `aside.echo` is
  optional and unbuilt, style reference §4) — the `.compare`/`synoptic`
  code paths are deleted, not disabled.
- **`app/main.js`** — the one real rework. `discourseOf()`, the
  discourse-bracket half of `buildBookMap()`, and the discourse half of
  `renderPlacement()` are dropped (§A1: no discourse layer). Reads
  `movements[]` as `{n, name, span, units}` — `data/units.json`'s own
  Phase 1 shape — instead of Matthew's `{id, label}`; `unitsByMovement()`/
  `buildBookMap()`/`renderPlacement()` all read `m.n`/`m.name` accordingly,
  so there's exactly one movement-shape convention live in the codebase,
  not two. `normalizeSectionHeadings()` is dropped entirely (not just
  simplified) — it exists in Matthew to clean up legacy pre-contract
  heading markup from artifacts migrated before the style reference
  existed; Joshua's artifacts arrive in the `h3.pericope` shape from unit
  1, so there is nothing for it to normalize. **A real behavioral bug
  caught while porting, not just adapting cosmetically:** `hoistStructure
  Blocks()` in Matthew skips only `section.block.legend` when hoisting
  structural blocks to the top of a unit — safe there because Matthew's
  endnotes are a bare `.notes` section, not `.block`. Joshua's endnotes
  are `<section class="block notes">` (style reference §4) — carrying
  `block` too — so a naive unchanged port would have hoisted every unit's
  endnotes to the top, above the translation. Fixed by also skipping
  `.notes` in the hoist loop.
- **`css/styles.css`** — the real design pass (previously a class-name-only
  scaffold). Deliberately **not** Matthew's parchment/illuminated-
  manuscript palette (crimson + gold on cream, Cormorant Garamond display
  type) — Lane's call: an Old Testament / conquest-narrative theme,
  "similar but unique." Sun-bleached wilderness ground (`--bg`), clay/
  terracotta for verse numbers and endnote markers (`--accent-clay`,
  replacing Matthew's crimson), bronze for pericope headings and active
  chrome (`--accent-bronze`, replacing gold), Jordan-valley teal-indigo for
  movement-placement text (`--accent-jordan`, new — Matthew has no
  equivalent slot). Display type is **Cinzel** (carved-inscription
  capitals) in place of Cormorant Garamond; body serif is **Frank Ruhl
  Libre** in place of EB Garamond. Component vocabulary matches the style
  reference's §4 exactly (`mast`, `kicker`, `pericope`, `block`,
  `block.legend`, `block.notes`, `v`, `n`, `r`, `rl`, `gloss`, `en`); `.
  compare` is removed from the whitelist rather than kept unused (Phase 2:
  no compare box), and Matthew-only content components with no Joshua
  analogue (`.structure`/`.frame`/`.triads`/`.mirror`/`.gem` — the
  genealogy box, `.prayer`, `.itin`, `table.exod` — none in Joshua's
  component table) are not ported at all.
- **`pipeline/port_artifact.py`**'s hue-assignment system (`WELL`,
  `assign_hues()`, `_lab`/`_de` perceptual-distance collision avoidance)
  ported near-verbatim from Matthew, with Joshua's **own** `WELL` — a
  distinct desert/Jordan-valley set of ~20 hues, not Matthew's crimson-and-
  gold-leaning one, sharing none of its hex values. `merge_units_json()`
  now assigns a genuinely local (non-tracked) root a colour from this well,
  avoiding collisions with the unit's own existing local hues and with the
  global colour of every tracked thread the unit also uses — same
  algorithm Matthew uses, ported once colour timing was decided (Lane:
  assign now, not at Phase 5). A tracked thread's colour still lives only
  in `data/threads.json`, Lane's hand-authored policy file; nothing here
  writes it.

Smoke-tested in a real browser against the still-empty `data/*.json`: nav
renders 24 unit chips grouped under 4 movements (marked "not yet built"),
the book map renders with roman-numeral movement groups and no discourse
brackets, search renders with the updated hint text and no results, no
console errors, mobile width (375px) unaffected. No unit has been built
yet — that's Phase 5, next.

## Repo layout

```
CLAUDE.md                       this file -- how the repo behaves
PLAN.md                         phase list, open questions, Phase 0.6 rework list
Port analysis.md                Matthew-pipeline port audit (guide, not gospel)
Claude_ai_chat_side_instructions.md research-project operating instructions
joshua_study_style_reference.md the artifact contract -- authoritative over this file
joshua_literary_unit_map.md     24 units / 4 movements, confirmed as-is
translation-choices.md          hand-maintained English-rendering glossary
threads-digest.md               generated from data/threads.json, never hand-edit
resources.md                    MISSING -- referenced by Claude_ai_chat_side_instructions.md, not yet authored
project-side/README.md          index of files that round-trip with the research project
project-side/sync-state.json    fallback hash-diff state for check_project_sync.py
project-side/synced/            auto-generated mirror pushed to GitHub for the project's connector sync -- never hand-edit
Joshua-reading.txt              generated, see "Source data" above
Joshua-words.tsv                generated, see "Source data" above
Joshua-english.txt              generated, see "Source data" above
candidate-boundaries.md         generated, see "Source data" above
pipeline/build_reading.py       Hebrew generator (reading.txt, words.tsv, boundaries.md)
pipeline/build_english.py       English generator (Joshua-english.txt, from WEB USFM)
pipeline/hebrew.py              deterministic Hebrew -> Latin transliteration
pipeline/test_hebrew.py         hebrew.py's regression test -- authoritative scheme definition
pipeline/roots.py               data/roots.json loader/validator (id-set root identity)
pipeline/test_roots.py          roots.py's regression test
pipeline/audit_thread_coverage.py   thread tag-coverage audit -- set arithmetic over word ids
pipeline/verify_thread_coverage.py  its verify step, written ahead of any real thread generator
pipeline/unit_meta.py           fragment metadata parse/validate/generate
pipeline/test_unit_meta.py      unit_meta.py's regression test, incl. the §8 worked-example acceptance test
pipeline/threads_digest.py      data/threads.json -> threads-digest.md generator
pipeline/port_artifact.py       drop a research artifact into the site (Phase 3)
pipeline/apply_retrofit.py      idempotent fragment-edit ops, replayed by build.py
pipeline/retrofit-tags.json     hand-authored fragment edits (empty, no units built yet)
pipeline/retro-tags.json        generated retro fixes, merged by port_artifact.py (not created until a port runs)
pipeline/scan_occurrences.py    units/*.html -> data/occurrences.json
pipeline/verify_occurrences.py  independent count re-derivation + tagged-flag check
pipeline/refresh_meta.py        regenerate every built fragment's meta block
pipeline/build.py               re-derive everything downstream of committed fragments
pipeline/check_project_sync.py  fallback: reports which project-side files need re-pasting
pipeline/sync_to_github.py      primary: mirrors project-side files into project-side/synced/ and pushes
pipeline/test_apply_retrofit.py, test_scan_occurrences.py, test_verify_occurrences.py, test_port_artifact.py
                                 Phase 3 regression tests (test_port_artifact.py is the full end-to-end one)
data/units.json                 real 24-unit / 4-movement registry, no units built yet
data/threads.json               thread registry (empty, no threads defined yet)
data/roots.json                 root registry (empty; id-set-per-slug shape, tracked threads only)
data/occurrences.json           generated by scan_occurrences.py (empty, no units built yet)
index.html                      app shell entry point (Phase 4)
app/main.js                     router, footnote jump/return, book map, pager (Phase 4, no discourse layer)
app/threads.js                  colour resolution + legend, ported unchanged from Matthew
app/search.js                   concordance search, ported near-unchanged from Matthew
app/spotlight.js                per-verse .gloss note toggle, trimmed vs. Matthew (no compare/synoptic)
css/styles.css                  real design pass (Phase 4) -- Joshua's own clay/bronze/Jordan palette, Cinzel + Frank Ruhl Libre
.claude/launch.json             local static-file server config for previewing the app shell
source-artifacts/                incoming research artifacts (joshua_NN_translation.html) -- not created until the first one lands
pipeline/corpus/wlc/            morphhb OSIS XML (pinned)
pipeline/corpus/lexicon/        HebrewLexicon XML (pinned)
pipeline/corpus/web/            WEB USFM source (pinned)
package.json                    records the morphhb pin
```
