# Bible Study Platform — Design Review Menu

**Date:** 2026-09-17
**Scope:** everything on disk under `Projects/Bible/Joshua` and `Projects/Bible/Matthew` (contracts, chat-side instructions, unit maps, data files, pipelines, tests, app shells, session logs, the Matthew `docs/audit/*` fork drafts, the one built Joshua unit and all eleven Matthew units).
**Not read:** `resources.md` (lives only in the Claude.ai project; not on disk). Anything that depends on its contents is marked as unverified.

This is a menu, not a spec. Every item has an ID so you can reply "keep A3, drop D7". Items marked **speculative** are ideas I could not ground in a specific file. Everything else cites the file and detail that prompted it.

A few things I verified by running code rather than reading prose, because they change the picture:

| Check | Result |
|---|---|
| Joshua `unit_meta.generate(1)` run through `unit_meta.validate()` | **10 errors** (every `opens` entry lacks the required `note`) |
| Duplicate thread colours in Matthew `threads.json` | 3 sets: `sea`/`mercy`, `apo-tote`/`emmanuel`/`son-of-david`, `fringe`/`cross` |
| Matthew `units.json` local-root entries shadowed by a global thread | 44 entries across 30 roots |
| OSHB bare lemma ids in Joshua carrying more than one letter suffix | 12 of 1,156 (e.g. 834 a/c/d, 3588 a/b, 2416 a/e) |
| `data-w` attributes in the unit 1 *source* artifact | 0 (all were added by hand on the repo side) |
| Thread ids shared by both books | `cross` (stauros in Matthew, ʿavar in Joshua) |

---

## A. Current improvements: Joshua

### A1 — `refresh_meta` regenerates a meta block that fails the project's own validator
`build.py` runs `refresh_meta.py`, which rewrites every built fragment's meta block from `generate()`. `generate()` emits `opens`/`payoffs` as `{id, ref}` with no `note`, but `validate()` (correctly, per style reference §3) requires `note` on both. So every build silently writes `units/unit-01.html` into a shape that would fail validation if anything re-checked it. The existing regression test passes only because it uses an empty `threads.json`.
- **Evidence:** `pipeline/unit_meta.py` `_threads_touching()` vs. `validate()` lines 205–211; `test_unit_meta.py:457–469` uses `{"threads": []}`; `units/unit-01.html` meta has ten `opens` with no `note`.
- **Where:** Claude Code.
- **Effort:** S.
- **Depends on:** A2 (decide where `opens.note` lives).

### A2 — `opens.note` has no persistent home
The style reference makes `note` required on `opens[]`, the porter prints it in the thread delta, and then nothing stores it: `threads.json`'s `opens` is `{unit, ref}` with no `note` slot (only `payoffs[]` entries carry one). In practice unit 1's opening notes were folded into each thread's prose `note` by hand. Either add `opens.note` to the `threads.json` schema (and have `generate()` round-trip it) or drop the requirement for `opens` and keep it for `payoffs`.
- **Evidence:** `data/threads.json` `opens` objects; `joshua_study_style_reference.md` §3; `pipeline/port_artifact.py` `thread_delta()` "popover note for the opens".
- **Where:** both.
- **Effort:** S.
- **Depends on:** none.

### A3 — "Declare tracked threads in `roots[]` too" is undone on every regen
Style reference §1 says to declare tracked threads in the artifact's `roots[]`. `merge_units_json()` skips thread roots when writing `units.json`, and `generate()` rebuilds `roots[]` from `units.json`, so the built fragment's `roots[]` contains only local roots. The rule is therefore unenforceable and self-erasing, which is exactly the Matthew ambiguity the port analysis flagged (§6.2 item 3) recurring here. Pick one meaning for `roots[]` and make `generate()` honour it.
- **Evidence:** `units/unit-01.html` `roots[]` lists command/insight/listen/murmur/shatter/valor only; `port_artifact.py` `merge_units_json()` line 176 `continue`; `Port analysis.md` §6.2 (3).
- **Where:** both.
- **Effort:** S.
- **Depends on:** none.

### A4 — Hue-collision avoidance has a blind spot and no backstop
`assign_hues()` seeds `taken` from `meta.roots` only, so a tracked thread the artifact tags but does not declare in `roots[]` is invisible to collision avoidance (Matthew hit exactly this: three same-unit collisions after unit 11). Joshua's `verify_occurrences.py` dropped the per-unit collision check "because colours don't exist yet", but they have existed since Phase 4, so the rationale is stale and nothing re-checks after a thread is recoloured or promoted. Derive `taken` from the fragment's actual `data-root` spans and restore a collision check in `build.py`.
- **Evidence:** `port_artifact.py` `merge_units_json()` lines 166–170; `CLAUDE.md` "verify_occurrences.py — narrower than Matthew's"; Matthew `improvements_log.md` 2026-09-10 (cont. 5) "collisions the porter's hue-assigner missed".
- **Where:** Claude Code.
- **Effort:** S.
- **Depends on:** A3.

### A5 — Build a `data-w` assigner; today it is a seven-step manual recipe
The unit 1 source artifact contained zero `data-w` attributes; every one in the built fragment was added by hand following the retrofit recipe in `CLAUDE.md`. That recipe (pull id-set hits per verse, pull spans per verse, zip, resolve mismatches) is mechanical and is the single largest per-unit cost on the repo side. A script that assigns `data-w` where the per-verse zip is unambiguous, and reports only the ambiguous verses, would make the porter's "missing data-w — hard error" line actionable in one command.
- **Evidence:** `source-artifacts/joshua_01_translation.html` (0 `data-w=`); `CLAUDE.md` "Retrofit recipe" steps 1–7; `port_artifact.py` `_append_coverage()` "missing data-w … hard error".
- **Where:** Claude Code.
- **Effort:** M.
- **Depends on:** none.

### A6 — The chat side is told not to chase word ids, but the contract requires them in two places
`Claude_ai_chat_side_instructions.md` pass 3 says "mark roots with data-root only; don't hand-chase data-w ids". The style reference checklist item 8 requires `data-w` on every tracked span, and §3 requires `w` on any `retro` entry that adds or retags onto a tracked thread. The chat side cannot satisfy the retro rule without chasing ids. Resolve by making `w` optional in the artifact and having the porter (or A5's tool) fill it, then say so in both files.
- **Evidence:** chat-side instructions pass 3; style reference §3 `retro[]` and §7 item 8; `unit_meta.validate()` lines 284–291.
- **Where:** both.
- **Effort:** S.
- **Depends on:** A5.

### A7 — OSHB letter suffixes are not opaque; stripping them can merge lexemes
Style reference §2 says suffixes like `834a` are "treated as opaque — not homograph markers", and `roots.py` strips them before matching and before the "no id in two roots" check. In Joshua's word table 12 bare ids carry more than one suffix, and OSHB uses those letters to separate distinct lemmas (834 a/c/d; 3588 a/b; 2416 a/e). None of the ten current roots is affected, but the policy makes it impossible ever to track one homograph without the other. Match on the full suffixed id when `roots.json` gives one, and fall back to bare only when it does not. I did not confirm each suffix's meaning against `LexicalIndex.xml`; do that before relying on "opaque".
- **Evidence:** computed from `Joshua-words.tsv`; `pipeline/roots.py` `bare_id()`; style reference §2.
- **Where:** Claude Code + style reference §2.
- **Effort:** S–M.
- **Depends on:** none.

### A8 — Three files disagree about `resources.md`
`project-side/README.md` says it is "Missing — needs authoring". `CLAUDE.md` says it "lives only in the Claude.ai project, not the repo, by design". The chat-side instructions tell the project to read it before pass 1 and cite only commentaries listed there. If it is the canonical inventory, the repo should hold it and sync it like every other contract file; if it is project-only, the README row should go.
- **Evidence:** the three files named; `check_project_sync.py` `TRACKED_FILES` omits it.
- **Where:** both.
- **Effort:** S.
- **Depends on:** none.

### A9 — Stale status text in data and docs
`data/units.json` `_note` still opens "No units built yet". `CLAUDE.md` says `app/threads.js` is "unchanged" from Matthew, but it was extended with the `example` field (and `main.js` records a cache-bust bug caused by that change). Style reference §5 still lists naḥalah and the y'all question as "open at unit 1" though both are locked in `translation-choices.md`. Small, but these are the files the chat side reads.
- **Evidence:** `data/units.json` line 2; `CLAUDE.md` "App shell" section vs. `app/threads.js` line 43; style reference §5 closing line vs. `translation-choices.md` Log 2026-09-16.
- **Where:** Claude Code.
- **Effort:** S.
- **Depends on:** none.

### A10 — Scheduled sync commits are cluttering history
Five of the last fifteen commits are "Sync project-side docs" from the 15-minute scheduled task. It works, but generated-mirror commits interleaved with real ones make `git log` and bisecting harder as the book grows. Options: run the sync as a post-commit hook instead of a timer, push the mirror to a `project-side` branch, or keep the mirror in a tiny separate repo the connector points at.
- **Evidence:** `git log --oneline -15` in Joshua; `project-side/README.md`.
- **Where:** Claude Code.
- **Effort:** S.
- **Depends on:** none.

### A11 — `translation-choices.md` carries native Hebrew into a chat-facing file
The glossary's Hebrew column holds pointed script (pulled by word id, so not hand-typed). It is synced to the project whose standing rule is "never print native script". Replace the column with word id + `hebrew.py` transliteration, which is also what the no-hand-typing rule wants.
- **Evidence:** `translation-choices.md` Glossary table; chat-side instructions "never print native script … not in an artifact, not in an attribute".
- **Where:** both.
- **Effort:** S.
- **Depends on:** none.

### A12 — `tagged` flag is vestigial in Joshua
Every Joshua thread is `tagged: true` from birth because id-based coverage makes an untagged thread a build error. The field is a Matthew retrofit-era artefact. Keep it only if the shared schema (section D) keeps it; otherwise drop.
- **Evidence:** `data/threads.json` (all ten `tagged: true`); Matthew `threads.json` `_note` explains its original purpose.
- **Where:** Claude Code.
- **Effort:** S.
- **Depends on:** D3.

### A13 — Record declined candidates so they stop being re-proposed
Unit 1 proposed `all` (kol); the decision was to keep it local, yet it appears neither as a thread nor as a local root. The decision lives only in a session log. A small `declined` map (slug → why, date) in `roots.json` or `threads.json`, surfaced in `threads-digest.md`, tells the chat side not to propose it again and tells the porter to flag a re-proposal.
- **Evidence:** `pipeline/out/thread-delta-01.md` candidate `all`; `CLAUDE.md` promotion note "kol … asked, kept local"; `units/unit-01.html` has no `all` root.
- **Where:** both.
- **Effort:** S.
- **Depends on:** none.

### A14 — Put the Masoretic paragraph breaks to work
`candidate-boundaries.md` lists all 94 petuḥah/setumah breaks and nothing consumes it. Two cheap uses: warn when a pericope heading's `· C:V` start does not coincide with a Masoretic break (a nudge, not a gate, since the style reference says to prefer those breaks), and render the breaks as faint gutter marks in the reading view so the reader sees the tradition's own paragraphing.
- **Evidence:** `candidate-boundaries.md`; style reference §6 "Prefer the Masoretic paragraph breaks"; no reference to the file in `pipeline/` or `app/`.
- **Where:** Claude Code.
- **Effort:** M.
- **Depends on:** none.

### A15 — Decide `aside.echo` before unit 3
Unit 1 already carries cross-book echoes as gloss prose (Exod 3:12 at 1:5, Exod 12:39 at 1:11, Deut 1:26 at 1:18, Deut 3:18–20 in note 6). Joshua is saturated with Deuteronomy, and the Jordan crossing (unit 3) will want Exodus 14 side by side. The component is designed but unbuilt; ship it with its nesting check before the pressure to improvise a shape arrives.
- **Evidence:** `units/unit-01.html` glosses and note n6; style reference §4 `aside.echo`; `CLAUDE.md` "`.echo` left out until wanted".
- **Where:** both.
- **Effort:** M.
- **Depends on:** D5 if the component registry lands first; otherwise none.

### A16 — Editorial TODOs are shipping in reader prose
Endnote n2 in unit 1 ends "Worth rechecking before the note ships." The voice rule keeps commentators and repo files out of prose, but nothing catches draft language. A ten-line check for phrases like "before the note ships", "TODO", "recheck" in fragment text, or a `draft: true` unit flag that blocks port, closes this.
- **Evidence:** `units/unit-01.html` `u01-n2`.
- **Where:** Claude Code.
- **Effort:** S.
- **Depends on:** none.

### A17 — Reports transliterate without overrides
The thread delta and `--ids` report call bare `transliterate()`, so kol renders as `kal` in the candidate preview. Use `transliterate_word(surface, lemma, morph)`; the rows have the fields.
- **Evidence:** `pipeline/out/thread-delta-01.md` `all` preview (`כָּל (kal) ×109`); `port_artifact.py` `_append_candidate_preview()`.
- **Where:** Claude Code.
- **Effort:** S.
- **Depends on:** none.

### A18 — Promotion authority is stated three ways
`CLAUDE.md` and `roots.json` `_note` say Claude decides, biased book-wide. `threads-digest.md`'s header and the style reference §3 say "Lane decides". `unit_meta.py`'s docstring calls ids "evidence for Lane's decision". Align the text with the 2026-09-16 decision.
- **Evidence:** `CLAUDE.md` "Thread promotion"; `threads-digest.md` header; `joshua_study_style_reference.md` §3 `candidates[]`; `unit_meta.py` docstring.
- **Where:** both.
- **Effort:** S.
- **Depends on:** none.

### A19 — Local roots get a fresh colour per unit
A local root that recurs in a later unit is coloured independently each time (Matthew's `kingdom` was one hex in units 3–4 and another in unit 5). Joshua will hit this at unit 2 with `command` (tsawah) or `listen` (shamaʿ). Either the promotion bias handles it (promote on second sighting, which the policy now favours) or `units.json` needs a book-level local palette keyed by slug so a local root keeps its hue.
- **Evidence:** Matthew `session_summary_2026-09-10_thread-expansion.md` "kingdom was #9c2f8f in units 3/4 but #5f7d2e in unit 5"; Joshua `merge_units_json()` per-unit `existing`.
- **Where:** Claude Code.
- **Effort:** S–M.
- **Depends on:** A18.

### A20 — Validate built fragments in `build.py`
`validate_fragment()` runs only on the incoming artifact during port, and only as a report. Retrofit edits, `refresh_meta`, and hand edits can all push a shipped unit out of contract with no signal (A1 is one instance). A `validate_units.py` hard step over `units/*.html` makes the contract hold after port, not just at port.
- **Evidence:** `pipeline/build.py` `STEPS`; `port_artifact.py` `_append_fragment_findings()` "NOT a hard gate".
- **Where:** Claude Code.
- **Effort:** S.
- **Depends on:** A1.

### A21 — WEB English is described as the base text but plays no visible role
Your brief calls WEB the base English text. `CLAUDE.md` lists `Joshua-english.txt` as source data; it was removed from the project-side sync on 2026-09-16; the chat-side instructions never mention it; and the style reference says the verse text is "not a polish of an existing English version". Decide what WEB is for (a starting draft the chat side edits, a diff target, or a fallback for unbuilt units on the site) and write it down once.
- **Evidence:** `CLAUDE.md` "Source data"; `project-side/README.md` "No longer synced"; style reference §5 "Translation philosophy".
- **Where:** both.
- **Effort:** S.
- **Depends on:** none.

### A22 — Uncommitted work and path-move residue
`improvements_log.md`, `session_index.md`, `build_reading.py`, and `build_english.py` are modified but uncommitted after the repo move. The last session summary also notes that committing means running the sync. Small housekeeping before anything else lands.
- **Evidence:** `git status` in Joshua; `session_summary_2026-09-17_doc_trim.md` "Uncommitted".
- **Where:** Claude Code.
- **Effort:** S.
- **Depends on:** none.

---

## B. Current improvements: Matthew

### B1 — Adopt Joshua's hardened validator wholesale
Matthew's `unit_meta.validate()` still accepts unknown keys, any subset of `threads` sub-keys, and has no fragment-level checks. The port analysis documented the costs: `descriptor`/`discourse` authored for eleven units and dropped, unit 11 shipped without a legend, unit 8 ships Greek script inside an `href`. Joshua's `validate_fragment()` closes all of these and is language-neutral apart from the script regex.
- **Evidence:** `Matthew/pipeline/unit_meta.py` lines 103–194; `Port analysis.md` §6.2 items 1, 2, 6, 7; `units/unit-11.html` (no `section.block.legend`).
- **Where:** Claude Code.
- **Effort:** M.
- **Depends on:** D3 if the shared core lands first; otherwise none.

### B2 — Three sets of tracked threads share a hex
`sea` and `mercy` are both `#2f6db3`; `apo-tote`, `emmanuel`, and `son-of-david` are all `#8a3c70`; `fringe` and `cross` are both `#455a6b`. They do not co-occur in a built unit yet, so the per-unit collision check is quiet, but the global tier's promise ("that thread's fixed colour in every unit") is broken, and any dashboard or canon view will show two threads as one. Recolour and add a book-wide uniqueness assertion to `verify_occurrences.py`.
- **Evidence:** computed from `data/threads.json`; `verify_occurrences.py` checks collisions per unit only.
- **Where:** Claude Code.
- **Effort:** S.
- **Depends on:** none.

### B3 — Move Greek root identity to lemma ids and word ids
Matthew's substring stems need long `exclude` lists (`call` excludes thirteen forms), phrase threads are "coverage by hand", and eleven threads still have no stems at all. Joshua measured the same approach at 0–42% recall on weak Hebrew roots and replaced it with id sets plus `data-w`. MorphGNT provides lemma and morphology for the SBLGNT text Matthew already uses, so a `Matthew-words.tsv` with positional word ids is a mechanical build. This is the biggest single quality upgrade available to Matthew, and it is the second-language test of the adapter boundary in section D.
- **Evidence:** `pipeline/thread-stems.json`; `session_summary_2026-09-12_translation-choices-audit.md` "still have no Greek stems"; `HEBREW-TRANSLITERATION.md` §3.2; Joshua style reference §2 table.
- **Where:** Claude Code (+ chat side once `data-w` appears in the contract).
- **Effort:** L.
- **Depends on:** D3, D14.

### B4 — Adopt the project-side sync mirror
Matthew still relies on hand-pasting `threads-digest.md` and `translation-choices.md` into the project and on keeping `Matt.txt` byte-identical to `MatthewSBLGNT.txt` by discipline. Joshua's `project-side/synced/` plus GitHub connector removes both failure modes. Port `sync_to_github.py` and `check_project_sync.py` with a Matthew `TRACKED_FILES`.
- **Evidence:** `instructions.md` "keep the two in sync"; `PIPELINE.md` §C items 3–4; Joshua `project-side/README.md`.
- **Where:** Claude Code.
- **Effort:** S–M.
- **Depends on:** none (A10 informs the shape).

### B5 — Clean `units.json`'s local roots
44 local-root entries are shadowed by a global thread (harmless but misleading), and unit 2 carries wrong data from the legacy legend backfill (`name` → translit "kaleō", `save` → "Iēsous", `david` → "basileus"/"king"). Regenerate local roots from each fragment's actual `data-root` set intersected with the meta `roots[]`, then delete the rest.
- **Evidence:** computed from `data/units.json` and `data/threads.json`; `data/units.json` unit 2 `roots`.
- **Where:** Claude Code.
- **Effort:** S.
- **Depends on:** none.

### B6 — Stale docs and data notes
`CLAUDE.md` status says units 1–10 built and unit 11 next (11 is built). Style reference §7.2 marks units 10 and 11 as unbuilt. `units.json` `_note` still credits the retired `extract_legends.py`. `threads.json` has `egerō` where `translation-choices.md` has `egeirō`. `docs/audit/port-analysis.md` is modified and uncommitted.
- **Evidence:** the files named; `git status` in Matthew.
- **Where:** Claude Code.
- **Effort:** S.
- **Depends on:** none.

### B7 — Retire or archive the `docs/audit/*` fork drafts
Six untracked files (`ARCHITECTURE.md`, `BOOTSTRAP.md`, `CLAUDE.md`, `HEBREW-TRANSLITERATION.md`, `PIPELINE.md`, `PROJECT-INSTRUCTIONS.md`) describe a Joshua that no longer exists (stems, `candidates.stems`, `greek-title` masthead, `<p id="n1">` endnotes). They are excellent history and wrong as instructions. Commit them under a "historical, superseded by the Joshua repo" banner, or move the still-true parts (the irreversibility tiers in `BOOTSTRAP.md`) into the shared core (D8) and delete the rest.
- **Evidence:** `git status` in Matthew; `PROJECT-INSTRUCTIONS.md` §2 `candidates[]` shape vs. Joshua `unit_meta.py`.
- **Where:** Claude Code.
- **Effort:** S.
- **Depends on:** D8 for the salvage.

### B8 — Legend required, and validate built fragments
Same as A20 for Matthew, with a live bug to fix first: unit 11 renders with no colour key. `rebuildLegend()` correctly fails closed; the fix is the fragment.
- **Evidence:** `units/unit-11.html`; `app/threads.js` lines 89–90; `Port analysis.md` §6.2 (2).
- **Where:** Claude Code.
- **Effort:** S.
- **Depends on:** B1.

### B9 — Decide whether Matthew adopts Joshua's voice rule
Matthew's notes name Constable, Chrysostom, France, and Dale Allison (unit 11 notes 7, 8, 13). Joshua forbids named commentators in fragment prose. This is a real editorial choice, not a bug: the Matthew notes read as a scholarly dialogue; Joshua's read as a standalone study. Whichever you pick, the core contract should say it once (see C3).
- **Evidence:** `units/unit-11.html` notes n7, n8, n13; Joshua style reference §4 "Voice".
- **Where:** both.
- **Effort:** S to decide; M to retrofit Matthew if you choose Joshua's rule.
- **Depends on:** C3.

### B10 — Things Matthew does that Joshua should consider adopting
Matthew has four things Joshua deliberately dropped that Joshua will want in some form: (a) the OT citation pointer convention, whose Joshua analogue is a Deuteronomy or Exodus pointer at verses that quote or near-quote (1:3–5 reworks Deut 11:24; 1:5 reworks Deut 31:6–8); (b) structural blocks (`ring`, `table.exod`, `itin`), which the allotment chapters, the 31-king list in ch. 12, and the Levitical-city lists will need as tables; (c) the synoptic aside, whose Joshua analogue is a Joshua ↔ Judges 1 parallel at units 13–16; (d) a compare box, which Joshua could re-scope as a "WEB vs. this study" row since WEB is the declared base text. None of these needs to be inherited as-is; each needs its own shape and check (Port analysis §7.9).
- **Evidence:** Matthew style reference §3; Joshua `units/unit-01.html` glosses citing Deut; `joshua_literary_unit_map.md` units 12–20.
- **Where:** both.
- **Effort:** M each.
- **Depends on:** D5.

### B11 — Phrase threads become auditable with lemma data
`son-of-man`, `son-of-david`, `law-prophets`, `apo-tote`, `emmanuel`, and `little-faith` are "coverage by hand". With word ids, a phrase thread is a lemma n-gram (`5207 444` for huios anthrōpou with article handling) and the audit can count it.
- **Evidence:** `thread-stems.json` `"phrase": true` entries; `audit_thread_coverage.py` "phrase threads (coverage by hand, not audited)".
- **Where:** Claude Code.
- **Effort:** S once B3 exists.
- **Depends on:** B3.

### B12 — The `.prayer` set-piece block defeats the verse audit
`father` at 6:9 is tagged inside a `.prayer` block that is not a `.v`, so the audit reports a false gap and the hole-filling heuristic exists to paper over it. The core contract should either require every verse's text to sit in a `p.v` (set-pieces as `p.v` with a `data-form="poem"` attribute and line breaks) or define a verse-bearing wrapper the audit understands. This matters more for poetry books (E2) than for Matthew.
- **Evidence:** `session_summary_2026-09-10_thread-expansion.md` "father @ 6:9 … false positive"; `audit_thread_coverage.py` `tagged_map()` hole-filling docstring.
- **Where:** both.
- **Effort:** M.
- **Depends on:** D1.

### B13 — `research-prompts.md` and `thread-stems.json` retire with B3
Both exist to drive substring stems. Fold the still-useful part (the "check yourself against what's already tagged" discipline) into the core chat-side workflow.
- **Evidence:** `pipeline/research-prompts.md`; `pipeline/thread-stems.json`.
- **Where:** Claude Code.
- **Effort:** S.
- **Depends on:** B3.

---

## C. Cross-project inconsistencies

Each of these is a place where the two contracts disagree and neither file says which is intended.

### C1 — What `translit` holds
Matthew: same-stem forms joined by `·` (`pistis · pisteuō`). Joshua: one bare root form, no inflected-form lists, no stem labels (decided 2026-09-17). For Greek, noun/verb pairs look different on the page (`pistis`/`pisteuō`), so listing them helps a reader; for Hebrew the forms share consonants and the list was noise. This may be a legitimate per-language difference, but the core should say that rather than leaving two rules.
- **Evidence:** Matthew style reference §1 "Same-stem forms"; Joshua style reference §1 paragraph 3.
- **Where:** both. **Effort:** S. **Depends on:** D1.

### C2 — Who promotes a candidate
Matthew: "Lane decides", everywhere. Joshua: Claude decides, biased book-wide, asks only when unsure (and still says "Lane decides" in two files, see A18). Choose one policy for the core workflow, or make it a profile setting with a stated default.
- **Evidence:** Matthew style reference §2 "Never assumed — surfaced for Lane"; Joshua `CLAUDE.md` "Thread promotion".
- **Where:** both. **Effort:** S. **Depends on:** none.

### C3 — Named commentators in artifact prose
Matthew names them freely in notes; Joshua forbids them anywhere in fragment prose. See B9.
- **Evidence:** as B9. **Where:** both. **Effort:** S. **Depends on:** none.

### C4 — `note` on `opens`/`payoffs`
Matthew optional; Joshua required (and Joshua's generator cannot produce it, A1). Decide once.
- **Evidence:** Matthew `unit_meta.py` line 135; Joshua `unit_meta.py` lines 205–211. **Where:** both. **Effort:** S. **Depends on:** A2.

### C5 — `threads` sub-keys
Matthew: any subset, each checked if present. Joshua: all four required. Joshua's rule is stricter and cheaper to reason about; adopt it in core.
- **Evidence:** Matthew `unit_meta.py` lines 128–131; Joshua lines 197–203. **Where:** both. **Effort:** S. **Depends on:** B1.

### C6 — Legend optional vs. required
Matthew style reference §3 says optional and the site "rebuilds it from data". It does not; it fills an existing one. Joshua says required. Joshua is right; Matthew's text is wrong.
- **Evidence:** Matthew style reference §3; `app/threads.js` line 89. **Where:** both. **Effort:** S. **Depends on:** none.

### C7 — Notes container markup
Matthew: `<div class="notes"><ol>`. Joshua: `<section class="block notes"><ol>`. The difference already caused one bug (the hoist function moving Joshua's endnotes to the top). The retired `PROJECT-INSTRUCTIONS.md` draft used a third shape (`<p id="n1">`). One shape in core.
- **Evidence:** Matthew style reference §3 "Endnotes"; Joshua style reference §4 table; Joshua `CLAUDE.md` "hoistStructureBlocks() skips .notes". **Where:** both. **Effort:** S (M if Matthew's eleven units are migrated). **Depends on:** D1.

### C8 — What a `.gloss` is
Matthew: "short contextual gloss in italics, sits directly beneath the verse". Joshua: "word-by-word translation discussion, collapsed behind the per-verse `*` toggle", with an added rule that endnote markers never sit inside it. Same class, different job. Either name the two things differently or define one.
- **Evidence:** Matthew style reference §3 "A verse + inline gloss"; Joshua style reference §4 table and "(learned, 2026-09-17)". **Where:** both. **Effort:** S. **Depends on:** D1.

### C9 — Endnote-marker placement
Joshua: marker is the last thing in the verse `<p>`. Matthew: no rule, and unit 11's compare-box "Text-form" rows carry citations that Joshua would put in an endnote. Adopt Joshua's rule in core.
- **Evidence:** Joshua style reference §4 verse row; Matthew style reference §3. **Where:** both. **Effort:** S. **Depends on:** none.

### C10 — ʿeved "servant" vs. doulos "slave"
Joshua renders ʿeved as "servant" (thread `servant`, Moses' title). Matthew renders doulos as "slave, not servant" by rule. The LXX renders ʿeved with doulos in most of the places Matthew's reader would meet it, so a canon-wide reader will see the same relationship worded two ways. Not necessarily wrong (Moses as "slave of Yahweh" is a real choice some translations make), but it should be a decision, not an accident.
- **Evidence:** Joshua `threads.json` `servant`; Matthew `translation-choices.md` "slave, not servant". **Where:** both (chat side decides, both glossaries record). **Effort:** S. **Depends on:** F20.

### C11 — y'all rule worded two ways
Matthew: "y'all only for a genuine second-person plural". Joshua: "y'all, always" for 2pl, singular unmarked. Same rule; harmonize in a shared conventions file so a third book does not get a third wording.
- **Evidence:** Matthew `instructions.md`; Joshua `translation-choices.md` y'all row. **Where:** both. **Effort:** S. **Depends on:** F20.

### C12 — sky/skies has no Hebrew counterpart decision
Matthew renders ouranos as "sky/skies" everywhere. Joshua has no shamayim row, and shamayim occurs at 2:11, 8:20, 10:11, 11:4. Decide before unit 2 (Rahab's "God in the skies above and on the earth beneath" is the first hit).
- **Evidence:** Matthew `translation-choices.md` conventions; Joshua `translation-choices.md` glossary (no shamayim). **Where:** chat side. **Effort:** S. **Depends on:** F20.

### C13 — Thread slug `cross` means two different lexemes
Matthew `cross` is stauros; Joshua `cross` is ʿavar. Harmless inside each book; a collision the moment anything canon-wide keys on slug. Fix at the canon layer with namespacing (F1), not by renaming (H7).
- **Evidence:** both `threads.json` files. **Where:** Claude Code. **Effort:** S. **Depends on:** F1.

### C14 — Source-text sync discipline
Matthew: manual byte-identity between `Matt.txt` and `MatthewSBLGNT.txt`. Joshua: word table synced through the mirror. See B4.
- **Evidence:** as B4. **Where:** Claude Code. **Effort:** S. **Depends on:** B4.

### C15 — `candidates[]` schema
Matthew `{root, why, stems?, exclude?}`; Joshua `{root, why, ids?, refs?}`. Converges under B3; until then the core must allow a profile-declared evidence field.
- **Evidence:** both `unit_meta.py` docstrings. **Where:** both. **Effort:** S. **Depends on:** B3, D3.

### C16 — Gloss style
Joshua forbids stem and part-of-speech labels in glosses. Matthew's glosses and `units.json` still carry morphology shorthand ("beget (gen-)", "immerse (bapt-)"). Decide whether the Joshua rule is core.
- **Evidence:** Joshua style reference §1; Matthew `units.json` unit 1 `beget`, `threads.json` `immerse`. **Where:** both. **Effort:** S. **Depends on:** D1.

### C17 — Masthead
Matthew has a `greek-title` line (translit anchor phrase + gloss) and a descriptor tail; Joshua has neither. The Joshua masthead is cleaner; the Greek-title line is genuinely useful for a Greek reader. Core masthead with an optional profile-enabled "anchor phrase" line.
- **Evidence:** Matthew style reference §2 masthead; Joshua style reference §8. **Where:** both. **Effort:** S. **Depends on:** D5.

---

## D. Shared core architecture

The two repos are already about 85% the same code by line count (Port analysis §5), and the differences that matter are concentrated: transliteration, corpus loader, root-identity strategy, component set, palette, and the book map. That is a small, nameable surface, which is the precondition for a core. The Matthew `ARCHITECTURE.md` argued against extracting a framework with only two books; that advice was right at the time and is addressed in G4 and H1 (extract after Joshua has several units, not before).

### D1 — Split the style reference into a core contract and a book profile
**Core (book-agnostic):** the fragment shape (one `article`, meta block first); the meta schema and its closed key set; the `threads` schema with all four sub-keys; the one-lexical-root colour policy and the "tag every occurrence, follow the lexeme" rule; the base component set and its markup (mast, legend required, pericope with range, `p.v`/`span.n`, `r`/`rl`, gloss as following sibling, notes container, endnote markers last in the verse); endnote id/href integrity; no inline style; no native script anywhere including attributes; the checklist skeleton; the worked-example mechanism (each profile supplies one); the three-pass workflow and the four standing moves; the promotion and retro mechanics.
**Profile (per book):** language and transliteration module; corpus, word-table format, id normalisation, and whether word ids exist; the unit map and groupings; enabled optional components; palette well and theme tokens; wording conventions specific to the book; the commentary set and lens; the voice rule if you decide it varies (C3); versification map (E3).
**Borderline cases, argued:** the voice rule belongs in core (a reader moving between books should not feel two editorial personalities; B9 decides which). `translit` shape (C1) belongs in the language profile because the reason it differs is a property of the language, not the book. `data-w` belongs in core as "required when the profile declares word ids". The promotion policy belongs in core workflow. The legend-required and notes-container rules are core because the app depends on them. Structural components are core mechanism (whitelist, nesting check, hoist behaviour) with a profile-enabled set (D5).
- **Evidence:** both style references; `Port analysis.md` §1; `ARCHITECTURE.md` §2 "Exactly three things are worth parameterizing".
- **Where:** both.
- **Effort:** M.
- **Depends on:** C1–C9 decisions.

### D2 — Where the core lives: a separate `bible-core` repo, vendored by pin, not a submodule
You want every book to keep its own repo and Pages site. A `bible-core` repo holding `contract/core.md`, the shared Python package, the shared JS modules, and the core stylesheet, consumed by each book through a `core_sync.py` that copies a tagged release into `book/core/` and records `CORE_VERSION`, gives you one place to fix a bug and an explicit, reviewable step to adopt it per book. Git submodules would work but add friction on Windows and OneDrive and confuse tooling that reads the working tree; a plain vendored copy with a version file is boring in the right way. A monorepo is the other defensible answer, but it fights the one-repo-per-book rule and makes per-book Pages deploys awkward.
- **Evidence:** your brief ("Every book will always have a repo"); Joshua `improvements_log.md` 2026-09-17 (path-move breakage shows how much absolute-path fragility already exists on this machine).
- **Where:** Claude Code.
- **Effort:** M.
- **Depends on:** D1.

### D3 — Validators as a core package plus thin adapters
Core package (`biblecore/`): `meta.py` (parse/validate/generate/inject), `fragment.py` (all fragment checks, script-leak regex supplied by the language adapter), `threads.py` and `roots.py` schema validators, `retrofit.py`, `scan.py`/`verify.py`, `digest.py`, `colour.py` (Lab distance, well selection, uniqueness), `port.py` (the single porter), `build.py` (orchestrator reading `book.json`), `sync.py`. Adapters: `lang/hebrew.py` and `lang/greek.py` (transliterate, script range, id normalisation), `corpus/oshb.py` and `corpus/morphgnt.py` (word-table loader, Ketiv/Qere or variant policy, verse index). The audit is core set-arithmetic over whatever ids the corpus adapter yields. Book repos keep `book.json`, `data/`, `units/`, `source-artifacts/`, the theme CSS, and any book-only scripts (`build_reading.py` is a corpus-adapter concern and moves to core).
- **Evidence:** the two `port_artifact.py`, `unit_meta.py`, and `audit_thread_coverage.py` pairs differ almost entirely in the corpus half; `Port analysis.md` §1.7 "the single most directly portable file".
- **Where:** Claude Code.
- **Effort:** L.
- **Depends on:** D1, D4.

### D4 — A `book.json` profile manifest
Today the profile is scattered: `units.json` `book`, the `WELL` palette in `port_artifact.py`, the storage key in `main.js`, fonts in `index.html`, the source-artifact glob in the porter, the reading-text prefix derivation. One manifest: `{book, abbrev, language, corpus: {kind, pin, word_ids}, versification, components: [...], palette: [...], theme: {...}, unit_map: "…", contract: "core-1.0"}`. Apply the unknown-key rule to the manifest too (H5).
- **Evidence:** `port_artifact.py` `WELL`; `main.js` `CENTER_TEXT_KEY`; `audit_thread_coverage.py` `_text_file_and_prefix()` (`book[:4]` heuristic with a self-check).
- **Where:** Claude Code.
- **Effort:** S–M.
- **Depends on:** D2.

### D5 — A component registry: each optional component is CSS + check + JS + snippet, shipped together
Core defines base components. Optional components (ring, correspondence table, itinerary, synoptic/parallel aside, echo aside, compare box, poem/line block, speaker label, superscription, spec table) each live in one folder with their stylesheet, their nesting or content check, their spotlight handler, and their style-reference snippet. A profile enables a set; the whitelist and the checklist are generated from the enabled set. This is the generalisation of Joshua's "ship the check in the same commit as the class" rule and it prevents the drift the port analysis found (§6.3, seven unregistered classes).
- **Evidence:** `Port analysis.md` §6.3; Joshua style reference §4 "A new class is a decision"; Joshua `CLAUDE.md` `.echo` note.
- **Where:** Claude Code (+ style-reference generation).
- **Effort:** M.
- **Depends on:** D3.

### D6 — Keep the Claude.ai side in sync by pointing, not restating
Each project's instruction field becomes about twenty lines: the lens and commentary set, the three passes, and "the contract is `core-contract.md` and `<book>-profile.md` in the synced folder; the checklist is generated in `<book>-checklist.md`". Both projects already learned that restated rules drift (Joshua trimmed its docs by half without losing a rule). The mirror carries core, profile, digest, glossary, declined list, and word table.
- **Evidence:** `session_summary_2026-09-17_doc_trim.md`; `PIPELINE.md` §C item 5 "the contract lives in three places … drifted".
- **Where:** both.
- **Effort:** S.
- **Depends on:** D1, B4.

### D7 — Versioning so shipped units never break
Give the core contract a version (`core-1.0`, `1.1`, `2.0`), record it in `book.json`, and add `contract` to the meta block's allowed keys so every unit carries the version it was written against. The validator selects rules by version; a unit built under 1.x validates against 1.x until an explicit migration script (retrofit-style, idempotent, with a report) moves it forward. Rule: core never silently regenerates a shipped fragment. A1 is the live demonstration of why: a schema tightened after unit 1 shipped, and the regenerator quietly wrote non-conforming output.
- **Evidence:** A1; `Port analysis.md` §3.2 (regen wiped hand edits); Joshua `unit_meta.py` docstring on `ALLOWED_TOP_LEVEL_KEYS`.
- **Where:** Claude Code.
- **Effort:** M.
- **Depends on:** D3.

### D8 — Bootstrap a new book from a template script
`new_book.py --book Judges --abbrev Judg --lang hebrew --corpus oshb` should produce the repo skeleton, `book.json`, empty `data/*.json` that pass `build.py`, a theme stub, a profile stub with TODOs, a project-side instruction stub, session-context files, and print the irreversibility-ordered checklist from `BOOTSTRAP.md` (transliteration scheme, root strategy, glossary seeded, unit map confirmed) as the things a script cannot decide. Build the script by bootstrapping the third book with it and recording every manual step.
- **Evidence:** `Matthew/docs/audit/BOOTSTRAP.md` tiers 0–5; Joshua `session_index.md` 2026-09-14 (the manual bootstrap took five sub-sessions).
- **Where:** Claude Code.
- **Effort:** M.
- **Depends on:** D2, D4.

### D9 — Shared test suite with per-profile acceptance
Core tests run against synthetic fixtures; each profile supplies a worked example that the acceptance test extracts and validates (Joshua already does this against its §8 fence). `python -m biblecore.test` in any book repo runs core tests plus the book's language and corpus tests (`test_hebrew.py` stays authoritative for the Hebrew scheme).
- **Evidence:** `test_unit_meta.py` acceptance test; `CLAUDE.md` "The test file is the scheme's authoritative definition".
- **Where:** Claude Code.
- **Effort:** S–M.
- **Depends on:** D3.

### D10 — Split the stylesheet into core components and a theme token file
Joshua's stylesheet is a fork of Matthew's with a different palette and fonts and a trimmed component set. Separate `core.css` (chrome, base and optional components, using CSS custom properties) from `theme.css` (tokens: ground, ink, accent, verse-number, heading, fonts). A new book is a token file. Keep the per-book look you asked for; stop forking structure.
- **Evidence:** the two `styles.css` class inventories (Joshua is a strict subset plus a theme).
- **Where:** Claude Code.
- **Effort:** M.
- **Depends on:** D5.

### D11 — Generic groupings instead of movements and discourses
Matthew hard-codes movements and discourses; Joshua deleted the discourse code. Kings will want reigns, Psalms the five books, Daniel the Aramaic block, Job the speech cycles, Acts the "word grew" summaries. One schema, `groupings: [{kind, n, label, span, units}]`, rendered by kind (band, bracket, label), covers all of them and removes the largest divergence between the two `main.js` files.
- **Evidence:** `Matthew/app/main.js` `discourseOf()` and `buildBookMap()` brackets; Joshua `main.js` header comment; `phase-4-5-plan.md` decision "no discourse-equivalent".
- **Where:** Claude Code.
- **Effort:** M.
- **Depends on:** D4.

### D12 — Word ids as a core capability flag
Core rule: "if the profile declares `word_ids: true`, every tracked-thread span carries `data-w`, candidates carry `ids`, retro carries `w`, and the audit is id-based; otherwise the profile must supply a stem matcher". That makes B3 a profile change rather than a fork, and lets a book without morphological data (a Septuagint-only book, say) still ship.
- **Evidence:** Joshua style reference §2; Matthew `thread-stems.json`.
- **Where:** Claude Code.
- **Effort:** S (rule) + B3 (data).
- **Depends on:** D3.

### D13 — One porter driven by the manifest
`port.py` reads the source-artifact pattern, the language adapter, and the enabled components from `book.json`. The only book-specific behaviour left is the palette and the corpus. Delete the two forked `port_artifact.py` files.
- **Evidence:** the two porters differ in `to_fragment()` (Matthew keeps legacy cleaners), the candidate preview, and the coverage shape; everything else is identical.
- **Where:** Claude Code.
- **Effort:** M.
- **Depends on:** D3, D5.

### D14 — A divergence guard
`core_diff.py` reports any file under `book/core/` that differs from the pinned core release, so a quick local fix in one book does not silently become a fork. Pair it with a rule: fixes go to `bible-core` and are re-vendored.
- **Evidence:** Joshua's `threads.js` is documented as "unchanged" and is not (A9), which is exactly this drift at small scale.
- **Where:** Claude Code.
- **Effort:** S.
- **Depends on:** D2.

### D15 — A canon-level conventions file that per-book glossaries inherit
`canon/conventions.md`: y'all, Yahweh, sky/skies, Anointed, Immerser, look/amen, slave/servant, life/being. Each book's `translation-choices.md` starts by importing it and records only book-specific decisions and deviations. C10–C12 are the first three entries.
- **Evidence:** Matthew `translation-choices.md` "General style conventions"; Joshua glossary duplicating the Yahweh and y'all rows.
- **Where:** both.
- **Effort:** S.
- **Depends on:** none (F20 is the same item seen from the canon side).

### D16 — Core chat-side workflow with profile hooks
The three passes and four standing moves are identical across both projects and belong in core. Profiles add: the commentary set and how to weigh it, genre-specific structure cautions (E14), the cross-book standing move (F3), and the local scoping flags (discourses, off-grid unit breaks).
- **Evidence:** `Claude_ai_chat_side_instructions.md` and Matthew `instructions.md` §"Per unit — three passes" are near-identical.
- **Where:** chat side.
- **Effort:** S.
- **Depends on:** D1.

---

## E. Genre and corpus profiles

Everything here is forward-looking. Items marked **speculative** describe books you have not started; the grounded part is what the current pipeline cannot express.

### E1 — Versification maps are a core need, not a genre one
The audit derives the expected verse sequence from the source text, which works for Joshua and Matthew because WEB and SBLGNT numbering agree with the Hebrew and Greek. It fails for Psalms (MT counts the superscription as verse 1, English does not), Joel and Malachi (chapter splits), Daniel 3–4 (Aramaic 3:31–33 = English 4:1–3), 1 Kings 4–5, and Song 6–7. A per-book `versification` map (source ref → display ref) consulted by the audit, the porter, and the app's verse anchors belongs in core 1.0 because retrofitting it later touches every shipped unit's anchors.
- **Evidence:** `audit_thread_coverage.py` `expected_seq()`; `build_english.py` asserts equal verse counts (would fail on Psalms).
- **Where:** Claude Code. **Effort:** M. **Depends on:** D4.

### E2 — Hebrew poetry profile (Psalms, Lamentations, poetic insets)
Needs: a line/colon component (`p.v` containing `span.l` lines, so B12's audit problem is solved by design rather than hole-filling); parallelism marking as a light `data-pair="A"` attribute rather than a typed taxonomy; acrostic gutter letters (transliterated: ʾalef, bet…) for Ps 9–10, 25, 34, 37, 111–112, 119, 145 and Lamentations; a superscription component with the MT/English numbering offset from E1; selah and stanza marks; and a "psalm card" mini-profile for the short breakdown-per-psalm idea, where a unit is one psalm and the meta is compact. Root threads in Psalms will cluster around ḥesed, ʾemunah, tsedeq, nefesh, and the divine names, which argues for seeding the glossary before psalm 1. **Speculative** beyond the component list.
- **Evidence:** B12; Joshua style reference §4 (no line component); your brief.
- **Where:** both. **Effort:** L. **Depends on:** D5, E1.

### E3 — Law profile (Exodus 20–23, Leviticus, Deuteronomy)
Needs: a parallel-law table (Exod 21 ↔ Deut 15 ↔ Lev 25 is the same component as Kings ↔ Chronicles, E9); case-law structure markers ("when… then") as a `data-form` attribute on `p.v`; ritual-sequence blocks (Matthew's `itin` chips reused); phrase threads for formulae ("I am YHWH your God", "you shall not") which the id-based audit can count as lemma n-grams (B11). Exodus mixes narrative, law, and tabernacle spec, so components must be enabled per book but usable per unit (E13). **Speculative.**
- **Where:** both. **Effort:** M. **Depends on:** D5, B11.

### E4 — Wisdom profile (Proverbs, Job, Ecclesiastes)
Units are not chapters: Proverbs 10–22 are two-line sayings with catchword chains, Job is speech cycles, Ecclesiastes is reflective movements. Needs the line component (E2), a speaker-label component for Job's dialogue, groupings by cycle (D11), and keyword-pair threads (ḥakam/kesil) where Joshua's "split a paired opposition into two roots" rule already gives the answer. **Speculative.**
- **Where:** both. **Effort:** M. **Depends on:** E2, D11.

### E5 — Prophecy profile (Isaiah, Jeremiah, Ezekiel, the Twelve)
Prose and poetry alternate inside one unit, so the profile enables both verse forms. Oracle formulae ("thus says YHWH", "oracle of YHWH", "woe") are phrase threads. A historical-anchor line per unit (reign, date) feeds a timeline (F9). Jeremiah's LXX is shorter and differently ordered than the MT, which makes the text-form component (E11) load-bearing there rather than a footnote. **Speculative.**
- **Where:** both. **Effort:** M–L. **Depends on:** E2, E11.

### E6 — Apocalyptic profile (Daniel, Revelation)
Daniel is bilingual: 2:4b–7:28 is Aramaic. OSHB carries Aramaic with its own morph codes and lexicon ids, so the corpus adapter needs a per-word language flag, `hebrew.py` needs an Aramaic override set (the script and most of the scheme carry over), and the meta or the span needs `data-lang` so glosses can say "Aramaic". Both books want a vision ↔ interpretation pairing component (a two-column table), a symbol registry that is really a canon-level thread family (beast, horn, seventy), and for Revelation the densest OT-allusion graph in the canon (F3), plus hymn insets in Greek (E2's line component, Greek flavour). **Speculative** except the Aramaic corpus facts.
- **Evidence:** OSHB `morph` codes prefix `A` for Aramaic; `Joshua-words.tsv` shows the `H` prefix convention.
- **Where:** both. **Effort:** L. **Depends on:** D3, E2, F3.

### E7 — Gospels profile (Mark, Luke, John) and a generalised parallel component
Matthew's synoptic aside is hand-authored per verse and would be authored again in Mark and again in Luke. Generalise it to a parallel component keyed by a pericope id (Aland numbers are the standard) so one authored parallel renders in all three books, and the sites cross-link. John needs "I am" and sign threads; Luke needs the travel-narrative grouping (D11). Mark is the natural second Gospel because it is the source-critical baseline Matthew's boxes already assume.
- **Evidence:** `synoptic_parallels_units_01_10.md` header ("Mark priority + Q is assumed throughout"); Matthew style reference §3 synoptic aside.
- **Where:** both. **Effort:** M–L. **Depends on:** D5, F6.

### E8 — Acts and Luke–Acts continuity
Threads that begin in Luke and pay off in Acts (Spirit, witness, the "word of God grew" summaries, table fellowship) are the first real test of cross-book threads (F1). Acts needs a speech component (speaker, audience, setting) and Matthew's itinerary chips plus a map (F8). Groupings by "word grew" summary statements (D11). **Speculative.**
- **Where:** both. **Effort:** M. **Depends on:** F1, F8.

### E9 — Parallel histories (Samuel–Kings ↔ Chronicles) and regnal formulae
The same parallel component as E7 with prose columns; regnal accession and death formulae as phrase threads; a Deuteronomistic verdict field per unit ("did evil / did right in the eyes of YHWH") for a kings dashboard; a chronology component (F9); prophet-king pairings as a type-scene family (F4). Kings is on your list, so this profile and E1's versification map are the concrete next-Hebrew-book needs. **Speculative** beyond that.
- **Where:** both. **Effort:** M–L. **Depends on:** D5, D11, F4, F9.

### E10 — Epistles profile
Units are argument moves, not episodes; the unit map heuristic changes (E14). Needs a rhetorical-outline grouping, a "therefore" hinge marker, vice/virtue list tables, and OT-citation density that makes F3 the main attraction. Pauline chronology ties to Acts (E8). **Speculative.**
- **Where:** both. **Effort:** M. **Depends on:** D11, F3.

### E11 — Text-form component for MT/LXX and NT variants
Joshua unit 1 already notes "absent from the Greek" at 1:4 and 1:14 in gloss prose, and Matthew's compare box has a "Text-form" row. A small `aside.textform` (or a row type inside the existing gloss) with a `data-src` of `lxx`, `mt`, `qere`, `sbl-apparatus` gives these a home and lets a future LXX corpus adapter fill them from data. Full LXX morphology (CATSS) has licensing limits; start with hand-authored rows and the NETS links Matthew already uses.
- **Evidence:** `units/unit-01.html` 1:4 and 1:14 glosses; Matthew style reference §3 compare box "Text-form".
- **Where:** both. **Effort:** M. **Depends on:** D5.

### E12 — Greek transliteration gets Joshua's discipline
`greek.py` has no test file and a docstring that admits "good enough for legend headwords". Give it a `test_greek.py` that is the scheme's authoritative definition, decide the macron question explicitly (keep ē/ō: they disambiguate η/ε and ω/ο, which is the same "diacritic only where the plain letter is claimed" principle Joshua uses, not vowel length), and record the scheme in the Greek language profile.
- **Evidence:** `Matthew/pipeline/greek.py`; Joshua `CLAUDE.md` "test_hebrew.py is the authoritative definition"; `HEBREW-TRANSLITERATION.md` §1.1.
- **Where:** Claude Code. **Effort:** S–M. **Depends on:** none.

### E13 — Components enabled per book, usable per unit
Exodus (narrative + law + spec), Isaiah (prose + poetry), and Daniel (court tale + vision) all mix genres inside one book. The profile enables a component set; any unit may use any enabled component; the porter does not need a per-unit genre. Say this in D5 so nobody designs per-unit genre flags.
- **Where:** Claude Code. **Effort:** S. **Depends on:** D5.

### E14 — Genre-specific phrasing of "be tough on structures"
The learned rule came from over-fitted chiasms in Matthew. Narrative invites imposed rings; poetry has real acrostics and real strophes; epistles have real rhetorical outlines. The core says "textually verifiable"; each genre profile says what counts as verification there (Masoretic breaks, acrostic letters, formula repetition, discourse markers).
- **Evidence:** Matthew `instructions.md` lens line; Joshua style reference §6; `Port analysis.md` §3.4.
- **Where:** chat side. **Effort:** S. **Depends on:** D16.

### E15 — Lists, genealogies, and allotments as a table component
Josh 12 (31 kings), Josh 15–19 (boundary and town lists), Num 1 and 26, 1 Chr 1–9, Matt 1. A `table.list` component that allows `data-root` spans in cells (unlike the synoptic aside) and links place names to F8. Joshua unit 12 is the first need and is nine units away.
- **Evidence:** `joshua_literary_unit_map.md` units 12–20; Matthew unit 1 genealogy markup (`.gem`, `.triads`, book-specific classes).
- **Where:** both. **Effort:** M. **Depends on:** D5.

### E16 — Aramaic and Hebrew in one word table
For Daniel and Ezra the word table needs a language column, the root registry needs to allow Aramaic lexicon ids (different Strong's range), and glosses must say which language a word is. Cheap if designed into the corpus adapter now; awkward as a retrofit.
- **Where:** Claude Code. **Effort:** S–M. **Depends on:** D3.

---

## F. Canon-wide features

### F1 — Canon thread registry with namespaced ids
Book threads keep their slugs and colours. A `canon/threads.json` maps canon-level threads to book-level ones: `{"id": "inheritance", "arc": "covenant", "members": [{"book": "joshua", "thread": "inherit", "lemma": "heb:5157"}, {"book": "matthew", "thread": "gentle", "ref": "5:5", "lemma": "grc:klēronomeō"}]}`. Joshua's `inherit` and Matthew's "the gentle will inherit the earth" (5:5) are one canon thread today with no link between them. Namespacing also dissolves the `cross` collision (C13).
- **Evidence:** Joshua `threads.json` `inherit` note; Matthew `threads.json` `gentle` note (5:5); C13.
- **Where:** Claude Code (+ chat-side standing move). **Effort:** M. **Depends on:** D2.

### F2 — A Hebrew → LXX → NT lexical bridge
Matthew's `mercy` note already argues "eleos = LXX for hesed". A curated bridge table (Hebrew lemma id → LXX Greek lemma(s) → NT lemma) turns that from prose into data: the canon page for ḥesed shows Joshua 2:12, the LXX rendering, and Matthew 9:13. Seed it by hand per canon thread; a fuller table needs a licensed Hatch–Redpath-style dataset and is a later question. **Speculative** beyond the seed.
- **Evidence:** Matthew `threads.json` `mercy` note; Joshua `translation-choices.md` ḥesed row (open).
- **Where:** both. **Effort:** M (seed), L (full). **Depends on:** F1.

### F3 — Intertext and quotation graph
`canon/intertext.json` with edges `{from, to, kind: quotation|allusion|echo|type-scene, note, source_unit}`. Matthew's ten OT citation pointers are already edges; Joshua unit 1's glosses cite Exod 3:12, Exod 12:39, Deut 1:26, Deut 3:18–20, Ps 1:2. Add a chat-side standing move ("a cross-book echo → an intertext entry in the meta block"), a meta key `intertext[]` (allowed under D7), and a porter step that merges edges. Render as per-verse chips ("cites Isa 7:14", "cited by Matt 1:23"), reverse links once the target book is built, and a graph page on the hub.
- **Evidence:** Matthew style reference §3 "OT citation pointer"; `units/unit-01.html` glosses.
- **Where:** both. **Effort:** M. **Depends on:** D7, F6.

### F4 — Type-scene index
Both projects' lens names type-scenes; nothing records them. A registry `{id, label, instances: [{book, ref, unit, note}]}` for scouts/spies, water crossing, commissioning ("be strong and firm"), covenant renewal, mountain theophany, annunciation, meal with sinners. The standing move is the same shape as F3.
- **Evidence:** chat-side lens lines in both instruction files; Joshua unit 1 note 1 ("Be strong and firm" frame).
- **Where:** both. **Effort:** S–M. **Depends on:** F1.

### F5 — Encode the metanarrative arcs
Creation, covenant, exile, presence are named in both lenses and encoded nowhere. Give canon threads and type-scenes an `arc` field and build the canon dashboard around arcs. This is the cheapest way to make the "one story" claim visible on the site.
- **Evidence:** both instruction files' "creation–covenant–exile–presence".
- **Where:** both. **Effort:** S. **Depends on:** F1.

### F6 — A canon hub site over federated book sites
`lanehaden157.github.io/Bible/` lists books, progress (units built of total, read from each book's `units.json`), the canon registries, and cross-book search. Each book stays its own Pages site; the hub fetches their `data/*.json` (same host, no CORS issue). A book switcher in every book's topbar links back.
- **Evidence:** both `index.html` shells are identical apart from theme; `units.json` already carries `built` per unit.
- **Where:** Claude Code. **Effort:** M. **Depends on:** D10.

### F7 — Cross-book concordance
A hub-side script pulls each book's `occurrences.json` into `canon/index.json`; the search page then answers "where does natan/didōmi appear in every built unit". With F2, a Hebrew search can offer its LXX/NT counterpart.
- **Evidence:** `app/search.js` (per-book index built at load).
- **Where:** Claude Code. **Effort:** S–M. **Depends on:** F6.

### F8 — Maps with a places registry
Allotments (Josh 13–21), conquest campaigns (10–11), the Jordan crossing, Jesus' Galilee, Acts' journeys, the Exodus itinerary. A `places.json` (slug, ancient and modern names, coordinates, source) and an SVG map component with data-driven pins from `data-place` spans. Coordinates from an openly licensed dataset (check OpenBible.info's terms) or hand-entered for the few dozen sites a book needs. Start with one static SVG per book; interactivity later.
- **Evidence:** `joshua_literary_unit_map.md` movements II–III; Matthew style reference `itin` component.
- **Where:** both. **Effort:** L. **Depends on:** D5.

### F9 — Timelines
Kings chronology (with the co-regency problem stated, not solved), Luke–Acts, Matthew's narrative time, the prophets against the kings. A `timeline` component reading a per-book `events.json`. **Speculative.**
- **Where:** both. **Effort:** M. **Depends on:** D5.

### F10 — Structures as data, rendered as SVG
Rings and correspondence tables are hand-written HTML today. Declare them in the meta (`structures: [{kind: ring, rows: [...]}]`) and render SVG from data. Then a structure is searchable, the "verified only" rule can require a `verified_by` field, and the same declaration can feed an interactive view (click A, highlight A′). Matthew shelved ring interactivity; this is the prerequisite.
- **Evidence:** Matthew style reference §3 ring markup; `PLAN.md` "Shelved: Ring/chiasm JS interactivity".
- **Where:** both. **Effort:** M–L. **Depends on:** D7.

### F11 — Per-word interlinear layer from the word table
`Joshua-words.tsv` and the pinned lexicon files are on disk and, by `CLAUDE.md`'s own admission, "not yet consulted by any build". A verse-level toggle that lists every word with transliteration, lemma gloss (from `HebrewStrong.xml` or BDB), and morphology in plain words, plus "highlight every word with this lemma in the book" (via the id set, not just tagged spans), turns the corpus you already pinned into a reader feature. With B3 the same works for Greek.
- **Evidence:** `CLAUDE.md` "HebrewLexicon … Not yet consulted by any build"; `data-w` already links spans to words.
- **Where:** Claude Code. **Effort:** M. **Depends on:** none (B3 for Greek).

### F12 — Link to the vocabulary app both ways
Export a per-book and canon `vocab.json` (lemma id, translit, gloss, count, first unit, thread id) as a stable file the vocabulary app can import; accept deep links in (`#/lemma/5414`) that open the concordance filtered to that lemma; and, if the app exposes URLs, link each word popover out to its card. I do not know the app's format, so this is a contract to agree, not a design. **Speculative.**
- **Where:** Claude Code. **Effort:** S–M. **Depends on:** F7.

### F13 — Navigation for a large site
Book switcher in the topbar, a canon map (books × groupings) on the hub, breadcrumb (book › movement › unit), "continue where you left off" per book from localStorage, per-book progress on the hub, and a reference lookup box that parses "Josh 6:17" or "Matt 5:5" and jumps.
- **Evidence:** `app/main.js` router (per-book only); Matthew `ideas.md` "Reading progress".
- **Where:** Claude Code. **Effort:** M. **Depends on:** F6.

### F14 — Search beyond tagged roots
Today search covers tagged roots only. Build a static full-text index over verse text per book (small; a JSON of verse → text), add lemma-id search from the word table, and reference lookup (F13). Keep it client-side; the corpus is small.
- **Evidence:** `app/search.js` `buildIndex()` reads `occurrences.json` only.
- **Where:** Claude Code. **Effort:** M. **Depends on:** none.

### F15 — Thread popovers reach across books
In a thread popover, "elsewhere in the canon" links via F1, and for lexemes with an F2 bridge, "in the Greek: eleos (Matt 9:13)". The popover already has the trajectory and "also in Unit X"; this is one more row.
- **Evidence:** `app/threads.js` `openPop()`.
- **Where:** Claude Code. **Effort:** S. **Depends on:** F1.

### F16 — Reading modes
Translation only; translation with glosses open; with notes; interlinear (F11). A settings toggle like the existing centre-text one. Cheap and reader-facing.
- **Evidence:** `index.html` settings panel; `spotlight.js` collapse mechanism.
- **Where:** Claude Code. **Effort:** S. **Depends on:** none.

### F17 — Data as a documented, versioned API
`data/*.json` is already static and public. Document the shapes, add `version` (Joshua has it, Matthew's `units.json` does not), and treat them as the interface the hub, the vocab app, and any future tool consume.
- **Evidence:** Joshua `threads.json` `version: 1`; Matthew `units.json` (no version).
- **Where:** Claude Code. **Effort:** S. **Depends on:** D7.

### F18 — Print and EPUB per book
Spotlight already opens everything on print. A per-book "whole study" page that concatenates built units, and an EPUB build, are cheap wins for reading away from the site. **Speculative** on demand.
- **Where:** Claude Code. **Effort:** S–M. **Depends on:** none.

### F19 — Reader annotations
Matthew Phase 8 (localStorage notes) is still unbuilt. Keep shelved until the hub exists; canon-wide notes would want sync, which is a different product.
- **Evidence:** Matthew `PLAN.md` Phase 8.
- **Where:** Claude Code. **Effort:** M. **Depends on:** F6.

### F20 — Canon-level translation conventions
The same item as D15, listed here because it is the first canon registry and the one that makes C10–C12 checkable: with F2, "ʿeved → doulos" and "servant vs. slave" become a query, not a memory.
- **Where:** both. **Effort:** S. **Depends on:** none.

### F21 — Curated reading paths
Sequences across books built from the registries ("the land": Gen 12 → Deut 1 → Josh 1 → Matt 5:5; "be strong": Deut 31 → Josh 1 → Hag 2 → 1 Cor 16). Trivial to render once F1–F4 exist. **Speculative.**
- **Where:** Claude Code. **Effort:** S. **Depends on:** F1, F3.

### F22 — A canon-level "declined and decided" ledger
The book-level declined list (A13) plus canon-level decisions (which canon threads exist, which lexical bridges are accepted) in one place the chat side can read, so a new book's project does not re-litigate settled calls.
- **Where:** both. **Effort:** S. **Depends on:** A13, F1.

---

## G. Roadmap

Ordered by dependency and by what it costs to change later. Effort is cumulative for the group.

### G1 — This week, in Joshua: fix the correctness items
A1, A2, A3, A4, A20, A22, A9, A17, A18. All small, all in files the next unit touches. Do them before unit 2 so unit 2 is the first unit ported under a contract that round-trips.
- **Effort:** S–M total. **Depends on:** none.

### G2 — Before unit 2: the data-w assigner and the chat/contract reconciliation
A5 then A6. This removes the largest per-unit manual cost and the one contradiction the chat side will trip on every unit.
- **Effort:** M. **Depends on:** G1.

### G3 — Before unit 2: the wording decisions that get expensive later
C10, C12, and the canon conventions file (D15/F20) in its first, tiny form; A21 (WEB's role); A13 (declined list). These are ten-minute decisions now and a retroactive pass at unit 10 (Matthew's lesson).
- **Effort:** S. **Depends on:** none.

### G4 — Ship Joshua units 2–4 under the current fork
Do not extract the core from one Hebrew unit. Movement I complete gives you the Jordan crossing (echo component pressure, A15), Rahab (ḥesed, nefesh decisions), and Gilgal, which is enough to see what the profile actually needs. Track every "I wish the contract said…" in a running list for D1.
- **Effort:** content work. **Depends on:** G1–G3.

### G5 — Matthew hygiene in parallel
B2, B5, B6, B7, B8 are all small and independent of the core. B4 (sync mirror) is the one that changes the daily loop and is worth doing before unit 12.
- **Effort:** S–M. **Depends on:** none.

### G6 — Extract the core after Joshua unit 4 and Matthew unit 12
D1 (contract split), D2 (repo and vendoring), D4 (manifest), D3 (package), D7 (versioning), D9 (tests), D14 (guard). Core 1.0 should be exactly what both books already do, with the C-items resolved, not a redesign. Migrate Joshua first (fewer units), then Matthew (B1 as the migration test for D7).
- **Effort:** L. **Depends on:** G4, C1–C9 decisions.

### G7 — Second language adapter: Greek word ids
B3 with D12. This proves the adapter boundary and lifts Matthew to Joshua's audit quality. B11 and B13 follow for free.
- **Effort:** L. **Depends on:** G6.

### G8 — Component registry and stylesheet split, driven by real needs
D5 and D10, then the first optional components in the order units demand them: echo (A15), table.list (E15, Joshua unit 12), parallel (E7/E9), textform (E11). Build each with its first unit, not ahead.
- **Effort:** M each. **Depends on:** G6.

### G9 — Canon registries as flat files, populated by standing moves
F1, F3, F4, F5 as JSON with a handful of hand-entered rows and a chat-side standing move each. No UI until the hub. This is cheap and the data compounds with every unit.
- **Effort:** S–M. **Depends on:** G6 (for the meta keys), otherwise none.

### G10 — Bootstrap the third book with the template script
D8, built by using it. Kings is the natural choice if you want to stress the profile (regnal formulae, chronology, Chronicles parallel, versification); Judges is the natural choice if you want the cheapest possible fork (same corpus, same genre, cycle refrain as a grouping). I would pick Judges for the template and Kings for the profile work.
- **Effort:** M. **Depends on:** G6, G8.

### G11 — Hub, then cross-book features
F6, then F7, F13, F15, F11. Only after two books have several units each.
- **Effort:** M–L. **Depends on:** G9, G10.

### G12 — Genre profiles when their book starts
E2 (poetry) before Psalms; E9 before Kings; E6 before Daniel; E7 before Mark. E1 (versification) and D11 (groupings) go into core 1.0 regardless, because they are cheap now and expensive later.
- **Effort:** varies. **Depends on:** G6.

---

## H. Risks and things not to do

### H1 — Do not extract the core from one Hebrew unit
Matthew's own `ARCHITECTURE.md` made this case and it still holds: with eleven Matthew units and one Joshua unit you know what varies between Greek and Hebrew but not what varies between two Hebrew narrative books, and you have no poetry at all. G4 is the mitigation.
- **Evidence:** `Matthew/docs/audit/ARCHITECTURE.md` opening paragraph. **Where:** both. **Effort:** none. **Depends on:** none.

### H2 — Do not use git submodules for the core
Windows, OneDrive-synced working trees, and tooling that reads the working tree make submodules a recurring source of "why is core empty". Vendor a pinned copy (D2) and guard it (D14).
- **Evidence:** repo lives under OneDrive; the 2026-09-17 path move already broke absolute paths. **Where:** Claude Code. **Effort:** none.

### H3 — Do not let core changes propagate silently into shipped units
A tightened rule must not re-validate old units against itself without a migration, and a regenerator must never write a fragment that the current validator rejects (A1 shows both failure modes in miniature). D7's version pin and "migrations are explicit scripts with reports" is the guard. The Matthew `extract_units` incident (eight units silently diverged) is the same lesson one level up.
- **Evidence:** A1; `Port analysis.md` §3.2. **Where:** Claude Code. **Effort:** none.

### H4 — Do not build genre components speculatively
Section E lists what profiles will need; none of it should exist before its first unit. Joshua's discipline (ship the class with its CSS, check, and JS in one commit, only when a unit wants it) is the right one and scales.
- **Evidence:** Joshua `CLAUDE.md` `.echo` note; `Port analysis.md` §7.9. **Where:** both. **Effort:** none.

### H5 — Do not let `book.json` become a kitchen sink
Every manifest key must be consumed by code, and unknown keys must error, or the manifest becomes the next `descriptor`/`discourse`. Apply the closed-key rule from `unit_meta.py` to the manifest and to profile documents' declared fields.
- **Evidence:** `Port analysis.md` §6.2 (1). **Where:** Claude Code. **Effort:** none.

### H6 — Do not automate the editorial firewall, including at the canon layer
`threads.json`, `roots.json`, and the canon registries are policy. The porter proposes; a human disposes. F1–F5 get the same rule as the book-level files, or the canon layer fills with machine-generated links nobody has judged.
- **Evidence:** `Port analysis.md` §4; both `threads.json` `_note`s. **Where:** both. **Effort:** none.

### H7 — Do not rename thread slugs to unify across books
Renaming `cross` in either book touches every fragment, `retrofit-tags.json`, and `occurrences.json`. Namespace at the canon layer (F1) and leave book slugs alone.
- **Evidence:** C13; style reference §9 on the cost of renumbering. **Where:** Claude Code. **Effort:** none.

### H8 — Do not merge the books into one site
A hub over federated book sites (F6) keeps each book's deploy, theme, and history independent, which is what "every book will always have a repo" implies. A single mega-site couples every book's build to every other.
- **Where:** Claude Code. **Effort:** none.

### H9 — Do not let generated mirrors and scheduled commits dominate history
A10 at book level; at core level, never commit generated `synced/` or `pipeline/out/` into the core repo. Keep the mirror on a branch or in its own repo.
- **Evidence:** Joshua `git log`. **Where:** Claude Code. **Effort:** none.

### H10 — Do not "harmonise" transliteration schemes across languages
Any scheme change rewrites prose inside every shipped unit of that language with no script to help (the transliterations live in sentences). Greek keeps ē/ō; Hebrew keeps no vowel length; both are principled (E12). Freeze each scheme behind its test file and version it with the language adapter.
- **Evidence:** `BOOTSTRAP.md` §0.1; `CLAUDE.md` transliteration section. **Where:** both. **Effort:** none.

### H11 — Watch thread density before it becomes a reader problem
Matthew has 58 tracked threads by unit 11, including father, kingdom, evil, righteous, and spirit, which fire in nearly every unit. At some point most words in a verse are coloured and the colour stops carrying information. Do not solve this with a data taxonomy (the reverted root/motif tier); solve it in display (a per-unit "quiet" set, or the isolate-thread toggle from `ideas.md`). Flagging as a risk, not a change. **Speculative** as to the threshold.
- **Evidence:** `threads-digest.md` (58 threads); `Port analysis.md` §3.5. **Where:** Claude Code. **Effort:** none now.

### H12 — Do not let the Claude.ai instruction fields grow back
Both projects trimmed their contracts by about half and lost nothing. The core-plus-profile split (D6) only works if the instruction field points at the synced files instead of restating them.
- **Evidence:** `session_summary_2026-09-17_doc_trim.md`. **Where:** chat side. **Effort:** none.

### H13 — Check licences before the canon site quotes more
OSHB and HebrewLexicon are CC BY 4.0; WEB is public domain; SBLGNT is free with attribution; MorphGNT is CC BY-SA; NASB and Hart are copyright and appear only as short comparison rows. CATSS LXX morphology has use restrictions. A hub that aggregates many books makes attribution and quote length a real question; decide the policy once and put it in core.
- **Evidence:** Joshua `CLAUDE.md` "Corpus pin" licence notes; Matthew compare-box rows. **Where:** both. **Effort:** S.

### H14 — Do not write the new-book template before the third book
D8 built in the abstract will encode Joshua's accidents. Build it by bootstrapping Judges or Kings and recording what you had to do by hand (G10).
- **Evidence:** Joshua `session_index.md` 2026-09-14 parts 1–7 (the manual bootstrap surfaced decisions no template would have guessed). **Where:** Claude Code. **Effort:** none.

---

## Triage table

| ID | Title | Section | Effort | My recommendation | Keep/Drop |
|---|---|---|---|---|---|
| A1 | refresh_meta regenerates a meta block that fails the validator | A | S | strongly recommend | |
| A2 | opens.note has no persistent home | A | S | strongly recommend | |
| A3 | "Declare tracked threads in roots[]" is undone on regen | A | S | strongly recommend | |
| A4 | Hue-collision blind spot and no backstop | A | S | strongly recommend | |
| A5 | Build a data-w assigner | A | M | strongly recommend | |
| A6 | Chat side told not to chase word ids; contract requires them | A | S | strongly recommend | |
| A7 | OSHB letter suffixes are not opaque | A | S–M | worth considering | |
| A8 | Three files disagree about resources.md | A | S | strongly recommend | |
| A9 | Stale status text in data and docs | A | S | worth considering | |
| A10 | Scheduled sync commits clutter history | A | S | optional | |
| A11 | Native Hebrew in translation-choices.md | A | S | worth considering | |
| A12 | tagged flag vestigial | A | S | optional | |
| A13 | Record declined candidates | A | S | strongly recommend | |
| A14 | Use the Masoretic paragraph breaks | A | M | worth considering | |
| A15 | Decide aside.echo before unit 3 | A | M | strongly recommend | |
| A16 | Editorial TODOs shipping in prose | A | S | worth considering | |
| A17 | Reports transliterate without overrides | A | S | worth considering | |
| A18 | Promotion authority stated three ways | A | S | strongly recommend | |
| A19 | Local roots get a fresh colour per unit | A | S–M | worth considering | |
| A20 | Validate built fragments in build.py | A | S | strongly recommend | |
| A21 | WEB's role is undefined | A | S | worth considering | |
| A22 | Uncommitted work after the path move | A | S | strongly recommend | |
| B1 | Adopt Joshua's hardened validator | B | M | strongly recommend | |
| B2 | Three sets of threads share a hex | B | S | strongly recommend | |
| B3 | Greek root identity by lemma and word ids | B | L | strongly recommend (after core) | |
| B4 | Adopt the project-side sync mirror | B | S–M | strongly recommend | |
| B5 | Clean units.json local roots | B | S | worth considering | |
| B6 | Stale docs and data notes | B | S | worth considering | |
| B7 | Retire or archive docs/audit drafts | B | S | worth considering | |
| B8 | Legend required; validate built fragments | B | S | strongly recommend | |
| B9 | Decide whether Matthew adopts the voice rule | B | S/M | worth considering | |
| B10 | Matthew features Joshua should consider | B | M each | worth considering | |
| B11 | Phrase threads become auditable | B | S | worth considering | |
| B12 | .prayer set-piece defeats the audit | B | M | worth considering | |
| B13 | Retire research-prompts and thread-stems | B | S | optional | |
| C1 | What translit holds | C | S | strongly recommend (decide) | |
| C2 | Who promotes a candidate | C | S | strongly recommend (decide) | |
| C3 | Named commentators in prose | C | S | strongly recommend (decide) | |
| C4 | note on opens/payoffs | C | S | strongly recommend (decide) | |
| C5 | threads sub-keys | C | S | strongly recommend | |
| C6 | Legend optional vs required | C | S | strongly recommend | |
| C7 | Notes container markup | C | S/M | worth considering | |
| C8 | What a .gloss is | C | S | worth considering | |
| C9 | Endnote-marker placement | C | S | worth considering | |
| C10 | ʿeved servant vs doulos slave | C | S | worth considering | |
| C11 | y'all rule worded two ways | C | S | optional | |
| C12 | sky/skies has no Hebrew decision | C | S | strongly recommend | |
| C13 | Thread slug cross collides | C | S | worth considering | |
| C14 | Source-text sync discipline | C | S | strongly recommend (via B4) | |
| C15 | candidates[] schema | C | S | worth considering | |
| C16 | Gloss style | C | S | optional | |
| C17 | Masthead | C | S | optional | |
| D1 | Split style reference into core + profile | D | M | strongly recommend | |
| D2 | Separate bible-core repo, vendored by pin | D | M | strongly recommend | |
| D3 | Validators as core package plus adapters | D | L | strongly recommend | |
| D4 | book.json profile manifest | D | S–M | strongly recommend | |
| D5 | Component registry | D | M | strongly recommend | |
| D6 | Claude.ai side points, not restates | D | S | strongly recommend | |
| D7 | Contract versioning | D | M | strongly recommend | |
| D8 | Bootstrap template script | D | M | worth considering | |
| D9 | Shared test suite with per-profile acceptance | D | S–M | strongly recommend | |
| D10 | Core CSS plus theme tokens | D | M | worth considering | |
| D11 | Generic groupings | D | M | strongly recommend | |
| D12 | Word ids as a capability flag | D | S | strongly recommend | |
| D13 | One porter driven by the manifest | D | M | strongly recommend | |
| D14 | Divergence guard | D | S | worth considering | |
| D15 | Canon conventions file | D | S | strongly recommend | |
| D16 | Core chat-side workflow with profile hooks | D | S | strongly recommend | |
| E1 | Versification maps in core | E | M | strongly recommend | |
| E2 | Hebrew poetry profile | E | L | worth considering (before Psalms) | |
| E3 | Law profile | E | M | optional | |
| E4 | Wisdom profile | E | M | optional | |
| E5 | Prophecy profile | E | M–L | optional | |
| E6 | Apocalyptic profile and Aramaic | E | L | worth considering (before Daniel) | |
| E7 | Gospels profile and generalised parallel | E | M–L | worth considering | |
| E8 | Acts and Luke–Acts continuity | E | M | optional | |
| E9 | Parallel histories and regnal formulae | E | M–L | worth considering (before Kings) | |
| E10 | Epistles profile | E | M | optional | |
| E11 | Text-form component | E | M | worth considering | |
| E12 | Greek transliteration gets a test file | E | S–M | strongly recommend | |
| E13 | Components per book, usable per unit | E | S | strongly recommend | |
| E14 | Genre-specific structure cautions | E | S | worth considering | |
| E15 | Lists and allotments table component | E | M | worth considering | |
| E16 | Aramaic and Hebrew in one word table | E | S–M | worth considering | |
| F1 | Canon thread registry | F | M | strongly recommend | |
| F2 | Hebrew → LXX → NT lexical bridge | F | M/L | worth considering | |
| F3 | Intertext and quotation graph | F | M | strongly recommend | |
| F4 | Type-scene index | F | S–M | worth considering | |
| F5 | Encode the metanarrative arcs | F | S | worth considering | |
| F6 | Canon hub over federated sites | F | M | strongly recommend | |
| F7 | Cross-book concordance | F | S–M | worth considering | |
| F8 | Maps with a places registry | F | L | worth considering | |
| F9 | Timelines | F | M | optional | |
| F10 | Structures as data, rendered as SVG | F | M–L | worth considering | |
| F11 | Per-word interlinear from the word table | F | M | strongly recommend | |
| F12 | Vocabulary app link | F | S–M | worth considering | |
| F13 | Navigation for a large site | F | M | worth considering | |
| F14 | Search beyond tagged roots | F | M | worth considering | |
| F15 | Popovers reach across books | F | S | worth considering | |
| F16 | Reading modes | F | S | worth considering | |
| F17 | Data as a versioned API | F | S | worth considering | |
| F18 | Print and EPUB | F | S–M | optional | |
| F19 | Reader annotations | F | M | optional | |
| F20 | Canon translation conventions | F | S | strongly recommend | |
| F21 | Curated reading paths | F | S | optional | |
| F22 | Canon "declined and decided" ledger | F | S | worth considering | |
| G1 | This week: Joshua correctness fixes | G | S–M | strongly recommend | |
| G2 | Before unit 2: data-w assigner + reconciliation | G | M | strongly recommend | |
| G3 | Before unit 2: wording decisions | G | S | strongly recommend | |
| G4 | Ship Joshua 2–4 under the current fork | G | content | strongly recommend | |
| G5 | Matthew hygiene in parallel | G | S–M | strongly recommend | |
| G6 | Extract the core after Joshua 4 / Matthew 12 | G | L | strongly recommend | |
| G7 | Greek word ids as second adapter | G | L | strongly recommend | |
| G8 | Component registry driven by real needs | G | M each | worth considering | |
| G9 | Canon registries as flat files | G | S–M | worth considering | |
| G10 | Bootstrap the third book with the template | G | M | worth considering | |
| G11 | Hub, then cross-book features | G | M–L | worth considering | |
| G12 | Genre profiles when their book starts | G | varies | worth considering | |
| H1 | Do not extract the core from one Hebrew unit | H | — | strongly recommend | |
| H2 | Do not use git submodules | H | — | strongly recommend | |
| H3 | Do not let core changes propagate silently | H | — | strongly recommend | |
| H4 | Do not build genre components speculatively | H | — | strongly recommend | |
| H5 | Do not let book.json become a kitchen sink | H | — | strongly recommend | |
| H6 | Do not automate the editorial firewall | H | — | strongly recommend | |
| H7 | Do not rename thread slugs across books | H | — | strongly recommend | |
| H8 | Do not merge books into one site | H | — | worth considering | |
| H9 | Do not let mirrors dominate history | H | — | worth considering | |
| H10 | Do not harmonise transliteration schemes | H | — | strongly recommend | |
| H11 | Watch thread density | H | — | worth considering | |
| H12 | Do not let instruction fields grow back | H | — | strongly recommend | |
| H13 | Check licences before the hub quotes more | H | S | worth considering | |
| H14 | Do not write the template before the third book | H | — | worth considering | |
