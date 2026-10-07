---
title: Failure codes, motion, sound and spec
slug: failures-motion
summary: Failure codes for rendered takes (action, opening, end state, anatomy, physics, text, dialogue, sound, seams, spec, loudness): symptom, cause, cheapest fix, rung, check.
tags: [vocab, qc, failures, taxonomy, motion, audio]
last_checked: 2026-10-07
sources: ["field lessons 005, 011, 014, 015, 020, 021 (maintainer's local renders, 2026-09)", "https://tech.ebu.ch/publications/r128"]
---
<!-- copied from shared/vocab/failures-motion.md sha256:666e9e27b59929feeb66c9acebe6df805ae93c4d83adee27575f2a4620f0f1ff; edit the source -->

# Failure codes, motion, sound and spec

## Vocabulary

Rungs and checks as in `failures-picture`.

| Code | Symptom | Cause | Cheapest fix | Rung | Check |
|---|---|---|---|---|---|
| `action-incomplete` | action stops short or plays in slow motion | too much action for the length | one action; longer, or split the card | 2 | action |
| `frozen-start` | picture holds still for the first frames | image-to-video eases in | write "already moving"; trim the head | 7 | action |
| `bad-opening` | wrong opening, the same on every reroll | the seed fixes the opening | new seed; then a guide still at frame 0 | 2 | opening |
| `end-state-wrong` | last frame differs from the card | model ran its own course | next card starts from the observed end | 6 | end-state |
| `anatomy` | hands, limbs or faces melt or multiply | small, fast or hidden subject | larger, slower, side-on; cut around it | 6 | anatomy |
| `physics-morph` | objects merge, pass through or slide | contact and weight unstated | name contact and weight; fewer subjects | 1 | physics |
| `text-artifact` | subtitles, captions, watermark, garbled signs | quoted dialogue; signs in scene | the card's dialogue syntax; negative terms | 1 | text |
| `dialogue-wrong` | line missing, wrong mouth, lips off | two speakers, or speaker not in shot | one speaker per shot, in the cast; else the mix | 1 | audio |
| `name-misread` | a name said wrong | spelling guessed | `pronounce` respelling | 1 | audio |
| `sound-wrong` | silence, music, or the wrong sound | sound left to the model | name ambience and effects | 1 | audio |
| `seam-restart` | a cut between renders reads as a restart | separate renders of one scene | `compile --sequence`; one sound across | 6 | seam |
| `spec-mismatch` | fps, size, aspect or length off | settings not from the params file | render with the params file; conform | 2 | spec |
| `loudness-off` | loudness or true peak off target | mix not normalised | normalise in the mix | 7 | loudness |

## Rules

- `spec-mismatch` and `loudness-off` are measured (`qc spec`, `qc loud`), never judged by eye.
- A take failing only on rung-7 codes is kept: verdict `keep-fix-in-edit`.
