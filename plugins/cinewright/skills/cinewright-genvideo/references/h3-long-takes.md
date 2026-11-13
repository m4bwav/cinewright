---
title: H3 long takes, long video-to-video and known misreads
slug: h3-long-takes
summary: MiniMax H3 past one clip: one-take shots without cuts, long video-to-video in windows, prompts H3 misreads, a refine pass that drops the cloned voice. Windows, latent chain measured.
tags: [minimax, h3, long-take, video-to-video, prompt-lint, audio, untested]
last_checked: 2026-11-13
sources: ["r/StableDiffusion 1x6jui1, H3-LongTakeNoCuts (MIT) and a GPL last-frame route", "r/StableDiffusion 1x42kt9, H3 Motion Context (GPL) and Clip Stitcher (MIT)", "r/StableDiffusion 1xgcfk3 and 1xp9mfh, H3 temporal windows and spatial tiles node pack (MIT)", "r/StableDiffusion 1xj2omy, Picky prompt linter (GPL, ideas only)", "r/StableDiffusion 1xbobrr, an H3 character LoRA against references", "r/aigamedev 1x8m8ly, seven H3 tricks for game character actions", "r/comfyui 1xbzx5n, SyncTile v5.5 (MIT) + Media IO (Apache-2.0)", "r/StableDiffusion 1wio4eg, two-stage H3, measured 2026-11-12"]
---

# H3 long takes, long video-to-video and known misreads

Single makers' reports, reworded, unless marked measured. GPL sources are ideas only.

## Rules

- Long takes: cut per shot by default; a cut hides each render restarting picture and sound.
- A one-take shot longer than one clip: carry the previous clip's motion latent into the next (H3 Motion Context, GPL node pack; 22 frames, audio 18, match_tail trim). 3 x 260 frames (2026-11-09): join motion spike 1.39/1.56 vs 5.04/5.45 for a last-frame chain, no luma steps, audio carries. Local: `h3_video.py --save-latent/--continue-from`. Last-frame chaining (H3-LongTakeNoCuts, MIT) only for hard cuts.
- End each chained segment on a held still beat unless the shot must keep moving. Measured 2026-11-10, one seed: seam SSIM 0.923 vs 0.812, no audio dropout.
- Either route: re-anchor the background with masked earlier frames, replace audio in post, grade out saturation creep.
- V2V longer than ~150 frames: MiniMaxH3TemporalWindow on model + CLIP, 124/22 (local `h3_video.py --windows 124/22`). Measured 2026-11-09, 413 frames at 864x480: 2048 s vs 3673 s one pass; SSIM first/last 100 frames 0.89/0.53 vs 0.66/0.34; no seams; still drifts in the last third. Spatial tiles only in a low-denoise second stage.
- 4K two-stage (SyncTile v5.5, MIT): stage 1 at 0.5 MP in 124-frame windows, 39 overlap, latent upscale, stage 2 in 1472x896 tiles, sigmas 0.878/0.8/0.6316/0, streamed decode.
- Two-stage long takes (low-res, latent upscale, full-size refine; LBH-123-AI upscaler, Apache-2.0): not adopted. 14% faster than windows, but the face turns into another person. Keep windows 124/22; chain the motion latent when the face matters most.
- Keep a background swap: a guide still every 4-5 s, "in every frame" in the prompt, 24 fps input.
- A refine or upscale pass can drop a cloned voice: mux the stage-1 audio back.
- Face-refine for `face-mush`: crop a steady padded face box, resample at 0.35-0.45 denoise with the bible face ref, feather it back; keep only if identity and sharpness both rise. Measured 2026-11-09 (0.4, backlit 50 px face): +21% sharpness, 311 s per 5.2 s.
- A famous setting or named character pulls the face to the prior; describe, don't name.

## Pitfalls

Known misreads, a pre-render checklist (warnings; thresholds are guesses):

- A `[Shot N]` cut that brings in no new subject or framing gets merged into the shot before it.
- Quality words (4k, masterpiece) do nothing and take words from the action.
- More than about one cut per two seconds, or a shot under about 1.5 s, gets dropped or blurred into its neighbour.
- A shot whose text has no verb of action renders as a still with drift.
- Two or more camera moves in one shot: H3 does one, or a muddle of both.
- Game character actions (stance as first and last frame, on-the-spot motion): pixelwright-animate's model-effects entry.

## Numbers

- Long-chain drift shows from segment 5-6 (last-frame route report); Motion Context untested past 3. Untested: Drift-Control tapered overlap mask (GPL).
- Two-stage vs windows vs chain (2026-11-12, 362 frames, one seed; s, seam spike, ArcFace mean/min): LBH-123 schedule 1214, 1.37, 0.436/0.185; windows 1415, 1.51, 0.519/0.461; latent chain 1034, 1.93, 0.535/0.394. Upscaling a noisy latent: colour noise.
- One H3 character LoRA (single report): 8 stills + crops, 14 clips on 17n+5, rank 16, 3,520 steps, 41 min hosted.
- Tested 2026-11-10 (V2V, 209 frames, one seed): SyncTile blend and carry lose the set in window 2 (SSIM 0.35/0.38); `--windows 124/22` keeps it (0.39). Use windows for V2V; SyncTile only for 4K tiling.

## Verify

- Long take: per-join brightness and saturation step, and a face crop at each join against segment 1.
- Refine pass: listen at the first spoken line before keeping it.
