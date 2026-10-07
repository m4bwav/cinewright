---
title: Reference clips
slug: reference-clips
summary: What makes a reference clip work for cloning (3-30 s, dry, one speaker, exact transcript, neutral first) and how to cut one from a generated take with voice ref.
tags: [voice, reference, cloning, takes, transcript]
last_checked: 2026-10-07
sources: ["https://github.com/QwenLM/Qwen3-TTS", "https://github.com/index-tts/index-tts", "https://elevenlabs.io/docs/overview/capabilities/voices", "https://github.com/diodiogod/TTS-Audio-Suite", "cinewright voice tests, 2026-10-07 (practice)"]
---

# Reference clips

## Rules

- One speaker, dry, no music, effects or reverb under it; the clone copies everything it hears, room and mood included.
- Length 3-30 s of speech per clip (most open engines); ElevenLabs instant clones want 1-2 minutes, more can hurt.
- Exact transcript in the ref's `text`: Qwen3-TTS ICL, CosyVoice3, Higgs and F5 read it; a wrong word becomes a wrong sound.
- Neutral clip first; then one clip per emotion the script needs. Use the emotion clip for that line, the neutral one otherwise.
- From generated takes: choose lines with nothing under them, cut with `voice ref <take> --start S --end E --out voices/<id>/<emotion>.wav --text "<line>"`. It cuts, makes mono, trims silence, levels and resamples (default 24 kHz; use the rate the engine wants).
- Several good takes: keep the best two or three as separate refs; never splice words from different takes into one clip.
- Transcript source: the card's `dialogue.line`, checked against the audio by ear or ASR (Whisper). Do not trust an LLM listening to names.
- Keep the source: `from` names the take, `start_s` and `end_s` the span.

## Numbers

- Engine rates: Qwen3-TTS, Chatterbox, CosyVoice 24 kHz; VoxCPM2 48 kHz output; video model audio often 32 kHz AAC.
- `voice ref` warns outside 3-30 s, and when under 30% of the speech is voiced (music under it).

## Pitfalls

- Measuring or cloning a whole clip with a score under it: pitch read 286 Hz for a man's line in a local test; cut to the line or isolate the voice first (a vocal separator such as Demucs or ElevenLabs Voice Isolator).
- A shouted reference makes every line shout.

## Verify

- `CINE voice measure voices/<id>/neutral.wav --text "<line>"` shows no WARNING lines.
