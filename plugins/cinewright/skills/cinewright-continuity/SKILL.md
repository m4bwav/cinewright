---
name: cinewright-continuity
description: "Script supervisor for AI video: character, wardrobe, location and scene-axis bibles, 180-degree rule, screen direction, 30-degree rule, eyelines and props in hand, checked per shot by a continuity diff. Use when shots must match, a character drifts between clips, a cut jumps or flips. Also 'refresh cinewright-continuity'."
license: MIT
---

# cinewright-continuity

Keep every shot consistent with the bibles and with the shot before it: who people are, what they wear and hold, which side of the line the camera stands on, which way people move and look, the time and light. Outcome: bibles in the project folder, a clean `continuity diff`, cards whose identity strings match the bible word for word.

`CINE` means `python scripts/cine.py` run from the folder holding this file (run it, never read it). Knowledge: read [references/INDEX.md](references/INDEX.md) once, then `CINE kb show <slug> --section Rules`. Never read the whole folder.

## Step 0: freshness

Read `evergreen.json`. If `contradiction` is set or today is on or after `next_due`, say so in one line, do the task with the current content, then run `evergreen-refresh` if the evergreen plugin is installed. If `tests.failing` is non-empty, say so and run `evergreen-tune` after the task.

## Step 1: bibles before cards

Write these in the project folder (shapes in `scripts/schemas/`; layout in cinewright, entry `project-layout`):

- `bibles/characters.json`: one identity string per character, wardrobe by scene. Rules: `kb show identity-strings`.
- `bibles/locations.json`: one description string per place.
- `bibles/scenes.json`: per scene the axis line, camera side A, where each character sits and travels as seen from side A, time of day, sun. Rules: `kb show axis-and-screen-direction`.
- `bibles/style.json`: format and one look string.
- `bibles/props.json` (optional): one description per held prop; compiled verbatim (cinewright-design, entry prop-constants).

Then `CINE cards validate <project>`; fix every ERROR.

## Step 2: diff every card

1. New cards start from the bible: `CINE cards new <project> --id 1D --scene 1 --cast a,b` copies identity and wardrobe.
2. Run `CINE continuity diff <project>`. The evidence is its last line, `continuity diff: N cards, 0 errors, ...`. Quote it.
3. Fix each ERROR in the card, or in the bible when the bible is wrong. Never silence a check. Codes and fixes: `kb show shot-checklist`.
4. Try a change first with `--with changed-card.json`.

Rules the diff cannot see (read once per film): `kb show ai-continuity`, `kb show thirty-degree-rule`, `kb show eyelines`.

## Step 3: hand off and close the loop

- A clean diff goes to cinewright-genvideo to compile prompts. If it is not installed, say "install the cinewright plugin for prompt compiling".
- After a render, write what the last frame really shows into the take's `observed_end_state` and copy it into the next card's `start_state`.

## Output

The diff summary line, each of its errors and warnings with its fix as `card field: old -> new`, and any call the rules could not make, for the user to decide. Report as errors only what the diff or a named rule finds; a doubt from reading by eye goes last, as one question, never as an error.

## While working: capture learnings

If the user corrects you, the same error happens twice, or a workaround turns up, add an entry to [LEARNINGS.md](LEARNINGS.md) now (check existing entries first). If it proves a rule here wrong, fix the rule, log it in [CHANGELOG.md](CHANGELOG.md), and set `contradiction` in `evergreen.json`.

## Maintenance

This skill is evergreen (tier `slow`; state in `evergreen.json`). Files: [RESEARCH.md](RESEARCH.md) (findings and search plan), [CHANGELOG.md](CHANGELOG.md), [LEARNINGS.md](LEARNINGS.md), [TESTS.md](TESTS.md) and `evals/evals.json`. How to maintain it, with or without the evergreen plugin: [MAINTENANCE.md](MAINTENANCE.md). Refresh with `evergreen-refresh`, test with `evergreen-test`, fix with `evergreen-tune`.
