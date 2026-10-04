# cinewright: session S3 (pre-production craft)

You are building stage S3 of cinewright, a plugin set for AI video that is private now and public at release, maintained as evergreen units. It gives an agent the craft of every film role plus AI video generation, so generated video holds together within and between shots. S1 built the scaffold, the router, continuity and the `cine.py` CLI. S2 added nine model cards with a compiler for each, the failure codes, the `cinewright-qc` skill (qc and takes commands) and the first real local render. This session writes the pre-production craft skills: `cinewright-script`, `cinewright-shots`, `cinewright-design` and `cinewright-movement`. It does not touch camera, lighting or history (S4), or post (S5).

## Read first (only these, in order)

1. `ai-docs/HANDOFF.md`, then Mark's review of the S2 PR (`gh pr list -R m4bwav/cinewright --state all`, then `gh pr view <n> -R m4bwav/cinewright --comments`). If the S2 PR is still open, branch `s3/preproduction` off `s2/genvideo-qc` and say so. If he asked for changes, make those first. He was asked about a model-card budget row (`ai-docs/decisions/2026-10-03-proposed-model-card-budget-row.md`): apply his answer.
2. `ai-docs/decisions/` (S1 and S2 decisions: shared copies, field-lesson citations, failure codes in shared vocab, render media location).
3. `ai-docs/plans/PLAN.md` §2 (skill set and slices: `shots` is core, the other three are `cinewright-craft`), §4, §6 budgets, §7 tiers, §10 S3. This is the spec.
4. `CODEMAP.md`. Run `python scripts/cine.py --help`; read only the functions you change.
5. Brief §3 rows for story, direction and blocking, shot design, production design, costume, and movement; §4 sources (`ai-docs/research/2026-10-03-research-brief.md`). Cite books, never copy them.
6. The cinewright-qc LEARNINGS entry from the first render, and field lessons 017, 019, 020 and 021 (titles in `plugins/cinewright/skills/cinewright-continuity/LEARNINGS.md` and the vault sidecar's mapping note).

## The step

1. Four skills, each a full evergreen unit: SKILL.md of 80 lines or fewer, RESEARCH, CHANGELOG, LEARNINGS, TESTS, evergreen.json with the tier from PLAN §7 (slow), and evals with 2 triggers, 2 decoys, 1 action, 1 outcome and a baseline. `shots` goes in `plugins/cinewright`; `script`, `design` and `movement` go in `plugins/cinewright-craft`, whose manifests and README must list them.
2. References are knowledge entries: rules, numbers and vocabulary the model lacks. Script: logline, beats, scene turns, slugline format, dialogue for generated voices. Shots: coverage, blocking, shot list order, the 30-degree and size-step rule shared with continuity. Design: turnaround sheets (field lesson 017), clean references with no emblems (019), color script, costume arc. Movement: weight, contact and follow-through, one phrase per shot, and hard subjects shown side-on, few and large (020, 021). Shared vocabulary goes in `shared/vocab/` and `build` copies it in; never paste the same paragraph into two skills (budget counts duplicates).
3. Any new card or bible field goes in the schemas, the compiler and the continuity diff together, with a test. Keep the identity-verbatim guard and the staging part in sequences (genvideo L-003, L-004).
4. Plan the example idea from start to finish, using each new skill once: brief, beats, shot list, bibles, design notes, continuity diff clean, then a compile for one model. Write it as `examples/three-shot` changes or a second example folder, whichever is smaller.
5. Budgets: each SKILL.md and entry green. All 13 descriptions must stay under 4,000 characters in total and the core five under 1,800. Measure after each skill.

## Rules

- No AI attribution anywhere: commits, PRs, files.
- Public-repo hygiene: no LAN IPs, hostnames, GPU model, local paths under `D:/`, or names of Mark's private projects in any shipped file. `cine.py kb lint` catches paths, LAN addresses and GPU names; names are on you. Private notes go in the vault sidecar (`everlast.py note --private`).
- Write knowledge as rules, numbers and vocabulary. One default, not a menu. Cite primary sources, mark what is unverified, and date what changes.
- Take ideas from other skill repos, never text. Nothing adapted from smixs/visual-skills without attribution.
- Use relative markdown links, never wikilinks. Cite lessons with their code names; cite private field lessons as "field lesson NNN" with a title.
- Edit `shared/`, then run `python scripts/cine.py build`; never edit the copies inside skills.
- Run commands yourself; never hand them to Mark. Python 3.9+, standard library only; test on 3.9 too (`py -V:Astral/CPython3.9.25`).
- Heredocs in the Bash tool mangle `\\` and some apostrophes: write patch scripts with the Write tool and run them.
- At a yellow budget reading, tell Mark in one line and keep going; a red reading fails the build.
- Record as you go: `ai-docs/log.md`, LEARNINGS in the skill that taught the lesson, and decisions in `ai-docs/decisions/`.

## Stop and ask Mark when

S3's exit check passes: the example idea is planned from start to finish with every new skill used once; tests, `kb lint` and `budget` are green; `claude plugin validate` passes on the root and on each plugin; `evergreen.py lint` passes on each skill; all of it is quoted in the log. Then open a PR, assign `m4bwav`, add the `needs-review` label, give him the PR link and a short summary of what works, and stop. The PR holds code, so it waits for his review; do not merge it. Also stop before any hosted render (show the prompt, the settings and the expected cost from `compile`, then wait), before publishing anything (the repo stays private), and before changing another repo.

## Chain rule

When this session's step is done, rewrite `ai-docs/next-session-prompt.md` as the prompt for the next fresh session: what to read first (only what that step needs), the step and its limits, the rules, when to stop and ask, and this paragraph unchanged at the end. Commit it with the handoff and paste it in your final message.
