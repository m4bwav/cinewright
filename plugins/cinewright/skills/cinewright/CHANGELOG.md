# Changelog: cinewright

Every change to [SKILL.md](SKILL.md) and its companions, newest first, each with the reason. Reasons cite findings in [RESEARCH.md](RESEARCH.md) (`R-`), lessons in [LEARNINGS.md](LEARNINGS.md) (`L-`), and test runs in [TESTS.md](TESTS.md) (`T-`). State in `evergreen.json`. Protocol: [MAINTENANCE.md](MAINTENANCE.md).

Entry shape: `### C-YYYYMMDD-n · date · one-line summary`, then `because:`, `files:`, and a sentence on what changed.

### C-20261004-3 · 2026-10-04 · Description tuned (S6)
- because: T-20261004-1, L-001
- files: SKILL.md
- Description tuned for triggering: the Use clause adds "plan an idea as shots"; "scene" left the film list for the budget

### C-20261004-2 · 2026-10-04 · Pipeline names the S5 skills (edit, finish, sound)
- because: user request (S5)
- files: SKILL.md
- The stage table's last row split into QC, Edit, Grade and deliver, Sound and mix, each naming its skill and evidence.

### C-20261004-1 · 2026-10-04 · Pipeline names the S3 skills; project layout adds script, design notes and the prop bible
- because: user request (cinewright S3)
- files: SKILL.md, references/project-layout.md
- The Step 2 table gains Script and Design rows and routes the shot list to cinewright-shots with cinewright-movement for actions; the layout lists `script.md`, `design.md` and the optional `bibles/props.json`.

### C-20261003-1 · 2026-10-03 · Created as an evergreen unit (cinewright S1)
- because: user request, R-20261003-1
- files: SKILL.md, references/, needs.json, RESEARCH.md, LEARNINGS.md, TESTS.md, evals/evals.json, evergreen.json, MAINTENANCE.md
- Initial version. Tier `moderate`, interval 30d. First test run is logged in TESTS.md.
