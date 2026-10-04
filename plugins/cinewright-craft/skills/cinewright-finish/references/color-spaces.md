---
title: Color spaces for AI video
slug: color-spaces
summary: AI video arrives display-referred Rec.709 (sometimes tagged sRGB) in 8-bit, so grade it in Rec.709 with gentle moves; scene-referred ACES or log pipelines apply only when camera or CG plates join it.
tags: [finish, color, color-space, aces, rec709, log]
last_checked: 2026-10-04
sources: ["https://docs.acescentral.com/background/about-aces-2/", "https://docs.acescentral.com/encodings/acescct/", "https://www.itu.int/rec/R-REC-BT.1886", "Alexis Van Hurkman, Color Correction Handbook, 2nd ed., 2014"]
---

# Color spaces for AI video

## Rules

- Scene-referred footage keeps the light's ratios from the scene (camera log, raw, ACES); a display transform makes it viewable. Display-referred footage is already baked for a screen (Rec.709, sRGB).
- Generated video is display-referred: an 8-bit Rec.709-like file, often 4:2:0, sometimes tagged with the sRGB transfer (seen 2026-10-04 on a local model's output). Grade it as Rec.709; there is no log to decode and no extra latitude to recover.
- Work in 10-bit or higher intermediates (`-pix_fmt yuv420p10le` or a mezzanine codec) even though the source is 8-bit, so grade steps do not band.
- Mixing in camera or CG plates: bring everything into one working space. With ACES, grade in ACEScct (quasi-log, AP1 primaries) and convert the generated Rec.709 clips in by the inverse output transform; ACES 2 (2025) improved those inverses. Without ACES: convert log plates to Rec.709 with the camera maker's LUT, then grade together.
- Tag what you deliver, and tag it in the picture itself: in ffmpeg 9 `-color_trc` on the output did not replace a source frame's sRGB tag; `setparams=range=tv:colorspace=bt709:color_primaries=bt709:color_trc=bt709` in the filter chain did (entry delivery-color).
- Retagging is not converting: change tags when the data is already that space; convert (zscale, a LUT) when it is not.

## Vocabulary

- scene-referred, display-referred, working space, ACES, ACEScct, ACEScg (linear AP1 for CG), IDT and ODT (input and output transforms; output transforms in ACES 2), log, LUT, bit depth, chroma subsampling.

## Pitfalls

- Applying a log-to-709 LUT to an AI clip: it is already 709; the result is crushed and oversaturated.
- Grading an 8-bit file in 8-bit: banding in skies and shadows.

## Verify

- `ffprobe -v error -select_streams v -show_entries stream=pix_fmt,color_range,color_space,color_transfer,color_primaries clip.mp4` before grading and on the delivery file.
