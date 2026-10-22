---
title: Calibrating a judge against the reviewer
slug: judge-calibration
summary: Keep a labelled set of reviewer verdicts, score every gate and judge prompt on it with kappa and interval bounds, let a check reject alone only above a 90 % lower bound, re-run on edits.
tags: [qc, judge, calibration, labels, kappa, gates, regression]
last_checked: 2026-10-22
sources: ["Huyen, AI Engineering, O'Reilly 2025, on feedback loops", "Thakur et al., Judging the Judges, arXiv 2406.12624", "Trust or Escalate, ICLR 2025, arXiv 2407.18370", "EvalGen, Who Validates the Validators, UIST 2024, arXiv 2404.12272", "Rubric-induced preference drift, arXiv 2602.13576, 2026", "Stroebl, Kapoor, Narayanan, inference scaling flaws, arXiv 2411.17501", "Hamel Husain, Creating an LLM judge that drives business results, https://hamel.dev/blog/posts/llm-judge/", "field test 2026-10-12 and 2026-10-15: 152 labelled takes, 624 labelled claims"]
---

# Calibrating a judge against the reviewer

## Rules

- Keep a labelled set: one row per take (and per shot where a note names it) with the reviewer's verdict, fault codes and the line the verdict came from. The reviewer's word outranks the agent's; a keeper the reviewer later faulted is the most valuable row.
- Labels are binary pass/fail plus a written reason, never 1-5.
- Score every check on that set before trusting it: precision and recall per fault code, how many keepers it would reject, and Cohen's kappa. Raw agreement flatters a judge when most answers are yes (83 % agreement is kappa 0.47 when both sides say yes 80 % of the time).
- A check may reject a take on its own only when the 95 % lower bound of its reject precision is 90 % or more and it rejected no keeper. Otherwise it flags for review. Use the bound, not the point value: 27 of 30 is 74-97 %.
- Every change to a judge prompt, a standing claim or a threshold is a release: re-run the labelled set and the ledger, and keep the change only when kappa does not drop. Edits that look harmless can move a judge by tens of points.
- When the agent's own reads are the labels, read the frames before reading the judge's answer, or the labels copy the judge.
- A judge that abstains is better than one that guesses: below its calibrated confidence it says "review" and the take goes to the escalation queue (entry vision-judge).
- Every reviewer correction becomes a standing claim at once, judged and logged from the next take on; it becomes a gate only after it passes the bar above.
- Re-label a few random takes each week, unannounced, to catch drift in the judge and in the labels.
- Put a few takes the gates removed into every film's label queue, picked at random. Labels taken only on takes that passed the gates can never show a gate wrong. The loop sees only what it chose to show (after Huyen, *AI Engineering*, on degenerate feedback loops).
- With an imperfect verifier, more samples stop helping early: its false-positive rate caps what rerolling can reach. Measure false positives before raising the reroll budget (entry take-selection).

## Numbers

- Start with about 30 labelled examples, add until no new fault kinds appear.
- Kappa 0.61 or more is "substantial"; aim there before a judge decides alone.
- Expert to expert agreement runs about 72-75 % on creative work; a judge at that level matches a second reviewer.
- Rule of three: zero keepers rejected out of n bounds the true rate at about 3/n.

## Pitfalls

- Tuning thresholds on the same takes you report: hold out one film or one round.
- A judge variant that wins by staying silent: count a missing verdict as a miss.

## Verify

- The ledger prints kappa and interval bounds per check and per prompt variant, and the latest edit did not lower them.

Related: builds on [qc-loop](qc-loop.md); see also [vision-judge](vision-judge.md), [take-selection](take-selection.md).
