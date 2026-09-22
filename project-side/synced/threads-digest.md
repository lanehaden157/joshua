# Cross-unit threads — canonical digest

Generated from `data/threads.json` (version 1). 18 threads, 18 open.

**This is the source of truth for thread tagging.** In a unit's fragment, a root that appears in the `id` column below is a *tracked thread*: tag every occurrence `<span class="r" data-root="<id>" data-w="<word id>">…</span>` (the OSHB word id from `Joshua-words.tsv`) and list it under `threads.opens` / `threads.payoffs` in the unit-meta block, with a matching id set in `data/roots.json`. A root that is recurring but *not* here is unit-local — tag it with its own name (no `data-w` needed) and just declare it in the unit's own `roots`. To propose promoting a local root to a tracked thread, add it to `threads.candidates` with a one-line reason (the Strong's/lemma `ids` you've actually observed in `Joshua-words.tsv`, plus a few representative `refs`, if you have them). **Claude decides, biased toward book-wide** (Lane, 2026-09-16): a local root that later pays off is worse than a tracked one that doesn't, so promote on a real second sighting. Ask Lane only when genuinely unsure.

| id | root (data-root) | translit | gloss | opens | payoffs | status |
|---|---|---|---|---|---|---|
| `cross` | `cross` | ʿavar | cross over; the far side (of the Jordan) | 1 (1:2) | 2 (2:10) · 2 (2:23) · 3 (3:17) | open |
| `firm` | `firm` | ʾamats | be firm, be resolute (the glottal ʾ, aleph — not the ʿ of ʿavar) | 1 (1:6) | — | open |
| `give` | `give` | natan | give | 1 (1:2) | 2 (2:9) · 2 (2:24) | open |
| `inherit` | `inherit` | naḥal | cause to inherit, give as an inheritance | 1 (1:6) | — | open |
| `possess` | `possess` | yarash | take possession, possess | 1 (1:11) | 3 (3:10) | open |
| `rest` | `rest` | nuaḥ | give rest; lay/set down (causative) | 1 (1:13) | 3 (3:13) | open |
| `send` | `send` | shalaḥ | send | 1 (1:16) | 2 (2:1) | open |
| `servant` | `servant` | ʿeved | slave (Moses' title, 'slave of Yahweh') | 1 (1:1) | — | open |
| `sole` | `sole` | kap | palm of the hand; sole of the foot | 1 (1:3) | 3 (3:13) · 3 (4:18) | open |
| `strong` | `strong` | ḥazaq | be strong; strong (adjective) | 1 (1:6) | 3 (4:24) | open |
| `swear` | `swear` | shavaʿ̲ | swear (an oath) | 1 (1:6) | — | open |
| `torah` | `torah` | torah | instruction, the Torah (here 'the scroll of the torah') | 1 (1:7) | — | open |
| `blood` | `blood` | dam | blood | 2 (2:19) | — | open |
| `chase` | `chase` | radaf | chase, pursue | 2 (2:5) | — | open |
| `devote` | `devote` | ḥaram | devote to destruction | 2 (2:10) | — | open |
| `melt` | `melt` | masas | melt | 2 (2:11) | — | open |
| `fear` | `fear` | yareʾ | fear, stand in awe of | 3 (4:14) | 3 (4:24) | open |
| `lodge` | `lodge` | lun | spend the night; lodging place | 3 (3:1) | — | open |

## Notes per thread

- **`blood`**: 'his blood on his head' (2:19) is the bloodguilt logic the cities-of-refuge law runs on — the blood-avenger of 20:3, 20:5, 20:9.
- **`chase`**: Chasing: Jericho's decoy chase (2:5–22) turns into Israel's own routs (7:5, where Israel is the one chased; 8:16–24; 10:10, 19; 11:8), the blood-avenger who chases the manslayer to a city of refuge (20:5), 'one of you chases a thousand' (23:10), and Egypt chasing the fathers to the Reed Sea (24:6).
- **`cross`**: the book's first command, qum ʿavor 'rise, cross' (1:2), relayed down the chain (1:11); ʿever 'far side' marks the eastern tribes as people of the other bank. One root, both ids.
- **`devote`**: first ḥaram in the book, in Rahab's mouth (2:10), before Israel has devoted a single Canaanite city; becomes the governing law of Jericho, Ai, and the campaign reports.
- **`fear`**: yareʾ: Israel fears Joshua as it feared Moses (4:14); the crossing is so that Israel fears Yahweh (4:24); 'do not fear' before battle (8:1; 10:8); 'fear Yahweh and serve him' at Shechem (24:14). Promoted to a tracked thread 2026-09-22 (Lane, unit 3).
- **`firm`**: ʾamats, always paired with ḥazaq; kept as its own root per the colour policy (split pairs).
- **`give`**: natan ×8 in unit 1's speeches; Yahweh 'is giving' (participle) vs. 'Moses gave' (perfect) — the land as gift, already done and not yet done.
- **`inherit`**: tanḥil 'you will cause to inherit' (1:6) is the first naḥal-family word in the book, ahead of naḥalah 'inheritance' in the allotment chapters (units 13-20).
- **`lodge`**: lun, 'lodge the night', with malon 'lodging place': Israel spends the night before each decisive move (the Jordan 3:1, the stones 4:3, 4:8, Jericho 6:11, Ai 8:9). Promoted to a tracked thread 2026-09-22 (Lane, unit 3).
- **`melt`**: Melting hearts: Rahab's 'our heart melted' (2:11) returns for the Amorite and Canaanite kings (5:1) and, reversed, for Israel after Ai (7:5).
- **`possess`**: Qal yarash 'possess' only in unit 1; the Hiphil 'drive out' arrives later in the book — the stem split is the thread.
- **`rest`**: meniaḥ 'giving rest' (1:13) and yaniaḥ (1:15) set up the book's completion formula (21:44, 22:4, 23:1). Widened 2026-09-22 (Lane) to include 3240, the lexicon's separate number for the causative 'lay down' at 4:3, 4:8 — the stones set down exactly where the feet came to rest.
- **`send`**: 'wherever you send us we will go' (1:16) — the next verse in the book, 2:1, is Joshua sending the spies.
- **`servant`**: ʿeved YHWH belongs to Moses in unit 1; watch whether and when Joshua receives it (24:29).
- **`sole`**: kap regel, 'sole of the foot': promised at 1:3 ('every place the sole of your foot treads'), made literal at 3:13 and 4:18, where soles touching and leaving the water start and stop the miracle. Promoted to a tracked thread 2026-09-22 (Lane, unit 3) — a phrase-level thread with a Torah history.
- **`strong`**: ḥazaq ×4 — three times from Yahweh, the last time from the eastern tribes (1:18); recurs at 10:25. Widened 2026-09-22 (Lane) to include 2389, the adjective used at 4:24.
- **`swear`**: Oaths bind the book together: Yahweh's oath to the fathers (1:6), Rahab's oath (2:12, 17, 20), its keeping (6:22), the Gibeonite oath (9:15, 19-20), the rest formula (21:43-44).
- **`torah`**: 'the scroll of the torah' (1:8) opens a line to 8:31-34, 22:5, and 23:6.

## Considered and kept local

These were proposed as threads and deliberately declined. Don't re-propose one without a specific new payoff in view -- say what changed.

- **`all`** (declined 2026-09-16, unit 1): kol, 236 occurrences book-wide. Asked Lane (the frequency made it a genuine toss-up) and kept local: a root that common carries no signal as a tracked thread -- colouring it would tint the page without telling a reader anything. Re-propose only with a specific payoff in view, not on frequency alone.
- **`cross-fords`** (declined 2026-09-21, unit 2): maʿ̲berot, 'the fords' (2:7) -- cognate with the tracked 'cross' root but a distinct lemma (4569b) and a single occurrence. Widening an already-tracked thread's id set on one thin hit isn't the same call as promoting a new one; declined for now. Re-propose only if maʿ̲berot recurs with its own payoff.
