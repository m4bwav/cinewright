---
title: Wall strings
slug: wall-strings
summary: The location description holds only what every angle shares; each wall gets its own string in walls, and a card's camera.faces adds it. A whole-room description pulls every shot to its hero wall.
tags: [sets, location, bible, reverse-angle, compile]
last_checked: 2026-10-07
sources: ["Set field test, 2026-10-07: eleven locations of a real public building on a local image model; two of two off-wall shots came back as the establishing view", "https://higgsfield.ai/blog/consistent-characters-locations", "https://help.storyboarder.ai/en/articles/14067900-how-to-create-consistent-locations-with-the-location-editor"]
---

# Wall strings

## Rules

- A description that names a room's hero features (the desk before three windows) wins over any framing words. "Reverse shot looking north" came back as the desk and windows again. The nouns in the prompt decide what is in frame.
- Split the room in the location bible:
  - `description`: only what every angle shares. Materials, wall color, trim, floor, era, light quality. No object that sits on one wall.
  - `walls`: one string per wall or view, keyed `north`, `east`, `toward-desk`, `from-balcony`. Each names what that wall shows and nothing on the other walls.
- A card that faces a wall sets `camera.faces` to its key. `compile` writes the description, then that wall's string. `cards validate` and `continuity diff` give a WALL error for a key the location lacks.
- A wall string for a reverse says what is not in view when the model would add it by habit: "no windows and no desk in view".
- Write each wall string as if the camera stands in the room facing it: "facing the north wall: a white marble fireplace, a portrait above it, sofas facing each other".
- A famous place's name pulls in its most photographed view. Named, a building shows its postcard facade from every side, through every window and even from its own balcony, and its best-known room shapes the others. Outside the establishing view, describe the geometry (a straight front, a square porch, a triangular pediment, a flat end wall) and leave the name out. Say "no buildings in view" when the camera looks out from the place.
- One location id per place. Do not split a room into several locations to fake walls; scenes, axes and props hang off the location.

## Numbers

- Wall strings: 20 to 300 characters (schema). Description plus one wall string should stay under about 450 characters, so the action still leads the prompt.

## Vocabulary

- hero wall (the wall the establishing shot favours), reverse (the opposite wall), faces, wall string.

## Pitfalls

- Leaving the hero features in `description` after adding walls: the model still pulls to them.
- One seed per set holds palette and light, but the same seed with the same nouns also repeats the composition. Change the nouns, not the seed.

## Verify

- `CINE continuity diff <project>` shows no WALL error, and the compiled prompt for a reverse card holds its wall string and none of the hero wall's nouns.
