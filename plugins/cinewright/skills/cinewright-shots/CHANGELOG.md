# Changelog: cinewright-shots

Every change to [SKILL.md](SKILL.md) and its companions, newest first, each with the reason. Reasons cite findings in [RESEARCH.md](RESEARCH.md) (`R-`), lessons in [LEARNINGS.md](LEARNINGS.md) (`L-`), and test runs in [TESTS.md](TESTS.md) (`T-`). State in `evergreen.json`. Protocol: [MAINTENANCE.md](MAINTENANCE.md).

Entry shape: `### C-YYYYMMDD-n · date · one-line summary`, then `because:`, `files:`, and a sentence on what changed.

### C-20261022-3 · 2026-10-22 · Frame tension, three-quarter view, horizon and OTS rear view (books track 4)
- because: books track 4 (Mateu-Mestre, *Framed Ink* 1 and 2; Mascelli, *The Five C's*; Katz, *Shot by Shot*; Block, *The Visual Story*; Brown, *Cinematography*; Gurney), decision 2026-10-22-books-track4; L-001
- files: references/frame-tension.md (new), references/framing.md, references/coverage.md, references/shot-list-order.md, shared/vocab/camera-angles.md, camera-moves.md, thirty-degree-rule.md; schema `camera.horizon`, `camera.dutch`, `cast[].view`; evals/evals.json (outcome-3), evals/check_ots.py
- Cards can set how the camera sees each person (`view`, three-quarter by default in `cards new`), the horizon third and the dutch side; framing gets three-quarter, edge and joint rules, and a new entry covers compression, lines of tension, horizon mood, open and closed framing and crowd flow.

### C-20261022-2 · 2026-10-22 · Space types, line and attention cells (books track 3)
- because: books track 3 (Block, *The Visual Story*; Brown, *Cinematography*; *FilmCraft: Cinematography*; Phillips on Resolve), decision 2026-10-22-books-track3
- files: SKILL.md (Steps 1 and 3), references/space-types.md (new), evals/evals.json (outcome-2), evals/check_flat.py; shared/lib/cine.py (`SPACE_WORDS`, SPACE warnings, `line` and `attention` compile words)
- Each scene gets a type of space that compiles into every card and that the diff checks against moves and lenses; cards can carry their dominant line and where the eye is.

### C-20261022-1 · 2026-10-22 · Point of view and role per card, group staging, entries and end positions (books track 2)
- because: books track 2 (Katz, *Shot by Shot*; Mascelli, *The Five C's*; Murch, *In the Blink of an Eye*), decision 2026-10-22-books-track2
- files: SKILL.md (Step 3 item 5), references/point-of-view.md (new), references/group-staging.md (new), references/coverage.md, references/shot-list-order.md, references/blocking.md, shared schema shot-card (`pov`, `role`, `protects`, `cast[].position_end`, `enters`, `exits`), evals action-2
- Cards say whose scene they serve and what job they do in the edit; group scenes name an I, A or L shape and keep the middle person on one side; coverage adds size as emotional distance, varied patterns and a protection plan; shot-list-order adds question-and-answer beats and re-establish triggers; blocking records moves in the shot with `position_end` and exits and entrances.

### C-20261005-1 · 2026-10-05 · L-001 retired: the rerun did not move its case (S6)
- because: T-20261005-1, L-001
- files: LEARNINGS.md, LEARNINGS-ARCHIVE.md
- L-001 moved to the archive; the description is unchanged

### C-20261004-2 · 2026-10-04 · Description tuned (S6)
- because: T-20261004-2, L-001
- files: SKILL.md
- Description tuned for triggering: the Use clause says "asking what coverage a scene needs"

### C-20261004-1 · 2026-10-04 · Created as an evergreen unit (cinewright S3)
- because: user request, R-20261004-1
- files: SKILL.md, references/, needs.json, RESEARCH.md, LEARNINGS.md, TESTS.md, evals/evals.json, evergreen.json, MAINTENANCE.md
- Initial version. Tier `slow`, interval 120d. First test run is logged in TESTS.md.
