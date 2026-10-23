---
title: Camera angles
slug: camera-angles
summary: Vertical angle tokens (eye-level to dutch) with what each reads as and where its horizon sits, camera height, dutch pairs, the azimuth number for the 30-degree check, and framing tokens.
tags: [vocab, camera, angle, framing, horizon]
last_checked: 2026-10-22
sources: ["Daniel Arijon, Grammar of the Film Language, 1976", "Marcos Mateu-Mestre, Framed Ink, 2010", "Joseph V. Mascelli, The Five C's of Cinematography, 1965", "https://en.wikipedia.org/wiki/Camera_angle"]
---

# Camera angles

## Vocabulary

Vertical angle (`camera.angle`), with what it reads as and the horizon it puts in frame (`camera.horizon`):

| Token | Camera | Reads as | Horizon |
|---|---|---|---|
| `eye-level` | at the subject's eye height | neutral, a peer | through the eyes of everyone standing |
| `high` | above, looks down | small, trapped, watched | `upper-third` or `above-frame` |
| `low` | below the eyes, looks up | towering, in control, a threat | `lower-third` or `below-frame` |
| `ground` | lens near the floor | huge, energetic; feet must touch the ground | near the bottom edge |
| `overhead` | straight down | a map: strategy, isolation | `above-frame` |
| `dutch` | horizon tilted (`camera.dutch`: `left` or `right`) | unstable, panic | tilted |

Azimuth (`camera.azimuth_deg`): horizontal position of the camera around the subject, measured on the scene's camera side. 0 and 180 lie on the axis line; 90 is square to it. Any value from 0 to 180 is on that side.

Framing (`camera.framing`): `single`, `two-shot`, `ots` (over the shoulder), `insert` (object, no cast), `pov` (what a character sees), `group`.

## Numbers

- 30 degrees of azimuth is the smallest change that reads as a new angle between two shots of the same subject.
- Reverse shots in a two-person dialogue sit near 45 and 135 on the same side.

## Rules

- Write the vertical angle in every compiled prompt; "eye level" is the default and still stated.
- Give the camera height and the horizon together: the horizon words pin the angle, and models put it mid-frame by default. Set `camera.horizon` outdoors; leave it unset indoors, since every noun in a prompt tends to get drawn and a horizon needs an outside (after Mateu-Mestre, *Framed Ink*).
- `eye-level` is the subject's eye level: seated people get a seated-height camera. A POV shot takes the looker's height, cheated toward it, so an adult looking at a child is slightly high (after Mascelli, *The Five C's*).
- A person whose eyes sit below the line the other people's eyes are on reads as dominated. Use it for a power shift inside a two-shot (after *Framed Ink*).
- Dutch angle only when the scene bible's style allows it; it reads as an error otherwise. Tilt enough to look meant, open the scene on level shots, and tilt opposing subjects in opposite directions (`dutch: left` then `right`).

## Verify

- `continuity diff`: HORIZON warns when a low angle has a high horizon or a high angle a low one; DUTCH warns when two opposing subjects tilt the same way.
