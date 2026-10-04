---
title: Thirty-degree rule and size steps
slug: thirty-degree-rule
summary: When a cut between two shots of the same subject reads as a jump cut, the numbers the diff checks, and how to fix one.
tags: [continuity, 30-degree-rule, jump-cut, coverage]
last_checked: 2026-10-03
sources: ["Daniel Arijon, Grammar of the Film Language, 1976", "https://en.wikipedia.org/wiki/30-degree_rule"]
---
<!-- copied from shared/vocab/thirty-degree-rule.md sha256:e10b456f47cfac3787c09b40f4654ffc1a2fa6846344f8875bbcc10ae4372a9a; edit the source -->

# Thirty-degree rule and size steps

## Rules

- Two consecutive shots of the same subject in one scene must differ by at least 30 degrees of camera azimuth, or by at least two shot sizes. Otherwise the cut reads as a jump: the picture twitches instead of changing view.
- Record `camera.azimuth_deg` on every card (0-180 on side A, 90 square to the axis) so the diff can check it.
- Fix a jump in planning: move the second camera 30+ degrees, change size by two steps (`MS` to `CU`), or put a different subject between (a reaction, an insert).
- A deliberate jump cut is a style; write it in the style bible and in the card's `notes`.

## Numbers

- 30 degrees azimuth, or 2 size steps (sizes ordered EWS, WS, FS, MWS, MS, MCU, CU, ECU).
- Shot and reverse shot in dialogue: near 45 and 135 degrees, same size, same lens.

## Verify

- `continuity diff` code 30-DEGREE: error when both cards give azimuth and the change is too small; warning when azimuth is missing.
