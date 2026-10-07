---
title: Master plates
slug: master-plates
summary: One wide establishing plate per set and time of day, made first and passed as a reference in every shot there; a 3D world or 360 pano is the stronger source when reverses matter.
tags: [sets, plates, references, establishing, 3d, panorama]
last_checked: 2026-10-07
sources: ["https://higgsfield.ai/blog/consistent-characters-locations", "https://invideo.io/faq/how-do-you-use-seedance-20-reference-to-video-for/", "https://docs.worldlabs.ai/marble/export/gaussian-splat/index.md", "https://github.com/Tencent-Hunyuan/HY-World-2.0", "https://flick.art/blog/blender-ai-filmmaking", "https://blog.google/innovation-and-ai/technology/ai/veo-3-1-ingredients-to-video/"]
volatile_claims: ["reference counts per model change with releases", "World Labs Marble input and export limits", "HY-World 2.0 is the newest open 3D world model"]
---

# Master plates

## Rules

- Generate the widest plate first and match every closer plate to it. It fixes the geography: where the windows are, which way the light falls, which landmarks show.
- One master per time of day. Day and night versions of a set are two plates, made from the same plan and the same words with only the light line changed.
- Make plates at the renderer's frame (16:9 for most video models), at the image model's native size, never upscaled from a small render. No people, no readable text.
- Pass the set's plate in every shot at that set, alongside the character references. A location left out of one call is reinvented in that clip.
- Name plates `refs/sets/<id>/<id>_<wall-or-view>_<time>.png` and list the passed ones in the location's `refs`.
- When reverses and moves matter more than speed, build a 3D source first and render plates from it:
  1. a box blockout in Blender (plain boxes, a camera, stand-ins) rendered as depth for a depth-guided image model, or
  2. a generated world (World Labs Marble, HY-World 2.0) exported as splats or a mesh, or
  3. a 360 equirectangular pano cropped to perspective views by yaw, pitch and field of view.

## Numbers

- Reference slots per call (2026): Veo 3.1 up to 3; Runway Gen-4 1-3; Kling 3.0 up to 4; MiniMax H3 1-5; Seedance 2.0 up to 9 images. The set plate takes one slot; characters take the rest.
- Marble takes 2-8 photos or one image or pano; exports splats (about 2M or 500k) and a GLB of about 600k triangles.
- One field account: a box blockout as depth landed an angle that took 7-8 tries from image references alone.

## Pitfalls

- Locking a background image raises consistency and lowers angle freedom: a plate pins the view it shows. Make the plate for the view the shot needs.
- A 3D world model invents the parts its input never showed; check it against the plan like any plate.
