---
title: Battle scenes
slug: battle-scenes
summary: Plan a battle as a map, two sides with fixed screen direction, three to five phases, and many small fights; build scale from few large foreground figures, haze and compositing, never a rendered mass.
tags: [movement, battle, war, crowds, fights, geography, scale]
last_checked: 2026-10-04
sources: ["Steven D. Katz, Film Directing Shot by Shot, 1991", "Daniel Arijon, Grammar of the Film Language, 1976", "VES Handbook of Visual Effects, 3rd ed., 2020"]
---

# Battle scenes

## Rules

- Draw a top-down map first in the design notes: where each side starts, the line between them, the objective, the hero's path. The line between the sides is the battle's axis; every card's camera stays on one side of it.
- Side A always enters and attacks toward one screen direction (left to right), side B the other, for the whole battle. Give each side a lead in `characters.json` and set their `travel` in the scene's axis so `continuity diff` checks DIRECTION.
- Make the sides readable in one glance: one color and one silhouette each (banner color, helmet shape), in the wardrobe strings and the color script (cinewright-design).
- Split the battle into 3-5 phases (approach, clash, turn, rout, aftermath). Each phase is a scene in `scenes.json` with its own light, weather and smoke state; damage and dirt move forward as wardrobe stages.
- Cover each phase as geography plus small fights: an establishing wide, then the hero's fight as single exchanges (entry fights-and-stunts), reactions, and a re-establishing wide every four cards.
- Scale without a rendered crowd (entry hard-subjects): 1-5 large figures in the foreground, the mass as silhouettes in dust or smoke behind, long lenses to stack depth. The wide army shot is built in compositing by tiling separate generations of small groups (cinewright-finish, entry crowd-multiplication), or left implied by sound (cinewright-sound, entry battle-sound). Cutting it: cinewright-edit, entry cutting-a-battle.
- Charges and cavalry: one or two riders side-on and large; the line is background dust.
- Keep the camera simple in combat cards: static, one slow move, or handheld only if the style allows it.
- Check the model card and the brief's rating before writing blood, wounds or death.

## Numbers

- Phases 3-5; foreground figures 1-5; a re-establishing wide at least every 4 cards; combat cards 3-5 s.

## Pitfalls

- "A massive battle with thousands of soldiers" gives clones, merged limbs and armies that switch sides between shots.
- A side that changes screen direction without a shown turn reads as a retreat.

## Verify

- `continuity diff` shows no DIRECTION, POSITION or HARD-SUBJECT findings, or notes explain each.
