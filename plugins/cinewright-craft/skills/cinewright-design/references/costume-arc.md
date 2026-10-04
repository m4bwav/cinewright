---
title: Costume arc
slug: costume-arc
summary: Wardrobe that changes with the story, written as per-scene wardrobe strings in the character bible, with progressive damage and dirt tracked scene by scene.
tags: [design, costume, wardrobe, arc, damage, silhouette]
last_checked: 2026-10-04
sources: ["Deborah Nadoolman Landis, Costume Design, 2012", "Avril Rowlands, The Continuity Supervisor, 4th ed., 2000"]
---

# Costume arc

## Rules

- Wardrobe is a string per scene in `bibles/characters.json` `wardrobe`: `default` plus one key per scene id where it changes. `cards new` copies the right one and the continuity diff checks it word for word.
- A costume arc shows the story: a change of clothes, a coat taken off, damage that builds. Name in the design notes which beat causes each change.
- Progressive damage and dirt only increase within a story day: write each stage as its own scene wardrobe ("sleeve torn at the left elbow", then "sleeve torn at the left elbow, soot across the chest"). Never let a later scene be cleaner without an on-screen reason.
- Name the side of every tear, stain or bandage as the character's own left or right, as identity marks are.
- Silhouette first: each main character readable by outline alone (a long coat against a short jacket, a hood, a hat). Two characters with the same silhouette and color get confused across separately generated shots.
- Color by character (entry color-script): one costume color per person that no one else in the scene wears.
- Wardrobe strings name garment, color, material and one wear detail, in that order, 25 words or fewer. No brand names.
- Each new wardrobe stage needs its own reference sheet (entry turnaround-sheets).

## Numbers

- Wardrobe string: 25 words or fewer; identity string stays separate and holds no clothing.

## Vocabulary

- costume arc, wardrobe change, breakdown (aging and dirt), continuity stages (stage 1, 2, 3), silhouette, hero costume, doubles.

## Pitfalls

- Clothing words inside an identity string fight the wardrobe string when the costume changes; keep them apart.
- "Same outfit" in a prompt means nothing to a model; paste the full wardrobe string every time.

## Verify

- `continuity diff` shows no WARDROBE error; the design notes list each wardrobe stage with its scene and cause.
