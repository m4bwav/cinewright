---
title: Style-bible fields carry camera and history choices into prompts
kind: decision
status: accepted
date: 2026-10-04
verified: 2026-10-04
stale_after: 2027-04-04
tags: [style-bible, compile, continuity, camera, history, schema]
summary: "Read before adding a look, lens or lighting feature: S4 put lighting, frame_aspect, allowed_moves and history in the style bible, compiled them under a guard, checked lens_family and moves in the diff, and added --style"
---

# Style-bible fields carry camera and history choices into prompts

## Context

PLAN §10's S4 exit check: "shoot it like 1970s New Hollywood, 2.39" must change the compiled prompts in checkable ways. Two obstacles. The compiler reads only the project, and a skill installed alone cannot reach another plugin's references, so prompts cannot look up history cards. And no model renders 2.39 (compile stops on an aspect the model card does not offer).

## Decision

- **Fields, not lookups.** The style bible gains `lighting` (verbatim string), `frame_aspect` (the composed and delivered frame), `allowed_moves` (camera moves the look permits) and `history` (the card ids, for the record). `lens_family` already existed and is now checked. cinewright-history translates card tags into these fields; cinewright-camera writes them directly.
- **Compile.** The style part becomes look + lighting + a composition sentence when `frame_aspect` differs from the render ("Composed for a 2.39:1 widescreen crop, heads and action inside the middle 74% of the frame height."). It sits in the style part, so every model card's `order` and the sequence header already place it, said once per generation. A guard stops the compile when the lighting string or the sentence is missing, like the identity and prop guards. The render aspect in the params never changes; finishing crops.
- **Diff.** LENS warns when a card's `lens_mm` is outside every NN-NNmm range in `lens_family`; MOVE warns when a card's move is not in `allowed_moves`. Warnings, since a style can be broken on purpose with a note.
- **`--style FILE`** on `cards validate`, `continuity diff` and `compile`, so a look is tried beside the current one before it replaces `bibles/style.json`. The example keeps its S2-rendered prompts and adds `compiled/veo-new-hollywood/`.
- **Validator:** `uniqueItems` support added, for `allowed_moves`.
- **Shared vocab:** aspect-ratios, lens-terms and lighting-terms in `shared/vocab/`, copied into camera and history.

## Reasons

Fields keep a project's compile reproducible whatever is installed, and the guard and diff make the style checkable. Rejected: the compiler reading history cards by id (depends on install, breaks the one-skill ZIP); asking models for letterbox bars (bar height drifts between takes); changing the example's own style bible (would rewrite the prompts S2 rendered); a per-model lighting part (nine model-card edits for no gain, since `style` is in every order).

Related: builds on [2026-10-04-prop-bible-and-pre-production-checks.md](2026-10-04-prop-bible-and-pre-production-checks.md); see also [2026-10-03-shared-sources-copied-into-skills-with-a-hash-header.md](2026-10-03-shared-sources-copied-into-skills-with-a-hash-header.md)
