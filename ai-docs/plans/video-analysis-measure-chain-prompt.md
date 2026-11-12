# Chain prompt: cinewright video analysis, benchmark measurement and proof

This prompt does not change between sessions. State lives in `D:/m4bwa/Claude/Projects/Ai/cinewright/ai-docs/chains/video-analysis/build/measure/HANDOFF.md`, never here. Work in the cinewright repo (`D:/m4bwa/Claude/Projects/Ai/cinewright`).

## Load state first

1. Read the goal, motivating failure and stop points in `D:/m4bwa/Claude/Projects/Ai/cinewright/ai-docs/plans/2026-11-11-video-analysis-continue-prompt.md` (do not run its order of work; this chain owns only the part below).
2. Read this chain's HANDOFF.md, then the "Video analysis track" section of `ai-docs/HANDOFF.md`, the newest `ai-docs/log.md` entries, `AGENTS.md` and `CODEMAP.md`.
3. Compare HANDOFF.md's age with the log and git commits; trust the newer evidence.

## This chain's work, in order

1. Prove it on the benchmark: find the Project Nexus character height in SceneTools units (the brief assumes 2.0, unverified), write a madnesswright issue or brief with room 1 at about 6.2 x 3.2 H, and a side-by-side render with a character at the back wall.
2. Pan on cel animation: ORB or landmark matching on the background instead of whole-frame phase correlation (L-20261111-2), so `pan_px` works on the benchmark.
3. Measure rooms 2-10 of the benchmark and fill the notation from shots (Gemini draft plus frames).

## Stop early

Stop with `Status: waiting` when the next step needs Mark: paid API spend past a small test, any madnesswright change beyond a brief or issue, or a release that renames public skills. Put the question on an askwright page, name the set in HANDOFF.md, and do every other step first. After the last step, write `Status: finished`.

## Hand-over

- Commit on a branch, open a PR, merge it yourself once checks pass (global rules); tag and release if the version is bumped, then update installed plugins. Other chains share this repo: pull before branching, keep PRs small.
- Log the session in `ai-docs/log.md`; research in `ai-docs/research/`.
- Last steps, in order: run evergreen-wrapup (skip quietly if absent; report a failure, never block), update this chain's HANDOFF.md (done, next, waiting on Mark, Status), then end with only this report: outcome (worked, idle, waiting, finished, failed); one line on what changed; questions page if any; HANDOFF.md path. When run by hand, print exactly:

`Execute D:/m4bwa/Claude/Projects/Ai/cinewright/ai-docs/plans/video-analysis-measure-chain-prompt.md`
