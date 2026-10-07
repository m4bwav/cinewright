---
title: Consistent character voices for AI video (research for cinewright-voice)
date: 2026-10-07
kind: note
summary: How people keep a character's voice the same across shots in 2026, by hand, with AI engines, with ComfyUI and Ollama, and how to measure it; the evidence behind cinewright-voice.
tags: [research, voice, tts, voice-cloning, comfyui, ollama, consistency]
---

# Consistent character voices (2026-10-07)

Read this when changing cinewright-voice's defaults, refreshing it, or asking why it picks the engines it does. Two research passes (craft and local tooling; engines, video models, law and testing) plus a local test on the maintainer's PC. Sureness: H = primary source read, M = reputable secondary, L = aggregator only. The skill's dated rules live in its `references/`; this note keeps the reasons.

## Practice without AI

- Animation, games and audiobooks keep a voice with a voice sheet (casting fields: age band, gender, pitch, resonance, texture, pace, accent, energy, attitude, a cultural reference point), a pronunciation list (sometimes recorded), and a short reference recording the actor replays before each session (H: GDC Vault "Character Voices" 2010, "Anatomy of Great Voice-Over" 2016; M: ACX narrator advice; CMOS Shop Talk 2019-10-15).
- ACX consistency numbers: RMS -23 to -18 dB, peaks -3 dB or lower, noise floor -60 dB or lower, 1-5 s room tone head and tail (H: help.acx.com audio submission requirements).
- Pickups match by same mic, distance and room. In post: EQ match first, then reverb, then a shared room tone; EQ matching cannot fix a reverb mismatch (M: iZotope Dialogue Match, Production Expert).

## Engines (dates are release dates)

- Qwen3-TTS (2026-01-22, Apache-2.0, 0.6B and 1.7B, 10 languages): VoiceDesign from text, then `create_voice_clone_prompt` on Base makes a reusable prompt, then `generate_voice_clone` for every line. `ref_text` required unless `x_vector_only_mode` (lower quality). About 4 GB VRAM (M). This is the documented design-then-clone recipe the skill adopts as its open default (H: github.com/QwenLM/Qwen3-TTS).
- IndexTTS-2.5 (2026-08-10, bilibili licence, not OSI): duration control 0.5-2.0x for dubbing to shot length, emotion from audio, an 8-value vector or text; timbre and emotion separate; no transcript needed (H).
- Chatterbox Turbo, Nano, Multilingual V3 (MIT): about 10 s reference in the same language; exaggeration and cfg 0.5 default; every output watermarked (Perth) (H).
- F5-TTS v1: code MIT, weights CC-BY-NC; empty ref_text is auto-transcribed (H). CosyVoice3 0.5B (Apache-2.0, needs prompt_text) (H). Higgs TTS 3 4B (2026-06-04, non-commercial plus a creator grant; transcript required) (M). VoxCPM2 (2026-04, 48 kHz, design and two clone modes) (M). Fish S2 open, S2.1 Pro closed (M). Dia2 (Apache-2.0, [S1]/[S2]) (M). OmniVoice (Apache-2.0, 600+ languages) (L). VibeVoice: pulled 2025-09-05, back restricted with watermark; treat as no cloning (M). Kokoro: no cloning.
- ElevenLabs: Eleven v4 and v4 Turbo launched 2026-09-28 (M); v3 out of alpha 2026-02-02 with audio tags (H). A stable voice is voice_id + model_id + voice_settings + seed (seed is best effort). IVC wants 1-2 min (more can hurt); PVC 30-180 min. Voice Changer (speech to speech) keeps timing and acting (H).
- Others: Cartesia (10-60 s; the clone takes the clip's mood), OpenAI custom voices (eligible customers, consent recording), Gemini TTS (30 prebuilt voices), Hume Octave 2, MiniMax Speech (H/M).

## Video models

- Kling 3.0 binds a voice to a character Element from 5-30 s of speech or a 3-8 s talking video (H, 2026-06-26): the one native route that carries a voice across shots.
- Veo 3.1: voice set only by the prompt's description, drifts between clips; Flow "Voice Ingredients" (30 preset voices) is reported but not confirmed by Google (L). Sora 2 cameos carry face and voice (M). Wan2.6-R2V takes a reference video for look and voice (H).
- Common route for everything else: keep the picture, replace the dialogue with the locked voice, then lip-sync (InfiniteTalk, MuseTalk 1.5, Kling Lip Sync) or keep the take's timing with voice conversion (Seed-VC 1-30 s reference zero-shot; ElevenLabs Voice Changer) (H/M).

## Local tooling

- ComfyUI core (0.38.2, tested 2026-10-07) has audio load, save, trim, concat, merge and record nodes but no TTS.
- TTS Audio Suite (diodiogod, v5.9.2, pushed 2026-10-04, licence NOASSERTION): 19 engines including Qwen3-TTS, IndexTTS-2/2.5, Chatterbox, F5, CosyVoice3, Higgs and RVC. "Save Character Voice" writes `models/voices/<name>.wav`, `<name>.reference.txt` (transcript), `<name>.txt`; "Voice Designer" (Qwen3, MOSS) makes a voice from text. Isolates fragile engines; warns about s3tokenizer, NumPy, librosa (H). Other packs and their staleness are in the skill's comfyui entry.
- Ollama: release notes name audio input only for gemma4 on MLX (v0.33.3) (H), but on 2026-10-07 the Windows build 0.40.0 accepted a WAV (base64 in the `images` field of `/api/chat`) for `gemma4:12b` and transcribed it, as did a Mac running `gemma4:12b-mlx`. Results: transcript close but wrong on rare words ("hallowed halls" heard as "hollows"); the Windows run once reported two speakers for one; it called a male voice (measured 99 Hz median) female. So Ollama drafts transcripts and voice notes; it never judges identity. No Ollama TTS; the Orpheus GGUF route needs an outside SNAC decoder (M).

## Measuring a voice

- Speaker-embedding cosine (SIM): WavLM-large SV (Seed-TTS-Eval), SpeechBrain ECAPA (threshold 0.25), Resemblyzer (about 0.75-0.80, M). Thresholds differ per model; a 2026 study found generic encoders missed about 32% of Seed-VC clones at a fixed threshold (arXiv 2607.15694). So: one embedding model, compare each line to the character's own reference baseline.
- Stdlib check built here: YIN pitch on 8 kHz mono with a 35 dB energy gate. On Windows SAPI voices it read 90 Hz (David, male) and 180 Hz (Zira, female), 0.4 s per clip. On generated video audio with music under the dialogue it read 286-343 Hz with a 25-semitone range: music corrupts it, so measure only the cut line or an isolated voice.
- Adult F0 bands: male about 85-155 Hz, female about 165-255 Hz (textbook, U).

## Law and consent

- EU AI Act Art. 50 deepfake disclosure applies from 2026-08-02; marking for systems already on the market by 2026-12-02 (M). NO FAKES Act cleared Senate Judiciary 2026-06-18, not law (M). ELVIS Act (Tennessee) and New York digital-replica law in force. SAG-AFTRA 2026 terms: separate written consent with a specific description of use (M).

## Open questions

- TTS Audio Suite licence (NOASSERTION); VoxCPM2 and Fish S2 licences; Flow Voice Ingredients primary source; Sora 2 API cameo voices; SIM floors across emotional takes; per-engine VRAM.

## Refresh search plan

GitHub API `repos/{diodiogod/TTS-Audio-Suite, QwenLM/Qwen3-TTS, index-tts/index-tts, resemble-ai/chatterbox, Plachtaa/seed-vc}` (pushed_at, releases); `search/repositories?q=comfyui+tts&sort=updated`; ollama releases grep audio; ElevenLabs changelog; kling.ai/blog voice; "Veo voice reference"; NO FAKES House markup; AI Act Art. 50 code of practice; `site:arxiv.org speaker similarity zero-shot TTS`; GDC Vault voice-over; help.acx.com.
