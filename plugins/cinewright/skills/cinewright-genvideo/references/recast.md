---
title: Recast an existing clip (character swap)
slug: recast
summary: H3 Recast prompt rules for swapping 1-3 people in an existing clip in one pass (one line per person, colour bleed, clip vs reference). Untested; Viggle swap is tested.
tags: [minimax, h3, recast, swap, video-to-video, untested]
last_checked: 2026-11-09
sources: ["r/StableDiffusion 1x9n0dl, H3 Recast (Bambushu, MIT), 2026-11", "Civitai 2027766, BFS character swap LoRA (NRDX)"]
---

# Recast an existing clip (character swap)

Untested here. H3 Recast (Bambushu, MIT) runs Ref2VA with NRDX's BFS character swap LoRA and swaps 1-3 people in one pass, keeping motion, set and the clip's audio. The tested alternative is Viggle Remake `swap` ([viggle-remake](viggle-remake.md)).

## Rules

- Scene reference: one frame of the clip, same framing, every face visible, everyone edited into the new look (any image editor).
- One line per person, left to right, `<who they are now> becomes <new look>`; the filled lines set the person count.
- Everyone in shot needs a line, an unchanged person described as they are, or they get re-dressed.
- Big changes land (age, gender, hair colour, build); subtle ones fall back to the clip. Never give a colour already on that person: it bleeds.
- Motion, hands, lips, accessories and clothes come from the clip; face and body from the reference. Want sunglasses: put them in the reference.
- Caption: the LoRA's trained `body_swap` form (subject_definitions, summary, detailed_description), people placed as left / middle / right of `<Picture 1>`.

## Numbers

- Author's single runs: 16 GB VRAM plus 64 GB RAM (RAM peaks about 62 GB), cu130 PyTorch; 3 people at 1.5 MP, 6 s about 92 min on a 16 GB card, 18 min on a 5090. 20 steps, cfg 1.

## Notes

- Viggle's vendor MCP (untested here): It windows, paints keyframes, renders, checks and stitches long videos; it defaults to diffusers, too big for 16 GB, and needs a custom ComfyUI worker (one user built one, r/StableDiffusion 1xqbon5).
