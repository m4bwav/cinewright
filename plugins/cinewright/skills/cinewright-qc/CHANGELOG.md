# Changelog: cinewright-qc

Every change to [SKILL.md](SKILL.md) and its companions, newest first, each with the reason. Reasons cite findings in [RESEARCH.md](RESEARCH.md) (`R-`), lessons in [LEARNINGS.md](LEARNINGS.md) (`L-`), and test runs in [TESTS.md](TESTS.md) (`T-`). State in `evergreen.json`. Protocol: [MAINTENANCE.md](MAINTENANCE.md).

Entry shape: `### C-YYYYMMDD-n · date · one-line summary`, then `because:`, `files:`, and a sentence on what changed.

### C-20261004-2 · 2026-10-04 · Loudness presets and the loudness-targets vocab
- because: user request (S5) and the S5 loudness re-check recorded in cinewright-sound RESEARCH.md
- files: SKILL.md, references/qc-loop.md, needs.json, references/loudness-targets.md (copy), shared/lib/cine.py
- `qc loud --preset web|ebu-r128|atsc-a85|netflix|music-streaming`; the default moved from -16 ± 1 LUFS, -1 dBTP to the web preset (-18 ± 2, -2 dBTP) after the S5 re-check found the brief's R128 tolerance wrong and EBU's streaming range in R128 s2.

### C-20261004-1 · 2026-10-04 · Prop rubric item shows the prop's description
- because: first local render: 1A failed prop-drift (a cardboard box for a tin one) with nothing on the rubric to say what tin looks like
- files: scripts/cine.py (copy), scripts/schemas/prop-bible.schema.json (copy), needs.json
- `qc rubric` writes the props check as `holds the <name> (<description>)` when the prop bible describes it.

### C-20261003-2 · 2026-10-03 · Lessons from the first real render
- because: L-001, L-002
- files: SKILL.md (Step 1, Step 3), references/qc-loop.md, shared/lib/cine.py (qc spec takes a generation label)
- Multi-shot generations are measured whole and changed one thing at a time; identity is read on a full frame per shot.

### C-20261003-1 · 2026-10-03 · Created as an evergreen unit (cinewright S2)
- because: user request, R-20261003-1
- files: SKILL.md, references/qc-loop.md, needs.json, SETUP.md, RESEARCH.md, LEARNINGS.md, TESTS.md, evals/evals.json, evergreen.json, MAINTENANCE.md
- Initial version. Tier `moderate`, interval 30d. Commands `qc sheet|spec|loud|rubric` and `takes log|lastframe` in the shared runtime; failure codes shared with cinewright-genvideo.
