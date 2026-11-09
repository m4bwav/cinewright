---
title: H3 long takes, long video-to-video and known misreads
slug: h3-long-takes
summary: MiniMax H3 past one clip: one-take shots without cuts, long video-to-video in windows, prompts H3 misreads, a refine pass that drops the cloned voice. Community reports, untested.
tags: [minimax, h3, long-take, video-to-video, prompt-lint, audio, untested]
last_checked: 2026-11-09
sources: ["r/StableDiffusion 1x6jui1, H3-LongTakeNoCuts (MIT) and a GPL last-frame route, 2026-11", "r/StableDiffusion 1x42kt9, H3 Motion Context (GPL) and Clip Stitcher (MIT), 2026-11", "r/StableDiffusion 1xgcfk3 and 1xp9mfh, H3 temporal windows and spatial tiles node pack (MIT), 2026-11", "r/StableDiffusion 1xj2omy, Picky prompt linter (GPL, ideas only), 2026-11", "r/StableDiffusion 1xbobrr, an H3 character LoRA against references, 2026-11", "r/aigamedev 1x8m8ly, seven H3 tricks for game character actions, 2026-11"]
---

# H3 long takes, long video-to-video and known misreads

Every item here is a single maker's report, reworded; none has been rendered here yet. GPL sources are ideas only.

## Rules

- Long takes: cut per shot stays the default. Each render restarts picture and sound, and a cut hides that.
- A one-take shot longer than one clip, two routes. (a) Chain clips on the last frame, then a refine pass at 0.5-0.6 denoise with a masked by-frame blend across each join (H3-LongTakeNoCuts, MIT). (b) Carry the previous clip's motion latent into the next instead of a still (H3 Motion Context, GPL node pack, plus the MIT Clip Stitcher for the joins); motion and sound carry across the seam. Pick between them after a side-by-side on the same 30 s take.
- On either route: re-anchor the background with masked frames from earlier shots, replace the audio in post, and grade out the saturation that creeps up segment by segment.
- Long video-to-video (a plate past about 150-190 frames, or past a remake model's 345-frame cap): render overlapping windows on the 17k+5 grid, carry the last frames of each window into the next, crossfade the overlap. Spatial tiles only in a low-denoise second stage.
- A refine or upscale pass can drop a cloned voice: keep the stage-1 audio and mux it back over the refined picture.
- Face-refine for `face-mush` (a good shot, a smeared face): crop a steady padded box round the face, resample it at 0.35-0.45 denoise with the bible face ref, feather-stitch it back; keep only if identity on the crop and Laplacian sharpness both rise.
- A famous setting or a named character in the prompt pulls the face toward the model's prior; describe the place instead of naming it.

## Pitfalls

Known misreads, as a pre-render checklist (warnings, never blockers; the thresholds are guesses):

- A `[Shot N]` cut that brings in no new subject or framing gets merged into the shot before it.
- Quality words (4k, masterpiece, best quality, ultra detailed) do nothing useful and take words from the action.
- More than about one cut per two seconds, or a shot under about 1.5 s, gets dropped or blurred into its neighbour.
- A shot whose text has no verb of action renders as a still with drift.
- Two or more camera moves in one shot: H3 does one, or a muddle of both.
- Game character actions (stance as first and last frame, on-the-spot motion): pixelwright-animate's model-effects entry.

## Numbers

- Drift on long chains shows from segment 5-6 (route a report).
- One H3 character LoRA (single report): 8 stills plus crops and 14 clips on 17n+5, rank 16, 3,520 steps, 41 min on a hosted datacenter GPU.
- Window test plan: a 400+ frame plate at 864x480, one pass against windows of 124 frames with 22 overlap; per-frame SSIM to the plate over time and the seam-frame difference.

## Verify

- Long take: per-join brightness and saturation step, and a face crop at each join against segment 1.
- Refine pass: listen at the first spoken line before keeping it.
