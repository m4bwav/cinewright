---
name: cinewright-design
description: "Production and costume designer for AI video: turnaround sheets, clean reference images, prop descriptions, costume arc and color script. Use when designing characters, costumes, props or palette (sets and locations: cinewright-sets), or when a prop or outfit drifts between clips. Also 'refresh cinewright-design'."
license: MIT
---

# cinewright-design

Design what the camera sees so it holds across separately generated shots: one turnaround sheet per character and costume, references cleaned of stray marks, a fixed description per prop, wardrobe by scene, and a color script. Outcome: `refs/`, `bibles/props.json`, wardrobe and palette in the bibles, and `design.md` notes.

`CINE` means `python scripts/cine.py` run from the folder holding this file (run it, never read it). Knowledge: read [references/INDEX.md](references/INDEX.md) once, then `CINE kb show <slug> --section Rules`. Never read the whole folder.

## Step 0: freshness

Read `evergreen.json`. If `contradiction` is set or today is on or after `next_due`, say so in one line, do the task with the current content, then run `evergreen-refresh` if the evergreen plugin is installed. If `tests.failing` is non-empty, say so and run `evergreen-tune` after the task.

## Step 1: palette and color script

Set three to five named colors in `bibles/style.json` `palette`, then one color-script row per scene in `design.md` with its dominant color and why (`kb show color-script`).

## Step 2: costumes

Write wardrobe per scene in the character bible, with each damage stage as its own scene string and silhouettes that differ (`kb show costume-arc`). Keep clothing out of identity strings.

## Step 3: props

Add every held or close-up prop to `bibles/props.json` with a fixed description (`kb show prop-constants`). Card `holding` values use the prop's `name`.

## Step 4: reference images

1. Write the turnaround sheet prompt per character and costume: three views, flat light, grey backdrop, identity and wardrobe strings verbatim (`kb show turnaround-sheets`). Generating the image is the user's image tool's job; writing the prompt never starts a paid render.
2. Before any reference is used, list what to paint out and check marks at full size (`kb show clean-references`).
3. Add the cropped views to the character's `refs`.

## Step 5: check

Run `CINE cards validate <project>` and `CINE continuity diff <project>`; quote both last lines. No PROP or WARDROBE findings may remain. Record what changed in `design.md`.

## Output

The palette, the color-script rows, each wardrobe stage with its cause, the prop descriptions, and the reference prompts with their clean-up list.

## While working: capture learnings

If the user corrects you, the same error happens twice, or a workaround turns up, add an entry to [LEARNINGS.md](LEARNINGS.md) now (check existing entries first). If it proves a rule here wrong, fix the rule, log it in [CHANGELOG.md](CHANGELOG.md), and set `contradiction` in `evergreen.json`.

## Maintenance

This skill is evergreen (tier `slow`; state in `evergreen.json`). Files: [RESEARCH.md](RESEARCH.md) (findings and search plan), [CHANGELOG.md](CHANGELOG.md), [LEARNINGS.md](LEARNINGS.md), [TESTS.md](TESTS.md) and `evals/evals.json`. How to maintain it, with or without the evergreen plugin: [MAINTENANCE.md](MAINTENANCE.md). Refresh with `evergreen-refresh`, test with `evergreen-test`, fix with `evergreen-tune`.
