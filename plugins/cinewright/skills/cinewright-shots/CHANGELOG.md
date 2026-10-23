# Changelog: cinewright-shots

Every change to [SKILL.md](SKILL.md) and its companions, newest first, each with the reason. Reasons cite findings in [RESEARCH.md](RESEARCH.md) (`R-`), lessons in [LEARNINGS.md](LEARNINGS.md) (`L-`), and test runs in [TESTS.md](TESTS.md) (`T-`). State in `evergreen.json`. Protocol: [MAINTENANCE.md](MAINTENANCE.md).

Entry shape: `### C-YYYYMMDD-n · date · one-line summary`, then `because:`, `files:`, and a sentence on what changed.

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
