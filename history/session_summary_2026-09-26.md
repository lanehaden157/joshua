# Session 2026-09-26

## Done
- **Sync:** `Joshua-reading.txt`, `Joshua-english.txt`, `joshua_literary_unit_map.md`, `resources.md` (now in the repo) and `candidate-boundaries.md` are synced to the project. `resources.md` §1 is one synced list, points to `Joshua-reading.txt` (the project had called it `Joshua-Hebrew.txt`; kept the repo name, which core expects) and to `candidate-boundaries.md` for the Masoretic breaks (it had said they weren't on hand).
- **Onto bible-core 0.7.1** (Lane: all of it except the template app shell):
  - `book.json`, vendored `biblecore/`, `data/palette.json`; `pipeline/` removed except a `sync_to_github.py` shim; `retrofit/`, `corpus/{lexicon,web}`, `tools/build_english.py`, `out/`.
  - Proof: scratch re-port of units 1–4 byte-identical apart from the `contract` stamp; `corpus` rebuild byte-identical; audit 0 gaps; `biblecore test` 8/8; app browser-checked.
  - Chat-side instruction field restructured: lens + Joshua additions, pointing to synced `core-workflow.md`. Needs a hand paste.
  - bible-core: tests follow Joshua's new layout (227/227, one test dropped: Joshua's own audit no longer exists); hub reads Joshua's emitted `lemmas.json` (concordance unchanged); ARCHITECTURE/README/core-plan updated.

## Takeaways
- Core's validator warns on close colours; it found `devote` and `servant` sharing `#8a2f3a`.
- The `JoshuaProjectSideSync` scheduled task's working directory is `Projects\Joshua`, which no longer exists, so it has been failing (0x8007010B) since the repo moved under `Bible\`.

## Follow-up (same day, Lane: "fix all")
- Scheduled task `JoshuaProjectSideSync` deleted and `pipeline/` shim removed. Sync now runs with every commit/push (memory rule); docs updated.
- Recoloured by the algorithm: `devote` #8a2f3a → #53350e (promoted after `servant`); unit 3 local `land` #8a2f3a → #55642f (it collided too). Build clean; browser-checked.
- Hub rebuilt and pushed (`29926f1`): Matthew's threads, Joshua's devote colour.

## Open
- Lane: paste `Claude_ai_chat_side_instructions.md`, then `python -m biblecore sync-check --mark-pasted`; delete the hand-uploaded copies on the project side.
