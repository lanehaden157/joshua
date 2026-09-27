# Joshua Study — Resources

> **Single authored copy.** This file lives in the repo and reaches the
> Claude.ai project through the synced folder, like the text files below.
> Edit it in the repo; the sync picks up the change on its own.
>
> **This file says what is on hand and what each thing is good for. It does not
> say how to work** — that lives directly in the project's instructions field,
> not a separate synced file — **and it does not say what to produce** —
> that's `joshua_study_style_reference.md`. If you find yourself wanting to
> duplicate a rule from either into here, don't.
>
> **The commentary list below is exhaustive.** Nothing else is available. Don't
> cite a commentary that isn't here, and don't imply coverage you don't have.

---

## 1. Text and data

**Everything in this section is synced from the repo, under
`project-side/synced/`.** Synced files will **not** appear in a plain file
listing or directory tool. That's expected, not a sign a file is missing:
search project knowledge by filename or a distinctive phrase before
concluding it isn't there. Only the commentaries (§2) are plain project
attachments.

- `Joshua-reading.txt` (was `Joshua-Hebrew.txt` as a project attachment) —
  pointed Hebrew, `Josh C:V<TAB>text`. For quoting. No paragraph markup of
  any kind (see below) and still carries OSHB's morpheme slashes (e.g.
  `וְ/כָל`); strip before quoting a phrase.
- `Joshua-english.txt` — WEB-classic English verse text. A baseline reference,
  not this study's own translation. Renders the divine name as Yahweh,
  matching `translation-choices.md` row 1.
- `joshua_literary_unit_map.md` — the 24-unit/4-movement structural map
  (Entry, Conquest, Allotment, Epilogue). State the unit and passage from here
  before each walkthrough; flag any divergence from the chapter grid. Chs.
  1–9 are checked against the Masoretic *petuḥah*/*setumah* breaks (see
  `candidate-boundaries.md`, below); chs. 10–24 rest on Hawk and Dozeman's
  structural outlines rather than hand-verification.
- `candidate-boundaries.md` — every *petuḥah* (open) and *setumah* (closed)
  paragraph break in Joshua, 94 in all (52 + 42), in order, from the same
  pinned OSHB text as `Joshua-reading.txt`. Each row names the verse the break
  **follows**. A raw list, not an interpretation: use it to test a unit
  boundary against the Masoretic paragraphing, and say so when a unit cuts
  across a break or a break falls mid-unit. `Joshua-reading.txt` itself
  carries no paragraph markup, so this file is the place to look.
- `Joshua-words.tsv` — one row per word: OSHB word id, ref, surface form,
  lemma, morph. **This is what you read ids off when tagging.** Generated
  from the same pinned morphhb release as `Joshua-reading.txt`; if the two
  disagree, stop and tell Lane rather than working around it.
- `threads-digest.md` — the tracked threads, generated from the site's
  `data/threads.json`. The source of truth for which roots are tracked, the
  `data-root` slug each uses, and the lemma ids each covers. Nothing about
  threads lives in project memory.
- `translation-choices.md` — the wording glossary. Check before rendering a
  Hebrew lexeme; match the prior decision or flag the deviation explicitly.
- `joshua_study_style_reference.md` — the artifact contract. Read before
  pass 4 (the artifact).
- `canon-leads-unit-NN.md` — one per unit: where the unit's rare words and
  Torah-shared phrases occur elsewhere in the Hebrew Bible. The starting list
  for the intertext pass.
- `roots.json` — the lemma id set behind each tracked thread.
- `resources.md` — this file.

---

## 2. The commentary set

State where readings diverge and why; don't let one silently displace another.

### Hawk, *Joshua* (Berit Olam)
`dokumen_pub_berit-olam-joshua-*.txt`

The closest thing here to this project's lens, and the first stop in passes 1
and 2: narrative art, type-scenes, the boundary-and-identity theme, the ḥerem
discussion. Text is clean, but his transliterations are glyph-damaged (ḥerem
prints as `˙∑rem`). Re-derive every Hebrew form from `Joshua-words.tsv`. Never
copy one out of this file.

### Dozeman, *Joshua* (Anchor Yale, 2015 / 2023)
`dozeman_vol1_fixed.txt` (chs. 1–12) · `AYBC_-_6_2__Iosue_13_24__*.txt` (chs. 13–24)

The technical anchor: LXX text criticism, composition history, geography. Vol 2
is the only real coverage of the allotment chapters anywhere in this set.

**Use `dozeman_vol1_fixed.txt` only.** The original vol 1 PDF had its digits
mapped to private-use codepoints, so every chapter and verse number extracted
blank. If a vol 1 quotation ever comes through as `Josh :–`, it's the wrong
file — say so rather than reconstructing the reference.

### Rashi (Metsudah 1997, via Sefaria)
`Rashi_on_Joshua_-_en_-_merged.txt`

All 24 chapters, ~630 verse entries. The midrashic and intertextual voice, often
hearing a Torah echo before a critical commentary names it. Raw Sefaria export:
it contains native Hebrew script and ~2,100 HTML tags, so strip the markup and
transliterate anything quoted.

### Radak (Sefaria, Hebrew only)
`Radak_on_Joshua_-_he_-_Radak_on_Nach.txt`

All 24 chapters, 610 verse entries, digital text rather than a scan. The
grammarian of this set: roots, binyanim, the force of a waw at the head of a
clause, comparisons with Targum Yonatan. His first comment in the book is on why
Joshua opens with a waw, which tells you the register.

**There is no English in this file**, which makes Radak the one source Lane
cannot check against a published rendering. So whenever he is used:

- present the content as a rendering rather than a citation;
- give the transliterated Hebrew phrase he is commenting on alongside the gloss;
- say so when an abbreviation or a compressed construction leaves the sense
  genuinely uncertain, instead of smoothing it over.

Raw Sefaria export — native script throughout and ~860 HTML tags, so strip the
markup and transliterate everything that reaches the page.

---

## 3. Gaps — name them out loud, don't paper over them

There is no evangelical verse-level volume (Hess, Howard, Butler), no Alter, no
Origen, and no dedicated treatment of the ethics (McConville, Moberly, Earl).
Younger's *Ancient Conquest Accounts* — the ANE control for Assyrian, Hittite,
and Egyptian conquest rhetoric, and the closest thing this set had to direct
coverage of Joshua 9–12 — was on hand but is gone for good; don't cite it and
don't reconstruct its arguments from Dozeman's summaries of it.

Where a unit turns on something this set can't reach, search the web during pass
2 and say that's what you're doing. Do not stretch Hawk or Dozeman past what
they actually argue to cover a hole.
