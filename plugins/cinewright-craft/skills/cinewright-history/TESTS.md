# Tests: cinewright-history

Test runs for [SKILL.md](SKILL.md). Cases live in `evals/evals.json`. A failure that taught something is a lesson in [LEARNINGS.md](LEARNINGS.md); a fix it caused is logged in [CHANGELOG.md](CHANGELOG.md) with `because: T-...`; research it triggered is in [RESEARCH.md](RESEARCH.md); counts are in `evergreen.json` under `tests`. Rules: [MAINTENANCE.md](MAINTENANCE.md) and the evergreen protocol's TESTING.md.

A test passes on evidence (a tool call in the trace, a file, a marker), never on the transcript's claim.

Entry shape: `### T-YYYYMMDD-n · date · harness · env · passed/total`, one line per failing case, then `led to:`. Newest first. Budget 150 lines.

## Runs

### T-20261004-1 · 2026-10-04 · claude -p (Sonnet, headless, restricted scratch folder) · windows/claude-code · baselines only, 2 cases
- action-1 baseline: changed the render aspect to 2.39:1 (unrenderable), brand name in the look, hand-made compile. Globbed the home folder for SKILL.md (timed out, nothing found): not contaminated, but the sandbox let Glob leave the folder (L-002).
- outcome-1 baseline: passed without the skill; the case does not discriminate (replace in S6).
- Trigger, decoy and with-skill runs on three models are S6.
- led to: C-20261004-1, L-002
