# Learnings: cinewright-history

Procedural lessons for [SKILL.md](SKILL.md). Research findings live in [RESEARCH.md](RESEARCH.md); every change is logged in [CHANGELOG.md](CHANGELOG.md); test runs in [TESTS.md](TESTS.md); state in `evergreen.json`. Format: [MAINTENANCE.md](MAINTENANCE.md) (LEARNINGS-FORMAT in the evergreen protocol). Retired entries go to LEARNINGS-ARCHIVE.md with a reason.

Write an entry the moment a real signal happens: a user correction, the same error twice, a workaround, an environment fact, a failed test. Check existing entries first: add, update, retire or none. Trigger and Hypothesis are required.

## Active

### L-001 · 2026-10-04 · A style reaches the prompt only through style-bible fields, never through card ids or names
- Trigger: 2026-10-04, S4 design of the exit check: compile reads only the project, and a skill installed alone cannot reach another plugin's references
- Hypothesis: If the compiler looked up history cards, a project would compile differently depending on what is installed, and names in prompts drift toward famous frames
- Rule: Translate card tags into look, lighting, lens_family, frame_aspect and allowed_moves; keep card ids in history for the record only
- Evidence: C-20261004-1 (references/applying-styles.md, shared/schemas/style-bible.schema.json), confirmed 2026-10-04
- Scope: skill
- Status: active · helpful 1 · harmful 0 · last_confirmed 2026-10-04

### L-002 · 2026-10-04 · Headless baselines: Glob and Grep can leave the folder; deny them outside it
- Trigger: 2026-10-04, S4 history action baseline: with Bash denied, the run globbed the home folder for SKILL.md; the search timed out, so nothing was found, but the tool was not refused
- Hypothesis: In non-interactive mode reads outside the working folder are refused, but Glob and Grep with an explicit path are not, so a sandbox built on tool denial alone leaks through them
- Rule: For skill-free baselines deny Glob and Grep too (or give them deny rules for the home and repository drives), keep fixtures on another drive from the repository, and scan every trace for paths outside the run folder
- Evidence: T-20261004-1, confirmed 2026-10-04
- Scope: testing
- Status: active · helpful 1 · harmful 0 · last_confirmed 2026-10-04
