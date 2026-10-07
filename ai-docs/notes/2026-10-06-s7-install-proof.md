---
title: S7 install proof, route by route
kind: note
status: active
date: 2026-10-06
verified: 2026-10-07
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

## Public repo retest (2026-10-07, after the history rewrite)

| Host | Route | Result |
|---|---|---|
| Claude Code | `claude plugin marketplace add m4bwav/cinewright --scope local`, `claude plugin install cinewright@cinewright --scope local`, clean cache | 5 skills; Sonnet called `Skill cinewright:cinewright-continuity` and its `cine.py`. PASS. Haiku answered without the skill in its one run |
| GitHub Copilot CLI | `copilot plugin marketplace add m4bwav/cinewright`, `copilot plugin install cinewright@cinewright` | "Installed 5 skills"; `skill` called with `cinewright-continuity`. PASS |
| any agent (`gh skill`) | `gh skill install m4bwav/cinewright cinewright-continuity --agent claude-code --scope project` | exit 0, files and `metadata:` block written; Sonnet called `Skill cinewright-continuity`. PASS |
| claude.ai Upload, claude.ai Add marketplace, VS Code Copilot | as above | not run: the agent's browser was refused for claude.ai, and VS Code needs a settings change and the chat UI. WAIT for Mark |

All three test installs removed, including the plugin cache folder.

## Account routes (2026-10-07, S7c, release v0.1.0)

Mark approved all three in the session. Same trigger prompt; tag v0.1.0 (main fad9ec6).

| Host | Route | Result |
|---|---|---|
| claude.ai (Opus 5.5) | Customize > Skills > Add > Upload skill, `dist/cinewright-continuity.zip` from the release | uploaded (26 files, enabled). New chat: activity shows "Loaded skill cinewright-continuity", then its Step 0 ran ("Check skill freshness and load axis rules", no failure); footer "Used in this session: Skills: cinewright-continuity". PASS |
| claude.ai (Opus 5.5) | Customize > Plugins > Add > Add marketplace > Add from a repository, `m4bwav/cinewright`, Sync | marketplace listed all three plugins (Cinewright, Cinewright craft, Cinewright dev); Add on Cinewright: "0.1.0, 5 skills". New chat: "Loaded skill cinewright-continuity (cinewright)". Trigger PASS. Script FAIL: the model ran `cd /mnt/skills/plugins/cinewright:cinewright-continuity`, which does not exist, so every `cine.py` call failed (exit 2) and it answered from general knowledge |
| VS Code 1.141 Copilot Chat | `chat.plugins.enabled: true` and `chat.plugins.marketplaces: ["m4bwav/cinewright"]` in user settings; install with `copilot plugin install cinewright@cinewright` into `~/.copilot/installed-plugins/` (the folder VS Code reads); trigger with `code chat -n -m agent "<prompt>"` | VS Code ran the chat through its Copilot CLI agent host; the session's `events.jsonl` shows `skill` called with `cinewright-continuity`, then `view` of its `evergreen.json` and `references/axis-and-screen-direction.md` under the installed folder. PASS, with a caveat: installed by the CLI, not VS Code's Install button (the agent cannot click in the VS Code window) |

Quirks:

- claude.ai plugin route: plugin skills are namespaced `cinewright:cinewright-continuity`, and the model guessed that as a folder name. "Run from the folder holding this file" is not enough there; the skills need a way to find their own folder. Open, see LEARNINGS L-006 `claude-ai-plugin-skill-folder-unknown` in cinewright-continuity. An uploaded skill (the ZIP route) did not hit it.
- claude.ai Add marketplace shows a toast, "Auto-sync requires the Claude GitHub App to have access to this repository" with Grant access. Not granted; the manual sync worked without it.
- claude.ai has no visible control to remove an added marketplace source (only a Source filter entry "cinewright"). Removing an uploaded skill is a permanent delete ("This skill and its version history will be permanently deleted"), which the agent leaves to Mark.
- Both claude.ai chats were connected to the PC through Claude Desktop and said "your evergreen plugin is overdue for its research refresh": that came from the PC's session hook, not from the skill (continuity's `next_due` is 2027-01-31).
- The release ZIPs were unzipped and scanned for drive paths, LAN addresses, hostnames, GPU names and the sidecar's private names: clean (one substring false positive inside the public `github.com/m4bwav/...` URL).

Cleanup: VS Code: plugin uninstalled, marketplace removed, `~/.copilot/config.json` and `settings.json` hold no cinewright entry, VS Code user settings restored byte-identical to the backup. claude.ai: plugin removed ("You can add it back later"); uploaded skill switched off. Left for Mark: delete the uploaded skill (permanent), remove the cinewright marketplace source if the UI offers it, close the VS Code window `code chat -n` opened.
