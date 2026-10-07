# cinewright: session S7d (skills find their own folder on claude.ai, public CI, 0.1.1)

You are finishing stage S7 of cinewright, a public plugin set for AI video (https://github.com/m4bwav/cinewright) maintained as evergreen units. S7c (2026-10-07) released v0.1.0 and ran the account routes. Every route installs and triggers, but on the claude.ai plugin route (Customize > Plugins > Add marketplace) the model guessed the skill folder as `/mnt/skills/plugins/cinewright:cinewright-continuity`, every `cine.py` call failed, and it answered from general knowledge. The uploaded-ZIP route did not hit this. This session fixes that, turns on CI now that the repo is public, and prepares 0.1.1.

## Read first (only these, in order)

1. `gh pr list -R m4bwav/cinewright --state all`. If a PR from S7c is open or Mark commented on one, do what he asked first.
2. `ai-docs/HANDOFF.md`, then the 2026-10-07 "S7c" entry at the end of `ai-docs/log.md`.
3. The "Account routes" section of `ai-docs/notes/2026-10-06-s7-install-proof.md`, and L-006 in `plugins/cinewright/skills/cinewright-continuity/LEARNINGS.md`.

## The step

- Folder fix: every public SKILL.md has the same line, "`CINE` means `python scripts/cine.py` run from the folder holding this file". Change it so a model that does not know the path finds it first, for example by searching for this skill's `scripts/cine.py` beside its SKILL.md, and never builds a path from the skill name. Keep it one or two lines. Edit the shared source if the line is generated (`cine.py build`), else each SKILL.md. Run the eval suite for at least cinewright-continuity on Sonnet to show nothing regressed (evergreen-test), and update CHANGELOG and L-006 in the skill.
- CI: `.github/workflows/ci.yml` is `workflow_dispatch` on a self-hosted runner, from the private period. Add push and pull_request triggers and a GitHub-hosted ubuntu, windows and macos matrix with Python 3.9 and 3.x (PLAN D6 and the file's own comment). Check one run passes.
- Versions 0.1.0 to 0.1.1 in marketplace.json and each plugin's manifests; one PR with all of it for Mark's review.
- After Mark merges: rerun scrub and kb lint, rebuild the 13 ZIPs, tag v0.1.1 on main's head, `gh release create v0.1.1 dist/*.zip` with short notes (standing yes for releases once the PR is merged). Then, only with Mark's yes in the session, retest the claude.ai plugin route: Add marketplace, install Cinewright, the trigger prompt from the install-proof note, evidence that `cine.py` ran (the activity row shows the command and no "Failed"), remove the plugin.

## Rules

- No AI attribution anywhere: commits, PRs, release notes, files.
- Public repo: no LAN IPs, hostnames, GPU model, local drive paths or names of Mark's private projects in any file, commit message, PR text or release note. `cine.py scrub --names <vault sidecar scrub-names.txt>` checks files only; check commit messages, PR text and release text by eye. Do not let the everlast docs-sync PR mode open a PR on this repo until everlast is fixed.
- A test passes on evidence, never on the reply's claim. Remove every test install, including `~/.claude/plugins/cache/cinewright/` and `~/.copilot/installed-plugins/cinewright/`.
- Deleting an uploaded skill on claude.ai is a permanent delete: leave it to Mark. Do not grant the Claude GitHub App access.
- Relative markdown links, never wikilinks. Cite lessons with their code names.
- Run commands yourself; never hand them to Mark. Python 3.9+, standard library only.
- Write patch scripts with the Write tool in the scratchpad and run them; edit repo files in binary mode to keep line endings. Read every lint result before committing.
- Record as you go: `ai-docs/log.md`, LEARNINGS in the skill that taught the lesson, decisions in `ai-docs/decisions/`.

## Stop and ask Mark when

- Before any action on his claude.ai account or VS Code settings, before tagging if the PR is not merged, before changing another repo, before any directory or awesome-copilot submission, before any hosted render, and before merging or cutting any skill.
- When the step's work passes its checks: the PR link, the release link and the route result go in the log and HANDOFF; a docs-only PR merges itself once checks pass, anything else waits for his review.

## Chain rule

When this session's step is done, rewrite `ai-docs/next-session-prompt.md` as the prompt for the next fresh session: what to read first (only what that step needs), the step and its limits, the rules, when to stop and ask, and this paragraph unchanged at the end. Commit it with the handoff and paste it in your final message.
