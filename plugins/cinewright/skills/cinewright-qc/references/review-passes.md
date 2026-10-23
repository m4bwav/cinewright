---
title: Review passes and note format
slug: review-passes
summary: How film and VFX reviewers look at a take, in passes (real time, silent, per element, cut points, sound), and how each note is written as one record with time, region, code and one fix.
tags: [qc, review, notes, dailies, passes, continuity]
last_checked: 2026-10-22
sources: ["SPOTLIGHT error annotation protocol, arXiv 2511.18102, 2025-11", "MovieLabs QC vocabulary (video, audio, production), https://www.movielabs.com/md/qcvocabulary/", "Walter Murch, In the Blink of an Eye, 2nd ed., 2001 (Rule of Six)", "Frame.io comment guide, https://help.frame.io/en/articles/5042472", "SyncSketch compare and ghosting guides, https://support.syncsketch.com/", "Netflix QC modes (spot QC sampling), backlothelp.netflix.com, read through search 2026-10-15"]
---

# Review passes and note format

## Rules

- Watch the whole take once at normal speed before any detail work, and write down the first time something looks wrong. A paused frame cannot show flicker, morphs or a slow-motion feel.
- Then the passes, in order: silent and continuous (write only the action you saw; if it is not the card's action, it is a reroll); silent and stopped at each cut (identity, screen direction, positions, gaze, scale); per element (identity at start, middle and end; wardrobe; props through every occlusion; text); sound with eyes closed; the exported file in another player.
- Brief faults (anatomy, things popping in or out) last a fraction of a second: step frames around motion peaks. Long faults (prompt adherence, physics) show on the sheet.
- Fresh eyes: mirror the frame to see errors the eye has got used to; put take N beside take N-1 (or their difference image) to see what the one change did.
- Cut points: the last second of shot A beside the first second of shot B; gaze, position, direction of travel and light must carry over.
- One note is one record: time range, screen region, code from the failure vocabulary, severity 1-5 (how easily a viewer spots it), what you saw in eight words or more, and the one fix. Rank notes by what they cost the story; drop the small ones.
- Never ask for what cannot be fixed. A note that only a different model could satisfy is "re-plan the card", not "reroll".
- Look pass, after the per-element pass: light, atmosphere, space, line, moves and attention, one rubric verdict each (entry look-pass).
- When notes conflict, give up the lowest first: emotion, story, rhythm, eye-trace, the screen plane, 3D space (Murch). A strong emotional take hides a small continuity flaw; the reverse never holds.
- Assume a physics-heavy shot has a glitch until checked: people spot one in most of them.
- Secondary props degrade first; identity drifts first in eye shape, lip line and hairline on head turns.
- Per kept take, pick the one frame that sums up the shot, usually near its out point, and lay them all out in cut order on one contact sheet. Reading the board left to right catches hairline, collar, prop and light drift between shots that are not adjacent (after Murch).

## Numbers

- SPOTLIGHT: error segments average 2.5 s in 6.5 s clips; humans still find about twice what the best video model localises.
- Physics-critical generated clips with a visible glitch: 83 to 94 % (arXiv 2603.19607).
- Spot sampling when time is short: the head, quarter, half, three quarters and tail, plus one real-time pass.

## Vocabulary

- dailies, notes, spot QC, flash frame, coffee cup (something that does not belong), continuity error, extraneous effect, eye-trace.

## Pitfalls

- Judging from the sheet alone: it misses brief faults and every timing fault.
- Five notes and five changes on the next take: one change, the cheapest (entry qc-loop).

## Verify

- Every fail in a rubric has a time, a code and a fix; no note says only "feels off".

Related: builds on [qc-loop](qc-loop.md); see also [look-pass](look-pass.md), [vision-judge](vision-judge.md), [judge-calibration](judge-calibration.md).
