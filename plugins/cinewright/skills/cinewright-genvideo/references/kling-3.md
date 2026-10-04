---
title: Kling 3.0 model card
slug: kling-3
summary: Kuaishou Kling 3.0 (kling-v3): 3-15 s, 720p-4k, 16:9, 9:16 or 1:1, native audio, multi-shot up to 6, 3 elements, dialogue as Name (tone): line.
tags: [model-card, kling, kuaishou, hosted, audio, multi-shot]
last_checked: 2026-10-03
sources: ["https://kling.ai/quickstart/klingai-video-3-model-user-guide", "https://kling.ai/document-api/guides/capability-map/video", "https://kling.ai/document-api/api/video/3-0-omni/text-to-video", "https://kling.ai/document-api/api/video/3-0-omni/image-to-video"]
model: kling
vendor: Kuaishou
version: "3.0"
status: current
volatile_claims: ["IDs kling-v3, kling-v3-omni, kling-3.0-turbo", "3-15 s whole seconds; 4k on v3 and omni only", "audio off by default in the API", "app price 9 credits/s at 720p with audio; USD API price unverified"]
---

# Kling 3.0 model card

## Numbers

- Released 2026-02-06. `kling-v3`, `kling-v3-omni`, `kling-3.0-turbo` (Turbo: 720p and 1080p, no frames, no elements).
- 3-15 s in whole seconds. 720p, 1080p, 4k. 16:9, 9:16, 1:1. fps unverified.
- Audio: `settings.audio` `native` or `off`, default off: set `native` for dialogue.
- Multi-shot: 1-6 shots of 1 s or more, lengths summing to the total; 512 characters per shot.
- Elements: up to 3, each from 2-4 images or a video (can carry a voice), named `@Name` in the prompt.
- First frame, optional last frame. No seed, no negative field. Prompt 3,072 characters, 2,500 advised.

## Rules

- Order in the guide's examples: setting and ambience, people, camera, then speaker-tagged dialogue.
- Dialogue: `Mom (softly, in a surprised tone): Wow, I didn't expect this.` Tone and language inside the parentheses, colon, no quotes. A voice bound to an element needs no tone.
- Shots: `Shot 1, ... Shot 2, ...`; the settings file carries each shot's length (`multi_shot`).
- Element names must not contain each other (`@Ann` and `@Anna` clash).

## Pitfalls

- Audio default off: a dialogue card rendered with defaults comes back silent.

## Verify

- Re-check the volatile claims and the USD price before a paid render.

## Compile

```json
{"model_id": "kling-v3", "durations_s": [3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15], "aspect_ratios": ["16:9", "9:16", "1:1"], "resolutions": ["720p", "1080p", "4k"], "max_words": 400, "max_chars": 2500, "order": ["context", "subject", "action", "camera", "light", "style", "audio"], "dialogue": "{name}{tone_paren}: {line}", "audio": "{sound}", "timestamp": "Shot {n},", "shot_lengths": "multi_shot", "max_reference_images": 3, "ref_tag": "@{name}", "ref_replaces_name": true, "negative_prompt": "none", "seed": false, "param_names": {"duration": "duration", "aspect": "aspect_ratio", "refs": "elements"}}
```
