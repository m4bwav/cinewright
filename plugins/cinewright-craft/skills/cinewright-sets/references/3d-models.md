---
title: 3D models for film and AI video
slug: 3d-models
summary: What 3D is for in a film (previs, techvis, control) and how much to build: only what the cameras see, detail by shot size, grey not textured, real scale and lens; polywright builds it.
tags: [sets, 3d, previs, techvis, blockout, lod, splats, style, polywright]
last_checked: 2026-10-17
sources: ["https://thethirdfloorinc.com/?p=76", "https://caveacademy.com/wiki/post-production-assets/modelling/model-lods/, 2020", "https://www.tripo3d.ai/blog/explore/hd-model-hero-asset-requirements-for-film-vfx", "https://3dart.it/camera-projection-in-nuke", "https://unity.com/blog/games/realizing-rapid-conceptual-design-with-kitbashing", "https://radiancefields.com/jurassic-world-rebirth-and-gaussian-splatting, 2026-02-13", "https://flick.art/blog/blender-ai-filmmaking, 2026-06", "https://dev.epicgames.com/documentation/en-us/unreal-engine/unreal-vcam-virtual-camera-settings", "Field tests 2026-10-13 to 10-17 (ai-docs/research)"]
volatile_claims: ["splats are used for scouting and layout, not final pixels", "which video models take depth, pose and Canny controls"]
---

# 3D models for film and AI video

## Rules

- Say what the 3D is for before anyone builds it: **previs** (try the shots), **techvis** (prove a shot can be made: lens, camera distance, travel), **postvis** (stand-ins over a rendered take to judge the cut), or **control** (a depth, pose or edge video that drives the generator, `kb show blockout-control`). In AI video one blockout usually serves previs and control at once.
- Build from the cards, not the script. Every planned camera with its lens, height and mark goes into the scene first; model only what those frusta see. A wall no card faces is not built.
- Detail follows the largest size the object reaches on screen. Hero objects (the camera lingers, a hand touches it, the story turns on it) get a model and a prop sheet (cinewright-design, `kb show prop-sheets`); background is silhouette and mass.
- Far things are not modelled: a sky, a skyline or a mountain range is a painted plate on a card or a 2.5D projection. That holds while the camera moves little; a big move past it needs geometry.
- Real places: scout from a capture (photogrammetry, Gaussian splats, a map tile) and block on it; productions use splats for layout and sightlines, not final pixels.
- Hard-surface sets (machines, ships, ruins) come fastest from kitbashing: reused parts arranged, then repainted by the image model.
- People in the blockout are stand-ins for height, marks and facing; identity comes from turnarounds and references, never from the mesh's face.
- Controls are grey: clay, depth, pose, Canny of the clay. Texture in a control fights the references and is copied. The look (photoreal, painted, toon) lives in the style bible and the references; the blockout is the same for every style.
- Real scale in metres (people 1.7 to 1.8 m), the card's lens on a 36 mm wide filmback, camera height in metres. A wrong scale or lens makes a control that fights the prompt.
- Ask polywright for it ([contract](https://github.com/m4bwav/polywright/blob/main/skills/polywright/references/contract.md), target `video-blockout`): list the cards with their cameras, the sets, the hero props, the marks per beat and the passes wanted. polywright's side of the same work: [film-and-video](https://github.com/m4bwav/polywright/blob/main/skills/polywright/references/film-and-video.md).

## Numbers

- Detail by shot size (one VFX school's LOD ladder): EWS lowest, LS, FS, MFS, MCU and CU high, ECU custom. An object seen at most in a wide gets the wide's level.
- Pose skeletons under about 40 px tall are noise: depth for the mass, pose for the front ranks and the leads (crowd test, 2026-10-13).
- A blade at real width breaks up in depth at a 4 m two-shot; 2.8 times as thick reads (fight test, 2026-10-16).
- Canny of the clay at 0.95 kept a hero object 28 m away at its planned size; depth at 0.7 to 0.9 washed image plates white (set test, 2026-10-15).

## Vocabulary

- previs, techvis, postvis, stuntvis, hero asset, background asset, LOD, set dressing, kitbash, matte painting, 2.5D projection, digital double, splat, clay render, filmback.

## Pitfalls

- A detailed, textured blockout: slow to build and it confuses the model; rough shapes drive it better.
- Modelling the whole location, then finding a card's end state below the frame. Check every end state through its card's camera first.
- A still control for a moving action freezes the people at their marks.

## Verify

- Each card's camera view of the blockout beside its storyboard frame: same subjects, sides, sizes and horizon.
