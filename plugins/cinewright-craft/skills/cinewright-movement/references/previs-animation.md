---
title: Previs animation
slug: previs-animation
summary: Animation checks for 3D previs before it becomes a control video: wind-ups, offset limbs, drifting holds, arcs, trailing parts, timing by weight. Book craft, untested on video models.
tags: [movement, previs, fights, animation, 3d, blockout]
last_checked: 2026-10-22
sources: ["Roland Hess, Tradigital Blender, 2011: animation principles, moving holds, breaking simultaneous motion", "polywright bpy-recipes-physics (Rigify headless), Blender 5.2.1, 2026-10-22"]
---

# Previs animation

## Rules

Check every keyed 3D previs (a fight, a fall, a crowd charge) against these before rendering its control passes (after Hess, *Tradigital Blender*):

- Anticipation: a strike or throw gets a counter-move (weapon drawn back, hips dropped) a few frames before it. A pose change with no wind-up can read as a jump cut.
- Offset limbs: hands and feet start and stop one or two frames apart, never on the same frame. More than a few frames looks uncoordinated.
- Moving holds: a held pose keeps a small drift. A frozen mannequin in a depth control may freeze the person in the video.
- Arcs: hands and weapons travel on curves. A straight line between two keys cuts through the body.
- Overlap: cloaks, hair and a blade tip trail the hand and keep moving after the body stops.
- Timing by weight: light blades move fast, heavy blows settle long, and the contact key is sharp with an ease out after it.
- Falls and rolls need a rigged body, not a box mannequin. Rigify builds a full rig headless in one call; for a game skeleton it carries too many bones, but for previs it is fine.

## Numbers

- Wind-up 2 to 6 frames before the action key; limb offsets 1 to 2 frames; hold drift 1 to 2 cm and 1 to 2 degrees; trailing parts 2 to 4 frames behind the hand.

## Pitfalls

- None of these has been tried against a video model yet: test one change at a time against the same take.

## Verify

- A sheet of the key frames plus the frames just before each strike: every strike has a wind-up, no two limbs land on one frame.

Related: builds on [fight-previs](fight-previs.md); see also [fight-plan](fight-plan.md).
