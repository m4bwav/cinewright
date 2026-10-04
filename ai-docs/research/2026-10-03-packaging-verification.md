---
title: Packaging claims checked against primary docs
date: 2026-10-03
kind: note
summary: Which install routes and manifest rules for Claude Code, claude.ai and Copilot hold as of 2026-10-03, and the one that changes the plugin layout.
tags: [packaging, marketplace, copilot, claude-ai, directory]
---

# Packaging claims checked (2026-10-03)

Read this when laying out plugin folders, writing manifests, or testing installs. It re-checks brief §10 and §12 ([2026-10-03-research-brief.md](2026-10-03-research-brief.md)) against primary docs.

| Claim | Verdict | Source |
|---|---|---|
| anthropics/skills slices one `skills/` tree with `"source": "./"`, `"strict": false`, `"skills": [...]` | Confirmed | https://github.com/anthropics/skills/blob/main/.claude-plugin/marketplace.json |
| Marketplace needs `name`, `owner` (`owner.name`), `plugins`; each entry `name` + `source` | Confirmed | https://code.claude.com/docs/en/plugins/marketplace-reference |
| Skill listing budget 1% of context; `description` + `when_to_use` cut at 1,536 chars | Confirmed | https://code.claude.com/docs/en/skills |
| Agent Skills frontmatter: only `name` (1-64, lowercase-hyphen, matches folder), `description` (1-1024), `license`, `compatibility` (1-500), `metadata` (string map), `allowed-tools` | Confirmed | https://agentskills.io/specification |
| claude.ai ZIP: the skill folder is the ZIP's top level | Confirmed | https://claude.com/docs/skills/how-to |
| claude.ai rejects unknown frontmatter keys | Not in docs; seen in anthropics/claude-code#24826 (closed as duplicate of #21758, closed 2026-03-25). Ship the six spec keys only | issue tracker |
| claude.ai: Customize > Plugins > Add marketplace (owner/repo) | Confirmed. Limits: 5,000 files and 200 MB per plugin. A top-level `bin/` makes chat refuse the plugin | https://claude.com/docs/plugins/platform-support |
| Agent Plugins 1.0: `plugin.json` with `$schema` + `name` | Confirmed, real, 1.0.0. `$schema`: `https://agent-plugins.org/schemas/1.0.0/plugin.schema.json`. MCP file is `mcp.json` | https://agent-plugins.org/specification |
| Copilot skill folders `.github/skills`, `.claude/skills`, `.agents/skills`, `~/.copilot/skills`, `~/.agents/skills` | Confirmed | https://docs.github.com/en/copilot/concepts/agents/about-agent-skills |
| `gh skill install OWNER/REPO SKILL` | Confirmed, gh 2.90.0+, still preview. Flags `--agent`, `--scope`, `--pin` | https://cli.github.com/manual/gh_skill |
| Copilot CLI `copilot plugin marketplace add owner/repo` reads `.claude-plugin/marketplace.json` | Confirmed, as its second location after `.github/plugin/` | https://docs.github.com/en/copilot/how-tos/copilot-cli/customize-copilot/plugins-marketplace |
| VS Code installs plugins from marketplaces | Confirmed: setting `chat.plugins.marketplaces`, command "Chat: Install Plugin From Source", Extensions view `@agentPlugins`. Reads Agent Plugins, Copilot and `.claude-plugin/plugin.json` manifests. Which `marketplace.json` path it reads: unverified (inferred `.claude-plugin/`) | https://code.visualstudio.com/docs/copilot/customization/agent-plugins |
| Netflix loudness −27 LKFS ±2 LU dialogue-gated, true peak −2 dBTP | Confirmed from Netflix spec text via search snippet; live page is JavaScript-only (now studiopartner.netflix.net). Re-read in a browser before encoding | Netflix Sound Mix Spec v1.5 |

## What changes the layout

- With `strict: false`, a plugin entry that lists `skills` must have no `plugin.json` declaring components in its folder, or the plugin fails to load. With no `plugin.json`, the marketplace entry is the manifest.
- The Claude directory takes **one plugin per submission** and wants `.claude-plugin/plugin.json` inside that plugin's folder. The root-sliced pattern serves a marketplace but cannot be submitted as is.
- Directory file rules: 512 files or fewer per plugin, non-image files under 256 KiB, no symlinks, submodules or LFS, README of 40+ words, a LICENSE, no `.DS_Store`/`Thumbs.db`, names safe on Windows and macOS. Checklist: https://claude.com/docs/plugins/pre-submission-checklist
- Conclusion used by the plan: physical plugin folders, each with its own `.claude-plugin/plugin.json` and Agent Plugins `plugin.json`, listed by one root marketplace. See [../plans/PLAN.md](../plans/PLAN.md) §3.

## Still to test (S7)

VS Code marketplace path; whether `gh skill install` finds skills under `plugins/*/skills/`; Copilot CLI install from this repo end to end; claude.ai plugin install of a nested plugin folder.

Related: builds on [2026-10-03-research-brief.md](2026-10-03-research-brief.md)
