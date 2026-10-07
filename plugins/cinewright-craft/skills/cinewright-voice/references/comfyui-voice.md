---
title: Voices in ComfyUI
slug: comfyui-voice
summary: ComfyUI has no core TTS; TTS Audio Suite adds 19 engines, a Voice Designer and Save Character Voice files. Install cautions and the saved-voice layout.
tags: [voice, comfyui, tts, custom-nodes, local]
last_checked: 2026-10-07
sources: ["https://github.com/diodiogod/TTS-Audio-Suite", "https://docs.comfy.org/built-in-nodes/LoadAudio.md", "https://github.com/Plachtaa/seed-vc"]
volatile_claims: ["TTS Audio Suite (v5.9.2, pushed 2026-10-04) is the maintained ComfyUI voice pack"]
---

# Voices in ComfyUI

## Rules

- Core ComfyUI (0.38, checked 2026-10-07) has Load, Save, Trim, Concat, Merge and Record Audio but no TTS node. Speech needs a custom node pack.
- Default pack: TTS Audio Suite (diodiogod), from ComfyUI Manager. One set of nodes runs Qwen3-TTS, IndexTTS-2/2.5, Chatterbox, F5, CosyVoice3, Higgs and RVC, with SRT timing for whole scenes.
- Its Voice Designer node makes a voice from a description (Qwen3, MOSS). Its Save Character Voice node writes `models/voices/<name>.wav`, `<name>.reference.txt` (the transcript) and `<name>.txt`. Copy them into `voices/<id>/` and voices.json: the project is the record, not ComfyUI.
- Before installing, ask the user and note how to roll back (a copy of the custom_nodes folder and `pip freeze`). The pack warns about s3tokenizer, NumPy and librosa conflicts; a working video setup matters more than a voice node.
- Save the workflow JSON with its seed beside the clips (`voices/<id>/workflow.json`).
- Queue it through the ComfyUI API like any other job; writing a workflow never authorises a long or paid render.

## Numbers

- Qwen3-TTS about 4 GB VRAM (secondary source). Load one engine at a time on a GPU shared with video models.

## Pitfalls

- Stale packs: AIFSH CosyVoice-ComfyUI (2024), Enemyx VibeVoice (2026-02), snicolast IndexTTS2 (2025-10). Prefer the suite.
- Seed-VC upstream was last pushed 2025-04: it still converts zero-shot from 1-30 s, but expect no fixes.

## Verify

- The saved WAV plays the chosen voice, and `CINE voice measure` on it prints no WARNING line.
