---
title: Lens terms
slug: lens-terms
summary: Focal-length bands on full-frame 35 mm with what each does to faces and space, plus the lens words a style card or style bible uses (spherical, anamorphic, zoom, vintage, bokeh, flare).
tags: [vocab, camera, lens, focal-length, history]
last_checked: 2026-10-04
sources: ["Blain Brown, Cinematography: Theory and Practice, 3rd ed., 2016", "ASC Manual, 11th ed., 2022", "https://en.wikipedia.org/wiki/Anamorphic_format"]
---
<!-- copied from shared/vocab/lens-terms.md sha256:b4d3d926d7377cab65c09bbbe2766605d42897db301b73933e3ca4c717f52a56; edit the source -->

# Lens terms

## Vocabulary

| Band (mm) | Name | Effect | Prompt words |
|---|---|---|---|
| 14-24 | wide | space stretches, near objects loom, faces distort close up | wide-angle lens, deep space |
| 28-40 | normal-wide | natural space, room for action | 35mm lens |
| 50 | normal | close to the eye's perspective | 50mm lens |
| 85-135 | portrait, long | flattering faces, background compressed and soft | telephoto lens, compressed background |
| 200+ | very long | heavy compression, shimmer, isolates a figure in a crowd | long telephoto lens |

| Term | Meaning |
|---|---|
| spherical | ordinary round-image lens; round bokeh |
| anamorphic | squeezes the width 2x on capture; oval bokeh, horizontal streak flares, wider view for the same focal length |
| prime / zoom | fixed focal length / variable; a zoom can change size during the shot (`zoom-in`) |
| vintage glass | older coatings: lower contrast, flare, soft corners |
| bokeh | the shape and softness of out-of-focus points |
| flare | light scattered from a bright source into the lens |
| focus pull | focus moving from one subject to another during a shot |
| `lens_family` | style-bible string: kind and range, e.g. `spherical zooms, 25-250mm` |

## Rules

- Bands are in 35 mm still-photo terms, which is how video models read a focal length. A Super 35 cinema camera gets the same view at about two-thirds of the number.
- A card's `lens_mm` must fall inside the style's `lens_family` ranges; `continuity diff` warns LENS otherwise.
