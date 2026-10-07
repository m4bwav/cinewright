# Tests: cinewright-voice

Test runs for [SKILL.md](SKILL.md). Cases live in `evals/evals.json`. A failure that taught something is a lesson in [LEARNINGS.md](LEARNINGS.md); a fix it caused is logged in [CHANGELOG.md](CHANGELOG.md) with `because: T-...`; research it triggered is in [RESEARCH.md](RESEARCH.md); counts are in `evergreen.json` under `tests`. Rules: [MAINTENANCE.md](MAINTENANCE.md) and the evergreen protocol's TESTING.md.

A test passes on evidence (a tool call in the trace, a file, a marker), never on the transcript's claim.

Entry shape: `### T-YYYYMMDD-n · date · harness · env · passed/total`, one line per failing case, then `led to:`. Newest first. Budget 150 lines.

## Runs

### T-20261007-1 · 2026-10-07 · evals/run_evals.py (claude -p --restricted, dontAsk, fresh folder on another drive) · windows/claude-code · 7/7 cases on Sonnet
- Models: S Sonnet 5 only (Haiku and Opus deferred for budget); with the skill 3 runs each; trigger counts are invocations.
- Cases: trigger-1 S 3/3; trigger-2 S 3/3; decoy-1 S 0/3; decoy-2 S 0/3; decoy-3 S 0/3; action-1 S 3/3 (`cine.py voice ref` in every trace); outcome-1 S 3/3 (check_voices.py exit 0, judge 3/3).
- Baseline without the skill, one run: action-1 fail (no cine.py), outcome-1 fail (checks 0/1, judged 0/1).
- led to: none
