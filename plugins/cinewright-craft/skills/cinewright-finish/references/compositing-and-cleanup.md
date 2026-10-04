---
title: Compositing and cleanup
slug: compositing-and-cleanup
summary: Match every layer to the plate (light, color temperature, blacks, grain, motion blur, lens, focus, camera height), fix edges and spill, and paint out short AI artifacts.
tags: [finish, vfx, compositing, cleanup, paint, artifacts]
last_checked: 2026-10-04
sources: ["VES Handbook of Visual Effects, 3rd ed., 2020", "Ron Brinkmann, The Art and Science of Digital Compositing, 2nd ed., 2008"]
---

# Compositing and cleanup

## Rules

- Match list, checked for every added layer against the plate: light direction, color temperature, black level, highlight level, grain or noise, motion blur, lens distortion, depth of field, camera height and perspective.
- Blacks first: the darkest part of the layer equals the darkest part of the plate at the same depth. Wrong blacks are the most visible mismatch.
- Edges: soften a matte by the plate's own sharpness (1-2 px on a soft AI render); remove spill (green or blue light on the edge) before color matching.
- Grain last over the whole composite, so plates from different generations share one texture.
- Cleanup of AI artifacts: an extra finger, a melting background object, a flash of text. Paint out with a clean patch from a neighbouring frame (frame hold on a region), or crop the region out when the frame allows. Longer than about 12 frames or on a face: re-render (cinewright-qc).
- Identity faults (a scar on the wrong side) are not cleanup: re-render, unless one still frame is held.
- Composite before the grade's look, after correct and balance of each plate (entry grade-order). Upscale after compositing.

## Vocabulary

- plate, matte, key, spill, roto, paint, garbage matte, premultiplied, edge blend, grain match, frame hold.

## Pitfalls

- A layer from a generation with a different lens look (wide vs long): perspective breaks even when color matches.
- Sharpening a composite: halos appear on every matte edge.

## Verify

- Contact sheet (`CINE qc sheet`) shows matched blacks and grain; a 2x crop of an edge shows no fringe.
