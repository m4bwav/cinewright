---
title: Mix and loudness
slug: mix-and-loudness
summary: Mix in a fixed order (dialogue, effects, ambience, music) at 48 kHz, then reach the stated target once on the whole mix: gain and limiter, a linear loudnorm pass, qc loud.
tags: [sound, mix, loudness, loudnorm, true-peak, ffmpeg]
last_checked: 2026-10-04
sources: ["https://ffmpeg.org/ffmpeg-filters.html", "https://tech.ebu.ch/docs/r/r128v4_0.pdf", "Tomlinson Holman, Sound for Film and Television, 3rd ed., 2010"]
---

# Mix and loudness

## Rules

- State the target first (shared vocab loudness-targets; default web: -18 ± 2 LUFS, -2 dBTP).
- Order: set dialogue level and clarity; place hard effects and foley against it; ambience and room tone under it (about 10-15 dB below dialogue); music last, ducked under lines (entry music-spotting). Mix on the locked cut only.
- Resample every source to 48 kHz before mixing; mix at 24-bit.
- Never normalise clips one by one. Reach the target once, on the whole mix:
  1. Measure: `loudnorm` with `print_format=json` gives input I, TP, LRA and threshold.
  2. If the gain needed plus the input true peak exceeds the target peak, add the gain and a limiter first (`volume=...dB,alimiter=limit=0.7:level=disabled`), then measure again.
  3. Second pass with `linear=true` and all four measured values. Without them, or without headroom, loudnorm silently switches to dynamic mode (it compresses and works at 192 kHz, so set `-ar 48000`).
  4. Run `CINE qc loud mix.wav --preset <target>` and again on the delivery file; quote both.
- Loudness range (LRA) for web and phones: about 5-10 LU; wider ranges make quiet lines inaudible on a phone speaker.
- Stems are normalised together with the mix (same gain), never each to the target (entry sound-layers).

## Numbers

- ffmpeg loudnorm defaults: I -24, LRA 7, TP -2; `linear` defaults to true but needs the measured values.
- R128 meter tolerance ±0.2 LU; true-peak meter ±0.3 dB.

## Verify

```
ffmpeg -i premix.wav -af loudnorm=I=-18:TP=-2.5:LRA=11:print_format=json -f null -
ffmpeg -i premix.wav -af "loudnorm=I=-18:TP=-2.5:LRA=11:measured_I=<I>:measured_TP=<TP>:measured_LRA=<LRA>:measured_thresh=<thr>:linear=true" -ar 48000 -c:a pcm_s24le mix.wav
python scripts/cine.py qc loud mix.wav --preset web
```

## Notes

- 2026-10-04, S5 exit check: a generated take at -27.6 LUFS and -10.3 dBTP needed +13.9 dB, which would have put the peak near +3.5 dBTP; gain plus limiter, then a linear pass to -18, measured -17.6 LUFS and -6.3 dBTP. Linear passes can land a few tenths off; re-meter.
