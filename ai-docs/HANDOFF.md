# Handoff

## Current state
- Released: v0.1.0 on main fad9ec6, https://github.com/m4bwav/cinewright/releases/tag/v0.1.0 (13 skill ZIPs). Repo public since 2026-10-07.
- Install routes (record: [notes/2026-10-06-s7-install-proof.md](notes/2026-10-06-s7-install-proof.md)): Claude Code, Copilot CLI, `gh skill`, claude.ai skill Upload and VS Code Copilot Chat all PASS. claude.ai Add marketplace: the skill triggers, but its `cine.py` calls fail because the model guesses the plugin skill folder (`/mnt/skills/plugins/cinewright:cinewright-continuity`). LEARNINGS L-006 `claude-ai-plugin-skill-folder-unknown` in cinewright-continuity.
- VS Code route caveat: installed with the Copilot CLI into `~/.copilot/installed-plugins/`, which VS Code reads; VS Code's own Install button was not exercised.

- cinewright-voice (14th skill) built 2026-10-07 on branch voice-skill, merged to main as PR #18 (https://github.com/m4bwav/cinewright/pull/18) on 2026-10-07 after merging cinewright-sets into it; Sonnet evals 7/7, Haiku and Opus not run. Description budget YELLOW (4,680/4,000 with cinewright-sets; red at 5,500). TTS Audio Suite in ComfyUI not installed on the PC: install only with Mark's go, then run the design-then-clone route once and record it in the skill's SETUP.md.

- Branch cartwheel-night, PR #21 (https://github.com/m4bwav/cinewright/pull/21), waiting for review: `qc measure`, `compile --sequence --join`, card `music` field, tests copy `assets/` (91 OK). From a 60 s comedy field test; details in the 2026-10-07 log entry. Budget yellow: shared/lib 104 KB.

- Branch preproduction-gaps (2026-10-09, PR waiting for review): prop `states` and card `props`, prop and location refs now sent to the model, `shared/lib/cine_post.py` (animatic, grade measure/match; shipped by edit and finish only), entries prop-sheets, lora-or-references, animatic, shot-matching, blockout-control, identity-score. Budget yellow: runtime shared/lib 120 KB (green 100, red 150), one entry 714/700 tokens. Details: 2026-10-09 log entry.

- Branch critic-research-2026-10-15 (2026-10-15): `qc judge` / `qc agree` / standing claims, six critic entries, `air-steps`; research note [research/2026-10-15-critic-research.md](research/2026-10-15-critic-research.md). Open from it, in order: per-region crops and geometry checks (screen side, people count, gaze, smile) before the judge; pairwise take ranking in a command; voice checks as commands (forced alignment, speaker similarity); score `qc judge --twice` on the reviewer's own verdicts, not the agent's.

- Branch fight-plans (2026-10-15, PR waiting for review): fight plan schema, `cine_fight.py` check and sheet (movement only), entries fight-plan, fight-from-a-book, fight-previs, eval action-2 (3/3 Sonnet), harness allow list for `cine_*.py`. Research [research/2026-10-15-fight-planning.md](research/2026-10-15-fight-planning.md). Budget: runtime 145 KB of red 150, so the next runtime addition needs a trim first. Open from it: the five local tests at the end of the research note (H3 timecoded hits first); `pw.py duel` in polywright only if test 1 shows blades survive depth control.

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
