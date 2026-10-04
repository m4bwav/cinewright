---
title: Color script
slug: color-script
summary: A palette of three to five named colors per film, a dominant color per scene that moves with the story, and where each lands in the bibles so every prompt carries it.
tags: [design, color, palette, color-script, look]
last_checked: 2026-10-04
sources: ["Bruce Block, The Visual Story, 2nd ed., 2008", "Vincent LoBrutto, The Filmmaker's Guide to Production Design, 2002", "Amid Amidi, The Art of Pixar, 2011"]
---

# Color script

## Rules

- One film palette of three to five named colors in `bibles/style.json` `palette`, plus the look string that names how they sit together ("cold blue storm light against warm amber flame").
- A color script: one row per scene in the design notes with its dominant color, its accent, and why. The dominant color moves with the story value (entry scene-turns in cinewright-script): calm scenes share colors (affinity), the turn brings in contrast.
- Tie each character to a color by costume or light, and keep it for the whole film unless the costume arc changes it on purpose.
- Use plain color words a model knows ("navy", "amber", "rust", "bone white"), never codes or brand names. Hex values go in the design notes for the grade, not in prompts.
- Put scene color where it compiles: the scene bible's `sun` for the main light color and direction, the location description for set colors, wardrobe strings for costume colors.
- Warm against cool is the strongest contrast a prompt carries reliably; saturation and value contrast come next.
- Grade all shots together in finishing; the color script is the target the grade matches.

## Numbers

- Palette: 3-5 colors. Per scene: 1 dominant, 1 accent.
- Color temperature words: candle about 1900 K, tungsten 3200 K, daylight 5600 K, overcast and shade 6500-7500 K (details: cinewright-camera).

## Vocabulary

- palette, dominant, accent, affinity, contrast, warm and cool, saturation, value (light and dark), color script, color arc.

## Pitfalls

- "Teal and orange" or "cinematic grade" alone drifts toward the same stock look in every model; name the colors of things in the shot.
- Changing the look string between shots of one scene changes the color of everything; keep it identical and move color through light and wardrobe.

## Verify

- `style.json` has a `palette`; the design notes hold one color-script row per scene; the look string is the same in every compiled prompt.
