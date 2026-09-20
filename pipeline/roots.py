"""Loader/validator for data/roots.json -- Lane's hand-curated registry of
tracked-thread root identity: which Strong's/lemma ids belong to one root.
See joshua_study_style_reference.md §2 for why (id-based, not substring-
stem matching) and phase-0.6-plan.md §A5/§A6 for the two decisions this
module enforces: an id claimed by two roots is a hard failure, and this
registry holds tracked threads only -- local (non-thread) roots stay in a
unit's own unit-meta roots[] {root, translit, gloss} (see unit_meta.py),
counted per-verse, no id set needed.

Schema (data/roots.json):
    {"_note": "...", "version": 1,
     "roots": {"<slug>": {"ids": ["2763a", "2764a"], "note": "..."}}}

Nothing in the pipeline writes this file's content -- it's Lane's policy,
same as threads.json (joshua_study_style_reference.md §6). This module
only reads and validates it.
"""
import csv
import json
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
ROOTS_JSON = os.path.join(HERE, "..", "data", "roots.json")
THREADS_JSON = os.path.join(HERE, "..", "data", "threads.json")
WORDS_TSV = os.path.join(HERE, "..", "Joshua-words.tsv")

_SLUG_RE = re.compile(r"^[a-z0-9-]+$")
_ID_RE = re.compile(r"^(\d+)\s?([a-z]|\+)?$")


def bare_id(id_str: str) -> str:
    """'2763a' -> '2763'; '310 a' -> '310'; '2764' -> '2764'; '1007+' ->
    '1007'. The trailing letter is an opaque OSHB disambiguator
    (joshua_study_style_reference.md §2), not part of the id used for
    matching -- accepted both compact (roots.json's own spelling, e.g.
    '2763a') and space-separated (Joshua-words.tsv's spelling, e.g.
    '310 a'). A trailing '+' is OSHB's own marker for a lemma that
    continues into an adjacent word as part of a multi-word proper name
    (e.g. "בֵּית" "1007+" + the next word, together "Bethel") -- also just
    stripped, same as the letter. Raises ValueError if id_str doesn't
    match digits plus one of these optional trailing markers."""
    m = _ID_RE.match(id_str)
    if not m:
        raise ValueError(
            f"malformed id {id_str!r}: expected digits with an optional "
            f"trailing lowercase letter or '+', e.g. '2763', '2763a', '1007+'"
        )
    return m.group(1)


def lemma_key(id_str: str) -> str:
    """Normalize an id while KEEPING its disambiguating letter.

    '310 a' -> '310a'; '2763a' -> '2763a'; '1007+' -> '1007'; '5414' ->
    '5414'. The two markers are not the same thing, which is why they are
    treated differently here (review A7):

    * The trailing **letter** separates genuinely distinct lexemes that
      share a Strong's number. In Joshua: 3885a *lodge* vs 3885b *murmur*;
      2416a *alive* vs 2416e *life*; 6924a *front* vs 6924b *eastward*.
      Stripping it makes those impossible to tell apart, so a root that
      wants one and not the other cannot say so.
    * The trailing **'+'** is OSHB's marker for a lemma continuing into an
      adjacent word as part of a multi-word proper name (Beth-el is '1007+'
      plus the next word). Same lexeme either way, so it is always stripped.

    Some letters really are inflectional rather than lexical -- 834a/b/c/d
    are all *ʾăšer* with different prefixes, 859a-e all *ʾattâ* by person
    and number. Writing the bare id still covers those, because a bare id
    in a root's id set matches every letter variant. Precision is opt-in.
    """
    m = _ID_RE.match(id_str)
    if not m:
        raise ValueError(
            f"malformed id {id_str!r}: expected digits with an optional "
            f"trailing lowercase letter or '+', e.g. '2763', '2763a', '1007+'"
        )
    letter = (m.group(2) or "").strip()
    return m.group(1) + (letter if letter.isalpha() else "")


def split_ids(ids):
    """A root's id list -> (bare_ids, exact_ids).

    A bare id ('2416') matches every letter variant of that number; a
    suffixed id ('2416e') matches only that lexeme. So a root can be as
    coarse or as precise as the word actually needs.
    """
    bare, exact = set(), set()
    for i in ids:
        key = lemma_key(i)
        if key[-1:].isalpha():
            exact.add(key)
        else:
            bare.add(key)
    return bare, exact


def load_roots(path: str = None) -> dict:
    """path defaults to the module-level ROOTS_JSON, resolved at CALL time
    (not bound as a mutable default at import time) so a caller -- a test,
    or another module doing `roots.ROOTS_JSON = ...` -- can monkeypatch it
    and have every no-arg load_roots() call see the new path."""
    if path is None:
        path = ROOTS_JSON
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def known_lemma_ids(words_tsv: str = WORDS_TSV) -> set:
    """Every lemma id that actually occurs in Joshua-words.tsv, in both
    forms -- bare ('2416') and letter-preserving ('2416e') -- so a root
    declaring either spelling can be checked against reality. A lemma
    field may hold several "/"-separated
    segments (one per surface morpheme); bound-prefix segments (c, b, d,
    k, l, m, ...) aren't ids and are skipped."""
    known = set()
    with open(words_tsv, encoding="utf-8") as f:
        reader = csv.DictReader(f, delimiter="\t")
        for row in reader:
            for seg in row["lemma"].split("/"):
                seg = seg.strip()
                if not seg or not seg[0].isdigit():
                    continue
                known.add(bare_id(seg))
                known.add(lemma_key(seg))
    return known


def validate(data: dict, words_tsv: str = WORDS_TSV, threads_data: dict = None) -> list:
    """Validate a parsed roots.json document. Returns a list of error
    strings (empty if clean).

    threads_data, if given, is a parsed threads.json document -- every
    thread's `root` must resolve to a slug declared here (§A6/§D)."""
    errors = []
    roots = data.get("roots")
    if not isinstance(roots, dict):
        return ["roots.json's top-level 'roots' must be an object (slug -> entry)"]

    known_ids = known_lemma_ids(words_tsv)
    bare_owner = {}   # '2416'  -> slug claiming every lexeme under it
    exact_owner = {}  # '2416e' -> slug claiming just that lexeme

    for slug, entry in roots.items():
        if not _SLUG_RE.match(slug):
            errors.append(f"{slug!r}: slug must match [a-z0-9-]+")
        if "kind" in entry or "members" in entry:
            errors.append(f"{slug}: 'kind'/'members' are not allowed (reverted taxonomy, see §1)")
        if "translit" in entry or "gloss" in entry or "color" in entry or "colour" in entry:
            errors.append(f"{slug}: translit/gloss/colour don't belong in roots.json -- this file is id-sets only")

        ids = entry.get("ids")
        if not isinstance(ids, list) or not ids:
            errors.append(f"{slug}: 'ids' must be a non-empty list")
            continue
        if not entry.get("note"):
            errors.append(f"{slug}: missing required 'note'")

        for id_str in ids:
            try:
                bare = bare_id(id_str)
            except ValueError as exc:
                errors.append(f"{slug}: {exc}")
                continue
            if bare not in known_ids:
                errors.append(
                    f"{slug}: id {id_str!r} (bare {bare}) is not a lemma in "
                    f"{os.path.basename(words_tsv)}"
                )
            elif lemma_key(id_str)[-1:].isalpha() and                     lemma_key(id_str) not in known_ids:
                # The number exists but not this lexeme. Under A7 a
                # suffixed id matches only its own lexeme, so this would
                # match nothing at all -- a silent zero, which is worse
                # than a loud error.
                errors.append(
                    f"{slug}: id {id_str!r} -- {bare} occurs in "
                    f"{os.path.basename(words_tsv)} but not with that "
                    f"letter, so this id would match nothing. Use the bare "
                    f"id {bare!r} to match every variant."
                )
            key = lemma_key(id_str)
            precise = key[-1:].isalpha()

            # A bare id claims every lexeme under that number; a suffixed
            # id claims exactly one. So 3885a and 3885b may sit in
            # different roots (lodge vs murmur), but a bare 3885 collides
            # with either (review A7).
            clash = None
            if bare_owner.get(bare) not in (None, slug):
                clash = bare_owner[bare]
            elif precise and exact_owner.get(key) not in (None, slug):
                clash = exact_owner[key]
            elif not precise:
                other = next((o for k, o in exact_owner.items()
                              if bare_id(k) == bare and o != slug), None)
                clash = other

            if clash is not None:
                errors.append(
                    f"id {id_str!r} claimed by both {clash!r} and {slug!r} "
                    f"roots (§A5: an id in two roots is a hard failure)"
                )
            elif precise:
                exact_owner[key] = slug
            else:
                bare_owner[bare] = slug

    # `declined` is the ledger of candidates considered and deliberately
    # kept local (review A13). Without it the decision lives only in a
    # session log, so the same root gets re-proposed every few units and
    # re-argued from scratch.
    declined = data.get("declined")
    if declined is not None:
        if not isinstance(declined, dict):
            errors.append("roots.json's 'declined' must be an object "
                          "(slug -> {why, date, unit?, ids?})")
        else:
            for slug, entry in declined.items():
                if not _SLUG_RE.match(slug):
                    errors.append(f"declined {slug!r}: slug must match [a-z0-9-]+")
                if not isinstance(entry, dict):
                    errors.append(f"declined {slug}: entry must be an object")
                    continue
                if not entry.get("why"):
                    errors.append(f"declined {slug}: missing required 'why' -- "
                                  "a bare 'no' gets re-litigated")
                if not entry.get("date"):
                    errors.append(f"declined {slug}: missing required 'date'")
                if slug in roots:
                    errors.append(f"declined {slug}: also a tracked root -- a "
                                  "slug is one or the other, not both")

    if threads_data is not None:
        thread_roots = {
            t.get("root") for t in threads_data.get("threads", []) if isinstance(t, dict)
        }
        for root_slug in thread_roots:
            if root_slug not in roots:
                errors.append(
                    f"threads.json thread root {root_slug!r} has no matching "
                    f"data/roots.json entry"
                )

    return errors


if __name__ == "__main__":
    data = load_roots()
    threads_data = None
    if os.path.exists(THREADS_JSON):
        with open(THREADS_JSON, encoding="utf-8") as f:
            threads_data = json.load(f)
    errs = validate(data, threads_data=threads_data)
    if errs:
        print(f"FAIL: {len(errs)} error(s)")
        for e in errs:
            print(" -", e)
        raise SystemExit(1)
    print(f"PASS: {len(data.get('roots', {}))} root(s) valid")
