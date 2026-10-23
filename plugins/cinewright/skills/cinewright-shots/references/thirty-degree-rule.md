---
title: Thirty-degree rule and size steps
slug: thirty-degree-rule
summary: When a cut between two shots of the same subject reads as a jump cut, the numbers the diff checks, and how to fix one.
tags: [continuity, 30-degree-rule, jump-cut, coverage]
last_checked: 2026-10-22
sources: ["Daniel Arijon, Grammar of the Film Language, 1976", "Joseph V. Mascelli, The Five C's of Cinematography, 1965", "https://en.wikipedia.org/wiki/30-degree_rule"]
---
<!-- copied from shared/vocab/thirty-degree-rule.md sha256:a915bc874ce9bdec46585fc6984b37c79520b8bc37abd72932c5b2876f20c0a5; edit the source -->

# Thirty-degree rule and size steps

## Rules

- Two consecutive shots of the same subject in one scene must differ by at least 30 degrees of camera azimuth, or by at least two shot sizes. Otherwise the cut reads as a jump: the picture twitches instead of changing view.
- Record `camera.azimuth_deg` on every card (0-180 on side A, 90 square to the axis) so the diff can check it.
- Fix a jump in planning: move the second camera 30+ degrees, change size by two steps (`MS` to `CU`), or put a different subject between (a reaction, an insert).
- A deliberate jump cut is a style; write it in the style bible and in the card's `notes`.
- Prefer both changes at once: a size step and 30 or more degrees. A straight-in cut (same azimuth, tighter size) suits a centred subject who relates to people on both sides. When two people relate across the frame, move in and around to the side of the one who is looking (after Mascelli, *The Five C's*; Murch).

## Numbers

- 30 degrees azimuth, or 2 size steps (sizes ordered EWS, WS, FS, MWS, MS, MCU, CU, ECU).
- Shot and reverse shot in dialogue: near 45 and 135 degrees, same size, same lens.

## Verify

- `continuity diff` code 30-DEGREE: error when both cards give azimuth and the change is too small; warning when azimuth is missing.
- `continuity diff` code STRAIGHT-IN: warning when the cut goes two or more sizes tighter, the azimuth moves under 10 degrees, and someone in the shot stands off centre.
