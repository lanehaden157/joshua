"""Independently re-derive occurrence counts against data/occurrences.json.

Hebrew fork of Projects/Matthew/pipeline/verify_occurrences.py, narrower on
purpose (not a straight port -- Matthew's own colour-resolution and
collision checks are redundant here, not just adaptable):

  - The count-mismatch check is ported as-is: it's genuinely independent
    work (a line-oriented tokeniser, not scan_occurrences' regex, so a bug
    in one approach doesn't hide in both) and nothing else in this pipeline
    does it.
  - Matthew's "every data-root resolves to a colour" check is DROPPED, not
    adapted -- unit_meta.check_data_root_resolves() already does this job,
    more rigorously (it's part of validate_fragment(), run on every build),
    and audit_thread_coverage.py checks tracked-thread ids at the word
    level on top of that. Re-checking mere resolution here would be the
    exact "copying just because" this fork is trying not to do.
  - Matthew's perceptual-colour-distance collision check is DROPPED, not
    stubbed: it needs real hex colour values, which don't exist in this
    project until Phase 4's design pass assigns them. Nothing to check
    against yet; add it back then if it's still wanted.
  - The threads.json tagged-flag sanity check is ported as-is (schema
    consistency, not colour-dependent, and nothing else checks it).

Exit non-zero on any failure.
"""

import glob
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
UNITS = os.path.join(ROOT, "units")
DATA = os.path.join(ROOT, "data")

fail = []


def load(name):
    return json.load(open(os.path.join(DATA, name), encoding="utf-8"))


def recount(html):
    """Token-by-token count, independent of scan_occurrences' regex structure."""
    counts = {}
    for tok in html.replace(">", "> ").split():
        if tok.startswith('data-root="'):
            r = tok.split('"')[1]
            counts[r] = counts.get(r, 0) + 1
    return counts


def main():
    occ = load("occurrences.json")
    threads_json = load("threads.json")

    for path in sorted(glob.glob(os.path.join(UNITS, "unit-*.html"))):
        slug = os.path.splitext(os.path.basename(path))[0]
        html = open(path, encoding="utf-8").read()
        mine = recount(html)
        theirs = {r: v["total"] for r, v in occ.get(slug, {}).items()}
        if mine != theirs:
            fail.append(f"{slug}: count mismatch\n   verify={mine}\n   json  ={theirs}")

    # thread tagged-flag sanity
    all_roots = set()
    for path in glob.glob(os.path.join(UNITS, "unit-*.html")):
        all_roots |= set(recount(open(path, encoding="utf-8").read()))
    for t in threads_json.get("threads", []):
        present = t["root"] in all_roots
        if t.get("tagged") and not present:
            fail.append(f"thread '{t['id']}' tagged:true but root '{t['root']}' "
                       f"not in any fragment")
        if not t.get("tagged") and present:
            fail.append(f"thread '{t['id']}' tagged:false but root '{t['root']}' "
                       f"IS in a fragment -- flip the flag")

    if fail:
        print("FAIL")
        for f in fail:
            print(" -", f)
        sys.exit(1)
    print("occurrences verified -- counts match, tagged flags consistent")


if __name__ == "__main__":
    main()
