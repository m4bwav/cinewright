# Changelog: cinewright-sound

Every change to [SKILL.md](SKILL.md) and its companions, newest first, each with the reason. Reasons cite findings in [RESEARCH.md](RESEARCH.md) (`R-`), lessons in [LEARNINGS.md](LEARNINGS.md) (`L-`), and test runs in [TESTS.md](TESTS.md) (`T-`). State in `evergreen.json`. Protocol: [MAINTENANCE.md](MAINTENANCE.md).

Entry shape: `### C-YYYYMMDD-n · date · one-line summary`, then `because:`, `files:`, and a sentence on what changed.

### C-20261006-1 · 2026-10-06 · Conform effects and foley to a cue's tempo
- because: R-20261006-1
- files: references/conform-to-tempo.md, references/INDEX.md, SKILL.md
- New entry conform-to-tempo (tempo match, then warp, then cut; Rubber Band ratios 0.75-1.35; beats, eighths and triplets; quiet edit points; stereo correlation before mono; active RMS; report unheard until auditioned). SKILL.md Step 2 gains one line pointing to it. Description unchanged (the evals cover triggering).

### C-20261004-2 · 2026-10-04 · Description tuned (S6)
- because: T-20261004-2, L-003
- files: SKILL.md
- Description tuned for triggering: the description says a film's clips and ends the Use clause with "not podcasts or making music"

### C-20261004-1 · 2026-10-04 · Created as an evergreen unit (cinewright S5)
- because: user request, R-20261004-1, L-001, L-002
- files: SKILL.md, references/, needs.json, RESEARCH.md, LEARNINGS.md, TESTS.md, evals/evals.json, evergreen.json, MAINTENANCE.md
- Initial version. Tier `moderate`, interval 30d. Lessons L-001 and L-002 recorded at creation from the S5 exit check. First test run is logged in TESTS.md.
