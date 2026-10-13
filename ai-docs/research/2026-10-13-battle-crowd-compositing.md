---
title: Battle and crowd scenes from separate generations
summary: Deep research (2026-10-13) on making big battles and crowds when video models fail at them; three routes (cut, tile, 3D blockout), the tools for each, and what landed in cinewright, polywright and the private image-generation skill.
tags: [research, battle, crowds, compositing, blockout, vace, alpha, matting]
date: 2026-10-13
---

# Battle and crowd scenes from separate generations

Question: video models fail on battles and crowds. Can separate small scenes be generated and combined into one big battle view? How good are models at joining them? The user's own direction from this session: the Blender route, which takes work off the generation models, is the favourite.

Method: one quick web sweep, then four parallel research agents (local open models and ComfyUI nodes; hosted models and practitioner making-ofs; the 3D blockout route; other agent plugins and skills). Reddit was blocked for every tool. Unverified items are marked.

Related: builds on [crowd-multiplication](../../plugins/cinewright-craft/skills/cinewright-finish/references/crowd-multiplication.md), [battle-scenes](../../plugins/cinewright-craft/skills/cinewright-movement/references/battle-scenes.md); see also [crowd-blockout](../../plugins/cinewright-craft/skills/cinewright-movement/references/crowd-blockout.md), [crowd-prompting](../../plugins/cinewright/skills/cinewright-genvideo/references/crowd-prompting.md).

## Answer

- No model joins separate clips into a battle by itself. The working routes are the old VFX ones with AI making the pieces: cut a battle from many small shots, tile small-group plates into a wide, or stage the mass in 3D and let the model paint over it.
- Professional precedent: House of David season 2 (Amazon, Wonder Project) showed armies of about 100k per side with fewer than 200 extras on set; wide shots mixed real extras with AI crowds, assets were built in Unreal and made photoreal by generative tools, then composited in Nuke or After Effects; AI shots were cut in and out of live action; about 20 generations per shot used (VP Land 2025-10-16; Creative + Tech Orbit 2025-11-20; TheWrap 2025-11-10).
- Generative compositing models exist only as research for now: GenCompositor (ICLR 2026, code and weights out, needs 40 GB+ VRAM, no ComfyUI node) and HarmoVid (CVPR 2026, no code found).

## Route 1: cut (cheapest)

- A scene is 3-8 shots; continuity rides on references and first/last frames; extend compounds drift (ocdevel MLA-26, 2026).
- Cut AI wides against close coverage and cut on impacts and whips; one continuous ambience bed and a sound event on every splice make separate clips one sequence (invideo FAQ, vendor; PJ Ace 2026-05-13).
- Budget 3-20 generations per kept shot.

## Route 2: tile small groups (locked camera)

- Plate: the first frame before anyone enters, or "locked tripod, empty field, no people" (Beeble crowd tutorial 2026-06-25, vendor; Kling 3.0 gave the best crowd motion there).
- Cut-outs: Wan-Alpha generates RGBA video (Wan 2.1 T2V 14B plus an RGBA LoRA and two VAEs, native ComfyUI docs; v2.0 Dec 2025 has no ComfyUI version yet). SAM 3 / 3.1 Multiplex is native in ComfyUI (`SAM3_VideoTrack`, text prompts like `person:40`, shared memory across many objects). MatAnyone 2 (CVPR 2026) for soft edges; BiRefNet per frame flickers; RVM is outdated.
- Masked insert: `WanVaceToVideo` (sides step 16, length 4n+1, control video, control masks, reference image; grey the masked area in the control). Wan 2.1 VACE 14B or 1.3B; Kijai's Wan 2.2 Fun VACE GGUF holds only the VACE blocks.
- Unify: relight or regrade the merged frame, never the layer alone; low-denoise V2V (0.3-0.45) with depth control over the whole composite; Light-A-Video (IC-Light plus a video model) as a community node if light still disagrees.

## Route 3: 3D blockout (the favourite)

- Paid Blender crowd add-ons (Procedural Crowds Pro, iCrowds, Horde) document no scripting API; CrowdMaster is dead. Plain bpy is the agent's route. Free figures: Quaternius animation library (CC0), MPFB (CC0 output).
- Controls: VACE takes depth, pose, flow, grey, scribble, layout; Wan 2.2 Fun Control takes canny, depth, OpenPose, MLSD (81 frames, 16 fps). Depth convention for VACE is documented nowhere; Depth Anything outputs inverse depth, so match that (unverified which works better).
- Pose for small figures is noise (under about 40 px tall a figure covers a few latent cells): depth for everyone, pose for the front ranks only.
- Camera: export the blockout's camera; ViPE, MegaSaM and VGGT estimate cameras from AI clips (MegaSaM's Blender add-on is built for an older CUDA and may not run on the newest cards); Uni3C and ReCamMaster are camera-controlled Wan options.
- Agent-skill rule (smixs visual-skills, CC BY 4.0, idea only): coarse proxies beat detailed ones as driving video; name each primitive by role, not colour; strip gizmos.
- Gap: no public example of a crowd or battle made through VACE or Fun Control from a blockout was found.
- Tested here (2026-10-13): a `pw.py crowd` depth video (240 soldiers, 56 frames) drove MiniMax H3 through Fun ControlNet Union 2.0 on a 16 GB card. Formation, screen direction, camera and the moment the lines meet followed the blockout; 0.8 strength made soldiers uniform, 0.6 released at 40% of the steps kept the layout with more variety. Without control the model drew two blocks from the words alone but met later and looser. Wan VACE is still untested.

## Crowd prompting (any route)

- Tiers: one hero, 1-3 featured extras with set actions, the rest as groups; prompt order setting, hero, extras, groups, camera, exclusions; 2-3 movement lanes, never funnel bodies through one point; stress ladder from 3 people up; score frames and log the first broken one (seedance.tv crowd workflow 2026-09-13).
- One reference per subject with a role and an ignore-list; Seedance stable to about 8 image subjects; open models hold about 4 identities (Phantom); explicit clone ban; a priority line (smixs visual-skills).
- Best-of-2 keyframes judged by a vision model; more adds nothing; ViMax admits its keyframes falter in crowded, contact-rich scenes (HKUDS/ViMax, 2026-07).

## What changed (2026-10-13)

- polywright: `pw.py crowd` (two armies of low-poly soldiers with offset walk cycles; depth, mask, clay and OpenPose passes, videos, camera.json, contact sheet), hub section and references/crowd-blockouts.md. Verified: 240 figures, 81 frames, four passes in 81 s on a CPU with Blender 5.2.1.
- cinewright: new entries crowd-blockout (movement) and crowd-prompting (genvideo); battle-scenes and crowd-multiplication updated.
- The private image-generation skill: a crowd-shot recipe for the local hosts (see its repository).

## Sources

- https://www.vp-land.com/stories/house-of-david-season-2-used-253-ai-generated-shots-here-s-how-they-did-it
- https://creativetechorbit.substack.com/p/the-making-of-house-of-david-how
- https://beeble.ai/blog/canvas-tutorial-crowd-vfx
- https://www.seedance.tv/blog/comfyui-crowd-video-workflow
- https://github.com/smixs/visual-skills
- https://github.com/HKUDS/ViMax
- https://docs.comfy.org/tutorials/video/wan/wan-alpha
- https://docs.comfy.org/tutorials/utility/video-segment-sam3
- https://arxiv.org/abs/2512.11782
- https://docs.comfy.org/built-in-nodes/conditioning/video-models/wan-vace-to-video
- https://docs.comfy.org/tutorials/video/wan/vace
- https://comfy.org/workflows/video_wan2_2_14B_fun_control-67a816af8a73/
- https://github.com/ali-vilab/VACE
- https://www.runcomfy.com/comfyui-workflows/blender-to-comfyui-ai-renderer-2-0-workflow-cinematic-video-output
- https://superhivemarket.com/products/procedural-crowds
- https://quaternius.com/packs/universalanimationlibrary.html
- https://github.com/nv-tlabs/vipe
- https://github.com/TencentARC/GenCompositor
- https://arxiv.org/abs/2605.28811
- https://arxiv.org/abs/2502.08590
- https://ocdevel.com/mlg/mla-26
- https://www.fxguide.com/quicktakes/vfx-in-tvcs-how-to-make-a-crowd/
