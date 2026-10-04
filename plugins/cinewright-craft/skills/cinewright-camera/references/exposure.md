---
title: Exposure
slug: exposure
summary: Set the overall brightness of the film as a key (high, normal, low) and keep it per scene; write darkness as shaped shadow with a visible source, never as 'dark', and protect skin and highlights.
tags: [camera, exposure, contrast, low-key, night]
last_checked: 2026-10-04
sources: ["Blain Brown, Cinematography: Theory and Practice, 3rd ed., 2016", "Blain Brown, Motion Picture and Video Lighting, 3rd ed., 2018"]
---

# Exposure

## Rules

- One exposure key per scene: high-key, normal or low-key (lighting-terms vocab). It goes in the style bible's `lighting` string when it holds for the film, or in the scene's `sun` string when it changes by scene.
- Night and dark scenes: name a source and let it shape the shadow ("lit only by the lamp, faces half in shadow"). "Dark" or "very dark" alone gives muddy grey noise or a lit set. (Practice observation, unverified across models.)
- Expose for skin: the face of the subject stays readable in every card, even in low-key. Ask for a rim or an eye light when the face is mostly in shadow.
- Silhouettes are a choice: say "in silhouette against the window" and accept that identity strings will not read; never put a silhouette on a card that must sell identity.
- Highlights: a lamp, a window or the sky blow out in some models; name them as "glowing" rather than "bright white" when detail matters.
- Day for night and underexposed looks are graded in finishing (cinewright-finish), not asked of the model; prompt a normal exposure with the night's light direction.

## Numbers

- 18% grey is the meter's middle; skin sits about one stop above it in a normal key. For the cinematographer's notes, not prompts.

## Vocabulary

- key (high, low), stop, underexposed, overexposed, blown out, crushed blacks, silhouette, day for night, eye light.

## Pitfalls

- Exposure that changes between cards of one scene reads as a different time of day; the diff cannot see it, qc can (failure codes in cinewright-qc).
- "Underexposed" in a prompt can drop the whole frame into noise on local models; prefer "low-key, deep shadows" and grade down later.

## Verify

- Each scene has one key, stated once in the style or the scene `sun` string.
