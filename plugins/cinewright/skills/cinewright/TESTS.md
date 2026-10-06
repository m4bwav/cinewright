# Tests: cinewright

Test runs for [SKILL.md](SKILL.md). Cases live in `evals/evals.json`. A failure that taught something is a lesson in [LEARNINGS.md](LEARNINGS.md); a fix it caused is logged in [CHANGELOG.md](CHANGELOG.md) with `because: T-...`; research it triggered is in [RESEARCH.md](RESEARCH.md); counts are in `evergreen.json` under `tests`. Rules: [MAINTENANCE.md](MAINTENANCE.md) and the evergreen protocol's TESTING.md.

A test passes on evidence (a tool call in the trace, a file, a marker), never on the transcript's claim.

Entry shape: `### T-YYYYMMDD-n · date · harness · env · passed/total`, one line per failing case, then `led to:`. Newest first. Budget 150 lines.

## Runs

### T-20261005-2 · 2026-10-05 · evals/run_evals.py (claude -p --restricted, dontAsk, fresh folder on another drive) · windows/claude-code, Claude Code 2.1.281 · 4/7 cases on all three models
- Models: H Haiku 4.5, S Sonnet 5, O Opus 5.5; with the skill 3 runs each; trigger counts are invocations.
- Cases: trigger-1 H 0/3 S 3/3 O 3/3; trigger-2 H 3/3 S 3/3 O 3/3; decoy-1 H 0/3 S 0/3 O 0/3; decoy-2 H 0/3 S 0/3 O 0/3; decoy-3 H 0/3 S 0/3 O 0/3; action-1 H 1/3 S 3/3 O 3/3; outcome-1 H 1/3 S 3/3 O 3/3.
- Mixed harness: rev 2 (a refused command covers that command only) for the 2026-10-05 reruns of the Sonnet and Opus failures, rev 1 for the rest; a full rev-2 rerun is deferred for budget. Haiku-only failures: decision item 5 (answers without loading the skill).
- FAIL trigger-1 · trigger · undertrigger · H 0/3 S 3/3 O 3/3
- FAIL action-1 · action · no-op · H 1/3 S 3/3 O 3/3
- FAIL outcome-1 · outcome · wrong-outcome · H 1/3 S 3/3 O 3/3
- led to: none

### T-20261005-1 · 2026-10-05 · evals/run_evals.py (claude -p --restricted, dontAsk, fresh folder on another drive) · windows/claude-code, Claude Code 2.1.281 · 4/7 cases on all three models
- Models: H Haiku 4.5, S Sonnet 5, O Opus 5.5; with the skill 3 runs each; trigger counts are invocations.
- Cases: trigger-1 H 0/3 S 3/3 O 3/3; trigger-2 H 3/3 S 3/3 O 3/3; decoy-1 H 0/3 S 0/3 O 0/3; decoy-2 H 0/3 S 0/3 O 0/3; decoy-3 H 0/3 S 0/3 O 0/3; action-1 H 1/3 S 3/3 O 3/3; outcome-1 H 1/3 S 3/3 O 3/3.
- Tuning rounds 1 and 2: value cases rerun on all models with a 60-turn cap and full-reply judging; triggers of the ten skills whose descriptions changed rerun. Haiku 4.5 failures are mostly the skill not invoked (the model answers in one turn); after one description rewrite they are recorded, not tuned further. Worth (pooled with versus without): no CUT.
- FAIL trigger-1 · trigger · undertrigger · H 0/3 S 3/3 O 3/3 · Haiku answered with no tool; was 3 of 3 in the first matrix, so Haiku noise at 3 runs
- FAIL action-1 · action · no-op · H 1/3 S 3/3 O 3/3 · Haiku did not invoke the skill in 2 of 3
- FAIL outcome-1 · outcome · wrong-outcome · H 1/3 S 3/3 O 3/3 · Haiku did not invoke the skill in 2 of 3
- led to: none

### T-20261004-1 · 2026-10-04 · evals/run_evals.py (claude -p --restricted, dontAsk, fresh folder on another drive) · windows/claude-code, Claude Code 2.1.281 · 4/7 cases on all three models
- Models: H Haiku 4.5, S Sonnet 5, O Opus 5.5; with the skill 3 runs each; trigger counts are invocations.
- Cases: trigger-1 H 3/3 S 3/3 O 3/3; trigger-2 H 0/3 S 3/3 O 3/3; decoy-1 H 0/3 S 0/3 O 0/3; decoy-2 H 0/3 S 0/3 O 0/3; decoy-3 H 0/3 S 0/3 O 0/3; action-1 H 2/3 S 3/3 O 3/3; outcome-1 H 1/3 S 3/3 O 3/3.
- First S6 matrix after three harness fixes (cine.py by any path, setup copies, deterministic checks); 155 runs that hit the account's session limit were run again.
- FAIL trigger-2 · trigger · undertrigger · H 0/3 S 3/3 O 3/3
- FAIL action-1 · action · no-op · H 2/3 S 3/3 O 3/3 · evidence is now the trace only: two baselines passed on characters.json
- FAIL outcome-1 · outcome · wrong-outcome · H 1/3 S 3/3 O 3/3
- led to: L-001, C-20261004-3

### T-20261003-1 · 2026-10-03 · claude -p (Sonnet, headless) · windows/claude-code · baseline only, 1 case
- action-1 baseline without the skill: no bibles, cards or check; wrote a renderer's film.json and prompts directly (evidence absent)
- Trigger, decoy and with-skill runs on three models are S6.
- led to: none
