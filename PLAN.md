# Joshua Study — Build Plan

Phased plan for building the Joshua study as a static site on the same engine
as the Matthew project. Draft for Lane's sign-off; adapted from `Port
analysis.md`'s assessment of what ports unchanged vs. what needs new work —
read that file for the reasoning behind each call below, this is the plan
that follows from it, not a restatement of it.

---

## What exists today

- **`Port analysis.md`** — full audit of the Matthew pipeline against a
  Hebrew/Joshua port: per-file classification (language-neutral / Matthew-
  content / needs new work), a git-archaeology section of what broke and why
  each guardrail exists, and a ranked gap list (§7) of what should exist
  *before* unit 1 rather than be discovered after. Net assessment: **~85%
  of the pipeline is directly reusable** (`unit_meta.py`, `port_artifact.py`'s
  mechanism, `scan_occurrences.py`, `verify_occurrences.py`,
  `refresh_meta.py`, `build.py`, `threads_digest.py`, the entire `/app`
  layer), **~10% needs a new sibling module** (`hebrew.py`, replacing
  `greek.py`'s role), **~5% needs small parameter changes** (the hardcoded
  book prefix/filename in `audit_thread_coverage.py`).
- **`joshua_literary_unit_map.md`** — 24 units across 4 movements, chapters
  1–9 checked directly against the Masoretic petuḥah/setumah breaks,
  10–24 resting on Hawk/Dozeman/Firth's structural outlines. **Confirmed by
  Lane as-is** — units 10–24 don't need another look.
- **`joshua_study_style_reference.md`** and **`Claude_ai_chat_side_instructions.md`** — the
  artifact contract and research-project operating instructions, both
  authored by Lane. These are the authoritative documents for the schema
  and scheme going forward — see "Reconcile against the style reference"
  below for where they supersede work already done this session.
- **`project-side/README.md`** — index of every file that needs to round-
  trip with the Claude.ai research project (paths, direction, update
  cadence), so nothing has to be hunted for turn to turn.
- **The Hebrew/English source data** (done this session, §7 items 1–8 of
  `Port analysis.md`): `Joshua-reading.txt`, `Joshua-words.tsv`,
  `Joshua-english.txt`, `candidate-boundaries.md`, all verified against BHS
  and cross-checked counts. `pipeline/hebrew.py` (the new transliterator,
  tested against real corpus word ids, `pipeline/test_hebrew.py`).
  `pipeline/audit_thread_coverage.py` forked with the final-letter fold,
  per-morpheme matching, and book-field-driven source lookup already fixed
  — not discovered after the fact, per §7 items 1–3, 6. `pipeline/verify_
  thread_coverage.py` written before any thread generator exists (§7 item
  3). `pipeline/unit_meta.py` forked with `validate()` hardened past what
  Matthew shipped with: unknown-top-level-key hard fail, component
  whitelist, endnote link integrity, zero-Hebrew-script policy (§7 items
  4, 5, 7, 8), proven against synthetic fixtures in `pipeline/
  test_unit_meta.py` since no real fragment exists yet to test against.

### Findings carried forward from `Port analysis.md`

1. **The final-letter-form fold** (§7.1) — Hebrew's citation form is the
   one that fails without it (`מֶלֶךְ` melek, singular, final kaf), the
   reverse of Greek's final-sigma problem where the inflected form broke.
   Already fixed in `strip_accents`, verified against real Josh 2:3/2:10.
2. **Prefix-stacking makes `exclude` load-bearing from day one** (§7.2) —
   ו/ה/ל/ב/כ/מ/ש stack on a word's head; `exclude` lists will run longer
   than Greek's did. `--forms` gets run on every stem before commit, not
   just suspicious ones — already demonstrated live on the kol/Caleb
   over-match (251 raw, 236 real).
3. **Verify before generator, not after** (§7.3) — Matthew's worst silent
   bug shipped across seven files before `verify_occurrences.py` existed.
   `verify_thread_coverage.py` exists before the first thread generator
   does, on purpose.
4. **Component whitelist + required-component check** (§7.4) — ten lines,
   catches both an unknown class creeping in and a required one (the
   legend) going missing. Already in `unit_meta.py`.
5. **Kill unconsumed fields before unit 1** (§7.5) — `ALLOWED_TOP_LEVEL_
   KEYS` in `unit_meta.py`'s `validate()` makes an unknown meta-block key
   a hard failure instead of a silent no-op, so a dead field announces
   itself on first use instead of eleven units later.
6. **Book prefix/filename as a parameter, not a hardcoded literal** (§7.6)
   — read from `units.json`'s `book` field, self-checked against the
   source file's own first line. Already done; the *next* fork (Judges)
   is the one this protects.
7. **Endnote link integrity** (§7.7) — `id`/`href` set equality, already
   in `unit_meta.py`.
8. **Attribute-and-text-node script policy, stated explicitly** (§7.8) —
   zero native Hebrew script in a fragment, one named exception
   (`threads.candidates[].stems`, NOT `.exclude`), policy stated in the
   failure message itself.
9. **Genre-shaped components decided up front, not inherited** (§7.9) —
   Matthew's `aside.synoptic` encodes Gospel-parallel comparison, which
   has no Joshua/Judges analogue in the same shape. **Open**: decide
   Joshua's own compare-box shape (if any) before porting `port_artifact.
   py`'s structure-nesting logic, rather than quietly repurposing
   `synoptic` and re-running §3.6's nesting bug.
10. **`translation-choices.md` from unit 1, not unit 10** (§7.10) —
    Matthew's arrived late and cost a retroactive reconciliation pass.
    Seeded now, empty except the divine name (Yahweh — matches `hebrew.
    py`'s `OVERRIDES`) and six open TODO rows (ḥerem, ḥesed, naḥalah,
    goel, nefesh, and the y'all-for-2pl register question) with no
    default filled in.
11. **Session-context files on day one** (§7.11) — `session_index.md`,
    `improvements_log.md` already exist and have been kept current all
    session; this file is the missing third leg.

---

## Design decisions (locked, inherited from Matthew unless noted)

- **Color/thread engine**: unchanged from Matthew — `data-root` resolves
  global (tracked thread, `threads.json`) then local (unit's own palette,
  `units.json`), a root resolving to no color anywhere is a hard verify
  failure. `data/roots.json` is new for this project (Matthew has no
  equivalent — roots live inline per-unit). Shape as of Phase 0.6: a
  hand-curated **set of Strong's/lemma ids** per root, with a note (§2) —
  id-based, not string-based, for the same reason the matching engine
  moved to ids (weak-root substring matching measured badly). Flat,
  non-taxonomic — Matthew built and reverted a richer `kind`/`members`
  taxonomy the same day it shipped (§3.5); not repeating that here either.
- **Transliteration only, no native script** — inherited policy, now a
  machine-checked one (`unit_meta.py`'s `check_no_hebrew_script`), not
  just a stated convention.
- **RTL/bidi**: not needed under the above policy. `css/styles.css` has
  zero RTL support today (Latin-only fonts, no `dir=`/`unicode-bidi`) —
  fine as long as the no-native-script policy holds; flagged as a real gap
  only if that policy is ever relaxed.
- **Book-agnostic where cheap** — continues Matthew's own stated goal
  (confirmed met there: no hardcoded `28`/`"Matthew"` in the orchestration
  layer). Joshua is itself meant to fork cleanly to Judges next.

---

## Phases

### Phase 0 — Corpus + transliteration + guardrails ✅ DONE

Covered above under "What exists today" / "Findings carried forward."
`Joshua-reading.txt`, `Joshua-words.tsv`, `Joshua-english.txt`,
`candidate-boundaries.md`, `pipeline/hebrew.py` + tests, `pipeline/
audit_thread_coverage.py` + `verify_thread_coverage.py`, `pipeline/
unit_meta.py` + tests, `css/styles.css` (starter scaffold), `data/units.json`
/ `data/threads.json` (empty scaffolding, runnable today).

### Phase 0.5 — Session-context + policy files ✅ DONE

`PLAN.md` (this file), `data/roots.json` (seeded flat this session; the
id-set shape landed in Phase 0.6), `translation-choices.md` seeded,
`pipeline/threads_digest.py` ported and run once against the empty
`threads.json` to prove the round trip works end to end before unit 1.
`project-side/README.md` index created; `Claude_ai_chat_side_instructions.md` and
`joshua_study_style_reference.md` landed from Lane.

### Phase 0.6 — Reconcile against the style reference ✅ DONE (2026-09-14)

**Execution plan: [`phase-0.6-plan.md`](phase-0.6-plan.md)** — self-contained,
written to be pasted into a fresh session. The list below is the summary;
the plan file has the measured current output by word id, the decisions
got from Lane, ordering, and done criteria (all met — see
`improvements_log.md`'s 2026-09-14 parts 8–10 for the full record).

**§A decisions, as answered:**

1. Tsadi → `ts` digraph (not `ṣ`) — matches how shin was already handled.
2. Morpheme boundaries → hyphenated (`ha-melek`, `u-`), not joined solid.
3. Aleph/ayin → kept the combining-underline convention on ayin (ʿ̲).
4. Ketiv/Qere → the Qere id is what an artifact tags and the audit counts.
5. One id in two roots → hard fail.
6. `data/roots.json` → tracked threads only; local roots stay in a unit's
   own `unit-meta` `roots[]`.
7. Override API → `transliterate_word(surface, lemma, morph)` +
   `transliterate_ref("Josh C:V")`, plus a no-override bare
   `transliterate(text)` fallback.
8. `pipeline/thread-stems.json` → deleted (not archived).

`joshua_study_style_reference.md` was written after (and independently of)
most of Phase 0's engineering, and it superseded several concrete
decisions already made — not just extended them. This phase's rework, all
landed:

1. **Root/thread matching → id-based, not substring-stem.** `data/roots.json`
   now holds hand-curated Strong's-id sets per root; every tracked-thread
   span carries `data-w`; `audit_thread_coverage.py` does set arithmetic.
   `pipeline/thread-stems.json` is deleted. `unit_meta.py`'s
   `threads.candidates[]` is now `{root, why, ids?, refs?}`.
2. **`pipeline/hebrew.py` scheme corrections** — no spirantization, real
   sheva na/nach + dagesh-forte doubling, hiriq-yod and tsere-yod matres,
   furtive patach, lemma-keyed overrides (bare `YHWH`, not `Yahweh` —
   that stays a `translation-choices.md` rendering decision), tsadi as
   `ts`, sin as `ś`. Full detail in `CLAUDE.md`'s Transliteration section;
   `pipeline/test_hebrew.py` is still the scheme's authoritative
   definition, rebuilt with every expected value hand-derived from real
   word codepoints.
3. **`unit_meta.py`** reworked to match the style reference's §3/§4/§7
   exactly — see `CLAUDE.md`'s Fragment metadata section for the full
   list of hardened checks, including a new acceptance test that
   validates the style reference's own §8 worked example.

See `improvements_log.md`'s 2026-09-14 parts 8–10 for the session-by-
session record, and `CLAUDE.md` for how the reworked pipeline behaves now.

### Phase 1 — Populate `units.json` from the Literary Unit Map ✅ DONE (2026-09-15)

`joshua_literary_unit_map.md`'s 24 units / 4 movements transcribed into
`data/units.json` rows (`n`, `slug`, `passage`, `title`, `movement`,
`built: false`), plus a `movements[]` array (name/span/unit-list per
movement). Verified against the pipeline, not just by eye: every
`passage` string round-trips through `audit_thread_coverage.parse_range()`
to the exact chapter:verse bounds the map states (including both
off-grid breaks — unit 8's 8:30–9:2, unit 24's 24:29–33), and every unit
number round-trips through `unit_meta.generate()` + `validate()` clean.
That check caught a real bug in `generate()` (missing `threads.retro`),
fixed along with it.

### Phase 2 — Cross-book echo component ✅ RESOLVED

No Matthew-style compare/translation-comparison box (Lane's call). The
style reference already designs the Joshua-appropriate alternative:
`aside.echo` (§4) — a narrower, optional component for a real intertextual
echo (a Deuteronomy command answered by a Joshua fulfillment, the
conquest-summary tension with Judges 1), shipped only if unit 1 actually
wants it, with its own nesting-depth check shipped in the same commit —
explicitly *not* inheriting Matthew's `aside.synoptic` and its markup-
specific nesting check (§3.6's bug).

### Phase 3 — Port the reusable ~85% ✅ DONE (2026-09-15)

Turned out to be less "port unchanged" than `Port analysis.md` §1.8
expected, and that was the right call, not a shortcut — see `CLAUDE.md`'s
"Porting a unit" section for the full reasoning per file. Summary:
`apply_retrofit.py`, `scan_occurrences.py`, `refresh_meta.py`, `build.py`
ported close to unchanged (genuinely generic markup/schema logic).
`port_artifact.py` ported deliberately **slimmer** than Matthew's — no
`extract_units.py` cleanup pipeline (nothing to clean up in artifacts
that already arrive in the style-reference shape), no `--backfill`, no
hue-assignment system (colour is Phase 4's job), candidate preview now
runs on `ids` through `audit_thread_coverage.py` instead of Hebrew stems.
`verify_occurrences.py` ported **narrower** than Matthew's — its colour-
resolution and collision checks are dropped, not adapted, since
`unit_meta.check_data_root_resolves()` already does the resolution check
more rigorously and collision-checking needs colour values that don't
exist yet. `build.py` gained one step Matthew never needed:
`pipeline/roots.py` (id-set integrity).

Also added while building the porter: `threads.retro` entries now carry
an optional `w` (OSHB word id), required when the entry adds/retags onto
a tracked thread (checklist 7) — a real schema gap the porter's own
retro-merge logic surfaced. Fixed while there: the style reference's own
§8 worked example had three wrong details (two mismatched word ids, one
wrong verse number) that a stricter check would have caught earlier;
fixed all three.

Full end-to-end test (`pipeline/test_port_artifact.py`) runs the real
porter against a scratch copy of `data/`/`units/`, using the style
reference's own §8 worked example as the incoming artifact — dry-run,
real port, fragment validation, a retro fix merged onto an earlier unit,
local-roots-get-no-colour, and thread-delta report content. All passing,
first real attempt.

### Phase 4 — The app shell ✅ DONE (2026-09-15)

**Execution plan: [`phase-4-5-plan.md`](phase-4-5-plan.md)** — the §A
decisions Lane gave before B started: no discourse-equivalent overlay
(movements only), colours assigned now rather than deferred to Phase 5,
and a Matthew-style rich book map (not a plain chip list). Also asked
mid-session and folded in: a distinct Old-Testament/conquest theme
("similar but unique" to Matthew's Gospel-manuscript look), not a
recolour of the same design.

`index.html` + `app/*.js` ported per `phase-4-5-plan.md`'s §B measurement
— `threads.js` unchanged, `search.js` near-unchanged (hint text only),
`spotlight.js` trimmed to the `.gloss` path only (no compare/synoptic),
`main.js` reworked (no discourse code at all, `movements[]` read as
`{n, name, span, units}` not Matthew's `{id, label}`). One real bug caught
while porting, not just adapting: Matthew's `hoistStructureBlocks()` skips
only `.legend` when moving structural blocks to the top of a unit, safe
there because Matthew's endnotes are a bare `.notes` section; Joshua's are
`<section class="block notes">` (style reference §4), so an unchanged port
would have hoisted every unit's endnotes above the translation — fixed by
also skipping `.notes`. `css/styles.css` got its real design pass: Joshua's
own clay/bronze/Jordan-valley palette and Cinzel + Frank Ruhl Libre type,
not Matthew's crimson/gold parchment look. `pipeline/port_artifact.py`
gained Matthew's hue-assignment system (`WELL`/`assign_hues`/perceptual-
distance collision avoidance), ported with Joshua's own distinct `WELL`
palette, now assigning genuinely local (non-tracked) roots a real colour
on port instead of deferring it. Full detail in `CLAUDE.md`'s "The app
shell" section.

Smoke-tested in a real browser against the still-empty `data/*.json`: 24
unit chips under 4 movements, book map with roman-numeral movement groups
and no discourse brackets, search page renders with no results, no console
errors, works at 375px mobile width. Every `pipeline/test_*.py` and
`pipeline/build.py` re-verified clean before and after — this phase didn't
touch pipeline *logic*, only `port_artifact.py`'s colour assignment
(covered by a new, currently-passing regression test).

### Phase 5 — Unit 1 ✅ DONE (2026-09-17)

*Rights of Passage* (1:1–18) built and live (`345cb5f`). What it changed:

- **Threads:** 10 tracked threads/roots. `cross` is one root over both
  *ʿavar*/*ʿever* ids; `inherit` includes 5159 alongside 5157. Promotion is
  now Claude's call, biased book-wide (`4d856c7`), with a documented
  retrofit recipe (`3f5e287`).
- **Contract changes from review (`a290044`):** no stem/part-of-speech
  labels in glosses; endnote markers at verse end, not inside `.gloss`;
  no named commentators or repo references in fragment prose; optional
  `example` field; tag notable local words (*insight*, *murmur*,
  *shatter*, *valor*).
- **Fixes:** manual `?v=N` cache-buster on app module imports (GitHub
  Pages caching); v15 tags only *rest*, with *gives* untagged, since `rl`
  still shows the root's colour (`a3d3532`, `b5bcee5`).
- **Docs trimmed (2026-09-17):** style reference, chat-side instructions,
  and CLAUDE.md roughly halved or more, no rules dropped.

### Phase 6 — Units 2–24

Build units in order through the same loop: `build.py` has the unit's
canon-leads sheet waiting → research artifact (Claude.ai, four passes, pass 3
the intertext ledger) → `port_artifact.py` → thread promotion + retrofit →
browser review → commit + sync.

**To do: units 1–2 through the intertext pass.** Their echoes and
cross-reference asides were drafted in Claude Code from memory (2026-09-21)
and are provisional. The project side runs pass 3 against each shipped unit
and delivers a revised artifact; re-port with `port_artifact.py N --force`. Revisit per unit whether anything from Matthew's
later phases (concordance/dashboard, persistence, author ergonomics) has
become worth building.

---

## Open questions for Lane

None open.
