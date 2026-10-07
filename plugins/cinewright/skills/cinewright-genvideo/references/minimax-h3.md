---
title: MiniMax H3 model card
slug: minimax-h3
summary: MiniMax H3, local open weights: 4-15 s, 24 fps, joint audio, labelled fields, [Shot N] cuts, camera as type + amplitude + speed, no negative prompt.
tags: [model-card, minimax, local, audio]
last_checked: 2026-10-03
sources: ["https://huggingface.co/MiniMaxAI/MiniMax-H3", "https://huggingface.co/MiniMaxAI/MiniMax-H3/blob/main/docs/VIDEO_PROMPT_WRITING_GUIDE_base_en.md", "field lessons 011, 014, 015 (local renders, 2026-09)"]
model: minimax-h3
vendor: MiniMax
version: "H3 Base"
status: current
volatile_claims: ["4-15 s at 24 fps", "17k+5 frame grid (field notes)", "license: USA, EU, UK, Korea users apply"]
---

# MiniMax H3 model card

## Numbers

- HF `MiniMaxAI/MiniMax-H3`: `H3-Base-FL2VA` (first, last frame), `H3-Base-Ref2VA` (9 images, 3 videos, 3 audio).
- 4-15 s, 24 fps, joint stereo audio. Short side 768.
- Field notes (check the node tooltip): frames on a 17k+5 grid (209 = 8.7 s); sizes multiples of 32.
- CFG-distilled, so no negative prompt.

## Rules

- Three labelled fields (description, soundscape, music; `N/A` when empty); the compiler writes them.
- Shot 1 opens with the style; later shots `[Shot 2] At 00:05.000, the camera cuts to ...`.
- Camera as a sentence: type, `with small amplitude`, `at slow speed`; omit medium and normal.
- Dialogue: `the baker with a calm voice (S1) says: <d>[English] Hello.</d>`; then `(S2)`. Everyone else in the shot gets `while the lips of ... remain completely closed`.
- A speaker not in the shot: `says in an off-screen voiceover: <d>...</d>`, then the on-screen lips stay closed (the guide's exact phrase). Written as a plain `says`, H3 gave a rival's off-screen shout to the only face in frame (library test, 2026-10-07).
- Names: H3 guesses how to say an invented name; the guide says nothing on pronunciation. `pronounce` in characters.json respells it inside `<d>` only (unverified on H3; test with a 4 s render before a long one).
- Several shots per render: each render restarts picture and sound (field lesson 011).
- Bad opening: new seed, then a guide still at frame 0 (field lessons 014, 015).

## Compile

```json
{"model_id": "H3-Base-FL2VA", "durations_s": [4, 15.1], "frames": {"fps": 24, "step": 17, "offset": 5}, "aspect_ratios": ["16:9", "9:16"], "resolutions": ["480p", "608p", "768p"], "sizes": {"480p": {"16:9": "864x480", "9:16": "480x864"}, "608p": {"16:9": "1056x608", "9:16": "608x1056"}, "768p": {"16:9": "1344x768", "9:16": "768x1344"}}, "max_words": 300, "order": ["style", "camera", "subject", "move", "action", "context", "light", "dialogue"], "prefix": "[Shot 1]", "layout": "integrated_multimodal_description: {main}\n\noverall_soundscape: {sound}\n\nnon_diegetic_music: N/A", "move_style": "sentence", "move_suffix": " with small amplitude at slow speed", "dialogue": "{name}{voice_clause} ({speaker}) says{tone_clause}: <d>[English] {line}</d>{silent_clause}", "dialogue_offscreen": "{name}{voice_clause}, off screen, ({speaker}) says in an off-screen voiceover{tone_clause}: <d>[English] {line}</d>{silent_clause}", "dialogue_silent": " while the lips of {names} remain completely closed", "audio": "{sound}", "timestamp": "", "timestamp_next": "[Shot {n}] At {start_ms}, the camera cuts to", "sequence_head": ["style", "people", "context", "sun"], "sequence_block": ["camera", "move", "staging", "action", "key", "dialogue"], "sequence_join": " ", "max_reference_images": 9, "ref_tag": "<Picture {n}>", "seed": true, "param_names": {"duration": null, "aspect": null, "resolution": null, "refs": "refs", "frames": "length"}}
```
