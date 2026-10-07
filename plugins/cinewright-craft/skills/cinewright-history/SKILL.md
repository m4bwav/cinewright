---
name: cinewright-history
description: "Film history style cards for AI video: movements, eras, genres, directors and cinematographers, as style-bible fields the prompts carry. Use when asked for a period, genre or filmmaker's look ('like 1970s New Hollywood', 'film noir look'). Also 'refresh cinewright-history'."
license: MIT
---

# cinewright-history

Turn a style request into checkable fields: pick at most three style cards, translate their tags into the style bible (look, lighting, lens family, frame, allowed moves, card ids), try the look beside the current one, and show what changed in the compiled prompts. Outcome: `styles/<name>.json` (then `bibles/style.json` once chosen), a diff, and a before-and-after compile.

`CINE` means `python scripts/cine.py` run from the folder holding this file (run it, never read it). Knowledge: read [references/INDEX.md](references/INDEX.md) once, then `CINE kb show <slug> --section Vocabulary` for cards and `--section Rules` for the rest. Never read the whole folder.

## Step 0: freshness

Read `evergreen.json`. If `contradiction` is set or today is on or after `next_due`, say so in one line, do the task with the current content, then run `evergreen-refresh` if the evergreen plugin is installed. If `tests.failing` is non-empty, say so and run `evergreen-tune` after the task.

## Step 1: pick cards

1. `CINE kb search <words from the request>`, then `kb show <entry> --section Vocabulary`. Card ids are the bold words.
2. Take at most one movement or era, one genre, one director or cinematographer. Name the chosen ids and why in one line each. No card fits: say so and build from the camera vocabulary instead.

## Step 2: translate

Follow `kb show applying-styles --section Rules`. Copy `bibles/style.json` to `styles/<name>.json` and set `look`, `lighting`, `lens_family`, `frame_aspect` (when the frame is not the render aspect), `allowed_moves` and `history`. Keep the story's palette. Never write a director, film or studio name into any field that compiles.

## Step 3: check and compare

1. `CINE cards validate <project> --style styles/<name>.json` and `CINE continuity diff <project> --style styles/<name>.json`. Each LENS or MOVE warning names a card to change (lens or move), or the style to widen; say which.
2. `CINE compile <project> --model <model> --card <id>`, then the same with `--style styles/<name>.json`. Show the changed sentences side by side: look, lighting, the composition sentence, and that the rendered aspect in the params stayed the same.

## Step 4: adopt

When the user picks the look, copy it over `bibles/style.json`, change the flagged cards, and rerun the diff; it must be clean. Cut and sound tags go to the edit and sound notes, not the prompts.

## Output

The card ids used, the new style fields, the diff result, and the before-and-after compiled sentences.

## While working: capture learnings

If the user corrects you, the same error happens twice, or a workaround turns up, add an entry to [LEARNINGS.md](LEARNINGS.md) now (check existing entries first). If it proves a rule here wrong, fix the rule, log it in [CHANGELOG.md](CHANGELOG.md), and set `contradiction` in `evergreen.json`.

## Maintenance

This skill is evergreen (tier `glacial`; state in `evergreen.json`). Files: [RESEARCH.md](RESEARCH.md) (findings and search plan), [CHANGELOG.md](CHANGELOG.md), [LEARNINGS.md](LEARNINGS.md), [TESTS.md](TESTS.md) and `evals/evals.json`. How to maintain it, with or without the evergreen plugin: [MAINTENANCE.md](MAINTENANCE.md). Refresh with `evergreen-refresh`, test with `evergreen-test`, fix with `evergreen-tune`.
