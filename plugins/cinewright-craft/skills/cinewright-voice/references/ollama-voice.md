---
title: Ollama in a voice pipeline
slug: ollama-voice
summary: What a local Ollama model is good for here (drafting sheets, design prompts, delivery tags, respellings, rough transcripts of clips) and what it must not judge.
tags: [voice, ollama, local, llm, transcription]
last_checked: 2026-10-07
sources: ["https://github.com/ollama/ollama/releases", "https://elevenlabs.io/docs/best-practices/prompting", "cinewright voice tests with gemma4 on Ollama 0.40.0 (Windows) and an MLX build, 2026-10-07 (practice)"]
volatile_claims: ["Ollama has no TTS; gemma4 models with the audio capability accept audio input"]
---

# Ollama in a voice pipeline

## Rules

- Ollama makes text, not speech. Use it for drafts you then check: a voice sheet from the character bible, a design prompt from the sheet, delivery tags per line, respellings for `pronounce`.
- Delivery tags (ElevenLabs style `[whispers]`, `[sighs]`): one or two per line at most, and only ones that fit the voice.
- Listening: a model whose `ollama show` lists the `audio` capability (gemma4) takes a WAV as base64 in the `images` list of a `/api/chat` message; 16 kHz mono worked. Use it for a rough transcript and a first description of a take's voice.
- Never let it judge identity, gender or the spelling of names. In the 2026-10-07 test it heard "hallowed halls" as "hollows", once reported two speakers for one, and called a man (99 Hz median pitch) female. Pitch comes from `voice measure`; words come from the script, checked by ear or Whisper.
- With two hosts, ask the larger or better-served model: the same clip got the right speaker count from the slower host.

## Numbers

- A 15 s clip: about 4-11 s per answer once the model is loaded; the first call loads it (48 s seen).

## Pitfalls

- Orpheus GGUF in Ollama emits audio tokens that need an outside SNAC decoder; it is not a plain Ollama route.
- Release notes named gemma4 audio for MLX only, yet a Windows build answered audio on 2026-10-07: check the model's capabilities, not the notes.
