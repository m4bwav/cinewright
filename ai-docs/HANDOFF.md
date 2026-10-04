# Handoff

## Current state
- S3 (pre-production craft) was done on 2026-10-04 on branch `s3/preproduction` off `main` (the S2 PR #3 was merged with no comments). Its PR (#4, https://github.com/m4bwav/cinewright/pull/4) waits for Mark's review. The repo is private: https://github.com/m4bwav/cinewright.
- Built: `cinewright-shots` in core; `cinewright-script`, `cinewright-design` and `cinewright-movement` in craft (17 knowledge entries, each a full evergreen unit with evals and a baseline). Runtime: optional `bibles/props.json` (schema, validate, compile pastes the description with a verbatim guard, diff, qc rubric), `cards list`, DIALOGUE and HARD-SUBJECT diff warnings. The thirty-degree rule moved to shared vocab. 57 tests. Layout: [../CODEMAP.md](../CODEMAP.md).
- The example now runs brief, script, design notes, shot list, bibles with props, a clean diff and compiles for Veo and MiniMax H3 ([../examples/three-shot/README.md](../examples/three-shot/README.md)).
- Mark's answer on the model-card budget row was applied: cards are green at 900 est. tokens ([decision](decisions/2026-10-03-proposed-model-card-budget-row.md)).
- Exit check outputs are quoted in [log.md](log.md).

## In progress
- Mark's review of the S3 PR, and one question: the proposed runtime budget row ([decision](decisions/2026-10-04-proposed-runtime-budget-row.md)). Until then the budget reads YELLOW on one row: the genvideo folder at 152 of 150 KB, because the 70 KB runtime copy grew.

## Decisions made this session
- Prop bible and pre-production checks ([decision](decisions/2026-10-04-prop-bible-and-pre-production-checks.md)).
- `test_budget_green` became `test_budget_not_red`, matching PLAN §6 (CI fails at red; yellow is reported).

## Watch
- The H3 sequence prompt of the example is 377 words against a 300-word guide (S2's 336-word take rendered well). Watch for loss of detail on the next local render.
- Veo Gemini API preview IDs shut down 2026-10-22; re-check before any hosted render.
- Description budget: 8 skills use 2,403 of 4,000 characters; the remaining five skills need about 300 each.
- Unverified: 2.5 words a second per model; the 9:16 button areas; the local animal resolution figure (one model).

## Next single action
- After Mark reviews the S3 PR, run [next-session-prompt.md](next-session-prompt.md) (S4: camera, lighting and history).
