"""Regression test for roots.py, against synthetic roots.json fixtures
built from real lemma ids pulled from Joshua-words.tsv (3068 YHWH, 3389
Jerusalem, 3605 kol -- all confirmed present via hebrew.py's own OVERRIDES
table and its corpus sweep). No real thread/root content exists yet
(data/roots.json is still empty scaffolding), so every fixture here is
synthetic and self-contained.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from roots import bare_id, known_lemma_ids, validate  # noqa: E402

# Ids confirmed to occur in Joshua-words.tsv (see hebrew.py's OVERRIDES /
# test_hebrew.py's corpus sweep).
REAL_ID_YHWH = "3068"
REAL_ID_JERUSALEM = "3389"
REAL_ID_KOL = "3605"


def test_known_lemma_ids_contains_real_ids():
    known = known_lemma_ids()
    failures = []
    for id_ in (REAL_ID_YHWH, REAL_ID_JERUSALEM, REAL_ID_KOL):
        if id_ not in known:
            failures.append(f"{id_}: expected in known_lemma_ids(), not found")
    return failures


def test_valid_document_passes():
    data = {
        "version": 1,
        "roots": {
            "divine-name": {"ids": [REAL_ID_YHWH], "note": "the tetragrammaton"},
            "kol": {"ids": [REAL_ID_KOL], "note": "totality"},
        },
    }
    errors = validate(data)
    if errors:
        return [f"expected a clean document to pass, got: {errors}"]
    return []


def test_unknown_id_fails():
    data = {
        "version": 1,
        "roots": {"bogus": {"ids": ["999999"], "note": "does not exist in the corpus"}},
    }
    errors = validate(data)
    if not any("999999" in e and "not a lemma" in e for e in errors):
        return [f"expected an unknown-id failure, got: {errors}"]
    return []


def test_bad_slug_fails():
    data = {
        "version": 1,
        "roots": {"Bad Slug!": {"ids": [REAL_ID_KOL], "note": "n"}},
    }
    errors = validate(data)
    if not any("slug must match" in e for e in errors):
        return [f"expected a bad-slug failure, got: {errors}"]
    return []


def test_lettered_id_normalizes():
    failures = []
    if bare_id(f"{REAL_ID_KOL}a") != REAL_ID_KOL:
        failures.append(f"bare_id({REAL_ID_KOL}a) did not strip the trailing letter")
    # A lettered id for a real lemma should validate cleanly even though
    # Joshua-words.tsv itself never carries that exact lettered spelling --
    # only the bare numeric id needs to occur.
    data = {
        "version": 1,
        "roots": {"kol": {"ids": [f"{REAL_ID_KOL}a"], "note": "lettered variant"}},
    }
    errors = validate(data)
    if errors:
        failures.append(f"expected a lettered id for a real lemma to validate, got: {errors}")
    return failures


def test_id_in_two_roots_fails():
    data = {
        "version": 1,
        "roots": {
            "root-a": {"ids": [REAL_ID_KOL], "note": "first claim"},
            "root-b": {"ids": [REAL_ID_KOL], "note": "second claim"},
        },
    }
    errors = validate(data)
    if not any("hard failure" in e for e in errors):
        return [f"expected an id-in-two-roots failure, got: {errors}"]
    return []


def test_missing_note_fails():
    data = {"version": 1, "roots": {"kol": {"ids": [REAL_ID_KOL]}}}
    errors = validate(data)
    if not any("missing required 'note'" in e for e in errors):
        return [f"expected a missing-note failure, got: {errors}"]
    return []


def test_kind_members_rejected():
    data = {
        "version": 1,
        "roots": {"kol": {"ids": [REAL_ID_KOL], "note": "n", "kind": "verb"}},
    }
    errors = validate(data)
    if not any("kind" in e and "members" in e for e in errors):
        return [f"expected a kind/members rejection, got: {errors}"]
    return []


def test_translit_gloss_rejected():
    data = {
        "version": 1,
        "roots": {"kol": {"ids": [REAL_ID_KOL], "note": "n", "translit": "kol"}},
    }
    errors = validate(data)
    if not any("id-sets only" in e for e in errors):
        return [f"expected a translit-field rejection, got: {errors}"]
    return []


def test_thread_with_missing_root_fails():
    data = {
        "version": 1,
        "roots": {"kol": {"ids": [REAL_ID_KOL], "note": "n"}},
    }
    threads_data = {
        "version": 1,
        "threads": [{"id": "give", "root": "give", "status": "open"}],
    }
    errors = validate(data, threads_data=threads_data)
    if not any("give" in e and "no matching" in e for e in errors):
        return [f"expected a missing-thread-root failure, got: {errors}"]
    return []


def test_thread_with_present_root_passes():
    data = {
        "version": 1,
        "roots": {"kol": {"ids": [REAL_ID_KOL], "note": "n"}},
    }
    threads_data = {
        "version": 1,
        "threads": [{"id": "kol", "root": "kol", "status": "open"}],
    }
    errors = validate(data, threads_data=threads_data)
    if errors:
        return [f"expected a matching thread root to pass, got: {errors}"]
    return []


_TESTS = [
    test_known_lemma_ids_contains_real_ids,
    test_valid_document_passes,
    test_unknown_id_fails,
    test_bad_slug_fails,
    test_lettered_id_normalizes,
    test_id_in_two_roots_fails,
    test_missing_note_fails,
    test_kind_members_rejected,
    test_translit_gloss_rejected,
    test_thread_with_missing_root_fails,
    test_thread_with_present_root_passes,
]


if __name__ == "__main__":
    all_failures = []
    for t in _TESTS:
        all_failures += [f"{t.__name__}: {f}" for f in t()]

    if all_failures:
        print(f"FAIL: {len(all_failures)} of {len(_TESTS)} checks failed\n")
        for f in all_failures:
            print(f"  - {f}")
        raise SystemExit(1)
    print(f"PASS: {len(_TESTS)} checks")
