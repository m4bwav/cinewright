# Handoff

## Current state
- Repo PUBLIC since 2026-10-07: https://github.com/m4bwav/cinewright. History rewritten first (old paths and private names out of every commit; main's tree unchanged). Backup bundle of the old history beside the repo folder; rewrite inputs in the vault sidecar.
- Public routes retested and removed: Claude Code, Copilot CLI, `gh skill` (all PASS on Sonnet). Record: [notes/2026-10-06-s7-install-proof.md](notes/2026-10-06-s7-install-proof.md).
- Branch `s7b/routes`: versions 0.1.0, docs. Exit check all green (log, 2026-10-07 "history rewritten, repo public"). PR waits for Mark.

## Waiting on Mark
- Review and merge the s7b/routes PR. Then: tag v0.1.0 on main and `gh release create` with the 13 ZIPs (standing yes).
- claude.ai skill Upload, claude.ai Add marketplace, VS Code Copilot route: the agent's browser was refused; approve them in a session, or do them by hand.
- Old commits stay reachable from PR #1-#11 pages (refs/pull); only GitHub Support can purge. Closed PRs #12-#13 show a hostname in their head branch name.
- everlast docs-sync PR mode puts the hostname in branch, title and body: fix in everlast before the next sync to this public repo.
- Registrations (evergreen, mark-local) and directory or awesome-copilot submissions: each needs its own go.
- Audiobook pronunciation of the hero's name and the 4 s H3 test: still open.

## Open from the film test
- Sequence header puts every cast member in every shot; no per-scene constants; the 300-word guide for multi-shot H3.

## Next single action
- Once the s7b/routes PR merges, run [next-session-prompt.md](next-session-prompt.md) (S7c: release 0.1.0, the three account routes).
