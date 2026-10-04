---
title: Blocking
slug: blocking
summary: Where each person stands and moves in a scene, written from camera side A in the scene bible before any card, with staging in depth and a reason for every move.
tags: [shots, blocking, staging, positions, depth, proxemics]
last_checked: 2026-10-04
sources: ["Judith Weston, Directing Actors, 1996", "Steven D. Katz, Film Directing Shot by Shot, 1991", "Edward T. Hall, The Hidden Dimension, 1966"]
---

# Blocking

## Rules

- Block the scene before writing cards: for each character, the start position and any travel as seen from side A, in `bibles/scenes.json` (`axis.positions`, `axis.travel`). Cards copy these; the continuity diff checks them.
- Positions are three words only: frame-left, center, frame-right. Two people in one scene never share one position.
- One move per person per shot. A move across the frame is a travel direction (left-to-right) and stays the same for the whole scene.
- Every move has a reason the shot can show: "crosses to the window and looks out", not "walks across the room". A move with no reason reads as drift.
- Stage in depth: a framing element in the foreground, the subject in the midground, the place behind. Write each layer in the card's action or the location string.
- To move the axis, let a character cross it on screen in one shot; the next cards use the new side. Record it with `crosses_axis` and a `cross_reason`.
- Re-block only on a new master. Inside a run of singles, nobody changes sides.

## Numbers

- Distance between two people (Hall 1966): intimate under 0.45 m, personal 0.45-1.2 m, social 1.2-3.6 m, public over 3.6 m. Write it in the prompt as a picture ("an arm's length apart"), not a number.
- Two people talking, standing: personal distance unless the scene is about closeness or threat.

## Vocabulary

- mark: where a person stops. cross: a move from one mark to another. staging: where people are in the frame and in depth. cheat: turning a person toward camera more than real life would.

## Pitfalls

- A lone subject is drawn centered unless the card says otherwise; write the position words every time.
- A scene with people "around a table" has no left and right. Pick the two people the scene is between; they define the axis.
- Story directions ("toward the door", "toward the enemy") mean nothing to the model; use the travel words.

## Verify

- Every on-screen person has `position` on the card and a position in the scene's axis block.
- `continuity diff` shows no POSITION or DIRECTION errors.
