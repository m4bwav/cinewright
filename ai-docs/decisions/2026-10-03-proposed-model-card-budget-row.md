---
title: Model-card budget row (accepted)
kind: decision
status: accepted
date: 2026-10-03
verified: 2026-10-04
stale_after: 2027-01-04
tags: [budget, model-cards, genvideo]
summary: "Read before adding a fact to a model card: cards have their own budget row, green at 900 est. tokens, red over 1,200; ordinary entries keep 700"
---

# Model-card budget row (accepted)

## Context

PLAN §6 sets reference entries at 700 estimated tokens (green) and 1,200 (red). In S2 the nine model cards measured 646-700, and the two failure-code entries 695-700. Bringing H3 (843 at first) and Veo (802) to green took cutting repetition and prose, not facts. The size table, layout and dialogue templates in the Compile block are data that the compiler needs, about 330 tokens for H3. The next fact anyone added (a new resolution, a price change) would have tipped a card into yellow.

## Decision

Proposed in S2; Mark answered on 2026-10-04 ("apply your budget thing if you think its cool") and S3 applied it. One row in PLAN §6 and in `BUDGETS` in `scripts/cine.py`:

| Measure | Green | Yellow | Red |
|---|---|---|---|
| Model card tokens (est.), Compile block included | ≤ 900 | 901-1,200 | > 1,200 |

The row applies only to entries whose frontmatter has `model` (`measure()` routes them to `card_tokens`). Ordinary entries, including the failure-code tables, keep 700. Line limits (60 green) still apply to cards.

A typical task loads one model card, so the extra 200 tokens fall within the 5,000-token task target (§6).

## Reasons

A card has to hold vendor facts, rules and a machine-read Compile block all at once. Ordinary entries hold only the first two. Rejected: moving Compile blocks to a separate JSON file, because that would split one model's truth across two files and the drift check would need a new path.

Related: see also [../plans/PLAN.md](../plans/PLAN.md)
