# Handoff

## Current state
- S5 (post: edit, finish, sound) was done on 2026-10-04 on branch `s5/post`, off `s4/camera-history` because the S4 PR #5 (https://github.com/m4bwav/cinewright/pull/5) was still open with no comments. The S5 PR waits for Mark's review: see the log's S5 entry for its link. The repo is private: https://github.com/m4bwav/cinewright.
- Built: `cinewright-edit` (8 entries), `cinewright-finish` (8) and `cinewright-sound` (6 plus the shared `loudness-targets`) in craft, each a full evergreen unit with evals and baselines; shared vocab `cut-terms` and `loudness-targets`. Runtime: `qc loud --preset web|ebu-r128|atsc-a85|netflix|music-streaming`, default web (-18 ± 2 LUFS, -2 dBTP) ([decision](decisions/2026-10-04-loudness-presets-with-a-web-default.md)). 63 tests. Layout: [../CODEMAP.md](../CODEMAP.md).
- Exit check passed: the S2 render cut to 336 frames (14.000 s), balanced and graded with bt709 tags, mixed to -17.6 LUFS and -6.3 dBTP; `qc loud --preset web` and `qc spec` pass. Numbers in [examples/three-shot/README.md §8](../examples/three-shot/README.md); outputs quoted in [log.md](log.md); media and the text records stay in the local render folder (private note in the vault sidecar).
- Loudness targets were re-verified from primary pages; the research brief's R128 ±0.5 LU tolerance was wrong and A/85 was revised in July 2026.

## In progress
- Mark's review of the S4 and S5 PRs, and the open runtime budget row question ([decision](decisions/2026-10-04-proposed-runtime-budget-row.md)). The budget reads YELLOW on that one row: genvideo's folder at 157 of 150 KB.

## Watch
- Outcome cases that do not discriminate: camera, history, sound (replace in S6). Finish and sound action cases need ffmpeg, which Bash-denied baselines cannot reach.
- Description budget: 13 skills use 3,799 of 4,000 characters; curate has about 200 left.
- Unverified: YouTube -14 LUFS, Apple Music -16, AES TD1008; DCI 14 fL in the main spec; ATSC and Netflix presets are approximate (no dialogue gate in ebur128).
- Veo Gemini API preview IDs shut down 2026-10-22; re-check before any hosted render.
- History timestamps marked `~` and per-model claims (mm numbers, depth words, the 2.39 sentence) stay unverified.

## Next single action
- After Mark reviews the S4 and S5 PRs, run [next-session-prompt.md](next-session-prompt.md) (S6: evals and tuning).
