---
title: Shot list and order
slug: shot-list-order
summary: The shot list is the cards; slate letters, cut order versus writing order, how beats map to shots, grouping shots into generations, and which shot to render first.
tags: [shots, shot-list, slate, order, generations]
last_checked: 2026-10-04
sources: ["Steven D. Katz, Film Directing Shot by Shot, 1991", "Giuseppe Cristiano, The Storyboard Design Course, 2007", "https://en.wikipedia.org/wiki/Shot_list"]
---

# Shot list and order

## Rules

- The shot list is the folder of cards; never keep a second list by hand. `CINE cards list <project>` prints it in cut order.
- Each card: one subject, one action, one camera move, 3-8 s, and a `beat` that says what the audience learns from the shot.
- Slate: scene number plus letter (1A, 1B). Letters follow the order the cards were written; `order` is the position in the cut and may differ.
- Write a scene's cards master first, then singles, then the insert; then set `order` for the cut.
- Short form: one beat is one or two shots. A beat that needs three shots is two beats.
- Durations add up to the brief's target length, within 10%.
- Group into generations: consecutive cards of one scene, on one camera side, whose total fits the model's longest take, render as one generation (`compile --sequence`). Put a seam only where the place or the side changes.
- Render first the shot others depend on: the one whose last frame starts a continuation, or the first shot of each recurring character, so identity is checked before the rest are spent.

## Numbers

- At about 4 s a shot, a minute holds about 15 shots.
- Model longest takes (2026-10): 8 s (Veo 3.1) to 15 s (Kling 3.0, Seedance 2.5); the model card has the exact number.

## Vocabulary

- shooting order: the order takes are made. cut order: the order they play. pickup: a shot added after the first pass.
- Slate letters skip I and O, which read as 1 and 0.

## Pitfalls

- A card whose action holds "then" is two cards (`continuity diff` ONE-ACTION).
- A long run of singles with no wide shot loses the geography; put a wide shot back in at least every eight shots or at every re-block.

## Verify

- `cards list` last line: shot count, scenes and total seconds match the brief.
- `cards validate` shows 0 errors; every card has a `beat`.
