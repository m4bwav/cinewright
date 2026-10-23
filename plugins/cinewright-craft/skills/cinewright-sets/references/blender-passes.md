---
title: Blender passes
slug: blender-passes
summary: Render a blockout's control passes in Blender: inverse depth over one range per shot, masks per side from the same render, Mist only with care, line passes, no depth of field or motion blur.
tags: [sets, blockout, blender, depth, mask, previs, control]
last_checked: 2026-10-22
sources: ["Jason van Gumster, Blender All-in-One For Dummies, rendering in passes", "polywright bpy-recipes-scenes and bpy-recipes-physics, run on Blender 5.2.1, 2026-10-22"]
volatile_claims: ["Blender 5.2 compositor and File Output API names"]
---

# Blender passes

## Rules

- Depth control: inverse depth, near white, one near and far range for the whole shot, or the control video pulses. polywright's `pw.py crowd` and `pw.py duel` render it; for a hand-built scene, a shader AOV that maps 1 / view depth over the shot's range does the same (polywright recipe `passes-one-render`).
- Mist is anti-aliased and normalised but maps plain distance, not 1/z, so near figures get fewer tones. If Mist is used, fix its start and depth to the shot's whole range, falloff linear, inverted so near is white, written as 16-bit PNG. Whether a video model follows Mist as well as inverse depth is untested.
- Masks per character or team come from the same render: a shader AOV or Cryptomatte, no second render with swapped materials.
- Keep depth of field and motion blur off in every control pass. Write the lens, f-stop and focus distance into the camera record and let the prompt name them.
- Line control straight from geometry (Grease Pencil Line Art or Freestyle) is an option beside a Canny of a clay render; which one a video model's edge control prefers is untested.
- Set pieces (falling debris, banners, cloaks): bake rigid bodies and cloth headless, then render them through the same passes (polywright recipes `rigidbody-bake`, `cloth-bake`). Bake before rendering.
- Background crowds and dressing: scatter variants with Geometry Nodes rather than placing each one (`pw.py crowd --scatter` for standing figures).

## Numbers

- Render passes at the film's exact frame count and rate. One Cycles render can write inverse depth, masks, Mist and normals together.

## Vocabulary

- inverse depth, Mist pass, shader AOV, Cryptomatte, Line Art, File Output node.

## Pitfalls

- An unnamed File Output node writes `Unsaved<pass>.png` from an unsaved file.
- Two faces on the same plane flicker in clay, depth and edge passes. Delete one or move it.
- A range per frame instead of per shot: the depth video pulses as the camera moves.

## Verify

- Frames 1, middle and last of each pass side by side: near is white, the masks cover the right people, nothing flickers.

Related: see also [blockout-control](blockout-control.md), [master-plates](master-plates.md); crowds: entry crowd-blockout (cinewright-movement).
