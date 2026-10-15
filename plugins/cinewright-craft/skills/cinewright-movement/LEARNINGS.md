# Learnings: cinewright-movement

Procedural lessons for [SKILL.md](SKILL.md). Research findings live in [RESEARCH.md](RESEARCH.md); every change is logged in [CHANGELOG.md](CHANGELOG.md); test runs in [TESTS.md](TESTS.md); state in `evergreen.json`. Format: [MAINTENANCE.md](MAINTENANCE.md) (LEARNINGS-FORMAT in the evergreen protocol). Retired entries go to LEARNINGS-ARCHIVE.md with a reason.

Write an entry the moment a real signal happens: a user correction, the same error twice, a workaround, an environment fact, a failed test. Check existing entries first: add, update, retire or none. Trigger and Hypothesis are required.

## Active

### L-001 · 2026-10-04 · Draw an animal-drawn vehicle from the side; from behind, the order comes out wrong
- Trigger: Field lesson 020 of the maintainer's local renders, 2026-09-30, 'Draw a horse team and wagon from the side; from behind, the image model puts the horses behind the wagon'
- Hypothesis: From behind, 'in front of the vehicle' and 'nearest the camera' conflict in the model's layout; a side view has no such ambiguity
- Rule: Make guide stills and last beats side views with the direction in frame words, and check every still for the order before using it
- Evidence: C-20261004-1 (references/hard-subjects.md), confirmed 2026-10-04
- Scope: skill
- Status: active · helpful 1 · harmful 0 · last_confirmed 2026-10-04

### L-002 · 2026-10-04 · Few animals, large in frame; a far column of animals cannot be drawn
- Trigger: Field lesson 021 of the maintainer's local renders, 2026-09-30, 'Few animals, large in frame, fix the legs; a far column of animals cannot be drawn'
- Hypothesis: Leg detail scales with the animal's size in pixels; a far animal gets about one token of the model's grid
- Rule: Frame 1-5 animals at a third of the frame height or more, side-on, each named differently, the mass as one background line; spend compute on resolution, not steps
- Evidence: C-20261004-1 (references/hard-subjects.md, shared/lib/cine.py HARD-SUBJECT check), confirmed 2026-10-04
- Scope: skill
- Status: active · helpful 1 · harmful 0 · last_confirmed 2026-10-04

### L-003 · 2026-10-15 · An eval allow list written for one script silently blocks its companions
- Trigger: action-2 (fight plan) failed 2 of 2 on Sonnet: the skill wrote the plan and ran `cine_fight.py check` five times, every call refused, because the harness allowed `*cine.py*` only. The first fix then passed on `cine_fight.py check --help`.
- Hypothesis: allow-list patterns and evidence patterns name the file that existed when they were written; a new script needs both widened, and a pattern that matches the command name alone also matches its help
- Rule: when a skill ships a new script, add it to the harness allow list in the same change, and make the evidence pattern require the real argument (here a `.json` path), not the command name
- Evidence: evals/run_evals.py BASH_ALLOW (cine_*.py), evals.json action-2 input_match, T-20261015-1
- Scope: skill
- Status: active · helpful 1 · harmful 0 · last_confirmed 2026-10-15
