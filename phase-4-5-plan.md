# Phase 4 + 5: the app shell, then Unit 1

Paste this into a fresh session. It stands on its own.

## Read first, in this order

1. **`CLAUDE.md`** — how the repo behaves today. Phases 0 through 3 are done;
   this file describes the pipeline as it currently exists.
2. **`PLAN.md`** — phase list. Phase 4 and Phase 5's current (thin)
   descriptions are what this plan replaces. Phase 2 is already resolved
   (no Matthew-style compare box; `aside.echo` instead, only if unit 1
   wants it).
3. **`joshua_study_style_reference.md`** §4 (components) and §8 (the worked
   example) — the artifact contract the app shell has to render correctly.
4. **`joshua_literary_unit_map.md`** — 24 units, 4 movements, confirmed
   as-is. No discourse-equivalent structure exists in Joshua's own
   document (see §A1 below).
5. **`Port analysis.md`** §1.11 — the original assessment that the app
   shell is "essentially wholesale portable from Matthew." Section B below
   is a re-measurement of that claim against the actual files; it's true
   for some files and not others.
6. **`data/units.json`**, **`data/threads.json`**, **`data/roots.json`**,
   **`data/occurrences.json`** — all exist, all real shape, all currently
   empty of content except `units.json`'s 24 rows (`built: false`
   everywhere).
7. The session-context files: `session_index.md`, `improvements_log.md`,
   most recent `session_summary_*.md`.

## Ground rules

- **Never hand-type Hebrew or fabricate content.** Same discipline as every
  prior phase. Phase 5's Unit 1 prose/translation is Lane's own work
  (via the Claude.ai research project, `instructions.md`'s workflow) —
  this session doesn't write it.
- **Ask Lane before guessing on design or scope.** Batch the §A questions
  at the start, same as every prior phase's plan.
- **Run `pipeline/test_*.py` and `pipeline/build.py` before and after
  touching anything in `pipeline/`** — the whole pipeline is green right
  now (10,120+11+43+19+4+5+8+11 checks across the test files, `build.py`
  clean end to end). Don't let that regress.
- Update `improvements_log.md` and `session_index.md` as you go, in
  chronological order at the bottom of each file (append after the most
  recent entry — a past session pasted new entries in the wrong position
  twice; check the section order after each edit). Write a
  `session_summary_<date>.md` at the end.

## Current state, measured 2026-09-15 (don't re-derive; spot-check if in doubt)

**Pipeline (Phases 0–3): done.** `pipeline/hebrew.py` transliterates the
whole corpus; `pipeline/unit_meta.py` validates the full style-reference
contract, including a live acceptance test against the style reference's
own §8 worked example; `pipeline/audit_thread_coverage.py` does id-set
coverage auditing; `pipeline/port_artifact.py` can take a research artifact
from `source-artifacts/joshua_NN_translation.html` to a committed,
validated `units/unit-NN.html` plus a thread-delta report. All of this is
tested, including a full end-to-end run of the porter
(`pipeline/test_port_artifact.py`).

**No units exist yet.** `units/` is empty. `data/units.json` has all 24
rows with `built: false`. `data/threads.json` has zero threads.
`data/roots.json` has zero roots. `data/occurrences.json` is `{}`.

**No colours are assigned anywhere.** Phase 3 deliberately deferred this
(Lane's call: "leave it for Phase 4"). Concretely: `data/threads.json`
threads have no `color` field, and `port_artifact.py`'s
`merge_units_json()` writes local roots into `units.json` as
`{translit, gloss}` only. **This blocks the app shell from rendering
anything but plain black text** — Matthew's `app/threads.js`
`injectPalette()` (below) reads `th.color`/`lm.color` and silently skips
any root with none. Phase 4 cannot finish without addressing this one way
or another — see §A2.

**`css/styles.css` is a whitelist scaffold, not a design.** It defines
just enough class selectors (`mast`, `kicker`, `pericope`, `block`,
`legend`, `notes`, `v`, `n`, `r`, `rl`, `gloss`, `compare`, `en`) for
`unit_meta.py`'s component-whitelist check to have something to diff
fragments against. Every rule body is empty (`{ }`). A real visual design
pass is Phase 4's other half, alongside the JS.

## A. Decisions to get from Lane first (ask all at once)

1. **Is there a Joshua equivalent of Matthew's "discourse" overlay?**
   Matthew's app shell draws two structural layers over the unit
   navigator: **movements** (Joshua has this: 4 movements, already in
   `data/units.json`) and **discourses** (Matthew's 5 major teaching
   blocks, each spanning several units, drawn as labeled brackets in the
   book-map and referenced in each unit's masthead placement line — see
   `discourseOf()`/`buildBookMap()`/`renderPlacement()` in
   `Projects/Matthew/app/main.js`). Joshua's literary unit map has no
   documented sub-movement grouping like this.
   - Recommendation: **drop the discourse layer entirely** for now —
     render movements only. `data/units.json`'s `discourses: []` array
     stays empty (it's real, Matthew-inherited schema per
     `Port analysis.md` §6.2, not vestigial — see `CLAUDE.md`'s Phase 1
     entry — just unused unless Lane wants an analogous concept later).
   - If Lane *does* want an equivalent (e.g. grouping units by recurring
     type-scene, or by which chapters share a `ḥerem` arc), that's a
     content decision or Lane's to make, structurally similar to the
     Literary Unit Map itself — treat it as a `joshua_*` content document
     to author before wiring it into `main.js`, not something to invent
     here.
2. **Colour timing.** Three options, roughly in order of how much this
   session should build:
   - (a) **Assign colours now**, as part of Phase 4 — port Matthew's
     hue-well + collision-avoidance system (`WELL`, `assign_hues()`,
     `_lab`/`_de` in `Projects/Matthew/pipeline/port_artifact.py`) into
     Joshua's `port_artifact.py`, and hand-seed `data/threads.json` colours
     for whatever threads Lane wants to pre-declare.
   - (b) **Ship Phase 4 with no colour** (plain text, dotted-underline
     styling optional) and revisit once Unit 1's real roots/threads exist
     in Phase 5 — colour assignment is arguably easier to get right with
     real content in front of you than in the abstract.
   - (c) Something in between — e.g. wire the *mechanism*
     (`injectPalette`/`rebuildLegend`, CSS custom-property plumbing) now,
     but leave the actual hue-assignment algorithm and its collision math
     for later, once real data shows how many concurrent local roots a
     typical unit actually has.
   - No recommendation here — this is a real design-taste call, not an
     engineering one.
3. **Book map / unit nav visual scope.** Matthew's `buildBookMap()` is a
   fairly elaborate horizontal-scroll movement/discourse map with a key.
   Given open question 1, does Lane want:
   - a similarly rich map (movements only, no discourse brackets), or
   - a simpler list/grid of 24 unit chips grouped by movement, deferring
     a fancier visual map to a later polish pass?
4. **Search hint text and examples.** `app/search.js`'s placeholder/hint
   currently says `Type a transliterated root (aphiēmi, or just aphiemi)
   or an English gloss (forgive).` — needs Hebrew-appropriate examples
   once real roots exist. Not blocking (can ship generic text and revisit
   in Phase 5), but flag so it doesn't get forgotten.
5. **`resources.md`.** Still missing, still Lane-authored, still out of
   scope here — mentioned only so nobody assumes this plan covers it.

## B. What actually ports vs. what needs rework (measured against the real files)

`Port analysis.md` §1.11 called the app shell "essentially wholesale
portable... cosmetic string/localStorage-key literals only." Re-measured
against `Projects/Matthew/app/*.js` + `index.html` (2026-09-15): **true for
about half of it by line count, not the whole thing.**

| file | lines | verdict |
|---|---|---|
| `index.html` | 51 | Portable. Title/description/brand strings, Google Fonts choice (Joshua may want a different pairing — Lane's call, not blocking), and `data-unit`/asset-path literals only. |
| `app/search.js` | 107 | **Portable near-unchanged.** `fold()` (line 103) is already diacritic-generic (`NFD` + strip combining marks) — works for `ḥerem`/`ṭape` the same way it worked for `aphiēmi`. Only the hint text (§A4) needs updating. |
| `app/threads.js` | 275 | **Portable, but functionally inert until §A2 is resolved.** Entirely data-driven off `data/threads.json` + `units.json` roots + `data/occurrences.json` — no Greek/Matthew-specific logic at all. `injectPalette()` (line 52) and `rebuildLegend()` (line 88) both key off a `color` field that doesn't exist in any real Joshua data yet. Ports the *code* unchanged; produces a colourless site until real colours exist. |
| `app/spotlight.js` | 161 | **Needs trimming, not just adapting.** Handles three component kinds: `.gloss` (Joshua has this), `.compare` (Joshua does **not** — Phase 2 resolved no compare box), `aside.synoptic` (Joshua's analogue, `aside.echo`, is optional and undecided — style reference §4). Port the `.gloss` path; drop the `.compare` path entirely (dead weight, and `compare` is in `css/styles.css`'s whitelist only because the style reference's own component table lists it as a *deferred* item, not a built one — double check whether to remove it from the whitelist too if it stays unused); leave `aside.synoptic` handling out until/unless `aside.echo` actually ships (same "ship the check in the same commit as the class" discipline the style reference asks for elsewhere, §4). |
| `app/main.js` | 484 | **The one real rework.** Roughly a third of this file (`discourseOf()`, the discourse-bracket half of `buildBookMap()`, the discourse half of `renderPlacement()`) exists only for Matthew's discourse layer — see §A1. Everything else (routing, footnote jump/return, verse-anchor scrolling, pager, settings panel, nav toggle) is generic and ports directly. **Field-name mismatch to fix regardless of §A1's answer**: Joshua's `data/units.json` `movements[]` entries are shaped `{n, name, span, units}` (this project's Phase 1 shape); `main.js` expects `{id, label}` (`m.id`, `m.label`, see `unitsByMovement()`/`buildBookMap()`/`renderPlacement()`). Reconcile one way (rename Joshua's fields, or adapt `main.js` to read `n`/`name`) — don't leave both conventions live in the same codebase. |
| `css/styles.css` | starter scaffold | Needs the real design pass PLAN.md's Phase 4 already called for — this was never claimed to be portable. |

## Order

A → B (informed by A's answers) → wire `index.html`/`app/*.js`/`css/styles.css`
together → smoke-test against the empty `data/*.json` (site should load,
show "no units built yet", search should render with zero results) →
Phase 5.

## Phase 5 — Unit 1

Once Phase 4's shell renders the empty state correctly:

1. Lane runs the research-project workflow (`instructions.md`) for Unit 1
   (`1:1–18`, per the Literary Unit Map) and saves the artifact as
   `source-artifacts/joshua_01_translation.html`.
2. `python pipeline/port_artifact.py 1 --dry` first — review the thread
   delta, fix anything `unit_meta.validate_fragment()` flags.
3. `python pipeline/port_artifact.py 1` for real.
4. `python pipeline/build.py` to regenerate `occurrences.json`/
   `threads-digest.md` and run the coverage audit.
5. Load the site, actually look at Unit 1 rendered. This is the first time
   any of this pipeline output has been seen in a browser — expect to find
   real issues (the style reference's own checklist says as much: "whatever
   breaks here is cheaper than whatever breaks at unit 15").
6. If Unit 1 wants `aside.echo` (style reference §4's one optional
   component), that's the trigger to build it — component class, CSS,
   *and* its nesting-depth check, in the same commit, not the class alone.

## Done when

- §A's questions are answered before B starts.
- `index.html` + `app/*.js` + `css/styles.css` load against the current
  empty `data/*.json` and show a sane empty state (no console errors, nav
  renders 24 unit chips marked "not yet built", search page renders with
  no results).
- Every existing `pipeline/test_*.py` still passes and `pipeline/build.py`
  still runs clean — this phase shouldn't need to touch the pipeline at
  all, and if it turns out to, that's worth a pause to ask why.
- Unit 1 is ported, builds clean, and renders correctly in a real browser.
- `CLAUDE.md` gets a new section describing the app shell (mirroring how
  each prior phase added one), `PLAN.md` marks Phases 4 and 5 done, and
  the session-context files are updated.

## Out of scope

- Anything past Unit 1 (Phase 6+, deliberately unplanned per `PLAN.md` —
  Matthew's own Phase 5–9 menu — interactions, dashboard/concordance
  polish, persistence, author ergonomics — is a reasonable menu to draw
  from once Unit 1 shows what Joshua's content actually needs).
- `resources.md`.
- Deciding `aside.echo`'s shape in the abstract — that's Unit 1's call, if
  it comes up at all.
