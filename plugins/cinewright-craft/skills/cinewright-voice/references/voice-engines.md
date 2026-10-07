---
title: Voice engines
slug: voice-engines
summary: Which TTS engine to use for a locked character voice in 2026 (default Qwen3-TTS, hosted ElevenLabs), with licence, reference length and transcript needs per engine.
tags: [voice, tts, engines, cloning, licence]
last_checked: 2026-10-07
sources: ["https://github.com/QwenLM/Qwen3-TTS", "https://github.com/index-tts/index-tts", "https://github.com/resemble-ai/chatterbox", "https://github.com/SWivid/F5-TTS", "https://github.com/FunAudioLLM/CosyVoice", "https://elevenlabs.io/docs/overview/capabilities/voices"]
volatile_claims: ["ElevenLabs newest model is Eleven v4 (2026-09-28)", "Qwen3-TTS is Apache-2.0 with VoiceDesign and clone", "IndexTTS-2.5 is the newest IndexTTS"]
---

# Voice engines

## Rules

- One engine per film. Switching engines mid-film changes the voice even from the same reference.
- Default open engine: Qwen3-TTS (Apache-2.0). It designs a voice from text and clones it; about 4 GB VRAM.
- Default hosted engine: ElevenLabs (Voice Design, instant clone, audio tags, Voice Changer).
- A line that must fit a shot length exactly: IndexTTS-2.5 (`duration_factor` 0.5-2.0).
- Check the licence before a public or paid release; non-commercial weights are marked below.

## Numbers

| engine | licence | reference | transcript | notes |
|---|---|---|---|---|
| Qwen3-TTS 0.6B/1.7B | Apache-2.0 | 3 s+ | yes (x-vector mode without, lower quality) | 10 languages, VoiceDesign |
| IndexTTS-2.5 | bilibili model licence, not OSI | short clip | no | emotion by audio, vector or text |
| Chatterbox Turbo, Multilingual V3 | MIT | about 10 s, same language | no | watermarked; exaggeration, cfg 0.5 |
| CosyVoice3 0.5B | Apache-2.0 | 3-30 s | yes | 9 languages plus dialects |
| F5-TTS v1 | code MIT, weights CC-BY-NC | short clip | transcribed if empty | non-commercial |
| Higgs TTS 3 4B | non-commercial plus creator grant | short clip | yes | 100+ languages |
| VoxCPM2 | not checked | short clip | for full clone | 48 kHz, design and clone |
| ElevenLabs | paid service | instant 1-2 min, professional 30-180 min | no | voice_id + model + settings + seed |
| Kokoro | Apache-2.0 | none | n/a | fixed voices, no cloning |

## Pitfalls

- VibeVoice: pulled 2025-09-05, back with a watermark and an impersonation ban; do not clone with it.
- Multi-speaker engines (Dia2, MOSS-TTSD) generate whole scenes and can swap voices between runs. Lock each voice by its reference, not by a speaker tag.

## Notes

- 2026-10-07: Eleven v4 and v4 Turbo launched 2026-09-28 (secondary source); v3 left alpha 2026-02-02. IndexTTS-2.5 released 2026-08-10. Higgs TTS 3 released 2026-06-04.
