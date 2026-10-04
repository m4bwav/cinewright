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
