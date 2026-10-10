---
title: Blockout control
slug: blockout-control
summary: Drive a shot's motion and layout from a rough 3D blockout or phone footage turned into a depth, pose, edge or layout-box video, through a model's control input; references still carry the look.
tags: [sets, blockout, previs, control, depth, pose, 3d]
last_checked: 2026-10-09
sources: ["flick.art, Blender for AI filmmaking, 2026-06", "invideo FAQ, Blender blocking render as camera reference, 2026-10-08", "docs.comfy.org, MiniMax H3 Fun ControlNet tutorial, 2026", "alibaba-pai, MiniMax-H3-Fun-Controlnet-Union-2.0 model card, 2026-09", "RunComfy, H3 Fun Control workflow, 2026"]
volatile_claims: ["which open video models take depth or pose control", "Fun ControlNet Union 2.0 is the H3 control release"]
---

# Blockout control

## Rules

- Use a control video when words keep failing a blocking (crossings, a camera path, a vehicle's line). References carry the look; the control carries geometry and timing.
- Sources, cheapest first:
  1. layout boxes: a coloured box per subject on white, moved over time (ffmpeg drawbox or any editor);
  2. a box blockout in Blender: cubes and mannequins, the planned camera, rendered at the film's size and frame rate as depth (Mist pass) or a grey Workbench pass for edges;
  3. phone footage of someone acting the beat, turned into pose (people) or depth (anything).
- Pick the signal by subject: pose for people only; depth or edges for animals, vehicles, props and sets.
- Render the control at the shot's frame rate and length (longer is trimmed, shorter holds its last frame).
- Pair it with a first frame or references. Control alone gives the right motion with an invented look.
- Strength 0.6 to 1.0 for one control; two controls summed to 1.0 or less (depth 0.3 plus pose 0.4). Stop the control at about 60% of the steps so the model restores texture; lower it if the result looks flat.
- Check the control at start, middle and end against the plan: a grey render is not automatically a depth pass. Say in the prompt that the camera moves, or the model may move the subject instead.

## Numbers

- Strength 0.6-1.0 (one control); end at 0.6 of the steps; guidance unchanged.
- MiniMax H3: Fun ControlNet Union 2.0 (canny, depth, pose, inpainting with a mask), applied as a model patch; works with first frame and references. Wan VACE, LTX control LoRAs and Kling motion control are the alternatives.

## Vocabulary

- blockout, previs, control video, depth pass, pose, layout boxes, model patch.

## Pitfalls

- Pose control on a horse or a car: the pose detector sees nothing. Use depth.
- Control at full strength to the last step: plastic, flat surfaces.
- A camera-move node that only adds prompt words is not camera control.

## Verify

- Three frames of the render beside the same frames of the control: same positions, same timing.
