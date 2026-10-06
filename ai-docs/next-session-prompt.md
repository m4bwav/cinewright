# cinewright: session S6, continued (finish the exit check)

You are finishing stage S6 of cinewright, a plugin set for AI video that is private now and public at release, maintained as evergreen units. It gives an agent the craft of every film role plus AI video generation. S1 to S5 built thirteen skills, the `cine.py` runtime and the worked example. The first S6 session built the eval harness, ran the three-model matrix (Haiku 4.5, Sonnet 5, Opus 5.5) and two tuning rounds. This session finishes S6: the remaining Sonnet and Opus failures, the reruns that are pending, the records, the PR. It does not build cinewright-curate or package anything (S7).

## Read first (only these, in order)

1. `ai-docs/HANDOFF.md`, then the newest S6 entries in `ai-docs/log.md` (the 2026-10-04 and 2026-10-05 sections, the matrix at the end).
2. `ai-docs/decisions/2026-10-05-eval-harness-and-model-matrix.md` and `ai-docs/solutions/2026-10-05-headless-evals-on-windows-dead-ends.md`. Do not change the harness without reading the solutions table: every fault in it first looked like a skill failure.
3. `evals/run_evals.py --help` and its module docstring; `evals/record_tests.py` docstring.
4. `gh pr list -R m4bwav/cinewright --state all`; if Mark commented on anything since 2026-10-05, do what he asked first. Stay on branch `s6/evals` (pushed). If Mark has answered the runtime budget row question (`ai-docs/decisions/2026-10-04-proposed-runtime-budget-row.md`), apply his answer; until then genvideo's folder stays yellow and is reported, not cut.
5. The evergreen protocol's TESTING.md (find the plugin with `evergreen.py where`) and the evergreen-tune skill, for the loop.

The results from the first session are on this PC (the vault sidecar note "S6 eval results location and spend" says where); `run_evals.py run` resumes and skips recorded runs, `--rerun` repeats them.

## The step

1. Rerun what changed without a rerun: continuity outcome-1 (C-20261005-1) and shots outcome-1 (the `cine.py` bible fix), both arms, all three models.
2. Tune the remaining Sonnet and Opus failures (HANDOFF "In progress") with evergreen-tune: reproduce from the kept run folder and trace (`evals/inspect_run.py <key> --reply`), classify, write the learning in that skill's LEARNINGS, the smallest edit, rerun that skill's whole suite on all three models. Three iterations at most per case, counting the two already spent (each TESTS.md says which). Start with the Opus pattern in HANDOFF "Watch": decide harness friction or skill rule, on evidence.
3. Haiku-only failures stay recorded with the reason in decision item 5 unless a change made for Sonnet or Opus moves them.
4. Confirm or retire the round-1 lessons whose Evidence says "rerun pending", against the new T- entries.
5. Record: `python evals/record_tests.py --evergreen <evergreen.py> --out <results>` (one T- entry per skill, the tests block, dated baselines), `export-worth` then `evergreen.py worth <skill> --results <dir> --record`, and the matrix summary in `ai-docs/log.md`.

## Rules

- No AI attribution anywhere: commits, PRs, files.
- Public-repo hygiene: no LAN IPs, hostnames, GPU model, local paths under D:/, or names of Mark's private projects in any shipped file, eval prompt or harness. `cine.py kb lint` catches paths, LAN addresses and GPU names; names are on you. Raw traces and results stay outside the repository; private notes go in the vault sidecar (`everlast.py note --private`).
- A test passes on evidence, never on the reply's claim. Write knowledge edits as rules, numbers and vocabulary; one default, not a menu; do not cite a page you have not checked this session.
- Relative markdown links, never wikilinks. Cite lessons with their code names. Inside a unit's companions, a lesson ID from another unit carries the full unit name (cinewright-qc L-001); cite another unit's research by file name.
- Edit `shared/`, then `python scripts/cine.py build`; never edit the copies inside skills.
- Run commands yourself; never hand them to Mark. Python 3.9+, standard library only; test on 3.9 too (`py -V:Astral/CPython3.9.25`).
- Heredocs in the Bash tool mangle `\\`, `\n` inside strings and some apostrophes: write patch scripts with the Write tool and run them. Print reports with `sys.stdout.reconfigure(encoding="utf-8")`.
- Commit the source before every suite run; a skill edited mid-run leaks into runs that copy the plugin after the edit.
- Watch the description budget (3,888 of 4,000; curate still needs about 200). At a yellow budget reading, tell Mark in one line and keep going; a red reading fails the build.
- Record as you go: `ai-docs/log.md`, LEARNINGS in the skill that taught the lesson, decisions in `ai-docs/decisions/`.

## Stop and ask Mark when

- Before any run batch over about 150 headless runs: state the count and the expected agent time in one line and wait for his go.
- Before merging or cutting any skill (the worth check has marked none CUT; ten are TRIM, a recommendation only).
- When S6's exit check passes: every case passes on all three models or carries a recorded reason, no skill is marked CUT by the worth check, results are in each TESTS.md; tests (3.x and 3.9), kb lint and budget pass (green, or yellow only on rows Mark has been told about); `claude plugin validate` passes on the root and on each plugin; `evergreen.py lint` passes on each skill; all of it quoted in the log. Then open a PR from `s6/evals` to `main` (it also carries S5, which PR #6 merged into `s4/camera-history`; say so in the PR body), assign m4bwav, add the needs-review label, give him the PR link and a short summary of what works, and stop. The PR holds code, so it waits for his review; do not merge it. Also stop before any hosted render, before publishing anything (the repo stays private), and before changing another repo.

## Chain rule

When this session's step is done, rewrite `ai-docs/next-session-prompt.md` as the prompt for the next fresh session: what to read first (only what that step needs), the step and its limits, the rules, when to stop and ask, and this paragraph unchanged at the end. Commit it with the handoff and paste it in your final message.
