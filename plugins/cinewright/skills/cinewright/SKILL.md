---
name: cinewright
description: "Film director for AI video: turns an idea into a planned film (logline, shot list, bibles, prompts, QC, edit, delivery) and routes each stage to the right cinewright skill. Use when the user wants to make a short film, trailer, music video or ad with AI video models, plan an idea as shots, or asks what comes next. Also 'refresh cinewright'."
license: MIT
---

# cinewright

Plan a film like a crew, check it like a script supervisor, then hand each shot to whatever renders it. Every stage writes a file in the project folder; the next stage reads that file, never the chat.

`CINE` means `python scripts/cine.py` run from the folder holding this file (run it, never read it). Knowledge: read [references/INDEX.md](references/INDEX.md) once, then `CINE kb show <slug> --section Rules`. Never read the whole folder.

## Step 0: freshness

Read `evergreen.json`. If `contradiction` is set or today is on or after `next_due`, say so in one line, do the task with the current content, then run `evergreen-refresh` if the evergreen plugin is installed. If `tests.failing` is non-empty, say so and run `evergreen-tune` after the task.

## Step 1: set up the project

Create the folder from `kb show project-layout`. Write `brief.md`: logline (one sentence), target length, format, and the beats (one line each). Ask the user only for what changes the film: length, aspect, the renderer they will use.

## Step 2: run the pipeline

One default path (`kb show pipeline` for gates and the repair ladder). Each row names its evidence.

| Stage | Writes | Skill |
|---|---|---|
| Script | `brief.md`, `script.md` | cinewright-script (craft) |
| Bibles | `bibles/*.json` | cinewright-continuity |
| Design | `bibles/props.json`, wardrobe, palette, `refs/`, `design.md` | cinewright-design (craft) |
| Shot list | `cards/*.json`, 3-8 s, one subject, one action, one move; `CINE cards list` | cinewright-shots; actions by cinewright-movement (craft) |
| Check | `continuity diff` with 0 errors | cinewright-continuity |
| Prompts | `compiled/<model>/` | cinewright-genvideo |
| Render | takes in `takes/` | the user's renderer, after their go if it costs money |
| QC | `qc/`, `takes/` | cinewright-qc |
| Edit | `edit/cut.md`, the locked cut | cinewright-edit (craft) |
| Grade, VFX, deliver | `finish/grade.md`, the delivery file | cinewright-finish (craft) |
| Sound and mix | `sound/plan.md`, the mix, `CINE qc loud --preset` | cinewright-sound (craft) |

1. Bibles come before cards, so `cards new` can copy identity strings.
2. After the cards, run `CINE cards validate <project>` and quote its last line.
3. A skill that is not installed: say "install cinewright-craft for <stage>" and do the stage with the rules in `kb show pipeline`.
4. Writing a prompt never authorises a paid render. Ask first, every time.

## Step 3: export for a local render pipeline

`CINE cards export <project> --film-json --out <project>/film.json` writes the shot list (name, size, seeds, lengths in frames, refs) for long-render pipelines that read that shape.

## Output

The project folder path, the stage reached, the evidence line of the last check, and the next single action.

## While working: capture learnings

If the user corrects you, the same error happens twice, or a workaround turns up, add an entry to [LEARNINGS.md](LEARNINGS.md) now (check existing entries first). If it proves a rule here wrong, fix the rule, log it in [CHANGELOG.md](CHANGELOG.md), and set `contradiction` in `evergreen.json`.

## Maintenance

This skill is evergreen (tier `moderate`; state in `evergreen.json`). Files: [RESEARCH.md](RESEARCH.md) (findings and search plan), [CHANGELOG.md](CHANGELOG.md), [LEARNINGS.md](LEARNINGS.md), [TESTS.md](TESTS.md) and `evals/evals.json`. How to maintain it, with or without the evergreen plugin: [MAINTENANCE.md](MAINTENANCE.md). Refresh with `evergreen-refresh`, test with `evergreen-test`, fix with `evergreen-tune`.
