---
title: Failure codes, picture and continuity
slug: failures-picture
summary: Failure codes for rendered takes (identity, wardrobe, props, direction, eyeline, light, look, camera, space, attention): symptom, cause, cheapest fix, rung, check.
tags: [vocab, qc, failures, taxonomy, continuity]
last_checked: 2026-10-22
sources: ["field lessons 005, 010-013, 017, 019 (maintainer's local renders, 2026-09)", "set field test, 2026-10-15: a rapier duel from a novel, one card three ways", "Pat P. Miller, Script Supervising and Film Continuity, 3rd ed., 1999", "Blain Brown, Cinematography: Theory and Practice, 3rd ed., 2016", "Bruce Block, The Visual Story, 3rd ed., 2021"]
---

# Failure codes, picture and continuity

## Vocabulary

Rung: the repair ladder in the router's `pipeline` entry (1 prompt, 2 parameter, 3 regenerate, 4 keyframe, 5 v2v, 6 re-plan, 7 edit, 8 cut). Check: the `qc rubric` item.

| Code | Symptom | Cause | Cheapest fix | Rung | Check |
|---|---|---|---|---|---|
| `identity-drift` | face, age, hair or mark off the bible | identity paraphrased or missing; no ref | paste the identity verbatim; add a turnaround ref | 1 | identity |
| `identity-merge` | two people share a face | two weakly told-apart people | a sentence on who has what; one ref each | 1 | identity |
| `wardrobe-drift` | costume colour, cut or layer changes | wardrobe not restated | paste the scene's wardrobe verbatim | 1 | wardrobe |
| `prop-drift` | prop changes size or shape, appears or vanishes | prop defined loosely | one prop constant in every prompt | 1 | props |
| `emblem-copied` | a mark from a ref shows on the subject | models copy small marks from refs | paint the mark out of the ref | 4 | wardrobe |
| `direction-flip` | subject crosses the frame the wrong way | story direction, not frame terms | fixed screen-direction phrase; then a new seed | 1 | direction |
| `side-swap` | people swap frame sides between shots | positions unstated, or axis crossed | state frame positions; camera back to its side | 1 | position |
| `eyeline-wrong` | looks the wrong way or into the lens | no direction or no target | direction and target (`at Tomas`) | 1 | eyeline |
| `light-flip` | key side, sun or time of day changes | light not restated | restate sun and key side from the bible | 1 | light |
| `look-drift` | grade, grain or palette differs | look string edited or missing | paste the look verbatim; match in the grade | 7 | style |
| `wrong-framing` | size or angle not as carded | camera words buried late | camera first, one size, one angle | 1 | camera |
| `wrong-move` | extra, missing or fast camera move | two moves, or no speed | one move with a speed ("slow") | 1 | camera |
| `set-drift` | the room behind is not the planned one: a wall, opening, stair or dressing the set does not have | the set passed only as a grid of views; the card's wall string missing | Canny control from the blockout at the card's own camera; the faced wall's plate as a ref | 4 | set |
| `flat-light` | the face is lit from beside the camera, no modelling, no shadow side | key side unstated, or on the near side of the face | restate the key on the far side of the face (`key_side` = the side the face turns to) | 1 | light |
| `source-mismatch` | the light on the face disagrees with the lamp, fire or window in frame | the practical named without its side | carry the source: "the lamp at frame left lights her face from the left" | 1 | light |
| `atmos-unlit` | rain, haze or smoke invisible or flat, lit from the front | no light behind it | set `light.atmosphere`; compile writes it backlit | 1 | light |
| `tone-hides-subject` | the face or subject the card needs is lost in shadow or glare | dark key, bright background, or a hide not planned | a reveal phrase or a rim; `light.tone: hide` only when meant | 1 | light |
| `space-break` | depth reads against the scene's space: lines into the distance in a flat scene, a cramped wall in a deep one | space words missing, or a move or lens that undoes them | restate the scene's `space`; a 2D move or a longer lens for flat, staged depth for deep | 1 | space |
| `attention-jump` | at the cut the eye has to cross the frame where the plan keeps it in place | subject cell not planned, or the take put it elsewhere | `attention` cells on both cards; reframe in the crop; or cut to a reaction | 7 | attention |

## Rules

- Log the code (`takes log --fix`); try its rung once, then climb one.
- One change per reroll. Three failed takes of one card: re-plan the card (rung 6).
