---
title: Continuity rules specific to AI video
slug: ai-continuity
summary: What separately generated clips lose between shots (identity, props, sound, direction) and the planning rules that carry it across.
tags: [continuity, ai-video, seams, identity, seeds]
last_checked: 2026-11-09
sources: ["https://cloud.google.com/blog/products/ai-machine-learning/ultimate-prompting-guide-for-veo-3-1", "Maintainer's local-render field notes, 2026-09 (private; lessons 005, 011, 012, 013)", "Joseph V. Mascelli, The Five C's of Cinematography, 1965", "David Bordwell, Janet Staiger and Kristin Thompson, The Classical Hollywood Cinema, 1985", "David Bordwell, A Labyrinth of Linkages, 2013", "David Bordwell, Narration in the Fiction Film, 1985"]
---

# Continuity rules specific to AI video

## Rules

- Each generation starts its picture and sound from nothing. Two clips cut together read as the scene restarting unless something carries across: the same identity strings, refs, light phrase, and one continuous sound named on both sides of the cut.
- Prefer one generation holding several shots (timestamp blocks) over separate clips, when the model supports it. Put separate generations only at real changes of place or camera side.
- A clip continued from the previous clip's last frame keeps composition but loses who people are and the shape of props. Restate identity strings and prop constants in every continuation.
- At a continuation seam, the next clip starts "already moving, no pause"; trim the first few frames where the model eases in.
- Every prompt states direction with the fixed screen-direction phrases. The model has no map of the scene.
- Describe what is there. Exclusion lines lose against strong associations; write absences inside the positive description.
- Anything may change during a shot, nothing between shots. Where someone moved in a card, record where they ended (`position_end`); the next card matches that end state, not the scene's opening block, and the diff checks it (after Mascelli, *The Five C's*).
- Setup motifs: a recurring situation reuses its setup (same camera words, same start image) and varies one or two named parameters (size, look direction, position, costume) so the change reads (*Labyrinth* pp. 21-27). A payoff prop is visible in an earlier card of the same setup (*Classical Hollywood* p. 59).
- A role can own a screen side for the whole film (performer right, onlooker left); every card with that role keeps the side (*Labyrinth* p. 24).
- Cheat cut: small position drift passes when the cut changes both size and angle and the axis holds (*Classical Hollywood* p. 59). Weight errors: face, speaker and left-right order high; hand and prop offsets low (*Narration* p. 165). Never downgrade identity or wardrobe.
- Contradiction matters, omission does not. A close card fails only when its background contradicts the establishing frame (a window where the wide showed a wall), not because it leaves things out (*Classical Hollywood* p. 60).

## Numbers

- Trim about 9 frames (at 24 fps, under 0.4 s) from the head of each continued clip; the model eases in over that span.
- Overlap the sound at a remaining seam by a fraction of a second (0.1-0.2 s) so it does not cut dead.
- Violation budget, warn only: classical studio films broke spatial continuity on under 2% of cuts (*Classical Hollywood* p. 58). Over 1 AXIS or EYELINE error in 50 cuts reads as deliberately disorienting.

## Pitfalls

- Fixing a continuation by rerolling only the later clip while the earlier one's end state was wrong: fix the end state first.

## Notes

- 2026-10-03: numbers from one local model's renders; unverified on hosted models. Re-check on the first hosted render (needs the maintainer's go).
