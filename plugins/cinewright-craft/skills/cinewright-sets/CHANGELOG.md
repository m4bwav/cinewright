# Changelog: cinewright-sets

Every change to [SKILL.md](SKILL.md) and its companions, newest first, each with the reason. Reasons cite findings in [RESEARCH.md](RESEARCH.md) (`R-`), lessons in [LEARNINGS.md](LEARNINGS.md) (`L-`), and test runs in [TESTS.md](TESTS.md) (`T-`). State in `evergreen.json`. Protocol: [MAINTENANCE.md](MAINTENANCE.md).

Entry shape: `### C-YYYYMMDD-n · date · one-line summary`, then `because:`, `files:`, and a sentence on what changed.

### C-20261007-2 · 2026-10-07 · Famous names pull the postcard view
- because: L-003
- files: references/wall-strings.md, LEARNINGS.md
- wall-strings gains the rule to describe geometry, not the name, outside the establishing view.

### C-20261007-1 · 2026-10-07 · Created as an evergreen unit
- because: user request, R-20261007-1, R-20261007-2, L-001, L-002
- files: SKILL.md, references/ (set-plan, wall-strings, master-plates, coverage-angles, set-light, set-check), needs.json, RESEARCH.md, LEARNINGS.md, TESTS.md, evals/evals.json, evals/check_walls.py, evergreen.json, MAINTENANCE.md; shared: location bible `walls`, shot card `camera.faces`, compile adds the faced wall, WALL check, validator `propertyNames`
- Initial version. Tier `moderate`, interval 30d, because the AI tooling for sets (3D worlds, angle-edit models, reference slots) changes monthly.
