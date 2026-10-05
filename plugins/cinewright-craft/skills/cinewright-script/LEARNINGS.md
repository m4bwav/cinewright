# Learnings: cinewright-script

Procedural lessons for [SKILL.md](SKILL.md). Research findings live in [RESEARCH.md](RESEARCH.md); every change is logged in [CHANGELOG.md](CHANGELOG.md); test runs in [TESTS.md](TESTS.md); state in `evergreen.json`. Format: [MAINTENANCE.md](MAINTENANCE.md) (LEARNINGS-FORMAT in the evergreen protocol). Retired entries go to LEARNINGS-ARCHIVE.md with a reason.

Write an entry the moment a real signal happens: a user correction, the same error twice, a workaround, an environment fact, a failed test. Check existing entries first: add, update, retire or none. Trigger and Hypothesis are required.

## Active

### L-001 · 2026-10-04 · A without-skill baseline is contaminated when the agent can find the repository on disk
- Trigger: 2026-10-04, S3 baselines: two of four headless runs in bare scratch folders searched the whole disk (`find /`), found the cinewright repository because the copied example names it, and ran its cine.py (T-20261004-1)
- Hypothesis: A capable agent with a hint in the files and filesystem access looks for the tool the files mention; a bare working folder does not hide the rest of the disk
- Rule: Run baselines where the repository cannot be reached (another machine, a cloud session, or a sandbox limited to the working folder), and strip skill names from copied fixtures; mark any run that touched the repository as contaminated, never as a pass or fail
- Evidence: T-20261004-1 in this unit, cinewright-design and the S3 log, confirmed 2026-10-04
- Scope: skill
- Status: active · helpful 1 · harmful 0 · last_confirmed 2026-10-04

### L-002 · 2026-10-04 · Check a changed line with the diff, not by counting
- Trigger: 2026-10-04, S6 matrix T-20261004-2: action-1 (would a longer line fit card 1B; check it properly) invoked the skill but ran no `continuity diff` in Sonnet 1 of 3 and Opus 1 of 3 runs; those runs counted the words by hand (17 words in 4 s) and answered
- Hypothesis: Step 4 said to run the diff "once cards exist", which reads as part of a first pass, and the arithmetic looks easy enough to skip the tool
- Rule: Whenever a line changes, put it in its card and run `CINE continuity diff`; quote the DIALOGUE warning; never count words by hand instead
- Evidence: C-20261004-2 (SKILL.md Step 4); rerun pending
- Scope: skill
- Status: active · helpful 0 · harmful 0 · last_confirmed 2026-10-04
