---
name: cinewright-qc
description: "Checks rendered AI video takes against their shot cards: contact sheets, a per-shot rubric, spec and loudness checks with ffmpeg, failure codes routed to the cheapest fix. Use when reviewing a generated clip, deciding reroll or keep, or asking why a take failed. Also 'refresh cinewright-qc'."
license: MIT
---

# cinewright-qc

Judge each take against its card, not against taste, and turn every failure into one cheapest next change. Outcome: a contact sheet, a filled rubric, a take record with verdict and failure code, and the one change for the next take.

`CINE` means `python scripts/cine.py` run from the folder holding this file (run it, never read it). Knowledge: read [references/INDEX.md](references/INDEX.md) once, then `CINE kb show <slug> --section Rules`. Never read the whole folder. ffmpeg and ffprobe must be on PATH; if a command says they are missing, follow [SETUP.md](SETUP.md).

## Step 0: freshness

Read `evergreen.json`. If `contradiction` is set or today is on or after `next_due`, say so in one line, do the task, then run `evergreen-refresh` if the evergreen plugin is installed. If `tests.failing` is non-empty, say so and run `evergreen-tune` after the task.

## Step 1: measure

1. `CINE qc sheet <clip>` writes `<clip>.sheet.png` (2 fps up to 10 s, then 1 fps). Read the sheet once, whole; never one read per frame.
2. `CINE qc spec <clip> --project <p> --card <id> --params <compiled settings>`: fps, size, aspect, length, audio stream. For a multi-shot generation pass its label (`--card 1A+1B+1C`). Quote its last line.
3. `CINE qc measure <clip> --project <p> --card <label>`: machine checks a sheet misses (planned cuts found, early or late; frozen picture; dead air; clipping; speech where a line is planned; `--every <s>` adds seam level jumps in a cut film) and a 0-100 score. Its fails are facts to confirm in Step 2, not verdicts on look or acting. When takes compete, rank them on it before reading sheets.
4. `CINE takes lastframe <clip> --out <p>/qc/<id>-<n>.last.png` for the end state.

## Step 2: judge

1. `CINE qc rubric <p> --card <id> --clip <clip>` (no `--clip` before the first take) writes `<p>/qc/<id>.rubric.json`; never write a checklist by hand: one item per check the card makes possible (identity, wardrobe, props, positions, eyelines, light, camera, action, start and end state, text, sound, seam).
2. Fill each `verdict` with `pass`, `fail` or `na` from the sheet, the last frame and the audio. On a fail, set `code` from the item's `codes` and a `note` saying what you saw. Judge rules: `kb show qc-loop --section Rules`. An identity item with faces in a close shot can be scored against the bible's refs instead of by eye; wide shots stay by eye (`kb show identity-score`).
3. `CINE qc rubric --read <rubric>` prints the fails ordered by repair rung and the one change for the next take. Evidence: its last line.

## Step 3: log and route

1. `CINE takes log <p> --card <id> --model <m> --verdict <v> --fix <code> --file <clip> --change "<one change from the last take>"`. It finds the compiled prompt and settings and hashes the prompt.
2. Apply the printed fix (cinewright-genvideo recompiles; cinewright-continuity fixes cards). One change per reroll; a multi-shot generation gets one change across all its cards, the cheapest rung among them.
3. Three failed takes of one card: stop and re-plan the card (it prints when).
4. A pass: write what the last frame shows (`takes lastframe ... --take <record> --observed "..."`) and copy it into the next card's `start_state`.

A hosted re-render costs money: show the prompt, settings and cost, and ask first.

## Step 4: loudness at the mix

`CINE qc loud <mixed file> --preset <target>`: integrated loudness and true peak against a delivery preset (`web`, the default: -18 ± 2 LUFS, -2 dBTP; also `ebu-r128`, `atsc-a85`, `netflix`, `music-streaming`; `kb show loudness-targets`).

## Output

The sheet path, the rubric's last line, the take record path, and the one change for the next take (or "pass").

## While working: capture learnings

If the user corrects a verdict, the same failure survives its fix twice, or a code is missing, add an entry to [LEARNINGS.md](LEARNINGS.md) now (check existing entries first). If it proves a rule here wrong, fix the rule, log it in [CHANGELOG.md](CHANGELOG.md), and set `contradiction` in `evergreen.json`.

## Maintenance

This skill is evergreen (tier `moderate`; state in `evergreen.json`). Files: [RESEARCH.md](RESEARCH.md), [CHANGELOG.md](CHANGELOG.md), [LEARNINGS.md](LEARNINGS.md), [TESTS.md](TESTS.md), [SETUP.md](SETUP.md) and `evals/evals.json`. How to maintain it, with or without the evergreen plugin: [MAINTENANCE.md](MAINTENANCE.md). Refresh with `evergreen-refresh`, test with `evergreen-test`, fix with `evergreen-tune`.
