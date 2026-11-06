---
title: Gemini Omni Flash model card
slug: gemini-omni
summary: Google gemini-omni-1.2-flash, the Gemini API's default video model since 2026-11: 3-15 s, 360p-4k, 16:9 or 9:16, 24 fps, audio, refs described in words, no seed; 1.1 reroutes to it 2026-12-03.
tags: [model-card, gemini, omni, google, hosted, audio]
last_checked: 2026-11-05
sources: ["https://aistudio.google.com/docs/omni", "https://aistudio.google.com/docs/models/gemini-omni-flash", "https://aistudio.google.com/docs/deprecations", "https://aistudio.google.com/docs/pricing", "https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/model-versions"]
model: omni
vendor: Google
version: "1.2 Flash"
status: current
volatile_claims: ["gemini-omni-1.2-flash stable since 2026-11-05; Vertex retirement 2027-11-05 or later", "gemini-omni-1.1-flash reroutes to 1.2 at 1.2 rates from 2026-12-03", "3-15 s through the duration parameter, default 10 s", "$12.00 per 1M video output tokens (about $0.07/s at 720p)", "control tags deprecated", "no seed, no negative prompt field"]
---

# Gemini Omni Flash model card

## Numbers

- `gemini-omni-1.2-flash`, stable since 2026-11-05 on the Gemini API (Interactions API) and listed on Vertex. `gemini-omni-1.1-flash` routes to it from 2026-12-03, at 1.2 rates.
- 3-15 s: `duration` in `response_format`, `"3s"` to `"15s"`, default `"10s"`. First and last frame and each extend turn: 3-10 s. Extended total 30 s.
- 360p, 720p (default), 1080p and 4k (upscaled). 16:9 or 9:16. 24 fps. Audio by default.
- Up to 6 image refs, at most 3 per character for 2 characters. Video refs of 3 s: 3 for a clip up to 10 s, 1 for 11-15 s; new generations only. No audio refs, no seed, no negative prompt field.
- About $0.023/s at 360p, $0.07 at 720p, $0.104 at 1080p, $0.209 at 4k.

## Rules

- It cuts between shots by default: one shot starts `In a single continuous shot.` (compiler does it).
- Several shots: unpadded timecodes `[0-3s] ...` (`compile --sequence`).
- Sound: `Sound design: ...`. Exclusions as plain sentences, never a field.
- Edits: short prompt plus `Keep everything else the same.`
- Refs: `<IMAGE_REF_0>`, `<FIRST_FRAME>` and the other control tags are deprecated; say in words what each input is. The compiler writes `(shown in reference image N)`, its own wording after Google's "the character shown in the reference image".

## Pitfalls

- Dialogue: Google's page says speech "is supported when extending previously generated videos via multi-turn", and gives no line syntax. The compiler's `Name says: "line"` on a new generation is untested and may not speak: for a shot that needs a line, plan an extend turn or pick another model. No voice editing, and no adding lines to an uploaded video where someone talks.
- Extend: each turn counts its timestamps from where the new section starts.
- No seed: every reroll is a new take; keep the one you like.

## Verify

- Re-check the volatile claims; the first paid take should settle the ref wording and the dialogue form.

## Notes

- 2026-11-05: verified against https://aistudio.google.com/docs/omni; moved to 1.2 Flash
- 2026-11-05: verified against https://aistudio.google.com/docs/omni; read the whole page: speech is documented only for multi-turn extends

## Compile

```json
{"model_id": "gemini-omni-1.2-flash", "durations_s": [3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15], "aspect_ratios": ["16:9", "9:16"], "resolutions": ["360p", "720p", "1080p", "4k"], "max_words": 250, "order": ["camera", "subject", "action", "context", "light", "style", "audio"], "dialogue": "{name} says{tone_clause}: \"{line}\"", "audio": "Sound design: {sound}", "timestamp": "[{start_s}-{end_s}s]", "single_shot": "In a single continuous shot.", "max_reference_images": 6, "ref_tag": "(shown in reference image {n})", "negative_prompt": "none", "seed": false, "param_names": {"duration": "duration", "aspect": "aspect_ratio", "refs": "references"}, "duration_format": "{d}s", "usd_per_s": {"360p": 0.023, "720p": 0.07, "1080p": 0.104, "4k": 0.209}}
```
