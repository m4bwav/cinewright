---
title: Camera moves
slug: camera-moves
summary: The camera-move tokens a shot card allows (one per card), what each does physically, and the prompt words each compiles to.
tags: [vocab, camera, movement, shots]
last_checked: 2026-10-22
sources: ["Joseph V. Mascelli, The Five C's of Cinematography, 1965", "Steven D. Katz, Film Directing Shot by Shot, 1991", "Bruce Block, The Visual Story, 2nd ed., 2008", "https://en.wikipedia.org/wiki/Camera_movement"]
---
<!-- copied from shared/vocab/camera-moves.md sha256:7d9e6c191de061041409b61c9d24e5a4bb3a74e5d58795a39c54013a047718ed; edit the source -->

# Camera moves

## Vocabulary

| Token | Physical move | Prompt words |
|---|---|---|
| `static` | locked off, no move | static camera |
| `pan-left` / `pan-right` | camera turns on its axis | slow pan left / slow pan right |
| `tilt-up` / `tilt-down` | camera pivots vertically | slow tilt up / slow tilt down |
| `dolly-in` / `dolly-out` | camera travels toward or away from subject | slow dolly in / slow dolly out |
| `push-in` | same as `dolly-in`, the word for a slow move to a realization | slow push in |
| `arc-left` / `arc-right` | camera circles the subject at one distance | the camera arcs slowly left around the subject, the background sliding behind |
| `truck-left` / `truck-right` | camera travels sideways, parallel to subject | camera trucks left / camera trucks right |
| `track` | camera travels with a moving subject at the same distance | tracking shot following |
| `crane-up` / `crane-down` | camera rises or lowers | crane up / crane down |
| `handheld` | operator-held, small natural shake | handheld camera |
| `zoom-in` / `zoom-out` | focal length changes, camera stays put | slow zoom in / slow zoom out |
| `dolly-zoom` | camera travels in while zooming out (rare, one per film) | dolly zoom, the background stretching away while the subject keeps the same size |

## Rules

- One move per card. A shot that needs two moves is two cards, or one move that motivates the next card.
- State speed in the prompt: "slow" is the default; video models over-accelerate moves left unqualified.
- A move never crosses the scene axis unless the card sets `crosses_axis` with a reason (see the axis entry).
- A move on a still subject starts and ends on held frames: set `camera.settle`, which compiles to "the camera holds, then ..., then holds". The holds are the edit's handles (after Mascelli, *The Five C's*).
- A move cannot be trimmed mid-move, so the card's length is the screen time it gets. Name in `beat` what the move reveals on the way; if it reveals nothing, make the card `static`.
- Continuation seams keep the "already moving" rule; `settle` is for moves that open and close a shot.
- Meanings: a push in reads as a realization, a pull back as a reveal or isolation. Tracking slower than the subject lets them pull ahead (winning); faster passes them (losing). A circle around a group unites it or puts it on show (after Katz, *Shot by Shot*).
- On a long lens, lateral moves look fast and moves toward the camera barely read.
- Pan, tilt and zoom are 2D moves: calmer, and they keep space flat. Dolly, track, crane and arc are 3D moves: the near and far planes slide apart, so they add depth and intensity. Handheld adds the most (after Block, *The Visual Story*). Dolly against zoom, arcs and the punch-in: the camera entry move-grammar.
- Who drives (book rules, unverified): the actor's start and stop set the camera's; a camera that stops while the walker goes on, or holds while someone leaves after a parting, is a statement the `beat` names (MS3 2.3, 8.9). Two people moving: lock to one body, not their middle (MS1 1.3). A pacing speaker: fixed distance and height, stop when he stops (MS2 7.10).
- Change height, angle or distance only when the movers stop: a wall hit or a fall gets the camera's change, so the stop reads as abrupt (MS1 1.3). A camera can take a blow: it eases back ahead of a lunging attacker, then halts and jolts sideways with the punch (MS1 1.2). Book rules, unverified.
- During a move one eye stays pinned in frame; compile can add "her eyes stay at the same place in frame" (MS1 5.1). Searching: rooted camera, pan and tilt only; indecision: tilt only (MS1 4.8; MS3 5.6). Book rules, unverified.
- Hide a fast move or zoom inside a body move, a background crossing or a following pan; hold then one rush beats a constant drift (MS2 10.1; MS3 11.2, 11.3; Bowen ch. 6). Book rules, unverified. Verify: camera stop within 0.5 s of the actor's; pinned eye drift under 5 % of frame width.

## Pitfalls

- Pan and truck are often confused by models; "the camera turns" vs "the camera slides sideways" disambiguates.
