---
title: strict false slicing cannot go to the Claude directory
kind: solution
status: active
date: 2026-10-03
verified: 2026-10-03
stale_after: 2027-01-01
tags: [packaging, marketplace, directory]
summary: "Read before changing plugin layout: why cinewright uses physical plugin folders, plus other session-1 surprises"
---

# strict false slicing cannot go to the Claude directory

## Problem

The kickoff asked for the anthropics/skills pattern: one shared `skills/` tree sliced into plugins with `"source": "./"` and `"strict": false`, plus a root Agent Plugins `plugin.json`.

## What was found (2026-10-03)

- With `strict: false`, a plugin folder whose `plugin.json` declares components conflicts with the marketplace entry and the plugin fails to load. With no `plugin.json`, the entry is the manifest (https://code.claude.com/docs/en/plugins/marketplace-reference).
- The Claude directory takes one plugin per submission and wants `.claude-plugin/plugin.json` in that plugin's folder (https://claude.com/docs/plugins/pre-submission-checklist). Root slicing cannot be submitted as is.
- Directory limits that bite a one-file-per-entry knowledge base: 512 files per plugin, non-image files under 256 KiB.

## Fix

Physical plugin folders under `plugins/`, each with its own Claude manifest and Agent Plugins `plugin.json`, listed by one root marketplace. See [../plans/PLAN.md](../plans/PLAN.md) §3 and §6 (files-per-plugin budget).

## Other surprises this session

- Evergreen's index rules are in PROTOCOL.md §9 (Tone and hygiene), not §10; §10 is the trunk-and-clones publishing model.
- local-render's LEARNINGS entries have no kebab-case code names, so they are cited by ID and title.
- chartwright already ships `scripts/cw.py`; cinewright's CLI is `cine.py` to avoid the clash.

## Verified by

Read of the three doc pages above on 2026-10-03 (packaging subagent); [../research/2026-10-03-packaging-verification.md](../research/2026-10-03-packaging-verification.md).
