---
title: Lighting setups
slug: lighting-setups
summary: Key from the upstage side (the far side of the face), back-cross keys for two people, one world side for the key across coverage, and the card light fields.
tags: [lighting, key, setup, motivated, practical, coverage]
last_checked: 2026-10-22
sources: ["Blain Brown, Motion Picture and Video Lighting, 3rd ed., 2018", "Blain Brown, Cinematography: Theory and Practice, 3rd ed., 2016"]
---

# Lighting setups

## Rules

- Start from the source the scene has (a window, a lamp, a fire, the sun) and write it in the scene bible's `sun` string with its direction and color. Every card of the scene gets it.
- Per card, set `light.key_side` (where the key comes from in frame), `light.quality` (hard or soft) and `light.motivation` (the source). The compiler writes "soft key light from frame right".
- Keep the key on the same world side across a scene: in a reverse pair the key moves from frame right to frame left because the camera turned, never because the light did. Write it per card from the camera's side (cinewright-continuity, axis).
- Default setup for faces: soft key at 45 degrees on the far side of the face (short side, the upstage side), a little fill, a back light for separation. Words: "soft key light from frame left, faces modelled, a thin rim of light on the hair". In frame terms the key comes from the side the face turns to: a face looking frame left takes `key_side: frame-left`. Compile adds "on the far side of the face"; `continuity diff` warns KEY-SIDE on a broad key (after Brown, *Cinematography*).
- Never light a face from beside the camera: flat front light has no modelling. Side and back light give shape and separation.
- Two people talking: back-cross keys. Each one's key is the other's back light, so each single is "lit from behind the other person, a rim of light on the far shoulder". With short-side keys on both singles the reverse pair agrees by construction.
- Low-key scenes can drop the fill: a kicker (a three-quarter back light grazing the shadow-side cheek) keeps the face off the background. Separation comes from a back light or a background darker or brighter than the face.
- `light.tone: hide` keeps a face in shadow or glare on purpose (an informant, a menacing entrance); a reveal is a person stepping into the light. Hidden faces skip the identity checks.
- Name the setup only when the look calls for it: Rembrandt (drama), butterfly (glamour), split (conflict), loop (default portrait) (lighting-terms vocab).
- Practicals, windows, exteriors and airborne matter: entry light-sources.
- Hard light for noon sun, noir and menace; soft light for overcast, interiors with windows, faces in close-up.

## Numbers

- Key at 30-45 degrees off the camera axis for loop and Rembrandt, 90 for split.

## Pitfalls

- A key side that flips between matched singles without a reason reads as a lighting error (qc catches it; the diff cannot).
- A broad key because the scene's sun fixes it: say "broad" in `light.motivation` so the warning knows it was chosen.
- Mixing hard and soft keys in one scene without a source change looks like two locations.

## Verify

- Every card of a scene has a key side consistent with its camera side and the scene's source.
- `CINE continuity diff <project>`: no KEY-SIDE warning left unanswered.
