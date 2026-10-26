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



### L-002 · 2026-10-25 · A split screen is two cards per window, sizes alternating by pair (`split-screen-pairs`)
- Trigger: 2026-10-25, a local news-satire film: a live two-way split screen written as one card per line gave every half a same-size cut to itself (12 30-DEGREE errors) and needed separate listening clips; ids like 5bA failed the schema, which allows only digits then letters
- Hypothesis: on a split screen each half is its own continuous camera, so a cut inside one half is a jump cut unless it changes size
- Rule: Open. Write a split screen as windows: per window one card per half, equal duration, each half with only its own speaker's lines (it listens with closed lips through the rest); alternate the size by window (MWS, MCU) so each half's cut clears the 30-degree rule; give both halves scenes that share one number (5a, 5b) so the slate ids stay digits plus letters
- Evidence: the film's card script (PAIRS); continuity diff 16 errors to 0
- Scope: skill (no split-screen guidance yet); maybe a `split` field later
- Status: active · helpful 1 · harmful 0 · last_confirmed 2026-10-25
