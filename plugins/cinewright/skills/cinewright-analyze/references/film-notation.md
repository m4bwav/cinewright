---
title: Film notation
slug: film-notation
summary: The notation file that records a video shot by shot and set by set in character heights, how to fill it, and how it maps onto shot cards and level briefs.
tags: [analysis, notation, breakdown, shots, sets]
last_checked: 2026-11-11
sources: ["https://www.scenedetect.com/docs/0.7/api.html", "https://ffmpeg.org/ffmpeg-filters.html#select_002c-aselect", "cinewright ai-docs/research/2026-11-11-room-scale-failure.md"]
---

# Film notation

## Rules

- One file per video: `NAME.notation.json`, version `0.1`, schema `scripts/schemas/film-notation.schema.json`. `AN notate` validates it and writes the readable view.
- Lengths are in **H**, one standing reference character head to feet. Each engine converts with its own character height; never store engine units or metres in the notation.
- Every set carries `confidence`: `measured` (scale run on a frame with both corners and a horizon), `estimated` (a corner off frame, or no horizon), `guess` (no measure file). A guess is never handed to a builder without saying so.
- `measured_from` names the measure file and timecode so anyone can redo the number.
- Shots come from `AN shots` (ffmpeg scene score, default 0.3, cuts closer than 0.5 s merged). In animation, white flashes, muzzle flashes and blood frames trigger false cuts: a shot under 0.6 s is checked against the frames before and after it before it counts.
- One continuous take with a crane or a pan is one shot; give it the dominant move and note the others in `notes`.
- Cast positions are on the set's floor plan: `x_H` from the left corner, `z_H` out from the back wall.
- On-screen text goes in `text_on_screen` verbatim; never carry a logo or a poster design into a rebuild, only its size and place.

## Notes

| Notation | Shot card | Level brief |
|---|---|---|
| shot size, angle, move | `camera.size`, `angle`, `move` (side A) | - |
| cast id, characters[].look, wardrobe | `cast[].identity`, `wardrobe` | spawn markers |
| action, sfx | `action`, `sound` | - |
| set width/height/depth_H | location bible notes | wall and floor sizes in units |
| features | props or location walls | primitives at x, y, w, h |

`AN rebuild --cards` clamps durations to 3-8 s and skips shots without an action.
