# cinewright: session S7b (public step: remaining routes, go public, release)

You are running the second half of stage S7 of cinewright, a plugin set for AI video that is private now and public at release, maintained as evergreen units. S1 to S6 built thirteen skills, the `cine.py` runtime, the worked example and the eval harness. S7's first half (2026-10-06) added `cinewright-curate` (dev plugin), `cine.py kb due|new|verify|retire` and `cine.py scrub`, proved three install routes on the private repo, built the per-skill ZIPs and scrubbed the repo to 0 hits. This session finishes what needs Mark's go: the remaining install routes, making the repo public, public-route retests and the 0.1.0 release. Do only the parts Mark has said yes to.

## Read first (only these, in order)

1. `gh pr list -R m4bwav/cinewright --state all`. If PR #11 (`s7b/release`, the dialogue fix from Mark's review of the library film) is still open, or Mark commented on it, do what he asked first and stop there if he has not reviewed it. Once it is merged, branch `s7b/routes` off `origin/main` (0.1.0 must carry that fix).
2. `ai-docs/HANDOFF.md` ("Waiting on Mark" lists his open answers), then the newest sections of `ai-docs/log.md` (2026-10-07: the film test and the dialogue fix; 2026-10-06: session S7).
3. `ai-docs/notes/2026-10-06-s7-install-proof.md` (routes, exact commands, quirks, cleanup).
4. `ai-docs/plans/PLAN.md` section 9 (install routes), the S7 paragraph in section 10 and decision D5.
5. If Mark has said how his audiobook pronounces the hero's name, or approved a short H3 test of the voiceover phrase and a respelling, do that first and record the result in the film-test note and genvideo L-012 / script L-003.

## The step

1. Routes he said yes to, one install and one trigger each, removed afterwards: claude.ai skill Upload (`dist/` ZIP; rebuild with `python scripts/cine.py zip <skill>`), claude.ai Customize > Plugins > Add marketplace, VS Code Copilot (`chat.plugins.marketplaces` or "Chat: Install Plugin From Source"). Record each in the install-proof note and PLAN section 9.
2. Before going public, rerun `python scripts/cine.py scrub --names <vault sidecar scrub-names.txt>` (the vault sidecar note "S6 eval results location and spend" and the file sit in the same sidecar) and `kb lint`; both must be clean. Then, only on Mark's go (D5): make the repo public, and rerun the Claude Code and `gh skill` routes against the public repo with nothing cached.
3. Release, only on Mark's go: bump versions (marketplace.json, each plugin's two manifests) to 0.1.0, tag, `gh release create` with the 13 ZIPs. Registration in evergreen and the mark-local marketplace, and directory or awesome-copilot submissions, are other repos or outward-facing: each needs its own go.
4. Exit check: every route installs and triggers once; tests (3.x and 3.9), kb lint, scrub, budget, `claude plugin validate` on the root and each plugin, `evergreen.py lint` on each skill; all quoted in `ai-docs/log.md`.

## Rules

- No AI attribution anywhere: commits, PRs, files.
- Public-repo hygiene: no LAN IPs, hostnames, GPU model, local paths under D:/, or names of Mark's private projects in any shipped file, eval prompt or harness. `cine.py scrub` with the sidecar names file catches these; `kb lint` catches paths, LAN addresses and GPU names. Raw traces and results stay outside the repository; private notes go in the vault sidecar (`everlast.py note --private`).
- A test passes on evidence, never on the reply's claim. Remove every test install afterwards, including `~/.claude/plugins/cache/cinewright/`, which `claude plugin uninstall` leaves behind.
- Relative markdown links, never wikilinks. Cite lessons with their code names (curate L-001 `optional-flag-copied`).
- Edit `shared/`, then `python scripts/cine.py build`; never edit the copies inside skills.
- Run commands yourself; never hand them to Mark. Python 3.9+, standard library only; test on 3.9 too (`py -V:Astral/CPython3.9.25`).
- Heredocs in the Bash tool mangle `\\`, `\n` inside strings and some apostrophes: write patch scripts with the Write tool, by absolute path in the scratchpad, and run them. Edit repo files in binary mode to keep line endings. Read every lint result before committing.
- Commit the source before every suite run; the `fixture: "repo"` cases copy `scripts/`, `shared/` and `plugins/` at each run start, so edit none of them while a batch runs.
- Budget: if before 2026-10-08, take the cheaper option at every choice and say what was deferred.
- Record as you go: `ai-docs/log.md`, LEARNINGS in the skill that taught the lesson, decisions in `ai-docs/decisions/`.

## Stop and ask Mark when

- Before any run batch over about 150 headless runs, or any batch at all before 2026-10-08: state the count and expected agent time in one line and wait for his go.
- Before any action on his claude.ai account or VS Code settings, before making the repo public (D5), before tagging a release, before changing another repo (the evergreen registry and the mark-local marketplace), before any directory or awesome-copilot submission, before any hosted render, and before merging or cutting any skill.
- When the step's work passes its checks: open a PR from `s7b/routes` to `main`, assign m4bwav, add the needs-review label, give him the link and a short summary, and stop. A PR holding code waits for his review; do not merge it.

## Chain rule

When this session's step is done, rewrite `ai-docs/next-session-prompt.md` as the prompt for the next fresh session: what to read first (only what that step needs), the step and its limits, the rules, when to stop and ask, and this paragraph unchanged at the end. Commit it with the handoff and paste it in your final message.
