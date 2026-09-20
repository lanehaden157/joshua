# Cross-unit threads — canonical digest

Generated from `data/threads.json` (version 1). 10 threads, 10 open.

**This is the source of truth for thread tagging.** In a unit's fragment, a root that appears in the `id` column below is a *tracked thread*: tag every occurrence `<span class="r" data-root="<id>" data-w="<word id>">…</span>` (the OSHB word id from `Joshua-words.tsv`) and list it under `threads.opens` / `threads.payoffs` in the unit-meta block, with a matching id set in `data/roots.json`. A root that is recurring but *not* here is unit-local — tag it with its own name (no `data-w` needed) and just declare it in the unit's own `roots`. To propose promoting a local root to a tracked thread, add it to `threads.candidates` with a one-line reason (the Strong's/lemma `ids` you've actually observed in `Joshua-words.tsv`, plus a few representative `refs`, if you have them). **Claude decides, biased toward book-wide** (Lane, 2026-09-16): a local root that later pays off is worse than a tracked one that doesn't, so promote on a real second sighting. Ask Lane only when genuinely unsure.

| id | root (data-root) | translit | gloss | opens | payoffs | status |
|---|---|---|---|---|---|---|
| `cross` | `cross` | ʿavar | cross over; the far side (of the Jordan) | 1 (1:2) | — | open |
| `firm` | `firm` | ʾamats | be firm, be resolute (the glottal ʾ, aleph — not the ʿ of ʿavar) | 1 (1:6) | — | open |
| `give` | `give` | natan | give | 1 (1:2) | — | open |
| `inherit` | `inherit` | naḥal | cause to inherit, give as an inheritance | 1 (1:6) | — | open |
| `possess` | `possess` | yarash | take possession, possess | 1 (1:11) | — | open |
| `rest` | `rest` | nuaḥ | give rest | 1 (1:13) | — | open |
| `send` | `send` | shalaḥ | send | 1 (1:16) | — | open |
| `servant` | `servant` | ʿeved | slave (Moses' title, 'slave of Yahweh') | 1 (1:1) | — | open |
| `strong` | `strong` | ḥazaq | be strong | 1 (1:6) | — | open |
| `torah` | `torah` | torah | instruction, the Torah (here 'the scroll of the torah') | 1 (1:7) | — | open |

## Notes per thread

- **`cross`**: the book's first command, qum ʿavor 'rise, cross' (1:2), relayed down the chain (1:11); ʿever 'far side' marks the eastern tribes as people of the other bank. One root, both ids.
- **`firm`**: ʾamats, always paired with ḥazaq; kept as its own root per the colour policy (split pairs).
- **`give`**: natan ×8 in unit 1's speeches; Yahweh 'is giving' (participle) vs. 'Moses gave' (perfect) — the land as gift, already done and not yet done.
- **`inherit`**: tanḥil 'you will cause to inherit' (1:6) is the first naḥal-family word in the book, ahead of naḥalah 'inheritance' in the allotment chapters (units 13-20).
- **`possess`**: Qal yarash 'possess' only in unit 1; the Hiphil 'drive out' arrives later in the book — the stem split is the thread.
- **`rest`**: meniaḥ 'giving rest' (1:13) and yaniaḥ (1:15) set up the book's completion formula (Hawk: 21:44, 22:4, 23:1).
- **`send`**: 'wherever you send us we will go' (1:16) — the next verse in the book, 2:1, is Joshua sending the spies.
- **`servant`**: ʿeved YHWH belongs to Moses in unit 1; watch whether and when Joshua receives it (24:29).
- **`strong`**: ḥazaq ×4 — three times from Yahweh, the last time from the eastern tribes (1:18); recurs at 10:25.
- **`torah`**: 'the scroll of the torah' (1:8) opens a line to 8:31-34, 22:5, and 23:6.

## Considered and kept local

These were proposed as threads and deliberately declined. Don't re-propose one without a specific new payoff in view -- say what changed.

- **`all`** (declined 2026-09-16, unit 1): kol, 236 occurrences book-wide. Asked Lane (the frequency made it a genuine toss-up) and kept local: a root that common carries no signal as a tracked thread -- colouring it would tint the page without telling a reader anything. Re-propose only with a specific payoff in view, not on frequency alone.
