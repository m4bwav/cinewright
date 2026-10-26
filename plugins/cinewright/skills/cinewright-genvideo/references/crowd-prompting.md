---
title: Crowd prompting
slug: crowd-prompting
summary: Prompt crowds in tiers (one hero, a few featured extras, the rest as groups on two or three lanes), bind each reference alone, ban clones, and keep within each model's subject limit.
tags: [genvideo, crowds, battle, references, prompting, extras]
last_checked: 2026-10-25
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
- More than about 5 acting people, or two armies: stage it in 3D (cinewright-movement, entry crowd-blockout) and render once with the blockout's depth as the control at about 0.8 (stop at 60% of the steps) plus one or two reference sheets per side, each named by its telling detail ("some like <Picture 1> (black crest), some like <Picture 2> (red tunic)"). Give each side its own blockout behaviour: a disciplined line in ranks, a horde scattered with staggered starts. Tiling groups (cinewright-finish, entry crowd-multiplication) is for a locked camera.
- Do not build a crowd by adding a few people per pass (masked video inpaint over the last pass). Tested 2026-10-25: four passes held about half of a 10-against-10 cast at about four times the render time; a region mask cannot add people behind people, newcomers crossing the mask edge are cut off, and without a composite the earlier people are redrawn. A masked add is for a few figures in empty space of an approved take ([research](../../../../../ai-docs/research/2026-10-25-layered-character-passes.md)).
- The check: `cards validate` warns CAST-COUNT when the cast plus the numbers written before a people noun pass 5. Run the blockout route without asking when the plan already allows the extra time (an unattended run, a budgeted film); otherwise ask once, with the count and the minutes.

## Numbers

- Open local models: about 4 distinct identities per generation. Seedance references: 1-8 image subjects stable, 1-5 with video or audio references. Kling elements: up to 4 images each.
- Keep 3 to 20 takes per kept crowd shot in the budget.
- 10 against 10, one draft each, same seed (2026-10-25): one prompt with references about 9 and 5-7 seen, the second side late; four masked passes about 5 and 6; a 3D blockout's depth at 0.6 without references 8 and 5 as clones; the blockout at 0.8 with one or two sheets per side about 10 in two ranks and 6-8. No benchmark measures more than 3 subjects (OpenS2V-Eval, MAGREF).

## Pitfalls

- "A massive army" or "thousands of soldiers": clones, merged limbs, sides that swap.
- Combat prompts add dirt and tears that drift between takes; lock wardrobe text in every card.

## Verify

- `CINE qc sheet` of the take: count the featured extras, no repeated face within a frame, groups keep their lane and direction.
