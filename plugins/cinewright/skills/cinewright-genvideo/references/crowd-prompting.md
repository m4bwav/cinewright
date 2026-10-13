---
title: Crowd prompting
slug: crowd-prompting
summary: Prompt crowds in tiers (one hero, a few featured extras, the rest as groups on two or three lanes), bind each reference alone, ban clones, and keep within each model's subject limit.
tags: [genvideo, crowds, battle, references, prompting, extras]
last_checked: 2026-10-13
sources: ["https://www.seedance.tv/blog/comfyui-crowd-video-workflow (2026-09-13)", "https://github.com/smixs/visual-skills (CC BY 4.0, ideas only)", "https://beeble.ai/blog/canvas-tutorial-crowd-vfx (2026-06-25, vendor)", "https://github.com/HKUDS/ViMax", "https://kling.ai/blog/kling-3-subject-binding-character-consistency"]
volatile_claims: ["open models hold about 4 distinct identities (Phantom 4 references)", "Seedance reference images: 1-8 subjects stable", "Kling 3.0 gave the best crowd motion in one vendor test"]
---

# Crowd prompting

## Rules

- Tiers: one hero (the strongest reference), one to three featured extras with a set action each, the rest described as groups with one shared action. Only the hero carries a full identity string.
- Prompt order: setting, hero, featured extras, groups, camera, exclusions.
- Groups move on two or three lanes, each with one direction, speed and depth ("a column marching left to right in the middle distance"). Never route several full bodies through one point: that is where bodies merge.
- Bind each reference image to one subject with a stated role (appearance, motion, scene) and say what to ignore in it; never "images 1-4 are four soldiers". Separate images beat a collage.
- Ban clones in words ("no identical faces, no twins in the background") and give look-alike extras different wardrobe and unsynchronised motion.
- Priority line when the shot is crowded: the subject that must survive, the beats that must happen, where the model may improvise, the final frame.
- Approve a still first (image model plus inpaint for faces and limbs), then image-to-video with conservative motion.
- Climb a stress ladder before the full shot: three people, then a passing extra, then a foreground overlap, then a far group. Note the first frame where a rule breaks, and fix it by spacing or a shorter take, not by rerolling.
- More than about 8 people in motion, or two armies: stage it in 3D (cinewright-movement, entry crowd-blockout) or tile groups (cinewright-finish, entry crowd-multiplication).

## Numbers

- Open local models: about 4 distinct identities per generation. Seedance references: 1-8 image subjects stable, 1-5 with video or audio references. Kling elements: up to 4 images each.
- Keep 3 to 20 takes per kept crowd shot in the budget.

## Pitfalls

- "A massive army" or "thousands of soldiers": clones, merged limbs, sides that swap.
- Combat prompts add dirt and tears that drift between takes; lock wardrobe text in every card.

## Verify

- `CINE qc sheet` of the take: count the featured extras, no repeated face within a frame, groups keep their lane and direction.
