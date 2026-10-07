# Changelog: cinewright-script

Every change to [SKILL.md](SKILL.md) and its companions, newest first, each with the reason. Reasons cite findings in [RESEARCH.md](RESEARCH.md) (`R-`), lessons in [LEARNINGS.md](LEARNINGS.md) (`L-`), and test runs in [TESTS.md](TESTS.md) (`T-`). State in `evergreen.json`. Protocol: [MAINTENANCE.md](MAINTENANCE.md).

Entry shape: `### C-YYYYMMDD-n · date · one-line summary`, then `because:`, `files:`, and a sentence on what changed.

### C-20261007-1 · 2026-10-07 · Speaker in the shot, pronounce respellings, tone as an adverb
- because: L-003 (owner's review of the library film), the cinewright-genvideo lesson on off-screen speakers
- files: SKILL.md, references/dialogue-for-generated-voices.md, LEARNINGS.md
- Step 2 asks for each speaker in the shot and a `pronounce` respelling for spoken rare names; the reference names the new SPEAKERS, OFFSCREEN, TONE and PRONOUNCE warnings and was tightened to stay in its token budget

### C-20261004-2 · 2026-10-04 · Step 4 runs the diff whenever a line changes (S6)
- because: T-20261004-2, L-002
- files: SKILL.md
- Step 4.2 now runs `continuity diff` whenever a line changes and forbids counting words by hand instead

### C-20261004-1 · 2026-10-04 · Created as an evergreen unit (cinewright S3)
- because: user request, R-20261004-1
- files: SKILL.md, references/, needs.json, RESEARCH.md, LEARNINGS.md, TESTS.md, evals/evals.json, evergreen.json, MAINTENANCE.md
- Initial version. Tier `slow`, interval 120d. First test run is logged in TESTS.md.
