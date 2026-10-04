---
title: Applying a style
slug: applying-styles
summary: Turn 'shoot it like 1970s New Hollywood, 2.39' into style-bible fields (look, lighting, lens_family, frame_aspect, allowed_moves, history) that compile and diff; no names in prompts.
tags: [history, style, style-bible, look, compile]
last_checked: 2026-10-04
sources: ["Bruce Block, The Visual Story, 2nd ed., 2008", "David Bordwell and Kristin Thompson, Film Art: An Introduction, 12th ed., 2019"]
---

# Applying a style

## Rules

- At most three cards per film: one movement or era, one genre, one director or cinematographer. More cards average into a stock look.
- On a conflict the most specific card wins: director over genre over movement or era. The brief's own choices (palette, story color script) win over every card.
- Translate each tag to a style-bible field, never a name:
  - look and grain tags plus the story palette: `look` (one string, 300 characters at most).
  - light tags: `lighting` (words from lighting-terms, with the ratio as shadow words).
  - lens tags: `lens_family` with a range in mm, so the diff checks every card's `lens_mm`.
  - frame: `frame_aspect` when it differs from the render.
  - move tags: `allowed_moves` (the card's moves plus `static`), so the diff warns MOVE on others.
  - card ids: `history`, for the record.
- Never write a director, cinematographer, film or studio name in a prompt; describe the devices. Names drift toward a famous frame or are refused by some models (unverified per model).
- Cut and sound tags go to the edit and sound notes (cinewright-edit, cinewright-sound), not the prompt.
- A user frame or format the model does not render (2.39, 1.37) stays the render aspect plus `frame_aspect`; finishing crops.
- Try a look first: write it to a separate file and use `--style FILE` on `cards validate`, `continuity diff` and `compile`, then copy it over `bibles/style.json` when chosen.

## Verify

- The diff on the new style shows no LENS or MOVE warning, or the cards were changed to fit.
- Each compiled prompt holds the new look, the lighting string and, when set, the composition sentence; the render aspect in the params is unchanged.
