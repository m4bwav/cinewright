# Changelog: cinewright-sets

Every change to [SKILL.md](SKILL.md) and its companions, newest first, each with the reason. Reasons cite findings in [RESEARCH.md](RESEARCH.md) (`R-`), lessons in [LEARNINGS.md](LEARNINGS.md) (`L-`), and test runs in [TESTS.md](TESTS.md) (`T-`). State in `evergreen.json`. Protocol: [MAINTENANCE.md](MAINTENANCE.md).

Entry shape: `### C-YYYYMMDD-n · date · one-line summary`, then `because:`, `files:`, and a sentence on what changed.

### C-20261015-2 · 2026-10-15 · First card against the set: control from the card's camera; the scene's sun names no wall
- because: L-005, L-006
- files: LEARNINGS.md
- The grid reference alone lost the room on the first card; Canny control from the card's own blockout camera kept it. The scene bible's sun line reaches every card, so it names no window.

### C-20261015-1 · 2026-10-15 · Blocking marks; light, plates and checks from a one-room field test
- because: user request (2026-10-15: sets, set references, blocking continuity, set LoRAs), L-003, L-004, research note ai-docs/research/2026-10-15-sets-and-loras.md
- files: references/blocking-marks.md (new), references/set-light.md, references/master-plates.md, references/set-check.md, SKILL.md (Step 1)
- Marks in metres per beat and cameras placed from them, with the derived checks; name a window wall's light only in its own plates; blockout plus Canny at a strength that keeps the hero's size, one grid reference; plate claims from a class render, asked twice.

### C-20261009-1 · 2026-10-09 · Blockout control
- because: user request (2026-10-09: research what AI film makers build to raise quality, and add the gaps: prop sheets, LoRAs, animatic, blockout control, identity scoring, one shared grade)
- files: SKILL.md (end of Step 3), references/blockout-control.md (new)
- A blockout or phone footage turned into a depth, pose or layout video drives motion through a model's control input; the entry covers sources, strengths and checks.

### C-20261007-1 · 2026-10-07 · Created as an evergreen unit
- because: user request, R-20261007-1, R-20261007-2, L-001, L-002
- files: SKILL.md, references/ (set-plan, wall-strings, master-plates, coverage-angles, set-light, set-check), needs.json, RESEARCH.md, LEARNINGS.md, TESTS.md, evals/evals.json, evals/check_walls.py, evergreen.json, MAINTENANCE.md; shared: location bible `walls`, shot card `camera.faces`, compile adds the faced wall, WALL check, validator `propertyNames`
- Initial version. Tier `moderate`, interval 30d, because the AI tooling for sets (3D worlds, angle-edit models, reference slots) changes monthly.
