# Project-side sync — index, not a copy

This folder holds **no files of its own** except this index. Every file below
lives at its one real path in the repo (linked); nothing is duplicated here.
That's deliberate, not an oversight — `instructions.md` says it outright:
*"Matthew's contract lived in three places and drifted."* A second copy here
would be exactly that mistake. This file exists so you don't have to hunt for
the paths, not to give any of them a second home.

**Workflow:** when a file marked "repo → project" below changes, re-paste its
current content into the Claude.ai project (instructions field for
`instructions.md`, project knowledge/files for the rest). Nothing detects
drift if this is skipped — same manual discipline Matthew's project ran on.

## Files

| file | direction | what it is | update cadence |
|---|---|---|---|
| [`instructions.md`](../instructions.md) | repo → project | Research project's operating instructions (persona, sourcing, three-pass workflow) | Re-paste into the project's instructions field whenever it changes |
| [`joshua_study_style_reference.md`](../joshua_study_style_reference.md) | repo → project | The artifact contract — fragment shape, unit-meta schema, component whitelist, transliteration scheme, checklist | Re-paste whenever it changes |
| [`translation-choices.md`](../translation-choices.md) | repo → project | Hand-maintained glossary of deliberate English renderings | Edit **in the same turn** as any wording decision — this is the rule that saved a retroactive pass on Matthew |
| [`threads-digest.md`](../threads-digest.md) | repo → project | Generated snapshot of tracked cross-unit threads — source of truth for what to tag | Regenerate (`python pipeline/threads_digest.py`) any time `data/threads.json` changes; never hand-edit |
| [`resources.md`](../resources.md) | repo → project | **Missing — needs authoring.** `instructions.md` already points to it as "the single authored inventory" (Hebrew/word files, generated digests, the commentary set). Nothing reads it yet because it doesn't exist. | N/A until created |
| [`data/roots.json`](../data/roots.json) | repo → project | Tracked-thread root identity — hand-curated Strong's/lemma id sets per root (style reference §2) | Re-paste whenever a root's id set changes |
| [`Joshua-words.tsv`](../Joshua-words.tsv) | repo → project | Per-word OSHB data (`word_id, ref, surface, lemma, morph`) — the thing every Hebrew string in an artifact must be pulled from, never hand-typed (style reference §2) | Static once generated; only changes if the corpus pin changes |
| [`Joshua-reading.txt`](../Joshua-reading.txt) | repo ↔ project | Pointed Hebrew verse text | Manual sync point, like Matthew's `Matt.txt` ↔ `MatthewSBLGNT.txt` — nothing detects drift if the project side's own copy diverges |
| [`Joshua-english.txt`](../Joshua-english.txt) | repo ↔ project | WEB-classic English verse text (baseline, not the study's own translation) | Same manual sync discipline |

## Also worth knowing about, not part of the sync loop

- [`CLAUDE.md`](../CLAUDE.md) — how *this repo* behaves (pipeline, pins,
  verification). Repo-side only; the project doesn't need it.
- [`PLAN.md`](../PLAN.md) — phase list and open questions. Repo-side only.
- [`Port analysis.md`](../Port analysis.md) — the audit this whole structure
  was designed against. Reference, not a live sync file.
- [`joshua_literary_unit_map.md`](../joshua_literary_unit_map.md) — fulfills
  the style reference's §9 TODO (unit numbers/slugs/passages/movements).
  Worth pasting into the project once at kickoff; not a per-turn sync file
  unless the map itself changes.
