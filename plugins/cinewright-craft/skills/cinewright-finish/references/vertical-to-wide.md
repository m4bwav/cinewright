---
title: Vertical to wide (video outpaint)
slug: vertical-to-wide
summary: A 9:16 clip becomes 16:9 by padding the sides black and outpainting them with the LTX-2.3 Outpaint IC-LoRA; the centre passes through, the sides are invented from the prompt.
tags: [finish, outpaint, aspect, vertical, reframe, ltx]
last_checked: 2026-11-12
sources: ["https://huggingface.co/oumoumad/LTX-2.3-22b-IC-LoRA-Outpaint", "https://github.com/Lightricks/LTX-2"]
---

# Vertical to wide (video outpaint)

## Rules

- Wide to vertical needs no model: crop (entry crop-to-frame). Vertical to wide: outpaint, never stretch or blur-fill.
- Route: LTX-2.3 22B distilled with oumoumad/LTX-2.3-22b-IC-LoRA-Outpaint at 1.0, the padded clip as the whole IC guide at frame 0, one distilled stage, cfg 1. comfyui-gen's `ltx23_ic.py` runs it (`pad`, then `run --lora ...Outpaint...:1.0`).
- Pad the vertical clip to the wide frame with black sides, centred. Prompt the whole wide scene (set, light, what stands at the sides), not only the centre; cfg 1 means a negative prompt does nothing.
- Work in 49-frame (2 s at 24 fps) chunks and cut on the clip's own cuts where you can. The sides are new content: check them against the set bible like any generated plate.
- Do it before the grade, so the grade sees the finished frame.
- Licence: the model and LoRA are under the LTX-2 Community License. Read its revenue terms before using them in a film that may be sold.

## Numbers

Tested 2026-11-12 on two 16:9 takes cut to a 9:16 centre (324 of 1024 px) and outpainted back to 1024x576:

- Kept centre against the source: 35.2 and 35.4 dB PSNR (passed through almost untouched). Sides against the real frame: 10-18 dB (invented, not recovered).
- No added flicker; no visible seam at the 9:16 edges; a hard cut inside the clip was followed.
- 70 s per 2 s clip warm, 92 s cold, on a 16 GB card.

## Verify

- Contact sheet of input, output and (when you have one) the true wide frame; look at the 9:16 edges for a seam.
- PSNR of the centre band against the input should stay above about 30 dB: `ffmpeg -i out.mp4 -i guide.mp4 -lavfi "[0]crop=324:576:350:0[a];[1]crop=324:576:350:0[b];[a][b]psnr" -f null -`
