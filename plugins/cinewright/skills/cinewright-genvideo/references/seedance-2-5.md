---
title: Seedance 2.5 model card
slug: seedance-2-5
summary: ByteDance Seedance 2.5 on BytePlus ModelArk: 4-30 s, 480p-1080p, six aspects, 24 fps, audio, up to 50 refs named @Image 1, Shot 1: lines, no seed or negative field.
tags: [model-card, seedance, bytedance, hosted, audio, multi-shot]
last_checked: 2026-10-03
sources: ["https://docs.byteplus.com/en/docs/modelark/seedance-2-5", "https://docs.byteplus.com/en/docs/modelark/2222480", "https://docs.byteplus.com/en/docs/modelark/2291680", "https://docs.byteplus.com/en/docs/ModelArk/1520757"]
model: seedance
vendor: ByteDance
version: "2.5"
status: current
volatile_claims: ["ID dreamina-seedance-2-5-260628; 2.0 is dreamina-seedance-2-0-260128", "4-30 s, 480p-1080p, 50 refs (30 images)", "seed documented for 1.x only", "list price unverified; 2.0 discounts end 2026-10-07"]
---

# Seedance 2.5 model card

## Numbers

- `dreamina-seedance-2-5-260628` (2.0: `dreamina-seedance-2-0-260128`, 4-15 s, 9 images, 3 videos, 3 audio, up to 4k).
- 4-30 s, or -1 for auto. 480p, 720p, 1080p. 16:9, 4:3, 1:1, 3:4, 9:16, 21:9, `adaptive`. 24 fps. `generate_audio` on by default.
- Up to 50 assets: 30 images, 10 videos, 10 audio (30 s of each). 4-5 advised. No real human faces as uploads.
- First and last frame by `role`; cannot mix with reference roles. No seed on 2.x; no negative field. Prompt up to about 1,000 English words.

## Rules

- Order: subject, action, scene, style, camera or cuts, sound.
- Refs: `Girl @Image 1 pushes the door open` (space before the number); `@Video 1`, `@Audio 1`.
- Shots: `Shot 1:` lines, one camera move each. Precise timestamps are unstable.
- Dialogue in braces, `asks {How did the exam go?}`; sound in angle brackets, `<rain on the glass>`.
- Exclusions as the vendor's constraint sentence at the end.

## Pitfalls

- The API reference says dialogue in double quotes, the prompt guide says braces: the card follows the guide. Check the first take.

## Verify

- Re-check the volatile claims and the price before a paid render.

## Compile

```json
{"model_id": "dreamina-seedance-2-5-260628", "durations_s": [4, 5, 6, 7, 8, 10, 12, 15, 20, 25, 30], "aspect_ratios": ["16:9", "4:3", "1:1", "3:4", "9:16", "21:9"], "resolutions": ["480p", "720p", "1080p"], "max_words": 1000, "order": ["subject", "action", "context", "light", "style", "camera", "audio"], "dialogue": "{name} says{tone_clause} {{{line}}}", "audio": "<{sound}>", "timestamp": "Shot {n}:", "max_reference_images": 30, "ref_tag": "@Image {n}", "negative_prompt": "inline", "negative_terms": "Avoid generating any text, subtitles or watermark.", "seed": false, "param_names": {"duration": "duration", "aspect": "ratio", "refs": "reference_images"}}
```
