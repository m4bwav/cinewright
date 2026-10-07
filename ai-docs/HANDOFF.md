# Handoff

## Current state
- PR #11 merged 2026-10-07; main b588d23 carries the dialogue fix. Repo still private: https://github.com/m4bwav/cinewright.
- S7b started on local branch `s7b/routes` (not pushed). Working tree scrub 0, kb lint 0, budget GREEN, 13 ZIPs rebuilt in `dist/`.
- Old commits hold drive paths and private project names (see the log, 2026-10-07 "S7b: history scrub"). Mark chose a history rewrite and force-push. The rewrite is proven (HEAD tree unchanged, rescan 0) but the force-push was refused by the auto-mode classifier, so nothing is pushed.

## Waiting on Mark
- Allow the force-push (or run it): re-run `git filter-repo --replace-text <sidecar history-rewrite-replacements.txt>` on a fresh `git clone --single-branch -b main` of the repo, check `HEAD^{tree}` equals main's, rescan with the sidecar `history-scrub-scan.py` (0 lines), `git push --force origin main`, then delete the merged remote branches s2/genvideo-qc, s3/preproduction, s4/camera-history, s5/post, s7/package, s7b/release, sound/beat-grid-conform, test/library-film. Old commits stay reachable under refs/pull/1-11 (GitHub Support can purge).
- After that: reset the local clone to the new main and redo s7b/routes on it (cherry-pick its doc commit).
- The browser call for the claude.ai routes was refused too; the claude.ai Upload, Add marketplace and VS Code routes need his explicit permission in the session.
- Standing yes (2026-10-06, film watched): those routes, D5 public, 0.1.0 release after this branch merges. Registrations and submissions each need their own go.
- Audiobook pronunciation of the hero's name and the 4 s H3 test: still open.

## Open from the film test
- Sequence header puts every cast member in every shot; no per-scene constants; the 300-word guide for multi-shot H3.

## Next single action
- Once the rewrite is pushed, run [next-session-prompt.md](next-session-prompt.md) from its "The step" section (routes, public, release).
