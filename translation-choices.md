# Translation Choices

A working glossary of deliberate English renderings for this study's own
translation. Seeded empty at unit 1, on purpose — Matthew's glossary arrived
at unit 10 and immediately produced a wording-audit session and a
retroactive reconciliation pass over everything already shipped
(`Port analysis.md` §7.10). Starting here costs nothing; starting late
costs a pass over the whole book. **Not** a list of every Hebrew word in the
fragments — just the ones where the choice was made on purpose and is worth
carrying forward consistently.

Verse refs below are Joshua chapter:verse. Hebrew forms are the actual OSHB
citation cited next to each row — pulled from `Joshua-words.tsv` by word id,
not hand-typed.

## How to use this file

Before rendering a Hebrew word in a new unit's translation, check this file
for a prior decision and match it. If a different rendering genuinely fits
better in a specific verse, use it — but say so explicitly (a note, or
flagged wherever this project's equivalent of a thread-delta report lives),
rather than silently drifting. Lane reviews the flag and decides whether
it's a one-off exception or a correction that should update this file
everywhere.

Keep this file current as part of normal workflow — any session that
changes a rendering updates the relevant row and the Log section below in
the same turn, without being asked separately. It's hand-maintained prose,
not generated from the fragments, so if a unit's actual text and this file
ever disagree, the unit is more likely right; flag the mismatch rather than
trusting the file blindly.

## Glossary

| word | Hebrew | rendering | note |
|---|---|---|---|
| divine name | יְהוָ֑ה (YHWH) | Yahweh | Matches `pipeline/hebrew.py`'s `OVERRIDES` table (Strong's 3068/3069) — not "LORD." Consistent with `Joshua-english.txt`'s WEB-classic source, which also uses Yahweh. |
| ʿeved | עֶ֣בֶד (Josh 1:1) | **slave** | Locked 2026-09-19 (Lane). Matches Matthew's doulos rule ("slave, not servant"), so the canon reads one relationship one way: the LXX renders ʿeved with doulos in most places a canon-wide reader meets it. Moses' title becomes "slave of Yahweh" — a real choice some translations make, and now a decision rather than an accident (platform review C10). Applied 2026-09-19 to unit 1 (all 5 occurrences: 1:1, 1:2, 1:7, 1:13, 1:15) via `retrofit-tags.json`, with the thread gloss updated to match. The thread *slug* stays `servant` — it is an internal identifier, never shown to a reader, and renaming it would mean retagging every span for nothing (review H7). |
| shamayim | בַּ/שָּׁמַ֣יִם (Josh 2:11) | **sky / skies** | Locked 2026-09-19 (Lane). Matches Matthew's ouranos rule, so a canon-wide reader meets one word for one thing. Four occurrences, and they split by sense — 2:11 (Rahab's "God in the skies above and on the earth beneath") and 8:20 (smoke going up) read cosmologically, while 10:11 (hailstones) and 10:13 (the sun standing still) are plainly physical; WEB itself renders the first pair "heaven" and the second "sky". Rendering all four the same is the deliberate choice: the fixed rule beats a per-verse judgement that would need re-litigating in every book. Note 11:4 does *not* contain shamayim — `platform-design-review.md` C12 lists it in error; the fourth occurrence is 10:13. |
| ḥerem | חֵ֛רֶם (Josh 6:17) | **devote(d) to destruction** (verb ḥaram); noun ḥerem rendered contextually ("designated for destruction" / "the ban") when it arrives | Locked 2026-09-21 (Lane, ahead of unit 5). First occurrence is 2:10 (Rahab, of Sihon and Og), already the `devote` thread's tracked root. Kept as an English phrase rather than transliterated like ḥesed/torah: the verb form dominates the book's early occurrences ("y'all devoted to destruction," "they devoted the city"), and a transliterated verb ("ḥaram'd") is far clunkier in running prose than a transliterated noun. Revisit only if the noun ḥerem (6:17 onward) turns out to need its own row. |
| ḥesed | חָ֑סֶד (Josh 2:12, 2:14) | **left untranslated ("ḥesed"), with a gloss** | Locked 2026-09-21 (Lane). Three occurrences: Rahab, 2:12 ×2 ("I have done ḥesed with you... you also will do ḥesed with my father's house") and 2:14 ×1 (the spies' reply, "we will do ḥesed and truth with you") — a reciprocal covenant-loyalty exchange, paired with "a sign of truth" and sworn by Yahweh, not the word's more common divine-to-human register. "Steadfast love" reads oddly for a spy-protection pact; "kindness" (WEB's choice) loses the obligation entirely; "loyalty" is the closest single word but still thinner than the term carries. Same pattern as `torah` (already transliterated, already a thread) — the word stays "ḥesed" in running prose, glossed at first occurrence rather than forced into one lossy English word. (Corrected 2026-09-21: this row previously said "two occurrences, both at 2:12" — the words file has three, 2:12 ×2 + 2:14 ×1; unit 2's actual tagging was already correct, only this row was wrong.) |
| Yam Suf | יַם ס֗וּף (Josh 2:10) | **Reed Sea** | Locked 2026-09-21 (Lane), first occurrence 2:10 (Rahab, "Yahweh dried up the waters of the Reed Sea"). More literal rendering of yam suf ("sea of reeds") than the traditional "Red Sea," which `Joshua-english.txt` (WEB classic, provenance-only) and most English translations use. |
| radaf | רִדְפ֥וּ (Josh 2:5) | **chase** (verb); participle **the chasers** | In use since unit 2, and the word Lane used when he asked for it to become a tracked thread (2026-09-21). "Chase" over the more common "pursue": it is plainer, and it keeps one English word across the decoy chase of ch. 2, the routs of chs. 7–11, the blood-avenger of 20:5 and "one of you chases a thousand" (23:10). Not yet formally locked. Flag it if a later unit wants "pursue". |
| naḥalah | לְ/נַחֲלָ֧ה (Josh 11:23) | **inheritance** | Locked 2026-09-16. Not "allotment" — that word belongs to this project's own "Allotment" movement title (`joshua_literary_unit_map.md`), a literary-map label, not a translation reason; using it here risked the choice running backward. "Inheritance" keeps the causative verb legible: `tanḥil` (1:6, causative of the same root) renders "cause to inherit" / "give as an inheritance," visibly matching the noun. |
| goel | מִ/גֹּאֵ֖ל (Josh 20:3) | **TODO** | Open. "Avenger" (of blood, its cities-of-refuge sense here) vs. the broader "redeemer" sense the same root carries elsewhere (Ruth, Job) — whether to render the same or differently by context is itself part of the open question. |
| nefesh | נַפְשֹׁתֵ֖י/נוּ (Josh 2:13) | **"life" / "being" by Hebrew grammatical number (Matthew's psychē rule), "person" for one bounded exception** | Locked 2026-09-21 (Lane: chose among life-fixed / being-fixed / life-being-context-dependent). 16 occurrences, not one register. **Rule A — self/address, matches Matthew exactly:** Hebrew singular → "life", Hebrew plural → "being(s)", never "soul" — 2:13 nafshoteinu (pl.) "our beings"; 2:14 nafsheinu (sg.) "our life"; 9:24 (pl.) "our beings"; 22:5 nafshekhem (sg., despite 2pl address — same idiom Matthew's rule already handles) "with all your heart and with all your life"; 23:11 (pl.) "your beings"; 23:14 (sg.) "your life." **Rule B — one documented exception, "person":** 10:28, 10:30, 10:32, 10:35, 10:37 (×2), 10:39, 11:11 (the ḥerem battle-report formula, "struck **the** [Heb. sg.] with the sword" — a generic-distributive singular for "every person," not one life) and 20:3, 20:9 (the cities-of-refuge law, "kills a person accidentally" — same generic-singular). Matthew's psychē has no occurrence in this register to borrow from: "he struck the life/being with the sword" is not idiomatic English and miscounts what's being described. This is a fixed, bounded rule (which verses take which rendering is settled here, not a per-verse call) — "context-dependent" only in the sense that Matthew's own rule already is. |
| y'all for 2pl | — | **y'all, always; possessives "y'all's"** | Locked 2026-09-16 (pronouns), extended 2026-09-22 (Lane, unit 3) to plural possessives ("Yahweh y'all's God," "y'all's children") — the drafted split kept possessives as plain "your"; Lane chose full consistency instead. 2nd-person-singular stays unmarked throughout. |
| ʾaron | הָ/אָר֞וֹן (Josh 3:3) | **chest** | Locked 2026-09-22 (Lane, unit 3, overriding the artifact's draft "ark"). First occurrence 3:3; "chest of the testimony" (4:16) kept as its own fixed phrase, same word. |
| berit | הַ/בְּרִית֙ (Josh 3:3) | **covenant** | Locked 2026-09-22 (Lane, unit 3). First occurrence 3:3, "chest of the covenant." |
| qadash (hitqaddeshu) | הִתְקַדָּ֑שׁוּ (Josh 3:5) | **set yourselves apart** | Locked 2026-09-22 (Lane, unit 3, chosen over "make yourselves holy" / "consecrate yourselves" / "sanctify yourselves"). Carries forward to 5:15 ("holy ground") and 7:13 (the Achan-lot command) — same root, watch how those render. |
| ʾerets | הָ/אָ֑רֶץ (Josh 3:11) | **land** (context-dependent; "earth" elsewhere) | Locked 2026-09-22 (Lane, unit 3) for "Lord of all the ʾerets" (3:11, 3:13) and "all the peoples of the ʾerets" (4:24) — chose "land" over the artifact's drafted "earth" to keep continuity with "the land" being given throughout the book. Not a blanket rule: revisit per occurrence where "earth" reads better (e.g. a cosmological sense, on the model of the `shamayim` split). |

## Log

- 2026-09-14: File created. Seeded the divine-name row (Yahweh, matches
  `hebrew.py`'s `OVERRIDES`); ḥerem, ḥesed, naḥalah, goel, nefesh, and the
  y'all-for-2pl question opened as TODO with no default filled in.
- 2026-09-16: naḥalah locked to "inheritance" (not "allotment" — that's the
  movement-title reason, not a translation reason). y'all-for-2pl locked to
  "always mark 2pl as y'all" — decided at unit 1 specifically because ch.1
  alternates singular/plural "you" and the alternation is meaningful.
- 2026-09-19: ʿeved locked to "slave", aligning with Matthew's doulos rule (platform review C10). Decision only — unit 1's prose and the `servant` thread gloss are unchanged and still need the rendering pass.
- 2026-09-19: ʿeved "slave" applied to unit 1 (5 occurrences) and the thread gloss updated; slug left as `servant`. shamayim locked to "sky/skies" everywhere (platform review C12), matching Matthew's ouranos rule — decided before unit 2 because Rahab's 2:11 is the first hit.
- 2026-09-21: ḥesed locked to left-untranslated-with-a-gloss (only 2 occurrences, both Rahab 2:12, a reciprocal loyalty pact rather than the word's usual divine register — same pattern as `torah`). nefesh locked to Matthew's psychē mechanism (life sg. / being pl.) for the self/address occurrences, with "person" as one documented exception for the ḥerem battle-formula and the cities-of-refuge law, where Matthew has no occurrence in that register to borrow from. Neither yet applied to unit 1 prose (unit 1 has no nefesh; ḥesed doesn't occur until unit 2).
- 2026-09-21 (part 2, unit 2 review): ḥerem locked to "devote(d) to destruction" (Lane, ahead of unit 5) — kept as an English phrase rather than transliterated since the verb form dominates the early occurrences and a transliterated verb reads far worse than a transliterated noun. Yam Suf locked to "Reed Sea" (Lane) over the traditional "Red Sea." Corrected the ḥesed row's occurrence count (3, not 2 — 2:12 ×2 + 2:14 ×1; the actual unit-02.html tagging was already right, only the glossary row was wrong).
- 2026-09-21 (part 5): radaf row added — "chase / the chasers", the rendering unit 2 already used, recorded when the root became the `chase` tracked thread. In use, not yet formally locked.
- 2026-09-22 (unit 3 port): 5 wording calls locked (Lane) and applied to `source-artifacts/joshua_03_translation.html` before porting — ʾaron → "chest" (not the artifact's drafted "ark"), berit → "covenant", qadash/hitqaddeshu (3:5) → "set yourselves apart", ʾerets → "land" at 3:11/3:13/4:24 (not "earth"), and y'all-for-2pl extended to possessives ("y'all's"). Also widened two tracked threads onto unit 3 occurrences: `rest` (5117) to include 3240, the causative "lay down" at 4:3/4:8; `strong` (2388) to include 2389, the adjective at 4:24 — both in `data/roots.json` and `data/threads.json`. Kept `sole`/`lodge`/`fear` as unit-3 local roots rather than promoting the artifact's book-wide candidates — promotion needs a hand-picked tracked-thread colour (Lane's call), left open rather than decided silently.
