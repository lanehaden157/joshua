# Session summary — 2026-09-24

**Done**
- Canon leads cited other books in Hebrew (WLC) numbering, e.g. Deut 29:8 for English 29:9. `canon_leads.fmt_ref()` now maps through `node_modules/morphhb/wlc/VerseMap.xml` (1,979 entries, 7 partial). Partial verses render as English ranges.
- New test; all 9 canon-leads checks pass. Regenerated leads for units 1–5.
- Audited existing echoes/notes (units, source artifacts, data): all already English-numbered.

**Takeaways**
- English numbering is the project standard for citations (Lane). VerseMap maps to KJV, which matches WEB and most English Bibles.

**Open**
- None. The project side may want to know the leads' numbering changed, in case notes were taken from an earlier sheet.
