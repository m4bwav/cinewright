---
title: H3 long takes, long video-to-video and known misreads
slug: h3-long-takes
summary: MiniMax H3 past one clip: one-take shots without cuts, long video-to-video in windows, prompts H3 misreads, a refine pass that drops the cloned voice. Windows, latent chain measured.
tags: [minimax, h3, long-take, video-to-video, prompt-lint, audio, untested]
last_checked: 2026-11-10
sources: ["r/StableDiffusion 1x6jui1, H3-LongTakeNoCuts (MIT) and a GPL last-frame route, 2026-11", "r/StableDiffusion 1x42kt9, H3 Motion Context (GPL) and Clip Stitcher (MIT), 2026-11", "r/StableDiffusion 1xgcfk3 and 1xp9mfh, H3 temporal windows and spatial tiles node pack (MIT), 2026-11", "r/StableDiffusion 1xj2omy, Picky prompt linter (GPL, ideas only), 2026-11", "r/StableDiffusion 1xbobrr, an H3 character LoRA against references, 2026-11", "r/aigamedev 1x8m8ly, seven H3 tricks for game character actions, 2026-11", "r/comfyui 1xbzx5n, SyncTile v5.5 (MIT) + Media IO (Apache-2.0), 2026-11"]
---

# H3 long takes, long video-to-video and known misreads

Items are single makers' reports, reworded, unless marked measured. GPL sources are ideas only.

## Rules

- Long takes: cut per shot by default; each render restarts picture and sound, and a cut hides that.
- A one-take shot longer than one clip: carry the previous clip's motion latent into the next (H3 Motion Context, GPL node pack; 22 frames, audio 18, match_tail trim). 3 x 260 frames (2026-11-09): join motion spike 1.39/1.56 vs 5.04/5.45 for a last-frame chain, luma steps gone, audio carries, same GPU (+5%). Local: `h3_video.py --save-latent/--continue-from`. Last-frame chaining (H3-LongTakeNoCuts, MIT) only for hard cuts.
- End each chained segment on a held still beat unless the shot must keep moving. Measured 2026-11-10, one seed: seam SSIM 0.923 vs 0.812, no audio dropout.
- On either route: re-anchor the background with masked frames from earlier shots, replace the audio in post, and grade out saturation creeping up per segment.
- V2V longer than ~150 frames: MiniMaxH3TemporalWindow on model + CLIP, 124/22 (local `h3_video.py --windows 124/22`). Measured 2026-11-09, 413 frames at 864x480: 2048 s vs 3673 s one pass; SSIM first/last 100 frames 0.89/0.53 vs 0.66/0.34; no seams; still drifts in the last third. Spatial tiles only in a low-denoise second stage.
- 4K two-stage (SyncTile v5.5, MIT): stage 1 at 0.5 MP untiled in 124-frame windows with 39 overlap, latent upscale, stage 2 at 1472x896 tiles with sigmas 0.878/0.8/0.6316/0, decode streamed. SyncTile blends each window per call; carry mode passes frames forward.
- Keep a background swap from reverting: a guide still every 4-5 s, "in every frame" in the prompt, input at 24 fps.
- A refine or upscale pass can drop a cloned voice: keep the stage-1 audio and mux it back over the refined picture.
- Face-refine for `face-mush` (a good shot, a smeared face): crop a steady padded box round the face, resample it at 0.35-0.45 denoise with the bible face ref, feather-stitch it back; keep only if identity on the crop and Laplacian sharpness both rise. Measured 2026-11-09 (H3-FaceRefine, 0.4, backlit 50 px face): +21% sharpness, 311 s per 5.2 s; mushy faces only.
- A famous setting or named character pulls the face toward the model's prior; describe, don't name.

## Pitfalls

Known misreads, as a pre-render checklist (warnings, never blockers; the thresholds are guesses):

- A `[Shot N]` cut that brings in no new subject or framing gets merged into the shot before it.
- Quality words (4k, masterpiece) do nothing and take words from the action.
- More than about one cut per two seconds, or a shot under about 1.5 s, gets dropped or blurred into its neighbour.
- A shot whose text has no verb of action renders as a still with drift.
- Two or more camera moves in one shot: H3 does one, or a muddle of both.
- Game character actions (stance as first and last frame, on-the-spot motion): pixelwright-animate's model-effects entry.

## Numbers

- Long-chain drift shows from segment 5-6 (last-frame route report); Motion Context untested past 3 segments. Try next: a tapered overlap mask, the carried prefix fading from pinned to free (post 1wio4eg, Drift-Control, GPL idea; untested).
- One H3 character LoRA (single report): 8 stills plus crops and 14 clips on 17n+5, rank 16, 3,520 steps, 41 min on a hosted datacenter GPU.
- Tested 2026-11-10 (864x480 V2V, 209 frames, 4 steps, one seed): SyncTile blend and carry both lose the set in window 2 (SSIM 0.35/0.38, set props vanish); `--windows 124/22` keeps it to the last frame (0.39). Use windows for V2V; SyncTile only for 4K tiling.

## Verify

- Long take: per-join brightness and saturation step, and a face crop at each join against segment 1.
- Refine pass: listen at the first spoken line before keeping it.
