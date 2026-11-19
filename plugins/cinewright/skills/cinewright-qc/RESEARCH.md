# Research: cinewright-qc

Findings that back [SKILL.md](SKILL.md). What it needs installed (ffmpeg): [SETUP.md](SETUP.md). Changes they caused are logged in [CHANGELOG.md](CHANGELOG.md); procedural lessons live in [LEARNINGS.md](LEARNINGS.md); test runs and their evidence in [TESTS.md](TESTS.md); schedule and state in `evergreen.json`. Protocol: [MAINTENANCE.md](MAINTENANCE.md).

Topic: Quality control of AI-generated video takes against shot cards. Tier `moderate`. Last refresh 2026-10-03; next due 2026-11-02.

## Current understanding

- Settled (practice): a take is judged against what the card and bibles asked for, item by item, like a script supervisor's notes; the repair cost ladder orders fixes cheapest first (router entry `pipeline`).
- Settled (tooling): ffmpeg's `tile` filter gives a contact sheet in one call; `ebur128=peak=true` reports integrated loudness, range and true peak; `-sseof` grabs the last frame. All three are in every full ffmpeg build.
- Moving (testing): automatic video scorers (VBench-2.0, VideoScore2 and successors) rate model quality over many clips; none checks one take against a shot card, so the rubric stays agent- or human-judged.
- Moving (2026-10-15): a local vision model is a usable second opinion per rubric item when it never sees the card text and describes first; a yes given in both claim orders was right 228 of 231 times on 368 labelled claims, a no in both only 54 of 95 (R-20261015-1, entry vision-judge).
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

### R-20261119-1 · 2026-11-19 · seam metric and framing check at chained joins (sc40 S28, S30, S39, S27, S12)
- Summary: stdlib seam score (luma spike over the local median, CIE76 colour step of 6 frames each side, settle dE at 0.5/1/2 s, segment drift) separates chained joins (spike 1.4-2.1x, step 0.4-1.6 dE) from scene cuts (spike 25-53x, step about 20 dE). Spike and step miss a push-in that speeds up at the join; a block-matching zoom estimate (192x108, median distance ratio) catches it: A's last frame to B at +1 s 1.063 against 1.005 over the second before (warn), still ending 1.000, a --continue-from join 0.978, steady pull-out chains 0.93 at a 1.1x rate (pass). Global colour transfer (MKL, Reinhard) removes a step (8.6 to 0.12 dE on a synthetic join) but real H3 joins sit under 2 dE already, and a ramp brings the offset back as creep: match only at 3 dE or more, constant. Rank competing takes of a continuation by the join before the rubric (S39, an unreleased pipeline, idea only).
- Track: tooling
- Sources: maintainer chain-join study 2026-11-19 (own code, stdlib + ffmpeg; ORB similarity fits with opencv as the reference); Reinhard et al. 2001; Pitie and Kokaram 2007; https://www.reddit.com/r/StableDiffusion/comments/1sdn1ga/ (S39)
- Magnitude: 0.3
- Applied: C-20261119-1

### R-20261119-2 · 2026-11-19 · background drift by DINOv2 embeddings (sc40 S29), noted
- Summary: masked background crops compared with the scene plate by DINOv2 embeddings (facebookresearch/dinov2, Apache-2.0 code and weights) would measure set drift that colour and thumbnail checks miss. Not installed or run. Worth it only once a film has scene plates and a person mask in its pipeline; cine_seam's struct and zoom checks cover the cheap part. Face embedders such as ArcFace have non-commercial weights.
- Track: tooling
- Sources: https://github.com/facebookresearch/dinov2
- Magnitude: 0.05
- Applied: none (note)

### R-20261117-1 · 2026-11-17 · hold take state (The Godfather Journal)
- Summary: Take log verdict `hold` for a non-keeper with a usable part; qc-loop rule. Book rule, unverified.
- Track: subject
- Sources: Ira Zuckerman, The Godfather Journal, 1972 (paraphrased; no text copied)
- Magnitude: 0.1
- Applied: C-20261117-1

### R-20261114-1 · 2026-11-14 · readable-device failure code (Sculpting in Time)
- Summary: New code for obvious peak slow motion, theme props and uncaused look-backs; fix by softening or an in-world cause. Book rule, unverified.
- Track: subject
- Sources: Andrey Tarkovsky, Sculpting in Time, 1986, ch. I and V (paraphrased; no text copied)
- Magnitude: 0.1
- Applied: C-20261114-1

### R-20261113-1 · 2026-11-13 · Failure codes shadow-mismatch, toy-scale, clipped-fire, visible-rig (Filming the Fantastic)
- Summary: Four codes with cheapest fixes routed to finish and camera. Book rule, unverified; no script check.
- Track: subject
- Sources: Filming the Fantastic: A Guide to Visual Effects Cinematography (Mark Sawicki, 2nd ed.) (paraphrased; no text copied)
- Magnitude: 0.1
- Applied: C-20261113-1

### R-20261015-1 · 2026-10-15 · How people and machines critique AI video, images, voices and sound
- Summary: five tracks (human review practice, vision judges, audio and voice judges, agentic critic loops, practitioner forums) and a field test of a vision judge on 624 labelled claims; full note ai-docs/research/2026-10-15-critic-research.md.
- Track: practice, testing, tooling
- Sources: https://arxiv.org/abs/2511.18102, https://arxiv.org/abs/2510.15831, https://arxiv.org/abs/2608.15574, https://arxiv.org/abs/2506.19441, https://arxiv.org/abs/2507.12705, https://www.movielabs.com/md/qcvocabulary/, https://www.reddit.com/r/comfyui/comments/1vknr0v/
- Magnitude: major (new judge, calibration and selection rules; two commands)
- Applied: C-20261015-1

### R-20261003-1 · 2026-10-03 · Initial research
- Summary: ffmpeg filters chosen from the ffmpeg docs (tooling); the rubric is built from the shot card's fields and the failure codes (practice: script supervision, the maintainer's field lessons); benchmark scorers checked and set aside for per-take review (testing: VBench-2.0, arXiv 2503.21755).
- Track: tooling
- Sources: https://ffmpeg.org/ffmpeg-filters.html#ebur128-1, https://ffmpeg.org/ffmpeg-filters.html#tile-1, https://arxiv.org/abs/2503.21755
- Magnitude: n/a (initial)
- Applied: C-20261003-1
