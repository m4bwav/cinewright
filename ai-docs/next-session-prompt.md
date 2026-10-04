# cinewright: session S5 (post: edit, finish, sound)

You are building stage S5 of cinewright, a plugin set for AI video that is private now and public at release, maintained as evergreen units. It gives an agent the craft of every film role plus AI video generation, so generated video holds together within and between shots. S1 built the scaffold, the router, continuity and the `cine.py` CLI. S2 added nine model cards with compilers, the failure codes and `cinewright-qc`. S3 added `cinewright-shots` (core) and `cinewright-script`, `cinewright-design` and `cinewright-movement` (craft). S4 added `cinewright-camera` and `cinewright-history`, style-bible fields (`lighting`, `frame_aspect`, `allowed_moves`, `history`, a checked `lens_family`), `--style FILE`, LENS and MOVE diff warnings, and a `battle-scenes` entry in movement. This session writes `cinewright-edit`, `cinewright-finish` and `cinewright-sound`. It does not touch evals tuning (S6) or packaging (S7).

## Read first (only these, in order)

1. `ai-docs/HANDOFF.md`, then Mark's review of the S4 PR (`gh pr list -R m4bwav/cinewright --state all`, then `gh pr view <n> -R m4bwav/cinewright --comments`). If the S4 PR is still open, branch `s5/post` off `s4/camera-history` and say so; if merged, branch off `main`. If he asked for changes, make those first. The runtime budget row question (`ai-docs/decisions/2026-10-04-proposed-runtime-budget-row.md`) may be answered there: apply his answer. Until he answers, the genvideo folder stays yellow and is reported, not cut.
2. `ai-docs/decisions/`, newest first: style fields (S4), prop bible, runtime budget row, shared copies with hash headers, failure codes, render media location.
3. `ai-docs/plans/PLAN.md` §2 (edit, finish, sound are `cinewright-craft`; finish and sound rows now name battle work), §5 (`qc loud`), §6 budgets, §7 tiers (edit slow, finish and sound moderate), §10 S5. This is the spec.
4. `CODEMAP.md`. Run `python scripts/cine.py --help`; read only the functions you change (likely `cmd_qc` and `loudness`).
5. Brief §3 rows for editing, color and finishing, VFX, sound and music; §4 sources (`ai-docs/research/2026-10-03-research-brief.md`). Cite books, never copy them.
6. One S4 skill as the template for a full unit: `plugins/cinewright-craft/skills/cinewright-camera/` (SKILL.md, companions, evals with baselines). Keep these links true: camera's `exposure` and `frame-rate-and-shutter` hand day-for-night and interpolation to cinewright-finish; history's `applying-styles` sends cut and sound tags to cinewright-edit and cinewright-sound; movement's `battle-scenes` sends crowd multiplication to cinewright-finish.

## The step

1. Three skills in `plugins/cinewright-craft`, each a full evergreen unit: SKILL.md of 80 lines or fewer, RESEARCH, CHANGELOG, LEARNINGS, TESTS, MAINTENANCE, evergreen.json (edit `slow`, finish and sound `moderate`), needs.json, and evals with 2 triggers, 2 decoys, 1 action, 1 outcome and baselines without the skill. Run baselines the S4 way (see `ai-docs/log.md` S4 and the camera TESTS.md): a scratch folder outside the repository with a stripped copy of the fixtures, Bash and web tools denied, Glob and Grep denied too or kept inside the folder (they can search outside it: cinewright-history L-002), the trace scanned for outside paths; mark any run that touched the repository as contaminated. On Windows call `claude` by its full path from `shutil.which`. List all three in both craft `plugin.json` files, the marketplace description and the README.
2. Knowledge entries, rules and numbers: edit (Murch's rule of six, J and L cuts, match cuts, cutting on action, pacing and average shot length, cutting around bad frames, cutting a battle with geography wides between fights); finish (grade order correct, balance, match, look; scene- and display-referred; ACES or log to Rec.709; delivery color spaces; the crop to the style's `frame_aspect`; day for night; crowd multiplication and cleanup in compositing; upscale and interpolation last); sound (layers, stems, Chion's terms, battle layers, loudness targets re-verified this session: EBU R128 v4, ATSC A/85, Netflix, web). Shared vocabulary goes in `shared/vocab/` when two skills need it.
3. Exit check from PLAN §10: the S2 render cut, graded and mixed to a stated target, `qc loud` within tolerance. The render media stays in the local render folder (decision); the repo gets commands, numbers and lessons only. If the S2 media cannot be found, say so before rendering anything new.
4. Any runtime change (for example a crop or a loudness preset in `qc`) goes into `shared/lib/cine.py` with a test, then `build`.
5. Budgets: each SKILL.md and entry green. The 10 descriptions total 3,044 characters; all 13 must stay under 4,000 (curate counts too when it exists), so keep each new description near 290. Measure after each skill.

## Rules

- No AI attribution anywhere: commits, PRs, files.
- Public-repo hygiene: no LAN IPs, hostnames, GPU model, local paths under `D:/`, or names of Mark's private projects in any shipped file. `cine.py kb lint` catches paths, LAN addresses and GPU names; names are on you. Private notes go in the vault sidecar (`everlast.py note --private`).
- Write knowledge as rules, numbers and vocabulary. One default, not a menu. Cite primary sources, mark what is unverified, and date what changes. Do not cite a paper or URL you have not checked this session.
- Take ideas from other skill repos, never text. Nothing adapted from smixs/visual-skills without attribution.
- Use relative markdown links, never wikilinks. Cite lessons with their code names; cite private field lessons as "field lesson NNN" with a title. Inside a unit's companions, a lesson ID from another unit must carry the full unit name (`cinewright-qc L-001`) or evergreen lint fails.
- Edit `shared/`, then run `python scripts/cine.py build`; never edit the copies inside skills.
- Run commands yourself; never hand them to Mark. Python 3.9+, standard library only; test on 3.9 too (`py -V:Astral/CPython3.9.25`).
- Heredocs in the Bash tool mangle `\\` and some apostrophes: write patch scripts with the Write tool and run them. When generating companions from a template, never split on a marker such as `### C-` that also appears in the header's "Entry shape" line.
- At a yellow budget reading, tell Mark in one line and keep going; a red reading fails the build.
- Record as you go: `ai-docs/log.md`, LEARNINGS in the skill that taught the lesson, and decisions in `ai-docs/decisions/`.

## Stop and ask Mark when

S5's exit check passes: the S2 render is cut, graded and mixed to a stated target and `qc loud` is within tolerance; tests (3.x and 3.9), `kb lint` and `budget` pass (green, or yellow only on rows Mark has been told about); `claude plugin validate` passes on the root and on each plugin; `evergreen.py lint` passes on each skill; all of it is quoted in the log. Then open a PR, assign `m4bwav`, add the `needs-review` label, give him the PR link and a short summary of what works, and stop. The PR holds code, so it waits for his review; do not merge it. Also stop before any hosted render (show the prompt, the settings and the expected cost from `compile`, then wait), before publishing anything (the repo stays private), and before changing another repo.

## Chain rule

When this session's step is done, rewrite `ai-docs/next-session-prompt.md` as the prompt for the next fresh session: what to read first (only what that step needs), the step and its limits, the rules, when to stop and ask, and this paragraph unchanged at the end. Commit it with the handoff and paste it in your final message.
