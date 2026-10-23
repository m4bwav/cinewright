# Tests: cinewright-sets

Test runs for [SKILL.md](SKILL.md). Cases live in `evals/evals.json`. A failure that taught something is a lesson in [LEARNINGS.md](LEARNINGS.md); a fix it caused is logged in [CHANGELOG.md](CHANGELOG.md) with `because: T-...`; research it triggered is in [RESEARCH.md](RESEARCH.md); counts are in `evergreen.json` under `tests`. Rules: [MAINTENANCE.md](MAINTENANCE.md) and the evergreen protocol's TESTING.md.

A test passes on evidence (a tool call in the trace, a file, a marker), never on the transcript's claim.

Entry shape: `### T-YYYYMMDD-n · date · harness · env · passed/total`, one line per failing case, then `led to:`. Newest first. Budget 150 lines.

## Runs

### T-20261022-1 · 2026-10-22 · evals/run_evals.py, Sonnet · Windows 11 dev machine · 3/3 after a description fix; triggers 12/12
- action-blender (new) · first pass 0/3: no run loaded the skill (one loaded cinewright-finish, then answered alone). The answers were sound Blender advice but none read the entry. After C-20261022-2 named blockout control passes in the description: 3/3, each ran `cine.py kb show blender-passes`. Baseline 0/1.
- trigger-1, trigger-2, decoy-1, decoy-2 rerun after the description change: 12/12.
- led to: C-20261022-2, L-003

None yet. Seven cases written at creation (two triggers, two decoys, one action, two outcomes; outcome-1 is checked by `evals/check_walls.py`). The runtime side (walls in compile, the WALL error, wall key names) is covered by three unit tests in `tests/test_cine.py`.
