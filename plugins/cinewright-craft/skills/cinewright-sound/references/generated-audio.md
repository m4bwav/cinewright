---
title: Generated audio
slug: generated-audio
summary: Treat a video model's audio as a guide track: resample to 48 kHz, keep usable dialogue, replace or cover its effects and ambience, hide generation seams under room tone.
tags: [sound, ai-video, generated-audio, dialogue, resample]
last_checked: 2026-10-04
sources: ["Tomlinson Holman, Sound for Film and Television, 3rd ed., 2010", "cinewright S2 render, 2026-10-03 (practice)"]
---

# Generated audio

## Rules

- Probe first: `ffprobe -show_streams` gives the codec, sample rate and channels. Generated audio is often AAC at a low rate (32 kHz seen in a local model's output, 2026-10-03); resample to 48 kHz with a good resampler before mixing (`aresample=48000:resampler=soxr` when ffmpeg has soxr, else plain `aresample=48000`).
- Split the model's track by use: dialogue you keep goes to the dialogue track; its effects and ambience are replaced by your own layers or kept low under them.
- Generated dialogue: keep it if lip sync and the line are right; else replace the line with a generated or recorded voice and keep the picture (cinewright-script, entry dialogue-for-generated-voices).
- Seams: each generation has its own noise floor and room. Lay continuous ambience and room tone across the whole scene, crossfade model audio over 2-4 frames at each cut (cinewright-edit, entry j-and-l-cuts).
- Effects in sync: models place impacts loosely. Put hard effects on the frame of contact (synchresis, entry chion-terms).
- Levels: model audio arrives far below delivery level (-29.6 LUFS integrated in the S2 render). Do not normalise each clip; mix, then set the loudness of the whole mix once (entry mix-and-loudness).
- Rights: music a model generates or a library provides needs its terms checked before public release; write the source in `sound/plan.md`.

## Numbers

- Delivery: 48 kHz, 24-bit PCM masters; AAC 48 kHz at 192 kb/s or more for web files only at the end.

## Pitfalls

- Normalising each shot to the target, then joining: the levels jump at every cut and the sum overshoots.
- Mixing at 32 kHz: the top octave is gone and resampling at export adds artifacts.

## Verify

- `ffprobe -v error -select_streams a -show_entries stream=sample_rate,channels mix.wav` reads 48000 and the planned channels.
