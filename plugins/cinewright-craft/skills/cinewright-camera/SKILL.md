---
name: cinewright-camera
description: "Cinematographer and gaffer for AI video: lens choice, depth of field, exposure, frame rate and shutter, aspect ratio and widescreen framing, anamorphic, lighting ratios and setups, color temperature. Use when choosing lenses, light or format, or when light drifts between clips. Also 'refresh cinewright-camera'."
license: MIT
---

# cinewright-camera

Decide how every shot is photographed and lit, and write it where the compiler and the continuity diff can use it: the style bible's format, lens family, lighting string and allowed moves, the scene's light source, and each card's lens and key. Outcome: `bibles/style.json` and `bibles/scenes.json` updated, cards with `lens_mm` and `light`, and a clean diff.

`CINE` means `python scripts/cine.py` run from the folder holding this file (run it, never read it). Knowledge: read [references/INDEX.md](references/INDEX.md) once, then `CINE kb show <slug> --section Rules`. Never read the whole folder.

## Step 0: freshness

Read `evergreen.json`. If `contradiction` is set or today is on or after `next_due`, say so in one line, do the task with the current content, then run `evergreen-refresh` if the evergreen plugin is installed. If `tests.failing` is non-empty, say so and run `evergreen-tune` after the task.

## Step 1: format

1. `aspect_ratio` and `resolution` are a size the model card offers; `fps` is the model's rate (`kb show frame-rate-and-shutter`).
2. If the film's frame differs (2.39, 1.85, 1.37), set `frame_aspect`; the compiler adds the composition sentence and finishing crops (`kb show aspect-and-framing`). Never ask for letterbox bars.

## Step 2: lenses and focus

1. Set `lens_family` with a range in mm ("spherical primes, 24-85mm"); anamorphic traits go in `look` once (`kb show lens-choice`, `kb show anamorphic`).
2. Give each card a `lens_mm` from the ladder (24 wide, 35 two-shot, 50 single, 85 close-up); matched singles share it.
3. Say depth in words on the card, the same for every card of a scene (`kb show depth-of-field`).

## Step 3: light

1. Write the film's `lighting` string: key style, contrast as shadow words, color of the main sources (`kb show lighting-ratios`, `kb show color-temperature`). It compiles verbatim into every prompt.
2. Per scene, the `sun` string names the source, its direction and color (`kb show lighting-setups`). One exposure key per scene (`kb show exposure`).
3. Per card, set `light.key_side`, `quality` and `motivation`, consistent with the camera side.

## Step 4: moves

If the look limits moves (handheld only, static only), list them in `allowed_moves`; the diff warns MOVE on any other.

## Step 5: check

Run `CINE cards validate <project>`, `CINE continuity diff <project>` and `CINE compile <project> --model <model> --card <id>`; quote the last lines and the compiled style sentences. No LENS or MOVE warnings may remain unless a card's `notes` say why.

## Output

The format and frame, the lens family and per-card lenses, the lighting string, each scene's source, and one compiled prompt showing them.

## While working: capture learnings

If the user corrects you, the same error happens twice, or a workaround turns up, add an entry to [LEARNINGS.md](LEARNINGS.md) now (check existing entries first). If it proves a rule here wrong, fix the rule, log it in [CHANGELOG.md](CHANGELOG.md), and set `contradiction` in `evergreen.json`.

## Maintenance

This skill is evergreen (tier `slow`; state in `evergreen.json`). Files: [RESEARCH.md](RESEARCH.md) (findings and search plan), [CHANGELOG.md](CHANGELOG.md), [LEARNINGS.md](LEARNINGS.md), [TESTS.md](TESTS.md) and `evals/evals.json`. How to maintain it, with or without the evergreen plugin: [MAINTENANCE.md](MAINTENANCE.md). Refresh with `evergreen-refresh`, test with `evergreen-test`, fix with `evergreen-tune`.
