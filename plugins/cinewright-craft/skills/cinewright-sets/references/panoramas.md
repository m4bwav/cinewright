---
title: Panoramas for plates
slug: panoramas
summary: Make a 360 equirectangular pano locally (from words with Qwen 360 v2, or around existing plates with Klein 4B ERP outpaint), gate its wrap seam, fix only the strip, crop perspective plates.
tags: [sets, plates, panorama, equirectangular, 360]
last_checked: 2026-11-12
sources: ["huggingface.co/ProGamerGov/qwen-360-diffusion (MIT; r/StableDiffusion 1pltzay)", "huggingface.co/nomadoor/flux-2-klein-4B-360-erp-outpaint-lora (Apache-2.0; r/comfyui 1rip661, u/nomadoor)", "maintainer GPU tests, one 16 GB card, 2026-11-12"]
volatile_claims: ["best open 360 pano model", "LoRA licences"]
---

# Panoramas for plates

## Rules

- Size 2048x1024 (2:1). Smaller 2:1 sizes break the horizon.
- From words: Qwen-Image-2512 (Apache-2.0) + Qwen 360 Diffusion v2 LoRA (ProGamerGov, MIT) at 1.0, prompt starting "equirectangular 360 panorama of". Without the LoRA the base draws an ordinary wide photo.
- Around plates you already have: FLUX.2 Klein 4B base, not distilled, + nomadoor's 4B ERP outpaint LoRA (Apache-2.0) at 0.9. Paste the reference photos at their yaw on a green 2:1 canvas, pass it as the reference latent; the LoRA fills the green. The 9B LoRA sits on non-commercial Klein 9B: never in a sellable project.
- Crop and gate with comfyui-gen `tools/pano.py`: `crop` (yaw, pitch, fov) and `seam` (mean wrap-edge step over mean neighbour step). Ratio under 5 passes.
- Over 5: roll the pano by half its width, refill a ~96 px strip over the old seam, then paste back only that strip.

## Numbers

- Qwen 360 v2: about 260 s and 15.3 GB a pano; seam 2.2-2.7 on 4 prompts against 7.4-9.3 for the base without the LoRA; horizon level 4 of 4.
- Klein 4B ERP: about 180 s and 14 GB; seam 1.65-2.18 before any fix, 0.7-1.4 after a strip refill; pasted references held within 11-16/255 in the re-cropped view.
- Crops at fov 75-90 read as straight-walled photos.

## Pitfalls

- A full refill pass regenerates the whole pano and drifts the pasted references (20-32/255): composite the strip only.
- A generated pano is an 8-bit picture: a background and a plate source, not an HDR light probe.
