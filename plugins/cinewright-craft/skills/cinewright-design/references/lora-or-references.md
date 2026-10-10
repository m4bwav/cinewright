---
title: LoRA or reference images
slug: lora-or-references
summary: When a trained character, prop or style LoRA beats reference images, which model to train first, a starting recipe and how to test it; video-model LoRAs come last.
tags: [design, lora, training, references, identity, consistency]
last_checked: 2026-10-09
sources: ["kohya-ss musubi-tuner docs/minimax_h3.md, 2026-09-24", "Black Forest Labs, FLUX.2 Klein training docs and HF blog 2026-06-04", "fal, How to train a LoRA for MiniMax H3, 2026-08-10", "note.com/sepiablue, H3 Ref2VA LoRA vs references, 2026-08-16"]
---

# LoRA or reference images

## Rules

- Default to references (turnaround, prop sheet, set plate). One maker's test of a character LoRA against the same model's plain references found them "indistinguishable" in most shots.
- Train a LoRA when the subject recurs: a series, a character in more than 10 to 15 shots, a hero prop across films, text-only shots.
- Train the image model first: a LoRA on the model that makes keyframes and reference views fixes outfit and body once, and the video model animates consistent stills.
- Train on the base checkpoint, run on the distilled one. CFG-distilled video models break under plain LoRA training: use the trainer's adapter, guidance loss or teacher matching.
- Captions: trigger word plus what changes (pose, angle, light, background); the trigger absorbs the fixed look. One costume per LoRA. Drop any image with a wrong detail: a LoRA learns mistakes too.
- Video-model LoRAs come last, for what references cannot carry (a style, a gait, a vehicle's motion); train them from clips, ideally hosted. Test on top of any turbo LoRA; combined strength past about 1.5 can break motion.

## Numbers

- Dataset: 25 to 40 images at 1024 px for a character (5 to 8 face close-ups among them), 15 to 25 for a prop; varied pose, light and background.
- Image LoRA: rank 16 to 32, lr about 1e-4, 1,500 to 2,500 steps, sample every 250; the best is often at 750 to 1,500. About 1 to 3 hours on a 12 to 16 GB consumer GPU for a 4B model.
- Video LoRA from clips: 10 to 200 clips of 3 to 15 s; hosted trainers charge about $0.005 a step (about $10 for 2,000 steps).
- Strength test: 0, 0.6, 0.8, 1.0.

## Vocabulary

- trigger word, rank, base vs distilled, training adapter, overfitting.

## Pitfalls

- Training on a turnaround grid (panels bleed: crop each view); picking the last checkpoint (it locks pose and background); judging by the loss curve, not the samples.

## Verify

- Same seeds, LoRA at 0 / 0.6 / 0.8 / 1.0: face and outfit hold without being listed in the prompt.
- One video shot from the LoRA's reference views against one from the plain views, same seed and prompt; keep the LoRA only if it wins on the qc rubric's identity checks.
