---
title: Viggle Remake model card
slug: viggle-remake
summary: Viggle Remake on local MiniMax H3: video-to-video re-shoot from a six-section prompt and painted frames, keeping motion, camera, cuts and sound; swap people or edit objects. Tested on 16 GB.
tags: [model-card, viggle, video-to-video, repair, local, open-weights]
last_checked: 2026-11-05
sources: ["https://huggingface.co/Viggle/Viggle-Remake"]
vendor: Viggle
version: "sha 21665fa7"
status: current
volatile_claims: ["frames 17n+5, 90 to 345", "pack tested by its authors on ComfyUI 0.42.0", "1280x736 at 226 frames aborts on 16 GB per the card; it finished here"]
---

# Viggle Remake model card

A LoRA on MiniMax H3 `fl2va`, not a prompt target: `cine.py compile` does not write its six sections. Write them by hand from an example in the model repo.

## Numbers

Measured 2026-11-04 on a 16 GB consumer GPU, ComfyUI 0.41.3, nvfp4 text encoder; some timings include cold loads. Edit int8 re-rendered on 0.42.0 gave identical pixels.

| File | Size, frames | Time | Peak VRAM | PSNR to published take |
|---|---|---|---|---|
| edit int8 | 832x480, 226 | 743 s | 11.8 GB | 29.65 dB |
| edit Q6_K | 832x480, 226 | 1127 s | 13.8 GB | 29.53 dB |
| edit Q4_K_M | 832x480, 226 | 1239 s | 16.0 GB | 29.13 dB |
| swap Q6_K | 832x480, 226 | 1163 s | 14.5 GB | 20.20 dB |
| edit Q6_K | 832x480, 124 | 456 s | 13.5 GB | |
| edit Q4_K_M, `--reserve-vram 10` | 1280x736, 124 | 1514 s | 12.2 GB | |
| edit Q4_K_M, `--reserve-vram 10` | 1280x736, 226 | 4589 s | 16.0 GB | |

- The published examples are labelled side-by-sides at 1280x368. Compare only the right half, or PSNR is meaningless (21.2 dB whole frame, 29.5 dB cropped). The swap's 20 dB is fast dough and fine detail; its frames match in mascot, action and camera. The vendor's 24.7 dB (bf16) is another measure.
- Seed 1 against seed 0: 35.9 dB, so a new seed changes little.
- `--reserve-vram`: Q6_K at 124 frames with none and with 6 gave identical pixels; none took 1554 s against 456 s, but loaded cold. No `CUDA error` appeared in any run.
- The vendor says 1280x736 at 226 frames aborts on 16 GB. It finished here, clean, in 76 minutes.

## Rules

- Use int8 first: fastest and lowest VRAM here, no worse by PSNR or by eye. int8 and GGUF already contain the LoRA; add none on top.
- `edit` for objects, background, weather, light and style; `swap` for people and characters. Six steps, euler, the ManualSigmas from the shipped workflow for that mode.
- Source at 24 fps, frames 17n+5. A source with both sides multiples of 32 and short edge 480 runs as is (864x480 works); anything else is cover-cropped.
- Prompt sections in order: subject_definitions, summary, retention_analysis, detailed_description, overall_soundscape, non_diegetic_music. Describe the target video, not the edit.
- Paint at the source's size. With cuts, pin one frame per shot: only the shot with the fault needs a painted one.
- A real person's likeness needs that person's consent, and the output is labelled as AI. Weights: MiniMax H3 Community License (name MiniMax H3 in a commercial product's UI, pass on the licence and NOTICE, written authorization above US$20M a year).

## Notes

- **Repair route (tested once).** A rejected film take, three shots, 864x480, 277 frames, where the Official carried a pale bucket instead of a basket. Klein painted frame 115 (best of four seeds); unpainted frames 40 and 200 pinned shots 1 and 3; int8, `edit`, 1248 s. The basket held through the shot, cuts, faces and action matched the source (30.1 dB), and the soundtrack difference was about -39 dB RMS. The film's owner chose this as first try for one wrong prop: the basket looks better, though they put the mistakes later.
- **Fight use: untested.** Recording a performer and re-shooting them for hard beats is inference from the vendor's description; no fight has been rendered.

## Pitfalls

- Asking to remove objects can give replacement instead: buckets on the ground became baskets, not bare sand, because the carried prop's new look spread.
- These render with no warning. A non-matching first reference is stretched into its pin (a square one squeezed and moved the farmhouse). A 30 fps source is taken frame for frame, so 7.5 s plays as 9.4 s with audio cut by seconds; sync not listened to.
- These fail in seconds with a clear message: frames off 17n+5, a pin count that is neither zero nor one per reference, a pin past the end.
- Vendor's known failures, unverified: non-humanoids in long takes, fine-detail artifacts, time drift in unpinned multi-shot clips. Unpinned was clean on one single-shot clip. Plates past ~345 frames: windows, [h3-long-takes](h3-long-takes.md).

## Verify

- Look at frames across every shot. The prop's look and any object the prompt removes need their own check.
