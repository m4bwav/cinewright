---
name: cinewright-sets
description: "Set and location designer for AI video: plan with walls and sun, per-wall descriptions, master plates, reverse angles, set light, plate checks. Use when building a set, location or environment reference for shots, or when a room drifts or a reverse repeats the wide between clips. Also 'refresh cinewright-sets'."
license: MIT
---

# cinewright-sets

Build each place the film returns to as a set: a plan, a bible entry whose words hold across every angle, one master plate per time of day, a plate for each wall the cameras will see, and a check of every plate against the plan. Outcome: `sets/<id>.md`, `bibles/locations.json` with `walls`, plates in `refs/sets/<id>/`, and a pass or fail per plate.

`CINE` means `python scripts/cine.py` run from the folder holding this file (run it, never read it). Knowledge: read [references/INDEX.md](references/INDEX.md) once, then `CINE kb show <slug> --section Rules`. Never read the whole folder.

## Step 0: freshness

Read `evergreen.json`. If `contradiction` is set or today is on or after `next_due`, say so in one line, do the task with the current content, then run `evergreen-refresh` if the evergreen plugin is installed. If `tests.failing` is non-empty, say so and run `evergreen-tune` after the task.

## Step 1: research and plan

1. List every scene at the set from `script.md`: INT or EXT, time of day, what happens.
2. A real place: research its current state with dated sources and tag each fact (`kb show set-plan`). An invented place: write its plan first, then its look.
3. Write `sets/<id>.md`: size, the walls by compass name with what stands on each, doors and windows, hero dressing with fixed positions, the north arrow, the sun per scene, and which walls each planned camera sees (`kb show set-plan`).

## Step 2: bible entry with walls

Write the location's `description` with only what every angle shares (materials, palette, era, light quality). Put each wall's features in `walls`, one string per wall or view. Cards that face a wall set `camera.faces`; `compile` adds that wall's string (`kb show wall-strings`).

## Step 3: master plates

Generate the widest establishing plate first, one per time of day, at the renderer's frame (`kb show master-plates`). Light comes from `kb show set-light`: a named source, a color temperature and a key side, the same words every time. Generating an image is the user's image tool's job; ask before any paid render.

When words keep failing a blocking (crossings, a camera path, a vehicle's line), drive the shot from a blockout's depth, pose or layout video (`kb show blockout-control`).

## Step 4: coverage

For every wall a camera will see, make its own plate from that wall's string, never a 180-degree turn of the master in text or with an angle-edit model. Small moves (up to about 45 degrees, push-ins) may come from the master (`kb show coverage-angles`).

## Step 5: check and clean

1. Check each plate at full size against the plan (`kb show set-check`): doors, windows and hero dressing on the right wall, light from the stated side, palette held, no readable text, no people.
2. Clean what fails (cinewright-design, entry clean-references) or regenerate; record pass or fail per plate in `sets/<id>.md`.
3. Add the passed plates to the location's `refs`. Run `CINE cards validate <project>` and `CINE continuity diff <project>`; quote both last lines. No WALL errors may remain.

## Output

The plan, the description and wall strings, the plates per wall and time of day with their verdicts, and the validate and diff lines.

## While working: capture learnings

If the user corrects you, the same error happens twice, or a workaround turns up, add an entry to [LEARNINGS.md](LEARNINGS.md) now (check existing entries first). If it proves a rule here wrong, fix the rule, log it in [CHANGELOG.md](CHANGELOG.md), and set `contradiction` in `evergreen.json`.

## Maintenance

This skill is evergreen (tier `moderate`; state in `evergreen.json`). Files: [RESEARCH.md](RESEARCH.md) (findings and search plan), [CHANGELOG.md](CHANGELOG.md), [LEARNINGS.md](LEARNINGS.md), [TESTS.md](TESTS.md) and `evals/evals.json`. How to maintain it, with or without the evergreen plugin: [MAINTENANCE.md](MAINTENANCE.md). Refresh with `evergreen-refresh`, test with `evergreen-test`, fix with `evergreen-tune`.
