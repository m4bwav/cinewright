---
title: Luma Ray3.2 model card
slug: luma-ray-3-2
summary: Luma ray-3.2: 5 or 10 s, 360p-1080p, six aspects, HDR and EXR, start and end frames, loop, no audio, about 100 words, present-tense mid-action verbs.
tags: [model-card, luma, ray, hosted, silent, hdr]
last_checked: 2026-10-03
sources: ["https://docs.agents.lumalabs.ai/guides/videos/generation", "https://docs.agents.lumalabs.ai/guides/model", "https://lumalabs.ai/ray", "https://docs.agents.lumalabs.ai/guides/pricing", "https://web.archive.org/web/20260517181538/https://lumalabs.ai/learning-center/articles/luma-video-models-field-guide"]
model: luma
vendor: Luma AI
version: "Ray3.2"
status: current
volatile_claims: ["ray-3.2 is the only Ray3 API model; Ray3 and Ray3.14 have no API ID", "5 s or 10 s, 360p-1080p, no 4k", "no audio", "$0.30 per 5 s at 720p, $1.20 at 1080p, pre-GA"]
---

# Luma Ray3.2 model card

## Numbers

- `ray-3.2` (Luma Agents API, `type: "video"`; edits `"video_edit"`). Legacy Dream Machine API: `ray-2` only.
- `5s` or `10s`; 10 s refuses HDR, keyframes and loop. 360p (draft), 540p, 720p, 1080p. 9:16, 3:4, 1:1, 4:3, 16:9, 21:9.
- `start_frame`, `end_frame` (image or a generation id to extend). HDR at 720p or 1080p; EXR (ACES2065-1) with HDR.
- No audio. No seed or negative prompt documented. Prompt 1-6,000 characters.
- $0.30 per 5 s at 720p, $1.20 at 1080p; HDR 2x, HDR plus EXR 3x (pre-GA prices).

## Rules

- About 100 words, present tense, mid-action verbs: "running", never "begins to run".
- Subject and action first, then a secondary consequence (dust, fabric, reflections), one named camera move, then light.
- Positive only: negatives work against you. Skip empty praise words ("beautiful", "vibrant").
- With keyframes, describe only what changes.

## Pitfalls

- cinewright prompts carry identity, wardrobe and place, so they run past 100 words: the compiler warns; cut context first, never identity.
- Dialogue and sound are dropped with a warning: record and mix them.

## Verify

- Re-check the volatile claims and price before a paid render.

## Compile

```json
{"model_id": "ray-3.2", "durations_s": [5, 10], "aspect_ratios": ["9:16", "3:4", "1:1", "4:3", "16:9", "21:9"], "resolutions": ["360p", "540p", "720p", "1080p"], "max_words": 100, "order": ["subject", "action", "context", "camera", "light", "style"], "dialogue": "", "audio": "", "max_reference_images": 0, "negative_prompt": "none", "seed": false, "param_names": {"aspect": "aspect_ratio", "duration": "duration", "refs": null}, "duration_format": "{d}s", "usd_per_s": {"720p": 0.06, "1080p": 0.24}}
```
