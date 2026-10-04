---
title: Failure codes, picture and continuity
slug: failures-picture
summary: Failure codes for rendered takes (identity, wardrobe, props, direction, eyeline, light, look, camera): symptom, cause, cheapest fix, rung, check.
tags: [vocab, qc, failures, taxonomy, continuity]
last_checked: 2026-10-03
sources: ["field lessons 005, 010-013, 017, 019 (maintainer's local renders, 2026-09)", "Pat P. Miller, Script Supervising and Film Continuity, 3rd ed., 1999"]
---
<!-- copied from shared/vocab/failures-picture.md sha256:1d5282fa2edbe43bfcf1261b31fc322b80de1abca2408285ce13c27d87c20dd1; edit the source -->

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

## Rules

- Log the code (`takes log --fix`); try its rung once, then climb one.
- One change per reroll. Three failed takes of one card: re-plan the card (rung 6).
