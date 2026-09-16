"""Keep project-side/synced/ current on GitHub, so a Claude.ai project's
GitHub-connector "sync" source always reflects the latest chat-side docs
with no manual re-pasting.

Copies each file in check_project_sync.TRACKED_FILES into
project-side/synced/<basename> (a flat, deliberately duplicated mirror --
see project-side/README.md), commits only if something actually changed,
and pushes to origin/main. Safe to run anytime, including on a schedule:
it's a no-op when nothing has changed.

Usage:
    python pipeline/sync_to_github.py
"""
import shutil
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from check_project_sync import ROOT, TRACKED_FILES  # noqa: E402

SYNCED_DIR = ROOT / "project-side" / "synced"


def run(*args):
    return subprocess.run(args, cwd=ROOT, capture_output=True, text=True, check=True)


def main() -> int:
    SYNCED_DIR.mkdir(parents=True, exist_ok=True)

    missing = []
    for rel in TRACKED_FILES:
        src = ROOT / rel
        if not src.exists():
            missing.append(rel)
            continue
        shutil.copyfile(src, SYNCED_DIR / Path(rel).name)

    if missing:
        print("MISSING on disk (skipped):")
        for rel in missing:
            print(f"  - {rel}")

    status = run("git", "status", "--porcelain", "--", str(SYNCED_DIR))
    if not status.stdout.strip():
        print("No changes to sync -- already up to date.")
        return 0

    changed = [line[3:] for line in status.stdout.splitlines()]
    run("git", "add", "--", str(SYNCED_DIR))
    message = "Sync project-side docs\n\n" + "\n".join(f"- {c}" for c in changed)
    run("git", "commit", "-m", message)
    run("git", "push")

    print("Synced and pushed:")
    for c in changed:
        print(f"  - {c}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
