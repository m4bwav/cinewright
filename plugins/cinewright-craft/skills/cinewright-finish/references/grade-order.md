---
title: Grade order
slug: grade-order
summary: Grade in four passes in this order, correct (exposure, balance, contrast per shot), balance (a scene's shots agree), match (scenes agree), look (the style, once, on top).
tags: [finish, color, grade, correction, look, cdl]
last_checked: 2026-10-04
sources: ["Alexis Van Hurkman, Color Correction Handbook, 2nd ed., 2014", "ASC Manual, 11th ed., 2022"]
---

# Grade order

## Rules

- Grade only a locked cut (cinewright-edit). Order, every time: correct → balance → match → look. A look laid on uncorrected shots multiplies their differences.
- Correct, per shot: set black point, white point and contrast on the waveform; neutralise white balance on something that should be neutral (a grey wall, a white shirt); keep the scene's motivated color (the amber flame is not a cast to remove).
- Balance, within a scene: every shot of one moment matches the master shot's exposure, contrast and skin tone. Generated takes from separate generations drift most here; shots from one multi-shot generation drift least.
- Match, across scenes and generations: same time of day looks the same; a deliberate change (night falls) changes on purpose.
- Look, last and once: the style bible's `look` (contrast curve, color split, grain, saturation) as one node or LUT over everything, with per-scene trims only.
- Skin: keep skin tones on the vectorscope's skin line in correct and balance; a look may push them off it a little, never to green or grey.
- Record each pass as numbers a script can repeat: ASC CDL (slope, offset, power per channel, plus saturation) or ffmpeg filter values, in `finish/grade.md`.

## Numbers

- ASC CDL: out = (in × slope + offset) ^ power, per R, G, B; saturation applied after (ASC Manual 2022).
- Rec.709 legal range video: black 16, white 235 in 8-bit code values; full range 0-255. Clip nothing important outside legal range on delivery.

## Vocabulary

- primary (whole-image) vs secondary (a qualified color or a window), lift (shadows), gamma (mids), gain (highlights), node, LUT, waveform, vectorscope, skin line.

## Pitfalls

- Fixing a generation's flicker with a grade: flicker varies frame to frame; use a deflicker filter (`deflicker` in ffmpeg) or re-render.
- Pushing an 8-bit, compressed AI clip hard: banding and blocking appear in skies and shadows. Grade gently, add grain last to hide banding.

## Verify

- `finish/grade.md` lists the four passes per scene with their values; a still from each shot of a scene side by side shows matching skin and blacks.
