# Joshua Study — Style Reference

> **The artifact contract.** What a unit artifact must contain and must not.
> `Claude_ai_chat_side_instructions.md` says how to work; `resources.md` says
> what's on hand; `CLAUDE.md` says how the repo behaves. Each rule lives in one
> of the four.

A guide, not a spec: where a rule gives a reason, the reason outranks the rule.
Rules marked **(learned)** cost something to find — read the cited source
before relaxing one. Every rule here either has a pipeline check or is a human
judgment call; if it's neither, delete it.

---

## 1. Colour policy

One **Hebrew lexical root** per `data-root` — the root and its same-root forms,
never a theme or a bundle of words. Split a paired opposition into two roots;
drop a one-passage wordplay. Fixed phrases the book repeats verbatim are the one
exception and live in `threads.json`.

Tag **every** occurrence with the one slug, **including where the English uses a
different word** — the tag follows the lexeme, not the gloss.

`translit` is one bare root form (`naḥal`, not `naḥalah · naḥal · tanḥil`);
`gloss` is plain English (§3). No inflected-form lists, no stem/binyan labels
(Lane, 2026-09-17). A stem split that matters (*yarash* "possess" vs. "drive
out") goes in a thread `note` or a verse `.gloss`, in plain language.

Every slug must resolve — in `threads-digest.md` or this artifact's `roots[]` —
or the build fails. Declare tracked threads in `roots[]` too.

**Tag notable words even when they aren't threads (Lane, 2026-09-17).** A single
striking translation choice in a single verse earns a `data-root` span and a
full `{root, translit, gloss}` entry (unit 1: *insight*, *murmur*, *shatter*,
*man of valor*). Read for these deliberately, the way you read for structure
(§6).

**`example`** — optional fourth field on any root: one short quoted clause from
the unit's own English, no citation. Add it when context clarifies the choice
faster than the gloss.

**Resist a richer taxonomy. (learned:** `8d096c9` built a root/motif two-tier
model; `98b721a` reverted it the same day. Hebrew's version — root vs. binyan
vs. semantic field — gets the same answer: one slug, one colour.**)**

---

## 2. Root identity — ids, not strings

**A root is a hand-curated set of Strong's ids in `roots.json`; every tracked
thread occurrence carries its OSHB word id.** No Hebrew string is ever compared
to another.

### Why not substring stems

Consonant-substring matching against OSHB Joshua:

| root | recall | precision |
|---|---|---|
| *lakad* "capture" | 100% | 100% |
| *ʿavar* "cross" | 95% | 68% |
| *natan* "give" | **42%** | 97% |
| *ḥaram* "devote" | 63% | 63% |
| *qum* "arise" | **24%** | 33% |
| *nakah* "strike" | **3%** | 100% |
| *Yehoshuaʿ* | **0%** | — |

Joshua's load-bearing verbs are weak roots.

### Why not bare lemmas either

One root often spans several Strong's numbers (*ḥaram* 2763/2764, *naḥal*
5157/5159, *yareʾ* 3372–3374), and one number can bundle senses worth splitting.
So a root is a **decision**, recorded as an id set with a note.

Lowercase suffixes on ids (`834a`) are kept in data, stripped at query time, and
treated as opaque — not homograph markers.

### What the artifact does

Tracked-thread spans carry the word id from `Joshua-words.tsv`:

```html
<span class="r" data-root="devote" data-w="068w5">devoted</span>
```

Local roots don't need `data-w`. The audit does set arithmetic over ids, so a
wrong word or mistyped id fails loudly.

**Never hand-type Hebrew; pull by word id. (learned:** Hebrew parser project —
NFC normalization alone reorders marks in 47% of Joshua's words.**)**

---

## 3. The hard contract

The artifact is **one `<article class="unit" data-unit="N">` and nothing
else** — no doctype/html/head/body/style/link, no inline `style`, no `--c-*`
vars. It opens with `<script type="application/json" id="unit-meta">`.

**Unknown top-level keys are a hard error. (learned:** Matthew's `descriptor`
and `discourse` were authored for eleven units and silently discarded.**)**

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

### `roots[]` — every entry `{root, translit, gloss, example?}`

`root` matches `[a-z0-9-]+`. **No** `color`/`colour` (the site assigns colours),
**no** `kind`/`members` (tried and reverted).

`gloss` is a short general definition — no `Qal:`/`Hiphil:`, no `noun:`. Where a
root splits across stems, fold both senses into one gloss without naming stems
(`"take possession; drive out"`) and put the why in a `note` or `.gloss`.

Never seed a gloss from Strong's first definition — misleading in 9 of 16
sampled Joshua words (*gevul* "cord", *ḥaram* "seclude").

### `threads` — `{opens, payoffs, candidates, retro}`

All four present, each a list, empty allowed.

**`opens[]` / `payoffs[]`** — `{id, ref, note}`. The artifact is the only author
of both. `id` must exist in `threads-digest.md` (propose new ones via
`candidates`); `note` is the one-line popover prose. **(learned:** Matthew's
`opens` stayed empty because openings were hand-authored elsewhere — two paths,
one dead.**)**

**`candidates[]`** — `{root, why, ids?, refs?}`. Proposals only. `ids` are the
Strong's ids you actually saw — evidence, not the decision. `refs` are a few
representative verses.

**`retro[]`** — `{unit, verse, text, root, why, nth?, op?, w?}`. Fixes for
**earlier** units (`unit` is a slug like `"unit-04"`, never this unit). `why`
required. `op` ∈ `add` (default), `retag`, `retag_word`, `untag_word`, `unwrap`,
`strip_span`, `text`. The root must resolve to a tracked thread or a declared
root of the target unit. `add`/`retag`/`retag_word` onto a tracked thread
requires `w`.

---

## 4. Components

Deliberately small. **A new class is a decision** — it needs CSS and a
whitelist entry, and the build reports unknown classes.

| component | shape | note |
|---|---|---|
| coloured word | `<span class="r" data-root="X" data-w="…">…</span>` | `data-w` required for tracked threads (§2). `class="rl"` only **outside** verse blocks (`394db71`). |
| verse | `<p class="v"><span class="n">17</span> … text<sup class="en"><a href="#n1">1</a></sup></p>` | one per verse, in order. The endnote marker is the last thing in the verse `<p>`, **never** inside the `.gloss` |
| gloss | `<span class="gloss">…</span>` | **following sibling** of the verse, never nested, always closed. Word-by-word translation discussion, collapsed behind the per-verse `*` toggle |
| pericope heading | `<h3 class="pericope">Title <span>· 6:1–7</span></h3>` | `· C:V` range required |
| legend | `<section class="block legend" aria-label="color key"><ul></ul></section>` | **required, even as an empty stub** |
| notes | `<section class="block notes"><ol><li id="n3">…</li></ol></section>` | real `<ol><li>`; every `href` resolves to an `id` in the fragment |

**(learned, 2026-09-17:** endnote markers inside `.gloss` hid the footnote behind
the toggle.**)** **(learned:** the legend was once "optional" — `rebuildLegend()`
only fills an existing one, and Matthew's unit 11 shipped with no colour key.**)**

Never hand-write swatches or `style="background:…"`.

**`aside.echo`** — optional, unbuilt: cross-book echo (Deuteronomy command →
Joshua fulfilment; conquest summary vs. Judges 1). `<aside class="echo"
data-anchor="C:V">`, a verse sibling. Ship it only with its nesting-depth check.
**(learned:** `67b2712` — asides spliced inside unclosed `.gloss` spans silently
collapsed.**)**

**Voice: no named commentators or resources, and no project-internal
references, anywhere in fragment prose (Lane, 2026-09-17).** Not "Dozeman
argues," not a Targum by name, not `Joshua-words.tsv` or a lemma id. Where views
differ, say so in general terms ("one reading," "scholars read this two ways")
and give the content of the disagreement. Research still uses real scholarship;
the fragment just stands alone. **(learned:** unit 1's first draft named eight
sources and two repo files in reader-facing prose.**)**

---

## 5. Hebrew in English

**Transliteration** comes only from `pipeline/hebrew.py`. Scheme: a diacritic
only where the plain letter is already claimed (`ḥ ṭ ś`, `ʾ`/`ʿ`); no vowel
marks.

- **No vowel length** (`mishpaṭ`).
- **No spirantization** (`melek`, `torah`) — one root, one spelling.
- **Dagesh forte doubles**, and sheva under it is vocal: `hammelakim`.
- **`יהוה` → `YHWH`**; the English rendering is **Yahweh**.

Overrides key on **lemma id**, not codepoint (U+05C7 occurs zero times). Seeded:
3068/3069 (YHWH), 3389 (Jerusalem), 3605 (*kol*).

`ʾ` and `ʿ` look identical on a phone — distinguish them by more than the mark.

**The test file is the scheme's authoritative definition**; prose summaries
drift.

**Translation philosophy.** The verse text is a fresh, wooden-but-readable
rendering from the Hebrew, not a polish of an existing English version.
Creative, intentional glosses are encouraged — the goal is understanding, not
conformity to traditional renderings.

**Wording.** Check `translation-choices.md` before rendering a lexeme and match
prior decisions. A better verse-specific rendering is fine — **flag the
deviation in the artifact** so Lane can decide one-off vs. correction. Update the
file's row and Log **in the same turn**. **(learned:** Matthew started this file
at unit 10 and paid with a retroactive audit — `b0f73cc`, `aed087e`,
`0138548`.**)**

*Open at unit 1: ḥerem, ḥesed, naḥalah, goel, nefesh, and whether `y'all` marks
second-person plurals.*

---

## 6. Judgment

**Be tough on structures.** Chiasms and rings only when textually verifiable.
Prefer the Masoretic paragraph breaks (52 *petuḥah*, 42 *setumah*) over patterns
you noticed. **(learned:** `e9105a5` cut eight over-reaching chiasms.**)**

**`threads.json` and `roots.json` are Lane's policy.** Nothing in the pipeline
writes either.

**Names are joined by hand.** Place-name wordplay is real (*Achor* / *ʿakar*,
7:25–26) but Strong's etymology is unreliable (*Gilgal*, *Jericho*). Add names
to `roots.json` one at a time, with the reason. *Beth-el* is two tagged words
sharing one id.

**Ask rather than guess** on design or scope.

---

## 7. Before saving — the checklist

1. One `<article>`, nothing above or below it.
2. Meta parses as JSON; required keys and all four `threads` sub-keys; no
   unknown top-level keys.
3. Every `roots[]` entry: `root` (`[a-z0-9-]+`) + bare `translit` + plain
   `gloss`, optional `example`; no `color`/`kind`/`members`, no stem or
   part-of-speech labels.
4. Every notable translation choice has a local span and `roots[]` entry (§1).
5. Every `opens`/`payoffs` `id` is in `threads-digest.md` and has a `note`.
6. Every `retro` targets an earlier unit, has a `why`, resolves, and carries
   `w` when adding/retagging onto a tracked thread.
7. Every `data-root` is in `threads-digest.md` or `roots[]`.
8. Every tracked-thread span has a `data-w` from `Joshua-words.tsv`.
9. Legend present, stub or filled.
10. Every pericope heading has its `· C:V` range.
11. `.gloss` blocks are closed following siblings.
12. Every endnote `href` resolves to an `id` in the file.
13. **Zero native Hebrew anywhere — attribute values included.**
14. No inline `style`, no `--c-*` vars, no class the stylesheet doesn't know.
15. Wording matches `translation-choices.md`, or the deviation is flagged.
16. No named commentator or project-internal reference in prose (§4).

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
hand."<sup class="en"><a href="#n1">1</a></sup></p>
<span class="gloss"><em>have given</em> —
<span class="rl" data-root="give">natan</span> in the perfect: the gift is spoken
as already accomplished.</span>

<section class="block notes">
  <h2>Notes</h2>
  <ol>
  <li id="n1">On the prophetic perfect, and why the English tense choice matters.</li>
  </ol>
</section>
</article>
```

---

## 9. The Literary Unit Map

Done — see `joshua_literary_unit_map.md` (24 units, 4 movements, confirmed by
Lane). Renumbering after units ship means editing `threads.json` opens/payoffs,
every `retro` entry, and every fragment's meta block.
