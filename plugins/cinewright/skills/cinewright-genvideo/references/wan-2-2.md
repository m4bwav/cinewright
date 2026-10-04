---
title: Wan 2.2 model card
slug: wan-2-2
summary: Alibaba Wan 2.2 A14B open weights (local, Apache 2.0): 480p or 720p at fixed sizes, 16 fps, frames 4n+1 (81 = 5 s), silent, style first, Chinese default negative prompt.
tags: [model-card, wan, alibaba, local, open-weights, silent]
last_checked: 2026-10-03
sources: ["https://github.com/Wan-Video/Wan2.2", "https://github.com/Wan-Video/Wan2.2/blob/main/wan/configs/shared_config.py", "https://github.com/Wan-Video/Wan2.2/blob/main/generate.py", "https://github.com/Wan-Video/Wan2.2/blob/main/wan/utils/system_prompt.py"]
model: wan
vendor: Alibaba
version: "2.2"
status: current
volatile_claims: ["A14B: 16 fps, 81 frames default, sizes 1280x720 and 832x480", "no FLF2V or VACE for 2.2 (Wan 2.1 only)", "Wan 2.5 and later hosted only"]
---

# Wan 2.2 model card

## Numbers

- Apache 2.0, 2025-07-28. `Wan2.2-T2V-A14B`, `Wan2.2-I2V-A14B`: 1280x720, 720x1280, 832x480, 480x832; 16 fps; frames 4n+1, 81 by default (5.06 s).
- `Wan2.2-TI2V-5B`: 1280x704 at 24 fps, 121 frames; sizes multiple of 32.
- No audio. First-and-last-frame and VACE exist for Wan 2.1 only. Wan 2.5 and later: hosted, not open.
- Default negative prompt: the Chinese `sample_neg_prompt` in the configs (copied below).
- No cost per take (local).

## Rules

- Style first, then subject, scene and motion; at most four light and camera settings (the vendor's prompt rewriter).
- 60-200 words. One action. Cards over 5 s: split, or render 81 frames and trim.

## Pitfalls

- Past 81 frames motion loops or drifts (untested in cinewright; the vendor default is 81).
- Dialogue and sound are dropped with a warning: record and mix them.

## Verify

- Re-check sizes and fps in the configs of the checkpoint you run.

## Compile

```json
{"model_id": "Wan2.2-T2V-A14B", "durations_s": [2, 5.0625], "frames": {"fps": 16, "step": 4, "offset": 1}, "aspect_ratios": ["16:9", "9:16"], "resolutions": ["480p", "720p"], "sizes": {"480p": {"16:9": "832x480", "9:16": "480x832"}, "720p": {"16:9": "1280x720", "9:16": "720x1280"}}, "max_words": 200, "order": ["style", "subject", "action", "context", "light", "camera"], "dialogue": "", "audio": "", "max_reference_images": 0, "negative_prompt": "field", "negative_terms": "色调艳丽，过曝，静态，细节模糊不清，字幕，风格，作品，画作，画面，静止，整体发灰，最差质量，低质量，JPEG压缩残留，丑陋的，残缺的，多余的手指，画得不好的手部，画得不好的脸部，畸形的，毁容的，形态畸形的肢体，手指融合，静止不动的画面，杂乱的背景，三条腿，背景人很多，倒着走", "seed": true, "param_names": {"duration": null, "aspect": null, "resolution": null, "negative": "negative_prompt", "frames": "frame_num"}}
```
