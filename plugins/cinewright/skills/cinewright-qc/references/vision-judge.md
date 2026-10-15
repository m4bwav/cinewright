---
title: Using a vision model as a judge
slug: vision-judge
summary: Turn a card into short claims, have a vision model describe the frames before judging, never show it the card text, crop small parts, let geometry decide sides and counts, and escalate split verdicts.
tags: [qc, judge, vlm, claims, crops, escalation]
last_checked: 2026-10-15
sources: ["field test 2026-10-14/15: 624 claims on a sky-duel film judged by gemma4:26b against the agent's reads by eye", "caption-then-verify, arXiv 2608.15574, 2026-08", "SPOTLIGHT, arXiv 2511.18102", "ViCrop, arXiv 2502.17422, ICLR 2025", "ViewSpatial-Bench, arXiv 2505.21500", "VQAScore, arXiv 2404.01291", "Gemma 4 model card (visual token budgets), Hugging Face google/gemma-4-26B-A4B-it", "Gemini API video understanding docs, https://ai.google.dev/gemini-api/docs/video-understanding (read 2026-10-15)"]
volatile_claims: ["Ollama returns logprobs for the first generated token only (0.35.1)", "agreement figures for gemma4:26b"]
---

# Using a vision model as a judge

## Rules

- Judge claims, not shots: split the card's action into short clauses and add the standing claims from reviewer notes (`qc rubric` items are claims too). Give each an id and ask for the verdicts keyed by id; numbered replies drift.
- Never show the judge the card text. Give it only what it needs to tell people apart (each character's looks), make it describe each frame first, then judge the claims from that description: yes only when clearly seen, no when the frames show otherwise or the thing is not there, unclear when out of frame.
- Ask all of a shot's claims in one reply. Asking each claim alone after a blind description made the judge call every claim the description did not mention false (82 % and 69 % against 92 % for the batch on the same claims).
- Small parts (hands, feet, held props, faces, a palm on a blade) go as crops beside the full frame, never only inside a grid: a 2x2 grid gives each frame about a quarter of the model's image budget. A per-person crop of native frames raised detail claims from 28 to 34 of 45.
- Let geometry answer what it can: screen left or right from detector boxes and face ids, people count from a person detector, gaze to the lens and smiling from face landmarks. Ask the model only what is left. Write sides as screen-left and screen-right; models confuse a person's own left with the viewer's.
- Timed events (a clash, a spear dissolving, someone rising from cloud) fall between quarter frames: sample densely around motion peaks, or two-second windows at 4 fps.
- Trust a yes more than a no: in the field test a yes given in both claim orders was almost always right, while most errors were false noes. Re-run the judge with the claims in reverse order; decide where both runs agree, and send splits to the next level.
- Escalation ladder: the local judge; then the agent itself on full-size frames and crops; then a hosted video model on the clipped window for timed events (it hears the sound, which settles scream against smile); then the reviewer's morning list.
- Keep a ledger: every claim, the judge's verdict, the agent's own read made before looking at the judge, and the judge's agreement and kappa per prompt version (entry judge-calibration).
- Physics judges sold as such ignore shuffled and frozen frames; ask concrete physical claims ("the falling spear turns to mist") instead.

## Numbers

- Agreement with the agent's reads on 624 claims (gemma4:26b): card text given 53 %; describe first, no card text 79 %; claims keyed by id 83 %.
- Two runs in opposite claim order, 368 claims: a yes in both was right 228 of 231 times (95 % bound 96-99.6 %) and covered 63 % of claims; a no in both only 54 of 95; 11 % split. Footwear claims were right 19 % of the time even on per-person crops: check feet yourself.
- Local cost: about 20-35 s a card on a 26B model; with a cached image prefix a follow-up question costs under a second.

## Pitfalls

- A judge prompt changed and adopted on one round: test it on the labelled set and under two paraphrases.
- Ollama 0.35.1 returns a log probability for the first generated token only, so a P(yes) score needs the verdict as the first token, and that costs accuracy (above).

## Verify

- The ledger's latest prompt version agrees with the reviewer at least as well as the one before it.

Related: builds on [qc-loop](qc-loop.md); see also [identity-score](identity-score.md), [judge-calibration](judge-calibration.md), [review-passes](review-passes.md).
