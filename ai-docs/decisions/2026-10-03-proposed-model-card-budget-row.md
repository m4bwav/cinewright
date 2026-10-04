---
title: Proposed model-card budget row (awaiting Mark)
kind: decision
status: proposed
date: 2026-10-03
verified: 2026-10-03
stale_after: 2026-11-03
tags: [budget, model-cards, genvideo]
summary: "Read before adding a fact to a model card: all nine sit at 640-700 est. tokens against a 700 line; the proposed separate row and its numbers"
---

# Proposed model-card budget row (awaiting Mark)

## Context

PLAN §6 sets reference entries at 700 estimated tokens (green) and 1,200 (red). In S2 the nine model cards measure 646-700, and the two failure-code entries 695-700. Bringing H3 (843 at first) and Veo (802) to green took cutting repetition and prose, not facts. The size table, layout and dialogue templates in the Compile block are data that the compiler needs, about 330 tokens for H3. The next fact anyone adds (a new resolution, a price change) will tip a card into yellow.

## Decision (proposed, not applied)

Add one row to PLAN §6 and to `BUDGETS` in `scripts/cine.py`:

| Measure | Green | Yellow | Red |
|---|---|---|---|
| Model card tokens (est.), Compile block included | ≤ 900 | 901-1,200 | > 1,200 |

The row applies only to entries whose frontmatter has `model`. Ordinary entries keep 700.

A typical task loads one model card, so the extra 200 tokens fall within the 5,000-token task target (§6).

## Reasons

A card has to hold vendor facts, rules and a machine-read Compile block all at once. Ordinary entries hold only the first two. Rejected: moving Compile blocks to a separate JSON file, because that would split one model's truth across two files and the drift check would need a new path.

Until Mark answers, thresholds stay as they are and cards are kept under 700.

Related: see also [../plans/PLAN.md](../plans/PLAN.md)
