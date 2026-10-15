---
title: Sets, set references, blocking continuity and LoRAs for video
summary: Research (2026-10-15) on whether a set LoRA earns its place, what video LoRAs are made for in 2026, how makers hold a room and people's positions across cuts, and how to make and check set plates; Gemini's LoRA claims checked; a one-room test on a rapier duel from a novel; what cinewright adopted.
tags: [research, sets, lora, references, blocking, marks, continuity, plates, controlnet, blockout]
date: 2026-10-15
---

# Sets, set references, blocking continuity and LoRAs for video

Questions (the user): is a set LoRA worth training for one short film; what LoRAs are made for now and whether set LoRAs are rising; the newest ways to get a setting right; how to keep a character at the same spot and facing across a cut; how to make reference images of one set; check a Gemini conversation's LoRA claims. Test: one invented set, the throne room of a rapier duel from a novel (90 s film, about 25 cards, every one on this set, at night).

Method: four parallel web passes (video LoRAs; blocking continuity; set reference images; the Gemini claims), each claim labelled tested, vendor, paper or inference, then a local test of the plate and check route. Full notes with every link, and the parts that name the maintainer's hardware, stay in the private sidecar; this note keeps what shipped entries cite.

## Answer: no set LoRA for one film

- Set LoRAs barely exist. A Civitai API census on 2026-10-15 (public API, undercounts; read shares): 0 location LoRAs among 830 for MiniMax H3, 0 among 392 for LTX 2.3, a couple of background effects for Wan 2.2. On image models, single real places are a handful (a train carriage on FLUX.2 Klein 9B, 197 downloads; one swimming pool). Tested census.
- The one reported single-room LoRA (SDXL, Reddit 2026-04-26) "learned details and textures of specific objects very well ... but couldn't connect one angle to another and had no layout consistency". A distilled-model location LoRA distorted limbs (its author). Official Wan LoRA guidance says to vary scenes so a LoRA does not lock onto one, which is the opposite of a set LoRA's goal ([civitai article 14070](https://civitai.com/articles/14070)). Tested anecdotes and vendor.
- No controlled LoRA-against-reference test for a location exists for any model. EntityBench ([arXiv 2605.15199](https://arxiv.org/html/2605.15199), 2026-05) scores cross-shot scene accuracy of research memory and reference systems at 0.12-0.40. Paper.
- What makers do instead (all tested anecdotes, no A/B): one grid image of 20 overlapping room photos as a single H3 reference held a room where the same photos as separate references did not; a 62-photo two-room grid failed ([thread, 2026-10-03](https://www.reddit.com/r/StableDiffusion/comments/1wwyva2/)). One master background, then per-angle plates made from it, then the video model ([thread, 2026-09-20](https://www.reddit.com/r/StableDiffusion/comments/1wlidkx/)). Vendors ship layout and reference adapters, not set LoRAs: LTX-2.5 IC-LoRA Layout-To-Render turns a grey Blender playblast into a shot ([card](https://huggingface.co/Lightricks/LTX-2.5-22b-IC-LoRA-Layout-To-Render), 2026-10-01), IC-LoRA Ingredients takes one sheet with a location panel ([card](https://huggingface.co/Lightricks/LTX-2.5-22b-IC-LoRA-Ingredients), 2026-09-10).
- Cost on a 16 GB consumer card (from the passes; estimates marked): an image-model set LoRA 1,500-2,000 steps, about 1.5-3 h (inference from vendor minimums and field timings); an H3 set LoRA about 3-8 h on stills, 10-25 h on clips (inference), with system RAM the limit: its text encoder pages about 59 GB, so 64 GB is the floor (maker reports).
- Break-even for this film: a 5 s H3 card renders in about 7-8 min on that card, so 3-8 h of training and an A/B equal 25-65 rerolls. A set LoRA pays only if references lose the room on more than about one card in three, and only if it fixes layout, which the one report says it does not. Route: 3D blockout, checked plates, one grid reference, control from the blockout for hard angles.

## What video LoRAs are made for (2026)

- H3's top 100 LoRAs by downloads (census, hand-sorted): about 10 speed (turbo) LoRAs that dominate, 35 style, 10 motion and action, 10 camera, 8 sliders, 5 effects, 1 voice, 0 sets. Hugging Face H3 repos after the checkpoints: character swap, spatial physics, camera motion, 360 orbit, wushu action, combat. Lightricks' own releases are camera, control and utility adapters (dolly, jib, depth, pose, clean plate, relight, day to night, Foley). Tested listing, vendor.
- Motion and camera LoRAs fill what the base model lacks (soft, slow action); characters are mostly carried by references now. Audio-video LoRAs are real but rare (LTX trainer; an ID-LoRA for face and voice; Foley LoRAs).
- Stacking: no measured thresholds. Two papers show quality falling as LoRAs are added (arXiv 2402.16843; 2606.03792, identity down 3-5 points from 2 to 5 LoRAs); total-weight caps of 1.0-1.5 are untested rules of thumb; turbo LoRAs run at 1.0 and users report them hurting reference adherence and audio.

## Gemini's claims

| Claim | Verdict | What is true |
|---|---|---|
| LoRA libraries: loralib, lora-library, Civitai; the first two old | Verified | loralib last commit 2024-12-17; lora-library a 2023 SD collection; Civitai is the hub |
| LoRA moved into PEFT, the backend of most tools | Partly | Diffusers, ltx-trainer and diffusion-pipe use PEFT; ai-toolkit, musubi-tuner and ComfyUI do not |
| Unsloth 2-5x faster; Axolotl; LLaMA-Factory; Kohya_ss | Partly | Unsloth says 2x and 70% less VRAM; the first three are language-model trainers; video LoRAs come from musubi-tuner, ai-toolkit, diffusion-pipe, ltx-trainer |
| 10-50 images per LoRA | Verified as a rule of thumb | guides: 15-30 character, 20-40 object, 30-100 style |
| Video LoRAs rising since LTX and MiniMax became locally trainable | Partly | MiniMax H3 is open (2026-08) and trainable (ai-toolkit 2026-08-03, musubi-tuner 2026-09-16); no count shows a sharp rise; the wave began with HunyuanVideo and Wan |
| A shift to motion LoRAs "because of VRAM"; LoRAs for prop and clothing consistency | Partly, reason wrong | motion and camera LoRAs are common, but character LoRAs train on stills and are the cheap ones; consistency is done by references |
| ID-LoRA learns a subject's look and voice | Partly | [arXiv 2603.10256](https://arxiv.org/abs/2603.10256): one in-context LoRA on LTX-2 trained on about 3,000 clips, given a face and a voice clip at run time; not trained per subject |
| An LTX Foley LoRA | Verified | a community LTX-2.3 Foley LoRA (video 2026-06-29) and an official gated Foley V2A LoRA; neither does speech or music |
| Voice LoRAs on Whisper and Bark; ACE-Step LoRAs on stems | Partly | Whisper only transcribes; no Bark LoRA workflow found; ACE-Step 1.5 LoRAs are real but train on full mixes |
| Set LoRAs "skyrocketing"; 15-20 angles lock a set "flawlessly" | Not found | no documented set LoRA with numbers; the census shows none |
| No cap on chained LoRAs in ComfyUI | Verified | rgthree's loader: "no real limit" |
| 3-5 safe, more than 3-4 ruins, 2-3 for video | Partly | only the direction is backed; the numbers have no source |

## Blocking continuity: marks, not a new model

- Crews: the script supervisor logs where the main actors are at the start and end of each take, screen direction, eyelines, key actions and lens; the overhead is a floor plan with actors, cameras and moves drawn on it. No source records metric positions; heights live in previs tools (Shot Designer, FrameForge). Secondary and vendor.
- Models: world-memory models keep a static room across camera revisits when given camera poses; multi-shot models keep identity and look, not floor positions (HoloCine, MultiShotMaster and others). On cross-shot spatial layout the best scored model reached 0.78 of 1 (PersonaShot, 2026-08), and every model scored 2.8-3.1 of 5 on spatial logic across shots (MuSS, 2026-08). Papers. The only systems that hold positions use explicit layout: FilmAgent's named standing points, CineMaster's 3D boxes rendered to depth. So the gap is a record and a check.
- H3 has no camera-pose input; the way to put its camera at a known spot is a control video rendered from a blockout camera at that spot (Fun ControlNet Union). Vendor docs, inference.
- Prior art for computing screen side from positions: Director's Lens (2011) checks the 180-degree, jump-cut and motion rules on a 3D scene; Blender's `world_to_camera_view` gives screen positions. Paper, vendor.
- Mirror flips fix screen direction but make a right-handed fencer left-handed and mirror the room: reroll with control instead. Inference.

## Set reference images

- No angle-edit model is trained on rooms: the Qwen-Image 2.1 multiple-angles LoRA was trained on 13,328 object and character pairs and scored below its own base on CLIP similarity; FLUX.2 Klein has no angle LoRA; a May 2026 report says Klein turns characters "but not so with the environment". Vendor, practitioner.
- A 360 panorama turns the camera but cannot move it; a master from the doors and a reverse from 30 m away need two panos that will not agree. Inference.
- World models that fit 16 GB give no reverse of an interior (single-image splats stay near the input view); the big ones need 60-80 GB; Marble's Chisel takes a box blockout plus a style prompt (hosted). Vendor, inference.
- A pano-native model made generic rooms that ignored the plan; ray-casting the plan into a scaffold and repainting it worked; naming objects in the style prompt made the model add them where walls were solid (Kovalchuk, HackerNoon, 2026-10-07). Tested anecdote.

## Test: one room, six plates, two checks (2026-10-15)

- Blockout: the set plan as a Blender scene (walls by compass, windows, platform and chair, gallery and stair, niches), about 10 s headless for six cameras; clay (Workbench with cavity), depth and a flat class render per camera.
- Paint: Z-Image Turbo with its Fun ControlNet Union 2.1 lite, 8 steps. Depth at 0.7 and 0.9 washed every plate milky white; Canny of the clay held the plan; at 0.8 the throne at 28 m was pulled close and drawn huge, at 0.95 it kept its planned size. Tested.
- The shared light line named the windows and the fire: the model cut fire-lit windows into the solid east and south walls in 6 of 6 plates of those two views. With the windows and fire named only in the views that hold the west wall, 0 of 6 did. Tested.
- An overhead floor view drew a whole room from plank lines and from the room nouns in the shared line; a text-only texture prompt rendered portrait and turned 90 degrees gave planks along the planned axis; its colour then needed a match to the master's floor. Tested.
- Plate check: the class render gives which third of the frame holds windows, gallery, throne and doors; those become claims; a local vision model answers them twice in opposite orders, a double yes passes, any no is looked at. It caught the window-on-the-wrong-wall plate (no/no) and passed the clean masters; its misses were parts cut by the frame edge. Tested on about 25 plates.
- Marks check: marks per phrase in metres and each card's camera placed from them (square to the pair on side A, or over one shoulder) give screen side, axis side, facing on screen, the wall behind and the 30-degree turn. Fixed plate cameras failed it four ways on the first draft (a side-on camera north of both fighters put the left fighter right; one camera on the line; an overhead with west at frame right flipped the order); placed from the marks, 13 beats, 0 errors. Tested.

## What cinewright adopted

- cinewright-sets: entry blocking-marks (marks in metres, cameras placed from them, the derived checks); set-light: name a window wall's light only in views that hold it; master-plates: the blockout-and-Canny route with its numbers and the one-grid reference; set-check: claims from a class render, asked twice.
- cinewright-design, lora-or-references: no set LoRA for one film, with the census, the failure report and the break-even.
- Not adopted: a marks-check command in the runtime (the prototype is about 10 KB against about 5 KB of runtime budget; the next session trims and ports it); angle-edit and pano routes as rules (none tested on rooms here); any stacking number.

Related: builds on [2026-10-15-fight-planning](2026-10-15-fight-planning.md), [2026-10-13-battle-crowd-compositing](2026-10-13-battle-crowd-compositing.md).
