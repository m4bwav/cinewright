---
title: Qwen3-TTS speed by host (CPU, CUDA, Apple Silicon)
date: 2026-10-10
kind: note
summary: How fast Qwen3-TTS 1.7B VoiceDesign runs on a PC CPU (measured), stock and CUDA-graph NVIDIA GPUs, and Apple Silicon through MLX, so a voice job goes to the host that finishes it soonest.
tags: [research, voice, tts, qwen3-tts, performance, mlx, apple-silicon, cuda]
---

# Qwen3-TTS speed by host (2026-10-10)

Read this before choosing where to run Qwen3-TTS voice design or cloning, or when a voice job seems slow. Speed below is **audio seconds per wall-clock second** (above 1 = faster than real time). Some sources quote RTF the other way round (wall / audio); those are converted. Sureness as in [2026-10-07-voice-consistency.md](2026-10-07-voice-consistency.md): H = primary source read, M = secondary, L = aggregator.

## Numbers

| Host and route | Model | Speed | Source |
|---|---|---|---|
| Maintainer's PC, CPU, stock `qwen_tts`, fp32, no flash-attn | 1.7B VoiceDesign | **0.18x** (49 clips, 320 s audio in 1,805 s; 30-40 s per 6-7 s line; load 9-80 s) | measured 2026-10-08/09 |
| RTX 4060 (Windows), stock | 1.7B | 0.23x | H: faster-qwen3-tts README |
| RTX 4060 (Windows), faster-qwen3-tts CUDA graphs | 1.7B | 1.83x | H: same |
| RTX 4090, stock / CUDA graphs | 1.7B | 0.82x / 4.22x | H: same |
| M2 Max, MLX bf16 (Soniqo Swift) | 1.7B Base | about 1.8x (RTF 0.55, 37 ms per step) | H: soniqo.audio |
| M2 Mac mini, mlx-audio | 1.7B | about 1x (1,000 characters a minute) | M: mybyways blog |

## What follows

- Stock PyTorch is slow everywhere: one decode step is hundreds of small kernel launches, so even a 4090 runs below real time. The measured CPU run (0.18x) is about what a stock RTX 4060 does (0.23x).
- On an NVIDIA card, use faster-qwen3-tts (CUDA graphs, VoiceDesign supported through `generate_voice_design`): 7-10x over stock. Blackwell (RTX 50) needs a cu128 or newer PyTorch build. Untested here; a 5060 Ti should land at or above the 4060's 1.83x.
- On Apple Silicon, use MLX (mlx-audio, or `mlx-community/Qwen3-TTS-12Hz-1.7B-VoiceDesign-*bit`), not PyTorch MPS: about 1-2x depending on the chip, 2-6 GB RAM (5-bit about 2 GB on disk, 5 GB in memory; 8-bit about 6 GB). No published PyTorch MPS numbers were found.
- A busy GPU changes the answer. When the NVIDIA card is rendering video, a Mac running MLX is the fastest free host, about 5-10x the PC's CPU route.
- mlx-audio ignores `split_pattern` for VoiceDesign and CustomVoice (only Base splits long text), so split long text by hand. One film line at a time is unaffected.
- Seeds are not portable between engines or quantizations: the same seed on MLX 5-bit and PyTorch fp32 gives a different voice. Lock a voice by its reference clip and transcript (the cinewright-voice recipe), never by seed alone, and record the engine and quantization with it.

## Sources

- https://github.com/andimarafioti/faster-qwen3-tts (benchmark tables, Windows and VoiceDesign support)
- https://soniqo.audio/guides/speak (M2 Max RTF)
- https://mybyways.com/blog/qwen3-tts-with-mlx-audio-on-macos (M2 mini, split_pattern bug)
- https://github.com/kapi2800/qwen3-tts-apple-silicon (MLX RAM by size, 8-bit VoiceDesign builds)
- https://huggingface.co/PowerBeef02/Qwen3-TTS-12Hz-1.7B-VoiceDesign-4bit (quantized VoiceDesign)
- https://pypi.org/project/faster-qwen3-tts/ (Blackwell PyTorch note, L)
