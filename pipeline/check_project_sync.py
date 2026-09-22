"""Detect which project-side files have changed since they were last pasted
into the Claude.ai project.

Tracks a git blob hash per file in project-side/sync-state.json. A file's
hash changes the instant its content changes, whether or not that change is
committed -- this is a content fingerprint, not a commit check.

Usage:
    python pipeline/check_project_sync.py              # report drift
    python pipeline/check_project_sync.py --mark-synced             # mark ALL tracked files synced now
    python pipeline/check_project_sync.py --mark-synced FILE [FILE ...]  # mark only these synced
"""
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
STATE_PATH = ROOT / "project-side" / "sync-state.json"

# Repo-relative paths of every file that has to round-trip into the
# Claude.ai project. Keep in sync with project-side/README.md's table.
TRACKED_FILES = [
    "joshua_study_style_reference.md",
    "translation-choices.md",
    "threads-digest.md",
    "data/roots.json",
    "Joshua-words.tsv",
] + sorted(  # the intertext pass's reading lists, one per unit (pipeline/canon_leads.py)
    p.relative_to(ROOT).as_posix() for p in (ROOT / "canon-leads").glob("canon-leads-unit-*.md"))


def hash_file(path: Path) -> str | None:
    if not path.exists():
        return None
    result = subprocess.run(
        ["git", "hash-object", str(path)],
        cwd=ROOT, capture_output=True, text=True, check=True,
    )
    return result.stdout.strip()


def load_state() -> dict:
    if not STATE_PATH.exists():
        return {}
    return json.loads(STATE_PATH.read_text(encoding="utf-8"))


def save_state(state: dict) -> None:
    STATE_PATH.parent.mkdir(parents=True, exist_ok=True)
    STATE_PATH.write_text(
        json.dumps(state, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )


def main() -> int:
    args = sys.argv[1:]
    state = load_state()

    if args and args[0] == "--mark-synced":
        targets = args[1:] or TRACKED_FILES
        now = datetime.now(timezone.utc).isoformat(timespec="seconds")
        for rel in targets:
            if rel not in TRACKED_FILES:
                print(f"  skip (not tracked): {rel}")
                continue
            h = hash_file(ROOT / rel)
            if h is None:
                print(f"  skip (missing on disk): {rel}")
                continue
            state[rel] = {"hash": h, "synced_at": now}
            print(f"  marked synced: {rel}")
        save_state(state)
        return 0

    stale = []
    missing = []
    ok = []
    for rel in TRACKED_FILES:
        path = ROOT / rel
        current = hash_file(path)
        if current is None:
            missing.append(rel)
            continue
        recorded = state.get(rel, {}).get("hash")
        if recorded is None or recorded != current:
            stale.append(rel)
        else:
            ok.append(rel)

    if stale:
        print("NEEDS RE-PASTE into the Claude.ai project:")
        for rel in stale:
            print(f"  - {rel}")
    if missing:
        print("MISSING on disk (referenced but not found):")
        for rel in missing:
            print(f"  - {rel}")
    if ok and not stale:
        print("Everything tracked is in sync.")
    elif ok:
        print(f"\n({len(ok)} file(s) already in sync)")

    return 1 if stale else 0


if __name__ == "__main__":
    raise SystemExit(main())
