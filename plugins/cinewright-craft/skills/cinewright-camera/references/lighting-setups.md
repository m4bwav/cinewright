---
title: Lighting setups
slug: lighting-setups
summary: Light each scene from its motivated source, keep the key on one world side across the coverage, and fill each card's light fields (key_side, quality, motivation) so prompts agree.
tags: [lighting, key, setup, motivated, practical, coverage]
last_checked: 2026-10-04
sources: ["Blain Brown, Motion Picture and Video Lighting, 3rd ed., 2018", "Blain Brown, Cinematography: Theory and Practice, 3rd ed., 2016"]
---

# Lighting setups

## Rules

- Start from the source the scene has (a window, a lamp, a fire, the sun) and write it in the scene bible's `sun` string with its direction and color. Every card of the scene gets it.
- Per card, set `light.key_side` (where the key comes from in frame), `light.quality` (hard or soft) and `light.motivation` (the source). The compiler writes "soft key light from frame right".
- Keep the key on the same world side across a scene: in a reverse pair the key moves from frame right to frame left because the camera turned, never because the light did. Write it per card from the camera's side (cinewright-continuity, axis).
- Default setup for faces: soft key at 45 degrees on the far side of the face (short side), a little fill, a back light for separation. Words: "soft key light from frame left, faces modelled, a thin rim of light on the hair".
- Name the setup only when the look calls for it: Rembrandt (drama), butterfly (glamour), split (conflict), loop (default portrait) (lighting-terms vocab).
- Practicals in frame sell the source; put the lamp, candle or screen in the location or the card's action.
- Hard light for noon sun, noir and menace; soft light for overcast, interiors with windows, faces in close-up.

## Numbers

- Key at 30-45 degrees off the camera axis for loop and Rembrandt, 90 for split.

## Pitfalls

- A key side that flips between matched singles without a reason reads as a lighting error (qc catches it; the diff cannot).
- Mixing hard and soft keys in one scene without a source change looks like two locations.

## Verify

- Every card of a scene has a key side consistent with its camera side and the scene's source.
