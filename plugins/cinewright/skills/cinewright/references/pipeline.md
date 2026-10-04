---
title: Default film pipeline
slug: pipeline
summary: The one default path from idea to delivery, the gate each stage must pass before the next, the repair cost ladder, and the money rule.
tags: [pipeline, producing, workflow, gates]
last_checked: 2026-10-03
sources: ["Steven D. Katz, Film Directing Shot by Shot, 1991", "Walter Murch, In the Blink of an Eye, 2nd ed., 2001", "https://cloud.google.com/blog/products/ai-machine-learning/ultimate-prompting-guide-for-veo-3-1"]
---

# Default film pipeline

## Rules

Stages in order. A stage starts only when the one before passed its gate.

| Stage | Gate (evidence) |
|---|---|
| Brief: logline, length, format, beats | `brief.md` exists, logline is one sentence |
| Bibles: style, characters, locations, scenes | `cards validate` shows 0 errors in `bibles/` |
| Shot list: one card per shot | every card validates; 3-8 s; one subject, one action, one move |
| Continuity | `continuity diff` shows 0 errors |
| Prompts | one compiled file per card, warnings read and handled |
| Reference sheets and keyframes | identity refs exist for every recurring character before the first render |
| Render | one take per card logged with seed and verdict |
| QC | each take checked against its card; fails routed by the repair ladder |
| Edit, grade, mix, deliver | the cut matches target length; loudness and format to spec |

- Plan few long generations over many short ones when the model can hold several shots in one generation (timestamp blocks): every seam between separate generations can read as the scene restarting.
- Put seams only at real changes of place or camera side. Carry one continuous sound across each remaining seam.
- Writing a prompt never authorises a paid render. Ask before each hosted call.

## Numbers

- Shot length 3-8 s. Under 3 s the model rarely finishes an action; past 8 s motion drifts.
- Three failed takes of one card: stop rerolling and re-plan the card.

## Vocabulary

Repair cost ladder, cheapest first. Try each rung once before climbing:

1. prompt wording, 2. one parameter (seed, duration, strength), 3. regenerate, 4. new keyframe or start frame, 5. video-to-video fix, 6. re-plan the card, 7. fix in the edit (cut around, reframe, speed), 8. cut the shot.

## Pitfalls

- Changing two things per reroll: you cannot tell which one helped. Change one.
- A continuation take needs the previous take's observed end state, not the planned one.

## Notes

- 2026-10-03: ladder, one-change-per-reroll and observed-end-state rules are ideas from MIT-licensed skill repos, credited in the README.
