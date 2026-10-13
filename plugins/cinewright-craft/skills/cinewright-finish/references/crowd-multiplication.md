---
title: Crowd multiplication
slug: crowd-multiplication
summary: Build a crowd or army wide by tiling separate generations of small groups over one locked background plate, each offset in time, scale and position, with haze to blend; never ask a model for the mass.
tags: [finish, vfx, compositing, crowds, battle, tiling]
last_checked: 2026-10-13
sources: ["VES Handbook of Visual Effects, 3rd ed., 2020", "Ron Brinkmann, The Art and Science of Digital Compositing, 2nd ed., 2008", "https://docs.comfy.org/tutorials/video/wan/wan-alpha", "https://docs.comfy.org/tutorials/utility/video-segment-sam3", "https://arxiv.org/abs/2512.11782 (MatAnyone 2)", "https://beeble.ai/blog/canvas-tutorial-crowd-vfx (2026-06-25, vendor)"]
---

# Crowd multiplication

## Rules

- Plates: one empty background plate (static camera, the battle's light and haze) and several generations of small groups (3-8 figures) shot with the same camera height, lens words, light direction and time of day. cinewright-movement, entry battle-scenes, plans the cards.
- Every group plate is a separate generation with a different seed and action ("advancing at a walk", "running", "bracing shields"). Repeating one plate side by side shows clones.
- Lock the camera in every plate (move `static`). Tiling with a moving camera needs tracking that most AI plates cannot give.
- Hero layer first, crowd layers after, each kept separate so one can be redone alone; rerun only the smallest failed region.
- Place groups back to front: far groups smaller and higher in frame, more haze and lower contrast, less saturation; near groups larger and sharper. Match the plate's perspective (horizon line through all figures' eyes at the camera height).
- Offset each copy in time (start frames apart) and flip only groups without readable asymmetric detail (banners with text, a hand that holds a sword).
- Plate: the plate's first frame before anyone enters, or a generation prompted "locked tripod, empty field, no people".
- Isolate groups, best first: generate them with an alpha channel (Wan-Alpha, RGBA PNG sequence; text-to-video only); track masks with SAM 3.1 Multiplex (`person:N`, one id per figure across frames); MatAnyone 2 only where soft edges show (hair, cloth, dust). Per-frame matting (BiRefNet) flickers; use it only for a first-frame seed. Soften edges by 1-2 px, blur inserted layers very slightly, add the same grain over all.
- Unify last: relight or regrade the whole merged frame from one reference frame, never the inserted layer alone; a low-denoise video-to-video pass over the whole composite (0.3-0.45) with the depth control locks the layout while matching light.
- Camera moving or sides meeting: stage the crowd in 3D instead (cinewright-movement, entry crowd-blockout).
- Blend with what hides seams: dust, smoke, rain and depth haze over the joins; foreground figures from the real shot on top.
- Same side, same screen direction in every tile (cinewright-continuity, screen direction).

## Numbers

- 3-8 figures per group plate; at least 4 distinct plates before any repeats; haze and contrast step per depth band.

## Pitfalls

- Matching scale by eye: figures float. Put all feet on the ground plane and check against the horizon.
- One light direction in the background and another in a group plate: the composite shows it at once (entry compositing-and-cleanup).

## Verify

- A contact sheet of the composite (`CINE qc sheet`) shows no repeated figure within one frame and one light direction throughout.
