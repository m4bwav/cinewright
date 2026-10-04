---
title: Upscale and interpolation
slug: upscale-and-interpolation
summary: Upscale and interpolate last, after the grade, crop and composites, once each; retime slow motion with motion interpolation only when the shot has simple motion, and check for warped frames.
tags: [finish, upscale, interpolation, retime, slow-motion, delivery]
last_checked: 2026-10-04
sources: ["https://ffmpeg.org/ffmpeg-filters.html", "cinewright S2 render, 2026-10-03 (practice)"]
---

# Upscale and interpolation

## Rules

- Finishing order: conform → cleanup and composites → grade (correct, balance, match, look) → crop to `frame_aspect` → titles → upscale → interpolate or retime → delivery encode. Upscale and interpolation come last because each invents pixels that later steps would amplify.
- Upscale once, straight to the delivery size; two passes double the invented detail. Check faces at 100%: an upscaler can change a face's features (identity) or add texture that flickers.
- Interpolation to raise frame rate (24 → 30 or 60) is for web delivery only; films stay at 24 (cinewright-camera, entry frame-rate-and-shutter).
- Slow motion from a 24 fps render: motion interpolation (`minterpolate` or a learned interpolator) works on simple, slow motion; it warps hands, crossing limbs, spinning objects and fast camera moves. Check every interpolated shot frame by frame; prefer asking the model for slow motion on the card.
- Simple retime without new frames (speed up, or slow by frame doubling) uses `setpts`; frame doubling stutters below about 70% speed.
- Keep the source and a pre-upscale master; the upscale is a delivery step, not the archive.

## Numbers

- 864x480 → 1920x1080 is 2.22x; anything over 4x invents most of the frame. A 50% slow motion from 24 fps needs 48 fps of motion.

## Pitfalls

- Interpolating before the edit: the cut lands on invented frames.
- Upscaling before the grade: the grade then pushes upscaler texture and banding.

## Verify

Slow a shot to 50% with motion interpolation, then upscale to 1080p:

```
ffmpeg -i shot.mov -vf "minterpolate=fps=48:mi_mode=mci,setpts=2*PTS,fps=24" -an slow.mov
ffmpeg -i final_cut.mov -vf "scale=1920:-2:flags=lanczos" -c:v libx264 -crf 16 -c:a copy up.mp4
```

- A contact sheet at 4 fps of the slowed shot (`CINE qc sheet slow.mov --fps 4`) shows no warped limbs.
