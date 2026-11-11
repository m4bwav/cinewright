---
title: Room scale from a frame
slug: room-scale
summary: Measure a set's width, height, floor depth and camera height in character heights from one frame, with the measure-file fields and the traps that made a rebuilt room 2.5 times too wide.
tags: [analysis, scale, sets, metrology, levels]
last_checked: 2026-11-11
sources: ["A. Criminisi, I. Reid, A. Zisserman, Single View Metrology, IJCV 40(2), 2000", "https://github.com/DepthAnything/Depth-Anything-3", "cinewright ai-docs/research/2026-11-11-room-scale-failure.md"]
---

# Room scale from a frame

## Rules

- The unit is a standing character. Measure it in the same frame as the walls; it is the only ruler a film always has.
- Pick a frame where the character's feet touch the floor close to the back wall and the camera is still. Read points off `AN frame --grid 50` at full resolution, never off contact-sheet thumbnails.
- Measure file fields: `width` (frame px), `characters[]` (`head_y`, `feet_y`), `wall` (`left_x`, `right_x`, `floor_y` at the back wall's base, `ceiling_y`, `left_open` or `right_open` when a corner is off frame), `horizon_y`, `floor_front_y`, optional `pan_px` and `hfov_deg`.
- Horizon: where two receding edges of a side wall (its ceiling and floor lines) meet, or let `scale` fit it from two or more characters standing at clearly different depths. With no horizon there is no depth, and the wall sizes are an upper bound.
- Depth depends on the lens: `scale` assumes 45 degrees across unless `hfov_deg` is set. Give the range for 45-60 degrees when the lens is unknown.
- A wall wider than the frame: measure where the corners show, or add the camera's travel as `pan_px`. `AN pan` works on textured live action; on flat cel animation moving characters swamp it, so read the pan off two frames with a shared landmark instead.
- Side-on stage films (most 2D animation) have a shallow floor and a low camera (about 1-1.3 H). A game camera that looks down from high makes the same floor read deeper: keep the measured depth and move the game camera, not the walls.
- Depth models (Depth Anything 3, MoGe-2, Depth Pro) are untested on cartoons; use them only on live action, as a cross-check.

## Numbers

Fan film room 1 (0:26): back wall at least 6.2 H wide, 2.63 H high, floor 2.7-3.7 H deep, camera 1.25 H. The level built by eye was about 16 H wide.
