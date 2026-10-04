---
title: Axis and screen direction (180-degree rule)
slug: axis-and-screen-direction
summary: The scene axis, camera side A, how positions and travel are recorded from side A, legal ways to cross the line, and why direction must be a fixed phrase.
tags: [continuity, axis, 180-degree-rule, screen-direction]
last_checked: 2026-10-03
sources: ["Daniel Arijon, Grammar of the Film Language, 1976", "Pat P. Miller, Script Supervising and Film Continuity, 3rd ed., 1999", "https://en.wikipedia.org/wiki/180-degree_rule"]
---

# Axis and screen direction

## Rules

- Every scene has one axis (line of action): between two characters who face each other, or along a line of travel. Record it in `bibles/scenes.json` as `axis.line`.
- All cameras stay on one side of it, side A. Characters then keep their side of the frame and their direction of travel in every shot.
- Record `positions` and `travel` as seen from side A. A card on side B flips every left and right; the diff computes the flip.
- Write direction with the fixed phrases in the screen-direction entry, the same words in every shot of the film. Story directions ("toward the enemy", "inland", "east") give each clip a random direction.
- Cross the line only on screen: the camera moves across in the shot, a character crosses the line in frame, or a neutral shot (straight down the axis) sits between. Set `crosses_axis` and `cross_reason` on that card; every later card of the scene is then side B.
- A chase or journey keeps one travel direction for the whole film unless the story turns it on screen.

## Numbers

- Neutral shot: camera within about 10 degrees of the axis line (azimuth near 0 or 180), subject moving toward or away from camera.

## Pitfalls

- Video models have no map of the scene. Without a fixed frame-relative phrase in every prompt, crowds and travellers face random ways.
- Never write a prop or goal whose purpose the shot cannot show; the model invents a direction for it.

## Verify

- `continuity diff` codes AXIS (side B without a reason), DIRECTION (travel flipped), POSITION (two people swapped sides).

## Notes

- 2026-10-03: the fixed-phrase rule generalises field lesson 012 from the maintainer's local renders (see LEARNINGS).
