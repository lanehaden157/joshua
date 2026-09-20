"""Hard-gate every built fragment in units/ against the contract.

Why this exists (platform review A20, A4):

`validate_fragment()` used to run only on the *incoming* artifact during
port, and only as a report. Everything that touches a fragment afterwards
-- apply_retrofit's edits, refresh_meta's regenerated meta block, a hand
edit -- could push a shipped unit out of contract with nothing to notice.
A1 was exactly that: refresh_meta wrote a meta block the project's own
validator rejected, on every build, silently.

So: re-validate what is actually on disk, as a build step that fails.

The colour check is A4's backstop. port_artifact.assign_hues() avoids
collisions at assignment time, but nothing re-checked after a thread was
recoloured or a local root promoted. Two roots tagged in the same unit
whose colours are closer than DE_MIN in CIE-Lab are indistinguishable to
a reader, which defeats the point of colouring them.
"""
import glob
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import unit_meta as um              # noqa: E402
from port_artifact import DE_MIN, ciede2000, roots_in_fragment  # noqa: E402

ROOT = os.path.dirname(HERE)
UNITS = os.path.join(ROOT, "units")

def unit_colours(slug, roots, threads, units_json):
    """root -> hex for every root tagged in this unit, tracked or local.

    Mirrors app/threads.js resolveUnit(): a tracked thread's colour comes
    from threads.json and wins; a local root's from units.json.
    """
    row = next((u for u in units_json["units"] if u.get("slug") == slug), None)
    local = (row or {}).get("roots") or {}
    out = {}
    for r in sorted(roots):
        if r in threads:
            c = threads[r].get("color")
        else:
            e = local.get(r)
            c = e.get("color") if isinstance(e, dict) else e
        if c:
            out[r] = c
    return out


def closest_pairs(colours, limit=3):
    """[(dE, root_a, hex_a, root_b, hex_b)] for the closest pairs, ranked.

    Always returns the tightest few whether or not they cross DE_MIN, so
    the ceiling is visible before it is hit rather than after.
    """
    items = sorted(colours.items())
    pairs = [(ciede2000(ca, cb), ra, ca, rb, cb)
             for i, (ra, ca) in enumerate(items)
             for rb, cb in items[i + 1:]]
    pairs.sort(key=lambda p: p[0])
    return pairs[:limit]


def check_colours(slug, colours):
    """Warn on same-unit pairs under DE_MIN, and show the ranked ceiling."""
    out = []
    pairs = closest_pairs(colours, limit=3)
    for d, ra, ca, rb, cb in pairs:
        if d < DE_MIN:
            out.append(f"colours close: '{ra}' ({ca}) / '{rb}' ({cb}) "
                       f"dE2000={d:.1f}, under {DE_MIN}")
    if pairs:
        ranked = ", ".join(f"{ra}/{rb} {d:.1f}" for d, ra, _, rb, _ in pairs)
        out.append(f"closest pairs in this unit (dE2000): {ranked}")
    return out


def check_thread_hexes_unique(threads):
    """No two tracked threads may share a hex, book-wide.

    Matthew has three sets of threads sharing a colour (review B2); a
    shared hex means two different threads look like one wherever they
    meet, in any unit. Cheap to assert, so assert it.
    """
    out, by_hex = [], {}
    for root, t in sorted(threads.items()):
        c = (t.get("color") or "").lower()
        if c:
            by_hex.setdefault(c, []).append(t.get("id", root))
    for c, ids in sorted(by_hex.items()):
        if len(ids) > 1:
            out.append(f"threads {', '.join(repr(i) for i in ids)} all use "
                       f"{c} -- two threads that look like one")
    return out


def main():
    threads_json = um._load("threads.json")
    units_json = um._load("units.json")
    threads = {t["root"]: t for t in threads_json["threads"]}

    book_warns = check_thread_hexes_unique(threads)
    for w in book_warns:
        print("  warn  (book-wide)", w)

    paths = sorted(glob.glob(os.path.join(UNITS, "unit-*.html")))
    if not paths:
        print("no built units to validate")
        return 0

    total_err, total_warn = 0, len(book_warns)
    for path in paths:
        name = os.path.basename(path)
        html = open(path, encoding="utf-8").read()
        meta = um.parse(html)

        errs = []
        if meta is None:
            errs.append("no meta block (unit_meta.parse returned None)")
        else:
            errs += [f"meta: {e}" for e in um.validate(meta, threads_json)]
            errs += um.validate_fragment(html, meta=meta,
                                         threads_json=threads_json)
        warns = um.warnings_for_fragment(html)
        if meta is not None:
            # Colour distance is a tunable aesthetic judgement, not a
            # contract breach, so it warns rather than failing the build.
            # It still gets said out loud on every build, which is the
            # backstop that was missing (review A4).
            slug = meta.get("slug") or name[:-5]
            warns += check_colours(
                slug, unit_colours(slug, roots_in_fragment(html),
                                   threads, units_json))
        total_err += len(errs)
        total_warn += len(warns)

        status = "FAIL" if errs else ("warn" if warns else "ok")
        print(f"{name}: {status}")
        for e in errs:
            print("  ERROR", e)
        for w in warns:
            print("  warn ", w)

    print(f"\n{len(paths)} unit(s): {total_err} error(s), "
          f"{total_warn} warning(s)")
    return 1 if total_err else 0


if __name__ == "__main__":
    sys.exit(main())
