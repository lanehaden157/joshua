# Joshua

How this repo behaves. The artifact contract (fragment shape, meta schema,
components, transliteration scheme, checklist) lives in
`joshua_study_style_reference.md` and is authoritative over this file — this
file points there rather than restating it.

**State (2026-09-26):** Phases 0–5 done; units 1–4 built (Movement I complete);
20 tracked threads in `data/threads.json`/`data/roots.json` (every one carries an
`echo`). **Runs on bible-core** since 2026-09-26: vendored `biblecore/`,
pinned in `biblecore/CORE_VERSION` and `book.json` `core` (Lane reversed the
2026-09-22 "not migrating" call). Mechanism lives in core:
`../bible-core/ARCHITECTURE.md`. Fix core bugs in bible-core and re-vendor
(`python ../bible-core/tools/core_sync.py ../Joshua`) rather than editing
`biblecore/` here (`../bible-core/tools/core_diff.py ../Joshua` reports local
edits). `source-artifacts/` is current for all four units: edit there and
re-port rather than editing `units/` by hand. Tracked-thread colours are
assigned algorithmically, same as local roots; hand-pick one only if Lane asks
(Lane, 2026-09-22: eyeballed colours collided).

Other sessions may be editing `../bible-core` or this repo at the same time:
see "Concurrent sessions" in `../bible-core/CLAUDE.md` (check `git status`,
stage explicit paths).

Lane prefers questions (the porter's `questions[]`, wording calls, thread
decisions) as AskUserQuestion multiple-choice popups, best provisional choice
first and marked "(Recommended)", rather than a list in chat.

Everyday commands, from the repo root:

    python -m biblecore port 6            # port source-artifacts/joshua_06_translation.html (--dry, --src X, --force)
    python -m biblecore build             # re-derive everything downstream of the fragments
    python -m biblecore test              # book-side checks: core pin, units, audit, idempotence
    python -m biblecore audit --ids ROOT  # every form/ref an id set pulls in
    python -m biblecore data-w 6          # fill data-w on a built unit by alignment
    python -m biblecore colour ROOT ...   # colours for threads about to be promoted
    python -m biblecore sync              # mirror synced files, commit AND push (run it when Lane OKs the push)

`python -m biblecore` with no command lists the rest.

## Project documents

- **`joshua_study_style_reference.md`** — the artifact contract.
- **`CHAT_SIDE_INSTRUCTIONS.md`** — the Claude.ai project's
  instruction field: Joshua's lens plus its additions to `core-workflow.md`
  (the shared four passes, ledger and standing moves, vendored from core and
  synced). Not in the synced mirror: Lane pastes it by hand. `sync-check`
  says when it's stale; run `sync-check --mark-pasted` after pasting.
- **`book.json`** — the book's core settings (paths, groupings, components,
  sync list). Closed schema: an unknown key is an error.
- **`joshua-literary-unit-map.md`** — 24 units, 4 movements, confirmed.
  Synced to the project (since 2026-09-26).
- **`PLAN.md`** — phase list and open questions.
- **`archive/`** — historical plans and audits (`Port analysis.md`, the
  Matthew-pipeline port audit; `phase-0.6-plan.md`, `phase-4-5-plan.md`,
  `platform-design-review.md`). Reference only; nothing reads them.
- **`translation-choices.md`** — English-rendering glossary. Update in the same
  turn as any wording decision.
- **`project-side/README.md`** — every file that round-trips with the Claude.ai
  project. Check there before hunting for a path.
- **`resources.md`** — Lane-authored inventory of the project's holdings
  (text files, digests, commentaries). Moved into the repo and the synced
  mirror 2026-09-26; before that it lived only in the Claude.ai project.
  Edit it here, not on the project side.

## Source data

- **`Joshua-reading.txt`** — pointed Hebrew, `Josh C:V<TAB>text`. Ketiv/Qere
  pairs use the pointed Qere.
- **`Joshua-words.tsv`** — one row per OSHB `<w>`:
  `word_id\tref\tsurface\tlemma\tmorph`. Ketiv and Qere each get a row, so
  10,083 rows, not 10,051.
- **`Joshua-english.txt`** — WEB classic (`eng-web`, "Yahweh", USA spelling;
  not `eng-webp`/`eng-webbe`), same line shape, footnotes stripped.
  **Role: provenance only** (Lane, 2026-09-19). It is *not* the base text of
  the study translation, not a draft the chat side edits, and not a diff
  target — the style reference is explicit that the verse text is "not a
  polish of an existing English version". Nothing in the build reads it. It
  is synced to the project (since 2026-09-26) as a baseline reference for
  the chat side, which is how `resources.md` describes it.
- **`candidate-boundaries.md`** — every petuhah/setumah marker, uninterpreted.
  Synced (since 2026-09-26); `resources.md` points the chat side to it.
- Generators: `python -m biblecore corpus` (reading, words, boundaries; its
  output was byte-identical to the old `build_reading.py` at the migration)
  and `tools/build_english.py` (Joshua-only; from WEB USFM, asserts the verse
  count matches the Hebrew file).

### Corpus pin

- **morphhb 2.0.2** — `package.json`/lock, `--save-exact`. shasum
  `2ea8c8adc94ff7bd1b3ac3fdbcfd1a489a4c145a` (matches npm registry). Read
  from `node_modules/morphhb/wlc/` (`npm ci` restores it). The committed copy
  of `Josh.xml` was dropped at the migration, after a byte compare.
- **HebrewLexicon @ `21c9add13bc727d3a951361778e97e3ff7afd1ce`** —
  `AugIndex.xml`, `LexicalIndex.xml`, `BrownDriverBriggs.xml`,
  `HebrewStrong.xml` in `corpus/lexicon/`. `HebrewStrong.xml` feeds the
  word glosses the build emits into `data/words/`.
- Both CC BY 4.0.
- **WEB classic** — `https://ebible.org/Scriptures/eng-web_usfm.zip`, book file
  `07-JOSeng-web.usfm`, in `corpus/web/`. Public domain.

### Verification (against printed BHS)

Re-check against the file on disk rather than trusting prior numbers:

- 658 verses; chapter 21 has 45 (21:36–37 present, unmarked).
- 10,083 `<w>`: 10,051 running text + 32 Qere under
  `<note type="variant"><rdg type="x-qere">`.
- 52 petuhah + 42 setumah = 94 breaks.

If a count drifts on re-fetch, flag it loudly — it likely means the corpus is
wrong, but that needs eyes.

## Transliteration — `biblecore/lang/hebrew.py`

Scheme rules: style reference §5. **bible-core's `tests/test_hebrew.py` is the
authoritative definition** (real OSHB word ids, hand-derived expectations,
plus a full-corpus sweep); if prose disagrees, the test wins.

Notes not in the style reference:

- Tsadi is `ts`, shin `sh`, sin `ś`. Morpheme boundaries are hyphenated
  (`ha-melek`, `u-`). Matres: shuruq, holam-male (bare vav + holam is a vowel,
  ~12% of words), hiriq-yod → `i`, tsere-yod → `e`. Furtive patach glides
  before the final guttural.
- Ayin carries a baked-in combining low line (ʿ̲) so it survives TSV/terminal/
  HTML without CSS.
- **Overrides key on lemma id** (3068/3069 → `YHWH`, 3389 → `Yerushalayim`,
  3605 → `kol`), so they apply only via `transliterate_word(surface, lemma,
  morph)` or `transliterate_ref("Josh C:V")`. Bare `transliterate(text)` is
  deterministic-only.

## Roots and thread coverage

A root is a hand-curated set of lemma ids, never a Hebrew string (style
reference §2).

- **`data/roots.json`** — tracked threads only:
  `{"roots": {"<slug>": {"ids": [...], "note": "..."}}}`. Lane's policy.
- A bare id claims every lexeme under a number, a suffixed id claims exactly
  one — so `3885a` *lodge* and `3885b` *murmur* can be separate roots (style
  reference §2 has the three real cases). A suffixed id the corpus never
  carries is an error, since it would match nothing.
- The audit (`biblecore/audit.py`) is set arithmetic over word ids: **gap**,
  **wrong**, **stray**, **missing_data_w**. Only `class="r"` spans count;
  `rl` is excluded. Ketiv rows are dropped by adjacency (exactly 32 pairs).
  Its independent re-derivation (formerly `verify_thread_coverage.py`) is
  bible-core's `tests/test_audit_verify.py`.

### Thread promotion: book-wide vs. local (Lane, 2026-09-16)

The promotion policy is in the style reference §3 (Claude decides, biased
book-wide; ask Lane when genuinely unsure). Unit 1 example: `kol`, 236
occurrences, asked, kept local.

Its colour comes from `python -m biblecore colour ROOT` by default (Lane,
2026-09-22; hand-pick only if Lane asks), checked against every other tracked colour plus every local
root colour on record in `data/units.json`. The well is `data/palette.json`:
65 colours, expanded from 20 on 2026-09-22 by generation, not by eye (muted
Lab-space candidates, filtered for WCAG contrast ≥ 2.8 against `--bg` and
`--panel`, greedily accepted at a minimum CIEDE2000 from every colour already
in). If it runs short again, expand it the same way.

Promotion makes every occurrence in every built unit require `data-w`. Existing
artifacts usually already wrap the occurrences, so it's normally
`python -m biblecore data-w N` (promotes in place), with a
`retrofit/retrofit-tags.json` entry only for what that can't decide.

**Retrofit recipe** (per promoted root, per unit, for the verses `data-w`
reports as undecided):

1. Compare the root's occurrences in `Joshua-words.tsv` for the verse with
   the fragment's `<span class="r" data-root="ROOT">` spans, in order.
2. Where the counts differ, look closer: one span over two Hebrew words
   (one `retag`, or split by hand), one Hebrew word as two spans (keep the
   span a reader recognizes as the root and `unwrap` the other — `rl` still
   picks up the root's colour, so demoting isn't enough; unit 1 v15 tags
   *rest*, not *gives*), or a truly untagged occurrence (`add`).
3. Same root + same text twice in a verse → `retag`'s `occ` (1-based).
4. One entry per occurrence: `{"unit", "verse", "from", "to", "text", "w"}`.
5. Re-run `python -m biblecore build` (it replays the retrofit file and
   audits); every promoted root must report clean. Don't hand-wave a nonzero
   count.

## Canon leads — `python -m biblecore leads`

The mechanical half of the project side's intertext pass (Lane, 2026-09-21):
Claude Code finds where words recur, the project side decides what matters.
Per unit, `canon-leads/canon-leads-unit-NN.md` lists rare words (≤ 20 verses
in the Hebrew Bible by default) and adjacent-lemma phrases shared with the
Torah, each with every hit, transliterated, in English (KJV) verse numbering
(Lane, 2026-09-24). Deliberately narrow: blind to common words, themes,
type-scenes and the New Testament. The build regenerates it for every built
unit plus the next one; `book.json` `sync.globs` syncs it.

Drafting cross-references here from memory is the thing this replaces. The
unit 1–2 echoes were written that way and are provisional until the project
side runs its pass on them.

## Fragment validation and porting

Both are core (`biblecore/meta.py`, `biblecore/port.py`); the rules live in the
style reference and `../bible-core/ARCHITECTURE.md`. Joshua-specific notes:

- The `example` check extracts the style reference's `## 8. Worked example`
  html fence — keep that heading and fence intact.
- The component whitelist reads every `css/*.css` (core's default).
- Core's validator warns about close colours, which Joshua's old pipeline
  never checked. At the migration it flagged `devote`, `servant` and unit 3's
  local `land` sharing `#8a2f3a`; `devote` (`#53350e`) and `land` (`#55642f`)
  were reassigned by the algorithm (Lane, 2026-09-26).
- **Re-porting a built unit needs `--force`.** `7af1a59` (the unit 2 port)
  re-ported unit 1 from a stale source artifact and silently lost four
  local roots, the anonymous-voice notes and the C7 markup. Promoting a
  thread doesn't need a re-port (`data-w N`).
- Endnote ids are prefixed per unit (`n1` → `u06-n1`).
- Retro entries merge into generated `retrofit/retro-tags.json`, separate
  from hand-authored `retrofit/retrofit-tags.json`.
- Each fragment's meta carries `contract` (the core version it conforms
  to); `python -m biblecore migrate` moves built units forward.
- The build also writes `data/canon.json`, `data/components.json`,
  `data/words/`, `data/lemmas.json`, `data/text.json` and
  `data/manifest.json`, for the canon hub and the app's reader features
  (search, interlinear, print).

## App shell

Since core 0.8.5 (Lane, 2026-09-26) Joshua runs bible-core's template app
shell, the same one Numbers runs: `index.html`, `app/*.js`, and
`css/core.css` + `components.css` + `division.css` (generated by
`python -m biblecore assets`) + `theme.css` (Joshua's own overrides). The
old forked shell and `css/styles.css` are in git history (before `82c5b42`).

- Movements come from `data/units.json` `groupings` (kind `movement`).
- Take shell updates from `../bible-core/template/app/`, and bump the
  `?v=` queries in `index.html`/`main.js`/`search.js` with them.
- Preview via `.claude/launch.json` (static file server; routes are
  `#/unit-01`).

## Repo layout

```
CLAUDE.md                        this file
book.json                        core settings for this book
biblecore/                       vendored bible-core (edit in bible-core; CORE_VERSION pins it)
PLAN.md                          phase list, open questions
archive/                         old plans + Port analysis.md (historical, reference only)
CHAT_SIDE_INSTRUCTIONS.md        the project's instruction field (pasted by hand)
core-workflow.md, canon-conventions.md, canon-decisions.md   vendored from core, synced
components-reference.md          generated from book.json components, synced
joshua_study_style_reference.md  the artifact contract (authoritative)
joshua-literary-unit-map.md      24 units / 4 movements
translation-choices.md           English-rendering glossary
threads-digest.md                generated from data/threads.json -- never hand-edit
resources.md                     project holdings inventory (Lane-authored, synced)
project-side/README.md           index of files round-tripping with the research project
project-side/sync-state.json     sync + paste hash state (biblecore sync-check; gitignored)
project-side/synced/             generated mirror for GitHub-connector sync -- never hand-edit
Joshua-reading.txt, Joshua-words.tsv, Joshua-english.txt, candidate-boundaries.md   generated source data
source-artifacts/                incoming research artifacts (joshua_NN_translation.html)
canon-leads/                     generated intertext reading lists, one per unit (synced)
units/                           ported fragments (unit-NN.html)
data/units.json                  24-unit registry + movement groupings
data/threads.json                tracked threads (Lane's policy)
data/roots.json                  tracked-thread id sets (Lane's policy)
data/palette.json                colour well (65, generated)
data/occurrences.json, canon.json, components.json, lemmas.json, text.json, manifest.json, words/   generated by the build
retrofit/retrofit-tags.json      hand-authored fragment edits (retro-tags.json generated)
out/                             port reports (gitignored)
index.html, app/*.js, css/*.css  app shell (core template; theme.css is Joshua's)
.claude/launch.json              local static server for previewing
tools/build_english.py           English generator (Joshua-only)
corpus/{lexicon,web}/            pinned sources (Hebrew comes from node_modules/morphhb)
package.json                     morphhb pin
```
