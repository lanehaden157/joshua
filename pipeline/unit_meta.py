"""The per-fragment metadata block: parse, validate, generate.

Hebrew fork of Projects/Matthew/pipeline/unit_meta.py -- same role and
shape (opens/payoffs/candidates/retro thread bookkeeping embedded in a
unit fragment). Reworked for phase-0.6-plan.md §F to match
joshua_study_style_reference.md exactly (§3 the hard contract, §4
components, §7 the checklist) -- this fork had drifted from the style
reference on several points (descriptor/discourse still allowed,
candidates[].stems exemption from the no-Hebrew check contradicting
checklist 12's "no exceptions", kind/members not rejected on roots[],
opens/payoffs not requiring a note) before this rework closed them.

Every fragment carries, right after <article class="unit" …>, a block:

    <script type="application/json" id="unit-meta">
    { …the JSON below… }
    </script>

Shape (style reference §3):
  unit       int      unit number
  slug       str      "unit-09"            (derived if absent)
  passage    str      "Joshua 9:1-27"
  title      str
  movement   int                           (optional; looked up from units.json)
  roots      [ {root, translit, gloss} ]
             every coloured root the unit tracks — translit + gloss ONLY, NO
             colour, no kind/members (that taxonomy was tried and reverted,
             style reference §1).
  threads    { opens:[{id,ref,note}], payoffs:[{id,ref,note}],
               candidates:[{root,why,ids?,refs?}],
               retro:[{unit,verse,text,root,why,nth?,op?,w?}] }
             All four sub-keys required, each a list, empty lists fine.
             opens/payoffs `note` is required (the popover line for that
             beat). candidates PROPOSE new threads (never written
             automatically); `ids` are Strong's/lemma ids actually observed
             in Joshua-words.tsv (evidence for Lane's decision, not the
             decision itself -- style reference §2/§6), `refs` are a few
             representative C:V verses. NOT `stems`/`exclude` -- that was
             this fork's own pre-style-reference design (substring-stem
             matching, phase-0.6-plan.md §1) and is rejected here now.
             `retro`'s `w` (an OSHB word id) is REQUIRED when `op` is
             `add`/`retag`/`retag_word` and the target root is a tracked
             thread -- that op creates or repoints a `data-root` span, and
             a tracked-thread span must carry `data-w` same as any other
             (checklist 7). Local-root retro fixes need no `w`.
             All of opens/payoffs/candidates/retro are consumed by the
             porter and dropped — generate() rebuilds the block from the
             data files, so none of this reaches the rendered page.

ALLOWED_TOP_LEVEL_KEYS below is the complete, closed set of authorable
top-level keys -- `descriptor`/`discourse` are NOT in it (style reference
§3's table has no such keys; Matthew shipped them as documented-but-
silently-dropped fields across eleven units before it added this check).
A key present in a fragment's meta block but not in that set is a HARD
validate() failure, not a warning -- see validate()'s docstring. Note that
being in ALLOWED_TOP_LEVEL_KEYS only means validate() won't reject the key
-- generate() below still has to be taught to round-trip it, or it's
dropped the moment a unit's block gets regenerated. That's a second,
separate failure mode this file does not yet close; don't assume
"validate() allows it" means "it survives a regen."

This module is the single definition meant to be shared by whatever
Joshua's future port_artifact.py/build.py end up being (neither exists
yet -- this is written ahead of them, same reasoning as
verify_thread_coverage.py being written ahead of the first thread
generator).
"""

import json
import os
import re
import unicodedata

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data")
CSS = os.path.join(ROOT, "css", "styles.css")

BLOCK_RE = re.compile(
    r'[ \t]*<script type="application/json" id="unit-meta">\s*'
    r'(\{.*?\})\s*</script>\n?',
    re.S,
)
ARTICLE_RE = re.compile(r'(<article class="unit"[^>]*>\n?)')


# ---------------------------------------------------------------- load helpers

def _load(name):
    return json.load(open(os.path.join(DATA, name), encoding="utf-8"))


def _unit_row(units_json, n):
    for u in units_json["units"]:
        if u["n"] == n:
            return u
    return None


# ---------------------------------------------------------------- parse

def parse(html):
    """Return the metadata dict from a fragment string, or None if absent."""
    m = BLOCK_RE.search(html)
    if not m:
        return None
    return json.loads(m.group(1))


def strip(html):
    """Remove an existing metadata block (used before re-injecting)."""
    return BLOCK_RE.sub("", html, count=1)


def inject(html, meta):
    """Insert / replace the metadata block immediately after the <article> tag."""
    html = strip(html)
    m = ARTICLE_RE.search(html)
    if not m:
        raise ValueError("fragment has no <article class=\"unit\"> open tag")
    body = json.dumps(meta, indent=2, ensure_ascii=False)
    block = f'<script type="application/json" id="unit-meta">\n{body}\n</script>\n'
    return html[:m.end()] + block + html[m.end():]


# ---------------------------------------------------------------- validate

REQUIRED = ("unit", "passage", "title", "roots", "threads")

# The complete, closed set of top-level keys a fragment's meta block may
# carry. Anything else is a hard validate() failure -- see module
# docstring. Extending this set is a deliberate schema change, not
# something a fragment author should be able to do just by typing a new
# key and having it silently pass.
ALLOWED_TOP_LEVEL_KEYS = {
    "unit", "slug", "passage", "title", "movement", "roots", "threads",
}

# threads must carry all four of these, each a list (style reference §3).
THREADS_SUBKEYS = ("opens", "payoffs", "candidates", "retro")

_ID_RE = re.compile(r"^\d+[a-z]?$")
_REF_RE = re.compile(r"^\d+:\d+$")
# OSHB word ids (Joshua-words.tsv's word_id column) are alphanumeric --
# deliberately not pinned to Joshua's own 5-character shape, so this stays
# book-agnostic for whatever forks this next (Judges).
_WORD_ID_RE = re.compile(r"^[0-9A-Za-z]+$")


def validate(meta, threads_json=None):
    """Return a list of human-readable problems ([] == clean). Every
    problem in this list is a hard build failure for whatever calls this
    (no separate warning tier) -- see check 1 below in particular."""
    errs = []
    if not isinstance(meta, dict):
        return ["metadata is not a JSON object"]

    # check 1: unknown top-level keys are a hard failure, not a warning.
    # This is the check that didn't exist for Matthew until after
    # "descriptor" and "discourse" had already shipped, undetected,
    # across eleven units -- both documented in that project's own
    # unit_meta.py docstring, neither ever wired into generate()'s
    # rebuild, so every regen silently dropped them.
    unknown = set(meta.keys()) - ALLOWED_TOP_LEVEL_KEYS
    for k in sorted(unknown):
        errs.append(f"unknown top-level key '{k}' -- not in ALLOWED_TOP_LEVEL_KEYS. "
                    f"If this is a real new field, add it there (and teach "
                    f"generate() to round-trip it) rather than letting it "
                    f"silently pass and then silently vanish on regen.")

    for k in REQUIRED:
        if k not in meta:
            errs.append(f"missing required key: {k}")
    if "unit" in meta and not isinstance(meta["unit"], int):
        errs.append("unit must be an integer")

    for i, r in enumerate(meta.get("roots", []) or []):
        where = f"roots[{i}]"
        for k in ("root", "translit", "gloss"):
            if not r.get(k):
                errs.append(f"{where}: missing {k}")
        if "color" in r or "colour" in r:
            errs.append(f"{where}: carries a colour — the site assigns colours, "
                        "declare translit + gloss only")
        if "kind" in r or "members" in r:
            errs.append(f"{where}: carries 'kind'/'members' — that taxonomy "
                        "was tried and reverted (style reference §1); a root "
                        "is {root, translit, gloss}, nothing more")
        if not re.fullmatch(r"[a-z0-9-]+", r.get("root", "x")):
            errs.append(f"{where}: root '{r.get('root')}' must be [a-z0-9-]")

    th = meta.get("threads", {}) or {}
    for key in THREADS_SUBKEYS:
        if key not in th:
            errs.append(f"threads.{key} is required (all four of "
                        f"{THREADS_SUBKEYS} must be present, empty lists fine)")
        elif not isinstance(th[key], list):
            errs.append(f"threads.{key} must be a list")

    for key in ("opens", "payoffs"):
        for i, e in enumerate(th.get(key, []) or []):
            if not e.get("note"):
                errs.append(f"threads.{key}[{i}]: missing required 'note' "
                            "(the popover line for this beat, checklist 4)")
            elif not isinstance(e["note"], str):
                errs.append(f"threads.{key}[{i}]: 'note' must be a string")

    for i, c in enumerate(th.get("candidates", []) or []):
        where = f"threads.candidates[{i}]"
        if not c.get("root"):
            errs.append(f"{where}: missing 'root'")
        elif not re.fullmatch(r"[a-z0-9-]+", c["root"]):
            errs.append(f"{where}: root '{c['root']}' must be [a-z0-9-]")
        if not c.get("why"):
            errs.append(f"{where}: missing 'why'")
        for k in ("stems", "exclude"):
            if k in c:
                errs.append(f"{where}: '{k}' is not part of the schema — "
                            "candidates are {root, why, ids?, refs?} now "
                            "(id-based, style reference §2/§3), not Hebrew "
                            "consonant-skeleton stems")
        if "ids" in c:
            if not isinstance(c["ids"], list) or not all(
                    isinstance(x, str) and _ID_RE.match(x) for x in c["ids"]):
                errs.append(f"{where}: 'ids' must be a list of strings matching "
                            f"^\\d+[a-z]?$ (e.g. '2763', '2763a')")
        if "refs" in c:
            if not isinstance(c["refs"], list) or not all(
                    isinstance(x, str) and _REF_RE.match(x) for x in c["refs"]):
                errs.append(f"{where}: 'refs' must be a list of 'C:V' strings "
                            f"(e.g. '6:5')")

    if threads_json is not None:
        ids = {t["id"] for t in threads_json["threads"]}
        roots = {t["root"] for t in threads_json["threads"]}
        for key in ("opens", "payoffs"):
            for e in th.get(key, []) or []:
                if e.get("id") not in ids:
                    errs.append(f"threads.{key}: '{e.get('id')}' is not a "
                                "thread id in data/threads.json "
                                "(use threads.candidates to propose a new one)")

        this_slug = meta.get("slug") or f"unit-{meta.get('unit', 0):02d}"
        try:
            units_json = _load("units.json")
        except Exception:
            units_json = {"units": []}
        unit_roots = {u["slug"]: set((u.get("roots") or {}).keys())
                      for u in units_json["units"]}
        VALID_OPS = {"add", "retag", "retag_word", "untag_word", "unwrap",
                     "strip_span", "text"}
        for i, e in enumerate(th.get("retro", []) or []):
            where = f"threads.retro[{i}]"
            slug = e.get("unit", "")
            op = e.get("op", "add")
            if not re.fullmatch(r"unit-\d{2}", slug):
                errs.append(f"{where}: 'unit' must be a slug like 'unit-06'")
            elif slug == this_slug:
                errs.append(f"{where}: retro is for EARLIER units, not this one "
                            f"({slug}) — tag this unit's own occurrences in the "
                            "fragment or in retrofit-tags.json directly")
            if not e.get("why"):
                errs.append(f"{where}: missing 'why'")
            if op not in VALID_OPS:
                errs.append(f"{where}: op '{op}' not one of {sorted(VALID_OPS)}")
            targets = ([e.get("to")] if op in ("retag", "retag_word", "text")
                       else [e.get("root")] if op in ("add", "unwrap", "untag_word")
                       else [])
            for r in filter(None, targets):
                known = slug in unit_roots and r in unit_roots[slug]
                if r not in roots and not known:
                    errs.append(f"{where}: '{r}' is neither a tracked thread nor "
                                f"a declared root of {slug} — a tag that resolves "
                                "to no colour is a hard verify failure")
                # A retro fix that creates or repoints a span onto a TRACKED
                # thread produces a span that must carry data-w (checklist 7),
                # same as any other tracked-thread span. Local roots don't
                # need one (style reference §2). See _ID_RE for the id format.
                if op in ("add", "retag", "retag_word") and r in roots:
                    wid = e.get("w")
                    if not wid or not _WORD_ID_RE.match(wid):
                        errs.append(f"{where}: op '{op}' targets tracked "
                                    f"thread '{r}' but has no valid 'w' (OSHB "
                                    "word id from Joshua-words.tsv) -- a "
                                    "tracked-thread span must carry data-w "
                                    "(checklist 7)")
    return errs


# ---------------------------------------------------------- validate_fragment

# Component classes every unit fragment must contain. The legend is
# section.block.legend (style reference §4), so both class tokens are
# required, not just "legend" -- a fragment with roots/threads but no
# rendered legend is exactly as broken as one referencing a CSS class that
# doesn't exist, just in the opposite direction.
REQUIRED_COMPONENT_CLASSES = {"block", "legend"}

CLASS_ATTR_RE = re.compile(r'class="([^"]*)"')
# Grep-level CSS class-selector scan, not a real CSS parser: any ".name"
# where name starts with a letter, so "12px"/".5em" don't get pulled in
# as fake classes. Good enough for a whitelist diff; a hand-rolled parser
# would be more precision than a fragment/stylesheet pair this small needs.
CSS_CLASS_RE = re.compile(r'\.([a-zA-Z][a-zA-Z0-9_-]*)')

ID_ATTR_RE = re.compile(r'id="([\w-]*n\d+[a-z]?)"')
HREF_ATTR_RE = re.compile(r'href="#([\w-]*n\d+[a-z]?)"')

# The full Hebrew Unicode block (U+0590-U+05FF): letters, niqqud,
# cantillation, and punctuation (maqqef, sof-pasuq, gershayim, …) all
# live in this one range. Deliberately not narrowed to "letters only" --
# a fragment with stray niqqud/cantillation and no base letters would
# still be a Hebrew-script leak.
HEBREW_SCRIPT_RE = re.compile("[֐-׿]")


def _css_classes(css_path=None):
    css_path = css_path or CSS
    if not os.path.exists(css_path):
        return None  # caller turns this into a hard failure, not a silent pass
    css = open(css_path, encoding="utf-8").read()
    return set(CSS_CLASS_RE.findall(css))


def check_component_whitelist(html, css_path=None):
    """1) every class used in the fragment must be defined in
    css/styles.css (grep-diff, not a CSS parser -- see CSS_CLASS_RE).
    2) every class in REQUIRED_COMPONENT_CLASSES must actually appear."""
    errs = []
    css_classes = _css_classes(css_path)
    if css_classes is None:
        errs.append(f"{css_path or CSS} not found -- can't check the fragment's "
                    "classes against it. Create the stylesheet (or point "
                    "css_path at the right one) before validating fragments.")
        css_classes = set()

    fragment_classes = set()
    for m in CLASS_ATTR_RE.finditer(html):
        fragment_classes.update(m.group(1).split())

    unstyled = sorted(fragment_classes - css_classes)
    for cls in unstyled:
        errs.append(f"fragment uses class '{cls}' which css/styles.css does "
                    f"not define -- typo, or a class that needs adding there")

    missing_required = sorted(REQUIRED_COMPONENT_CLASSES - fragment_classes)
    for cls in missing_required:
        errs.append(f"required component missing: no element with class "
                    f"'{cls}' in this fragment")
    return errs


def check_endnote_integrity(html):
    """Every id="…n<N>" must have a matching href="#…n<N>" and vice versa
    -- an endnote nobody links to, or a link to an endnote that doesn't
    exist, are both silent breakage (a dead citation marker, or a click
    that goes nowhere)."""
    ids = {m.group(1) for m in ID_ATTR_RE.finditer(html)}
    hrefs = {m.group(1) for m in HREF_ATTR_RE.finditer(html)}
    errs = []
    orphan_ids = sorted(ids - hrefs)
    orphan_hrefs = sorted(hrefs - ids)
    for i in orphan_ids:
        errs.append(f"endnote id=\"{i}\" has no href=\"#{i}\" pointing to it "
                    f"-- unreferenced endnote")
    for h in orphan_hrefs:
        errs.append(f"href=\"#{h}\" has no matching id=\"{h}\" -- link to a "
                    f"nonexistent endnote")
    return errs


def check_no_hebrew_script(html):
    """Zero native Hebrew script (letters, niqqud, or cantillation --
    U+0591-U+05F4) anywhere in a fragment, no exceptions, attribute values
    included (checklist 12). Policy: a fragment is English prose plus
    transliteration: the reader of the built site never needs the Hebrew
    script itself, and every Hebrew string in this pipeline is meant to be
    generated from OSHB and verified there (see CLAUDE.md), never
    hand-typed into a fragment.

    This fork previously exempted threads.candidates[].stems (a unit
    author drafting a new thread could write the actual Hebrew for
    legibility) -- that exemption directly contradicted checklist 12's "no
    exceptions, attribute values included" and is removed here. Now that
    candidates carry `ids`/`refs` (style reference §3), not Hebrew
    `stems`/`exclude` strings at all, there's no field left that would
    plausibly need one anyway."""
    hits = HEBREW_SCRIPT_RE.findall(html)
    if not hits:
        return []
    sample = "".join(sorted(set(hits))[:10])
    return [f"{len(hits)} native Hebrew script character(s) found in the "
            f"fragment (policy: fragments carry English + transliteration "
            f"only, no exceptions -- checklist 12). Sample: {sample!r}"]


# ------------------------------------------------------- newer fragment checks
# (checklist items 6, 7, 9, 13; §4's rl-outside-verse-blocks convention)

DATA_ROOT_RE = re.compile(r'data-root="([a-z0-9-]+)"')
SPAN_R_RE = re.compile(r'<span\s+class="r"([^>]*)>')
DATA_W_ATTR_RE = re.compile(r'data-w="')
PERICOPE_RE = re.compile(r'<h3\s+class="pericope">(.*?)</h3>', re.S)
PERICOPE_RANGE_RE = re.compile(r'·\s*\d+:\d+')
STYLE_ATTR_RE = re.compile(r'\bstyle\s*=\s*"')
CSS_VAR_RE = re.compile(r'--c-[a-zA-Z0-9_-]+')
VBLOCK_RE = re.compile(r'<(?:div|p)\s+class="v"[^>]*>(.*?)</(?:div|p)>', re.S)
RL_RE = re.compile(r'class="rl"')
_TAG_RE = re.compile(r"<[^>]+>")
_WS_RE = re.compile(r"\s+")


def _detag(s):
    return _WS_RE.sub(" ", _TAG_RE.sub("", s)).strip()


def check_data_root_resolves(html, meta=None, threads_json=None):
    """Every data-root slug must resolve to a colour: a threads.json
    thread's `root`, or this fragment's own meta.roots[] (checklist 6). A
    data-root that resolves to nothing is a hard build failure (style
    reference §1)."""
    if meta is None:
        meta = parse(html) or {}
    if threads_json is None:
        try:
            threads_json = _load("threads.json")
        except Exception:
            threads_json = {"threads": []}

    known = {t["root"] for t in threads_json.get("threads", [])}
    known |= {r["root"] for r in (meta.get("roots") or []) if r.get("root")}

    errs = []
    for slug in sorted(set(DATA_ROOT_RE.findall(html))):
        if slug not in known:
            errs.append(f"data-root=\"{slug}\" resolves to no colour -- not a "
                        f"thread in data/threads.json and not in this "
                        f"fragment's own roots[] (checklist 6)")
    return errs


def check_tracked_spans_have_data_w(html, threads_json=None):
    """Every span tagging a TRACKED thread (data-root matching a
    threads.json thread's root) must carry data-w (checklist 7, style
    reference §2). Local roots (declared only in this fragment's own
    roots[]) don't need one."""
    if threads_json is None:
        try:
            threads_json = _load("threads.json")
        except Exception:
            threads_json = {"threads": []}
    tracked = {t["root"] for t in threads_json.get("threads", [])}

    errs = []
    for m in SPAN_R_RE.finditer(html):
        attrs = m.group(1)
        rm = DATA_ROOT_RE.search(attrs)
        if not rm or rm.group(1) not in tracked:
            continue
        if not DATA_W_ATTR_RE.search(attrs):
            errs.append(f"span tags tracked thread '{rm.group(1)}' with no "
                        f"data-w attribute (checklist 7)")
    return errs


def check_pericope_headings(html):
    """Every h3.pericope must carry its '· C:V' (or C:V-C:V) range
    (checklist 9)."""
    errs = []
    for m in PERICOPE_RE.finditer(html):
        if not PERICOPE_RANGE_RE.search(m.group(1)):
            errs.append(f"pericope heading missing its '· C:V' range: "
                        f"{_detag(m.group(1))!r}")
    return errs


def check_no_inline_style(html):
    """No inline style=, no --c-* colour vars (checklist 13)."""
    errs = []
    if STYLE_ATTR_RE.search(html):
        errs.append("fragment has an inline style=\"...\" attribute -- not allowed")
    css_vars = sorted(set(CSS_VAR_RE.findall(html)))
    for v in css_vars:
        errs.append(f"fragment uses colour variable '{v}' -- the site assigns "
                    f"colours, no --c-* vars in a fragment")
    return errs


def warnings_for_fragment(html):
    """Non-fatal warnings -- distinct from validate_fragment()'s hard
    failures. Currently just class=\"rl\" inside a .v block (style
    reference §4: valid outside verse blocks, but inside one it's counted
    anyway, so rl there only mislabels intent, doesn't break anything)."""
    warnings = []
    for m in VBLOCK_RE.finditer(html):
        if RL_RE.search(m.group(1)):
            warnings.append("class=\"rl\" found inside a .v verse block -- "
                            "valid only outside verse blocks; inside one it's "
                            "counted anyway, so this only mislabels intent")
    return warnings


def validate_fragment(html, css_path=None, meta=None, threads_json=None):
    """All fragment-level HARD checks in one call: component whitelist,
    endnote integrity, zero Hebrew script, data-root resolution, tracked-
    span data-w, pericope headings, no inline style/--c-* vars. Does not
    include validate()'s meta-dict checks, and does not include
    warnings_for_fragment()'s non-fatal warnings -- run all three when
    checking a real fragment."""
    errs = []
    errs += check_component_whitelist(html, css_path)
    errs += check_endnote_integrity(html)
    errs += check_no_hebrew_script(html)
    errs += check_data_root_resolves(html, meta, threads_json)
    errs += check_tracked_spans_have_data_w(html, threads_json)
    errs += check_pericope_headings(html)
    errs += check_no_inline_style(html)
    return errs


# ---------------------------------------------------------------- generate
# (derive a metadata block for an already-built unit from the data files —
#  used to keep blocks fresh once a build step exists)

def _threads_touching(threads_json, n):
    opens, payoffs = [], []
    for t in threads_json["threads"]:
        if t.get("opens", {}).get("unit") == n:
            opens.append({"id": t["id"], "ref": t["opens"].get("ref", "")})
        for p in t.get("payoffs", []):
            if p.get("unit") == n:
                payoffs.append({"id": t["id"], "ref": p.get("ref", "")})
    return opens, payoffs


def generate(n, units_json=None, threads_json=None):
    """Build the metadata dict for unit n from the committed data files."""
    units_json = units_json or _load("units.json")
    threads_json = threads_json or _load("threads.json")
    row = _unit_row(units_json, n)
    if row is None:
        raise KeyError(f"unit {n} not in units.json")

    thread_roots = {t["root"] for t in threads_json["threads"]}
    roots = []
    for name, e in (row.get("roots") or {}).items():
        if isinstance(e, str):
            e = {"translit": "", "gloss": ""}
        if name not in thread_roots and not (e.get("translit") or e.get("gloss")):
            continue
        roots.append({"root": name,
                      "translit": e.get("translit", ""),
                      "gloss": e.get("gloss", "")})
    roots.sort(key=lambda r: r["root"])

    opens, payoffs = _threads_touching(threads_json, n)
    meta = {
        "unit": n,
        "slug": row["slug"],
        "passage": row["passage"],
        "title": row["title"],
        "movement": row.get("movement"),
        "roots": roots,
        "threads": {"opens": opens, "payoffs": payoffs, "candidates": [], "retro": []},
    }
    if meta["movement"] is None:
        del meta["movement"]
    return meta
