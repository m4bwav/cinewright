---
name: cinewright-script
description: "Screenwriter for AI video: logline, beats, scene turns, screenplay format and dialogue sized for generated voices. Use when writing or fixing the story, script, beats or lines of a short film, ad or music video before shots. Also 'refresh cinewright-script'."
license: MIT
---

# cinewright-script

Turn an idea into a story the camera can show: a one-sentence logline, beats that are visible changes, one turn per scene, a screenplay whose sluglines match the scene bible, and lines short enough for a generated voice. Outcome: `brief.md` and `script.md` in the project folder.

`CINE` means `python scripts/cine.py` run from the folder holding this file (run it, never read it). Knowledge: read [references/INDEX.md](references/INDEX.md) once, then `CINE kb show <slug> --section Rules`. Never read the whole folder.

## Step 0: freshness

Read `evergreen.json`. If `contradiction` is set or today is on or after `next_due`, say so in one line, do the task with the current content, then run `evergreen-refresh` if the evergreen plugin is installed. If `tests.failing` is non-empty, say so and run `evergreen-tune` after the task.

## Step 1: brief

Write `brief.md`: the idea as given, a logline of one sentence, length, format, and a numbered beat list sized to the length (`kb show logline-and-beats`). Each beat is one visible change.

## Step 2: scenes and turns

For each scene, write its goal, its opposition and its turn, with the value and its charge before and after (`kb show scene-turns`). Put the turn in one shot.

## Step 3: script.md

1. Plain-text screenplay: slugline, action, character cue, parenthetical, dialogue (`kb show screenplay-format`). No camera directions.
2. Lines: one speaker per shot and that speaker in the shot, 2.5 words a second at most, words a voice says cleanly (`kb show dialogue-for-generated-voices`). Give every speaker a `voice` string in the character bible, and every rare name that is spoken a `pronounce` respelling from the source the owner trusts.
3. Copy each slugline into `bibles/scenes.json` as the scene's `heading`.

## Step 4: hand off and check

1. Hand the script to cinewright-shots for cards. If it is not installed, say "install the cinewright plugin for shot lists".
2. Once cards exist, and whenever a line changes, put the line in its card and run `CINE continuity diff <project>`; quote its last line and any DIALOGUE warning. Never count words by hand instead: the diff is the check. Fix the line, not the shot length, unless the beat needs the time.

## Output

The logline, the beat list, each scene's value and turn, and any line you cut to fit, with its old and new word count.

## While working: capture learnings

If the user corrects you, the same error happens twice, or a workaround turns up, add an entry to [LEARNINGS.md](LEARNINGS.md) now (check existing entries first). If it proves a rule here wrong, fix the rule, log it in [CHANGELOG.md](CHANGELOG.md), and set `contradiction` in `evergreen.json`.

## Maintenance

This skill is evergreen (tier `slow`; state in `evergreen.json`). Files: [RESEARCH.md](RESEARCH.md) (findings and search plan), [CHANGELOG.md](CHANGELOG.md), [LEARNINGS.md](LEARNINGS.md), [TESTS.md](TESTS.md) and `evals/evals.json`. How to maintain it, with or without the evergreen plugin: [MAINTENANCE.md](MAINTENANCE.md). Refresh with `evergreen-refresh`, test with `evergreen-test`, fix with `evergreen-tune`.
