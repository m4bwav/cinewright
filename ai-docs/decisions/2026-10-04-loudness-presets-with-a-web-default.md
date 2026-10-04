---
title: Loudness presets with a web default
kind: decision
status: accepted
date: 2026-10-04
verified: 2026-10-04
stale_after: 2026-11-04
tags: [loudness, qc, sound, runtime, standards]
summary: "Read before changing qc loud or quoting a loudness number: five presets from sources checked 2026-10-04, default web -18 ± 2 LUFS and -2 dBTP; dialogue-gated specs are approximate on this meter"
---

# Loudness presets with a web default

## Context

`qc loud` took `--target`, `--tolerance` and `--true-peak` with a default of -16 ± 1 LUFS and -1 dBTP, set in S2 from the research brief. S5 re-verified every target from primary pages. The brief's EBU R128 tolerance of ±0.5 LU does not exist in R128 v4 (the target is -23.0, with ±1.0 LU only where it is not practical, as in live programmes); ATSC A/85 was revised in July 2026; EBU's streaming guidance is R128 s2 (Nov 2023), an interim distribution range of -20 to -16 LUFS, and Tech 3344 asks for -2 dBTP before a lossy encoder. YouTube, Apple Music and AES TD1008 figures could not be confirmed.

## Decision

- `qc loud --preset NAME` with five presets in `LOUD_PRESETS` (`shared/lib/cine.py`): `web` (-18 ± 2, -2 dBTP; the R128 s2 range), `ebu-r128` (-23 ± 0.2, the meter tolerance; -1 dBTP), `atsc-a85` (-24 ± 2, -2), `netflix` (-27 ± 2, -2), `music-streaming` (-14 ± 1, -1; Spotify). Explicit flags override a preset.
- The default with no preset is `web`, so the old -16 ± 1 default moves to -18 ± 2 and -2 dBTP. A film with no stated target is web video.
- ATSC and Netflix measure dialogue; ebur128 gates the whole programme, so those presets print that the result is approximate.
- The table lives once, as shared vocab `loudness-targets.md`, copied into cinewright-sound and cinewright-qc.

## Reasons

One default keeps the answer to "what level?" single; presets name the real delivery specs so a user asking for broadcast or Netflix gets the right numbers without looking them up. -18 ± 2 sits exactly on EBU's published distribution range. Rejected: -14 as the web default (a music-platform normalisation level from Spotify, not a video spec, and YouTube's figure is unverified); a dialogue gate (needs speech detection, outside the standard library).

Related: builds on [2026-10-03-failure-codes-live-in-shared-vocab-and-drive-the-rubric.md](2026-10-03-failure-codes-live-in-shared-vocab-and-drive-the-rubric.md); see also [2026-10-03-shared-sources-copied-into-skills-with-a-hash-header.md](2026-10-03-shared-sources-copied-into-skills-with-a-hash-header.md)
