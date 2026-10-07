---
title: Coverage angles
slug: coverage-angles
summary: A plate for every wall a camera sees: small moves may come from the master with an angle-edit model, reverses come from their own wall string or a 3D source, never a 180-degree turn of the master.
tags: [sets, coverage, reverse-angle, multi-angle, lora]
last_checked: 2026-10-07
sources: ["https://huggingface.co/fal/Qwen-Image-Edit-2511-Multiple-Angles-LoRA", "https://github.com/jtydhr88/ComfyUI-qwenmultiangle", "https://fal.ai/models/fal-ai/flux-2-lora-gallery/multiple-angles", "https://www.atlabs.ai/blog/master-cinematic-ai-video-how-to-control-camera-angles-consistency-with-nano-banana-pro", "Set field test, 2026-10-07"]
volatile_claims: ["Qwen-Image-Edit-2511 Multiple-Angles LoRA parameters", "over-the-shoulder is a weak point of image-edit angle changes"]
---

# Coverage angles

## Rules

- Plan coverage from the plan's coverage map: one plate per wall a camera faces, plus inserts for hero dressing seen close.
- Small moves (a turn up to about 45 degrees, a push-in, a tilt) can come from the master with an image-edit angle model. It keeps materials and light because it sees them.
- A reverse, or any wall the master does not show, gets its own plate from that wall's string (entry wall-strings), or a render from the 3D source (entry master-plates). An angle-edit model asked for 180 degrees invents the unseen half of the room.
- Keep the scene's axis: the reverse in a dialogue scene is on the same side of the line, so it looks across the room at the far wall, not back through the first camera (cinewright-continuity, entry axis-and-screen-direction).
- Change the angle by at least 30 degrees between cuts at a set, or the cut reads as a jump (cinewright-continuity, entry thirty-degree-rule).
- Regenerate an angle plate from its wall string with the master as a reference where the image model takes one, so materials match.

## Numbers

- Qwen-Image-Edit-2511 Multiple-Angles LoRA: 8 azimuths, elevations -30, 0, 30, 60 degrees, distances x0.6, x1.0, x1.8, strength 0.8-1.0. Trained on renders of subjects; its card does not claim whole rooms.
- Field test: 2 of 2 off-wall shots written as framing words on a whole-room description came back as the establishing view.

## Vocabulary

- coverage, master, reverse, insert, azimuth, elevation, angle plate.

## Pitfalls

- Over-the-shoulder plates from an edit model are a known weak point; make them from the wall string with stand-ins added at the shot stage.
- Rotating the master in text ("the same room seen from behind the desk"): the model keeps the master's composition.
