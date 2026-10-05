# Learnings: cinewright-shots

Procedural lessons for [SKILL.md](SKILL.md). Research findings live in [RESEARCH.md](RESEARCH.md); every change is logged in [CHANGELOG.md](CHANGELOG.md); test runs in [TESTS.md](TESTS.md); state in `evergreen.json`. Format: [MAINTENANCE.md](MAINTENANCE.md) (LEARNINGS-FORMAT in the evergreen protocol). Retired entries go to LEARNINGS-ARCHIVE.md with a reason.

Write an entry the moment a real signal happens: a user correction, the same error twice, a workaround, an environment fact, a failed test. Check existing entries first: add, update, retire or none. Trigger and Hypothesis are required.

## Active

None yet.

### L-001 · 2026-10-04 · Match the coverage question in the description
- Trigger: 2026-10-04, S6 matrix T-20261004-2: trigger-2 (what coverage do I need for a two-person dialogue scene) invoked the skill Haiku 0 of 3, answered in one turn; trigger-1 (break this scene into shots) went to the cinewright router Haiku 2 of 3
- Hypothesis: "planning coverage" is a task name, not the question users ask
- Rule: The Use clause says "asking what coverage a scene needs"
- Evidence: C-20261004-2 (description); rerun pending
- Scope: skill
- Status: active · helpful 0 · harmful 0 · last_confirmed 2026-10-04
