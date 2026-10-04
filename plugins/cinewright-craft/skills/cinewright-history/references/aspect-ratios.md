---
title: Aspect ratios
slug: aspect-ratios
summary: Cinema and delivery aspect ratios with their era, the style-bible frame_aspect string, and how much of a 16:9 render each keeps after the crop.
tags: [vocab, camera, aspect, format, history]
last_checked: 2026-10-04
sources: ["https://en.wikipedia.org/wiki/Aspect_ratio_(image)", "ASC Manual, 11th ed., 2022"]
---
<!-- copied from shared/vocab/aspect-ratios.md sha256:5ae623ce0adbacd1935513e00158dac0d6a30ea8cce1dcd3f9a07fe77b7c0d5a; edit the source -->

# Aspect ratios

## Vocabulary

| `frame_aspect` | Name | Era and use | Kept of a 16:9 render |
|---|---|---|---|
| `1.33:1` | silent full frame (4:3) | silent era; old TV | 75% of the width |
| `1.37:1` | Academy | sound films 1932 to the early 1950s | 77% of the width |
| `1.43:1` | IMAX film | large-format IMAX | 80% of the width |
| `1.66:1` | European widescreen | Europe from the 1950s | 93% of the width |
| `1.78:1` | 16:9 | TV, streaming, web; the usual render | all |
| `1.85:1` | flat widescreen | US theatrical from 1953 | 96% of the height |
| `2.00:1` | Univisium | 1950s Superscope; streaming series | 89% of the height |
| `2.20:1` | 70 mm (Todd-AO) | 1950s-60s roadshow epics | 81% of the height |
| `2.39:1` | anamorphic scope (2.35, 2.40) | 2.35 from 1957, 2.39 from 1970 | 74% of the height |
| `2.55:1` | early CinemaScope | 1954-1956 | 70% of the height |
| `9:16` | vertical | phone video | render 9:16, never crop |

## Rules

- The style bible's `aspect_ratio` is what the model renders (a size it offers); `frame_aspect` is what the film is composed and delivered in. They differ when the model has no such size.
- Written as `W:1` with two decimals, or `9:16` for vertical.

## Notes

- 2026-10-04: Wikipedia gives 1932 for Academy, May 1953 for 1.85, SMPTE 1957 for 2.35 and 1970 for 2.39.
