---
title: Proposed runtime budget row (awaiting Mark)
kind: decision
status: proposed
date: 2026-10-04
verified: 2026-10-04
stale_after: 2026-11-04
tags: [budget, runtime, skill-folder]
summary: "Read before adding code to shared/lib/cine.py: the 70 KB runtime copy pushes genvideo's folder past 150 KB; proposal to measure the runtime once, in its own row"
---

# Proposed runtime budget row (awaiting Mark)

## Context

PLAN §6 sets the skill folder at 150 KB green, 300 KB yellow. That line was set before the runtime existed. `shared/lib/cine.py` is copied into every skill so a one-skill ZIP works alone; it is 70 KB after S3 (prop bible, `cards list`, two new diff checks) and S4 and S5 add more code. In S3 the genvideo folder reached 151 KB (yellow): 70 KB runtime, 16 KB schemas, the rest knowledge and companions. Without the runtime it is about 85 KB. Every other skill will cross 150 KB the same way as the runtime grows, whatever its own content.

## Decision (proposed, not applied)

Split one row into two in PLAN §6 and `BUDGETS` in `scripts/cine.py`:

| Measure | Green | Yellow | Red |
|---|---|---|---|
| Skill folder, excluding hash-tracked copies of `shared/lib/` | ≤ 150 KB | 151-300 KB | > 300 KB |
| Runtime (`shared/lib/cine.py`), measured once | ≤ 100 KB | 101-150 KB | > 150 KB |

The folder row then measures what each skill's author controls; the runtime row stops the shared code from growing without a check. `duplicates()` already treats hash-tracked copies this way.

Until Mark answers, the threshold stays as it is, the budget reads YELLOW on this one row, and `test_budget_green` became `test_budget_not_red` to match PLAN §6 (CI fails at red; yellow is reported).

## Reasons

The runtime is one file with one source; counting it once per skill makes the folder budget measure the copy mechanism, not the skill. Rejected: raising the folder line to 200 KB (hides real knowledge growth too); splitting the runtime into per-skill modules (genvideo needs compile and takes, so it saves little and adds a build step); cutting vocab copies from genvideo to get under the line (trades knowledge for a number).

Related: builds on [2026-10-03-shared-sources-copied-into-skills-with-a-hash-header.md](2026-10-03-shared-sources-copied-into-skills-with-a-hash-header.md); see also [2026-10-03-proposed-model-card-budget-row.md](2026-10-03-proposed-model-card-budget-row.md)
