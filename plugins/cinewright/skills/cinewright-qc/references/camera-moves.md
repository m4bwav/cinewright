---
title: Camera moves
slug: camera-moves
summary: The camera-move tokens a shot card allows (one per card), what each does physically, and the prompt words each compiles to.
tags: [vocab, camera, movement, shots]
last_checked: 2026-10-22
sources: ["Joseph V. Mascelli, The Five C's of Cinematography, 1965", "Steven D. Katz, Film Directing Shot by Shot, 1991", "https://en.wikipedia.org/wiki/Camera_movement"]
---
<!-- copied from shared/vocab/camera-moves.md sha256:2274e31f2db5cdd7e2450fdb3caac94fa672a10d09601fa135b3b1219f3d1ffe; edit the source -->

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
- A move on a still subject starts and ends on held frames: set `camera.settle`, which compiles to "the camera holds, then ..., then holds". The holds are the edit's handles (after Mascelli, *The Five C's*).
- A move cannot be trimmed mid-move, so the card's length is the screen time it gets. Name in `beat` what the move reveals on the way; if it reveals nothing, make the card `static`.
- Continuation seams keep the "already moving" rule; `settle` is for moves that open and close a shot.
- Meanings: a push in reads as a realization, a pull back as a reveal or isolation. Tracking slower than the subject lets them pull ahead (winning); faster passes them (losing). A circle around a group unites it or puts it on show (after Katz, *Shot by Shot*).
- On a long lens, lateral moves look fast and moves toward the camera barely read.

## Pitfalls

- Pan and truck are often confused by models; "the camera turns" vs "the camera slides sideways" disambiguates.
