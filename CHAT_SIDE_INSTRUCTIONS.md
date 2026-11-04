The study

A literary-unit-by-unit walk through Joshua with Lane, in English. Lane has a little Hebrew, so the English carries the language: transliterate and gloss every Hebrew word each time you use it, and print no native script (the style reference §5 has the scheme).

Lens: intertextuality first, then narrative structure, keyword tracing, type-scenes and the creation–covenant–exile–presence metanarrative. The style reference (§1 echo, §4 Balance) holds the proportions and Lane's examples. Prefer Joshua's own markers — Deuteronomistic framing, allotment formulae, Masoretic paragraph breaks, the conquest-summary tension with Judges 1 — over imposed symmetry.

Where things are

You research and produce files here. Lane downloads them and copies them into the repo, where Claude Code ports and builds them. You can't see the repo's working copy or run its tools.

Synced files (`synced-index.md` lists them all) aren't on disk and don't appear in listings, and reading them by name fails. Download the ones you need whole at the start of a chat, the index first, and search large files with grep or sed:
`curl -sLO https://raw.githubusercontent.com/lanehaden157/joshua/main/project-side/synced/<file>`
If curl fails, use the fetch tool on the same address. If that fails too, use project search, whose results are excerpts only, and tell Lane which files you couldn't read whole.

Commentaries are project docs: `project_info` lists them and you read them by exact name (if `/mnt/project/` exists they're there too). `resources.md` says which is which.

Save files you produce in `/mnt/user-data/outputs/` and hand each one over as a download.

How we work

Precedence is the ladder in `core-workflow.md` (Lane in chat, this field, the style reference, `core-workflow.md`, the handoff, reference files); flag a conflict to Lane rather than picking one. Two chats per unit. The research chat reads `resources.md`, the unit map, the unit's canon-leads sheet, `translation-choices.md` and the earlier units' meta, runs passes 1-3, asks Lane its questions in chat, and after Lane's yes on the box list writes `<book>_NN_handoff.md` (shape in `canon-handoff-template.md`) as an output file. Lane pastes it into a fresh chat in this project: the build chat reads the handoff, the style reference, `translation-choices.md` and `threads-digest.md`, does pass 4 without redoing the research, asks every open call by AskUserQuestion popup before drafting (ask about anything missing or contradictory rather than re-researching), and uses `questions[]` only for what's still open.

Joshua on top of the core workflow

- Research pass (pass 2): check the commentaries in `resources.md` for the intertexts they argue for or against. For the New Testament, reach past the obvious (Rahab → Matthew 1:5, Hebrews 11:31, James 2:25).
- Shipped units are rebuilt through the normal research-then-build loop.
