# Research: cinewright-sound

Findings that back [SKILL.md](SKILL.md). Changes they caused are logged in [CHANGELOG.md](CHANGELOG.md); procedural lessons live in [LEARNINGS.md](LEARNINGS.md); test runs and their evidence in [TESTS.md](TESTS.md); schedule and state in `evergreen.json`. Protocol: [MAINTENANCE.md](MAINTENANCE.md).

Topic: Sound design and mixing for AI video: layers and stems, foley, ambience, music spotting, Chion's terms, generated audio, battle sound, mixing to loudness targets (EBU R128, ATSC A/85, Netflix, web). Tier `moderate`. Last refresh 2026-10-04; next due 2026-11-03.

## Current understanding

- Settled (craft): six layers and D/M/E stems (Holman 2010, Sonnenschein 2001), Chion's terms (Audio-Vision 2019), spotting (Karlin and Wright 2004).
- Settled (standards, checked 2026-10-04): EBU R128 v4 (Aug 2020) -23.0 LUFS, -1 dBTP, ±1.0 LU only where the target is not practical; R128 s2 (Nov 2023) -20 to -16 LUFS interim distribution; Tech 3344 -2 dBTP before lossy encoders; ATSC A/85:2026-07 -24 LKFS about ±2 dB, below -2 dBTP, dialogue-anchored; Netflix -27 LKFS ±2 LU dialogue-gated, -2 dBTP; Spotify -14 LUFS; BS.1770-5 (11/2023).
- Settled (runtime, 2026-10-04): `qc loud --preset web|ebu-r128|atsc-a85|netflix|music-streaming`, default web (-18 ± 2, -2 dBTP).
- Unverified: YouTube -14 LUFS (not in YouTube Help), Apple Music -16, AES TD1008 (access refused).

## Open questions

- A dialogue-gated meter in the standard library? ffmpeg's ebur128 has no dialogue gate, so ATSC and Netflix presets stay approximate.
- Do current video models deliver 48 kHz audio? The local model gave 32 kHz AAC.

## Search plan

Four tracks; every refresh runs at least one query on each, scoped to the time since the last refresh.

Subject:

- `EBU R128 revision loudness <year>`
- `ATSC A/85 revision <year>` and `Netflix sound mix specification loudness <year>`

Tooling:

- `path:SKILL.md "loudness"` on GitHub code search; skills.sh weekly installs for `audio mixing`
- `https://registry.modelcontextprotocol.io/v0/servers?search=audio`

Practice:

- `AI video generated audio mix foley <month> <year>`
- `streaming platform loudness normalization LUFS <year>`

Testing:

- `loudness meter BS.1770 test signals compliance <year>`
- `path:SKILL.md audio evals`

Best sources (primary first): EBU R128 and its supplements (tech.ebu.ch); ATSC A/85 (atsc.org); Netflix partner pages (studiopartner.netflix.net, JavaScript only: read in a browser); ITU-R BS.1770; Chion, Audio-Vision; Holman; Sonnenschein. Noisy: forum posts quoting platform LUFS numbers without a source.

## Findings log

Newest first. `Track` is subject, tooling, practice, or testing.

### R-20261004-1 · 2026-10-04 · Initial research
- Summary: Built from the research brief §3 sound row (subject), loudness re-verified from primary pages this session by a research pass (EBU R128 v4 and s2, Tech 3344, ATSC A/85:2026-07, both Netflix pages in a browser, Spotify, ITU BS.1770) with the brief's ±0.5 LU R128 tolerance found wrong and A/85:2013 superseded, the ffmpeg loudnorm documentation (tooling: linear mode needs the four measured values and falls back to dynamic), the S5 exit check (practice: a -27.6 LUFS take mixed to -17.6 LUFS and -6.3 dBTP), and TESTING.md (testing: `qc loud` output is checkable evidence).
- Track: subject
- Sources: https://tech.ebu.ch/docs/r/r128v4_0.pdf, https://tech.ebu.ch/docs/r/r128s2.pdf, https://www.atsc.org/wp-content/uploads/2026/07/A85-2026-07.pdf, https://studiopartner.netflix.net/studio/branded-sound-mix-spec-and-best-practices, https://support.spotify.com/us/artists/article/loudness-normalization/, https://ffmpeg.org/ffmpeg-filters.html
- Magnitude: n/a (initial)
- Applied: C-20261004-1
