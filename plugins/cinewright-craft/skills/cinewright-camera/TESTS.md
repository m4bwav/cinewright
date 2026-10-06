# Tests: cinewright-camera

Test runs for [SKILL.md](SKILL.md). Cases live in `evals/evals.json`. A failure that taught something is a lesson in [LEARNINGS.md](LEARNINGS.md); a fix it caused is logged in [CHANGELOG.md](CHANGELOG.md) with `because: T-...`; research it triggered is in [RESEARCH.md](RESEARCH.md); counts are in `evergreen.json` under `tests`. Rules: [MAINTENANCE.md](MAINTENANCE.md) and the evergreen protocol's TESTING.md.

A test passes on evidence (a tool call in the trace, a file, a marker), never on the transcript's claim.

Entry shape: `### T-YYYYMMDD-n · date · harness · env · passed/total`, one line per failing case, then `led to:`. Newest first. Budget 150 lines.

## Runs

### T-20261005-1 · 2026-10-05 · evals/run_evals.py (claude -p --restricted, dontAsk, fresh folder on another drive) · windows/claude-code, Claude Code 2.1.281 · 4/7 cases on all three models
- Models: H Haiku 4.5, S Sonnet 5, O Opus 5.5; with the skill 3 runs each; trigger counts are invocations.
- Cases: trigger-1 H 3/3 S 3/3 O 3/3; trigger-2 H 3/3 S 3/3 O 3/3; decoy-1 H 0/3 S 0/3 O 0/3; decoy-2 H 0/3 S 0/3 O 0/3; decoy-3 H 3/3 S 0/3 O 0/3; action-1 H 2/3 S 3/3 O 1/3; outcome-1 H 0/3 S 3/3 O 3/3.
- Tuning rounds 1 and 2: value cases rerun on all models with a 60-turn cap and full-reply judging; triggers of the ten skills whose descriptions changed rerun. Haiku 4.5 failures are mostly the skill not invoked (the model answers in one turn); after one description rewrite they are recorded, not tuned further. Worth (pooled with versus without): no CUT.
- FAIL decoy-3 · trigger · overtrigger · H 3/3 S 0/3 O 0/3 · Haiku after C-20261005-1 ('lighting a shot'); Sonnet's 1 of 3 on the same decoy is gone
- FAIL action-1 · action · no-op · H 2/3 S 3/3 O 1/3 · Opus: the first compound shell command was refused (dontAsk), then it edited the cards and never ran the check
- FAIL outcome-1 · outcome · undertrigger (skill not invoked in 3 of 3 failing runs) · H 0/3 S 3/3 O 3/3 · Haiku: compile not reached
- led to: C-20261005-1

### T-20261004-2 · 2026-10-04 · evals/run_evals.py (claude -p --restricted, dontAsk, fresh folder on another drive) · windows/claude-code, Claude Code 2.1.281 · 4/7 cases on all three models
- Models: H Haiku 4.5, S Sonnet 5, O Opus 5.5; with the skill 3 runs each; trigger counts are invocations.
- Cases: trigger-1 H 1/3 S 3/3 O 3/3; trigger-2 H 3/3 S 3/3 O 3/3; decoy-1 H 0/3 S 0/3 O 0/3; decoy-2 H 0/3 S 0/3 O 0/3; decoy-3 H 0/3 S 0/3 O 0/3; action-1 H 1/3 S 3/3 O 3/3; outcome-1 H 0/3 S 0/3 O 0/3.
- First S6 matrix after three harness fixes (cine.py by any path, setup copies, deterministic checks); 155 runs that hit the account's session limit were run again.
- FAIL trigger-1 · trigger · undertrigger · H 1/3 S 3/3 O 3/3
- FAIL action-1 · action · no-op · H 1/3 S 3/3 O 3/3 · evidence is now the trace only: two baselines passed on the style file
- FAIL outcome-1 · outcome · wrong-outcome · H 0/3 S 0/3 O 0/3 · harness: the compile needs genvideo's model cards in the core plugin, not loaded in this run; the case now loads it (plugins)
- led to: L-002, C-20261004-2

### T-20261004-1 · 2026-10-04 · claude -p (Sonnet, headless, restricted scratch folder) · windows/claude-code · baselines only, 2 cases
- action-1 baseline: craft right, data wrong: invented `frame` field, lighting string over the 200-character schema limit, no check run. Not contaminated.
- outcome-1 baseline: passed without the skill; the case does not discriminate (replace in S6).
- Trigger, decoy and with-skill runs on three models are S6.
- led to: C-20261004-1
