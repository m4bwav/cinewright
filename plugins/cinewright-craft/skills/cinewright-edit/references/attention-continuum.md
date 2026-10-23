---
title: Attention continuum
slug: attention-continuum
summary: Where the eye is at each cut on a nine-cell grid: attention start and end, the same cell across a calm cut, a jump only at a peak, and what the eye goes to first.
tags: [edit, attention, eye-trace, cuts, block, continuity]
last_checked: 2026-10-22
sources: ["Bruce Block, The Visual Story, 3rd ed., 2021, ch. 7 (Movement)", "Walter Murch, In the Blink of an Eye, 2nd ed., 2001 (eye-trace)"]
---

# Attention continuum

## Rules

- Lay a nine-cell grid on the frame: 1-3 the top row left to right, 4-6 the middle, 7-9 the bottom. Card `attention.start` and `attention.end` name the cell of the face or moving subject on the first and last frame (after Block, *The Visual Story*).
- In a calm stretch, the end cell of shot A is the start cell of shot B. The eye does not have to travel, so the cut hides, small continuity faults slip past and the cutting can be faster.
- A jump across the frame (two cells or more) jolts. Keep it for the planned peaks (card or scene `intensity` 50 or more) and for people who should feel apart. Too many jumps push the viewer out.
- Shot and reverse that should feel close put both faces in the same cell; an uneasy pair alternates left and right cells.
- What the eye goes to, in order: movement, then the brightest area, then faces and eyes, then a vanishing point, then whatever is newest. If the brightest area of a frame is not the subject, the eye goes there first.
- Compile writes the start cell into the card ("her face is in the upper left of the frame"), so plan it before rendering, not in the edit.

## Numbers

- A jump is the larger of the row and column difference; 2 means across the frame.
- `continuity diff` warns ATTENTION on a jump of 2 at intensity under 50 (or unset), and when the start cell's column disagrees with a single person's `position`.

## Pitfalls

- Cutting on matched action but with the eye flung across the frame: the match is lost.
- A bright window or sky behind the subject: the eye leaves the face for it.

## Verify

- `CINE continuity diff <project>`: no ATTENTION warnings, or each jump is a planned peak.
- Review each cut with the last frame of A beside the first frame of B (cinewright-qc review-passes); a jump the plan did not ask for is code `attention-jump`.

Related: see also [cut-points](cut-points.md), [visual-structure](../../cinewright-design/references/visual-structure.md).
