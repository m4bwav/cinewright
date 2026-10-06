---
title: Loudness targets
slug: loudness-targets
summary: Delivery loudness targets checked 2026-10-04 (EBU R128 v4 and s2, ATSC A/85:2026, Netflix, Spotify) with tolerance, true peak, how each is measured, and the matching qc loud preset.
tags: [vocab, sound, loudness, delivery, lufs, true-peak]
last_checked: 2026-10-04
sources: ["https://tech.ebu.ch/docs/r/r128v4_0.pdf", "https://tech.ebu.ch/docs/r/r128s2.pdf", "https://tech.ebu.ch/docs/tech/tech3344.pdf", "https://www.atsc.org/wp-content/uploads/2026/07/A85-2026-07.pdf", "https://studiopartner.netflix.net/studio/branded-sound-mix-spec-and-best-practices", "https://support.spotify.com/us/artists/article/loudness-normalization/", "https://www.itu.int/rec/R-REC-BS.1770"]
---
<!-- copied from shared/vocab/loudness-targets.md sha256:c46399f5ba9864e021687d39469700e3baa9dd507bbd6382940dc32bbbf258de; edit the source -->

# Loudness targets

## Vocabulary

| Delivery | Integrated | Tolerance | Max true peak | Measured | `qc loud --preset` |
|---|---|---|---|---|---|
| web video (default) | -20 to -16 LUFS | the range | -2 dBTP before a lossy encoder (Tech 3344) | whole programme | `web` (-18 ± 2) |
| EBU broadcast (R128 v4, Aug 2020) | -23.0 LUFS | on target; ±1.0 LU only where not practical (live) | -1 dBTP | whole programme, BS.1770 gating | `ebu-r128` (± 0.2, meter tolerance) |
| US broadcast (ATSC A/85:2026-07) | -24 LKFS | about ±2 dB | below -2 dBTP | dialogue (the anchor element) | `atsc-a85` (approximate) |
| Netflix | -27 LKFS | ±2 LU | -2 dBTP | dialogue-gated, BS.1770-1, full programme | `netflix` (approximate) |
| music streaming (Spotify) | -14 LUFS (normalisation level) | | -1 dBTP; -2 when louder than -14 | whole track | `music-streaming` |

- LUFS and LKFS are the same unit (BS.1770); LU is a difference in loudness. Current BS.1770 is revision 5 (11/2023).
- EBU R128 s2 (Nov 2023) prefers streaming at -23 unchanged and gives -20 to -16 LUFS as an interim distribution range; ATSC A/85:2026 recommends -23 to -27 LKFS for streaming.

## Rules

- State one target before mixing and quote the `qc loud` result against it. No target given: web.
- `qc loud` measures the whole programme with ffmpeg's ebur128 meter. Dialogue-gated specs (ATSC, Netflix) need a dialogue-gated meter for sign-off; the preset is a first check.

## Notes

- 2026-10-04: checked from the primary pages above. Unverified: a YouTube -14 LUFS figure (not in YouTube Help), Apple Music -16, AES TD1008 (page refused access). The Netflix help-centre links now redirect to studiopartner.netflix.net.
