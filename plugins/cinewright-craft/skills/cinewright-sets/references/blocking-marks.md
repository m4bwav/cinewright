---
title: Blocking marks
slug: blocking-marks
summary: Mark each person per beat in metres with a facing bearing, place every card's camera from the marks, and compute screen side, axis side, facing and the wall behind instead of typing them.
tags: [sets, blocking, marks, continuity, axis, camera, plan]
last_checked: 2026-10-15
sources: ["Script supervisor continuity practice: start and end positions, screen direction and eyelines per take (secondary sources, 2026-10-15)", "Lino, Christie et al., Director's Lens, ACM MM 2011", "FilmAgent, named standing points per set (paper and code, 2024)", "PersonaShot, arXiv 2608.16717, 2026-08; MuSS, arXiv 2604.23789, 2026-08", "Set field test, 2026-10-15: a rapier duel from a novel, one room, 13 beats"]
---

# Blocking marks

## Rules

- Video models do not keep where people stand across separate generations: the best scored model reached 0.78 of 1 on cross-shot layout, most scored about 0.6 (PersonaShot). Only explicit layout holds it. Keep the record and check the cards against it.
- Put the plan in metres: x east, y north, bearings clockwise from north; walls as polylines keyed like the location's `walls`. Mark each person per beat (a phrase of a fight, a line of dialogue): position, facing bearing, posture. Mark dropped props too: a sword that skids away must lie there in every later shot.
- Pick camera side A as a point on the plan (one side of the line between the two people) and keep it from the first beat.
- Place each card's camera from the marks, never from a fixed list of tripods. Side-on: square to the line through the pair, on side A, at the shot's distance. Over the shoulder: behind one person, a little toward side A, looking at the other. A fixed plate camera put the left fighter on the right once the fight drifted 3 m.
- Compute, then compare with the card:
  1. screen x of each person from the camera's position, bearing and lens (36 mm sensor): left of 0.4 is frame-left, right of 0.6 frame-right;
  2. axis side: the camera and the side A point on the same side of the line, or the card crosses;
  3. facing on screen: toward camera, back to camera, or profile looking frame-left or frame-right;
  4. the wall at frame centre must equal the card's `camera.faces`; the wall behind each person decides which plate and wall string the card needs;
  5. between cards, the camera turns 30 degrees or more about the pair, or the size changes by two steps (a cut-in);
  6. a person moves more than 3 m between beats only in a card that shows the move.
- An overhead has no left and right of its own: turn the frame so its top points the way side A cameras look, or the order flips.
- Fix a wrong screen side by moving the camera or rerolling with control from the blockout, not by mirroring: a flip makes a right-handed fencer left-handed and mirrors the room.
- The same marks and cameras drive the blockout render for control (entry blockout-control), so the check and the control come from one plan.

## Numbers

- Marks: positions to 0.1 m, facing to 5 degrees. Between consecutive cards in continuous time: within 0.5 m and 25 degrees, unless a card shows the move (starting thresholds, untested).
- Field test: 13 beats of a duel in one room; fixed cameras gave 4 errors (2 screen orders, 1 side B, 1 jump), cameras placed from marks gave 0.

## Vocabulary

- mark, blocking, overhead (plan with people and cameras), side A, wall behind, cut-in.

## Pitfalls

- A camera standing on the line: a small drift puts it on side B. Keep over-the-shoulder cameras 0.7 m or more off the line toward side A.
- Typing `side` and frame positions by hand once people move: they go stale after the first drift.

## Verify

- Compute the six values for every card from the plan (a short script over the marks and cameras does it) and list each mismatch. After rendering, read left-right order and facing in each clip's first and last frame against the computed values.
