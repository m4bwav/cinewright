# cinewright: session S6 (evals and tuning)

You are running stage S6 of cinewright, a plugin set for AI video that is private now and public at release, maintained as evergreen units. It gives an agent the craft of every film role plus AI video generation, so generated video holds together within and between shots. S1 built the scaffold, the router, continuity and the `cine.py` CLI. S2 added nine model cards with compilers, the failure codes and `cinewright-qc`. S3 added shots, script, design and movement. S4 added camera and history and the style-bible look fields. S5 added `cinewright-edit`, `cinewright-finish` and `cinewright-sound`, shared vocab `cut-terms` and `loudness-targets`, `qc loud --preset` (default web, -18 ± 2 LUFS, -2 dBTP), and cut, graded and mixed the S2 render to that target. Thirteen skills now exist, each with 2 trigger cases, 2 decoys, 1 action case, 1 outcome case and a one-run baseline. This session runs the suite and tunes what fails. It does not build `cinewright-curate` or package anything (S7).

## Read first (only these, in order)

1. `ai-docs/HANDOFF.md`, then Mark's reviews: `gh pr list -R m4bwav/cinewright --state all`, then `gh pr view <n> -R m4bwav/cinewright --comments` for the S4 PR (#5) and the S5 PR. Branch `s6/evals` off `main` if both are merged; otherwise off the newest open stage branch, and say which. Make any changes he asked for first. The runtime budget row question (`ai-docs/decisions/2026-10-04-proposed-runtime-budget-row.md`) may be answered there: apply his answer. Until then the genvideo folder stays yellow and is reported, not cut.
2. `ai-docs/plans/PLAN.md` §8 (proof), §6 (budgets), §10 S6. This is the spec.
3. The evergreen protocol's TESTING.md (find the plugin with `evergreen.py where`) and the `evergreen-test`, `evergreen-tune` and `evergreen-worth` skills.
4. One unit's tests as the shape: `plugins/cinewright-craft/skills/cinewright-sound/evals/evals.json` and its TESTS.md. Then the S4 and S5 baseline notes in `ai-docs/log.md` (how the scratch folder, the stripped example and the denied tools were set up, and what went wrong).

## The step

1. Harness, written once as a script under `evals/` (committed; no private paths, results data stays private): for each case, a fresh scratch folder on a drive other than the repository's with a copy of the fixtures, `claude -p --plugin-dir` for with-skill runs (the plugin under test only), skills disabled for baselines, `--strict-mcp-config`, a stream-json trace, and a scan of every tool input for paths outside the folder. Deny web, agent, Glob, Grep, Skill (baselines) and ToolSearch (it can load Bash). Action cases that need ffmpeg (finish, sound) get Bash limited to `ffmpeg`, `ffprobe` and `python scripts/cine.py`; the S5 Bash-denied baselines could not reach them. On Windows start `claude` by its full path from `shutil.which`. Mark any run that touched the repository as contaminated and rerun it.
2. Run every case three times on Haiku, Sonnet and Opus with the skill installed; baselines once per model for action and outcome cases. Pass marks: trigger 2 of 3 or better, decoy 0 of 3, action and outcome on evidence outside the transcript (TESTING.md). Add decoys against neighbours (chartwright, threewright, comfyui-gen, generic video editing) where a skill's description could catch them.
3. Replace the outcome cases that did not discriminate in baselines: camera, history and sound (each TESTS.md says so). The new case must need something only the skill gives (a style field, a diff warning, a preset).
4. Tune failures with `evergreen-tune`: reproduce, classify, write the learning in that skill's LEARNINGS, smallest edit, rerun; three iterations at most per case. Watch the description budget (3,799 of 4,000 characters for 13 skills, curate still to come at about 200).
5. Worth check per skill (`evergreen.py worth`, with and without the skill on its own cases). Merge or cut a skill only on evidence, and only after asking Mark. PLAN §2 names one candidate: shots and continuity, if they overlap on triggers.
6. Record every run as a `T-` entry in that skill's TESTS.md (model per entry), update `evergreen.json.tests`, and summarise the matrix in `ai-docs/log.md`.

## Rules

- No AI attribution anywhere: commits, PRs, files.
- Public-repo hygiene: no LAN IPs, hostnames, GPU model, local paths under `D:/`, or names of Mark's private projects in any shipped file, eval prompt or harness. `cine.py kb lint` catches paths, LAN addresses and GPU names; names are on you. Raw traces stay outside the repository; private notes go in the vault sidecar (`everlast.py note --private`).
- A test passes on evidence, never on the reply's claim. Write knowledge edits as rules, numbers and vocabulary; one default, not a menu; do not cite a page you have not checked this session.
- Use relative markdown links, never wikilinks. Cite lessons with their code names. Inside a unit's companions, a lesson ID from another unit carries the full unit name (`cinewright-qc L-001`); evergreen lint still rejects a cross-unit `R-` ID, so cite another unit's research by file name.
- Edit `shared/`, then run `python scripts/cine.py build`; never edit the copies inside skills.
- Run commands yourself; never hand them to Mark. Python 3.9+, standard library only; test on 3.9 too (`py -V:Astral/CPython3.9.25`).
- Heredocs in the Bash tool mangle `\\` and some apostrophes: write patch scripts with the Write tool and run them. Print reports with `sys.stdout.reconfigure(encoding="utf-8")`; a cp1252 console crashed the S5 report on an arrow.
- At a yellow budget reading, tell Mark in one line and keep going; a red reading fails the build.
- Record as you go: `ai-docs/log.md`, LEARNINGS in the skill that taught the lesson, decisions in `ai-docs/decisions/`.

## Stop and ask Mark when

- Before the full three-model run: state the number of headless runs and the expected agent time in one line and wait for his go (the matrix is about 13 skills × 6 cases × 3 runs × 3 models plus baselines, near 750 runs).
- Before merging or cutting any skill.
- When S6's exit check passes: every case passes on all three models or carries a recorded reason, no skill is marked CUT by the worth check, results are in each TESTS.md; tests (3.x and 3.9), `kb lint` and `budget` pass (green, or yellow only on rows Mark has been told about); `claude plugin validate` passes on the root and on each plugin; `evergreen.py lint` passes on each skill; all of it quoted in the log. Then open a PR, assign `m4bwav`, add the `needs-review` label, give him the PR link and a short summary of what works, and stop. The PR holds code, so it waits for his review; do not merge it. Also stop before any hosted render, before publishing anything (the repo stays private), and before changing another repo.

## Chain rule

When this session's step is done, rewrite `ai-docs/next-session-prompt.md` as the prompt for the next fresh session: what to read first (only what that step needs), the step and its limits, the rules, when to stop and ask, and this paragraph unchanged at the end. Commit it with the handoff and paste it in your final message.
