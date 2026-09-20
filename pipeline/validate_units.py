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
from port_artifact import DE_MIN, _de, roots_in_fragment  # noqa: E402

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


def check_colours(slug, colours):
    """Report any pair of roots in one unit closer than DE_MIN."""
    errs = []
    items = sorted(colours.items())
    for i, (ra, ca) in enumerate(items):
        for rb, cb in items[i + 1:]:
            d = _de(ca, cb)
            if d < DE_MIN:
                errs.append(f"colour collision: '{ra}' ({ca}) and '{rb}' "
                            f"({cb}) are dE={d:.1f}, under {DE_MIN} -- a "
                            f"reader cannot tell these two apart")
    return errs


def main():
    threads_json = um._load("threads.json")
    units_json = um._load("units.json")
    threads = {t["root"]: t for t in threads_json["threads"]}

    paths = sorted(glob.glob(os.path.join(UNITS, "unit-*.html")))
    if not paths:
        print("no built units to validate")
        return 0

    total_err = total_warn = 0
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
