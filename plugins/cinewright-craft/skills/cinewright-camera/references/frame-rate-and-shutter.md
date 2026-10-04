---
title: Frame rate and shutter
slug: frame-rate-and-shutter
summary: 24 fps with a 180-degree shutter is the film default; the model card fixes the render rate, so slow motion and staccato action are asked for in words and finished in the edit.
tags: [camera, frame-rate, shutter, motion-blur, slow-motion]
last_checked: 2026-10-04
sources: ["https://www.reddigitalcinema.com/red-101/shutter-angle-tutorial", "ASC Manual, 11th ed., 2022"]
---

# Frame rate and shutter

## Rules

- Default 24 fps, 180-degree shutter (exposure 1/48 s): the motion blur audiences read as film. 25 fps for PAL delivery, 30 for web and broadcast in the Americas.
- The render rate comes from the model card (`fps` in its Compile block); the style bible's `fps` must be one the model renders or the edit converts. Do not ask a model for a frame rate in the prompt text.
- Slow motion: write "in slow motion" on the card and keep the action short; a model shows less motion per second, it does not shoot 120 fps. Retiming in the edit is the fallback (cinewright-finish, interpolation).
- Narrow shutter (45-90 degrees): crisp, stuttering action, as in war and fight films. Ask for "sharp, staccato motion, no motion blur"; unverified how far models follow it.
- Wide shutter (360 degrees): smeared, dreamy motion. Ask for "heavy motion blur".
- Keep one shutter feel per scene; a mix reads as a fault.

## Numbers

- Shutter speed = 1 / (fps x 360 / angle): 24 fps at 180 degrees = 1/48 s; at 90 = 1/96 s; at 45 = 1/192 s.
- Common rates: 23.976 / 24, 25, 29.97 / 30, 48, 50, 59.94 / 60, 120.

## Vocabulary

- frame rate, shutter angle, motion blur, slow motion, overcrank, undercrank, speed ramp, staccato, judder.

## Pitfalls

- Fast pans at 24 fps judder; keep pans slow (camera-moves vocab says "slow").
- Interpolating 24 to 60 fps gives the soap-opera look; deliver at the render rate unless the platform demands more.

## Verify

- Style `fps` equals the model card's fps, or the finishing plan names the conversion.
- `qc spec` on a take reports the planned fps.

## Notes

- 2026-10-04: RED's tutorial gives 180 degrees as about 1/48 s at 24 fps and calls narrow angles stuttered and 360 softer and more fluid.
