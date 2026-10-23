# Learnings: cinewright-sets

Procedural lessons for [SKILL.md](SKILL.md). Research findings live in [RESEARCH.md](RESEARCH.md); every change is logged in [CHANGELOG.md](CHANGELOG.md); test runs in [TESTS.md](TESTS.md); state in `evergreen.json`. Format: [MAINTENANCE.md](MAINTENANCE.md) (LEARNINGS-FORMAT in the evergreen protocol). Retired entries go to LEARNINGS-ARCHIVE.md with a reason.

Write an entry the moment a real signal happens: a user correction, the same error twice, a workaround, an environment fact, a failed test. Check existing entries first: add, update, retire or none. Trigger and Hypothesis are required.

## Active

### L-005 · 2026-10-15 · `card-camera-control-holds-the-room`: a grid reference alone lost the room; Canny from the card's camera kept it
- Trigger: set field test, 2026-10-15: the plan passed a one-image grid of six plates as the only set reference in every card; the first card's take drew a generic hall with a stair the plan does not have and sconces for niches
- Hypothesis: a grid of views gives the materials but not which wall stands behind this camera; control rendered from the blockout at the card's own camera does
- Rule: per card, the grid as the set ref plus Canny control from the blockout at the card's camera (strength 0.6, end 0.4 on the local video model), the camera taken from the marks; the faced wall's single plate also kept the room, by copying itself, so use it as a ref only when the card's camera is near the plate's
- Evidence: one card three ways, same prompt and seed: grid alone lost the room, plate and grid plus control kept it (five set claims judged twice, then checked by eye); about 30 % more render time with control; one seed each
- Scope: skill (blockout-control, master-plates)
- Status: active · helpful 1 · harmful 0 · last_confirmed 2026-10-15

### L-006 · 2026-10-15 · `scene-sun-names-no-wall`: the scene's sun line is compiled into every card
- Trigger: set field test, 2026-10-15: the scene bible's `sun` said the firelight came "through the tall west windows", and the compiled prompt of a card facing the solid east wall carried it (L-003's fault again, by another field)
- Hypothesis: compile writes the scene's `sun` into every card of the scene whatever `camera.faces` says, as it does the location `description`
- Rule: the scene's `sun` gives the source's direction only ("firelight from the west"); windows, fires and other wall features go in their wall's string. Also keep the location's `refs` to the one grid: compile sends every location ref with every card
- Evidence: compiled card before and after; seven location refs became one
- Scope: skill (wall-strings, set-light)
- Status: active · helpful 1 · harmful 0 · last_confirmed 2026-10-15

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

### L-003 · 2026-10-22 · A Blender pass question does not reach this skill unless the description names blockout passes
- Trigger: three runs of a Mist-pass question for H3 depth control loaded no sets skill (T-20261022-1).
- Hypothesis: the description named sets, plates and light, nothing about blockouts or passes, so the model answered the Blender question itself.
- Rule: keep "3D blockouts rendered as control passes (Blender depth, Mist, masks)" in the description; plain Blender scripting stays polywright-blender's.
- Evidence: C-20261022-2; 0/3 then 3/3, triggers and decoys 12/12.
- Scope: skill
- Status: active · helpful 1 · harmful 0 · last_confirmed 2026-10-22
