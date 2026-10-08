---
name: cinewright-genvideo
description: "Writes AI video prompts: compiles shot cards plus bibles into one model's prompt and settings (Veo, Gemini Omni, Kling, Seedance, Runway, Luma, MiniMax H3, Wan, LTX-2), with refs, seeds, takes and cost. Use when asked for a prompt for one of these models or to turn shots into video-model prompts. Also 'refresh cinewright-genvideo'."
license: MIT
---

# cinewright-genvideo

Turn checked shot cards into prompts a given video model follows, without retyping identity, wardrobe or direction by hand. Outcome: one prompt file and one settings file per card (or per multi-shot generation) in `compiled/<model>/`.

`CINE` means `python scripts/cine.py` run from the folder holding this file (run it, never read it). Knowledge: read [references/INDEX.md](references/INDEX.md) once, then `CINE kb show <slug> --section Rules`. Never read the whole folder.

## Step 0: freshness

Read `evergreen.json`. This skill has `verify_at_use` on: before relying on a model card, re-check its `volatile_claims` (frontmatter) with one search each, and say in one line if any changed. If `contradiction` is set or today is on or after `next_due`, say so, do the task, then run `evergreen-refresh` if the evergreen plugin is installed.

## Step 1: check before compiling

Cards must pass `CINE continuity diff <project>` with 0 errors (cinewright-continuity). Compiling a broken card spreads the error to every take.

## Step 2: compile

1. Pick the model the user renders with. Keys and cards: `veo` (veo-3-1), `omni` (gemini-omni), `kling` (kling-3), `seedance` (seedance-2-5), `runway` (runway-gen-4-5), `luma` (luma-ray-3-2), `minimax-h3`, `wan` (wan-2-2), `ltx2` (ltx-2). Read its Rules and Numbers: `CINE kb show <card> --section Rules`.
2. Run `CINE compile <project> --model <key> --out <project>/compiled/<key>`. A size the model lacks stops the compile: change the bible or pass `--resolution` (a cheap local draft). Evidence: the line `wrote N prompts to ...` and the files.
3. Read each warning. A duration warning means trim in the edit; a word warning means shorten action or context, never the identity string.
4. Several cards of one scene in one generation, when the model has multi-shot syntax: add `--sequence`. Prefer it: every seam between generations can read as a restart. An establishing exterior before an interior goes in the same generation with `--join` (its card in its own scene): the new place is then named at the cut, else the model furnishes the exterior from the interior's words. Score under a card goes in its `music` field.
5. Hosted models print `est. $` per prompt: quote it when asking for the go.

The compile rule (what goes where, and why): `kb show compile-rule`.

## Step 3: render and log

- A render on a hosted model costs money. Show the prompt and settings and ask before any call. Local renders need no ask.
- One change per reroll. Keep the seed when only the end of a take is wrong; change it when the opening is wrong.
- Record each take with `CINE takes log` and judge it with cinewright-qc. Failure codes and fixes: `kb show failures-picture`, `kb show failures-motion`.

## Output

The compiled file paths, each warning with what you did about it, and the settings to use.

## While working: capture learnings

If the user corrects you, a model ignores part of a prompt twice, or a workaround turns up, add an entry to [LEARNINGS.md](LEARNINGS.md) now (check existing entries first). If it proves a card wrong, fix the card, log it in [CHANGELOG.md](CHANGELOG.md), and set `contradiction` in `evergreen.json`.

## Maintenance

This skill is evergreen (tier `fast`, `verify_at_use`; state in `evergreen.json`). Files: [RESEARCH.md](RESEARCH.md) (findings and search plan), [CHANGELOG.md](CHANGELOG.md), [LEARNINGS.md](LEARNINGS.md), [TESTS.md](TESTS.md) and `evals/evals.json`. How to maintain it, with or without the evergreen plugin: [MAINTENANCE.md](MAINTENANCE.md). Refresh with `evergreen-refresh`, test with `evergreen-test`, fix with `evergreen-tune`.
