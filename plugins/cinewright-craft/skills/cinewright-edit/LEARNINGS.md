# Learnings: cinewright-edit

Procedural lessons for [SKILL.md](SKILL.md). Research findings live in [RESEARCH.md](RESEARCH.md); every change is logged in [CHANGELOG.md](CHANGELOG.md); test runs in [TESTS.md](TESTS.md); state in `evergreen.json`. Format: [MAINTENANCE.md](MAINTENANCE.md) (LEARNINGS-FORMAT in the evergreen protocol). Retired entries go to LEARNINGS-ARCHIVE.md with a reason.

Write an entry the moment a real signal happens: a user correction, the same error twice, a workaround, an environment fact, a failed test. Check existing entries first: add, update, retire or none. Trigger and Hypothesis are required.

## Active

### L-001 · 2026-10-04 · A multi-shot generation is cut apart by scene detection, then trimmed per part
- Trigger: 2026-10-04, S5 exit check: the S2 render is one 14.375 s generation holding 1A, 1B and 1C, and the cut needed each part's in and out points
- Hypothesis: A model's internal cuts are hard picture changes that ffmpeg's scene score finds reliably at 0.25
- Rule: Run `select='gt(scene,0.25)',showinfo` on a multi-shot take first, treat each part as its own take, and trim inside the parts only
- Evidence: C-20261004-1 (references/cutting-around-bad-frames.md; scene cuts found at 6.000 s and 10.458 s, the cut conformed to 336 frames, 14.000 s), confirmed 2026-10-04
- Scope: skill
- Status: active · helpful 1 · harmful 0 · last_confirmed 2026-10-04

### L-002 · 2026-10-04 · Look at a strip of frames before calling an opening bad frames
- Trigger: 2026-10-04, S5 exit check: the qc rubric flagged 1A bad-opening (the lamp lens glows white from frame 1), which suggested trimming the head
- Hypothesis: Some 'bad openings' are the shot's content, not settle frames, and trimming cannot remove them
- Rule: Make a head strip (first 8 frames, then 2 s at 6 fps) and trim only if the fault ends; if it runs through the shot, send it back to qc as a re-render
- Evidence: C-20261004-1 (references/cutting-around-bad-frames.md Notes; the glow lasted the whole of 1A), confirmed 2026-10-04
- Scope: skill
- Status: active · helpful 1 · harmful 0 · last_confirmed 2026-10-04
