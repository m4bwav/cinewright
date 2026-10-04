---
title: Eyelines
slug: eyelines
summary: Which way each character must look in singles and over-the-shoulder shots so two separately generated shots read as people looking at each other.
tags: [continuity, eyeline, dialogue, coverage]
last_checked: 2026-10-03
sources: ["Daniel Arijon, Grammar of the Film Language, 1976", "Pat P. Miller, Script Supervising and Film Continuity, 3rd ed., 1999"]
---

# Eyelines

## Rules

- From side A, a character placed frame-left looks frame-right at a partner placed frame-right, and the partner looks frame-left. Keep that in every single, even when the partner is off screen.
- Record `looks_at` (who or what) and `eyeline` (frame-left, frame-right, up, down) on each cast entry. The diff derives the correct side from the scene's positions.
- Eyeline height matches the target: a seated child looks up at a standing adult, and the adult looks down, in every shot of the exchange.
- Looking into the lens is for a POV or a deliberate address only.
- Write the eyeline into the prompt as a fixed phrase ("looking toward frame right"). Without it, models center the gaze or look at the lens.

## Pitfalls

- An off-screen partner gives the model nothing to look at. Name the direction, and keep the frame position the shot needs (a single of the frame-left character leaves looking room on frame right).

## Verify

- `continuity diff` code EYELINE: the side is wrong for the camera side, or a lens look outside a POV.
