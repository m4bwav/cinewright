---
title: Failure codes, composites and scale
slug: failures-composite
summary: Failure codes for shots built from parts or meant to read huge (shadows that disagree, toy scale, a clipped fireball, a visible rig), plus who is in frame and beat order.
tags: [vocab, qc, failures, taxonomy, composite, scale]
last_checked: 2026-11-20
sources: ["PhyRubric, arXiv 2611.13576 (extra-person, beat-order: permanence and count failures 20.4 %, 25 % of takes never showed the event)", "Mark Sawicki, Filming the Fantastic: A Guide to Visual Effects Cinematography, 2nd ed. (paraphrased; book rules, unverified on our models)"]
---

# Failure codes, composites and scale

## Vocabulary

Columns as in failures-picture (rung = the repair ladder, check = the `qc rubric` item).

| Code | Symptom | Cause | Cheapest fix | Rung | Check |
|---|---|---|---|---|---|
| `shadow-mismatch` | an inserted subject's shadows point away from the plate's | parts made under different light | matching card (finish compositing-and-cleanup); regenerate the part with the plate's key | 3 | light |
| `toy-scale` | something huge reads small: shallow focus, clean surfaces, fast motion | no full-size cues on the card | deep focus, wear, slower motion (camera frame-rate-and-shutter) | 1 | camera |
| `clipped-fire` | a fireball, flash or lamp is a flat white blob | exposed for the scene, not the brightest source | ask for the flame's texture and a set lit by it; pull highlights in the grade | 1 | light |
| `visible-rig` | a flying or hanging figure looks held by a cable: stiff hips, clothes bunched at a harness point | pose of a suspended body | name a free pose (arms loose, clothes flowing); new seed | 1 | camera |
| `locked-drift` | a state the scene locked changes (the glass refills, the door swings shut) | the locked state not restated | paste the scene's `locked` list into start_state and the prompt | 1 | locked |
| `extra-person` | someone uncast appears, a person vanishes mid-take, or one person doubles | the card names who is there but not that no one else is | cast every visible person and add "no one else in frame"; new seed | 1 | count |
| `beat-order` | the beats happen out of order, merge, or one never happens | two or more beats in one untimed action | one beat per card, or timed beats (cards beats) | 1 | order |

## Rules

- Log and climb as in failures-picture. Shadow and scale checks need the plate and the insert side by side on one contact sheet.
