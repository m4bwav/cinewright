---
title: Clean references
slug: clean-references
summary: A reference image outranks the prompt, so every mark on it is copied into the video; paint out emblems, text and stray details before a reference goes into a shot.
tags: [design, references, emblems, cleanup, identity]
last_checked: 2026-10-04
sources: ["Field lesson 019, 2026-09-29: a video model copies a reference picture's small emblems onto the character, so clean every reference first"]
---

# Clean references

## Rules

- A reference image outranks the text for anything it shows. A small cross, logo, badge, letter or pendant on a reference appears in the video in the same place, whatever the prompt says.
- Clean before use, not later: paint out every unwanted mark, save the original as `<name>_orig.png`, and use only the cleaned file. A note to clean it later is not enough.
- Inspect references at full size, one by one. A contact sheet or montage hides marks a few pixels wide.
- What to remove: emblems and religious or national symbols the story does not need, brand logos and readable text, jewelry that was not designed, stray hands or props from another view, watermarks.
- What to keep: everything the identity string names (the scar, the braid). Check its side as the character's own left or right.
- After cleaning, render one test shot with the cleaned reference and the same seed: if the mark is gone, the reference was the cause.
- Text on screen (signs, labels) belongs in the design notes and the card, never only on a reference; models redraw text badly.

## Numbers

- Inspect at 100% zoom; a mark under about 1% of the image width is still copied.

## Vocabulary

- reference image, ingredient, element (vendor names for references), paint-out, clean plate.

## Pitfalls

- Negative prompt lines ("no emblems") lose against what a reference shows.
- An image model asked for plain armour or uniforms adds insignia by association; check every generated reference, not just found images.
- Logos and trademarks on references put brands in the film; remove them unless licensed.

## Verify

- For each file in a bible's `refs`, an `_orig` copy exists if it was edited, and the design notes say what was removed.
