---
title: Voices from video models
slug: video-model-voices
summary: Keeping a voice when the video model speaks the lines (Kling 3 voice binding, prompt-only models), and the replace route: new dialogue, then lip-sync or voice conversion.
tags: [voice, video-model, lip-sync, kling, veo, dubbing]
last_checked: 2026-11-09
sources: ["https://kling.ai/blog/kling-3-subject-binding-character-consistency", "https://github.com/MeiGen-AI/InfiniteTalk", "https://www.alibabacloud.com/blog/602742", "https://elevenlabs.io/docs/capabilities/voice-changer", "ComfyUI-MiniMaxH3Mod README v0.2.6, 2026-11", "r/StableDiffusion 1xnui9u, 2026-11"]
volatile_claims: ["Kling 3.0 binds a voice to an Element from 5-30 s of speech", "Veo 3.1 takes no custom voice input"]
---

# Voices from video models

## Rules

- Prompt-only models (Veo 3.1, MiniMax H3 and most others): the voice comes from the words. Keep the `voice` string verbatim in every shot (compile does this), expect drift, and plan the fix below.
- H3 audio references are not a voice clone (native, or RefMods from ComfyUI-MiniMaxH3Mod, MIT, which save reference latents as files, unmeasured against native refs): a male reference still gave a female voice in the RefMod author's tests. Clone with voicewright and mux.
- Kling 3.0: bind the voice to the character Element from 5-30 s of the locked reference (or a 3-8 s talking video). It is the native route that carries one voice across shots.
- Reference-video models (Wan2.6-R2V, Sora 2 cameos) take look and voice from a video of a consenting person.
- The take's voice drifts but acting and lips are right: convert its dialogue to the reference voice and keep the timing (entry voice-conversion).
- The line or its timing changes: generate it from the locked voice, then lip-sync the picture (InfiniteTalk, MuseTalk 1.5, Kling Lip Sync) or keep the mouth off screen.
- A line you will replace: ask the model for clean dialogue, no music, low ambience; cinewright-sound rebuilds the bed.
- Dubbing an existing clip (single user report, untested here): pull the voice off a noisy track with SAM-Audio Large (it beat MelBandRoFormer there), fit each translated line to the original line's length before TTS (Fish S2 Pro in that report), then lip-sync.

## Pitfalls

- Extending or continuing a clip loses the voice unless speech runs into its last second (Veo).
- A refine or upscale pass (H3 two-stage and similar) can drop the cloned voice: keep the stage-1 audio and mux it back (one maker's report, untested).
- Using one take's voice as the reference for the next compounds drift. Always clone from the locked bank.
