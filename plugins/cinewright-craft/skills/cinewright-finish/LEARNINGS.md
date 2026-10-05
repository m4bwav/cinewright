# Learnings: cinewright-finish

Procedural lessons for [SKILL.md](SKILL.md). Research findings live in [RESEARCH.md](RESEARCH.md); every change is logged in [CHANGELOG.md](CHANGELOG.md); test runs in [TESTS.md](TESTS.md); state in `evergreen.json`. Format: [MAINTENANCE.md](MAINTENANCE.md) (LEARNINGS-FORMAT in the evergreen protocol). Retired entries go to LEARNINGS-ARCHIVE.md with a reason.

Write an entry the moment a real signal happens: a user correction, the same error twice, a workaround, an environment fact, a failed test. Check existing entries first: add, update, retire or none. Trigger and Hypothesis are required.

## Active

### L-001 · 2026-10-04 · Set delivery color tags inside the picture with setparams
- Trigger: 2026-10-04, S5 exit check: the S2 render is tagged transfer iec61966-2-1 (sRGB); `-color_trc bt709` on the libx264 output left the tag as sRGB in ffmpeg 9.0.1
- Hypothesis: ffmpeg passes the frame's own color properties to the encoder, and they win over the output options
- Rule: Add `setparams=range=tv:colorspace=bt709:color_primaries=bt709:color_trc=bt709` at the end of the filter chain and check with ffprobe
- Evidence: C-20261004-1 (references/color-spaces.md, references/delivery-color.md; final file read bt709 for space, primaries and transfer after the change), confirmed 2026-10-04
- Scope: skill
- Status: active · helpful 1 · harmful 0 · last_confirmed 2026-10-04

### L-002 · 2026-10-04 · Balance with a linear luma map pinned at the shot's measured mid, not eq
- Trigger: 2026-10-04, S5 exit check: eq contrast and brightness computed for a 128 pivot moved the blacks of 1B and 1C to 18.5 and 17.7 instead of 20
- Hypothesis: eq's contrast does not pivot at the shot's own mid-grey, so computed values miss
- Rule: Measure YLOW and YAVG with signalstats, then `lutyuv=y='clip(M+(val-M)*g,0,255)'` with M the shot's YAVG and g chosen so YLOW lands on the master's; re-measure
- Evidence: C-20261004-1 (references/grade-order.md; blacks landed at 20.0, 19.5 and 19.7), confirmed 2026-10-04
- Scope: skill
- Status: active · helpful 1 · harmful 0 · last_confirmed 2026-10-04

### L-003 · 2026-10-04 · Exclude home-video restoration in the description
- Trigger: 2026-10-04, S6 matrix T-20261004-2: decoy-3 (upscale old family VHS tapes to 4K) invoked the skill Sonnet 2 of 3
- Hypothesis: "upscale and interpolation" and "cleanup" match restoration work
- Rule: The Use clause ends "not restoring home video"
- Evidence: C-20261004-2 (description); rerun pending
- Scope: skill
- Status: active · helpful 0 · harmful 0 · last_confirmed 2026-10-04
