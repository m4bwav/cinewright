# Tests: cinewright-curate

Test runs for [SKILL.md](SKILL.md). Cases live in `evals/evals.json`. A failure that taught something is a lesson in [LEARNINGS.md](LEARNINGS.md); a fix it caused is logged in [CHANGELOG.md](CHANGELOG.md) with `because: T-...`; research it triggered is in [RESEARCH.md](RESEARCH.md); counts and the failing list are in `evergreen.json` under `tests`. Rules: MAINTENANCE.md (testing section) and the plugin's `protocol/TESTING.md`.

A test passes on evidence (a tool call in the trace, a file, a marker, a log line), never on the transcript's claim that something was done.

Entry shape: `### T-YYYYMMDD-n · date · harness · env · passed/total`, then one line per failing case (`id · kind · class · what the evidence showed`), then `led to:` (L-, C-, R- ids or none). Newest first. Budget 150 lines; archive older runs to `TESTS-ARCHIVE.md`.

## Runs

### T-20261006-2 · 2026-10-06 · evals/run_evals.py (claude -p --restricted, dontAsk, fresh folder on another drive) · windows/claude-code, Claude Code 2.1.281 · 3/6 cases on all three models
- Models: H Haiku 4.5, S Sonnet 5, O Opus 5.5; with the skill 3 runs each; trigger counts are invocations.
- Cases: trigger-1 H 1/1 S 3/3 O 1/1; trigger-2 H 0/1 S 3/3 O 1/1; decoy-1 H 0/1 S 0/3 O 0/1; decoy-2 H 1/1 S 0/3 O 0/1; action-1 H 0/1 S 3/3 O 1/1; outcome-1 H 1/1 S 3/3 O 1/1.
- S7 first suite, budget week: Sonnet 3 runs per case, Haiku and Opus 1 run per case, one baseline per model; harness rev 2 with fixture repo
- FAIL trigger-2 · trigger · undertrigger · H 0/1 S 3/3 O 1/1 · Haiku only (1 run): answered without loading the skill; decision item 5 pattern, recorded not tuned
- FAIL decoy-2 · trigger · overtrigger · H 1/1 S 0/3 O 0/1 · Haiku only (1 run): took the chartwright knowledge-base note with the only knowledge-base skill loaded; recorded not tuned
- FAIL action-1 · action · no-op · H 0/1 S 3/3 O 1/1 · Haiku only (1 run): no kb verify call; Opus baseline also passed (found kb verify in the CLI help), so on Opus the action shows no gain
- led to: L-001, C-20261006-2

### T-20261006-1 · 2026-10-06 · not yet run · skill · 0/0
- Suite scaffolded; no run recorded. Write the cases in `evals/evals.json` (at least two trigger prompts, two decoys, one action case with evidence, one outcome case), run the baseline without the skill, then run with it (`evergreen-test`).
- led to: none
