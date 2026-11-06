# Viggle Remake review (2026-11-04)

Source: https://huggingface.co/Viggle/Viggle-Remake (card, COMFYUI.md, PROMPTING.md). Not rendered here: every figure below is the card's own, and its VRAM table was emulated on B200s.

## What it is

A video-to-video LoRA on MiniMax H3, successor to Viggle-Animate. It re-shoots a clip from a six-section prompt and 1-4 painted frames, keeping motion, camera, timing and soundtrack.

- `swap`: people and characters. `edit`: objects, background, weather, light, style.
- Weights: MiniMax H3 Community License (show "MiniMax H3" in a commercial product's UI, pass on the licence and NOTICE, written authorization above US$20M a year). Code: Apache 2.0.

## Live API check (2026-11-04)

Not gated. Created 2026-10-22, last modified 2026-11-04, sha 21665fa7. ComfyUI-format LoRAs are 3.77 GB each, larger than the card's 2.67 GB for `lora/`. usedStorage is 167.6 GB against the card's 210 GB; recheck sizes with a dry run.

## ComfyUI facts

- Node pack `comfyui/ComfyUI-Viggle-Remake`, tested on ComfyUI 0.42.0. Base is `fl2va`, not `ref2va`.
- Load the LoRA with LoraLoaderBypassModelOnly; the plain loader loses much of it at bf16.
- int8 and GGUF files already contain the LoRA. Do not add one on top.
- 6 steps, euler, ManualSigmas:
  - swap: 1.0, 0.990476, 0.965243, 0.923077, 0.8, 0.631579, 0.0
  - edit: 1.0, 0.983607, 0.96, 0.923077, 0.857143, 0.705882, 0.0
- Source must be 24 fps; the node does not resample. Frames are 17n+5, 90 to 345, recommended up to 294.
- 16 GB, 226 frames: 832x480 on int8 or Q4_K_M/Q6_K with `--reserve-vram 6`. 1280x736 reached only 124 frames (Q4_K_M, `--reserve-vram 10`); 226 aborted.
- Encoders: bf16 51.5 GB, int8 27.1 GB, nvfp4 15.7 GB; quality within noise.
- `CUDA error: invalid argument` on GGUF: raise `--reserve-vram`.

## Prompting facts

- Sections in order: subject_definitions, summary, retention_analysis, detailed_description, overall_soundscape, non_diegetic_music.
- Describe the target video, not the edit. `retention_analysis` is followed literally.
- Paint over a source frame at canvas size or source aspect.
- Pin only with cuts or when composition matters; a pin copies the painted composition at that frame.
- Known failures: non-humanoids in long takes, fine-detail artifacts, time drift in unpinned multi-shot clips.

## Proposed additions (not applied yet)

- cinewright-genvideo: new model card `viggle-remake.md`.
- cinewright-qc or -edit: a repair route for a good-motion take with one wrong element, before re-rolling. Our inference, untested.
- cinewright-movement `fight-previs.md`: recorded performer to Remake as a candidate for hard beats. Our inference, untested.
- cinewright consent rule: real-likeness swaps need the person's consent; label output as AI.
- The local render setup notes: install and 16 GB settings; a smoke test on this PC first.

## Local state checked

RTX 5060 Ti 16 GB. ComfyUI-GGUF is installed. No Viggle LoRA or node pack is installed, and no Viggle GGUF was seen. ComfyUI version not checked.
