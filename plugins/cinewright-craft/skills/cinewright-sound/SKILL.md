---
name: cinewright-sound
description: "Sound designer and mixer for AI video: layers, stems, foley, music, Chion's terms, generated audio, battle sound, mixing to a loudness target (EBU R128, ATSC, Netflix, web). Use when adding sound to or mixing clips. Also 'refresh cinewright-sound'."
license: MIT
---

# cinewright-sound

Give the locked cut a full soundtrack and mix it to a stated delivery target: every layer planned, generated audio cleaned up or replaced, the loudness reached once on the whole mix and proven by the meter. Outcome: `sound/plan.md`, the mix (and stems), and a passing `qc loud` quoted against the target.

`CINE` means `python scripts/cine.py` run from the folder holding this file (run it, never read it). Knowledge: read [references/INDEX.md](references/INDEX.md) once, then `CINE kb show <slug> --section Rules`. Never read the whole folder.

## Step 0: freshness

Read `evergreen.json`. If `contradiction` is set or today is on or after `next_due`, say so in one line, do the task with the current content, then run `evergreen-refresh` if the evergreen plugin is installed. If `tests.failing` is non-empty, say so and run `evergreen-tune` after the task.

## Step 1: target and inputs

1. State the delivery target in one line before any mixing (`kb show loudness-targets`). No target given: web (-18 ± 2 LUFS, -2 dBTP).
2. A locked cut from cinewright-edit. Probe its audio: codec, sample rate, channels, loudness (`CINE qc loud <cut>`); read each card's `dialogue` and `sound`.

## Step 2: plan the layers

1. Per scene: dialogue, hard effects, foley, ambience, room tone, music (`kb show sound-layers`). Every visible contact gets a sound.
2. Decide what is on screen, off screen and acousmatic, and whether the score follows the feeling (`kb show chion-terms`).
3. Battles: near, mid and far layers, a bed per phase, silence at the turn (`kb show battle-sound`).
4. Music cues spotted on story beats with source and license (`kb show music-spotting`).
5. Write it all in `sound/plan.md`.

## Step 3: generated audio

Resample to 48 kHz, keep the usable dialogue, cover seams with continuous ambience and room tone, put impacts on the frame of contact (`kb show generated-audio`; split edits: `kb show cut-terms`).

## Step 4: mix and loudness

1. Mix in order: dialogue, effects, ambience, music (`kb show mix-and-loudness`).
2. Reach the target once on the whole mix: measure, gain and limiter if the peak needs room, then a linear loudnorm pass.
3. Run `CINE qc loud <mix> --preset <target>` on the mix and on the delivery file; both must PASS. Quote the lines.
4. Stems (dialogue, music, effects) take the same gain as the mix.

## Output

The stated target, `sound/plan.md`, the mix and stems, and both `qc loud` results.

## While working: capture learnings

If the user corrects you, the same error happens twice, or a workaround turns up, add an entry to [LEARNINGS.md](LEARNINGS.md) now (check existing entries first). If it proves a rule here wrong, fix the rule, log it in [CHANGELOG.md](CHANGELOG.md), and set `contradiction` in `evergreen.json`.

## Maintenance

This skill is evergreen (tier `moderate`; state in `evergreen.json`). Files: [RESEARCH.md](RESEARCH.md) (findings and search plan), [CHANGELOG.md](CHANGELOG.md), [LEARNINGS.md](LEARNINGS.md), [TESTS.md](TESTS.md) and `evals/evals.json`. How to maintain it, with or without the evergreen plugin: [MAINTENANCE.md](MAINTENANCE.md). Refresh with `evergreen-refresh`, test with `evergreen-test`, fix with `evergreen-tune`.
