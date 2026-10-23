---
title: Eyelines
slug: eyelines
summary: Which way each character must look in singles and over-the-shoulder shots so two separately generated shots read as people looking at each other.
tags: [continuity, eyeline, dialogue, coverage]
last_checked: 2026-10-22
sources: ["Daniel Arijon, Grammar of the Film Language, 1976", "Pat P. Miller, Script Supervising and Film Continuity, 3rd ed., 1999", "Joseph V. Mascelli, The Five C's of Cinematography, 1965"]
---

# Eyelines

## Rules

- From side A, a character placed frame-left looks frame-right at a partner placed frame-right, and the partner looks frame-left. Keep that in every single, even when the partner is off screen.
- Record `looks_at` (who or what) and `eyeline` (frame-left, frame-right, up, down) on each cast entry. The diff derives the correct side from the scene's positions.
- Eyeline height matches the target: a seated child looks up at a standing adult, and the adult looks down, in every shot of the exchange.
- Looking into the lens is for a POV or a deliberate address only.
- Write the eyeline into the prompt as a fixed phrase ("looking toward frame right"). Without it, models center the gaze or look at the lens.
- A watcher following something that moves turns their head the opposite way on screen to its travel, as if it passed behind the camera. Record the turn with `eyeline` (start) and `eyeline_end` (after Mascelli, *The Five C's*).
- Two people on a phone or video call face opposite ways in their singles.
- Someone seen earlier who appears in a cut-away keeps the look that matches where they stood.

## Pitfalls

- An off-screen partner gives the model nothing to look at. Name the direction, and keep the frame position the shot needs (a single of the frame-left character leaves looking room on frame right).

## Verify

- `continuity diff` code EYELINE: the side is wrong for the camera side, or a lens look outside a POV.
- `continuity diff` LOOK-TRACK (warning): a head turn the same way as the watched person's travel in the scene bible.
