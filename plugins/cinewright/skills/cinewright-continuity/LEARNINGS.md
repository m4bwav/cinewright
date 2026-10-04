# Learnings: cinewright-continuity

Procedural lessons for [SKILL.md](SKILL.md). Research findings live in [RESEARCH.md](RESEARCH.md); every change is logged in [CHANGELOG.md](CHANGELOG.md); test runs in [TESTS.md](TESTS.md); state in `evergreen.json`. Format: [MAINTENANCE.md](MAINTENANCE.md) (LEARNINGS-FORMAT in the evergreen protocol). Retired entries go to LEARNINGS-ARCHIVE.md with a reason.

Write an entry the moment a real signal happens: a user correction, the same error twice, a workaround, an environment fact, a failed test. Check existing entries first: add, update, retire or none. Trigger and Hypothesis are required.

## Active

### L-001 · 2026-10-03 · Chained clips lose identity and prop shape; restate both in every continuation
- Trigger: Field lesson 005 of the maintainer's local renders, 2026-09-06, 'Chained clips lose character identity and prop continuity, and the splice reads as a pause'
- Hypothesis: A first frame conditions composition; nothing in it tells the model who a person is or what shape a prop has
- Rule: Restate the identity string and prop constants verbatim in every continued clip; start it 'already moving, no pause' and trim the eased-in head frames
- Evidence: C-20261003-1 (references/ai-continuity.md, references/identity-strings.md), confirmed 2026-10-03
- Scope: skill
- Status: active · helpful 1 · harmful 0 · last_confirmed 2026-10-03

### L-002 · 2026-10-03 · Separate generations cut together read as the scene restarting
- Trigger: Field lesson 011 of the maintainer's local renders, 2026-09-28, 'Independent shots cut together read as the scene restarting; write the cuts inside long renders'
- Hypothesis: Every generation starts picture and sound from nothing, so each seam looks like a new start
- Rule: Prefer one generation holding several shots; put seams only at real changes of place or side, with one sound named on both sides
- Evidence: C-20261003-1 (references/ai-continuity.md), confirmed 2026-10-03
- Scope: skill
- Status: active · helpful 1 · harmful 0 · last_confirmed 2026-10-03

### L-003 · 2026-10-03 · Story directions give random facing; use one fixed frame-relative phrase
- Trigger: Field lesson 012 of the maintainer's local renders, 2026-09-28, 'Crowds face random ways; give a fixed screen direction, not toward the enemy'
- Hypothesis: The model has no map of the scene, so directions defined by the story have no meaning to it
- Rule: Write direction with the fixed screen-direction phrases in every prompt of the film; never a goal the shot cannot show
- Evidence: C-20261003-1 (references/axis-and-screen-direction.md, shared vocab screen-direction), confirmed 2026-10-03
- Scope: skill
- Status: active · helpful 1 · harmful 0 · last_confirmed 2026-10-03

### L-004 · 2026-10-03 · Negative lines lose; describe what is there with absences inside it
- Trigger: Field lesson 013 of the maintainer's local renders, 2026-09-29, 'Describe what IS in a shot; Avoid entries lose against strong associations'
- Hypothesis: Exclusion text is weak conditioning next to strong scene associations
- Rule: Describe positively and put absences inside the description; add a contrast sentence when two groups share a shot
- Evidence: C-20261003-1 (references/identity-strings.md, references/ai-continuity.md), confirmed 2026-10-03
- Scope: skill
- Status: active · helpful 1 · harmful 0 · last_confirmed 2026-10-03
