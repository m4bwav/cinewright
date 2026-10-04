---
title: Runway Gen-4.5 model card
slug: runway-gen-4-5
summary: Runway gen4.5: 2-10 s, 720p, 1280:720 or 720:1280 (more ratios from an image), no audio, no refs, seed, 1,000-character prompt, $0.12/s; Aleph edits video.
tags: [model-card, runway, hosted, silent]
last_checked: 2026-10-03
sources: ["https://docs.dev.runwayml.com/api/", "https://docs.dev.runwayml.com/guides/models/", "https://help.runwayml.com/hc/en-us/articles/46974685288467", "https://help.runwayml.com/hc/en-us/articles/47313737321107-Text-to-Video-Prompting-Guide", "https://help.runwayml.com/hc/en-us/articles/48324313115155"]
model: runway
vendor: Runway
version: "Gen-4.5"
status: current
volatile_claims: ["gen4.5 is the flagship (announced 2025-12-01)", "no audio field in the API schema", "1,000-character prompt", "12 credits/s = $0.12/s"]
---

# Runway Gen-4.5 model card

## Numbers

- API `gen4.5` on `/v1/text_to_video` and `/v1/image_to_video` (`promptImage` is the first frame).
- 2-10 s, whole seconds. 720p. Text: `1280:720`, `720:1280`; from an image also `1104:832`, `960:960`, `832:1104`, `1584:672`.
- No audio (none in the schema), no reference images, no negative prompt. Seed 0-4294967295.
- `promptText` at most 1,000 characters (UTF-16 units). $0.12/s; ProRes or PNG +$0.05/s.
- Video-to-video edits: Aleph 2.0 (`aleph2`), its own guide.

## Rules

- Text to video: `[Camera] shot of [subject] [action] in [environment]. [Details]`.
- Image to video: describe the motion only (`The camera ... as the subject ...`); describe looks only for what changes.
- Positive, concrete words ("sharp focus", not "not blurry"). Timing as `[00:00 through 00:02]` or "then".
- One shot: add `Continuous, seamless shot.`; still camera: `The locked-off camera remains perfectly still.`

## Pitfalls

- Over 1,000 characters the API refuses: the compiler warns. Shorten action or context, never the identity string.
- Dialogue and sound are dropped with a warning: record and mix them.

## Verify

- Re-check the volatile claims and price before a paid render.

## Compile

```json
{"model_id": "gen4.5", "durations_s": [2, 3, 4, 5, 6, 7, 8, 9, 10], "aspect_ratios": ["16:9", "9:16"], "resolutions": ["720p"], "max_words": 170, "max_chars": 1000, "order": ["camera", "subject", "action", "context", "light", "style"], "dialogue": "", "audio": "", "timestamp": "[{start} through {end}]", "max_reference_images": 0, "negative_prompt": "none", "seed": true, "param_names": {"duration": "duration", "aspect": "ratio", "resolution": null, "refs": null}, "aspect_values": {"16:9": "1280:720", "9:16": "720:1280"}, "usd_per_s": {"720p": 0.12}}
```
