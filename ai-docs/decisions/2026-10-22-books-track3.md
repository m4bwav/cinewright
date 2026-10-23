---
title: Books track 3, visual structure and light rulings
kind: decision
status: active
date: 2026-10-22
verified: 2026-10-22
stale_after: 2027-04-22
tags: [books, visual-structure, light, space, attention, grade, schema, runtime]
entities: [cine.py, cine_post.py, shot-card, scene-axis-bible, style-bible, continuity-diff, cards-graph, grade-measure, grade-stabilize]
summary: "Read before changing visual_structure, scene intensity, space or color, card line, attention, light.tone or light.atmosphere, the SPACE, KEY-SIDE or ATTENTION warnings, cards graph, or grade measure --plan, stabilize, --sat and --warm: the calls made in books track 3"
---

# Books track 3, visual structure and light rulings

## Context

Track 3 of the book-learnings build (Block, *The Visual Story*; Brown, *Cinematography: Theory and Practice*; *FilmCraft: Cinematography*; Phillips on DaVinci Resolve) adds Block's visual structure plan and Brown's lighting rules to cinewright. The notes proposed fields, checks and measures; these are the calls made while building them. Related: builds on [2026-10-22-books-track2.md](2026-10-22-books-track2.md).

## Decision

- G1 Fields. Scene `intensity` (0-100), `space` (deep, flat, limited, ambiguous) and `color` (hue, brightness third, saturation, warmth); card `intensity`, `line` (horizontal, vertical, diagonal, curved) and `attention` (`start`, `end`, cells 1-9); style `visual_structure` (point_of_view, flow, climax, constants, plans, meanings). All optional, so every existing card still validates.
- G2 `tone` lives in `light.tone` (reveal or hide), not on the card: dialogue already has a `tone`. A hidden face pre-sets the identity rubric items to `na` and skips KEY-SIDE.
- G3 Atmosphere is a field, `light.atmosphere`, not a word match on prose: on 163 real cards the words were mostly dust on cars and floors (camera L-005 `atmosphere-is-a-field-not-a-word`). Firelight flicker comes only from `light.motivation`.
- G4 KEY-SIDE warns only on a single person with a side eyeline and a side key on the other side. "broad" in `light.motivation` or the style's lighting, high-key or flat lighting, and `tone: hide` silence it. On 163 real cards it fired 13 times (8 %), 13 of the 27 cards it can read; most were cars lit by a sun the scene fixes, hence the card-level opt-out. Compile adds "on the far side of the face" to a short-side key, which changed six committed example prompts.
- G5 SPACE counts dolly, track and crane as depth moves. Trucks are left out, because a truck past a wall square to the camera stays flat. Lenses under 35 mm warn in flat and limited scenes, and a deep scene whose cards are all static eye-level frames warns once. No real scene sets `space`, so the real cards cannot exercise it.
- G6 ATTENTION: a jump is the larger of the row and column difference; 2 is across the frame and warns below intensity 50 or with intensity unset. A start cell whose column disagrees with a single person's `position` warns too. No real card sets `attention`. A measured attention check on rendered cuts needs a face or subject detector; it belongs with track 4's `qc cutcheck` eye trace (cinema-a C3). Until then the rubric asks it (`attention` row), by eye or through `qc judge`.
- G7 `move-no-settle` and `pan-strobe` are review codes, not `qc measure` checks: both proxies failed on 354 real shots (qc L-007 `motion-proxies-miss-settle-and-strobe`). `qc measure` is unchanged.
- G8 `grade measure --plan` measures mean luma, the p5-p95 luma spread (tone), mean chroma (saturation), mean red minus blue (warmth), Sobel edge orientation shares (line) and mean frame difference (movement). A progression ranks the measure against cut order, with the expected direction read from the plan's from and to words; peaks ranks the distance from the film's median against intensity. Exit 1 when a class is two steps off or a plan runs AGAINST (|rho| 0.3). Class bounds: brightness by thirds of 0-255 (Block); chroma and warmth at the sixths of 354 real shots. Uncalibrated against faults (finish L-005 `colour-classes-miss-relative-light-faults`).
- G9 `grade stabilize` holds each frame to the shot's middle frame, gains smoothed over 1 s and clamped to 0.6-1.6, applied through ffmpeg `sendcmd` and `colorchannelmixer` in one pass. It warns over 8 luma of drift (finish L-004 `stabilize-reads-content-as-drift`).
- G10 `grade match --sat` and `--warm` take targets in `grade measure --plan` units and solve them together in four rounds, because the warm shift adds chroma and saturation scales red minus blue.
- G11 New rubric checks `space` and `attention` carry the new codes `space-break` and `attention-jump`; the four light codes go to `light`, the two move codes to `camera`.
- G12 Size: the look pass is its own qc entry (review-passes went past 1,200 tokens), and practicals, windows, exteriors and atmosphere moved from lighting-setups into a new light-sources entry. Runtime 182 KB of red 200 (yellow): cine.py +13 KB, cine_post.py +15 KB.
- G13 Left for track 4, with the other framing and camera vocabulary: the arc, push-in and dolly-zoom move tokens, the 2D and 3D move rules in the camera-moves vocab, the punch-in at the turn, dolly versus zoom, the lens and focus rules (who gets focus, wide-and-close) and `framing.md`. Surface divisions went into space-types.
- G14 Not built: `qc sheet --squint`, since a reviewer can squint at a small copy and a vision model can do it. Unassigned: vertical and square reframing with looking room, and stabilise-before-crop in crop-to-frame (finishing delivery).

## Consequences

- Planners can write a visual plan that compiles and that two commands check (`cards graph` before rendering, `grade measure --plan` after the edit). None of the new checks has labelled faults behind it; all warn or report, and the class bounds are published with their rates.
- Track 4 builds framing, camera-angle and eye-trace checks on these fields: `attention` cells, `line`, scene `space`, and the `attention` rubric row.
