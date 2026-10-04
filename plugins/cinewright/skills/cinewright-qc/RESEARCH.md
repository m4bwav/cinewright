# Research: cinewright-qc

Findings that back [SKILL.md](SKILL.md). Changes they caused are logged in [CHANGELOG.md](CHANGELOG.md); procedural lessons live in [LEARNINGS.md](LEARNINGS.md); test runs and their evidence in [TESTS.md](TESTS.md); schedule and state in `evergreen.json`. Protocol: [MAINTENANCE.md](MAINTENANCE.md).

Topic: Quality control of AI-generated video takes against shot cards. Tier `moderate`. Last refresh 2026-10-03; next due 2026-11-02.

## Current understanding

- Settled (practice): a take is judged against what the card and bibles asked for, item by item, like a script supervisor's notes; the repair cost ladder orders fixes cheapest first (router entry `pipeline`).
- Settled (tooling): ffmpeg's `tile` filter gives a contact sheet in one call; `ebur128=peak=true` reports integrated loudness, range and true peak; `-sseof` grabs the last frame. All three are in every full ffmpeg build.
- Moving (testing): automatic video scorers (VBench-2.0, VideoScore2 and successors) rate model quality over many clips; none checks one take against a shot card, so the rubric stays agent- or human-judged.
- One data point (2026-10-03, LEARNINGS L-002): a contact sheet at 300 px caught positions, eyelines and actions, but missed a scar on the wrong side; full frames caught it.

## Open questions

- Should the sheet carry timestamps per frame (drawtext needs a font path, which differs per OS)?
- Delivery loudness targets per platform: re-verified 2026-10-04 (cinewright-sound); copied here as shared vocab `loudness-targets`, one preset each in `qc loud --preset`.

## Search plan

Four tracks; every refresh runs at least one query on each, scoped to the time since the last refresh.

Subject:

- `AI video quality evaluation identity consistency benchmark <year>`
- `VBench-2.0 OR VideoScore successor <month> <year>`

Tooling:

- `ffmpeg ebur128 true peak changelog <year>`; ffmpeg release notes for `tile`, `ebur128`, `-sseof`
- `path:SKILL.md "contact sheet" video` on GitHub, sorted by recently updated

Practice:

- `AI film QC reroll workflow contact sheet <year>`
- `site:reddit.com/r/aivideo review takes consistency checklist`

Testing:

- `VLM video judge agreement with human raters <year>`
- `path:SKILL.md video qc evals`

Best sources (primary first): ffmpeg filter docs, EBU R128 and Tech 3341, benchmark papers on arXiv. Noisy: prompt-pack sellers.

## Findings log

Newest first. `Track` is subject, tooling, practice, or testing.

### R-20261003-1 · 2026-10-03 · Initial research
- Summary: ffmpeg filters chosen from the ffmpeg docs (tooling); the rubric is built from the shot card's fields and the failure codes (practice: script supervision, the maintainer's field lessons); benchmark scorers checked and set aside for per-take review (testing: VBench-2.0, arXiv 2503.21755).
- Track: tooling
- Sources: https://ffmpeg.org/ffmpeg-filters.html#ebur128-1, https://ffmpeg.org/ffmpeg-filters.html#tile-1, https://arxiv.org/abs/2503.21755
- Magnitude: n/a (initial)
- Applied: C-20261003-1
