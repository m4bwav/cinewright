---
title: Choosing between takes and spending rerolls
slug: take-selection
summary: Pick keepers by comparing takes two at a time in both orders, not by absolute scores; cap blind rerolls near three, then reroll with the critique; repair local faults; re-plan model limits.
tags: [qc, selection, pairwise, reroll, budget, repair]
last_checked: 2026-10-22
sources: ["Huyen, AI Engineering, O'Reilly 2025, on position bias in judges and reviewers", "VISTA, arXiv 2510.15831, CVPR 2026", "VLM judges can rank but cannot score, arXiv 2604.25235, 2026", "Ma et al., inference-time scaling for diffusion, arXiv 2501.09732", "ReflectionFlow, arXiv 2504.16080", "VideoRepair, arXiv 2411.15115; GEARS, arXiv 2608.29322", "CHIEF, arXiv 2606.18591", "practitioner take selector on local H3, https://www.reddit.com/r/comfyui/comments/1vix8l9/ (2026-08)", "Walter Murch, In the Blink of an Eye, 2nd ed., 2001"]
---

# Choosing between takes and spending rerolls

## Rules

- Gates first: a take that fails a proven gate is out whatever else it does well (entry judge-calibration).
- Rank the takes that pass by comparing two at a time: the same frame times of both side by side, one named axis per question (identity, gaze, blocking and screen side, restraint of the acting, life in the motion, sound), asked in both orders. Count a win only when both orders agree; a split is a tie and goes to the reviewer.
- Show the reviewer the two takes in random order, never the keeper always on one side, and record which take was on which side with the answer. People lean to the last option and model judges to the first, so a fixed side turns into a bias. With the sides recorded, the answers can be checked for one (after Huyen, *AI Engineering*).
- Never sum metrics that disagree. When face match and sharpness (or word recall) point at different takes, that is a review trigger. A frozen clip scores sharp, so a motion measure must sit beside any sharpness measure.
- Classify every fault before the next take: a prompt cause (missing, vague or conflicting words; edit the card) or a model limit (the model will not do it; re-plan the card, change the shot, or cut around it). Do not reroll model limits.
- Blind rerolls: about three per card. After that, reroll with the last take's critique in hand and change the one thing it names (entry qc-loop).
- A local fault in an otherwise good take is a repair, not a reroll: a region re-render, a face pass, a cut around the frames, or an insert.
- Fix structure before style: positions, identity and action before light, grade and texture.
- Every iteration can bring new faults while removing old ones: compare the new take with the previous keeper on all axes, not only the one that changed.
- Stop when the best take has not changed for two rounds, or the card hits three strikes.
- Ask alignment (does the take match the card) and fidelity (does it look real) as two separate pairwise questions, and record the pick for each axis. One merged question lets a real-looking take that misses the card beat a faithful one (Foster, *Generative Deep Learning* 2e, ch. 13).
- Rank takes blind to what they cost: reroll counts, render time and the planner's hopes stay out of the first pass. A take that took five rerolls has no claim on the cut (after Murch).

## Numbers

- Removing pairwise selection cut VISTA's win rate from 45.9 % to 33.3 %; a single non-adversarial judge (17.2 %) did worse than no refinement.
- Reflection-guided rerolls lifted hard prompts from 0.10 to 0.81 and easy ones only from 0.95 to 0.97: spend rerolls on hard shots.
- Reported keep rates: about 1 in 10 on closed models; 4-25 % in commercial AI shorts.

## Pitfalls

- Absolute scores a few points apart: noise. Rank pairwise.
- A VLM judge sees a clip as a few frames squeezed into a fixed token budget: evenly spaced frames can skip the moment that decides the take. Sample at beat times (contact, cut points) instead (Foster, *Generative Deep Learning* 2e, ch. 13).
- A judge used as the only selector across many samples: the search finds that judge's blind spots.

## Verify

- Each pick in a board names its pairwise wins and any ties sent to the reviewer.
- Over a run of reviewer answers, the share of left picks sits near half; a 95 % interval clear of 50 % is a side bias to fix before trusting the labels.

Related: builds on [qc-loop](qc-loop.md); see also [judge-calibration](judge-calibration.md), [vision-judge](vision-judge.md).
