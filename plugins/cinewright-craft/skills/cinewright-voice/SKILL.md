---
name: cinewright-voice
description: "Voice director for AI video: a voice sheet and locked reference clips per character, designed new or cut from generated takes, so every line sounds like the same person in every shot; TTS cloning, ComfyUI and Ollama routes, drift checks. Use when a film's character voices must match; not podcasts or app TTS. Also 'refresh cinewright-voice'."
license: MIT
---

# cinewright-voice

Give every speaking character one voice that holds across shots and sessions: a voice sheet, a locked reference bank, the exact engine settings, and a measured check on every new line. Outcome: `bibles/voices.json`, the clips under `voices/<character>/`, and a passing `voice check` per line.

`CINE` means `python scripts/cine.py` run from the folder holding this file (run it, never read it). Knowledge: read [references/INDEX.md](references/INDEX.md) once, then `CINE kb show <slug> --section Rules`. Never read the whole folder.

## Step 0: freshness

Read `evergreen.json`. If `contradiction` is set or today is on or after `next_due`, say so in one line, do the task with the current content, then run `evergreen-refresh` if the evergreen plugin is installed. If `verify_at_use` is true, re-check the due engine claims first (`kb show voice-engines --section Notes`). If `tests.failing` is non-empty, say so and run `evergreen-tune` after the task.

## Step 1: who speaks, which route

1. List the speakers from the cards' `dialogue` (or the script). Each needs a voice; a one-line extra can share a library voice.
2. Rights first: a real person's voice needs their written consent for this use; a living actor's or celebrity's sound-alike is out. Write `rights` per voice (`kb show voice-rights`).
3. Pick the route, one per film, and say it in one line (`kb show voice-engines`):
   - Default: design or clone with an open engine (Qwen3-TTS), in ComfyUI if the user runs it (`kb show comfyui-voice`).
   - Hosted: ElevenLabs when the user has an account.
   - Video model speaks the lines: Kling 3 voice binding, else the prompt's voice string plus a fix later (`kb show video-model-voices`).

## Step 2: the voice sheet

1. Fill `sheet` per character: age, gender, pitch, pace, timbre, then accent, energy, attitude, quirks (`kb show voice-sheet`).
2. Condense it to the short `voice` string in characters.json ("low, dry, unhurried"); compile copies that string into every prompt, so it never changes after the first render.
3. A local model can draft sheets and design prompts from the character bible (local-delegate skill or Ollama, `kb show ollama-voice`); you check them.

## Step 3a: a new voice

Write the design prompt from the sheet, generate 3-5 candidates on one fixed test line, pick one with the user, then lock it: a neutral reference clip with its exact words, the engine, model, voice id, seed and settings (`kb show voice-design`).

## Step 3b: from generated takes

Pick the takes where the character sounds right, cut each line out where nothing plays under it, and turn the best into references: `CINE voice ref <take> --start S --end E --out voices/<id>/neutral.wav --text "<line>"` (`kb show reference-clips`). Use the script's line as the transcript; check it by ear or ASR, never trust an LLM's hearing of names.

## Step 4: lock the bank

1. Neutral first, then one clip per emotion the script needs (angry, whisper, shout), each 3-30 s of dry speech.
2. Write `bibles/voices.json` (schema `scripts/schemas/voice-bible.schema.json`) and run `CINE voice check <project>`; fix every error.

## Step 5: every new line

1. Generate with the locked reference and settings only; one change per retry.
2. `CINE voice check <project> --character <id> --clip <line.wav> --text "<line>"`. DRIFT: regenerate; still off, convert the take to the reference voice; still off, re-cast (`kb show voice-conversion`, `kb show voice-measure`).
3. Pitch and pace are not identity: listen to each pass, or run a speaker-embedding check against the reference.
4. Replacing a video's dialogue: lip-sync the picture to the new line, or convert the take's own audio to keep its timing (`kb show video-model-voices`).

## Output

The route, `bibles/voices.json`, the reference clips, `voice check` lines for every delivered line, and anything unheard marked so.

## While working: capture learnings

If the user corrects you, the same error happens twice, or a workaround turns up, add an entry to [LEARNINGS.md](LEARNINGS.md) now (check existing entries first). If it proves a rule here wrong, fix the rule, log it in [CHANGELOG.md](CHANGELOG.md), and set `contradiction` in `evergreen.json`.

## Maintenance

This skill is evergreen (tier `fast`; state in `evergreen.json`). Files: [RESEARCH.md](RESEARCH.md), [CHANGELOG.md](CHANGELOG.md), [LEARNINGS.md](LEARNINGS.md), [TESTS.md](TESTS.md), `evals/evals.json`, [SETUP.md](SETUP.md) (ffmpeg; optional ComfyUI, Ollama, hosted keys). How to maintain it, with or without the evergreen plugin: [MAINTENANCE.md](MAINTENANCE.md). Refresh with `evergreen-refresh`, test with `evergreen-test`, fix with `evergreen-tune`.
