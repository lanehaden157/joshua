"""Regenerate the <script id="unit-meta"> block in every built fragment from
data/units.json + data/threads.json.

Ported from Projects/Matthew/pipeline/refresh_meta.py unchanged -- pure
generic-schema logic (Port analysis.md §1.8), no Greek/Hebrew-specific code.
Idempotent. Part of build.py.

New units get their meta block authored in the incoming artifact and merged
by port_artifact.py; this keeps the already-built ones in sync when the
data files change (a thread flips status, a gloss is edited, etc.).
"""

import glob
import os
import re
import sys

sys.path.insert(0, os.path.dirname(__file__))
import unit_meta as um  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
UNITS = os.path.join(ROOT, "units")


def main():
    uj = um._load("units.json")
    tj = um._load("threads.json")
    built = {u["n"] for u in uj["units"] if u.get("built")}
    changed = 0
    for path in sorted(glob.glob(os.path.join(UNITS, "unit-*.html"))):
        n = int(re.search(r"unit-(\d+)", path).group(1))
        if n not in built:
            continue
        html = open(path, encoding="utf-8").read()
        new = um.inject(html, um.generate(n, uj, tj))
        if new != html:
            open(path, "w", encoding="utf-8").write(new)
            changed += 1
            print(f"refreshed unit-{n:02d} meta")
    print(f"refresh_meta: {changed} fragment(s) updated")


if __name__ == "__main__":
    main()
