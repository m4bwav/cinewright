---
title: Blocking
slug: blocking
summary: Where each person stands and moves in a scene, written from camera side A in the scene bible before any card, with staging in depth and a reason for every move.
tags: [shots, blocking, staging, positions, depth, proxemics]
last_checked: 2026-10-22
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
- A move in the shot changes the block: set `position_end` on that cast entry. Later cards start from it, and the diff checks them against it. Anything may change during a shot, nothing between shots (after Mascelli, *The Five C's*).
- When the background changes between cards of a moving subject, the subject leaves card A and enters card B: set `exits` and `enters`. Leaving on the right means entering on the left. Leaving close past the camera means entering close past it.
- A card that cuts into a close shot has the person move into it (sits into frame, steps into the CU), so the edit can cut on the move.
- Three or more people: entry group-staging.
- Talking people mostly look at a task, an object or ahead; write the glance beats and one held look at the turn. Two people facing and staring for the whole card is the default failure. (Kenworthy MS2 9.3, 6.8) Book rule, unverified.
- Give each speaker a task with a named object; an object both look at and one touches ties the pair. (MS2 6.9, 9.11) Book rule, unverified.
- When power changes hands, the two cross and end on each other's sides; set `position_end` for both. (MS2 3.3) Book rule, unverified.
- At a shock, one person stops while the others go on and turn back. (MS2 8.2; MS3 8.9) Book rule, unverified.
- Secret or uneasy talk on a threshold, backlit, nobody crossing; a barrier between the two that one breaks at the turn. (MS2 3.4, 1.5) Book rule, unverified.
- Groups of five or more are staggered in depth so every face reads. (Bowen ch. 2) Book rule, unverified.
- Circling: the dominant one walks side-on around the other, who shuffles sideways to keep facing him and never spins on the spot (MS1 11.1). Moving arguments cross paths in half-circles with several changes of direction, never straight back-and-forth (MS1 11.8). A walking argument's leader looks back over the shoulder on the camera side, so the face reads (MS1 11.7). Book rules, unverified.

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
- `continuity diff` shows no EXIT-ENTRY errors and no MIDDLE-SWAP warnings.
