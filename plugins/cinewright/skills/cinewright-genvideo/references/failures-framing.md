---
title: Failure codes, framing and composition
slug: failures-framing
summary: Failure codes for rendered takes whose composition breaks: edge and background tangents, a competing focal point, horizon faults, floating feet, missing depth, a wrong OTS.
tags: [vocab, qc, failures, taxonomy, framing, composition]
last_checked: 2026-10-22
sources: ["Marcos Mateu-Mestre, Framed Ink, 2010, and Framed Ink 2, 2016", "Joseph V. Mascelli, The Five C's of Cinematography, 1965", "Richard Garvey-Williams, Mastering Composition, 2014"]
---
<!-- copied from shared/vocab/failures-framing.md sha256:bc7f12233d71909c45598198a77f510c5acef6d79c91eaf473ce9e63a2d18ded; edit the source -->

# Failure codes, framing and composition

## Vocabulary

Rungs and checks as in `failures-picture`. The eye jumping across a cut is `attention-jump` there.

| Code | Symptom | Cause | Cheapest fix | Rung | Check |
|---|---|---|---|---|---|
| `edge-tangent` | a head, hand or key object just touches the frame edge | no margin in the position words | "well inside the frame", or crop boldly through a limb (never at a joint); reroll | 1 | framing |
| `bg-tangent` | a pole, lamp, door edge or bright object grows out of a head or sits right behind it | background busy or not described, worst in close-ups | describe a plain background that falls away; move the object in the prompt; re-plan the angle | 1 | framing |
| `focal-competitor` | a bright light or saturated patch out-pulls the subject | background brighter or more saturated than the subject | "background in shadow, the subject the brightest thing"; grade it down | 1 | framing |
| `horizon-split` | horizon at mid-frame where the card wanted it low or high | horizon words missing or late | set `camera.horizon`; put it early in the prompt | 1 | camera |
| `horizon-head` | the horizon or a long line runs through a head or neck | camera height and eye line coincide | change the camera height or the horizon third; reroll | 1 | framing |
| `floating-feet` | feet miss the ground plane, or a figure's scale jumps against its neighbours | no contact or depth cue | ground-contact words ("both feet planted on the flagstones"); depth or pose control | 4 | framing |
| `flat-depth` | no foreground layer where the card named one | the foreground object named late | name the foreground layer first in the subject line | 1 | space |
| `ots-wrong` | the near person's nose or eye shows past the cheek, so the OTS reads as a two-shot, or their hair or costume drifts | the near person's view unstated | `view: three-quarter-back` on the near person (compiles to "only the cheek line showing"); restate the wardrobe | 1 | framing |

## Rules

- Composition faults are the cheapest to prevent in the card: margins, a described background, the horizon third and the foreground named first.
- Log the code (`takes log --fix`) as for the picture codes; a framing fault that survives two rerolls goes to the crop or the grade (rung 7) before a re-plan.
