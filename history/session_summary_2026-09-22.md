# Session summary — 2026-09-22: the intertext pass

## What Lane asked
The project side should spend real time researching intertextuality. Yesterday's unit 1–2 cross-references were written in Claude Code from memory, which skipped that research.

## What was done
- **Split of labour:** Claude Code runs the word search, the project side does the judging.
- **`pipeline/canon_leads.py`** writes `canon-leads/canon-leads-unit-NN.md`: rare words and Torah-shared phrases, with every hit, across the whole Hebrew Bible.
  - Scope was measured first. Listing every word would mean ~33,000 Torah verses for unit 2; the narrow version gives 16 leads.
  - `build.py` generates sheets for built units plus the next unit (units 1–3 now), and they sync to the project.
- **`pipeline/test_canon_leads.py`** (8 checks) pins real known links.
- **Chat-side instructions** now have four passes. Pass 3 is the intertext pass with a ledger (rejected links kept, with reasons) and a pause for Lane.
- **Other docs:** style reference, CLAUDE.md, project-side README and PLAN.md updated.

## Takeaways
- The leads sheet surfaces links nobody went looking for. Gen 19:4 (Sodom) for Josh 2:8 came out on the first run.
- It is blind to common words, themes and the New Testament. Tamar/scarlet will never show up there, which is why the ledger pass carries the real weight.

## Open questions / follow-ups
- **Lane must paste the updated `Claude_ai_chat_side_instructions.md` into the Claude.ai project by hand.** It isn't in the synced mirror.
- Should the ledger come back into the repo as a file? For now it lives in the project chat.
- Units 1–2 need their pass 3 run on the project side, then a re-port with `--force`.
- Not committed or synced yet.
