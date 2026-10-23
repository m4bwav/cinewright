# Learnings: cinewright-shots

Procedural lessons for [SKILL.md](SKILL.md). Research findings live in [RESEARCH.md](RESEARCH.md); every change is logged in [CHANGELOG.md](CHANGELOG.md); test runs in [TESTS.md](TESTS.md); state in `evergreen.json`. Format: [MAINTENANCE.md](MAINTENANCE.md) (LEARNINGS-FORMAT in the evergreen protocol). Retired entries go to LEARNINGS-ARCHIVE.md with a reason.

Write an entry the moment a real signal happens: a user correction, the same error twice, a workaround, an environment fact, a failed test. Check existing entries first: add, update, retire or none. Trigger and Hypothesis are required.

## Active

### L-001 · 2026-10-22 · `placement-pulls-to-centre`: placement words land near the centre, not on the third
- Trigger: books track 4 measured the main face on both sides of 219 planned cuts in local multi-shot takes (a face detector outside this runtime, OpenCV YuNet) against the cards' `position`
- Hypothesis: the video model pulls people toward the centre; "on the left of the frame" names a side, not a third
- Rule: when a side must read (a two-shot, a shot and its reverse, an `attention` cell), say the third and what fills the rest; judge placement by order (left of centre, centre, right of centre), not by thirds
- Evidence: single-person cards: frame-left faces at a median 0.37 of the width (53 faces, 18 on the left third), centre 0.49 (36), frame-right 0.60 (41, 6 on the right third); thirds agreement 32 of 100, the order always right
- Scope: skill (references/framing.md) and the compile words (POSITION_WORDS, unchanged)
- Status: active · helpful 0 · harmful 0 · last_confirmed 2026-10-22


