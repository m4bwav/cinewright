# Handoff

## Current state
- S7 up to the public step is done on branch `s7/package` (rebased on main after PR #8), with a PR to `main` waiting for Mark's review (assigned, label needs-review). The repo is still private: https://github.com/m4bwav/cinewright.
- New: cinewright-curate (dev plugin) and `cine.py kb due|new|verify|retire` plus `cine.py scrub` in the maintainer CLI ([decisions/2026-10-06-curate-commands-in-the-maintainer-cli-and-scrub-names-outside-the-repo.md](decisions/2026-10-06-curate-commands-in-the-maintainer-cli-and-scrub-names-outside-the-repo.md)). Harness `fixture: "repo"` for maintainer skills.
- Curate suite T-20261006-2: Sonnet 6/6, Opus 6/6 (1 run each), Haiku 3/6 (recorded). L-001 `optional-flag-copied` confirmed by the rerun.
- Install proof ([notes/2026-10-06-s7-install-proof.md](notes/2026-10-06-s7-install-proof.md)): Claude Code, Copilot CLI and `gh skill` installed and triggered on the private repo; 13 ZIPs in `dist/` (gitignored).
- Scrub: 0 hits with the vault sidecar's `scrub-names.txt`; private research-brief sections moved to the sidecar.
- Checks quoted in [log.md](log.md) (2026-10-06): tests 3.14 and 3.9, kb lint, validate x4, evergreen lint x14 pass; budget YELLOW on two rows.

## Waiting on Mark
- Review of the S7 PR.
- Go for the three routes that touch his account or settings: claude.ai skill Upload (one ZIP, removed after), claude.ai Add marketplace, VS Code Copilot marketplace setting.
- D5: make the repo public; then public-route retests, tag 0.1.0 with the 13 ZIPs as release assets, register in evergreen and the mark-local marketplace (other repos), directory and awesome-copilot submissions: each needs his go.
- Description budget 4,082 of 4,000 (yellow, from curate's 194 characters): trim only if he asks.
- Runtime budget row question (decisions/2026-10-04-proposed-runtime-budget-row.md): genvideo's folder 167 KB, yellow.

## Deferred (budget week until 2026-10-08)
- Curate on Haiku and Opus at 3 runs per case (ran 1); the S6 full rev-2 rerun (312 runs). Ask before either.

## Next single action
- Run [next-session-prompt.md](next-session-prompt.md) (S7 public step) once Mark has reviewed the S7 PR and answered the waiting items.
