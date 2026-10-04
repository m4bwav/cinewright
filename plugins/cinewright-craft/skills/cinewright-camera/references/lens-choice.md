---
title: Lens choice
slug: lens-choice
summary: Pick a focal length per card from what the shot must do to the face and the space; one lens family per film, recorded in the style bible so the continuity diff can check every card.
tags: [camera, lens, focal-length, perspective]
last_checked: 2026-10-04
sources: ["Blain Brown, Cinematography: Theory and Practice, 3rd ed., 2016", "Steven D. Katz, Film Directing Shot by Shot, 1991", "ASC Manual, 11th ed., 2022"]
---

# Lens choice

## Rules

- Default ladder: 24mm for wides and establishing shots, 35mm for two-shots and walking, 50mm for singles and mediums, 85mm for close-ups. Change it only with a reason written in the card's `notes`.
- Match the lens across a reverse pair: both singles of a conversation use the same focal length and distance, or the faces change size and the cut jumps (cinewright-continuity, matched singles).
- Close-ups below 35mm distort the face (nose grows, ears shrink). Use a wide close-up only on purpose: comedy, menace, a character losing control.
- Long lenses (85mm and up) flatten the background and isolate the subject; use them for a figure in a crowd, heat shimmer, or a chase seen from far.
- One lens family per film in `bibles/style.json` `lens_family`, with its range in mm ("spherical primes, 24-85mm"). The diff warns LENS when a card leaves it.
- Write the focal length in the card (`lens_mm`); the compiler says "50mm lens". Add an effect word only when the effect is the point ("wide-angle lens, the room stretching away").

## Numbers

- Ladder: 24 / 35 / 50 / 85 mm. Matched singles: same mm, same distance.
- A zoom card (`zoom-in`, `zoom-out`) starts and ends inside the family's range.

## Pitfalls

- A focal length alone changes little in most video models; size and angle words do more (shot-sizes vocab). The mm number tunes perspective, it does not set the size. (Practice observation, unverified across models.)
- "Fisheye" and "ultra-wide" take over the whole look; avoid them unless the film's style asks.
- Changing lens between two cards of the same subject without a size step reads as a jump (thirty-degree rule).

## Verify

- `continuity diff` shows no LENS warning; reverse singles share `lens_mm`.

## Notes

- 2026-10-04: focal bands from the shared lens-terms entry, 35 mm still-photo terms.
