---
title: Books track 7, Blender rulings
kind: decision
status: active
date: 2026-10-22
verified: 2026-10-22
stale_after: 2027-04-22
tags: [books, blender, blockout, passes, depth, mist, previs, animation, animatic]
entities: [blender-passes, previs-animation, blockout-control, master-plates, fight-previs, animatic, cinewright-sets]
summary: "Read before changing the Blender passes or previs animation entries, or the sets description's blockout words."
---

# Books track 7 (Blender), cinewright rulings

Source notes: the book-learnings folder, `blender-polywright.md` section 3. The commands and recipes live in polywright; cinewright only says when to use them.

- K1. New entries, not growth: blockout-control (3.2 KB), master-plates (3.9 KB) and fight-previs (3.4 KB) are near the 700-token line, so the Blender pass rules went into a new sets entry `blender-passes` and the animation checks into a new movement entry `previs-animation`. The old entries got one line each.
- K2. Inverse depth stays the depth signal. Mist is described as plain distance with fewer near tones; whether a video model follows it as well is written as untested, not decided.
  Update 2026-10-23: tested once on H3 (crowd push-in, 0.6/0.4, two seeds): the owner picked Mist blind both times (sets L-007). Inverse depth stays what `pw.py crowd` writes; Mist is now a pass worth trying beside it, not a rule.
- K3. Animation principles (after Hess) ship as checks, labelled untested on video models. No runtime check measures them.
- K4. Motion tracking for plates is one line in master-plates, untested headless; `pw.py match` covers stills.
- K5. The sets description names "3D blockouts rendered as control passes (Blender depth, Mist, masks)". Without it the eval never reached the skill (L-008 `description-names-blockout-passes`, first filed as a second L-003). Descriptions total 4,778 of the 5,500 red line.
- K6. No runtime change: shared/lib stays at 185 of 200 KB.
