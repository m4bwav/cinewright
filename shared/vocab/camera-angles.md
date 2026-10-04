---
title: Camera angles
slug: camera-angles
summary: Vertical angle tokens (eye-level to dutch), the azimuth number used for the 30-degree check, and framing tokens (single, OTS, insert).
tags: [vocab, camera, angle, framing]
last_checked: 2026-10-03
sources: ["Daniel Arijon, Grammar of the Film Language, 1976", "https://en.wikipedia.org/wiki/Camera_angle"]
---

# Camera angles

## Vocabulary

Vertical angle (`camera.angle`): `eye-level`, `high` (looks down), `low` (looks up), `overhead` (straight down), `ground` (lens near the floor), `dutch` (horizon tilted).

Azimuth (`camera.azimuth_deg`): horizontal position of the camera around the subject, measured on the scene's camera side. 0 and 180 lie on the axis line; 90 is square to it. Any value from 0 to 180 is on that side.

Framing (`camera.framing`): `single`, `two-shot`, `ots` (over the shoulder), `insert` (object, no cast), `pov` (what a character sees), `group`.

## Numbers

- 30 degrees of azimuth is the smallest change that reads as a new angle between two shots of the same subject.
- Reverse shots in a two-person dialogue sit near 45 and 135 on the same side.

## Rules

- Write the vertical angle in every compiled prompt; "eye level" is the default and still stated.
- Dutch angle only when the scene bible's style allows it; it reads as an error otherwise.
