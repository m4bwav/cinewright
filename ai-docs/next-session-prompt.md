# cinewright: session S1 (scaffold and one vertical slice)

You are building stage S1 of cinewright, a public-at-release, evergreen plugin set that gives an agent the craft of every film role plus AI video generation, so generated video is coherent within and between shots. The plan is settled; this session builds the skeleton and proves one path end to end. It does not write the craft knowledge (S3-S5) or more than one model card (S2).

## Read first (only these, in order)

1. `ai-docs/HANDOFF.md` and the decisions Mark answered (look for his replies in the PR #1 conversation, `gh pr view 1 -R m4bwav/cinewright --comments`, or in `ai-docs/decisions/`). If D2 (license) or D3 (slices) is unanswered, build with the recommendation and say so.
2. `ai-docs/plans/PLAN.md` §1-§7 and §10 S1. This is the spec.
3. `ai-docs/research/2026-10-03-packaging-verification.md`: manifest rules (`strict`, the six frontmatter keys, the Agent Plugins `$schema`, directory file limits, no `bin/`, no symlinks).
4. The evergreen unit rules: `D:/m4bwa/Claude/Projects/Ai/evergreen-protocol/protocol/PROTOCOL.md` §2 and §9, `TESTING.md`, and `templates/SKILL.md.template`, `evals.json.template`, `SETUP.md.template` in that repo. Use `evergreen.py` to scaffold `evergreen.json` rather than hand-writing it.
5. Skim `D:/m4bwa/Claude/Projects/Ai/threewright/skills/threewright/SKILL.md` and `kb/SCHEMA.md` for shape only.
6. Brief §6 Veo entry and the Veo prompt guide (https://cloud.google.com/blog/products/ai-machine-learning/ultimate-prompting-guide-for-veo-3-1 and https://docs.cloud.google.com/vertex-ai/generative-ai/docs/video/video-gen-prompt-guide): re-check Veo 3.1 durations, sizes, reference images and timestamp syntax before writing its card.

Delegate wide reading to subagents and keep their summaries.

## The step

Work on a branch off `main` (`s1/scaffold`).

1. Layout from PLAN §3: root `.claude-plugin/marketplace.json`; `plugins/cinewright/`, `plugins/cinewright-craft/` (empty skills list for now, README says so), `plugins/cinewright-dev/`, each with `.claude-plugin/plugin.json` and an Agent Plugins `plugin.json`; `shared/vocab/`, `shared/schemas/`, `shared/lib/`; `scripts/cine.py`; `tests/`; LICENSE (MIT unless Mark chose otherwise); README stub of 40+ words.
2. Schemas in `shared/schemas/`: reference entry, shot card, bibles (style, character, location, scene axis), model card, take record. Keep the shot card generator-neutral and built from film practice (shot list and script-supervisor columns), not from any competitor's card.
3. `cine.py` groups `kb` (index, search, show, lint), `cards` (new, validate, export --film-json), `compile` (Veo only), `continuity diff`, `budget` (PLAN §6 thresholds, duplicate detection), `zip`, `build` (copies `shared/vocab` entries per `needs.json` with sha256 headers; lint fails on drift). Python 3.9+ stdlib, cross-platform. A test per command; `python -m unittest` runs them.
4. Skills, each a full evergreen unit (SKILL.md ≤ 80 lines, RESEARCH, CHANGELOG, LEARNINGS, TESTS, evergreen.json, evals/evals.json with 2 triggers, 2 decoys, 1 action, 1 outcome, baseline): `cinewright` (router and pipeline), `cinewright-continuity` (bibles, axis and screen direction, 30-degree rule, eyelines, per-shot checklist; generalise comfyui-gen lessons L-005, L-011, L-012 and L-013 by title, without private context). `cinewright-genvideo` as a stub with only the Veo 3.1 card and the compile rule. Descriptions: trigger words first, within PLAN §6 character budgets, six frontmatter keys only.
5. One worked example under `examples/three-shot/`: a one-line idea → shot cards → bibles → `continuity diff` (clean, then one planted error caught) → compiled Veo prompts. Not rendered.
6. CI: `.github/workflows/ci.yml` running tests, `cine.py kb lint`, `cine.py budget`, `claude plugin validate` if available. Per D6, set `runs-on` for a self-hosted runner while private, or leave it manual-dispatch and run the same checks locally if no runner exists; say which.
7. Exit check (PLAN §10 S1): the example passes, budget green, `claude plugin validate .` passes for the marketplace and each plugin, tests pass, `cine.py zip` builds a claude.ai ZIP for `cinewright-continuity` with the skill folder at the top. Run every check yourself and quote the output in the log.

## Rules

- No AI attribution anywhere: commits, PRs, files.
- Public-repo hygiene: no LAN IPs, hostnames, GPU model, local paths under `D:/`, or names of Mark's private projects in any file that will ship. Private notes go in the vault sidecar (`everlast.py note --private`).
- Write knowledge as rules, numbers and vocabulary the model lacks. One default, not a menu. Cite primary sources; mark what is unverified; date what changes.
- Ideas from other skill repos only, never text. Nothing adapted from smixs/visual-skills without attribution.
- Relative markdown links, never wikilinks. Cite lessons with their code names; comfyui-gen's lessons have none, so cite them by ID and title.
- Run commands yourself; do not hand them to Mark.
- At a yellow budget reading, tell Mark in one line and keep going; red fails the build.
- Record as you go: `ai-docs/log.md`, LEARNINGS in the skill that taught it, decisions in `ai-docs/decisions/`.

## Stop and ask Mark when

S1's exit check passes: open a PR, assign `m4bwav`, add the `needs-review` label, give him the PR link and a short summary of what works, and stop. The PR holds code, so it waits for his review; do not merge it. Also stop if a choice would cost money (a hosted render, a paid API), publish anything (the repo stays private), or change another repo.

## Chain rule

When this session's step is done, rewrite `ai-docs/next-session-prompt.md` as the prompt for the next fresh session: what to read first (only what that step needs), the step and its limits, the rules, when to stop and ask, and this paragraph unchanged at the end. Commit it with the handoff and paste it in your final message.
