# Handoff

## Current state
- S6 (evals and tuning) is done on branch `s6/evals`, pushed, with a PR to `main` waiting for Mark's review (assigned, label needs-review). The PR also carries S5: PR #6 was merged into `s4/camera-history`, not `main`. The repo is private: https://github.com/m4bwav/cinewright.
- Exit check passed on 2026-10-05: Sonnet 88 of 88 cases, Opus 87 of 88 (continuity outcome-1, a recorded judge split), Haiku 52 of 88 (36 failures recorded under decision item 5); no skill CUT (4 KEEP, 9 TRIM); T-20261005-2 in every TESTS.md; tests on 3.14 and 3.9, kb lint, plugin validate and evergreen lint pass; budget YELLOW only on genvideo's folder (the unanswered runtime row). Output quoted in [log.md](log.md).
- Harness rev 2: both arms are told a refused command covers that command only. It fixed every Opus failure (the harness refused one command and Opus gave up on the shell). The record is mixed: rev 2 for the reruns of the Sonnet and Opus failures, rev 1 for the rest, said in each T- entry. [solutions/2026-10-05-headless-evals-on-windows-dead-ends.md](solutions/2026-10-05-headless-evals-on-windows-dead-ends.md), [decisions/2026-10-05-eval-harness-and-model-matrix.md](decisions/2026-10-05-eval-harness-and-model-matrix.md).
- Lessons: nine confirmed, three retired to LEARNINGS-ARCHIVE.md (edit L-003, genvideo L-006, shots L-001).

## In progress
- Nothing running. Waiting on Mark's review of the S6 PR.

## Deferred (Mark's budget call, 2026-10-05: weekly limit until Wednesday 2026-10-08)
- A full rev-2 rerun of the action and outcome cases (312 runs, three models, both arms) would make the record one harness. Optional; ask before starting.
- Continuity outcome-1 on Opus (judge split) and the Sonnet 1-in-3 slips (finish action, movement and qc outcomes; 3 of 3 on rev 2) were recorded, not tuned.
- TRIM verdicts on nine skills are recommendations; cut nothing without Mark.

## Watch
- Runtime budget row question (decisions/2026-10-04-proposed-runtime-budget-row.md) still unanswered: genvideo's folder 167 KB, yellow.
- Description budget 3,888 of 4,000; curate needs about 200, so S7 reads yellow unless something is trimmed. Tell Mark in one line.
- A skill edit means rerunning its suite on all three models (about 60 runs); commit before every run batch.

## Next single action
- Run [next-session-prompt.md](next-session-prompt.md) (S7: cinewright-curate, packaging, install proof) once Mark has reviewed the S6 PR.
