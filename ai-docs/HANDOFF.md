# Handoff

## Current state
- S4 (camera, lighting and history) was done on 2026-10-04 on branch `s4/camera-history` off `main` (the S3 PR #4 was merged with no comments). Its PR waits for Mark's review: PR_LINK. The repo is private: https://github.com/m4bwav/cinewright.
- Built: `cinewright-camera` (9 entries) and `cinewright-history` (11 entries, about 70 style cards) in craft, each a full evergreen unit with evals and baselines; shared vocab `aspect-ratios`, `lens-terms`, `lighting-terms`. Runtime: style-bible fields `lighting`, `frame_aspect`, `allowed_moves`, `history`; `lens_family` now checked; compile guard for the style strings; LENS and MOVE diff warnings; `--style FILE` on validate, diff and compile; `uniqueItems` in the validator. 62 tests. Layout: [../CODEMAP.md](../CODEMAP.md).
- Mark asked mid-session for battle and fight coverage: fights already lived in movement's `fights-and-stunts`; S4 added movement's `battle-scenes` entry, and PLAN §2 and §10 S5 now name the post half (cutting a battle, crowd multiplication, battle sound).
- The example shows the exit check: [styles/new-hollywood-239.json](../examples/three-shot/styles/new-hollywood-239.json) compiled to `compiled/veo-new-hollywood/` ([README §7](../examples/three-shot/README.md)).
- Exit check outputs are quoted in [log.md](log.md). Decision: [style fields](decisions/2026-10-04-style-fields-carry-camera-and-history.md).

## In progress
- Mark's review of the S4 PR, and the open runtime budget row question ([decision](decisions/2026-10-04-proposed-runtime-budget-row.md)). The budget reads YELLOW on that one row: genvideo's folder at 156 of 150 KB (the runtime copy grew again in S4).

## Watch
- History timestamps marked `~` are approximate and unchecked against copies.
- Unverified per model: mm numbers, depth words, ratio words, shutter words and the 2.39 composition sentence. Check the crop on the first render with a `frame_aspect`.
- The style strings add about 45 words; the variant's 1A is at Veo's 250-word guide, and the H3 sequence would be over 400 words with it.
- Veo Gemini API preview IDs shut down 2026-10-22; re-check before any hosted render.
- Description budget: 10 skills use 3,044 of 4,000 characters; the remaining three need about 290 each.

## Next single action
- After Mark reviews the S4 PR, run [next-session-prompt.md](next-session-prompt.md) (S5: edit, finish, sound).
