---
title: Set check
slug: set-check
summary: Check every plate at full size against the plan before use: right wall, doors and windows in place, hero dressing present, light side, palette, no readable text, no people; log pass or fail per plate.
tags: [sets, qc, check, signage, references]
last_checked: 2026-10-07
sources: ["https://gptproto.com/news/ai-video-generates-wrong-text", "https://higgsfield.ai/blog/consistent-characters-locations", "Set field test, 2026-10-07"]
---

# Set check

## Rules

- A plate passes only on what it shows, checked at full size. Check in this order:
  1. Wall: it shows the wall its file name says, not the hero wall again.
  2. Openings: doors and windows sit where the plan puts them, the same count.
  3. Hero dressing: each object the plan puts on that wall is there; nothing from another wall.
  4. Light: the bright side matches the light line for that wall (entry set-light).
  5. Palette and materials match the master.
  6. Text: no readable signs, plaques or labels. Models garble letters and the garble changes every frame. Keep signage blank in plates and add real text in post (cinewright-finish).
  7. People: none. Faces in portraits stay generic; no recognisable real person.
- Log each plate in `sets/<id>.md`: file, verdict, and the failing check by number.
- A failed plate: fix by the cheapest route. Clean a small mark (cinewright-design, entry clean-references); regenerate with a corrected wall string for a wrong wall; regenerate with a new seed only after the words are right.
- Move rejected plates to `refs/sets/_rejected/` with the reason in the name; they are evidence for the learnings.
- After shots render, check the first and last frame of each clip against the same list (cinewright-qc).

## Numbers

- Two seeds per wall plate is the default; keep the one that passes more checks.

## Pitfalls

- Judging from a thumbnail: wrong window counts and garbled plaques only show at full size.
- Passing a plate because it is beautiful. A handsome wrong wall breaks every reverse cut that uses it.
