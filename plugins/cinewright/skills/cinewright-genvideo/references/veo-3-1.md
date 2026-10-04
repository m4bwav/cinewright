---
title: Veo 3.1 model card
slug: veo-3-1
summary: Google Veo 3.1 on Vertex: 4/6/8 s, 720p-4k, 16:9 or 9:16, 24 fps, audio, 3 asset refs (8 s), timestamp blocks, $0.40/s; Gemini API previews end 2026-10-22.
tags: [model-card, veo, google, hosted, audio]
last_checked: 2026-10-03
sources: ["https://cloud.google.com/blog/products/ai-machine-learning/ultimate-prompting-guide-for-veo-3-1", "https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/veo/3-1-generate", "https://ai.google.dev/gemini-api/docs/veo", "https://ai.google.dev/gemini-api/docs/deprecations"]
model: veo
vendor: Google
version: "3.1"
status: current
volatile_claims: ["Vertex GA IDs retire 2026-11-17 or later", "Gemini API previews shut down 2026-10-22", "1080p, 4k and refs force 8 s", "3 asset refs", "$0.40/s with audio"]
---

# Veo 3.1 model card

## Numbers

- Vertex GA since 2025-11-17: `veo-3.1-generate-001`, `veo-3.1-fast-generate-001`.
- 4, 6 or 8 s; refs, 1080p and 4k force 8 s. 720p (default), 1080p, 4k. 16:9 or 9:16. 24 fps.
- Prompt cap 1,024 tokens; cinewright warns past 250 words (its own default).
- Up to 3 `asset` refs (one person or product each); no `style` refs.
- First and last frame: `image` plus `lastFrame`. Extend: +7 s per call.
- `seed` uint32: repeatable, not deterministic. $0.40/s with audio ($0.60 at 4k); Fast $0.10-0.30.

## Rules

- Order: cinematography, subject, action, context, style; audio in its own sentences.
- Dialogue: `The detective says: Your story has holes.` (colon, no quotes). Ambience `Ambient noise: ...`, effects `SFX: ...`.
- Several shots in one 8 s generation: `[00:00-00:02] ...` blocks (`compile --sequence`).
- Exclusions go in `negativePrompt` (Vertex) as nouns, never "no X"; in the prompt, describe what is there.

## Pitfalls

- Burnt-in subtitles: no documented fix; colon dialogue and `subtitles, captions` in `negativePrompt` (unverified).
- Extend loses the voice unless speech is in the last second.

## Notes

- 2026-10-03: re-checked. Gemini API default is now `gemini-omni`; Veo keeps extend and last frame. Guides differ on dialogue quotes; the Vertex colon form stays.

## Compile

```json
{"model_id": "veo-3.1-generate-001", "durations_s": [4, 6, 8], "aspect_ratios": ["16:9", "9:16"], "resolutions": ["720p", "1080p", "4k"], "resolution_duration_s": {"1080p": 8, "4k": 8}, "max_words": 250, "order": ["camera", "subject", "action", "context", "light", "style", "audio"], "dialogue": "{name} says{tone_clause}: {line}", "audio": "Ambient noise: {sound}", "timestamp": "[{start}-{end}]", "max_reference_images": 3, "reference_duration_s": 8, "negative_prompt": "field", "negative_terms": "subtitles, captions, on-screen text", "seed": true, "usd_per_s": {"720p": 0.4, "1080p": 0.4, "4k": 0.6}}
```
