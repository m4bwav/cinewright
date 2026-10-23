---
title: Space types
slug: space-types
summary: Block's four kinds of screen space (deep, flat, limited, ambiguous): the staging, lens and move each needs, the words compile writes, and the SPACE warnings.
tags: [shots, space, depth, staging, block, composition]
last_checked: 2026-10-22
sources: ["Bruce Block, The Visual Story, 3rd ed., 2021, ch. 3 (Space)", "Blain Brown, Cinematography: Theory and Practice, 3rd ed., 2016, Language of the Lens"]
---

# Space types

## Rules

- Set `space` on each scene in `bibles/scenes.json`; compile writes its words into every card once (after Block, *The Visual Story*). Deep space is more intense than flat; a change of space is a contrast the plan can use (entry visual-structure).
- Deep: the depth cues on. Lines converging to a vanishing point, people at near, middle and far, an object close to the lens, movement toward or away from camera, a dolly, track or crane, a wide lens (24-35mm), the distance hazier and cooler than the foreground.
- Flat: the depth cues off. A wall square to the camera, everyone on one plane at one size, movement across the frame only, static camera, pan, tilt or zoom, a long lens from far away, narrow tonal range, one colour temperature, soft background.
- Limited: two or three flat planes one behind another, told apart by figure size, no converging lines, movement across the frame only.
- Ambiguous: nothing of known size, camouflaging shadow, an odd angle or a mirror. It breaks the moment a person of known size enters, so use it for openings and inserts.
- Strongest depth cues first: converging lines, size change, texture, movement toward or away, haze, brighter and warmer reads nearer. Overlap is weak, and a blurred area carries no cue at all.
- 2D moves (pan, tilt, zoom) keep foreground and background moving together and flatten. 3D moves (dolly, track, crane) slide the foreground past the background and deepen. A long lens alone does not flatten; flat staging does.
- Surface divisions: a door edge, a pole or a bar of light between two people says they are apart; take it away when they come together.

## Vocabulary

- deep, flat, limited, ambiguous space; depth cue; vanishing point; frontal plane; surface division; frame within a frame.

## Pitfalls

- A flat scene with a dolly or a 24mm lens: the move or the lens puts the depth back (`SPACE` warning).
- A deep scene shot as static eye-level frames only: the depth never shows (`SPACE` warning on the scene).

## Verify

- `CINE continuity diff <project>` shows no SPACE warnings, or each is a planned contrast noted in the card's `notes`.
- In review, the take fails `space` when its depth reads against the scene's type (code `space-break`).

Related: builds on [visual-structure](../../../../cinewright-craft/skills/cinewright-design/references/visual-structure.md); see also [framing](framing.md).
