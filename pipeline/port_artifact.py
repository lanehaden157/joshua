"""Drop one research artifact into the site.

    python pipeline/port_artifact.py 5              # port source-artifacts/joshua_05_translation.html
    python pipeline/port_artifact.py 5 --dry         # show what would change, write nothing
    python pipeline/port_artifact.py 6 --src X.html  # build the thread-delta report from X, write nothing

Pipeline for a new unit N:
  1. read source-artifacts/joshua_0N_translation.html
  2. prefix its endnote ids (u0N-n1, ...) so ids stay unique once every
     unit's fragment lives on one page
  3. read the unit-meta block, validate it (unit_meta.validate, a hard gate)
  4. merge the unit into data/units.json (built:true; local (non-tracked)
     roots get {translit, gloss} -- no colour yet, Phase 4 assigns those)
  5. merge threads.retro (fixes for EARLIER units) into pipeline/retro-tags.json,
     dry-checking each against its target fragment first
  6. write the thread-delta report to pipeline/out/thread-delta-0N.md for Lane:
     - opens/payoffs that need a tagged/status flip
     - new-thread candidates, each with an id-set preview (data/roots.json
       shape) so Lane can review coverage before committing an id set
     - open questions (meta.questions[]) -- wording/data calls only Lane can
       make, also printed straight to stdout so whoever's running the port
       sees them immediately and can ask Lane right here instead of the
       chat side asking on the project side (2026-09-21)
     - fragment-structure findings, from unit_meta.validate_fragment() --
       reported, not a hard gate (the port still writes the fragment for
       review; only the meta-dict validation blocks the write)
     - the retro fixes that were merged
     - tracked-thread COVERAGE: audit_thread_coverage.coverage_for_fragment()
       -- every gap/wrong-id/stray/missing-data-w in this passage
  7. re-inject a normalised meta block, write units/unit-0N.html
  8. apply_retrofit (retrofit-tags.json + retro-tags.json), then
     scan_occurrences + verify_occurrences

Nothing is committed. Review the fragment in the browser, apply the thread
delta by hand if accepted, then commit.

Ported from Projects/Matthew/pipeline/port_artifact.py, deliberately slimmer
-- extract_units.py's cleanup pipeline (Greek-title parsing, script
stripping, local-palette extraction, verse/block normalization) does NOT
port: Joshua's source-artifacts/ already arrive in the style-reference
fragment shape from unit 1 (checklist 1: one <article>, nothing above or
below it), so there's nothing there to clean up. There is no --backfill:
no legacy units exist to backfill.

The colour/hue-assignment system (WELL palette, assign_hues, perceptual-
distance collision avoidance) DOES port, as of Phase 4 (Lane's call:
assign colours now, not at Phase 5) -- ported near-verbatim from Matthew's
version, with Joshua's own WELL (a distinct desert/Jordan-valley palette,
not Matthew's parchment/crimson-gold one -- see css/styles.css's header
comment for the full theme). Local (non-tracked) roots merged into
units.json now get a real {color, translit, gloss}; tracked-thread colours
still live in data/threads.json, which stays Lane's hand-authored policy
file -- nothing here writes it.
"""

import argparse
import glob
import json
import math
import os
import re
import sys

sys.path.insert(0, os.path.dirname(__file__))
import unit_meta as um              # noqa: E402
import audit_thread_coverage as atc  # noqa: E402
import assign_data_w as adw          # noqa: E402
import roots as root_lib             # noqa: E402
# transliteration in reports goes through atc._translit_row, which applies
# the lemma-keyed OVERRIDES (review A17); bare transliterate() would render
# kol as "kal".

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "source-artifacts")
UNITS = os.path.join(ROOT, "units")
DATA = os.path.join(ROOT, "data")
OUT = os.path.join(ROOT, "pipeline", "out")

# non-binding well of legible, parchment-friendly hues -- Joshua's own
# desert/Jordan-valley palette (terracotta, bronze, olive, jordan-teal,
# wine, umber), deliberately distinct from Matthew's crimson/gold well.
# See css/styles.css's header comment for the shared theme this draws from.
WELL = [
    "#b1481f", "#2f5f6b", "#8c6d1f", "#55642f", "#6b3620", "#3d6b4a",
    "#7a3f5c", "#1f6e7a", "#9c5a1e", "#4a4f6b", "#8a2f3a", "#5c6b1f",
    "#2f4f7a", "#a67c1e", "#6b1e46", "#1e7a5c", "#8f4a1e", "#3f5c6b",
    "#7a5c1e", "#5c3f7a",
]


# --------------------------------------------------------------- colour distance

def _lab(h):
    h = h.lstrip("#")
    r, g, b = (int(h[i:i + 2], 16) / 255 for i in (0, 2, 4))
    def lin(c): return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4
    r, g, b = lin(r), lin(g), lin(b)
    x = (r * 0.4124 + g * 0.3576 + b * 0.1805) / 0.95047
    y = r * 0.2126 + g * 0.7152 + b * 0.0722
    z = (r * 0.0193 + g * 0.1192 + b * 0.9505) / 1.08883
    def f(t): return t ** (1 / 3) if t > 0.008856 else 7.787 * t + 16 / 116
    fx, fy, fz = f(x), f(y), f(z)
    return (116 * fy - 16, 500 * (fx - fy), 200 * (fy - fz))


def _de(a, b):
    """CIE76 -- plain Euclidean distance in Lab. Kept for callers that want
    the cheap metric; prefer ciede2000() for anything a reader looks at."""
    return sum((x - y) ** 2 for x, y in zip(_lab(a), _lab(b))) ** 0.5


def ciede2000(a, b):
    """Perceptual distance between two hex colours (CIEDE2000, kL=kC=kH=1).

    Raw hue distance lies about how different two colours look -- two
    golds 20 degrees apart read as one colour, while two blues the same
    distance apart read as two. CIE76 (_de) is better but still uneven
    across the space. CIEDE2000 adds the lightness/chroma/hue weighting
    and the blue-region rotation term, so one threshold means roughly the
    same thing everywhere in the palette.
    """
    L1, a1, b1 = _lab(a)
    L2, a2, b2 = _lab(b)
    C1, C2 = math.hypot(a1, b1), math.hypot(a2, b2)
    Cb = (C1 + C2) / 2
    G = 0.5 * (1 - math.sqrt(Cb ** 7 / (Cb ** 7 + 25.0 ** 7))) if Cb else 0.5
    a1p, a2p = (1 + G) * a1, (1 + G) * a2
    C1p, C2p = math.hypot(a1p, b1), math.hypot(a2p, b2)

    def _h(ap, bp):
        if ap == 0 and bp == 0:
            return 0.0
        return math.degrees(math.atan2(bp, ap)) % 360

    h1p, h2p = _h(a1p, b1), _h(a2p, b2)
    dLp = L2 - L1
    dCp = C2p - C1p
    if C1p * C2p == 0:
        dhp = 0.0
    elif abs(h2p - h1p) <= 180:
        dhp = h2p - h1p
    elif h2p - h1p > 180:
        dhp = h2p - h1p - 360
    else:
        dhp = h2p - h1p + 360
    dHp = 2 * math.sqrt(C1p * C2p) * math.sin(math.radians(dhp) / 2)

    Lbp = (L1 + L2) / 2
    Cbp = (C1p + C2p) / 2
    if C1p * C2p == 0:
        hbp = h1p + h2p
    elif abs(h1p - h2p) <= 180:
        hbp = (h1p + h2p) / 2
    elif h1p + h2p < 360:
        hbp = (h1p + h2p + 360) / 2
    else:
        hbp = (h1p + h2p - 360) / 2

    T = (1 - 0.17 * math.cos(math.radians(hbp - 30))
         + 0.24 * math.cos(math.radians(2 * hbp))
         + 0.32 * math.cos(math.radians(3 * hbp + 6))
         - 0.20 * math.cos(math.radians(4 * hbp - 63)))
    dTheta = 30 * math.exp(-(((hbp - 275) / 25) ** 2))
    RC = 2 * math.sqrt(Cbp ** 7 / (Cbp ** 7 + 25.0 ** 7)) if Cbp else 0.0
    SL = 1 + (0.015 * (Lbp - 50) ** 2) / math.sqrt(20 + (Lbp - 50) ** 2)
    SC = 1 + 0.045 * Cbp
    SH = 1 + 0.015 * Cbp * T
    RT = -math.sin(math.radians(2 * dTheta)) * RC

    return math.sqrt((dLp / SL) ** 2 + (dCp / SC) ** 2 + (dHp / SH) ** 2
                     + RT * (dCp / SC) * (dHp / SH))


DE_MIN = 10          # CIEDE2000 distance below which two roots read as one


def assign_hues(local_roots, taken):
    """local_roots: [names]; taken: [hex already used in this unit]. Return {name:hex}.

    Picks the first WELL colour at least DE_MIN from everything already in
    play. When the well is exhausted against this unit -- unit 1 tags 16
    distinct roots and the well only yields 13 mutually distinct at
    DE_MIN -- fall back to the colour that is *furthest* from what is
    taken, rather than WELL[len(used) % len(WELL)], which ignored
    collisions outright and handed out exact duplicates of tracked-thread
    colours. The fallback is still a compromise and validate_units.py will
    report it; it just degrades gracefully instead of silently.
    """
    out, used = {}, list(taken)
    for name in local_roots:
        pick = next((c for c in WELL
                     if all(ciede2000(c, u) >= DE_MIN for u in used)), None)
        if pick is None:                       # well exhausted vs. this unit
            pick = max(WELL, key=lambda c: min((ciede2000(c, u) for u in used),
                                               default=float("inf")))
        out[name] = pick
        used.append(pick)
    return out


# --------------------------------------------------------------- fragment build

def prefix_endnotes(body, n):
    """id="n1" -> id="u06-n1", href="#n1" -> href="#u06-n1" -- keeps
    endnote ids unique once every unit's fragment lives on one page."""
    p = f"u{n:02d}-"
    body = re.sub(r'id="(n\d+)"', lambda m: f'id="{p}{m.group(1)}"', body)
    body = re.sub(r'href="#(n\d+)"', lambda m: f'href="#{p}{m.group(1)}"', body)
    return body


def to_fragment(raw, n):
    """Normalize an incoming artifact into the bare <article> fragment.
    Idempotent: re-running on an already-ported fragment changes only the
    endnote-id prefix (already prefixed -> no-op) and the re-injected meta
    block (regenerated fresh either way)."""
    html = raw.strip()
    if not re.search(r'<article class="unit"[^>]*>', html):
        sys.exit('artifact has no <article class="unit"> -- see '
                  "joshua_study_style_reference.md §3 (the hard contract)")
    body = um.strip(html)  # remove any existing meta block
    m = re.search(r'<article class="unit"[^>]*>\n?', body)
    inner = body[m.end():]
    inner = re.sub(r'\s*</article>\s*$', "", inner)
    inner = prefix_endnotes(inner, n)
    return f'<article class="unit" data-unit="{n}">\n{inner.strip()}\n</article>\n'


# --------------------------------------------------------------- units.json merge

def roots_in_fragment(html):
    """Every distinct data-root slug actually tagged in the fragment.

    The authority on which roots a unit uses is the markup, not meta.roots
    -- since roots[] is local-only (style reference §1), a tracked thread
    never appears there, so seeding collision-avoidance from meta.roots
    alone is blind to every tracked colour in the unit."""
    return set(re.findall(r'data-root="([a-z0-9-]+)"', html or ""))


def merge_units_json(meta, dry, fragment_html=None):
    """Merge the unit's row into data/units.json. Local (non-tracked) roots
    get {color, translit, gloss} -- a local hue is assigned here (Phase 4),
    avoiding collisions with this unit's own existing local hues AND the
    global colour of every tracked thread the unit actually tags (read from
    the fragment's data-root spans, not from meta.roots)."""
    uj = um._load("units.json")
    n = meta["unit"]
    row = um._unit_row(uj, n)
    if row is None:
        row = {"n": n, "slug": meta.get("slug", f"unit-{n:02d}"),
               "passage": meta["passage"], "title": meta["title"],
               "movement": meta.get("movement"), "built": False}
        uj["units"].append(row)
        uj["units"].sort(key=lambda u: u["n"])

    threads = {t["root"]: t for t in um._load("threads.json")["threads"]}
    existing = row.get("roots") or {}
    local = [r["root"] for r in meta["roots"] if r["root"] not in threads]
    taken = [e["color"] for e in existing.values()
             if isinstance(e, dict) and e.get("color")]
    tagged = roots_in_fragment(fragment_html) | {r["root"] for r in meta["roots"]}
    taken += [threads[r]["color"] for r in sorted(tagged)
              if r in threads and threads[r].get("color")]
    hues = assign_hues([r for r in local if r not in existing], taken)

    local_roots = {}
    for r in meta["roots"]:
        name = r["root"]
        if name in threads:
            continue  # this root's registry entry is threads.json's job
        prev = existing.get(name) if isinstance(existing.get(name), dict) else {}
        local_roots[name] = {
            "color": prev.get("color") or hues.get(name) or WELL[0],
            "translit": r["translit"],
            "gloss": r["gloss"],
        }

    row.update({"slug": meta.get("slug", row["slug"]), "passage": meta["passage"],
                "title": meta["title"], "built": True, "roots": local_roots})
    if meta.get("movement"):
        row["movement"] = meta["movement"]

    if not dry:
        path = os.path.join(DATA, "units.json")
        json.dump(uj, open(path, "w", encoding="utf-8"), indent=2, ensure_ascii=False)
        open(path, "a", encoding="utf-8").write("\n")
    return local_roots


# --------------------------------------------------------------- thread delta

def thread_delta(meta, fragment_html=None, retrofit_applied=True):
    threads = {t["id"]: t for t in um._load("threads.json")["threads"]}
    n = meta["unit"]
    slug = meta.get("slug", f"unit-{n:02d}")
    lines = [f"# Thread delta — Unit {n}", "",
             "Apply by hand to `data/threads.json` if accepted. "
             "The porter does not touch threads.json.", ""]

    th = meta.get("threads", {})
    touched = []
    for kind in ("opens", "payoffs"):
        for e in th.get(kind, []) or []:
            t = threads.get(e["id"])
            if not t:
                continue
            touched.append(e["id"])
            flags = []
            if not t.get("tagged"):
                flags.append("set `tagged: true`")
            if kind == "payoffs" and t.get("status") == "open":
                flags.append("consider `status: \"closed\"` if this is the final payoff")
            note = f" — {'; '.join(flags)}" if flags else " — already consistent"
            lines.append(f"- **{kind[:-1]}** `{e['id']}` at {e.get('ref', '?')}{note}")
            if kind == "payoffs" and not any(
                    p.get("unit") == n for p in t.get("payoffs", [])):
                entry = {"unit": n, "ref": e.get("ref", "")}
                if e.get("note"):
                    entry["note"] = e["note"]
                lines.append(f"    - add to `{e['id']}`.payoffs: "
                             f"`{json.dumps(entry, ensure_ascii=False)}`")
            elif kind == "opens" and not (t.get("opens") or {}).get("note"):
                entry = {"unit": n, "ref": e.get("ref", "")}
                if e.get("note"):
                    entry["note"] = e["note"]
                lines.append(f"    - set `{e['id']}`.opens: "
                             f"`{json.dumps(entry, ensure_ascii=False)}`")

    cands = th.get("candidates", []) or []
    if cands:
        lines += ["", "## New-thread candidates "
                  "(Claude decides, biased book-wide)", ""]
        declined = (um._load("roots.json").get("declined") or {})
        for c in cands:
            root = c.get("root", "?")
            lines.append(f"- `{root}` — {c.get('why', '').strip()}")
            if root in declined:
                d = declined[root]
                lines.append(f"    - **previously declined** "
                             f"{d.get('date', '?')}: {d.get('why', '').strip()}")
                lines.append("    - re-proposing is fine, but say what "
                             "changed -- a new payoff, not the same argument "
                             "(review A13).")
            _append_candidate_preview(lines, root, c)

    questions = meta.get("questions", []) or []
    if questions:
        lines += ["", "## Open questions for Lane", ""]
        for q in questions:
            lines.append(f"- **{q.get('topic', '?')}** — {q.get('note', '').strip()}")
            for opt in q.get("options", []) or []:
                lines.append(f"    - {opt}")

    retro = th.get("retro", []) or []
    if retro:
        lines += ["", "## Retro fixes for earlier units", "",
                  "Dry-checked against its target fragment, then merged into "
                  "`pipeline/retro-tags.json` (a real port only — not "
                  "`--dry`/`--src`):", ""]
        for e in retro:
            op = e.get("op", "add")
            lines.append(f"- `{e.get('unit','?')}` {op} `{e.get('root', e.get('to','?'))}` "
                         f"— {e.get('why','').strip()}")
            body = {k: v for k, v in e.items() if k not in ("op", "why")}
            lines.append(f"    `{json.dumps(body, ensure_ascii=False)}`")

    if fragment_html is not None:
        _append_fragment_findings(lines, fragment_html, meta)
        _append_coverage(lines, slug, fragment_html, meta.get("passage", ""),
                         retrofit_applied)

    if not touched and not cands and not retro and not questions:
        lines.append("_no tracked threads opened or paid off in this unit, "
                     "no candidates, no retro fixes, no open questions._")

    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, f"thread-delta-{n:02d}.md")
    open(path, "w", encoding="utf-8").write("\n".join(lines) + "\n")
    return path


def _append_candidate_preview(lines, root, cand):
    """Preview what a candidate's proposed `ids` would pull in book-wide --
    the review step before Lane commits an id set to data/roots.json (the
    id-based analogue of Matthew's stem preview, phase-0.6-plan.md §1)."""
    ids = cand.get("ids")
    if not ids:
        lines.append(f"    - no ids proposed yet; once some are, run "
                     f"`pipeline/audit_thread_coverage.py --ids {root}` "
                     f"against a draft data/roots.json entry to preview coverage")
        return
    try:

        words = atc.load_words()
        hits = atc.source_hits_for_root(words, ids)
        wbi = atc.words_by_id(words)
    except Exception as exc:  # pragma: no cover
        lines.append(f"    - (id preview unavailable: {exc})")
        return

    by_form = {}
    for wid, cv in hits.items():
        surface = wbi[wid]["surface"]
        e = by_form.setdefault(surface, {"n": 0, "wid": wid})
        e["n"] += 1
    lines.append(f"    - if promoted, data/roots.json entry: "
                 f"`\"{root}\": {{\"ids\": {json.dumps(ids)}, \"note\": \"...\"}}`")
    total = sum(e["n"] for e in by_form.values())
    lines.append(f"    - those ids match **{total}** word(s) book-wide "
                 f"({len(by_form)} distinct surface form(s)):")
    for surface, e in sorted(by_form.items(), key=lambda kv: -kv[1]["n"])[:12]:
        lines.append(f"        {surface} ({atc._translit_row(wbi[e['wid']])}) "
                     f"×{e['n']}")
    extra = len(by_form) - 12
    if extra > 0:
        lines.append(f"        …and {extra} more form" + ("s" if extra != 1 else ""))


def _append_fragment_findings(lines, html, meta):
    """unit_meta.validate_fragment()'s findings, reported -- NOT a hard gate
    (the port still writes the fragment for review; only validate() on the
    meta dict blocks the write, see port_one)."""
    try:
        threads_json = um._load("threads.json")
    except Exception:
        threads_json = {"threads": []}
    errs = um.validate_fragment(html, meta=meta, threads_json=threads_json)
    warnings = um.warnings_for_fragment(html)
    if errs or warnings:
        lines += ["", "## Fragment findings — fix before committing", ""]
        lines += [f"- **FAIL** {e}" for e in errs]
        lines += [f"- warning: {w}" for w in warnings]


def _append_coverage(lines, slug, html, passage, retrofit_applied=True):
    try:
        cov = atc.coverage_for_fragment(slug, html, passage)
    except Exception as exc:  # pragma: no cover
        lines.append(f"\n## Tracked-thread coverage\n\n(unavailable: {exc})")
        return
    lines += ["", "## Tracked-thread coverage in this unit", ""]
    if not retrofit_applied:
        lines.append("_(checked on the raw fragment — retrofit-tags.json not yet "
                     "applied; entries already there will show as gaps)_")
        lines.append("")
    if cov["warnings"]:
        lines.append("**alignment warnings — check these first:**")
        lines += [f"- {w}" for w in cov["warnings"]] + [""]
    if not cov["gaps"] and not cov["wrong"] and not cov["strays"] and not cov["missing_data_w"]:
        lines.append("Every tracked-thread occurrence in this passage is tagged. ✓")
        return
    if cov["gaps"]:
        lines.append(f"**{len(cov['gaps'])} occurrence(s) the Hebrew has but the "
                     f"fragment leaves untagged** — add to `retrofit-tags.json` "
                     f"`add` (fill in `text`):")
        lines.append("")
        for g in cov["gaps"]:
            txt = (g["text"][:90] + "…") if len(g["text"]) > 90 else g["text"]
            lines.append(f'    {{ "unit": "{slug}", "verse": {g["v"]}, '
                         f'"text": "???", "root": "{g["root"]}", "w": "{g["word_id"]}", '
                         f'"why": "{g["translit"]} {g["ch"]}:{g["v"]}" }},')
            if txt:
                lines.append(f"        # “{txt}”")
    if cov["wrong"]:
        lines += ["", f"**{len(cov['wrong'])} tagged id whose lemma isn't in the "
                      f"root's set — mistyped id?**"]
        for w in cov["wrong"]:
            lines.append(f"- `{w['word_id']}` (‹{w['surface']}›) tagged "
                         f"{w['root']} at {w['ch']}:{w['v']}")
    if cov["strays"]:
        lines += ["", f"**{len(cov['strays'])} tagged id that's out of range or "
                      f"doesn't exist — wrong verse or typo?**"]
        for s in cov["strays"]:
            lines.append(f"- `{s['word_id']}` tagged {s['root']}: {s['reason']}")
    if cov["missing_data_w"]:
        lines += ["", f"**{cov['missing_data_w']} tracked-thread span(s) with no "
                      f"data-w attribute — hard error, must fix before committing**"]


# --------------------------------------------------------------- retro + retrofit

RETRO_FIELDS = {
    "add": ("unit", "verse", "text", "root", "why", "nth", "cls", "w"),
    "retag": ("unit", "verse", "from", "to", "text", "why", "nth", "w"),
    "retag_word": ("unit", "from", "to", "match", "why"),
    "untag_word": ("unit", "root", "match", "why"),
    "unwrap": ("unit", "text", "root", "why"),
    "strip_span": ("unit", "class", "why"),
    "text": ("unit", "from", "to", "why"),
}
RETRO_SPEC = os.path.join(ROOT, "pipeline", "retro-tags.json")


def merge_retro(meta, dry):
    """Merge meta.threads.retro (fixes for earlier units) into the generated
    pipeline/retro-tags.json, which apply_retrofit.py loads alongside the
    hand-authored retrofit-tags.json. Each entry is dry-checked against its
    target fragment first; ones that wouldn't apply cleanly are reported,
    not written."""
    import apply_retrofit as ar
    retro = (meta.get("threads", {}) or {}).get("retro", []) or []
    if not retro:
        return 0, []
    rt = json.load(open(RETRO_SPEC, encoding="utf-8")) \
        if os.path.exists(RETRO_SPEC) else {}
    n = meta["unit"]
    stamp = f"from Unit {n} port ({_today()})"
    written, skips = 0, []
    for e in retro:
        op = e.get("op", "add")
        entry = {k: e[k] for k in RETRO_FIELDS.get(op, ()) if k in e}
        target_path = os.path.join(UNITS, e["unit"] + ".html")
        if not os.path.exists(target_path):
            skips.append(f"MISS {e['unit']}: fragment doesn't exist yet "
                         f"({e.get('why','').strip()})")
            continue
        html = open(target_path, encoding="utf-8").read()
        _, msg = ar.FNS[op](html, entry)
        if msg.startswith(("MISS", "SKIP")):
            skips.append(f"{msg}  ({e.get('why','').strip()})")
            continue
        if msg.startswith("ok"):
            continue  # already applied — nothing to record
        arr = rt.setdefault(op, [])
        if any(x == entry for x in arr):
            continue
        entry["_from"] = stamp
        arr.append(entry)
        written += 1
    if (written or skips) and not dry:
        json.dump(rt, open(RETRO_SPEC, "w", encoding="utf-8"), indent=2,
                  ensure_ascii=False)
        open(RETRO_SPEC, "a", encoding="utf-8").write("\n")
    return written, skips


def _today():
    import datetime
    return datetime.date.today().isoformat()


def run_retrofit_and_scan():
    import subprocess
    env = dict(os.environ, PYTHONIOENCODING="utf-8")
    for step in ("apply_retrofit.py", "scan_occurrences.py", "verify_occurrences.py"):
        print(f"\n=== {step} ===")
        r = subprocess.run([sys.executable, os.path.join(os.path.dirname(__file__), step)],
                           env=env)
        if r.returncode != 0 and step != "apply_retrofit.py":
            print(f"FAILED at {step}")
            return False
    return True


# --------------------------------------------------------------- commands

def print_questions(meta):
    """Wording/data calls the chat side flagged for Lane (meta.questions[]) --
    printed straight to stdout, at the top of the port, so whoever is
    running port_artifact.py sees them immediately and can ask Lane right
    here instead of the chat side asking on the project side (2026-09-21,
    Lane: 'i dont wanna be answering those on project side'). Also folded
    into the thread-delta report by thread_delta() for the written record,
    but this is the copy meant to actually get read."""
    questions = meta.get("questions", []) or []
    if not questions:
        return
    print("")
    print(f"=== {len(questions)} open question(s) for Lane ===")
    for q in questions:
        print(f"  [{q.get('topic', '?')}] {q.get('note', '').strip()}")
        for opt in q.get("options", []) or []:
            print(f"      - {opt}")


def port_one(n, dry, src=None):
    os.makedirs(OUT, exist_ok=True)
    if src:
        if not os.path.exists(src):
            sys.exit(f"--src not found: {src}")
        raw = open(src, encoding="utf-8").read()
    else:
        matches = glob.glob(os.path.join(SRC, f"joshua_{n:02d}_*.html"))
        if not matches:
            sys.exit(f"no source artifact: source-artifacts/joshua_{n:02d}_*.html")
        raw = open(matches[0], encoding="utf-8").read()

    meta = um.parse(raw)
    if meta is None:
        sys.exit('artifact has no <script id="unit-meta"> block — see '
                 "joshua_study_style_reference.md §3")
    meta.setdefault("unit", n)
    meta.setdefault("slug", f"unit-{n:02d}")
    errs = um.validate(meta, um._load("threads.json"))
    if errs:
        print("METADATA INVALID:")
        for e in errs:
            print("  -", e)
        sys.exit(1)

    print_questions(meta)

    fragment = to_fragment(raw, n)

    # A6: the chat side is told to mark roots with data-root only and not to
    # hand-chase word ids, so the artifact arrives without data-w. Fill them
    # here by per-verse alignment; anything ambiguous is reported and left
    # for a human rather than guessed at.
    w_edits, w_report = adw.plan(fragment, meta["passage"])
    if w_edits:
        fragment = adw.apply_edits(fragment, w_edits)
    print("")
    print("=== data-w assignment ===")
    print(f"assigned {len(w_edits)} span(s) by per-verse alignment"
          + (f"; {len(w_report)} need(s) a human:" if w_report else ""))
    for line in w_report:
        print("  needs eyes:", line)

    no_write = dry or bool(src)
    local_roots = merge_units_json(meta, no_write, fragment)
    if not meta.get("movement"):
        r = um._unit_row(um._load("units.json"), n)
        if r and r.get("movement"):
            meta["movement"] = r["movement"]
    fragment = um.inject(fragment, um.generate(n) if not no_write else meta)

    dest = os.path.join(UNITS, f"unit-{n:02d}.html")
    if no_write:
        why = "dry run" if dry else "--src: writing nothing"
        delta = thread_delta(meta, fragment, retrofit_applied=False)
        print(f"[{why}] would write {dest}")
        print(f"[{why}] local hues: { {k: v['color'] for k, v in local_roots.items()} }")
        nretro = len((meta.get("threads", {}) or {}).get("retro", []) or [])
        if nretro:
            print(f"[{why}] {nretro} retro fix(es) for earlier units — would be "
                  f"merged into pipeline/retro-tags.json (see the thread delta)")
        print(f"[{why}] thread delta -> {delta}  "
              f"(coverage checked before retrofit-tags.json is applied)")
        return

    open(dest, "w", encoding="utf-8").write(fragment)
    print(f"wrote {dest}")
    print(f"local hues: { {k: v['color'] for k, v in local_roots.items()} }")
    written, skips = merge_retro(meta, dry=False)
    if written:
        print(f"merged {written} retro fix(es) for earlier units -> "
              f"pipeline/retro-tags.json")
    for s in skips:
        print(f"  retro NOT merged — {s}")
    run_retrofit_and_scan()
    # coverage against the fragment as it now stands on disk (retrofit applied)
    final = open(dest, encoding="utf-8").read()
    delta = thread_delta(meta, final, retrofit_applied=True)
    print(f"\n>>> REVIEW THE THREAD DELTA: {delta}")
    print("\nported. view in the browser, apply the thread delta if accepted, then commit.")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("unit", nargs="?", type=int)
    ap.add_argument("--dry", action="store_true")
    ap.add_argument("--src", metavar="PATH",
                    help="port from this file instead of source-artifacts/; "
                         "writes nothing, just builds the thread-delta report "
                         "(for dry-running the porter on a practice fragment)")
    a = ap.parse_args()
    if not a.unit:
        ap.error("give a unit number")
    port_one(a.unit, a.dry, a.src)


if __name__ == "__main__":
    main()
