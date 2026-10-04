---
title: Lighting ratios
slug: lighting-ratios
summary: Set contrast as a key-to-fill ratio per film or scene and write it in shadow words a model follows; keep it in the style bible's lighting string so every prompt carries the same contrast.
tags: [lighting, contrast, ratio, high-key, low-key]
last_checked: 2026-10-04
sources: ["Blain Brown, Motion Picture and Video Lighting, 3rd ed., 2018", "ASC Manual, 11th ed., 2022"]
---

# Lighting ratios

## Rules

- Choose one ratio for the film: 2:1 for comedy and warmth, 4:1 for drama (the default), 8:1 or more for noir and horror (lighting-terms vocab).
- Write it in words, not numbers: "strong contrast, the far side of each face in deep shadow" for 4:1, "deep shadow, half the face lost in darkness" for 8:1, "soft even light, gentle shadows" for 2:1. The number goes in the design notes. (Models are not known to read ratios; unverified.)
- Put it in the style bible's `lighting` string with the key style and color: it compiles verbatim into every prompt and a guard stops the compile if it is lost.
- A scene that breaks the film's ratio (a bright flashback) says so in the scene's `sun` string; never change `lighting` between cards of one scene.
- High contrast needs a motivated source in the scene: a window, a lamp, a fire. Without one, the model lights evenly.

## Numbers

- 2:1 is one stop between key side and fill side; 4:1 two stops; 8:1 three stops.

## Pitfalls

- "Dramatic lighting" alone gives the same stock look in every model; give the ratio words and a source.
- Low-key on wide shots can lose the geography; lift the background with a practical or a window.

## Verify

- `lighting` is set and appears verbatim in every compiled prompt; scene exceptions live in `sun`.
