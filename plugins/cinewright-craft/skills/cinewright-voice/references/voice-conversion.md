---
title: Voice conversion
slug: voice-conversion
summary: When to convert a take's speech to the locked voice instead of regenerating it (keep acting and timing), with Seed-VC, RVC, Chatterbox VC or ElevenLabs Voice Changer.
tags: [voice, conversion, seed-vc, rvc, speech-to-speech]
last_checked: 2026-10-07
sources: ["https://github.com/Plachtaa/seed-vc", "https://arxiv.org/abs/2411.09943", "https://elevenlabs.io/docs/capabilities/voice-changer", "https://github.com/resemble-ai/chatterbox"]
---

# Voice conversion

## Rules

- Convert when the performance must stay: lip-synced video audio, a good take in the wrong voice, a guide line the user recorded.
- Regenerate (TTS from the locked voice) when the words change or the acting is wrong too.
- The target is the neutral reference clip (or the matching emotion clip), never another converted take.
- Zero-shot default: Seed-VC (1-30 s reference, no training). RVC trains a model per voice and keeps it as a file: worth it for a lead with many lines. Chatterbox ships a VC script. Hosted: ElevenLabs Voice Changer, stability high for consistency; it can remove background noise.
- Isolate the dialogue first if anything plays under it; convert; the sound mix puts the bed back.
- Re-check after converting: `voice check` and a listen. Conversion can smear consonants; keep the original take if the result is worse.

## Pitfalls

- Converting across gender or a large age gap gives artefacts: regenerate instead.
- Converting a whole mixed track gives the music the voice's timbre.
