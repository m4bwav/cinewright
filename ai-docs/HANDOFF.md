# Handoff

## Current state
- Released: v0.1.0 on main fad9ec6, https://github.com/m4bwav/cinewright/releases/tag/v0.1.0 (13 skill ZIPs). Repo public since 2026-10-07.
- Install routes (record: [notes/2026-10-06-s7-install-proof.md](notes/2026-10-06-s7-install-proof.md)): Claude Code, Copilot CLI, `gh skill`, claude.ai skill Upload and VS Code Copilot Chat all PASS. claude.ai Add marketplace: the skill triggers, but its `cine.py` calls fail because the model guesses the plugin skill folder (`/mnt/skills/plugins/cinewright:cinewright-continuity`). LEARNINGS L-006 `claude-ai-plugin-skill-folder-unknown` in cinewright-continuity.
- VS Code route caveat: installed with the Copilot CLI into `~/.copilot/installed-plugins/`, which VS Code reads; VS Code's own Install button was not exercised.

- cinewright-voice (14th skill) built 2026-10-07 on branch voice-skill, PR #18 (https://github.com/m4bwav/cinewright/pull/18) waits for review; Sonnet evals 7/7, Haiku and Opus not run. Description budget YELLOW (4,336/4,000). TTS Audio Suite in ComfyUI not installed on the PC: install only with Mark's go, then run the design-then-clone route once and record it in the skill's SETUP.md.

## Waiting on Mark
- claude.ai cleanup: delete the uploaded test skill cinewright-continuity (permanent delete; switched off for now), remove the cinewright marketplace source if the UI offers it, close the VS Code window `code chat -n` opened.
- Old commits stay reachable from PR #1-#11 pages (refs/pull); only GitHub Support can purge. Closed PRs #12-#13 show a hostname in their head branch name.
- everlast docs-sync PR mode puts the hostname in branch, title and body: fix in everlast before the next sync to this public repo.
- Registrations (evergreen, mark-local) and directory or awesome-copilot submissions: each needs its own go. Hold the Claude directory until the claude.ai plugin route runs its scripts.
- Audiobook pronunciation of the hero's name and the 4 s H3 test: still open.

## Open from the film test
- Sequence header puts every cast member in every shot; no per-scene constants; the 300-word guide for multi-shot H3.

## Next single action
- Run [next-session-prompt.md](next-session-prompt.md) (S7d: make the skills find their own folder on claude.ai, public CI triggers, 0.1.1).
