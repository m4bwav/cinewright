---
title: Identity score
slug: identity-score
summary: Score who is on screen by face embeddings against the character bible's refs (and props by crop similarity), with a margin over the other cast; trustworthy on MCU and closer, n/a on small faces.
tags: [qc, identity, faces, props, scoring, references]
last_checked: 2026-10-09
sources: ["OpenCV Zoo, YuNet face detector and SFace recognizer (Apache 2.0)", "ConsisID and OpenS2V-Eval benchmarks: FaceSim-Arc, NexusScore, 2025-2026", "VBench subject consistency (DINO features)", "field test on two eight-section films against the reviewer's verdicts, 2026-10-09"]
volatile_claims: ["InsightFace model weights are non-commercial", "thresholds tuned on one face model"]
---

# Identity score

## Rules

- Score faces against the character bible's `refs`: detect each face, embed it, take the cosine to every character's refs. A face is that character only when it scores high and beats every other cast member by a margin. Refs of two people can be close (0.49 between two old men in one test), so the margin matters more than the score.
- Score three frames per shot, spread across it, not one.
- Props, animals, masked or drawn characters: crop the subject with an open-vocabulary detector (its bible description as the text), then compare crop features (DINOv2) with its sheet.
- Verdicts: match, weak, other (a rival cast member or an uncast stranger wins), not found, n/a (no face big enough). Only "other" on a close shot is a hard fault; send it back with `identity-drift`.
- Faces under about 60 px (wide shots, faces behind car glass) are n/a, not a pass: at 40 to 45 px the right actor scored no better than a stranger. Check those by eye or with the vision rubric.
- Compare the picked takes of one character with each other too: a pass whose own refs were replaced (an old look kept in its folder) scores well against itself and only the cross-take check catches it.
- Licence: InsightFace's ArcFace weights are non-commercial; OpenCV's YuNet and SFace are Apache 2.0 and enough for this.

## Numbers

- SFace cosine, from one tuning run: match at 0.42 or more and 0.08 ahead of every rival; weak from 0.25; other when a rival reaches 0.30. The model's own "same person" line is 0.363.
- Prop crops with DINOv2: match 0.55, weak 0.40.
- Cost: about 7 s a take on a CPU for faces, about 20 s more with prop crops.

## Vocabulary

- face embedding, cosine similarity, margin, FaceSim, subject consistency.

## Pitfalls

- Trusting a high score with a small margin: the refs themselves are alike.
- Reading n/a as a pass on wide shots.

## Verify

- Run it on a pass the reviewer already judged: every take they rejected for the wrong person scores "other" or low, and every keeper scores match.
