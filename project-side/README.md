# Project-side sync — index, not a copy of the canonical files

Every file in the table below has **one canonical copy**, at the repo path
linked. That's deliberate — `Claude_ai_chat_side_instructions.md` says it
outright: *"Matthew's contract lived in three places and drifted."* This
file exists so you don't have to hunt for the canonical paths.

**`project-side/synced/` is the one deliberate exception.** It holds a flat,
auto-generated *copy* of every tracked file's current content (basenames
only, e.g. `data/roots.json` → `synced/roots.json`), pushed to
`github.com/lanehaden157/joshua`. Point the Claude.ai project's GitHub
connector at that folder and its "sync" feature pulls fresh content on its
own — no re-pasting, ever. Never hand-edit anything under `synced/`; it's
overwritten on the next sync.

**What keeps it current:** `pipeline/sync_to_github.py` copies every
`TRACKED_FILES` entry into `synced/`, and if anything actually changed,
commits and pushes. A Windows scheduled task (`JoshuaProjectSideSync`,
`schtasks`/Task Scheduler) runs it every 15 minutes — it's a silent no-op
when nothing's changed. Run it by hand any time with:

```bash
python pipeline/sync_to_github.py
```

To check the task itself (last run, next run, result code):

```powershell
Get-ScheduledTaskInfo -TaskName "JoshuaProjectSideSync"
```

**Fallback for projects that can't use a GitHub connector** (e.g. one
that only takes uploaded files): `pipeline/check_project_sync.py` still
does the old hash-diff-and-tell-you-what-changed job —

```bash
python pipeline/check_project_sync.py               # what needs re-pasting
python pipeline/check_project_sync.py --mark-synced  # after you've pasted everything
```

— tracked separately in `project-side/sync-state.json`, and also run
advisory (non-failing) inside `pipeline/build.py`.

`resources.md` doesn't exist yet, so it isn't in `TRACKED_FILES` — add it
to the list in `pipeline/check_project_sync.py` (both scripts import from
there) once it's authored.

## Files

| file | direction | what it is | update cadence |
|---|---|---|---|
| [`joshua_study_style_reference.md`](../joshua_study_style_reference.md) | repo → project | The artifact contract — fragment shape, unit-meta schema, component whitelist, transliteration scheme, checklist | Re-paste whenever it changes |
| [`translation-choices.md`](../translation-choices.md) | repo → project | Hand-maintained glossary of deliberate English renderings | Edit **in the same turn** as any wording decision — this is the rule that saved a retroactive pass on Matthew |
| [`threads-digest.md`](../threads-digest.md) | repo → project | Generated snapshot of tracked cross-unit threads — source of truth for what to tag | Regenerate (`python pipeline/threads_digest.py`) any time `data/threads.json` changes; never hand-edit |
| [`resources.md`](../resources.md) | repo → project | **Missing — needs authoring.** `Claude_ai_chat_side_instructions.md` already points to it as "the single authored inventory" (Hebrew/word files, generated digests, the commentary set). Nothing reads it yet because it doesn't exist. | N/A until created |
| [`data/roots.json`](../data/roots.json) | repo → project | Tracked-thread root identity — hand-curated Strong's/lemma id sets per root (style reference §2) | Re-paste whenever a root's id set changes |
| [`Joshua-words.tsv`](../Joshua-words.tsv) | repo → project | Per-word OSHB data (`word_id, ref, surface, lemma, morph`) — the thing every Hebrew string in an artifact must be pulled from, never hand-typed (style reference §2) | Static once generated; only changes if the corpus pin changes |

**No longer synced** (Lane's call, 2026-09-16): `Claude_ai_chat_side_instructions.md`,
`Joshua-reading.txt`, `Joshua-english.txt`. All three still exist at their
repo paths and are still authoritative there — they're just out of the
`project-side/synced/` loop now.

## Also worth knowing about, not part of the sync loop

- [`CLAUDE.md`](../CLAUDE.md) — how *this repo* behaves (pipeline, pins,
  verification). Repo-side only; the project doesn't need it.
- [`PLAN.md`](../PLAN.md) — phase list and open questions. Repo-side only.
- [`Port analysis.md`](../Port analysis.md) — the audit this whole structure
  was designed against. Reference, not a live sync file.
- [`joshua_literary_unit_map.md`](../joshua_literary_unit_map.md) — fulfills
  the style reference's §9 TODO (unit numbers/slugs/passages/movements).
  Worth pasting into the project once at kickoff; not a per-turn sync file
  unless the map itself changes.
