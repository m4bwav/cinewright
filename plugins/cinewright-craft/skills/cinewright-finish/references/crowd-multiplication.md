---
title: Crowd multiplication
slug: crowd-multiplication
summary: Build a crowd or army wide by tiling separate generations of small groups over one locked background plate, each offset in time, scale and position, with haze to blend; never ask a model for the mass.
tags: [finish, vfx, compositing, crowds, battle, tiling]
last_checked: 2026-10-04
sources: ["VES Handbook of Visual Effects, 3rd ed., 2020", "Ron Brinkmann, The Art and Science of Digital Compositing, 2nd ed., 2008"]
---

# Crowd multiplication

## Rules

- Plates: one empty background plate (static camera, the battle's light and haze) and several generations of small groups (3-8 figures) shot with the same camera height, lens words, light direction and time of day. cinewright-movement, entry battle-scenes, plans the cards.
- Every group plate is a separate generation with a different seed and action ("advancing at a walk", "running", "bracing shields"). Repeating one plate side by side shows clones.
- Lock the camera in every plate (move `static`). Tiling with a moving camera needs tracking that most AI plates cannot give.
- Place groups back to front: far groups smaller and higher in frame, more haze and lower contrast, less saturation; near groups larger and sharper. Match the plate's perspective (horizon line through all figures' eyes at the camera height).
- Offset each copy in time (start frames apart) and flip only groups without readable asymmetric detail (banners with text, a hand that holds a sword).
- Isolate groups with a key on a plain background plate (ask for a flat green or grey ground and sky) or a matte from a segmentation model; soften edges by 1-2 px; add the same grain over all.
- Blend with what hides seams: dust, smoke, rain and depth haze over the joins; foreground figures from the real shot on top.
- Same side, same screen direction in every tile (cinewright-continuity, screen direction).

## Numbers

- 3-8 figures per group plate; at least 4 distinct plates before any repeats; haze and contrast step per depth band.

## Pitfalls

- Matching scale by eye: figures float. Put all feet on the ground plane and check against the horizon.
- One light direction in the background and another in a group plate: the composite shows it at once (entry compositing-and-cleanup).

## Verify

- A contact sheet of the composite (`CINE qc sheet`) shows no repeated figure within one frame and one light direction throughout.
