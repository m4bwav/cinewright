# AGENTS.md

Rules for any AI agent (Claude Code, Copilot, Cursor, Codex) working in this repository. `CLAUDE.md` and `.github/copilot-instructions.md` only point here.

## What this is

cinewright: an evergreen plugin set that gives an agent the craft of every film role plus AI video generation, so generated video is coherent within and between shots. Status: S1 built (scaffold, three core skills, Veo 3.1 compile, worked example); where things live is in [CODEMAP.md](CODEMAP.md). The plan is [ai-docs/plans/PLAN.md](ai-docs/plans/PLAN.md); the next session's prompt is [ai-docs/next-session-prompt.md](ai-docs/next-session-prompt.md); start with [ai-docs/HANDOFF.md](ai-docs/HANDOFF.md).

## Rules

- This repository goes public at release. Nothing that ships may hold LAN addresses, hostnames, GPU models, local drive paths, or names of the maintainer's private projects. Private notes go to the everlast vault sidecar (`--private`).
- Knowledge is written as rules, numbers and vocabulary a capable model lacks. One default, not a menu. Cite primary sources; mark what is unverified; date anything that changes.
- Small files with pointers. A skill reads its generated `references/INDEX.md`, then opens only the entries it needs. Scripts are run, never read. Size budgets in PLAN.md are enforced by lint and CI.
- Take ideas from other skill repos, never text. Anything adapted from smixs/visual-skills (CC BY 4.0) carries attribution.
- Every skill is an evergreen unit (RESEARCH, CHANGELOG, LEARNINGS, TESTS, evergreen.json, evals).
- Relative markdown links, never wikilinks. Cite lessons with their code names, not bare IDs.
- No AI attribution anywhere: no Co-Authored-By trailers, no "generated with" lines in commits, PRs or files.
- Prose: plain short sentences, no em dashes.
- Edit vocabulary, schemas and the runtime library in `shared/`, never the copies inside a skill. Run `python scripts/cine.py build`, then the checks below; lint fails on drift.
- Before a PR: `python -m unittest discover -s tests`, `python scripts/cine.py kb lint`, `python scripts/cine.py budget` (red fails; tell Mark about a yellow in one line), `claude plugin validate` on the root and each `plugins/*` folder. CI is manual-dispatch while private, so run these locally and quote the output in `ai-docs/log.md`.
- Shipped files cite lessons from private projects as "field lesson NNN" with a title, never the project's name (see the decision in `ai-docs/decisions/`).

## everlast (session knowledge, load on demand)

- `ai-docs/INDEX.md` lists what past sessions learned here (solutions with verified commands, decisions with reasons, plans). At the start of a task, scan it and open only the entries whose title or tags match; no line matches: `everlast.py search "<key terms>"` before concluding nothing was recorded. Read `ai-docs/HANDOFF.md` when continuing unfinished work (everlast-resume skill).
- Before acting on an entry marked `(recheck due)`, run `everlast.py recheck <entry>`, re-run its Verified-by command only when that is read-only or safe (a build, a test, a version query), then record `everlast.py verify <entry>` or `verify <entry> --failed "what broke"`; a fix that changed is superseded, never reused blindly.
- Before finishing a task that hit a dead end, verified a non-obvious command, made a design choice, or taught you something about the user, record it (everlast-capture skill, or `everlast.py note` / `handoff`); rewrite `HANDOFF.md` when work is left unfinished. Say "nothing to record" when that is true.
- Anything naming a person, an internal host or name, a credential, or an opinion about people goes to the private sidecar (`--private`), never here. Lessons about the user or this machine go to the user tier (`--user`).
- Rules go in this file, system layout in CODEMAP.md; the doc set holds only what could not be re-derived from the code in a minute.
- Link documents together with relative markdown links: every markdown folder is reachable from an index whose lines say when to read each file (`ai-docs/INDEX.md` is generated from frontmatter; give entries a one-line `summary`), and an entry links the entries it relates to on a typed `Related:` line (`supersedes`, `contradicts`, `builds on`, `see also`). The set then reads as a graph for people in Obsidian and for agents alike. No wikilinks in the repo.
