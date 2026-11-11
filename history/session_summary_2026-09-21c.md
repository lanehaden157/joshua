# Session summary — 2026-09-21 (part 5): read-through feedback on units 1–2

## What Lane asked
1. Footnotes should look like Matthew's, not a white box.
2. Glosses should be short, with longer material moved to footnotes.
3. Less grammar and Radak; unit 2 was the worst case.
4. More intertextuality, e.g. Tamar and Matthew's genealogy in unit 2.
5. Words with a Torah or later-canon history should get a popover-style note (dread, scarlet, sole of the foot / Gen 8:9).
6. `chase` should become a tracked thread.

Lane's decisions: use a root-popover `echo` field rather than inline asides, and rework both units here rather than only changing the instructions.

## What was done
- **Footnotes:** CSS now matches Matthew (no panel, 16px ink, top rule), and `section.block.notes` is neutralised as well. Notes use a bold lead with the verse, Matthew-style.
- **`echo`:** added to roots[] and threads.json, wired through validate/generate/port/threads.js/CSS. All 15 threads and every notable local root in units 1–2 carry one.
- **`chase`:** radaf 7291 is tracked (#1d2a80) and tagged ×7 in unit 2, with id assignment fully automatic. Opens at 2:5.
- **Units 1–2 rewritten** in `source-artifacts/` and re-ported. Short glosses, grammar/textual material in footnotes, Radak-derived glosses cut, 20 cross-canon asides. All 73 Hebrew-Bible citations checked against morphhb.
- **Bugs found and fixed:**
  - Local-root `example` was never persisted, so it was dropped on regen.
  - The unit 2 port had silently re-ported unit 1 from a stale source, which is part of why Radak and stem labels were showing in unit 1. The porter now needs `--force` to overwrite.
  - Commentator name and stale internal note removed from threads.json.
- Docs updated: style reference (§1, §3, §4 *Balance*, checklist, §8), chat-side instructions, CLAUDE.md, translation-choices.md (radaf).

## Takeaways
- Source artifacts must stay current with the built fragments. The `--force` guard makes an accidental re-port impossible, but a deliberate one against a stale source would still regress the unit.
- The palette is crowded. validate_units warns on 6 near pairs across units 1–2 (dE 6–7), and `servant` and `devote` share `#8a2f3a` exactly in threads.json. These are warnings, not blockers.

## Open questions / follow-ups
- The `servant`/`devote` identical colour needs one of them recoloured (Lane's call on which).
- Style reference §5 "Still open: ḥerem, ḥesed, goel, nefesh" is stale; three of those are now locked.
- Not committed and not synced to the project side yet. The style reference and chat-side instructions changed, so the Claude.ai project needs `pipeline/sync_to_github.py` after commit.
- Lane should read the reworked units: the glosses and footnotes are now Claude-authored editorial content, not chat-side research output.
