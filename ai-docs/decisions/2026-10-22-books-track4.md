---
title: Books track 4, framing and prompt vocabulary rulings
kind: decision
status: active
date: 2026-10-22
verified: 2026-10-22
stale_after: 2027-04-22
tags: [books, framing, composition, camera, angle, horizon, moves, lens, focus, failures, schema, runtime]
entities: [cine.py, shot-card, continuity-diff, compile, qc-rubric, camera-angles, camera-moves, failures-framing]
summary: "Read before changing camera.horizon, camera.dutch, cast view, the arc, push-in or dolly-zoom moves, the STRAIGHT-IN, HORIZON or DUTCH warnings, the framing rubric row or the framing failure codes: the calls made in books track 4"
---

# Books track 4, framing and prompt vocabulary rulings

## Context

Track 4 of the book-learnings build (Mateu-Mestre, *Framed Ink* 1 and 2; Roberts, Chen and Garvey-Williams on composition; Gurney, *Color and Light* and *Imaginative Realism*; the items track 2 handed on from Mascelli, Katz and Murch, and track 3's G13 list from Block and Brown) adds framing, camera-angle, move and lens vocabulary to cinewright. The shared lighting and framing prompt words for image prompts went to a sibling private skill. Related: builds on [2026-10-22-books-track3.md](2026-10-22-books-track3.md).

## Decision

- H1 Fields, all optional: `camera.horizon` (lower-third, middle, upper-third, above-frame, below-frame), `camera.dutch` (left, right) and `cast[].view` (front, three-quarter, profile, back, three-quarter-back). Unset fields compile to nothing, so no committed example prompt changed.
- H2 The horizon is a field, not a default compiled from the angle: every noun in a prompt tends to get drawn, and indoors "horizon" asks for an outside. The out-of-frame values name the ground or the sky, never the word horizon.
- H3 The three-quarter default lives in `cards new` (`view: three-quarter`), not in compile, so existing cards keep their prompts.
- H4 STRAIGHT-IN warns on a cut two or more sizes tighter, under 10 degrees of azimuth, with someone in the shot off centre (Mascelli). It first fired on 7 of 163 real cards; two were cuts back out to a wide, which the rule is not about, so it reads cut-ins only: 4 of 163 (2.5 %), all two fighters across the frame on one axis (continuity L-008).
- H5 HORIZON warns when a low angle has a high horizon, a high angle a low one, or an overhead shot any horizon but above-frame. DUTCH warns when the side is set on a level angle, or when two consecutive dutch cards on different people tilt the same way (Mascelli's opposing pairs). No real card sets either field, so the real cards cannot exercise them; tests and mutation runs only.
- H6 New moves: `push-in` (an alias of `dolly-in` with its own word), `arc-left`, `arc-right`, `dolly-zoom`. Arcs, push-in and the dolly zoom count as 3D moves for SPACE.
- H7 Eight new failure codes go in a new vocab entry, failures-framing, because failures-picture sits near the red line. `eye-trace-jump` from the notes is track 3's `attention-jump` and was not added twice. One rubric row, `framing`, carries six of them; `horizon-split` goes to `camera`, `flat-depth` to `space`.
- H8 No `qc cutcheck` in the runtime. A measured eye trace needs a face or subject detector, which the stdlib runtime lacks; the prototype on 219 real cuts (a face detector outside the runtime) found a face on both sides of only 85 and could not be calibrated (qc L-008). The rubric `attention` row and the ATTENTION warning stay the check here.
- H9 Placement: the same data showed planned left and right faces at a median 0.37 and 0.60 of the width (shots L-001). The compile words "on the left of the frame" stay unchanged until a render test shows stronger words move it; the rule went into framing guidance.
- H10 Gurney's "light the maquette" became a corrected rule in blockout-control: depth, edge and pose controls carry no light, so only a blockout used as the first frame or guide still carries it. His supreme moment went to the animatic stills. His gamut-per-sequence item was already in color-script.
- H11 New entries rather than growing full ones: frame-tension (shots), move-grammar (camera). framing.md, lens-choice and depth-of-field grew by a few rules each.
- H12 Not built: diagonal travel as a `travel` token (it would need its own screen-direction rules; it is prompt words in framing.md), an OTS warning for a missing rear view (it would fire on every real OTS card, which has no `view`), the eye-level-of-a-seated-subject compile words, vertical reframing (still unassigned from G14).
- H13 Records: track 3's records had spliced each new entry into the "Entry shape" template line of twelve CHANGELOG and TESTS files; this track restored the template lines and moved those entries into their lists.

## Consequences

- Runtime 185 KB of red 200 (+3 KB). Track 7's cinewright part has about 15 KB before red.
- Planners can set the horizon, the dutch side and each person's view and get the words compiled; three diff warnings check them, one of them (STRAIGHT-IN) on real data.
