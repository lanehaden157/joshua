# Joshua Study — Style Reference

> **The artifact contract.** What a unit artifact must contain and what it must
> not. `Claude_ai_chat_side_instructions.md` says how to work and points here; `resources.md` says
> what is on hand and what each source is good for; `CLAUDE.md` says how the
> repo behaves. Every rule lives in exactly one of the four.

This is a guide, not a spec to satisfy. Where a rule gives a reason, the reason
outranks the rule — Joshua is a different book and some of this will be wrong
for it. Rebuild what doesn't work.

The exceptions are marked **(learned)**. Each cost something to find, in Matthew
or in the Hebrew parser project, and says where. Read the source before relaxing
one.

A corollary that keeps this file short: **every rule here either has a check in
the pipeline or is a judgment call a human makes.** If a rule is neither, delete
it. Matthew documented an endnote-pairing rule nothing checked, accepted two
meta fields nothing consumed, and stated a legend was optional when the site
required it.

---

## 1. Colour policy

One **Hebrew lexical root** per `data-root`: the root and its same-root forms,
nothing else. Never a theme, never a formula, never a bundle of different words.
Split a paired opposition into two roots. Drop a one-passage wordplay. Fixed
phrases the book repeats verbatim are the one exception and live in
`threads.json`.

A root's `translit` is the bare citation form only — `naḥal`, not `naḥalah ·
naḥal · tanḥil`. Tag **every** morphological occurrence with the one slug,
**including where the English renders it with a different word**. The tag
follows the lexeme, not the gloss.

**No inflected forms, no stem/binyan labels, in `translit` or `gloss` (2026-09-17,
Lane).** Lane doesn't want a list of "different Hebrew forms" or a `Qal:`/
`Hiphil:`/`noun:` tag cluttering the legend or a hover — he reads the plain
English gloss and works out the rest himself. `translit` is one bare root form;
`gloss` is a general, ungrammared definition (§3). A stem split (*yarash* Qal
"possess" vs. Hiphil "drive out" later in the book) is real information, but it
belongs in a thread's `note` or a verse's own `.gloss` popover — written out in
plain language, not as a grammatical label — when it's actually load-bearing for
that unit's translation choices, not pinned to the legend everywhere the root
appears.

Every slug must resolve to a colour: it appears in `threads-digest.md` or in
this artifact's own `roots[]`. A `data-root` that resolves to nothing is a hard
build failure. Declare tracked threads in `roots[]` too — redundant, harmless,
and it makes the array a reliable answer to "what does this unit track."

**Resist the richer taxonomy. (learned:** `8d096c9` built a two-tier root/motif
model across every file in the repo; `98b721a` reverted all of it the same day as
complexity the data didn't need. Hebrew's version of the temptation is root vs.
binyan vs. semantic field, and it will arrive around unit 3. The answer is the
same: one slug, one colour, the family spelled out in `translit`.**)**

---

## 2. Root identity — ids, not strings

**A root is a hand-curated set of Strong's ids in `roots.json`, and every tagged
occurrence of a tracked thread carries the OSHB word id it refers to.** No
Hebrew string is ever compared to another Hebrew string, anywhere in this
project.

### Why not substring stems

Measured against OSHB Joshua, matching each root's consonants as a substring:

| root | recall | precision |
|---|---|---|
| *lakad* "capture" | 100% | 100% |
| *ʿavar* "cross" | 95% | 68% |
| *natan* "give" | **42%** | 97% |
| *ḥaram* "devote" | 63% | 63% |
| *qum* "arise" | **24%** | 33% |
| *nakah* "strike" | **3%** | 100% |
| *Yehoshuaʿ* | **0%** | — |

Joshua's load-bearing verbs are weak roots. A stem list would silently miss most
of *natan*, nearly all of *nakah*, and the book's title character. That is the
exact failure the coverage audit exists to prevent.

### Why not bare lemmas either

One root routinely spans several Strong's numbers — *ḥaram* is 2763 (verb) and
2764 (noun), *naḥal* 5157/5159, *gevul* 1366/1367, *yareʾ* 3372/3373/3374 — and
one number sometimes bundles senses that want separating. So the root is a
**decision**, recorded in `roots.json` as a set of ids with a note. Adding
Hormah to the *ḥerem* root becomes a recorded judgment rather than a regex
accident.

Keep the lowercase letters on lemma ids (`834a`, `3588b`) in the data and strip
them at query time. They are not homograph markers — `834a` and `834d` are both
*ʾasher*. Their meaning is unverified; treat them as opaque.

### What the artifact does

Every span tagging a **tracked thread** carries the word id from
`Joshua-words.tsv`:

```html
<span class="r" data-root="devote" data-w="068w5">devoted</span>
```

Local roots — declared in this artifact's `roots[]` but not tracked threads —
don't need `data-w`; the audit counts those per verse.

The audit then does set arithmetic over ids: what the source has, minus what the
fragment tagged. Two things become loud that were previously silent — a wrong
word tagged inside a verse whose count happens to match, and a mistyped id,
which fails because the id's lemma isn't in the root's set.

**Never hand-type Hebrew. Always pull by word id. (learned:** the Hebrew parser
project's single strongest recommendation, and the reason maqqef, Unicode
normalization, final letter forms, and ketiv spelling never cost it anything.
NFC normalization alone reorders marks in 47% of Joshua's words, so any Hebrew
string that has passed through an editor will not byte-match the source.**)**

---

## 3. The hard contract

The artifact is **one `<article class="unit" data-unit="N">` and nothing else**.
No `<!doctype>`, `<html>`, `<head>`, `<body>`, `<style>`, `<link>`; no inline
`style="…"`; no `--c-*` colour variables. It opens with
`<script type="application/json" id="unit-meta">`.

**Unknown top-level keys are a hard error. (learned:** Matthew's research
project authored `descriptor` and `discourse` in every v2 artifact for eleven
units. Both were documented, both validated, both silently discarded, neither
consumed by anything. A field the pipeline drops is worse than a field that's
missing.**)**

### Top-level keys

| key | required | type | rule |
|---|---|---|---|
| `unit` | ✓ | int | an integer, not a string |
| `passage` | ✓ | str | `"Joshua 6:1–27"` |
| `title` | ✓ | str | |
| `roots` | ✓ | array | §1 |
| `threads` | ✓ | object | all four sub-keys, empty lists fine |
| `slug` | — | str | `"unit-06"`; derived from `unit` if omitted |
| `movement` | — | int | looked up from the Unit Map if omitted |

### `roots[]` — every entry `{root, translit, gloss}`

All three present and non-empty. `root` matches `[a-z0-9-]+` — no capitals,
underscores, or spaces. **No** `color`/`colour`: the site assigns colours. **No**
`kind`/`members`: that taxonomy was tried and reverted.

`gloss` is a short, general English definition — no stem/binyan label (`Qal:`,
`Hiphil:`, `Piel:`), no part-of-speech tag (`noun:`, `imperative:`). Lane reads
plain English and infers the grammar himself; a legend or hover cluttered with
that jargon is the opposite of what he wants (2026-09-17). Where a root
genuinely carries two different meanings across two stems — *yarash* in Joshua
is "drive out" in some occurrences and "take possession" in others — pick
whichever reads better as a single general gloss, or fold both into one
gloss without naming the stems (`"take possession; drive out"`), and put the
*why* (which occurrences, which stem, why it matters) in a thread's `note` or
the relevant verse's own `.gloss` popover instead. **(learned:** the parser
project glossed one string per lemma with no way to say "this root splits" at
all — the fix isn't a stem-labeled gloss, it's using the `note`/popover
channels that already exist for verse-specific nuance.**)**

Never seed a gloss from Strong's first definition. Sampled against Joshua
vocabulary it was misleading in 9 of 16 cases — *gevul* as "cord", *ḥaram* as
"seclude", *matteh* as "branch".

### `threads` — `{opens, payoffs, candidates, retro}`

All four keys present; each a list; empty lists allowed. "Required in the docs,
optional in the code" is how a research project learns to guess.

**`opens[]` / `payoffs[]`** — `{id, ref, note?}`. The artifact is the **only**
author of both; `threads.json` receives them through the thread delta. `id` must
already exist in `threads-digest.md`; propose new ones through `candidates`.
`ref` is the verse. `note` is the one-line popover prose for that beat, written
here, not only in the commentary.

> Matthew's `opens` was documented, validated, rendered into reports, and empty
> in every artifact, because openings were authored by hand in `threads.json`
> instead. Two paths, one dead. This keeps one.

**`candidates[]`** — `{root, why, ids?, refs?}`. Proposals only, never
auto-promoted. `root` matches `[a-z0-9-]+`; `why` is one line; `ids` are the
Strong's ids you actually observed in `Joshua-words.tsv` — evidence for Lane's
decision, not the decision itself, since assembling the id set for a root is his
call. `refs` are a few representative verses.

**`retro[]`** — `{unit, verse, text, root, why, nth?, op?, w?}`. Fixes for
**earlier** units: what the close reading of *this* unit made you notice about a
previous one. `unit` is a slug like `"unit-04"` and must not be this unit's own.
`why` is required. `op` ∈ `add` (default), `retag`, `retag_word`, `untag_word`,
`unwrap`, `strip_span`, `text`. The root it resolves to must be a tracked thread
or a declared root of the target unit. When `op` is `add`/`retag`/`retag_word`
and the target root is a **tracked thread**, `w` (the OSHB word id) is
required — that op creates or repoints a `data-root` span, and a tracked-thread
span must carry `data-w` same as any other (§7 checklist 7).

---

## 4. Components

A small vocabulary, deliberately. **Inventing a class is a decision, not a
formatting choice** — a new class needs CSS and a whitelist entry, and
`build.py` reports classes the stylesheet never mentions. Matthew accumulated
seven undocumented components across eleven artifacts; some got CSS after the
fact, some still render unstyled.

| component | shape | note |
|---|---|---|
| coloured word | `<span class="r" data-root="X" data-w="…">…</span>` | `data-w` required for tracked threads (§2). `class="rl"` only **outside** verse blocks — inside a `.v` block it's counted anyway, so `rl` there only mislabels intent (`394db71`). |
| verse | `<p class="v"><span class="n">17</span> …</p>` | one per verse, canonical order |
| gloss / compare | `<span class="gloss">…`, `<div class="compare">…` | **following siblings** of the verse, never nested inside it, never left unclosed around a following block |
| pericope heading | `<h3 class="pericope">Title <span>· 6:1–7</span></h3>` | the `· C:V` range is required. No `movement`/`panel`/`sectionhead` classes. |
| legend | `<section class="block legend" aria-label="color key"><ul></ul></section>` | **required, even as an empty stub** |
| notes | `<section class="block notes">` with bare `id="n3"` / `href="#n3"` | the porter prefixes ids per unit; every `href` must resolve to an `id` in the same fragment |

**The legend is required. (learned:** the style reference said it was optional
because "the site rebuilds it from data." It doesn't — `rebuildLegend()` *fills*
a legend the fragment already has and returns immediately if there is none.
Matthew's unit 11 shipped without one and the live site renders it with no colour
key. Nothing reported it.**)**

Never hand-write swatch dots or `style="background:…"`.

**`aside.echo`** — the one optional component, for cross-book echo: a Deuteronomy
command answered by a Joshua fulfilment, or the conquest summary against Judges
1. `<aside class="echo" data-anchor="C:V">`, a sibling of the verse, never
spliced inside an unclosed span. Ship it only when unit 1 actually wants it, and
ship its nesting-depth check in the same commit or don't ship it. **(learned:**
`67b2712` — a splice tool that didn't track open/close depth put eight asides
inside unclosed `.gloss` spans across six units; the renderer silently collapsed
them. Do **not** inherit Matthew's `aside.synoptic` and repurpose it; its check
is tuned to its own markup.**)**

---

## 5. Hebrew in English

**Transliteration** comes out of `pipeline/hebrew.py` and nowhere else. The
scheme in one sentence: *a diacritic only where the plain Latin letter is already
claimed by a different Hebrew letter*. So `ḥ ṭ ś` and the `ʾ`/`ʿ` pair, and no
vowel carries a mark.

- **No vowel length.** `mishpaṭ`, not `mišpāṭ`.
- **No spirantization.** `melek`, not `melekh`; `torah`, not `thorah`. A scheme
  that spells one root two ways defeats the colour system's whole claim. The
  parser project models b/k/p for pronunciation and says plainly it would not do
  so for a project like this one: *kol* comes out four ways there.
- **Dagesh forte doubles**: `hammelek`. And the sheva under a doubled consonant
  is **vocal**, so `hammelakim`, not `hamlakim` — the parser project's largest
  single sheva divergence, 242 words, and the one that makes a word look like a
  different word. Decide both together in unit 1 and log it.
- **`יהוה` transliterates as bare `YHWH`.** The English rendering is **Yahweh**
  (decided; `translation-choices.md` row 1).

**Overrides key on lemma id, not on codepoint.** U+05C7, the dedicated
qamats-qatan character, occurs **zero** times in the biblical text — a
codepoint-based rule would do nothing at all. Seed the override table with
3068/3069 (YHWH), 3389 (Jerusalem, which otherwise loses its second vowel and
comes out *yerushalam*), and 3605 (*kol*, which renders as *kal* in 185 of its
236 Joshua occurrences). Extend it when the log flags one.

Two implementation traps the parser project hit and paid for: the function must
handle phrases, not just single words — a verse passed through a one-word
transliterator silently lost every space — and word-initial shuruq is `u-`, not
`w-`.

**`ʾ` and `ʿ` are visually indistinguishable on a phone.** Wherever both appear
in a legend or gloss, distinguish them by something other than the mark alone.

**The scheme's authoritative definition is a test file of ~30 Joshua word ids and
their expected output.** Prose descriptions of it — here, in `hebrew.py`'s
docstring, in `CLAUDE.md` — are summaries and may drift; the parser project ended
up with three partly-contradictory descriptions of its own scheme. When they
disagree, the test file wins.

**Wording.** Before rendering a Hebrew lexeme in a new unit, check
`translation-choices.md` and match the prior decision. If a different rendering
genuinely fits better in a specific verse, use it — but **flag the deviation
explicitly in the artifact**, so Lane can decide whether it is a one-off or a
correction that should propagate. Same Hebrew root → same English root unless
flagged.

Any rendering decided or changed in a unit updates its row and the Log section
**in the same turn**, before moving on. **(learned:** Matthew started this file
at unit 10 and paid with a dedicated wording-audit session plus a retroactive
pass over everything already shipped — `b0f73cc`, `aed087e`, `0138548`.**)**

Seeded: the divine name → **Yahweh**. *TODO at unit 1: ḥerem, ḥesed, naḥalah,
goel, nefesh, and whether `y'all` marks genuine second-person plurals.*

---

## 6. Judgment

The things no check can catch.

**Be tough on structures.** Chiasms and rings only when real and textually
verifiable. They are easy to invent and narrative invites pattern-matching that
isn't there. **(learned:** `e9105a5` cut eight previously-published chiastic
structures across seven units as over-reaching. Joshua's version of this failure
will look different — imposed symmetry on episodes rather than on discourses — so
carry the caution and expect a new shape.**)** Joshua hands you real structure
for free: 52 *petuḥah* and 42 *setumah* paragraph breaks are marked in the text.
Prefer what the Masoretes marked over what you noticed.

**`threads.json` and `roots.json` are policy Lane owns.** Nothing in the pipeline
writes either. Which recurring word matters enough to track book-wide, and which
Strong's ids belong to one root, are the two genuinely subjective judgments in
the system — and the two most tempting to automate.

**Names are joined by hand.** Wordplay between a place name and a root is real
(*Achor* / *ʿakar* at 7:25–26) but Strong's etymology field is unreliable:
*Gilgal* needs two hops to reach *galal*, and *Jericho* offers two guesses. Put
names into `roots.json` one at a time, with the reason. Note also that *Beth-el*
is two tagged words sharing one id, so a per-word count doubles it.

**Ask rather than guess** on design or scope.

---

## 7. Before saving — the checklist

1. One `<article>`, nothing above or below it.
2. Meta block parses as JSON. All required keys, all four `threads` sub-keys, no
   unknown top-level keys.
3. Every `roots[]` entry has `root` + `translit` + `gloss`; `root` is
   `[a-z0-9-]+`; no `color`, no `kind`, no `members`; `translit` is the bare
   root form only, `gloss` is plain-English with no stem/binyan or
   part-of-speech label (§1, §3).
4. Every `opens`/`payoffs` `id` exists in `threads-digest.md` and carries a
   `note`.
5. Every `retro` entry targets an earlier unit, carries a `why`, and its root
   resolves; a `retro` entry that adds/retags onto a tracked thread carries a
   valid `w`.
6. Every `data-root` slug is in `threads-digest.md` or in this artifact's
   `roots[]`.
7. Every tracked-thread span carries a `data-w` id copied from
   `Joshua-words.tsv` — including where the English renders the root with an
   unexpected word.
8. Legend section present, stub or filled.
9. Every pericope heading carries its `· C:V` range.
10. `.gloss` / `.compare` are following siblings, all closed.
11. Every endnote `href` resolves to an `id` in the file.
12. **Zero native Hebrew anywhere in the file — no exceptions, attribute values
    included.**
13. No inline `style`, no `--c-*` vars, no per-root class names, no class the
    stylesheet doesn't know.
14. Wording matches `translation-choices.md`, or the deviation is flagged.

Save as `joshua_NN_translation.html`, zero-padded, and present the file. It
renders unstyled in chat — expected.

---

## 8. Worked example

Minimal and valid. Copy its shape.

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
    { "root": "give",   "translit": "natan", "gloss": "give, hand over" }
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
hand."</p>
<span class="gloss"><em>have given</em> —
<span class="rl" data-root="give">natan</span> in the perfect: the gift is spoken
as already accomplished.<sup class="en"><a href="#n1">1</a></sup></span>

<section class="block notes">
  <h2>Notes</h2>
  <p id="n1">On the prophetic perfect, and why the English tense choice matters.</p>
</section>
</article>
```

---

## 9. The Literary Unit Map

*TODO — required before unit 1. Renumbering after units ship means editing
`threads.json` opens and payoffs, every `retro` entry, and every fragment's meta
block.*

Needs, per unit: number, slug, passage, working title, movement. Plus, at the
top: the movement list, and every place a literary unit deliberately disagrees
with the chapter grid, stated once so no artifact re-derives it.

Two free inputs. OSHB marks 52 *petuḥah* (`<seg type="x-pe">`) and 42 *setumah*
(`x-samekh`) paragraph breaks in Joshua — candidate boundaries the tradition
already drew. And Joshua has 658 verses in OSHB with chapter 21 at 45, meaning
21:36–37 are present and unmarked; check that against a printed BHS before the
map treats chapter 21 as settled.
