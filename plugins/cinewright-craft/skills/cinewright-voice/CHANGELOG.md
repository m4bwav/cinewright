# Changelog: cinewright-voice

Every change to [SKILL.md](SKILL.md) and its companions, newest first, each with the reason. Reasons cite findings in [RESEARCH.md](RESEARCH.md) (`R-`), lessons in [LEARNINGS.md](LEARNINGS.md) (`L-`), and test runs in [TESTS.md](TESTS.md) (`T-`). State in `evergreen.json`. Protocol: [MAINTENANCE.md](MAINTENANCE.md).

Entry shape: `### C-YYYYMMDD-n · date · one-line summary`, then `because:`, `files:`, and a sentence on what changed.

### C-20261007-1 · 2026-10-07 · Created as an evergreen unit
- because: user request, R-20261007-1, L-001, L-002, L-003
- files: SKILL.md, references/, needs.json, SETUP.md, RESEARCH.md, LEARNINGS.md, TESTS.md, evals/, evergreen.json, MAINTENANCE.md; shared/lib/cine.py (`voice measure`, `voice ref`, `voice check`), shared/schemas/voice-bible.schema.json
- Initial version. Tier `fast`, interval 14d, verify at use for the engine claims. Ten reference entries; a voice bible (`bibles/voices.json`) checked by `cards validate` and `voice check`.
