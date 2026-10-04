# cinewright: session S4 (camera, lighting and history)

You are building stage S4 of cinewright, a plugin set for AI video that is private now and public at release, maintained as evergreen units. It gives an agent the craft of every film role plus AI video generation, so generated video holds together within and between shots. S1 built the scaffold, the router, continuity and the `cine.py` CLI. S2 added nine model cards with compilers, the failure codes and `cinewright-qc`. S3 added `cinewright-shots` (core) and `cinewright-script`, `cinewright-design` and `cinewright-movement` (craft), an optional prop bible, `cards list`, and DIALOGUE and HARD-SUBJECT diff warnings. This session writes `cinewright-camera` and `cinewright-history`. It does not touch post (S5: edit, finish, sound).

## Read first (only these, in order)

1. `ai-docs/HANDOFF.md`, then Mark's review of the S3 PR (`gh pr list -R m4bwav/cinewright --state all`, then `gh pr view <n> -R m4bwav/cinewright --comments`). If the S3 PR is still open, branch `s4/camera-history` off `s3/preproduction` and say so; if merged, branch off `main`. If he asked for changes, make those first. He was asked about a runtime budget row (`ai-docs/decisions/2026-10-04-proposed-runtime-budget-row.md`): apply his answer. Until he answers, the genvideo folder stays yellow and is reported, not cut.
2. `ai-docs/decisions/` (shared copies with hash headers, field-lesson citations, failure codes in shared vocab, render media location, model-card budget row, prop bible and pre-production checks).
3. `ai-docs/plans/PLAN.md` §2 (camera and history are `cinewright-craft`), §5, §6 budgets, §7 tiers (camera slow, history glacial), §10 S4. This is the spec.
4. `CODEMAP.md`. Run `python scripts/cine.py --help`; read only the functions you change (`card_parts`, `continuity_diff`, the style-bible schema).
5. Brief §3 rows for cinematography and lighting, §4 sources, §5 history and style cards (`ai-docs/research/2026-10-03-research-brief.md`). Cite books, never copy them.
6. One S3 skill as the template for a full unit: `plugins/cinewright-craft/skills/cinewright-design/` (SKILL.md, companions, evals). The design entry `color-script` already points to cinewright-camera for color temperature; keep that link true.

## The step

1. Two skills in `plugins/cinewright-craft`, each a full evergreen unit: SKILL.md of 80 lines or fewer, RESEARCH, CHANGELOG, LEARNINGS, TESTS, MAINTENANCE, evergreen.json (camera `slow`, history `glacial`), needs.json, and evals with 2 triggers, 2 decoys, 1 action, 1 outcome and a baseline run without the skill. In S3 two of four bare-folder baselines found this repository on disk and used its `cine.py` (cinewright-script L-001), so run baselines where the repository cannot be reached (a cloud session, or a sandbox limited to the working folder) with skill names stripped from copied fixtures, and mark any run that touched the repository as contaminated. On Windows call `claude` by its full path from `shutil.which`. List both in the craft manifests (both `plugin.json` files), the marketplace description and the README.
2. Camera references are knowledge entries: lens choice (14-24, 35, 50, 85-135), depth of field, exposure, frame rate and 180-degree shutter, aspect ratios, anamorphic, lighting ratios and setups, color temperature. Shared vocabulary (aspect ratios, lens words, lighting terms) goes in `shared/vocab/` when two skills need it, and `build` copies it in.
3. History cards follow brief §5: about 60 tokens each, tags not prose, one reference film with a timestamp. Group them into a few entries (movements, eras, genres, directors and DPs) so each entry stays green; never one file per card.
4. Exit check from PLAN §10: "shoot it like 1970s New Hollywood, 2.39" changes the compiled prompts in checkable ways. That needs a style-bible field (for example a list of history card ids, or lens and lighting fields): put it in the schema, the compiler and the continuity diff together, with a test. Keep the identity and prop verbatim guards and the staging part in sequences (genvideo L-003, L-004).
5. Show it on `examples/three-shot`: one style change, a recompile for one model, and the compiled-files test kept current.
6. Budgets: each SKILL.md and entry green. The 8 descriptions now total 2,403 characters; all skills must stay under 4,000 in total (curate counts too when it exists), so keep each new description near 300. Measure after each skill.

## Rules

- No AI attribution anywhere: commits, PRs, files.
- Public-repo hygiene: no LAN IPs, hostnames, GPU model, local paths under `D:/`, or names of Mark's private projects in any shipped file. `cine.py kb lint` catches paths, LAN addresses and GPU names; names are on you. Private notes go in the vault sidecar (`everlast.py note --private`).
- Write knowledge as rules, numbers and vocabulary. One default, not a menu. Cite primary sources, mark what is unverified, and date what changes. Do not cite a paper or URL you have not checked this session.
- Take ideas from other skill repos, never text. Nothing adapted from smixs/visual-skills without attribution.
- Use relative markdown links, never wikilinks. Cite lessons with their code names; cite private field lessons as "field lesson NNN" with a title. Inside a unit's companions, a lesson ID from another unit must carry the full unit name (`cinewright-qc L-001`) or evergreen lint fails.
- Edit `shared/`, then run `python scripts/cine.py build`; never edit the copies inside skills.
- Run commands yourself; never hand them to Mark. Python 3.9+, standard library only; test on 3.9 too (`py -V:Astral/CPython3.9.25`).
- Heredocs in the Bash tool mangle `\\` and some apostrophes: write patch scripts with the Write tool and run them.
- At a yellow budget reading, tell Mark in one line and keep going; a red reading fails the build.
- Record as you go: `ai-docs/log.md`, LEARNINGS in the skill that taught the lesson, and decisions in `ai-docs/decisions/`.

## Stop and ask Mark when

S4's exit check passes: the style request changes compiled prompts in checkable ways and a test proves it; tests (3.x and 3.9), `kb lint` and `budget` pass (green, or yellow only on rows Mark has been told about); `claude plugin validate` passes on the root and on each plugin; `evergreen.py lint` passes on each skill; all of it is quoted in the log. Then open a PR, assign `m4bwav`, add the `needs-review` label, give him the PR link and a short summary of what works, and stop. The PR holds code, so it waits for his review; do not merge it. Also stop before any hosted render (show the prompt, the settings and the expected cost from `compile`, then wait), before publishing anything (the repo stays private), and before changing another repo.

## Chain rule

When this session's step is done, rewrite `ai-docs/next-session-prompt.md` as the prompt for the next fresh session: what to read first (only what that step needs), the step and its limits, the rules, when to stop and ask, and this paragraph unchanged at the end. Commit it with the handoff and paste it in your final message.
