"""Re-derive everything downstream of the committed fragments. Safe to re-run.

  1. apply_retrofit.py     fragment edits from retrofit-tags.json (idempotent:
                           strip_span / text / *_word / unwrap / retag / add)
  2. refresh_meta.py       regenerate each built fragment's unit-meta block
  3. scan_occurrences.py   -> data/occurrences.json
  4. verify_occurrences.py independent re-derivation + tagged-flag checks
  5. roots.py              data/roots.json integrity -- every id set resolves
                           to a lemma, no id in two roots, every threads.json
                           thread's root has a roots.json entry (new step,
                           Matthew has no equivalent -- Phase 0.6)
  6. threads_digest.py     data/threads.json -> threads-digest.md
  advisory:
  7. audit_thread_coverage.py  Hebrew vs. fragments -- thread tag-coverage
                               gaps in built units (never fails the build)
  8. check_project_sync.py    which project-side/README.md files have
                               changed since they were last pasted into the
                               Claude.ai project (never fails the build)

units/*.html are the source of truth here -- this script never regenerates
them from source-artifacts/. Adding a NEW unit is `port_artifact.py NN`, not
this.

Ported from Projects/Matthew/pipeline/build.py -- pure generic orchestration
(Port analysis.md §1.8), plus the roots.py step Joshua's id-based root
identity needs and Matthew's colour-string roots never did.
"""

import subprocess
import sys
import os

HERE = os.path.dirname(os.path.abspath(__file__))
STEPS = ["apply_retrofit.py", "refresh_meta.py", "scan_occurrences.py",
         "verify_occurrences.py", "roots.py", "threads_digest.py"]
ADVISORY = ["audit_thread_coverage.py"]  # run with --check, show output, never fail the build
ADVISORY_BARE = ["check_project_sync.py"]  # run with no args, show output, never fail the build


def main():
    env = dict(os.environ, PYTHONIOENCODING="utf-8")
    for s in STEPS:
        print(f"\n=== {s} ===")
        r = subprocess.run([sys.executable, os.path.join(HERE, s)], env=env)
        if r.returncode != 0:
            print(f"\nFAILED at {s}")
            sys.exit(r.returncode)
    for s in ADVISORY:
        print(f"\n=== {s} (advisory) ===")
        subprocess.run([sys.executable, os.path.join(HERE, s), "--check"], env=env)
    for s in ADVISORY_BARE:
        print(f"\n=== {s} (advisory) ===")
        subprocess.run([sys.executable, os.path.join(HERE, s)], env=env)
    print("\nbuild ok")


if __name__ == "__main__":
    main()
