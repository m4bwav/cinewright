---
title: Gemini Omni Flash model card
slug: gemini-omni
summary: Google gemini-omni-1.1-flash, the Gemini API's default video model since 2026-08: 3-10 s set by the prompt, 360p-4k, 16:9 or 9:16, 24 fps, audio, image refs as tags, no seed.
tags: [model-card, gemini, omni, google, hosted, audio]
last_checked: 2026-10-03
sources: ["https://ai.google.dev/gemini-api/docs/omni", "https://ai.google.dev/gemini-api/docs/models/gemini-omni-flash", "https://ai.google.dev/gemini-api/docs/video", "https://ai.google.dev/gemini-api/docs/pricing"]
model: omni
vendor: Google
version: "1.1 Flash"
status: current
volatile_claims: ["stable on the Gemini API, preview on Vertex (gemini-omni-1.1-flash-preview)", "3-10 s, no duration parameter", "$17.50 per 1M output tokens (about $0.10/s at 720p)", "no seed, no negative prompt"]
---

# Gemini Omni Flash model card

## Numbers

- `gemini-omni-1.1-flash`, stable on the Gemini API since 2026-08-27 (Interactions API, `POST /v1beta/interactions`). Vertex: `gemini-omni-1.1-flash-preview` only.
- 3-10 s; no duration parameter, length follows the prompt. Extend +10 s, 40 s total.
- 360p, 720p (default), 1080p and 4k (upscaled). 16:9 or 9:16. 24 fps. Audio always.
- Image refs as `<IMAGE_REF_0>` tags (the guide shows 6; no stated cap); up to 3 video refs of 3 s; `<FIRST_FRAME>`, `<LAST_FRAME>`. No audio refs, no seed, no negative prompt.
- About $0.034/s at 360p, $0.10 at 720p, $0.15 at 1080p, $0.30 at 4k.

## Rules

- It cuts between shots by default: one shot starts `In a single continuous shot.` (compiler does it).
- Several shots: unpadded timecodes `[0-3s] ...` (`compile --sequence`).
- Sound: `Sound design: ...`. Exclusions as plain sentences, never a field.
- Edits: short prompt plus `Keep everything else the same.`

## Pitfalls

- Dialogue syntax is not in Google's guide (unverified): the compiler writes `Name says: "line"`. Check the first take for a burnt-in caption.
- No seed: every reroll is a new take; keep the one you like.

## Verify

- Re-check the volatile claims; the Veo card covers extend and last frame.

## Compile

```json
{"model_id": "gemini-omni-1.1-flash", "durations_s": [3, 4, 5, 6, 7, 8, 9, 10], "aspect_ratios": ["16:9", "9:16"], "resolutions": ["360p", "720p", "1080p", "4k"], "max_words": 250, "order": ["camera", "subject", "action", "context", "light", "style", "audio"], "dialogue": "{name} says{tone_clause}: \"{line}\"", "audio": "Sound design: {sound}", "timestamp": "[{start_s}-{end_s}s]", "single_shot": "In a single continuous shot.", "max_reference_images": 6, "ref_tag": "<IMAGE_REF_{n0}>", "negative_prompt": "none", "seed": false, "param_names": {"duration": null, "aspect": "aspect_ratio", "refs": "references"}, "usd_per_s": {"360p": 0.034, "720p": 0.1, "1080p": 0.15, "4k": 0.3}}
```
