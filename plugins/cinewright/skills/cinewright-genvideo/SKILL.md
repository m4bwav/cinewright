---
name: cinewright-genvideo
description: "AI video prompts: compiles a shot card plus bibles into one model's prompt and settings (Veo 3.1 now; Kling, Seedance, Runway, Luma, Wan, LTX-2, MiniMax H3 later), with refs, seeds and takes. Use when writing a Veo prompt or turning a shot list into video-model prompts. Also 'refresh cinewright-genvideo'."
license: MIT
---

# cinewright-genvideo

Turn checked shot cards into prompts a given video model follows, without retyping identity, wardrobe or direction by hand. Outcome: one prompt file and one settings file per card in `compiled/<model>/`. Stub: only the Veo 3.1 card exists so far.

`CINE` means `python scripts/cine.py` run from the folder holding this file (run it, never read it). Knowledge: read [references/INDEX.md](references/INDEX.md) once, then `CINE kb show <slug> --section Rules`. Never read the whole folder.

## Step 0: freshness

Read `evergreen.json`. This skill has `verify_at_use` on: before relying on a model card, re-check its `volatile_claims` (frontmatter) with one search each, and say in one line if any changed. If `contradiction` is set or today is on or after `next_due`, say so, do the task, then run `evergreen-refresh` if the evergreen plugin is installed.

## Step 1: check before compiling

Cards must pass `CINE continuity diff <project>` with 0 errors (cinewright-continuity). Compiling a broken card spreads the error to every take.

## Step 2: compile

1. Pick the model card: `CINE kb show veo-3-1 --section Numbers`. Check the style bible's aspect and resolution are on the list.
2. Run `CINE compile <project> --model veo --out <project>/compiled/veo`. Evidence: the line `wrote N prompts to ...` and the files.
3. Read each warning. A duration warning means trim in the edit; a word warning means shorten action or context, never the identity string.
4. Several short cards of one scene in one generation: add `--sequence` (timestamp blocks).

The compile rule (what goes where, and why): `kb show compile-rule`.

## Step 3: render and log

- A render on a hosted model costs money. Show the prompt and settings and ask before any call. Local renders need no ask.
- One change per reroll. Keep the seed when only the end of a take is wrong; change it when the opening is wrong.
- Record each take in `takes/<card>-<n>.json` (shape: `scripts/schemas/take.schema.json`).

## Output

The compiled file paths, each warning with what you did about it, and the settings to use.

## While working: capture learnings

If the user corrects you, a model ignores part of a prompt twice, or a workaround turns up, add an entry to [LEARNINGS.md](LEARNINGS.md) now (check existing entries first). If it proves a card wrong, fix the card, log it in [CHANGELOG.md](CHANGELOG.md), and set `contradiction` in `evergreen.json`.

## Maintenance

This skill is evergreen (tier `fast`, `verify_at_use`; state in `evergreen.json`). Files: [RESEARCH.md](RESEARCH.md) (findings and search plan), [CHANGELOG.md](CHANGELOG.md), [LEARNINGS.md](LEARNINGS.md), [TESTS.md](TESTS.md) and `evals/evals.json`. How to maintain it, with or without the evergreen plugin: [MAINTENANCE.md](MAINTENANCE.md). Refresh with `evergreen-refresh`, test with `evergreen-test`, fix with `evergreen-tune`.
