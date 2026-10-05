# Tests: cinewright-genvideo

Test runs for [SKILL.md](SKILL.md). Cases live in `evals/evals.json`. A failure that taught something is a lesson in [LEARNINGS.md](LEARNINGS.md); a fix it caused is logged in [CHANGELOG.md](CHANGELOG.md) with `because: T-...`; research it triggered is in [RESEARCH.md](RESEARCH.md); counts are in `evergreen.json` under `tests`. Rules: [MAINTENANCE.md](MAINTENANCE.md) and the evergreen protocol's TESTING.md.

A test passes on evidence (a tool call in the trace, a file, a marker), never on the transcript's claim.

Entry shape: `### T-YYYYMMDD-n · date · harness · env · passed/total`, one line per failing case, then `led to:`. Newest first. Budget 150 lines.

## Runs

### T-20261004-1 · 2026-10-04 · evals/run_evals.py (claude -p --restricted, dontAsk, fresh folder on another drive) · windows/claude-code, Claude Code 2.1.281 · 3/7 cases on all three models
- Models: H Haiku 4.5, S Sonnet 5, O Opus 5.5; with the skill 3 runs each; trigger counts are invocations.
- Cases: trigger-1 H 0/3 S 3/3 O 3/3; trigger-2 H 0/3 S 3/3 O 3/3; decoy-1 H 0/3 S 0/3 O 0/3; decoy-2 H 0/3 S 0/3 O 0/3; decoy-3 H 0/3 S 0/3 O 0/3; action-1 H 2/3 S 3/3 O 3/3; outcome-1 H 0/3 S 3/3 O 1/3.
- First S6 matrix after three harness fixes (cine.py by any path, setup copies, deterministic checks); 155 runs that hit the account's session limit were run again.
- FAIL trigger-1 · trigger · undertrigger · H 0/3 S 3/3 O 3/3
- FAIL trigger-2 · trigger · undertrigger · H 0/3 S 3/3 O 3/3
- FAIL action-1 · action · undertrigger (skill not invoked in 1 of 1 failing runs) · H 2/3 S 3/3 O 3/3 · evidence is now the trace only: two baselines passed on a hand-written 1A.txt
- FAIL outcome-1 · outcome · undertrigger (skill not invoked in 3 of 5 failing runs) · H 0/3 S 3/3 O 1/3
- led to: L-006, C-20261004-2

### T-20261003-2 · 2026-10-03 · unittest (repo tests) · windows/claude-code · 12/12 model-card tests
- One test per model checks shape, order and syntax with a regex that also matches the vendor's own example; the identity guard is tested on every model. Python 3.14 and 3.9.
- led to: C-20261003-2

### T-20261003-1 · 2026-10-03 · claude -p (Sonnet, headless) · windows/claude-code · baseline only, 1 case
- action-1 baseline without the skill: ran out of turns searching for a compiler; no prompt written (evidence absent)
- Trigger, decoy and with-skill runs on three models are S6.
- led to: none
