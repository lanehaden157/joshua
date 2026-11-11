# Joshua Study — Style Reference

Joshua's differences from `fragment-contract.md` (shared, read first). This
file wins.

## Components

On: echo, story (`book.json` `"components"`; markup in
`components-reference.md`).

- **echo** (`aside.echo`): verse-level cross-book link.
- **story** (`aside.story`): a *different, earlier* event told beside a verse.
- Root `echo`: a word with a canon history gets at least a local root with an
  `echo`, even if tagged nowhere else in the unit. *Sole of the foot* at 1:3 →
  Gen 8:9 and Deut 11:24; *scarlet* at 2:18 → Gen 38:28–30; *dread* at 2:9 →
  Exod 15:16.

## What belongs where

Each link lives in exactly one place:

| The link is… | It goes in |
|---|---|
| A word's history across books | root `echo` |
| One verse or phrase elsewhere sounding through this verse; one sentence says it | `aside.echo` |
| A different earlier event with the same shape, where the reader needs the background | `aside.story` |
| A direct quotation of earlier Scripture | `intertext[]`, kind `quotation` |
| A contested reading, an argument about a link, a debate that needs room | footnote |

A story box holds its own word-level evidence: no echo for the same link. The
conquest-summary tension with Judges 1 is a footnote or an echo. Story boxes
are harvested like echoes: don't repeat them in `intertext[]` or
`typescenes[]`. Every story box tells the story, states a difference, says
what it does here.

**Handoff box kinds:** story → `aside.story`; echo → `aside.echo`; type-scene
→ the story box's `data-scene` when it is told, otherwise a `typescenes[]`
entry; intertext and quotations → `intertext[]`. No OT pointer or
parallel/synoptic box in Joshua: footnote or echo.

Footnotes have room: a grammar point, a variant, a debate, archaeology. A
form that only *looks* odd (masculine suffix, singular object, Ketiv/Qere) →
footnote or left out.

## Hebrew in English

**Transliteration** comes only from core's Hebrew adapter
(`biblecore/lang/hebrew.py`): diacritic only where the plain letter is already
claimed (`ḥ ṭ ś`, `ʾ`/`ʿ`); no vowel length (`mishpaṭ`); no spirantization
(`melek`, `torah`); dagesh forte doubles, sheva under it vocal (`hammelakim`);
divine name `YHWH`, rendered **Yahweh**. `ʾ` and `ʿ` look identical on a
phone: distinguish them by more than the mark.

**Translation.** Fresh, wooden-but-readable rendering from the Hebrew, not a
polish of an existing English version. Creative, intentional glosses
encouraged. A stem split that matters (*yarash* "possess" vs. "drive out"):
fold both senses into one gloss without naming stems; the why goes in a
`note` or `.gloss`.

**Ids.** Bare id (`2416`) claims every lexeme under the number: the default.
Suffixed id (`2416e`) claims exactly one: use it when the number bundles
different words. In Joshua the split is real in three places: `3885a` *lodge*
vs `3885b` *murmur*; `2416a` *alive* vs `2416e` *life*; `6924a` *front* vs
`6924b` *eastward* (the boundary formula of the allotment). A `+` suffix
(`1007+`) is the corpus's multi-word-name marker, always stripped. A suffixed
id the corpus never carries is a hard error.

## Judgment

- Structure markers: Masoretic paragraph breaks (`candidate-boundaries.md`; 52
  *petuḥah*, 42 *setumah*) over patterns you noticed.
- Names are joined by hand: place-name wordplay is real (*Achor* / *ʿakar*,
  7:25–26), Strong's etymology unreliable (*Gilgal*, *Jericho*). Names go into
  `roots.json` one at a time, with the reason. *Beth-el* is two tagged words
  sharing one id.
- Still open: goel.

## 8. Worked example

Joshua's own; wins over the shared contract's.

```html
<article class="unit" data-unit="6">
<script type="application/json" id="unit-meta">
{
  "unit": 6,
  "slug": "unit-06",
  "passage": "Joshua 6:1–27",
  "title": "The City Given, the City Devoted",
  "movement": 2,
  "roots": [
    { "root": "devote", "translit": "ḥaram", "gloss": "devote irrevocably, put to the ban" },
    { "root": "give",   "translit": "natan", "gloss": "give, hand over",
      "echo": "Gen 12:7 — 'to your seed I will give this land,' the first promise to Abraham" }
  ],
  "threads": {
    "opens": [
      { "id": "devote", "ref": "6:17",
        "note": "the first ḥerem of the conquest — the city is not plunder but offering" }
    ],
    "payoffs": [
      { "id": "give", "ref": "6:2",
        "note": "'I have given Jericho into your hand' — the gift spoken as done before the walls move" }
    ],
    "candidates": [
      { "root": "shout", "why": "teruʿah at 6:5 and 6:20, and again at 1 Sam 4:5 — a war-cry that is also a liturgical shout",
        "ids": ["8643", "7321"], "refs": ["6:5", "6:20"] }
    ],
    "retro": [
      { "unit": "unit-05", "verse": 14, "text": "commander", "root": "devote",
        "w": "06UrB",
        "why": "the sar of Yahweh's army at 5:14 sets up the ḥerem claim; untagged" }
    ]
  }
}
</script>

<header class="mast">
  <div class="kicker">The Book of Joshua · Study Translation</div>
  <h1>The City Given, the City Devoted</h1>
  <div class="unit">Unit 6 · Joshua 6:1–27</div>
</header>

<section class="block legend" aria-label="color key"><ul></ul></section>

<h3 class="pericope">The Sealed City <span>· 6:1–5</span></h3>

<p class="v"><span class="n">1</span> Now Jericho was shut up tight, shut in
because of the sons of Israel — no one going out, no one coming in.</p>

<p class="v"><span class="n">2</span> And Yahweh said to Joshua, "See, I have
<span class="r" data-root="give" data-w="06Fu4">given</span> Jericho into your
hand."<sup class="en"><a href="#n1">1</a></sup></p>
<span class="gloss"><em>have given</em> —
<span class="rl" data-root="give">natan</span> in the perfect: the gift is spoken
as already accomplished.</span>

<div class="notes">
  <h2>Notes</h2>
  <ol>
  <li id="n1"><strong>have given (v2).</strong> On the prophetic perfect, and why the English tense choice matters.</li>
  </ol>
</div>
</article>
```

## Unit map

`joshua-literary-unit-map.md`: 24 units, 4 movements (Entry, Conquest,
Allotment, Epilogue), confirmed by Lane. `book.json` `groupings` =
`["movement"]`. Renumbering after units ship means editing `threads.json`
opens/payoffs, every `retro` entry and every fragment's meta block: ask Lane
first.
