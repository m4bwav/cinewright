---
name: cinewright-analyze
description: "Take an existing video apart into film notation and rebuild from it: shots, camera moves, sets measured in character heights, blocking, cast, props, audio; then shot cards or a game level brief. Also judges whether a video is AI-made. Use on 'break down this film', 'shot list from this YouTube video', 'how big is this room', 'rebuild this set as a level', 'is this video AI'. Not for checking your own rendered take against its shot card (keep or reroll): that is cinewright-qc. Also 'refresh cinewright-analyze'."
license: MIT
---

# cinewright-analyze

Turn a video into a film notation file (`<name>.notation.json`, schema `scripts/schemas/film-notation.schema.json`) whose sizes are measured, not guessed, and rebuild from it. Outcome: the notation, its Markdown view, and the cards or level brief asked for, each set marked measured, estimated or guess.

`AN` means `python scripts/cine_analyze.py` run from the folder holding this file (run it, never read it). `CINE` means `python scripts/cine.py`. Knowledge: read [references/INDEX.md](references/INDEX.md) once, then `CINE kb show <slug> --section Rules`.

## Step 0: freshness

Read `evergreen.json`. If `contradiction` is set or today is on or after `next_due`, say so in one line, do the task, then run `evergreen-refresh` if the evergreen plugin is installed.

## Step 1: get the video and cut it into shots

YouTube: download with `uvx yt-dlp -S res:720` into a work folder outside any repo (the film's art is not ours). Run `AN probe VIDEO`, then `AN shots VIDEO --out NAME.notation.json`. Animation flashes cause false cuts: check any shot under 0.6 s against the frames either side before trusting it (`kb show film-notation`).

## Step 2: describe each shot

Fill size, angle, move, cast, action, dialogue, sfx and on-screen text per shot from frames (`AN frame VIDEO --at T --grid 0`). For long films a Gemini pass on the URL can draft the descriptions with timestamps; check its timecodes against the shot list (`kb show extraction-routes`). Group shots into scenes and sets.

## Step 3: measure every set

Never size a room by eye or as a multiple of some template. For each set pick a frame with a standing character near the back wall and both corners if possible: `AN frame VIDEO --at T --out F.png` (50 px grid), read the points into a measure file, run `AN scale MEASURE.json` (`kb show room-scale`). Walls wider than one frame: measure across the pan and add `pan_px`. Write width_H, height_H, depth_H, camera and confidence into the set, with `measured_from`.

## Step 4: rebuild

`AN notate NAME.notation.json --out NAME.notation.md` (validates). Shot cards: `AN rebuild NAME.notation.json --cards DIR`, then hand them to cinewright-shots and cinewright-continuity. Game level: `AN rebuild ... --level BRIEF.md --char-height <engine units per character>`; hand the brief to the level's builder (madnesswright-scenes for Project Nexus).

## Step 5: compare

Put one film frame beside a render of the rebuild taken from a matching camera, with a character of known height at the back wall in both. Wall width and height in characters must agree within 15%; say which do not.

## AI-made video

Asked whether a video is AI: run `AN aidetect VIDEO --out DIR` (needs opencv-python and numpy), then follow `kb show ai-video-tells`: provenance first, then sampled frames against the checklist, an answer in confidence bands with timestamps, never a flat yes or no.

## Output

The notation path, the sets table (sizes in H with confidence), files written, and the comparison result.
