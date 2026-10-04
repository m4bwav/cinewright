---
title: Screen direction strings
slug: screen-direction
summary: The fixed phrases for travel, eyeline and frame position that every card and compiled prompt uses, so direction never drifts between shots.
tags: [vocab, continuity, screen-direction, eyeline]
last_checked: 2026-10-03
sources: ["Pat P. Miller, Script Supervising and Film Continuity, 3rd ed., 1999", "https://en.wikipedia.org/wiki/180-degree_rule"]
---

# Screen direction strings

## Vocabulary

Travel (`cast[].travel`): `left-to-right`, `right-to-left`, `toward-camera`, `away-from-camera`, `none`.
Eyeline (`cast[].eyeline`): `frame-left`, `frame-right`, `up`, `down`, `camera`.
Frame position (`cast[].position`): `frame-left`, `center`, `frame-right`.

Compiled phrases, used verbatim:

| Token | Prompt phrase |
|---|---|
| `left-to-right` | moving from left to right across the frame |
| `right-to-left` | moving from right to left across the frame |
| `toward-camera` | walking toward the camera |
| `away-from-camera` | walking away from the camera |
| `frame-left` (eyeline) | looking toward frame left |
| `frame-right` (eyeline) | looking toward frame right |

## Rules

- Write direction as the same fixed phrase in every shot. Paraphrases ("heading east", "to the right") let a model pick a new direction per clip.
- Directions are always as seen from the scene's camera side A. On side B every left and right flips.
- `camera` eyeline (looking into the lens) is only for a POV or a deliberate address; the diff flags it otherwise.
