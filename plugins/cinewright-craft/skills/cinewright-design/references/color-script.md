---
title: Color script
slug: color-script
summary: Three to five named colors, one named scheme, a scene color row (hue, brightness third, saturation, warmth) that moves with the story, taught meanings, successive contrast.
tags: [design, color, palette, color-script, look]
last_checked: 2026-10-22
sources: ["Bruce Block, The Visual Story, 3rd ed., 2021, ch. 6 (Color)", "James Gurney, Color and Light, 2010, pp. 132-133", "Vincent LoBrutto, The Filmmaker's Guide to Production Design, 2002", "Amid Amidi, The Art of Pixar, 2011"]
---

# Color script

## Rules

- One film palette of three to five named colors in `bibles/style.json` `palette`, plus the look string that names how they sit together ("cold blue storm light against warm amber flame").
- A color script: one row per scene in the design notes with its dominant color, its accent, and why. The dominant color moves with the story value (entry scene-turns in cinewright-script): calm scenes share colors (affinity), the turn brings in contrast.
- Give each scene a `color` row in `bibles/scenes.json`: `hue` (a plain word), `brightness` (dark, middle or bright: which third of the grey scale), `saturation` (muted, mid, saturated) and `warmth` (cool, neutral, warm). `grade measure --plan` checks the cut against it, and `grade match --sat --warm` holds it through the match.
- Name the scheme: one hue, a complementary pair, a three-way or a four-way split. Then set brightness and saturation for the whole film. No palette can be equally bright and equally saturated in every hue: saturated yellow is light, saturated blue is dark (after Block, *The Visual Story*).
- The colour script is the gamut changing with the story: each scene is a slice of the wheel, and the turn brings in what the earlier slices left out (after Gurney, *Color and Light*).
- The first scene that uses a colour teaches its meaning; keep it (`visual_structure.meanings`). Tie each character to a color by costume or light for the whole film unless the costume arc changes it on purpose.
- Successive contrast: a cool scene makes the warm scene after it look warmer, and complementaries cut together look more saturated. Put the cool scene before the one that must glow.
- One saturated object in a muted scene pulls the eye: give it to the subject.
- Audiences forget exact colour, so saturation can climb slowly across a film instead of jumping.
- Use plain color words a model knows ("navy", "amber", "rust", "bone white"), never codes or brand names. Hex values go in the design notes for the grade, not in prompts.
- Put scene color where it compiles: the scene bible's `sun` for the main light color and direction, the location description for set colors, wardrobe strings for costume colors.
- Warm against cool is the strongest contrast a prompt carries reliably; saturation and value contrast come next.
- Grade all shots together in finishing; the color script is the target the grade matches. Matching every shot to one hero per scene flattens a planned progression unless each scene keeps its own targets.

## Numbers

- Palette: 3-5 colors. Per scene: 1 dominant, 1 accent.
- Brightness thirds as `grade measure` reads them: mean luma under 85 dark, 85-169 middle, 170 and up bright (0-255).
- Color temperature words: candle about 1900 K, tungsten 3200 K, daylight 5600 K, overcast and shade 6500-7500 K (details: cinewright-camera).

## Vocabulary

- palette, dominant, accent, affinity, contrast, warm and cool, saturation, value (light and dark), color script, color arc.

## Pitfalls

- "Teal and orange" or "cinematic grade" alone drifts toward the same stock look in every model; name the colors of things in the shot.
- Changing the look string between shots of one scene changes the color of everything; keep it identical and move color through light and wardrobe.

## Verify

- `style.json` has a `palette`; the design notes hold one color-script row per scene; the look string is the same in every compiled prompt.
