---
title: Anamorphic look
slug: anamorphic
summary: Ask for the anamorphic look by its visible traits (oval bokeh, horizontal blue streak flares, falloff at the edges) in the look string, with a 2.39 frame_aspect; the model renders 16:9 either way.
tags: [camera, anamorphic, lens, flare, widescreen]
last_checked: 2026-10-04
sources: ["https://en.wikipedia.org/wiki/Anamorphic_format", "ASC Manual, 11th ed., 2022"]
---

# Anamorphic look

## Rules

- An anamorphic lens squeezes the width 2x on capture; a 50mm anamorphic sees as wide as a 25mm spherical, so cinematographers use longer lenses and get shallower focus.
- The visible traits are what a prompt can carry: vertical oval bokeh, horizontal streak flares (often blue) from bright points, slight barrel bend and soft edges, a wide frame.
- Put the traits in the style bible's `look` once ("anamorphic lens look, oval bokeh, horizontal blue lens flares"), set `frame_aspect` to "2.39:1", and set `lens_family` to "anamorphic primes, 40-100mm" or similar. Never repeat the words per card.
- Give flares a source: a practical lamp, headlights, a sunset in frame. No bright point, no flare.
- Close-ups: the 2x squeeze means a 75-100mm anamorphic for a close-up a 40-50mm spherical would give; keep `lens_mm` in that longer range for consistency with the family.

## Numbers

- Squeeze 2x (some lenses 1.3x or 1.5x). Classic frame 2.39:1.

## Vocabulary

- anamorphic, squeeze, desqueeze, oval bokeh, streak flare, scope, spherical.

## Pitfalls

- "Anamorphic" alone in a prompt often adds only flares, everywhere; name bokeh and a flare source too.
- Flares on every shot read as an effect; keep them where a light faces the lens.

## Verify

- `look` names the traits once, `frame_aspect` is set, and the cards' lens_mm sit in the anamorphic range.

## Notes

- 2026-10-04: traits and the 50mm-to-25mm equivalence from Wikipedia's anamorphic format article. Model behaviour unverified.
