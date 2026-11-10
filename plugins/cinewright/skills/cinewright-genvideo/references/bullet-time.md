---
title: Bullet time (frozen-time orbit)
slug: bullet-time
summary: A frozen-time 360 orbit of one photo on MiniMax H3 with the 360 Orbit LoRA; measured settings, times and limits.
tags: [h3, camera, orbit, lora]
last_checked: 2026-11-10
sources: ["https://huggingface.co/pablodawson/MiniMax-H3-360-Orbit-LoRA", "https://www.reddit.com/r/StableDiffusion/comments/1wuzyq0/", "local test 2026-11-10, 6 runs on a 16 GB consumer GPU"]
---

# Bullet time (frozen-time orbit)

## Rules

- Route: the same image as first and last frame, the 360 Orbit LoRA (pablodawson, H3 community licence) at 1.0 and the card's prompt verbatim; 768x768, 73 frames. Locally: `h3_video.py --first-frame X --last-frame X --lora2 <orbit lora>`.
- Default 8 turbo steps; 28 steps without turbo for a hero shot.
- People only. A prop or figure morphs mid-orbit: use a real 3D route (a splat or mesh turntable) for objects.
- The loop closes on the input frame, so orbits chain or loop.

## Numbers

- Measured 2026-11-10 (768x768, 73 frames, one seed): turbo 8 steps + orbit 154 s vs 410 s at 28 steps; full turn, back of the head seen; seam PSNR frame 0 vs 72 28-35 dB. Without the LoRA, identical frames render a near-still.

## Pitfalls

- The background is redrawn as the camera turns: plausible, not the real place.
- Orbit frames are not geometrically consistent; as 3D input they are pseudo-views only.
