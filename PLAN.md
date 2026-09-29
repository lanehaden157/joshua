# Joshua Study — Plan

Current state: `CLAUDE.md` ("State" line). How the repo behaves: `CLAUDE.md`. The
artifact contract: `joshua_study_style_reference.md`. This file is the phase
list and what's still open. The pre-2026-09-29 version of this plan (with the
Matthew-pipeline port audit's findings and the per-phase detail) is in git
history; `Port analysis.md` keeps the audit itself, and `improvements_log.md`
has the session-by-session record.

## Done

| phase | what | when |
|---|---|---|
| 0, 0.5 | Corpus (OSHB words, reading text, WEB English, boundaries), Hebrew transliterator + tests, guardrails, session/policy files | 2026-09-14 |
| 0.6 | Reconciled with the style reference: id-based roots (`roots.json` + `data-w`), transliteration scheme fixes, hardened `unit_meta` | 2026-09-14 |
| 1 | `data/units.json` from the literary unit map (24 units, 4 movements) | 2026-09-15 |
| 2 | Cross-book echo: `aside.echo` instead of a Matthew-style compare box | 2026-09-15 |
| 3, 4 | The port pipeline and the app shell (own theme: clay, bronze, Jordan valley) | 2026-09-15 |
| 5 | Unit 1 built and live | 2026-09-17 |
| 5.5 | Onto bible-core (vendored `biblecore/`, `book.json`, `python -m biblecore`); `pipeline/` retired. Byte-identical units bar the contract stamp | 2026-09-26 |
| — | Template app shell adopted (core 0.8.5): All books, reading modes, interlinear, print; `css/styles.css` retired | 2026-09-26 |

Units 1–4 are built (Movement I); 20 tracked threads.

## Open

- **Units 5–24.** Same loop each time: the unit's canon-leads sheet is waiting
  after the build, then the research artifact (Claude.ai, four passes, pass 3 the
  intertext ledger), `python -m biblecore port N`, thread promotion +
  `data-w`, browser review, commit. Revisit per unit whether anything from
  Matthew's later phases (concordance/dashboard, persistence, author ergonomics)
  has become worth building.
- **Units 1–2 through the intertext pass.** Their echoes and cross-reference
  asides were drafted in Claude Code from memory (2026-09-21) and are
  provisional. The project side runs pass 3 on each shipped unit and delivers a
  revised artifact; re-port with `python -m biblecore port N --force`.

## Decisions still in force

- **Roots are id sets, not strings.** `data/roots.json` holds hand-curated
  lemma-id sets per tracked root; every tracked-thread span carries `data-w`.
  Flat and non-taxonomic: Matthew built and reverted a richer root/motif model
  the same day.
- **Transliteration only, no native script**, checked by the build. Because of
  that the shell needs no RTL support; that changes only if the policy is ever
  relaxed.
- **Joshua-specific shape:** no Matthew-style compare or synoptic box; `aside.echo`
  covers the cross-book case.

## Open questions for Lane

None open.
