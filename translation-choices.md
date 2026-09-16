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
| ḥerem | חֵ֛רֶם (Josh 6:17) | **TODO** | Open. "Devoted to destruction" / "banned" / left untranslated ("ḥerem") are all live options — no default chosen. |
| ḥesed | חָ֑סֶד (Josh 2:12) | **TODO** | Open. "Steadfast love" / "kindness" / "loyalty" each lose something; no default chosen. |
| naḥalah | לְ/נַחֲלָ֧ה (Josh 11:23) | **inheritance** | Locked 2026-09-16. Not "allotment" — that word belongs to this project's own "Allotment" movement title (`joshua_literary_unit_map.md`), a literary-map label, not a translation reason; using it here risked the choice running backward. "Inheritance" keeps the causative verb legible: `tanḥil` (1:6, causative of the same root) renders "cause to inherit" / "give as an inheritance," visibly matching the noun. |
| goel | מִ/גֹּאֵ֖ל (Josh 20:3) | **TODO** | Open. "Avenger" (of blood, its cities-of-refuge sense here) vs. the broader "redeemer" sense the same root carries elsewhere (Ruth, Job) — whether to render the same or differently by context is itself part of the open question. |
| nefesh | נַפְשֹׁתֵ֖י/נוּ (Josh 2:13) | **TODO** | Open. "Life" / "soul" / "person" / left untranslated — famously resists any single fixed English equivalent; may end up context-dependent by deliberate choice rather than drift. |
| y'all for 2pl | — | **y'all, always** | Locked 2026-09-16. 2nd-person-plural address is always marked (e.g. "y'all"), 2nd-person-singular left unmarked — a fixed rule, not context-dependent, since Josh 1 alternates between singular "you" (Joshua) and plural "you" (the people / eastern tribes) and the alternation carries meaning that unmarked English would flatten. |

## Log

- 2026-09-14: File created. Seeded the divine-name row (Yahweh, matches
  `hebrew.py`'s `OVERRIDES`); ḥerem, ḥesed, naḥalah, goel, nefesh, and the
  y'all-for-2pl question opened as TODO with no default filled in.
- 2026-09-16: naḥalah locked to "inheritance" (not "allotment" — that's the
  movement-title reason, not a translation reason). y'all-for-2pl locked to
  "always mark 2pl as y'all" — decided at unit 1 specifically because ch.1
  alternates singular/plural "you" and the alternation is meaningful.
