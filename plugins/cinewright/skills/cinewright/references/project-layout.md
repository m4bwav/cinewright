---
title: Project folder layout
slug: project-layout
summary: The folders and files a cinewright film project holds, which stage writes each, and the commands that read them.
tags: [project, layout, files, pipeline]
last_checked: 2026-10-03
sources: ["https://github.com/m4bwav/cinewright/tree/main/examples/three-shot"]
---

# Project folder layout

## Rules

```
<project>/
  brief.md              logline, target length, format, beats
  bibles/style.json     format and the look string
  bibles/characters.json identity strings, wardrobe by scene
  bibles/locations.json one description per place
  bibles/scenes.json    axis, camera side, positions, travel, time, sun
  cards/<id>.json       one shot card per shot, id = scene + letter (1A)
  compiled/<model>/     <id>.txt prompt and <id>.params.json settings
  refs/                 reference sheets and keyframes
  takes/<id>-<n>.json   one record per take (seed, verdict, end state)
  film.json             optional export for long-render pipelines
```

- Card ids follow the slate: scene number plus shot letter. Order in the cut is the card's `order` field, not its file name.
- Shapes for every JSON file are in the skill's `scripts/schemas/`.
- Write the bibles before the cards; `cards new` copies identity strings from them.

## Verify

- `python scripts/cine.py cards validate <project>`: 0 errors.
- `python scripts/cine.py continuity diff <project>`: 0 errors.

## Notes

- 2026-10-03: the worked example in the repository's `examples/three-shot/` uses this layout.
