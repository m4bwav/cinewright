---
title: Day for night
slug: day-for-night
summary: Make night in the grade from a normally exposed render lit from the night's source direction: lower exposure about 2 stops, cool the mids, darken the sky most, keep practical lights warm and bright.
tags: [finish, grade, night, day-for-night]
last_checked: 2026-10-04
sources: ["Alexis Van Hurkman, Color Correction Handbook, 2nd ed., 2014", "Blain Brown, Cinematography: Theory and Practice, 3rd ed., 2016"]
---

# Day for night

## Rules

- Ask the model for a normal exposure with the night's light direction and hard, low sun or moon light (cinewright-camera, entry exposure). A model asked for "dark" gives noise; detail darkened in the grade survives.
- Avoid a visible sky in the render when possible; if it shows, it is the brightest thing and must go darkest (a window or gradient over the top of the frame).
- Grade, in order on top of the corrected shot: lower exposure about 2 stops; pull saturation down 30-50% (night vision sees less color); shift mids and shadows cool (blue, slightly cyan); keep blacks neutral or barely blue, never purple; keep highlights on faces from the motivated source.
- Practical lights (lamps, fires, windows) stay warm and bright: key them with a qualifier or a window and protect them from the darkening.
- Shadows from the sun stay; that is the giveaway of real day-for-night, and audiences accept it when the direction matches the scene's moon.
- Do it per scene as part of match, then the film's look on top (entry grade-order).

## Numbers

- Exposure down about 1.5-2.5 stops; saturation down 30-50%; color temperature shift to the cool side by roughly the gap between tungsten and daylight (3200 K vs 5600 K, shared vocab lighting-terms in cinewright-camera).

## Pitfalls

- Making it blue everywhere: skin turns grey-blue and dead; keep a warm source on faces.
- Darkening an 8-bit render by 2 stops then brightening a part back: banding and noise. Darken once with a curve, not in steps.

## Verify

- A still before and after side by side in `finish/`; the sky is darker than the faces; practical lights still read as on.
