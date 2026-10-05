# Learnings: cinewright-sound

Procedural lessons for [SKILL.md](SKILL.md). Research findings live in [RESEARCH.md](RESEARCH.md); every change is logged in [CHANGELOG.md](CHANGELOG.md); test runs in [TESTS.md](TESTS.md); state in `evergreen.json`. Format: [MAINTENANCE.md](MAINTENANCE.md) (LEARNINGS-FORMAT in the evergreen protocol). Retired entries go to LEARNINGS-ARCHIVE.md with a reason.

Write an entry the moment a real signal happens: a user correction, the same error twice, a workaround, an environment fact, a failed test. Check existing entries first: add, update, retire or none. Trigger and Hypothesis are required.

## Active

### L-001 · 2026-10-04 · Give linear loudnorm headroom: gain and a limiter first
- Trigger: 2026-10-04, S5 exit check: the premix at -27.86 LUFS and -10.33 dBTP needed about +14 dB, and loudnorm reported normalization_type dynamic
- Hypothesis: Linear mode applies one gain; when that gain would push the true peak over the target, ffmpeg falls back to dynamic compression without failing
- Rule: Read normalization_type in the first pass; if the gain plus input true peak exceeds the peak target, apply `volume` and `alimiter` first, measure again, then run the linear pass with the four measured values
- Evidence: C-20261004-1 (references/mix-and-loudness.md; result -17.6 LUFS, -6.3 dBTP, `qc loud --preset web` PASS), confirmed 2026-10-04
- Scope: skill
- Status: active · helpful 1 · harmful 0 · last_confirmed 2026-10-04

### L-002 · 2026-10-04 · Netflix spec pages need a browser
- Trigger: 2026-10-04, S5 research: the Netflix help-centre loudness links redirect to studiopartner.netflix.net, which renders only with JavaScript; a plain fetch returned nothing
- Hypothesis: The partner site is a single-page app
- Rule: Read Netflix spec pages in a browser (or a browser tool) and quote the line with its URL; do not cite the old help-centre article numbers as read
- Evidence: C-20261004-1 (shared vocab loudness-targets Notes; both pages read in Chrome), confirmed 2026-10-04
- Scope: skill
- Status: active · helpful 1 · harmful 0 · last_confirmed 2026-10-04

### L-003 · 2026-10-04 · Exclude podcasts and music in the description
- Trigger: 2026-10-04, S6 matrix T-20261004-2: decoy-3 (normalise a podcast to -16 LUFS) invoked the skill Haiku 3 of 3 and Sonnet 3 of 3; decoy-1 (a lo-fi track) Haiku 1 of 3
- Hypothesis: "mixing to a loudness target" matches any loudness request, and the description named no exclusion
- Rule: The description says a film's clips and ends the Use clause with "not podcasts or making music"
- Evidence: C-20261004-2 (description); rerun pending
- Scope: skill
- Status: active · helpful 0 · harmful 0 · last_confirmed 2026-10-04
