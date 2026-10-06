---
title: Eval harness and model matrix
kind: decision
status: active
date: 2026-10-05
verified: 2026-10-05
stale_after: 2026-12-05
tags: [evals, harness, testing, haiku]
summary: "Read before running or judging cinewright's evals: how a run is isolated and graded, why craft compile cases load core, and how Haiku-only failures are recorded"
---

# Eval harness and model matrix

## Decision

1. One harness, `evals/run_evals.py`, runs every skill's `evals/evals.json` headless: a fresh folder on a drive other than the repository's with the example stripped of README, design notes and compiled prompts; a per-run copy of the plugin under test (`--plugin-dir`, `--add-dir`) or skills disabled for the baseline; `--restricted --strict-mcp-config --permission-mode dontAsk`; tools Read, Write, Edit, Bash (plus Skill with the skill); Bash allowed for `cine.py` in any form, ffmpeg, ffprobe and read-only or single-file commands. Since harness rev 2 (2026-10-05) both arms are told, in an appended system line naming no tool, that a refused command covers that command only. Every tool input's paths are scanned; a run that reached the repository is contaminated and runs again.
2. Grading: trigger on the Skill call (2 of 3; decoy 0 of 3); action on the trace (the `cine.py` call), never a file a baseline could write by hand; outcome on stdlib checkers (`checks`) first, then a three-vote Sonnet judge on the remaining expectations, given every assistant message and every file the run wrote.
3. A case names `plugins` it needs beside its own (craft cases that compile load core), because that is a real install and `compile` needs genvideo's model cards.
4. Models: Haiku 4.5, Sonnet 5, Opus 5.5, three runs each with the skill and one baseline per model on value cases. Worth is read from the same runs, pooled over models (`export-worth`, then `evergreen.py worth --results`).
5. Haiku: where Haiku answers in one turn without loading the skill, one description rewrite is made; if it does not move, the failure is recorded with that reason in TESTS.md and not tuned further. Sonnet and Opus failures are tuned to the three-iteration limit.

## Reasons

Each harness choice came from a fault that first looked like a skill failure ([../solutions/2026-10-05-headless-evals-on-windows-dead-ends.md](../solutions/2026-10-05-headless-evals-on-windows-dead-ends.md)). Haiku uses the skills on task prompts (sound, design and script triggers 3 of 3) but answers short advice prompts itself; a description that grew for Haiku costs every user's listing budget (3,888 of 4,000 characters), which Sonnet and Opus already trigger on.

## Rejected

- `claude plugin eval`: Bash cases need a sandbox that native Windows lacks (TESTING.md section 6).
- Unrestricted Bash with the path scan as the only guard: a Sonnet run tried `find /` for a missing compiler; the repository would be reachable.
- `acceptEdits` to allow `cp -r`: it ran the command but left no copy in the probe, so setup copies instead.

Related: [../plans/PLAN.md](../plans/PLAN.md) section 8
