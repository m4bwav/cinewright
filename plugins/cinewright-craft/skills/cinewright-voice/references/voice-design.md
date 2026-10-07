---
title: Designing a new voice
slug: voice-design
summary: From sheet to locked voice: a design prompt, 3-5 candidates on one test line, pick, then lock the reference clip, engine, model, voice id, seed and settings.
tags: [voice, design, tts, elevenlabs, qwen3-tts]
last_checked: 2026-10-07
sources: ["https://github.com/QwenLM/Qwen3-TTS", "https://elevenlabs.io/docs/overview/capabilities/voices", "https://elevenlabs.io/docs/api-reference/text-to-speech/convert"]
---

# Designing a new voice

## Rules

- Design prompt, one paragraph: age and gender, pitch, pace, timbre, accent, energy, recording quality ("dry studio recording, close mic, no music"). Over 250 characters is steadier on ElevenLabs.
- Test line: one sentence of 8-15 s that fits the character and holds a question, a name from `pronounce`, and a number. Same line for every candidate.
- Make 3-5 candidates, play them to the user, keep one. Do not keep two "nearly right" voices.
- Lock immediately, before any film line: save the chosen candidate's audio as `voices/<id>/neutral.wav` with its exact words, and write engine name, model, version, voice id, seed and every setting into voices.json.
- Then generate every line from that reference (clone), never from the design prompt again. Qwen3-TTS documents exactly this: VoiceDesign makes the clip, `create_voice_clone_prompt` turns it into a reusable prompt, `generate_voice_clone` speaks each line.
- Hosted (ElevenLabs): the voice is voice_id + model_id + voice_settings + seed together; changing the model changes the voice.
- Emotion clips: generate the same sentence angry, quiet and loud from the locked reference, keep the ones that still sound like the person.

## Numbers

- ElevenLabs settings default: stability 0.5, similarity_boost 0.75; raise stability for consistency, lower it for more acting.
- Qwen3-TTS clone wants about 3 s or more and the reference's transcript (`ref_text`).

## Pitfalls

- Re-designing per scene: each design call is a new person.
- Seeds are best effort on hosted engines; the reference clip is the real lock.
