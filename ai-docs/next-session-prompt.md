# cinewright: session S7 (curate, packaging, install proof)

You are running stage S7 of cinewright, a plugin set for AI video that is private now and public at release, maintained as evergreen units. It gives an agent the craft of every film role plus AI video generation. S1 to S6 built thirteen skills, the `cine.py` runtime, the worked example and the eval harness, and passed the S6 exit check (Sonnet 88 of 88 cases, Opus 87 of 88, Haiku failures recorded). This session builds `cinewright-curate` (the dev plugin's knowledge-base upkeep skill), packages the plugins and proves every install route on the private repo. It does not make the repo public or submit anything without Mark's go.

## Read first (only these, in order)

1. `gh pr list -R m4bwav/cinewright --state all`. If the S6 PR (`s6/evals` to `main`) is still open, or Mark commented on it, do what he asked first and stop there if he has not reviewed it. Once it is merged, branch `s7/package` off `origin/main`.
2. `ai-docs/HANDOFF.md`, then the newest section of `ai-docs/log.md` (2026-10-05, "S6 finished").
3. `ai-docs/plans/PLAN.md`: section 2 (the curate row), section 6 (budgets), section 9 (install proof), the S7 paragraph and decisions D3 and D5.
4. If Mark has answered the runtime budget row question (`ai-docs/decisions/2026-10-04-proposed-runtime-budget-row.md`), apply his answer; until then genvideo's folder stays yellow and is reported, not cut.
5. The evergreen protocol's TESTING.md (find the plugin with `evergreen.py where`) for curate's suite, and `evals/run_evals.py --help` for the harness (rev 2; read `ai-docs/solutions/2026-10-05-headless-evals-on-windows-dead-ends.md` before changing it).

## The step

1. `cinewright-curate` in `plugins/cinewright-dev/`: add, verify and retire knowledge-base entries, refresh model cards, through `cine.py kb` commands. Scaffold it as an evergreen unit (`evergreen.py init --pointer`), write its suite (two triggers, two decoys including a neighbour, one action, one outcome), run it on three models with a baseline, record it. Its description costs about 200 characters of the 4,000 budget: the budget reads yellow; tell Mark in one line, and trim another description only if he asks.
2. Packaging and install proof per PLAN section 9 and the S7 paragraph: per-skill ZIPs, README (40+ words: what it runs and fetches), every install route on Windows on the private repo, one route on a second OS or `untested elsewhere` in TESTS.
3. Public scrub (`cine.py scrub`) over every file including `ai-docs/`; move private lines to the vault sidecar (`everlast.py note --private`). Report the result; do not make the repo public.
4. Record as you go, then the exit check: every route installs and triggers once; tests (3.x and 3.9), kb lint, budget, `claude plugin validate` on the root and each plugin, `evergreen.py lint` on each skill; all quoted in `ai-docs/log.md`.

## Rules

- No AI attribution anywhere: commits, PRs, files.
- Public-repo hygiene: no LAN IPs, hostnames, GPU model, local paths under D:/, or names of Mark's private projects in any shipped file, eval prompt or harness. `cine.py kb lint` catches paths, LAN addresses and GPU names; names are on you. Raw traces and results stay outside the repository (the vault sidecar note "S6 eval results location and spend" says where); private notes go in the vault sidecar.
- A test passes on evidence, never on the reply's claim. Write knowledge edits as rules, numbers and vocabulary; one default, not a menu; do not cite a page you have not checked this session.
- Relative markdown links, never wikilinks. Cite lessons with their code names. Inside a unit's companions, a lesson ID from another unit carries the full unit name (cinewright-qc L-001); cite another unit's research by file name.
- Edit `shared/`, then `python scripts/cine.py build`; never edit the copies inside skills.
- Run commands yourself; never hand them to Mark. Python 3.9+, standard library only; test on 3.9 too (`py -V:Astral/CPython3.9.25`).
- Heredocs in the Bash tool mangle `\\`, `\n` inside strings and some apostrophes: write patch scripts with the Write tool, by absolute path in the scratchpad, and run them. Print reports with `sys.stdout.reconfigure(encoding="utf-8")`. Edit repo files in binary mode to keep line endings.
- Commit the source before every suite run; a skill edited mid-run leaks into runs that copy the plugin after the edit.
- Budget: Mark is near his weekly limit until Wednesday 2026-10-08. Until then take the cheaper option at every choice (fewest runs that still prove the point) and say what was deferred.
- Record as you go: `ai-docs/log.md`, LEARNINGS in the skill that taught the lesson, decisions in `ai-docs/decisions/`.

## Stop and ask Mark when

- Before any run batch over about 150 headless runs, or any batch at all before 2026-10-08 beyond curate's own suite: state the count and expected agent time in one line and wait for his go.
- Before merging or cutting any skill (nine are TRIM, a recommendation only), before making the repo public (D5), before tagging a release, before any directory or awesome-copilot submission, before any hosted render, and before changing another repo (the evergreen registry and the mark-local marketplace are other repos).
- When S7's work up to the public step passes its checks: open a PR from `s7/package` to `main`, assign m4bwav, add the needs-review label, give him the link and a short summary, and stop. The PR holds code, so it waits for his review; do not merge it.

## Chain rule

When this session's step is done, rewrite `ai-docs/next-session-prompt.md` as the prompt for the next fresh session: what to read first (only what that step needs), the step and its limits, the rules, when to stop and ask, and this paragraph unchanged at the end. Commit it with the handoff and paste it in your final message.
