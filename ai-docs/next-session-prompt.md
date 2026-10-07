# cinewright: session S7c (release 0.1.0 and the account routes)

You are finishing stage S7 of cinewright, a public plugin set for AI video (https://github.com/m4bwav/cinewright) maintained as evergreen units. S7b (2026-10-07) rewrote the history to drop private paths and names, made the repo public, retested the Claude Code, Copilot CLI and `gh skill` routes against it and bumped every manifest to 0.1.0 on branch `s7b/routes`. This session cuts the release and runs the three routes that touch Mark's accounts. Do only the parts Mark has said yes to.

## Read first (only these, in order)

1. `gh pr list -R m4bwav/cinewright --state all`. If the s7b/routes PR is still open, or Mark commented on it, do what he asked first and stop there if he has not reviewed it.
2. `ai-docs/HANDOFF.md`, then the two 2026-10-07 "S7b" entries at the end of `ai-docs/log.md`.
3. `ai-docs/notes/2026-10-06-s7-install-proof.md` (both tables, quirks, cleanup).

## The step

- Release (standing yes from 2026-10-06, once the PR is merged): on `main`, check the manifests read 0.1.0, rebuild the 13 ZIPs (`python scripts/cine.py zip <skill>` for every skill but curate), `git tag v0.1.0` on main's head, push the tag, `gh release create v0.1.0 dist/*.zip` with short notes (what the two public plugins do, the install commands, the ZIP route). Check the release page lists 13 assets.
- Account routes (Mark must approve each in the session; the browser call was refused last time): claude.ai Customize > Skills > Upload `dist/cinewright-continuity.zip`; claude.ai Customize > Plugins > Add marketplace `m4bwav/cinewright`; VS Code Copilot (`chat.plugins.marketplaces` or "Chat: Install Plugin From Source"). One install and one trigger each, evidence from the UI (the skill shown as used), removed afterwards. Record each in the install-proof note and PLAN section 9.
- Before the release, rerun `python scripts/cine.py scrub --names <vault sidecar scrub-names.txt>` and `kb lint`; both must be clean.
- Registration in evergreen and the mark-local marketplace, and directory or awesome-copilot submissions, are other repos or outward-facing: each needs its own go.

## Rules

- No AI attribution anywhere: commits, PRs, release notes, files.
- Public repo: no LAN IPs, hostnames, GPU model, local drive paths or names of Mark's private projects in any file, commit message, PR text or release note. `cine.py scrub` checks files only; check commit messages and release text by eye. The everlast docs-sync PR mode puts the hostname in branch names and PR titles: do not let it open a PR on this repo until everlast is fixed.
- A test passes on evidence, never on the reply's claim. Remove every test install, including `~/.claude/plugins/cache/cinewright/`.
- Relative markdown links, never wikilinks. Cite lessons with their code names.
- Run commands yourself; never hand them to Mark. Python 3.9+, standard library only.
- Write patch scripts with the Write tool in the scratchpad and run them; edit repo files in binary mode to keep line endings. Read every lint result before committing.
- Record as you go: `ai-docs/log.md`, LEARNINGS in the skill that taught the lesson, decisions in `ai-docs/decisions/`.

## Stop and ask Mark when

- Before any action on his claude.ai account or VS Code settings, before tagging if the PR is not merged, before changing another repo, before any directory or awesome-copilot submission, before any hosted render, and before merging or cutting any skill.
- When the step's work passes its checks: the release page link and the route results go in the log and HANDOFF; a docs-only PR merges itself once checks pass, anything else waits for his review.

## Chain rule

When this session's step is done, rewrite `ai-docs/next-session-prompt.md` as the prompt for the next fresh session: what to read first (only what that step needs), the step and its limits, the rules, when to stop and ask, and this paragraph unchanged at the end. Commit it with the handoff and paste it in your final message.
