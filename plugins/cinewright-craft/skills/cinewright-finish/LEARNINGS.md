# Learnings: cinewright-finish

Procedural lessons for [SKILL.md](SKILL.md). Research findings live in [RESEARCH.md](RESEARCH.md); every change is logged in [CHANGELOG.md](CHANGELOG.md); test runs in [TESTS.md](TESTS.md); state in `evergreen.json`. Format: [MAINTENANCE.md](MAINTENANCE.md) (LEARNINGS-FORMAT in the evergreen protocol). Retired entries go to LEARNINGS-ARCHIVE.md with a reason.

Write an entry the moment a real signal happens: a user correction, the same error twice, a workaround, an environment fact, a failed test. Check existing entries first: add, update, retire or none. Trigger and Hypothesis are required.

## Active

### L-005 · 2026-10-22 · `colour-classes-miss-relative-light-faults`: absolute brightness thirds did not find the light faults a reviewer named
- Trigger: books track 3, calibrating `grade measure --plan` on 354 shots of reviewed local takes, 10 of them faulted for light
- Hypothesis: the reviewer's light notes are relative (lighter than the scene before, darker on the approach than in the close shots, golden where dusk was asked), so a fixed class per shot cannot see them
- Rule: the class check is a plan check, labelled uncalibrated; it never stands in for the reviewer's light verdict. Shots of one scene that step in brightness are the match's job (`grade match --luma`)
- Evidence: with dusk and night scenes planned dark, light-faulted takes had 0.19 of their shots off the plan and the rest 0.29; the luma and warmth spread inside a take did not separate them either (faulted median 19.4 luma, others 17.3). The progression ranking did read a sunset-to-night film correctly (luma rho -0.73, warmth -0.62), and a reversed plan came back AGAINST
- Scope: tool (shared/lib/cine_post.py grade measure --plan)
- Status: active · helpful 0 · harmful 0 · last_confirmed 2026-10-22

### L-004 · 2026-10-22 · `stabilize-reads-content-as-drift`: in a tracking shot the picture's own change looks like exposure drift
- Trigger: books track 3, `grade stabilize` on eight real shots: seven drifted 0.3 to 4.3 luma and fell to 0.2 to 1.6; the eighth "drifted" 11.9
- Hypothesis: the gains hold each frame's mean at the middle frame's, and a tracking shot's mean moves because the street in frame changes, not the exposure
- Rule: stabilize static and slow shots only; it warns over 8 luma, and a planned light change (a lamp switched on, a flash) keeps its original
- Evidence: the 11.9 shot was a backward track ahead of a running crowd down a street; the gains ran 0.98 to 1.17 on it
- Scope: tool (shared/lib/cine_post.py grade stabilize)
- Status: active · helpful 0 · harmful 0 · last_confirmed 2026-10-22

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
- Evidence: C-20261004-2 (description); confirmed T-20261005-1: decoy-3 Sonnet 0 of 3 (was 2 of 3)
- Scope: skill
- Status: active · helpful 1 · harmful 0 · last_confirmed 2026-10-05
