---
title: S1 built on the plan's recommendations for D1-D7
kind: decision
status: active
date: 2026-10-03
verified: 2026-10-03
stale_after: 2027-04-01
tags: [decisions, license, ci, slices]
summary: "Read before review: which PLAN §11 defaults S1 assumed (MIT, physical slices, manual-dispatch CI, bytes/4 tokens) because no answers existed"
---

# S1 built on the plan's recommendations for D1-D7

## Context

PR #1 was merged on 2026-10-04 with no comments, so none of PLAN §11 D1-D7 had an answer when S1 started.

## Decision

S1 used each recommendation and says so here, so Mark can overturn any of them in review.

| # | Used in S1 | Where it shows |
|---|---|---|
| D1 name | `cinewright` | everywhere |
| D2 license | MIT | `LICENSE` at the root and in each plugin folder |
| D3 slices | physical folders `plugins/cinewright` (3 skills now, 5 planned), `plugins/cinewright-craft` (empty), `plugins/cinewright-dev` (empty), all three in `.claude-plugin/marketplace.json` | manifests |
| D4 money | nothing spent; no render made | compile writes text only |
| D5 public | still private | |
| D6 CI | `.github/workflows/ci.yml` is `workflow_dispatch` only on `runs-on: [self-hosted]`; no runner is registered for this repo (`gh api repos/m4bwav/cinewright/actions/runners`: 0), so every check ran locally and the output is quoted in `log.md` | ci.yml header comment |
| D7 tokens | bytes / 4, labelled "est." in every budget line; no API key used | `cine.py budget` |

## Reasons

The S1 prompt says to build with the recommendations and say so when D2 or D3 is unanswered. Each choice is cheap to reverse: a license file, folder names, a workflow trigger.

Rejected: waiting for answers before building.

Related: builds on [../plans/PLAN.md](../plans/PLAN.md)
