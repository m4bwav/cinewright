---
title: Continuity rules specific to AI video
slug: ai-continuity
summary: What separately generated clips lose between shots (identity, props, sound, direction) and the planning rules that carry it across.
tags: [continuity, ai-video, seams, identity, seeds]
last_checked: 2026-10-03
sources: ["https://cloud.google.com/blog/products/ai-machine-learning/ultimate-prompting-guide-for-veo-3-1", "Maintainer's local-render field notes, 2026-09 (private; lessons 005, 011, 012, 013)"]
---

# Continuity rules specific to AI video

## Rules

- Each generation starts its picture and sound from nothing. Two clips cut together read as the scene restarting unless something carries across: the same identity strings, refs, light phrase, and one continuous sound named on both sides of the cut.
- Prefer one generation holding several shots (timestamp blocks) over separate clips, when the model supports it. Put separate generations only at real changes of place or camera side.
- A clip continued from the previous clip's last frame keeps composition but loses who people are and the shape of props. Restate identity strings and prop constants in every continuation.
- At a continuation seam, the next clip starts "already moving, no pause"; trim the first few frames where the model eases in.
- Every prompt states direction with the fixed screen-direction phrases. The model has no map of the scene.
- Describe what is there. Exclusion lines lose against strong associations; write absences inside the positive description.

## Numbers

- Trim about 9 frames (at 24 fps, under 0.4 s) from the head of each continued clip; the model eases in over that span.
- Overlap the sound at a remaining seam by a fraction of a second (0.1-0.2 s) so it does not cut dead.

## Pitfalls

- Fixing a continuation by rerolling only the later clip while the earlier one's end state was wrong: fix the end state first.

## Notes

- 2026-10-03: numbers from one local model's renders; unverified on hosted models. Re-check on the first hosted render (needs the maintainer's go).
