---
title: Crowd blockout
slug: crowd-blockout
summary: Stage an army or crowd in 3D (polywright pw.py crowd), render depth, pose and mask videos, and let the video model paint the look over them; the model never invents the mass.
tags: [movement, battle, crowds, blockout, 3d, control, vace, depth]
last_checked: 2026-10-13
sources: ["https://github.com/ali-vilab/VACE", "https://docs.comfy.org/built-in-nodes/conditioning/video-models/wan-vace-to-video", "https://www.runcomfy.com/comfyui-workflows/blender-to-comfyui-ai-renderer-2-0-workflow-cinematic-video-output", "https://github.com/smixs/visual-skills (CC BY 4.0, ideas only)", "https://www.vp-land.com/stories/house-of-david-season-2-used-253-ai-generated-shots-here-s-how-they-did-it (2025-10-16)"]
---

# Crowd blockout

## Rules

- Use it for any card with more than about 8 figures in motion, a moving camera over a crowd, or two armies meeting. Fewer figures: prompt them (entry hard-subjects).
- Build the crowd in 3D, not in the prompt: `pw.py crowd --out <shot>/blockout --action march|advance|charge|clash|hold --view side|behind|high --preview`, read `sheet.png`, then render the full shot. polywright owns the command; this entry owns the staging.
- Map the card to the blockout: side A is the side that travels frame left to frame right in the battle map (entry battle-scenes); the camera stays on one side of the battle line in every card.
- Drive the model with depth first (`depth.mp4`); add pose only for the front ranks, where limbs are 40 px or taller. Pose skeletons on tiny far figures are noise.
- Start frame: repaint the blockout's first clay frame into an approved still (costume, banner colour per side, light, haze), fix faces and limbs in the still, then generate the video from that still plus the depth video.
- Prompt the look and the camera words, not the head count; the blockout holds count, spacing and direction. Name each group by role ("the red-cloaked spearmen on the left"), never by its blockout colour.
- Keep proxies coarse: a hosted model given a blockout as reference video follows coarse shapes better than detailed ones.
- Camera static or one slow move; the model spends its capacity on bodies.
- Several shots of one battle reuse one saved blockout scene (`--save-blend`) with new cameras, so ranks and set agree between cards.

## Numbers

- Wan: 4n+1 frames (49, 65, 81) at 16 fps, sides divisible by 16 (832x480, 1280x720). MiniMax H3: 24 fps, 17k+5 frames. Pose only above 40 px figure height.
- Control strength (one local model, field lesson 097, 2026-10-13): about 0.6, released at 40% of the steps, keeps layout and timing with varied figures; 0.8 to 60% holds the exact formation but makes soldiers uniform.

## Pitfalls

- A depth range that changes per frame makes the video pulse; pw.py fixes one range per shot.
- Treating the blockout render as final: it is a control signal; judge the painted take with cinewright-qc.

## Verify

- `sheet.png` shows both sides in frame from the first frame, travel in the mapped screen direction, and no figure crossing the lens.
