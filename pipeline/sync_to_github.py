"""Kept so the JoshuaProjectSideSync scheduled task keeps working after the
move onto bible-core: it just runs `python -m biblecore sync` from the repo
root. Run that directly by hand."""
import os
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.exit(subprocess.call([sys.executable, "-m", "biblecore", "sync"], cwd=ROOT))
