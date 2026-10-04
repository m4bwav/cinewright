---
title: The QC loop
slug: qc-loop
summary: How to judge a take against its card from a contact sheet, last frame and audio; verdict rules, frame sampling numbers, one change per reroll, three strikes.
tags: [qc, review, rubric, takes, sampling]
last_checked: 2026-10-03
sources: ["https://arxiv.org/abs/2503.21755", "https://tech.ebu.ch/publications/r128", "Pat P. Miller, Script Supervising and Film Continuity, 3rd ed., 1999"]
---

# The QC loop

## Rules

- Judge against the card and the bibles, never against taste. A beautiful take that breaks the card fails.
- Read identity, wardrobe and props against the bible word by word, on one full frame per shot: a mark's side is the character's left or right, not yours.
- A fail names what you saw in the note ("braid gone after 2 s"), not a mood ("feels off").
- Unsure is `fail` with a note; a later reviewer can pass it. Never pass what you could not see: mark it `na` and say why.
- One code per failed item: the one whose symptom matches what you saw.
- The next take changes one thing: the cheapest fix the rubric prints. Two changes hide which one worked.
- Keep the seed when only the end is wrong; change it when the opening is wrong (the seed fixes the opening).
- Three failed takes of one card: re-plan the card. The card asks for something the model will not do.
- A take that fails only on edit-stage codes is kept as `keep-fix-in-edit`.
- Record the observed end state of every kept take; the next card starts from what is there, not what was planned.

## Numbers

- Sheet sampling: 2 fps for clips up to 10 s, 1 fps beyond; 4 columns, 320 px wide frames.
- Spec: length may run long (trim in the edit) but not 0.05 s short; aspect within 2 %; fps exact.
- Loudness default: -16 LUFS integrated within 1 LU, true peak at or below -1 dBTP (cinewright's web default; broadcast is -23 LUFS under EBU R128). Re-checked in S5.

## Pitfalls

- Fast motion between sampled frames hides morphs and hand errors: for action shots, add `--fps 4` on the moving part.
- The first frames of an image-to-video take hold still; that is `frozen-start`, fixed in the edit, not a reroll.

## Notes

- 2026-10-03: automatic VLM scorers (VBench-2.0 and successors) measure model quality across many clips, not one take against a card; the rubric is judged by the agent or a person.
