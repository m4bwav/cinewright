---
title: Filtration
slug: filtration
summary: Filter looks (mist, fog, double fog, low-contrast, diffusion, polarizer, grad ND) as visible traits in the look string; one grade per scene, matched across neighbours, no cancelling stacks.
tags: [camera, filters, diffusion, mist, fog, contrast, look]
last_checked: 2026-11-14
sources: ["ASC, American Cinematographer Manual, 7th ed., 1993, Filters chapter (pp. 201-224)"]
---

# Filtration

## Rules

- Ask for a filter by what it does to the picture, not by brand or grade: "soft halo around lamps" (mist), "lights bloom outward, low contrast" (fog), "milky low contrast, close faces still sharp" (double fog), "lifted shadows, highlights intact" (low-contrast). A brand name alone is noise to a video model. Book rule, unverified on our models.
- Mist keeps the glow tight to the source, fog spreads it wide. Pick the word for the halo size you want (ASC Manual, Filters).
- Thick real fog keeps near objects sharp and only drops contrast. Write "low contrast haze, foreground sharp" rather than "foggy filter", which softens everything (ASC Manual, Filters).
- Fog that should build with distance: say so in depth terms ("haze thickening toward the background"), the job a graduated fog filter does in camera. Book rule, unverified.
- The effect grows with light: a filter that halos a bright exterior does little in a dim room. Expect less glow at night and do not raise the grade word to make up for it (ASC Manual, Filters).
- One filtration grade per scene, written once in the look or the scene's `sun` string. If one shot needs heavy diffusion (a face, a dream), lightly diffuse its neighbours too, so the cut does not show the filter (ASC Manual, Filters).
- Diffusing a face: keep the eyes sharp. Write "soft skin, eyes sharp"; dull, soft eyes read as a fault, not a look.
- Never stack filters that cancel: a polarizer deepens colour while a low-contrast filter flattens it. Three effects at most in one look string (ASC Manual, Filters).
- Polarizer through glass or water: remove most of the reflection, not all. A trace of reflection tells the viewer there is a surface; without it a face behind a car window seems to float in open air (ASC Manual, Filters).
- Black-and-white: name the sky tone you want ("dark sky, white clouds"); on film a yellow to red filter did this, and only a blue sky darkens. A graduated ND darkens the sky but does not separate clouds (ASC Manual, Filters).

## Vocabulary

- mist, halation, bloom, fog, double fog, low-contrast, diffusion, net, star filter, polarizer, graduated ND, sky grad, center spot.

## Pitfalls

- Star and cross-screen streaks from a square net: rarely wanted; leave "star filter" out unless the brief asks for it.
- A pattern filter shows its pattern at small apertures and wide lenses. In AI terms: a deep-focus wide with "net diffusion" may render a visible screen texture; drop the diffusion word on deep wides.

## Notes

- Source: 1993 manual; the filter names are still sold and the optics have not changed. AI wording above is ours.
