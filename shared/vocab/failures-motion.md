---
title: Failure codes, motion, sound and spec
slug: failures-motion
summary: Failure codes for rendered takes (action, opening, end state, anatomy, flicker, physics, text, dialogue, lip lag, sound, seams, spec, loudness): symptom, cause, cheapest fix, rung, check.
tags: [vocab, qc, failures, taxonomy, motion, audio]
last_checked: 2026-11-19
sources: ["field lessons 005, 011, 014, 015, 020, 021 (maintainer's local renders, 2026-09)", "https://tech.ebu.ch/publications/r128", "Richard Williams, The Animator's Survival Kit, 2001"]
---

# Failure codes, motion, sound and spec

## Vocabulary

Rungs and checks as in `failures-picture`.

| Code | Symptom | Cause | Cheapest fix | Rung | Check |
|---|---|---|---|---|---|
| `action-incomplete` | action stops short or plays in slow motion | too much action for the length | one action; longer, or split the card | 2 | action |
| `frozen-start` | picture holds still for the first frames | image-to-video eases in | write "already moving"; trim the head | 7 | action |
| `insert-too-fast` | hands or tools flick through an insert or ECU | magnified motion reads sped up | "slowly, deliberately" in the insert, same tempo in the wide | 1 | action |
| `bad-opening` | wrong opening, the same on every reroll | the seed fixes the opening | new seed; then a guide still at frame 0 | 2 | opening |
| `end-state-wrong` | last frame differs from the card | model ran its own course | next card starts from the observed end | 6 | end-state |
| `anatomy` | hands, limbs or faces melt or multiply | small, fast or hidden subject | larger, slower, side-on; cut around it | 6 | anatomy |
| `flicker` | brightness pulses frame to frame inside one shot | the model's exposure wavers between frames | `deflicker` in the grade; re-render when it stays | 7 | light |
| `physics-morph` | objects merge, pass through or slide | contact and weight unstated | name contact and weight; fewer subjects | 1 | physics |
| `air-steps` | a flying figure walks on the air | flight pose unstated | legs together and trailing, body leaning into the flight; steps only for air-walkers | 1 | action |
| `move-no-settle` | still moving on the last frame, so the cut lands mid-move | no held end | `camera.settle` (held frames at both ends); trim to the hold | 2 | camera |
| `pan-strobe` | the background steps or smears across a fast pan or track | crossing faster than a third of the frame a second | "slow pan" or a longer shot; cut the fast part | 1 | camera |
| `text-artifact` | subtitles, captions, watermark, garbled signs | quoted dialogue; signs in scene | the card's dialogue syntax; negative terms | 1 | text |
| `dialogue-wrong` | line missing, wrong mouth, lips off | two speakers, speaker not in shot, or a speaking reference video (H3 copies its lips) | one speaker per shot, in the cast; else the mix | 1 | audio |
| `lip-lag` | the mouth moves before or after its voice | picture and sound drift in the render or mix | slip the sound by a steady measured lag; re-render when it wanders | 7 | audio |
| `bilabial-miss` | lips not closed 2 frames on M, B, P (Williams p. 309) | loose lip sync | re-render; cut away on the word | 6 | audio |
| `impact-sync` | hit sound before contact or 2+ frames after (p. 294) | placed by ear | slip to contact + 1 frame | 7 | audio |
| `name-misread` | a name said wrong | spelling guessed | `pronounce` respelling | 1 | audio |
| `sound-wrong` | silence, music, or the wrong sound | sound left to the model | name ambience and effects | 1 | audio |
| `seam-restart` | a cut between renders reads as a restart | separate renders of one scene | `compile --sequence`; one sound across | 6 | seam |
| `spec-mismatch` | fps, size, aspect or length off | settings not from the params file | render with the params file; conform | 2 | spec |
| `loudness-off` | loudness or true peak off target | mix not normalised | normalise in the mix | 7 | loudness |

## Rules

- `move-no-settle` and `pan-strobe` are judged by eye (cinewright-qc look-pass says why).
- `spec-mismatch` and `loudness-off` are measured (`qc spec`, `qc loud`), never judged by eye.
- `flicker` is measured too (`qc measure`): a shot whose mean brightness jumps off its neighbours' average often, every second. It warns, never fails, until `qc agree` has scored it on reviewed takes.
- `lip-lag`: people notice sound and picture about 45 ms apart, one or two frames at 24 fps (after Enochs, *Video Generation with AI*). Measure the lag before slipping the sound; a lag that changes along the take is a re-render.
- A take failing only on rung-7 codes is kept: verdict `keep-fix-in-edit`.
