---
title: Books track 2, cutting and continuity rulings
kind: decision
status: active
date: 2026-10-22
verified: 2026-10-22
stale_after: 2027-04-22
tags: [books, continuity, shots, edit, schema, runtime, budget]
entities: [cine.py, shot-card, continuity-diff, cut-points, point-of-view]
summary: "Read before changing the shot card's pov, role, position_end, enters, exits or settle fields, the track 2 diff codes, or the runtime budget: the small calls made in books track 2 and why"
---

# Books track 2, cutting and continuity rulings

## Context

Track 2 of the book-learnings build (Katz, *Shot by Shot*; Mascelli, *The Five C's*; Murch, *In the Blink of an Eye*) adds cutting and continuity rules to cinewright. The notes proposed fields and checks; these are the calls made building them.

## Decision

- F1 Runtime budget: the runtime was at its 150 KB red line before the track. Mark raised red to 200 KB on 2026-10-22 (asked in session; tracks 3 and 4 also add runtime). Yellow stays 101 KB and up. PLAN.md and `scripts/cine.py` BUDGETS carry the new line.
- F2 `role` does not repeat `camera.framing`: framing says what is in the frame (single, ots, insert, pov), role says the card's job in the edit (establishing, master, coverage, reaction, cut-in, cut-away, protection).
- F3 Entrances and exits are per person (`cast[].enters`, `cast[].exits`), like `travel`, not per card. Sides: frame-left, frame-right, near-camera. EXIT-ENTRY compares screen sides with the previous card in cut order, across scenes, because a background change is usually a scene change.
- F4 `cross_reason` stays free text: a token list as a schema enum would break existing cards. The diff warns when the reason does not open with one of the nine tokens.
- F5 `position_end` moves the scene's block: POSITION and EYELINE check each card against the block after the card before. Positions are kept in side A terms, flipped from a side B card.
- F6 LOOK-TRACK uses the scene's `axis.travel` for the watched person and a new `eyeline_end` for the turn, rather than a separate `turns` field.
- F7 A protection card is checked but never becomes the state the next card starts from. Cut order lists it next to the card it protects.
- F8 `camera.settle` is opt-in. Making every move start and end held would change every compiled prompt and fight the "already moving" rule at continuation seams.
- F9 ESTABLISH counts people film-wide and props per scene (continuity L-007 `establish-people-film-wide`).
- F10 Out of scope here, left for track 4 (framing and prompt vocabulary), because they are framing and composition: the STRAIGHT-IN warning (A5), the three-quarter default and diagonal travel (A6), camera height relative to the subject and dutch pairs (A7), `qc cutcheck` for eye trace at the cut (C3), and the `bg-tangent` and `ots-wrong` failure codes (C4, C5), open framing, the lens-choice note for cramped interiors, and mobile staging.

## Consequences

- Old cards validate unchanged; every new field is optional, and the new checks fire only when the fields are set, except ESTABLISH and MIDDLE-SWAP, which read existing fields. On 163 cards of seven local multi-shot films, the new checks raised no warnings after F9.

Related: builds on [2026-10-04-proposed-runtime-budget-row.md](2026-10-04-proposed-runtime-budget-row.md)
