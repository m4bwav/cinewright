---
title: Measuring voice consistency
slug: voice-measure
summary: What voice measure and voice check prove (pitch median and range, pace) and what they do not (identity); speaker-embedding similarity per character, and the ear test.
tags: [voice, qc, pitch, speaker-similarity, measure]
last_checked: 2026-10-07
sources: ["https://github.com/BytedanceSpeech/seed-tts-eval", "https://huggingface.co/speechbrain/spkrec-ecapa-voxceleb", "https://arxiv.org/abs/2607.15694", "https://help.acx.com/s/article/acx-audio-submission-requirements"]
---

# Measuring voice consistency

## Rules

- `voice check <project> --character <id> --clip <line> --text "<line>"` compares the line's median pitch with the character's neutral refs (limit `tolerance_st`, default 2 semitones) and its pace (25%). DRIFT fails; UNSURE means the measurement was noisy.
- A gap of 5 semitones or more is another voice (wrong gender or age): regenerate, never fix it in the mix.
- Pitch and pace pass a wrong voice in the same register. Identity needs an ear or a speaker-embedding model.
- Embedding check (optional, Python packages): one model for the whole film (SpeechBrain ECAPA, Resemblyzer or WavLM-SV). Score the refs against each other first for the character's own baseline, then pass a line that scores within it. Thresholds differ per model; a fixed one missed about a third of clones in a 2026 study.
- Measure the line alone: music and effects under it corrupt pitch.
- Same voice, different sound (room, mic): EQ-match to the reference, then reverb, then one room tone under the scene (cinewright-sound).

## Numbers

- Adult median pitch (textbook): men about 85-155 Hz, women about 165-255 Hz.
- ECAPA same speaker: cosine above 0.25 (SpeechBrain default). Seed-TTS-Eval human recordings score about 0.73 SIM.
- Pace: conversational English about 150-160 words a minute; `voice measure` counts pauses inside the line.

## Verify

- A known male and female clip differ by about 12 semitones (89 Hz and 180 Hz in the 2026-10-07 test).
