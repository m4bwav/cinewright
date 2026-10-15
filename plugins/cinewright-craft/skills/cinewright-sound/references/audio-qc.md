---
title: Checking generated sound, music and sync
slug: audio-qc
summary: Audio fault vocabulary, lip-sync tolerances, per-stem quality scores, tempo checks for music, every effect needs a visible cause; sync metrics and spectrograms as flags only.
tags: [sound, music, sfx, qc, sync, lip-sync]
last_checked: 2026-10-15
sources: ["MovieLabs QC vocabulary, audio and production lists, https://movielabs.com/md/qcvocabulary/audio/", "ITU-R BT.1359 and EBU R37 lip-sync tolerances (via https://en.wikipedia.org/wiki/Audio-to-video_synchronization)", "Audiobox Aesthetics, arXiv 2502.05139", "What do AV sync metrics measure?, arXiv 2608.25157, 2026-08", "THEval, arXiv 2511.04520", "Seeing isn't Hearing, arXiv 2511.13225", "Beat This!, https://github.com/CPJKU/beat_this", "LTX video-to-audio foley guide, https://docs.ltx.io/open-source-model/usage-guides/video-to-audio-foley"]
volatile_claims: ["sync metric reliability", "Audiobox PQ threshold"]
---

# Checking generated sound, music and sync

## Rules

- Name faults with the MovieLabs words: POP-CLICK-TICK, CLIPPING, DROPOUTS, LEVEL-SHIFT, DOUBLED-AUDIO, ECHO-REVERB, HUMM-BUZZ, TRUNCATED, SYNC-OFFSET, SYNC-DRIFT, EXTRANEOUS-EFFECT.
- Every effect needs a visible cause on screen at its frame; a sound with no cause is a fault, and so is a visible impact with no sound.
- Listen with eyes closed once, then with the picture; mark every place where sound covers a picture fault.
- Score each music cue and effect stem for production quality (Audiobox Aesthetics PQ) and compare takes of one cue; flag a stem far below its siblings.
- Music: check that the tempo holds (beat tracking; drift and dropped beats are common in generated music) and snap cuts to downbeats. Listen to cymbals, reverb tails and "s" sounds for shimmer; a take that starts noisy is regenerated, not repaired.
- Mood fit: rank candidate cues by text-audio similarity (CLAP) to the scene's mood words against a contrasting prompt; relative only.
- Quiet foley (steps, rain, typing) varies by seed: take the loudest of a few. Prompt only actions that are visible, and state "no music, no speech" positively.
- Sync metrics (Synchformer offset) flag shots for a look, never reject: they disagree with each other and have reported 0.9 s on in-sync audio. Lip-sync scores (LSE-C/D) correlate poorly with people.
- Spectrograms read as images show structure (gaps, clipping bands, hum lines, click streaks, a cut tail); never use them for words, emotion or naturalness.
- Join generated audio as PCM, never by stream-copying AAC; measure true peak on the final file.

## Numbers

- Lip sync: audio early is noticed from about 45 ms, late from about 125 ms (ITU-R BT.1359); keep within +40 / -60 ms (EBU R37), about one frame early, one and a half late at 24 fps.
- Sync windows: 4.8 s or more for the offset model.
- AAC stream-copy drift: 118 ms over four segments in one report.

## Pitfalls

- Judging music by one number: quality scores rank takes, they do not say the cue fits.
- Trusting the video model's own effects timing: models place impacts loosely (entry generated-audio).

## Verify

- Every hard effect lands on its frame of contact; the mix passes `qc loud`.

Related: builds on [generated-audio](generated-audio.md); see also [mix-and-loudness](mix-and-loudness.md).
