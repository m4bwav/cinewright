---
title: Extension and multi-shot model routes
slug: chain-models
summary: Which route carries a scene past one render (latent continuation, Wan VACE extend, multi-shot models) and the licence of each; read, not run.
tags: [continuity, ai-video, seams, multi-shot, extension]
last_checked: 2026-11-19
sources: ["https://github.com/yihao-meng/HoloCine", "https://arxiv.org/abs/2503.10589", "https://github.com/KlingAIResearch/MultiShotMaster", "https://github.com/Kevin-thu/StoryMem", "https://github.com/HVision-NKU/StoryDiffusion", "https://civitai.com/models/1536883", "Maintainer chain-join study 2026-11-19 (sc40 S8, S9, S10, S19, S49, S50)"]
---

# Extension and multi-shot model routes

## Rules

- Up to about 15 s: one render with cuts inside it on the main model. Past that, extend from the last segment, then measure every join (`cine_seam.py` in cinewright-qc).
- MiniMax H3: continue from the saved latent of the previous segment, not from its last frame.
- Wan: VACE extend keeps the last N frames as context and fills the rest; crop and stitch holds the background. Wan 2.1 VACE weights are Apache-2.0; the community workflows were not fetched.
- Keyframes first, then animate each, stays the pipeline for identity across shots: current image models with refs do what StoryDiffusion (Apache-2.0, SDXL era) did with a batch trick.

## Numbers

- HoloCine: a Wan 2.2 14B fine-tune with per-shot window attention; holds identity across cuts for up to about a minute. 14B on 16 GB needs GGUF or fp8; 5B variants exist.

## Pitfalls

- A multi-shot model is its own weights, never an add-on to the model the film is rendered on: switching mid-film changes the look.
- HoloCine's licence is "Other" and StoryMem's is custom: read each before a sold film.

## Notes

- 2026-11-19, read, not run: HoloCine (licence "Other") descends from Long Context Tuning (arXiv 2503.10589, no code). MultiShotMaster (KlingAIResearch, Apache-2.0, Wan 2.1 1.3B and 14B) makes several shots per generation with subject and scene refs. StoryMem (custom licence) keeps a keyframe memory of chosen frames from all earlier shots; refs per segment approximate it.
