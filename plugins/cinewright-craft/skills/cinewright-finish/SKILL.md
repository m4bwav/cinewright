---
name: cinewright-finish
description: "Colorist and VFX finisher for AI video: grade order, color spaces, delivery, crop to the film's frame, day for night, crowd multiplication, cleanup, upscale and interpolation. Use when grading or finishing generated clips; not restoring home video. Also 'refresh cinewright-finish'."
license: MIT
---

# cinewright-finish

Take the locked cut to a delivered picture: composites and cleanup, a four-pass grade, the crop to the film's frame, upscale and retime last, one tagged delivery encode. Outcome: `finish/grade.md` (every pass with its values), the delivery file, and its checks.

`CINE` means `python scripts/cine.py` run from the folder holding this file (run it, never read it). Knowledge: read [references/INDEX.md](references/INDEX.md) once, then `CINE kb show <slug> --section Rules`. Never read the whole folder.

## Step 0: freshness

Read `evergreen.json`. If `contradiction` is set or today is on or after `next_due`, say so in one line, do the task with the current content, then run `evergreen-refresh` if the evergreen plugin is installed. If `tests.failing` is non-empty, say so and run `evergreen-tune` after the task.

## Step 1: inputs

1. A locked cut from cinewright-edit; never grade before lock.
2. Probe it: pixel format, range and color tags (`kb show color-spaces --section Verify`). Generated clips are display-referred Rec.709 in 8-bit; work in 10-bit intermediates.
3. Read `bibles/style.json`: `look`, `aspect_ratio`, `frame_aspect`.

## Step 2: composites and cleanup

1. Crowds and army wides: tile separate generations of small groups over a locked plate (`kb show crowd-multiplication`).
2. Every added layer matches the plate; paint out short artifacts; identity faults go back to cinewright-qc (`kb show compositing-and-cleanup`).

## Step 3: grade

1. Correct, balance, match, look, in that order (`kb show grade-order`). Measure each shot (`signalstats`) and match blacks and skin within a scene before any look.
2. Night from day footage: `kb show day-for-night`.
3. Write each pass and its values in `finish/grade.md`, as filters or ASC CDL a script can repeat.

## Step 4: frame

If `frame_aspect` differs from `aspect_ratio`, crop to it after the grade, centered or reframed per shot, even sizes (`kb show crop-to-frame`; how much each frame keeps: `kb show aspect-ratios`).

## Step 5: last steps

1. Upscale once to the delivery size, then interpolate or retime only where needed; check every interpolated shot frame by frame (`kb show upscale-and-interpolation`).
2. Encode once with color tags set inside the picture (`kb show delivery-color`).
3. Check: `ffprobe` tags read the delivery space; `CINE qc spec <file> --project <p> --card <ids>` passes; `CINE qc sheet` of the result is read once. Quote the last lines.

## Output

`finish/grade.md`, the delivery file with its size, tags and checks, and anything sent back to qc.

## While working: capture learnings

If the user corrects you, the same error happens twice, or a workaround turns up, add an entry to [LEARNINGS.md](LEARNINGS.md) now (check existing entries first). If it proves a rule here wrong, fix the rule, log it in [CHANGELOG.md](CHANGELOG.md), and set `contradiction` in `evergreen.json`.

## Maintenance

This skill is evergreen (tier `moderate`; state in `evergreen.json`). Files: [RESEARCH.md](RESEARCH.md) (findings and search plan), [CHANGELOG.md](CHANGELOG.md), [LEARNINGS.md](LEARNINGS.md), [TESTS.md](TESTS.md) and `evals/evals.json`. How to maintain it, with or without the evergreen plugin: [MAINTENANCE.md](MAINTENANCE.md). Refresh with `evergreen-refresh`, test with `evergreen-test`, fix with `evergreen-tune`.
