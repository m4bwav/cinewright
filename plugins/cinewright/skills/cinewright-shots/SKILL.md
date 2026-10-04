---
name: cinewright-shots
description: "Shot list and coverage for AI video: blocking, which shots a scene needs, sizes, angles, moves, framing, cut order and grouping shots into generations. Use when breaking a script or scene into shots, planning coverage or a storyboard. Also 'refresh cinewright-shots'."
license: MIT
---

# cinewright-shots

Turn a scene into the shots the cut needs: block it, choose coverage, write one card per shot, put them in order and group them into generations. Outcome: blocked scene bibles, cards that validate, and a shot list printed from the cards.

`CINE` means `python scripts/cine.py` run from the folder holding this file (run it, never read it). Knowledge: read [references/INDEX.md](references/INDEX.md) once, then `CINE kb show <slug> --section Rules`. Never read the whole folder.

## Step 0: freshness

Read `evergreen.json`. If `contradiction` is set or today is on or after `next_due`, say so in one line, do the task with the current content, then run `evergreen-refresh` if the evergreen plugin is installed. If `tests.failing` is non-empty, say so and run `evergreen-tune` after the task.

## Step 1: block the scene

Before any card, write each person's position and travel as seen from camera side A into `bibles/scenes.json` (`kb show blocking`). The bibles must exist first (cinewright-continuity).

## Step 2: choose coverage

Pick the fewest shots the cut needs, plus one escape shot per scene (`kb show coverage`). For two people talking the default is master, matched singles, one insert.

## Step 3: write the cards

1. `CINE cards new <project> --id 1A --scene 1 --cast a,b` per shot; it copies identity and wardrobe from the bibles.
2. Fill one subject, one action, one camera move, 3-8 s, and a `beat`. Tokens: `kb show shot-sizes`, `kb show camera-angles`, `kb show camera-moves`.
3. Set `azimuth_deg` on every card. Two cuts in a row on one subject need 30 degrees or two size steps (`kb show thirty-degree-rule`).
4. Write framing as position words, never "rule of thirds" (`kb show framing`).
5. Hands, liquids, crowds, animals, fights: hand the action to cinewright-movement if installed; otherwise frame few subjects, large and side-on.

## Step 4: order and group

1. Set `order` for the cut; group consecutive cards of one scene and side into generations (`kb show shot-list-order`).
2. Run `CINE cards list <project>`, `CINE cards validate <project>` and `CINE continuity diff <project>`. Quote each last line; the shot list's last line is the evidence.
3. Hand the clean cards to cinewright-genvideo to compile. If it is not installed, say "install the cinewright plugin for prompt compiling".

## Output

The shot list table, the generation groups with their total seconds, and each card that needed a choice the rules could not make.

## While working: capture learnings

If the user corrects you, the same error happens twice, or a workaround turns up, add an entry to [LEARNINGS.md](LEARNINGS.md) now (check existing entries first). If it proves a rule here wrong, fix the rule, log it in [CHANGELOG.md](CHANGELOG.md), and set `contradiction` in `evergreen.json`.

## Maintenance

This skill is evergreen (tier `slow`; state in `evergreen.json`). Files: [RESEARCH.md](RESEARCH.md) (findings and search plan), [CHANGELOG.md](CHANGELOG.md), [LEARNINGS.md](LEARNINGS.md), [TESTS.md](TESTS.md) and `evals/evals.json`. How to maintain it, with or without the evergreen plugin: [MAINTENANCE.md](MAINTENANCE.md). Refresh with `evergreen-refresh`, test with `evergreen-test`, fix with `evergreen-tune`.
