# Changelog: cinewright-continuity

Every change to [SKILL.md](SKILL.md) and its companions, newest first, each with the reason. Reasons cite findings in [RESEARCH.md](RESEARCH.md) (`R-`), lessons in [LEARNINGS.md](LEARNINGS.md) (`L-`), and test runs in [TESTS.md](TESTS.md) (`T-`). State in `evergreen.json`. Protocol: [MAINTENANCE.md](MAINTENANCE.md).

Entry shape: `### C-YYYYMMDD-n · date · one-line summary`, then `because:`, `files:`, and a sentence on what changed.

### C-20261005-1 · 2026-10-05 · Output ranks the diff's errors above by-eye doubts (S6)
- because: T-20261004-1, L-005
- files: SKILL.md
- The Output section reports as errors only what the diff or a named rule finds, and puts one by-eye doubt last as a question

### C-20261004-1 · 2026-10-04 · Thirty-degree rule shared with cinewright-shots; prop bible and two new diff codes
- because: user request (cinewright S3); first local render's prop drift (cinewright-design L-003)
- files: references/thirty-degree-rule.md (now a copy of shared/vocab), references/shot-checklist.md, SKILL.md, needs.json
- The thirty-degree entry moved to shared vocab so shots and continuity read one source. Step 1 lists `bibles/props.json`. The checklist adds DIALOGUE and HARD-SUBJECT warnings and the PROP warning for a held prop with no description.

### C-20261003-1 · 2026-10-03 · Created as an evergreen unit (cinewright S1)
- because: user request, R-20261003-1
- files: SKILL.md, references/, needs.json, RESEARCH.md, LEARNINGS.md, TESTS.md, evals/evals.json, evergreen.json, MAINTENANCE.md
- Initial version. Tier `slow`, interval 120d. Lessons L-001 to L-004 recorded at creation. First test run is logged in TESTS.md.
