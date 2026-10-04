---
title: Crop to the film's frame
slug: crop-to-frame
summary: When the style bible's frame_aspect differs from the render, crop every shot to it in finishing (centered, or reframed within the crop per shot), with even pixel sizes, before any upscale.
tags: [finish, crop, aspect, frame-aspect, reframe]
last_checked: 2026-10-04
sources: ["https://ffmpeg.org/ffmpeg-filters.html", "https://en.wikipedia.org/wiki/Aspect_ratio_(image)"]
---

# Crop to the film's frame

## Rules

- Read `frame_aspect` and `aspect_ratio` in `bibles/style.json`. Equal or absent: no crop. Different: the render was composed for the crop (cinewright-camera, entry aspect-and-framing) and finishing makes it.
- Wider frame than the render (2.39 from 16:9): keep the full width, crop height. Narrower (1.37 from 16:9): keep the height, crop width.
- Center the crop by default. Reframe a shot (move the crop window up or down, never scale) when heads or the action fall outside it; note the offset per shot in `finish/grade.md`.
- Crop after the grade (the grade sees the whole frame for scopes), before upscaling and before titles.
- Deliver the cropped frame as its own size (for example 1920x804) for web and festivals; letterbox into 16:9 with black bars only when the delivery spec demands a 16:9 file.
- Sizes must be even for H.264 and H.265 4:2:0; round the cropped dimension down to even.

## Numbers

- Cropped height = width / frame_aspect, rounded down to even: 1280x720 → 1280x534 for 2.39; 1920x1080 → 1920x802; 864x480 → 864x360. For 1.85 from 1920x1080: 1920x1036. A delivery spec that names a size wins over the formula.
- How much of a 16:9 render each frame keeps: shared vocab `aspect-ratios`.

## Verify

Centered crop to 2.39 and an optional reframe 40 px up:

```
ffmpeg -i graded.mov -vf "crop=iw:trunc(iw/2.39/2)*2" -c:v libx264 -crf 12 -c:a copy cropped.mov
ffmpeg -i graded.mov -vf "crop=iw:trunc(iw/2.39/2)*2:0:(ih-trunc(iw/2.39/2)*2)/2-40" ...
```

- `ffprobe -v error -select_streams v -show_entries stream=width,height cropped.mov` gives the expected size.
