# Handoff

## Current state
- S6 (evals and tuning) is in progress on branch `s6/evals`, pushed, no PR yet (the exit check does not pass). It branched off `origin/s4/camera-history`: PR #6 (S5) was merged into that branch, not into `main`, so `main` lacks S5 and the S6 PR to `main` will carry it. Mark's S4 and S5 reviews had no comments. The repo is private: https://github.com/m4bwav/cinewright.
- Built: the eval harness `evals/run_evals.py` (plan, run, report, regrade, rejudge, export-worth), `evals/inspect_run.py`, `evals/record_tests.py`; outcome checkers `check_cabin.py` (camera), `check_kubrick.py` (history), `check_mix.py` (sound), `check_veo.py` (genvideo). Design: [decisions/2026-10-05-eval-harness-and-model-matrix.md](decisions/2026-10-05-eval-harness-and-model-matrix.md); twelve harness faults and fixes: [solutions/2026-10-05-headless-evals-on-windows-dead-ends.md](solutions/2026-10-05-headless-evals-on-windows-dead-ends.md).
- Ran the three-model matrix (Haiku 4.5, Sonnet 5, Opus 5.5) on Mark's go, then two tuning rounds: ten descriptions, script, continuity, edit and qc bodies, and a `cine.py` fix (malformed bibles stop with what to fix, 64 tests). T-20261005-1 in every TESTS.md; the matrix and worth table are in [log.md](log.md).
- Worth: no CUT; 3 KEEP, 10 TRIM (real gain at 1.5x the cost or more). Shots and continuity do not overlap: no merge.

## In progress
- Exit check. Sonnet: four cases at 2 of 3 (design outcome, finish action, movement outcome, qc outcome). Opus: camera, continuity, movement, qc and script actions at 1 or 2 of 3; shots outcome (crash fixed, not rerun); continuity outcome (output rule fixed, not rerun). Haiku: most value cases and several triggers fail because Haiku answers without loading the skill; recorded with that reason after one description rewrite (decision item 5).
- The runtime budget row question is still unanswered: genvideo's folder reads 166 KB (yellow).

## Watch
- Opus's failing action runs share a pattern: its first compound shell command is refused by the harness (`dontAsk`), and it carries on without the check. Decide whether that is harness friction (allow more read-only compounds) or a skill rule ("run the check as its own command").
- Every run that changes a skill must rerun that skill's suite on all three models; runs at 5-6 in parallel hit the account's session limit in about two hours (the harness stops itself and reruns resume).
- Description budget: 3,888 of 4,000; curate needs about 200, so S7 reads yellow unless something is trimmed.
- Round-1 lessons say "rerun pending" in their Evidence lines; confirm or retire each against T-20261005-1.

## Next single action
- Run [next-session-prompt.md](next-session-prompt.md) (S6 continued: finish the exit check, open the PR).
