# Cross-unit threads — canonical digest

Generated from `data/threads.json` (version 1). 0 threads, 0 open.

**This is the source of truth for thread tagging.** In a unit's fragment, a root that appears in the `id` column below is a *tracked thread*: tag every occurrence `<span class="r" data-root="<id>" data-w="<word id>">…</span>` (the OSHB word id from `Joshua-words.tsv`) and list it under `threads.opens` / `threads.payoffs` in the unit-meta block, with a matching id set in `data/roots.json`. A root that is recurring but *not* here is unit-local — tag it with its own name (no `data-w` needed) and just declare it in the unit's own `roots`. To propose promoting a local root to a tracked thread, add it to `threads.candidates` with a one-line reason (the Strong's/lemma `ids` you've actually observed in `Joshua-words.tsv`, plus a few representative `refs`, if you have them); Lane decides.

*(No threads defined yet — this file exists to prove the `threads.json` → `threads-digest.md` round trip works before unit 1, not because there's anything to digest. Regenerate once Lane adds the first thread.)*
