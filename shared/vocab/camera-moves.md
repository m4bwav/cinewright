---
title: Camera moves
slug: camera-moves
summary: The camera-move tokens a shot card allows (one per card), what each does physically, and the prompt words each compiles to.
tags: [vocab, camera, movement, shots]
last_checked: 2026-10-03
sources: ["Joseph V. Mascelli, The Five C's of Cinematography, 1965", "Steven D. Katz, Film Directing Shot by Shot, 1991", "https://en.wikipedia.org/wiki/Camera_movement"]
---

# Camera moves

## Vocabulary

| Token | Physical move | Prompt words |
|---|---|---|
| `static` | locked off, no move | static camera |
| `pan-left` / `pan-right` | camera turns on its axis | slow pan left / slow pan right |
| `tilt-up` / `tilt-down` | camera pivots vertically | slow tilt up / slow tilt down |
| `dolly-in` / `dolly-out` | camera travels toward or away from subject | slow dolly in / slow dolly out |
| `truck-left` / `truck-right` | camera travels sideways, parallel to subject | camera trucks left / camera trucks right |
| `track` | camera travels with a moving subject at the same distance | tracking shot following |
| `crane-up` / `crane-down` | camera rises or lowers | crane up / crane down |
| `handheld` | operator-held, small natural shake | handheld camera |
| `zoom-in` / `zoom-out` | focal length changes, camera stays put | slow zoom in / slow zoom out |

## Rules

- One move per card. A shot that needs two moves is two cards, or one move that motivates the next card.
- State speed in the prompt: "slow" is the default; video models over-accelerate moves left unqualified.
- A move never crosses the scene axis unless the card sets `crosses_axis` with a reason (see the axis entry).

## Pitfalls

- Pan and truck are often confused by models; "the camera turns" vs "the camera slides sideways" disambiguates.
