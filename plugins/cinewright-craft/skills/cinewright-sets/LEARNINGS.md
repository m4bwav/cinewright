# Learnings: cinewright-sets

Procedural lessons for [SKILL.md](SKILL.md). Research findings live in [RESEARCH.md](RESEARCH.md); every change is logged in [CHANGELOG.md](CHANGELOG.md); test runs in [TESTS.md](TESTS.md); state in `evergreen.json`. Format: [MAINTENANCE.md](MAINTENANCE.md) (LEARNINGS-FORMAT in the evergreen protocol). Retired entries go to LEARNINGS-ARCHIVE.md with a reason.

Write an entry the moment a real signal happens: a user correction, the same error twice, a workaround, an environment fact, a failed test. Check existing entries first: add, update, retire or none. Trigger and Hypothesis are required.

## Active

### L-003 · 2026-10-15 · `light-line-draws-the-windows`: name a wall's light source only in that wall's plates
- Trigger: set field test, 2026-10-15: a shared light line said firelight came "through the tall windows"; all six plates of the solid east and south walls came back with fire-lit windows cut into them
- Hypothesis: every noun in the prompt is drawn somewhere in the frame; the window noun wins over a solid wall's edges in the control picture
- Rule: the shared light line names the glow and its direction only; the window and the fire beyond go in the plates of the window wall
- Evidence: C-20261015-1; with the windows named per view, the same cameras and seeds gave 0 of 6 wrong walls
- Scope: skill
- Status: active · helpful 1 · harmful 0 · last_confirmed 2026-10-15

### L-004 · 2026-10-15 · `cameras-from-marks`: place card cameras from the marks, not from the plate list
- Trigger: set field test, 2026-10-15: coverage drawn with six fixed plate cameras failed the marks check four times once the duel drifted 3 m (the left fighter came out frame-right, one camera on the line, an overhead with the order flipped)
- Hypothesis: a plate fixes a wall, not a camera; the pair moves and the camera must follow it
- Rule: compute each card's camera from the pair's marks (side-on on side A, or over one shoulder); the plate only supplies the wall behind
- Evidence: C-20261015-1, references/blocking-marks.md; the same 13 beats with computed cameras: 0 errors
- Scope: skill
- Status: active · helpful 1 · harmful 0 · last_confirmed 2026-10-15

### L-001 · 2026-10-07 · `whole-room-string-pulls-to-hero-wall`: describe each wall on its own
- Trigger: set field test, 2026-10-07: a reverse to the fireplace wall and an east-door shot, both written as framing words after the room's full description, came back as the establishing desk-and-windows view (2 of 2)
- Hypothesis: the image model composes from the nouns in the prompt; framing words like "reverse shot looking north" carry little weight against named hero objects
- Rule: keep one-wall features out of the location description; give each wall its own string in `walls` and point the card at it with `camera.faces`; say what is not in view on a reverse
- Evidence: C-20261007-1 (references/wall-strings.md, compile and WALL check); re-render with the north wall's own string, same seed: fireplace, portrait over the mantel and sofas, no desk or windows (confirmed 2026-10-07)
- Scope: skill
- Status: active · helpful 1 · harmful 0 · last_confirmed 2026-10-07

### L-002 · 2026-10-07 · `stop-the-batch-when-the-words-change`: a running render keeps the old prompts
- Trigger: set field test, 2026-10-07: the batch script had loaded the shot list before the wall strings were written, so its later reverses would have rendered with the old words
- Hypothesis: a batch reads its prompts once at start
- Rule: after changing a set's words mid-batch, stop the batch, move the plates made with the old words to `_rejected/`, and restart; skip plates already made with the right words
- Evidence: field test log 2026-10-07
- Scope: skill
- Status: active · helpful 1 · harmful 0 · last_confirmed 2026-10-07
