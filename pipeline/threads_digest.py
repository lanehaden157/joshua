"""data/threads.json  ->  threads-digest.md   (repo root)

A human-readable snapshot of the canonical cross-unit threads. Ported from
Projects/Matthew/pipeline/threads_digest.py unchanged in structure -- per
Port analysis.md §1.8, this script is pure generic-schema/generic-markup
logic, not Matthew- or Greek-specific.

Regenerate whenever threads.json changes (build.py will, once it exists --
see PLAN.md Phase 3). Never hand-edit threads-digest.md — it is derived.
Runs (and produces a valid, if nearly-empty, digest) even against an empty
threads.json -- this is deliberately exercised before unit 1 so the
generator/data round trip is proven working, not assumed.
"""

import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "data", "threads.json")
OUT = os.path.join(ROOT, "threads-digest.md")


def _ref(d):
    return f"{d.get('unit', '?')}" + (f" ({d['ref']})" if d.get("ref") else "")


def _declined():
    """roots.json's declined ledger, or {} when absent."""
    path = os.path.join(ROOT, "data", "roots.json")
    try:
        with open(path, encoding="utf-8") as f:
            return json.load(f).get("declined") or {}
    except (OSError, ValueError):
        return {}


def main():
    data = json.load(open(SRC, encoding="utf-8"))
    threads = data["threads"]
    openc = sum(1 for t in threads if t.get("status") == "open")

    lines = [
        "# Cross-unit threads — canonical digest",
        "",
        f"Generated from `data/threads.json` (version {data.get('version', '?')}). "
        f"{len(threads)} threads, {openc} open.",
        "",
        "**This is the source of truth for thread tagging.** In a unit's fragment, "
        "a root that appears in the `id` column below is a *tracked thread*: tag "
        "every occurrence `<span class=\"r\" data-root=\"<id>\" data-w=\"<word "
        "id>\">…</span>` (the OSHB word id from `Joshua-words.tsv`) and list it "
        "under `threads.opens` / `threads.payoffs` in the unit-meta block, with a "
        "matching id set in `data/roots.json`. A root that is recurring but *not* "
        "here is unit-local — tag it with its own name (no `data-w` needed) and "
        "just declare it in the unit's own `roots`. To propose promoting a local "
        "root to a tracked thread, add it to `threads.candidates` with a one-line "
        "reason (the Strong's/lemma `ids` you've actually observed in "
        "`Joshua-words.tsv`, plus a few representative `refs`, if you have them). "
        "**Claude decides, biased toward book-wide** (Lane, 2026-09-16): a local "
        "root that later pays off is worse than a tracked one that doesn't, so "
        "promote on a real second sighting. Ask Lane only when genuinely "
        "unsure.",
        "",
    ]

    if not threads:
        lines += [
            "*(No threads defined yet — this file exists to prove the "
            "`threads.json` → `threads-digest.md` round trip works before unit "
            "1, not because there's anything to digest. Regenerate once Lane "
            "adds the first thread.)*",
            "",
        ]
        open(OUT, "w", encoding="utf-8").write("\n".join(lines))
        print(f"wrote {OUT} — 0 threads (empty threads.json, round trip OK)")
        return

    lines += [
        "| id | root (data-root) | translit | gloss | opens | payoffs | status |",
        "|---|---|---|---|---|---|---|",
    ]
    for t in sorted(threads, key=lambda x: (x.get("opens", {}).get("unit", 99), x["id"])):
        payoffs = " · ".join(_ref(p) for p in t.get("payoffs", [])) or "—"
        lines.append(
            f"| `{t['id']}` | `{t['root']}` | {t.get('translit', '')} | "
            f"{t.get('gloss', '')} | {_ref(t.get('opens', {}))} | {payoffs} | "
            f"{t.get('status', '')} |"
        )

    lines += ["", "## Notes per thread", ""]
    for t in sorted(threads, key=lambda x: x["id"]):
        lines.append(f"- **`{t['id']}`**: {t.get('note', '').strip()}")

    # Declined candidates (review A13). This is the half of the promotion
    # record that used to live only in a session log, so the same root got
    # re-proposed every few units and re-argued from scratch.
    declined = _declined()
    if declined:
        lines += ["", "## Considered and kept local", "",
                  "These were proposed as threads and deliberately declined. "
                  "Don't re-propose one without a specific new payoff in "
                  "view -- say what changed.", ""]
        for slug, e in sorted(declined.items()):
            unit = f", unit {e['unit']}" if e.get("unit") else ""
            lines.append(f"- **`{slug}`** (declined {e.get('date', '?')}"
                         f"{unit}): {e.get('why', '').strip()}")

    lines.append("")
    open(OUT, "w", encoding="utf-8").write("\n".join(lines))
    print(f"wrote {OUT} — {len(threads)} threads, {len(declined)} declined")


if __name__ == "__main__":
    main()
