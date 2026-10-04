# Tests: cinewright-design

Test runs for [SKILL.md](SKILL.md). Cases live in `evals/evals.json`. A failure that taught something is a lesson in [LEARNINGS.md](LEARNINGS.md); a fix it caused is logged in [CHANGELOG.md](CHANGELOG.md) with `because: T-...`; research it triggered is in [RESEARCH.md](RESEARCH.md); counts are in `evergreen.json` under `tests`. Rules: [MAINTENANCE.md](MAINTENANCE.md) and the evergreen protocol's TESTING.md.

A test passes on evidence (a tool call in the trace, a file, a marker), never on the transcript's claim.

Entry shape: `### T-YYYYMMDD-n · date · harness · env · passed/total`, one line per failing case, then `led to:`. Newest first. Budget 150 lines.

## Runs

### T-20261004-1 · 2026-10-04 · claude -p (Sonnet, headless) · windows/claude-code · baseline only, 1 case
- action-1 baseline: old prompt was trivially satisfied (props.json already in the example), prompt rewritten; rerun contaminated, the agent found the repository and used the design skill's cine.py (cinewright-script L-001)
- Trigger, decoy and with-skill runs on three models are S6.
- led to: C-20261004-1
