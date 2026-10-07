# Learnings: cinewright-curate

Procedural lessons for [SKILL.md](SKILL.md). Research findings live in [RESEARCH.md](RESEARCH.md); every change is logged in [CHANGELOG.md](CHANGELOG.md); test runs in [TESTS.md](TESTS.md); state in `evergreen.json`. Format and write-time gate: MAINTENANCE.md (LEARNINGS-FORMAT). Retired entries go to LEARNINGS-ARCHIVE.md with a reason.

Write an entry the moment a real signal happens: a user correction, the same error twice, a discovered workaround, an environment fact, a stated preference, a failed test or a failure in use. Check existing entries first, by meaning (`evergreen.py search "<the lesson>" --kinds learnings` finds near-duplicates in every registered unit): add / update / retire / none. Trigger and Hypothesis are required. Promote after three confirmations; retire when harmful > helpful.

## Active

<!-- Example (delete once you have a real entry):
### L-001 · 2026-10-06 · One-line lesson in plain words
- Trigger: what happened, with dates or counts
- Hypothesis: why
- Rule: the shortest instruction that prevents the trigger
- Evidence: C-20261006-1, T-20261006-1, confirmed 2026-10-06
- Scope: skill | repo:<slug> | env:<name> | global
- Status: active · helpful 1 · harmful 0 · last_confirmed 2026-10-06
-->

### L-001 · 2026-10-06 · `optional-flag-copied`: a bracketed optional flag in a command table gets copied
- Trigger: T-20261006-1, outcome-1 on Sonnet 0 of 3: every run retired a model that was "shut down for good" with `--status deprecated`, copied from the table row `kb retire <slug> --reason R [--status deprecated]`.
- Hypothesis: the model reads the bracketed option as part of the command to run, and the row named both cases at once.
- Rule: one table row per case, each with the exact command it needs; name the default in words, never as a bracketed flag.
- Evidence: C-20261006-2; T-20261006-2 rerun after the edit: Sonnet outcome-1 3 of 3, confirmed 2026-10-06
- Scope: skill
- Status: active · helpful 0 · harmful 0 · last_confirmed 2026-10-06
