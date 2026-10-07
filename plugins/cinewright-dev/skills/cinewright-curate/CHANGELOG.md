# Changelog: cinewright-curate

Every change to [SKILL.md](SKILL.md) and its companions, newest first, each with the reason. Reasons cite findings in [RESEARCH.md](RESEARCH.md) (`R-`), lessons in [LEARNINGS.md](LEARNINGS.md) (`L-`), and test runs in [TESTS.md](TESTS.md) (`T-`). State in `evergreen.json`. Protocol: MAINTENANCE.md.

Entry shape: `### C-YYYYMMDD-n · date · one-line summary`, then `because:` (IDs or "user request"), `files:` (file and section), and a sentence on what changed. Cite section headings, not line numbers.

### C-20261006-2 · 2026-10-06 · Retire row split: shut down (the default) and deprecated
- because: T-20261006-1, L-001
- files: SKILL.md (Step 2 table)
- The model-shutdown row now shows `kb retire <slug> --reason R` with the default status named in words; `--status deprecated` has its own row for a model still served.

### C-20261006-1 · 2026-10-06 · Created as an evergreen unit
- because: user request
- files: SKILL.md, RESEARCH.md, LEARNINGS.md, evergreen.json (skills: also TESTS.md and evals/evals.json)
- Initial version. Tier `moderate`, interval 30d. See R-20261006-1 for the research basis; the first test run, for a skill, is logged in TESTS.md.
