---
title: Aspect and framing
slug: aspect-and-framing
summary: Render at a size the model offers and compose for the film's frame_aspect; the compiler adds a composition sentence, finishing crops, and wide frames change how close-ups and two-shots are staged.
tags: [camera, aspect, framing, widescreen, crop, composition]
last_checked: 2026-10-04
sources: ["https://en.wikipedia.org/wiki/Aspect_ratio_(image)", "Gustavo Mercado, The Filmmaker's Eye, 2010", "Bruce Block, The Visual Story, 2nd ed., 2008"]
---

# Aspect and framing

## Rules

- `aspect_ratio` in the style bible is the render: a size the model card offers (`compile` stops otherwise). Most models render 16:9 and 9:16.
- `frame_aspect` is the film's frame. Set it when it differs: "2.39:1" for scope, "1.85:1" for flat, "1.37:1" for Academy. The compiler adds "Composed for a 2.39:1 widescreen crop, heads and action inside the middle 74% of the frame height." to every prompt, and finishing crops to it.
- Never ask the model for letterbox bars; bar height drifts between takes. Compose and crop.
- Wide frames (2.39): stage two people across the frame instead of over the shoulder, keep close-ups slightly looser, and use lead room on the side the character faces. Headroom shrinks: eyes on the top-third line.
- Narrow frames (1.33, 1.37): vertical composition, more headroom, singles fill the frame; the compiler asks to keep the subject in the middle of the width.
- Vertical 9:16 is a render, not a crop: plan it from the start, one subject, the face in the upper third, nothing important in the bottom fifth (captions and buttons; unverified per platform).
- Choose one frame per film; a change of frame mid-film is a statement (a flashback, an IMAX expansion) and goes in the brief.

## Numbers

- A 2.39 crop keeps 74% of a 16:9 render's height; 1.85 keeps 96%; 1.37 keeps 77% of the width (aspect-ratios vocab).

## Pitfalls

- Composing for 16:9 and cropping later cuts off heads and hands in mediums; the composition sentence must be in every prompt (a compile guard checks it).
- Models may ignore the sentence on some takes; check the crop on the contact sheet before keeping a take (cinewright-qc).

## Verify

- Compiled prompts carry the composition sentence; the params keep the rendered aspect.
