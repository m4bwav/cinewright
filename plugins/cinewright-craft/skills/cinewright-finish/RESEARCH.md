# Research: cinewright-finish

Findings that back [SKILL.md](SKILL.md). Changes they caused are logged in [CHANGELOG.md](CHANGELOG.md); procedural lessons live in [LEARNINGS.md](LEARNINGS.md); test runs and their evidence in [TESTS.md](TESTS.md); schedule and state in `evergreen.json`. Protocol: [MAINTENANCE.md](MAINTENANCE.md).

Topic: Color grading and VFX finishing for AI video: grade order, color spaces and delivery, crop to the film's frame, day for night, crowd multiplication, compositing and cleanup, upscale and interpolation. Tier `moderate`. Last refresh 2026-10-04; next due 2026-11-03.

## Current understanding

- Settled (craft): grade order correct, balance, match, look; ASC CDL; day-for-night method; the compositing match list (Van Hurkman 2014, ASC Manual 2022, VES Handbook 2020, Brinkmann 2008).
- Settled (standards, checked 2026-10-04): BT.1886 gamma 2.4 (2011), BT.2100-3 current (02/2025), ACES 2 released 2025 with ACEScct as the grading encoding, DCI direct-view SDR 48 cd/m² (addendum v1.1, 2023).
- Settled (runtime, 2026-10-04): generated clips are display-referred 8-bit and can carry an sRGB transfer tag; ffmpeg 9 keeps a frame's tag over `-color_trc`, `setparams` replaces it.
- Unverified: the main DCI spec's 14 fL figure and SMPTE ST 2084's contents beyond its title (both paywalled); how well learned interpolators handle generated motion.

## Open questions

- Which upscalers keep identity on generated faces? Test on the first 1080p delivery.
- Does the 2.39 composition sentence keep heads inside the crop (cinewright-camera's open question)? Check on the first render with a frame_aspect.

## Search plan

Four tracks; every refresh runs at least one query on each, scoped to the time since the last refresh.

Subject:

- `color grading order correction balance match look <year>`
- `ACES 2 release notes output transforms <year>`

Tooling:

- `path:SKILL.md "color grading"` on GitHub code search; skills.sh weekly installs for `color grading`
- `https://registry.modelcontextprotocol.io/v0/servers?search=video%20grading`

Practice:

- `AI video upscale interpolation workflow <month> <year>`
- `AI generated video color grade compositing crowd <year>`

Testing:

- `video quality metric upscaling interpolation benchmark <year>`
- `path:SKILL.md ffmpeg color evals`

Best sources (primary first): ACES documentation (acescentral); ITU-R BT.1886 and BT.2100; Van Hurkman, Color Correction Handbook; VES Handbook; Brinkmann; the ffmpeg filter documentation. Noisy: LUT packs sold as looks.

## Findings log

Newest first. `Track` is subject, tooling, practice, or testing.

### R-20261004-1 · 2026-10-04 · Initial research
- Summary: Built from the research brief §3 color, finishing and VFX rows (subject), ACES 2 and ACEScct pages, ITU BT.1886 and BT.2100 pages, the DCI direct-view addendum and the ffmpeg filter documentation (checked this session by a research pass), the S5 exit check on the S2 render (practice: signalstats per shot, balance by linear luma maps, sRGB transfer tag replaced with setparams), and TESTING.md (testing: probe tags, qc spec and a contact sheet are checkable).
- Track: subject
- Sources: https://docs.acescentral.com/background/about-aces-2/, https://www.itu.int/rec/R-REC-BT.1886, https://www.itu.int/rec/R-REC-BT.2100, https://ffmpeg.org/ffmpeg-filters.html
- Magnitude: n/a (initial)
- Applied: C-20261004-1
