---
title: Conform sound to a tempo
slug: conform-to-tempo
summary: Put recorded effects or foley on a music cue's tempo with the lightest edit: tempo match, then per-hit warp, then cut. Rubber Band in ffmpeg, stretches 0.75-1.35, quiet edit points, report unheard.
tags: [sound, foley, tempo, time-stretch, rubberband, music]
last_checked: 2026-10-06
sources: ["https://ffmpeg.org/ffmpeg-filters.html#rubberband", "field notes from recorded game sound effects on a 90 BPM grid, 2026-10-04 to 2026-10-06 (practice)"]
---

# Conform sound to a tempo

## Rules

- For effects or foley on a cue's beat (montage, march, machinery under a rhythmic score). Start from a recording: generated audio does not hold a tempo.
- Lightest touch first; processing is heard as damage:
  1. Tempo match: one continuous section re-tempoed uniformly; fit start and ratio so hits fall near the grid. Ratio 1.0 (untouched) is often best.
  2. Warp: each major hit pinned to a beat, each gap stretched alone. Suits continuous texture; sparse clicks over silence come out broken up.
  3. Cut: whole events (attack to tail) placed on beats. Only when no continuous run fits.
- Fit natural spacing against beats, eighths and triplets; take the grid that changes it least. Grace notes ride their main hit.
- Stretch: `rubberband=tempo=R:transients=crisp:detector=percussive:pitchq=quality`, every ratio 0.75-1.35.
- Edit where the recording is already quiet, not by fading through sound; then 10-20 ms anti-click fades. Keep the run-up into the first hit.
- Stereo to mono: check L/R correlation first; near zero, take the channel with more room.
- Match sources by active RMS, not peak; the mix still reaches its target once (entry mix-and-loudness).
- An agent cannot listen: report the sound as unheard until a person has auditioned it against the cue.

## Numbers

- Beat 60/BPM s, eighth 30/BPM, triplet 20/BPM (0.667, 0.333, 0.222 s at 90 BPM).
- One recording needed 16% for beats, 7% for eighths, 0% for triplets.
- Mono average of channels correlated 0.13: ambience about 3 dB down. Level match: -24 dBFS active RMS, peak cap 0.9.

## Pitfalls

- Denoising or splitting a bed from clean hits: heard as noise or a missing sound.

## Verify

- `ffmpeg -hide_banner -filters | grep rubberband` lists the filter; else use the untouched section.
- Print each hit's landing against the grid; the plan row says method, ratio or pins, grid, source, license and "unheard".
