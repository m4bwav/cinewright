---
title: LTX-2 model card
slug: ltx-2
summary: Lightricks LTX-2.5 open weights (local): joint audio, frames 8n+1, sizes multiple of 32, 24 fps, keyframes, one flowing paragraph, quoted dialogue, hard cuts named in sequence.
tags: [model-card, ltx, lightricks, local, open-weights, audio]
last_checked: 2026-10-03
sources: ["https://huggingface.co/Lightricks/LTX-2.5", "https://docs.ltx.io/open-source-model/usage-guides/prompting-guide", "https://docs.ltx.io/open-source-model/usage-guides/text-to-video", "https://docs.ltx.io/models/ltx-2-5"]
model: ltx2
vendor: Lightricks
version: "2.5"
status: current
volatile_claims: ["LTX-2.5 (2026-07-23) is current; LTX-2.3 and LTX-2 before it", "frames 8n+1, sizes multiple of 32", "local maximum length unverified (hosted API: 20 s)", "camera LoRAs for LTX-2 19B only"]
---

# LTX-2 model card

## Numbers

- `Lightricks/LTX-2.5` (2026-07-23; LTX-2.3 2026-03-04, LTX-2 2026-01-03). LTX-2.x Community License: commercial use free.
- Frames 8n+1 (97 = 4 s at 24 fps); width and height multiples of 32; 24 fps (25, 30 allowed). Base 768x512, upscaled 2x.
- Joint audio. Keyframes by image, frame index and strength; a first-and-last-frame template.
- Hosted API up to 20 s and 4k; the local ceiling is unverified, so cards stop at 20 s.
- The templates add a negative prompt; the card copies it. No cost per take (local).

## Rules

- One flowing paragraph, present tense, 4-8 sentences: shot, scene, action, people, camera, sound; cinewright puts people before their action so identity reads first.
- Camera relative to the subject: "pushes in", "circles around", "static frame".
- Dialogue in quotes with the manner: `She speaks quietly to herself, "He's late."`
- Several shots: one paragraph naming each cut ("A hard cut jumps to ..."), 2-4 shots, sound stated at each cut.

## Pitfalls

- Camera LoRAs fit LTX-2 19B only, not 2.5: write the move in words.

## Verify

- Re-check the version and the local length limit of the checkpoint you run.

## Compile

```json
{"model_id": "LTX-2.5", "durations_s": [1, 20], "frames": {"fps": 24, "step": 8, "offset": 1}, "aspect_ratios": ["16:9", "9:16", "1:1"], "resolutions": ["480p", "720p", "1080p"], "size_multiple": 32, "max_words": 200, "order": ["camera", "context", "subject", "action", "light", "style", "audio"], "dialogue": "{name} says{tone_clause}, \"{line}\"", "audio": "{sound}", "timestamp": "", "timestamp_next": "A hard cut jumps to", "sequence_join": " ", "max_reference_images": 0, "negative_prompt": "field", "negative_terms": "pc game, console game, video game, cartoon, childish, ugly", "seed": true, "param_names": {"duration": null, "aspect": null, "resolution": null, "negative": "negative_prompt", "frames": "num_frames", "fps": "frame_rate"}}
```
