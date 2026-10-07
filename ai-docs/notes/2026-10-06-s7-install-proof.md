---
title: S7 install proof, route by route
kind: note
status: active
date: 2026-10-06
verified: 2026-10-06
stale_after: 2027-01-06
tags: [install, packaging, s7, claude-code, copilot, gh-skill, claude-ai]
summary: "Read before the release or a public-route retest: which install routes were run on the private repo (Windows, 2026-10-06), the exact commands, what triggered, and which routes wait for Mark"
---

# S7 install proof (private repo, Windows 11, 2026-10-06)

## Summary

Three routes installed and triggered on the private repo (Claude Code, Copilot CLI, `gh skill`); three wait for Mark's go because they change his claude.ai account or VS Code settings; no second OS.

## Routes

Every route used `main` at f83076f (13 skills; curate is on `s7/package`). Each test install was removed afterwards. Trigger prompt in each: "My AI video clips keep flipping which side the two characters are on between shots. How do I keep them consistent?"

| Host | Route and command | Result |
|---|---|---|
| Claude Code 2.1.281 | `claude plugin marketplace add m4bwav/cinewright --scope local`, `claude plugin install cinewright@cinewright --scope local` in a temp git folder | installed (5 skills from the plugin cache); headless Sonnet run called `Skill cinewright:cinewright-continuity`, then ran its `cine.py`. PASS |
| GitHub Copilot CLI 1.0.92 | `copilot plugin marketplace add m4bwav/cinewright`, `copilot plugin install cinewright@cinewright` | "Installed 5 skills"; `copilot -p ... --output-format json` called `skill` with `cinewright-continuity`. PASS |
| any agent, GitHub CLI 2.100.0 | `gh skill install m4bwav/cinewright cinewright-continuity --agent claude-code --scope project` | found all 13 skills under `plugins/*/skills/` ("plugins/ convention"); installed to `.claude/skills/`; its `cine.py kb search` runs; headless Sonnet run called `Skill cinewright-continuity`. PASS |
| claude.ai | Customize > Skills > Add > Upload skill, `dist/cinewright-continuity.zip` | the form accepted the ZIP and its preview showed the right name and description; Upload not clicked (it adds a skill to Mark's account). WAITS for Mark |
| claude.ai / Desktop | Customize > Plugins > Add marketplace | not run: adds a marketplace to Mark's account, and a private repo needs the GitHub connection. WAITS for Mark (or for the public repo) |
| VS Code Copilot 1.140 | `chat.plugins.marketplaces` or "Chat: Install Plugin From Source" | not run: changes VS Code user settings. WAITS for Mark |
| second OS | none | untested elsewhere |

Quirks:

- `gh skill install` lists skills as `[plugins] cinewright/cinewright-continuity` but refuses that namespaced form ("not found"); the plain name works. Its first install printed "could not read directory" and exited 2 after writing every file; a second call reported "already installed". The installed SKILL.md gains a `metadata:` block (github-path, ref, repo, tree-sha).
- `claude plugin uninstall` and `marketplace remove` leave `~/.claude/plugins/cache/cinewright/` behind; delete it by hand after a test.
- ZIPs: `python scripts/cine.py zip <skill>` for each of the 13 public skills, 44-70 KB each, written to `dist/` (gitignored; they are release assets). Curate gets no ZIP: it needs a repository checkout.

Related: [../plans/PLAN.md](../plans/PLAN.md) §9 (statuses updated from this note)
