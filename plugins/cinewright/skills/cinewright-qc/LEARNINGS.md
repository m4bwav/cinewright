# Learnings: cinewright-qc

Procedural lessons for [SKILL.md](SKILL.md). What it needs installed (ffmpeg): [SETUP.md](SETUP.md). Research findings live in [RESEARCH.md](RESEARCH.md); every change is logged in [CHANGELOG.md](CHANGELOG.md); test runs in [TESTS.md](TESTS.md); state in `evergreen.json`. Format: [MAINTENANCE.md](MAINTENANCE.md) (LEARNINGS-FORMAT in the evergreen protocol). Retired entries go to LEARNINGS-ARCHIVE.md with a reason.

Write an entry the moment a real signal happens: a user correction, the same error twice, a workaround, an environment fact, a failed test. Check existing entries first: add, update, retire or none. Trigger and Hypothesis are required.

## Active

### L-001 · 2026-10-03 · A multi-shot generation is one take: measure it whole, change one thing across its cards
- Trigger: 2026-10-03, first local render (cards 1A, 1B, 1C in one 14 s H3 generation): `qc spec --card 1A` judged the 14.4 s clip against a 6 s card, and the three rubrics each proposed a different next change
- Hypothesis: Rubrics are per card but a reroll re-renders the whole generation, so per-card changes stack into several changes at once
- Rule: Pass the generation label to `qc spec` (`--card 1A+1B+1C`); pick the single cheapest fix across all the generation's rubrics for the next take
- Evidence: C-20261003-2 (shared/lib/cine.py qc spec, SKILL.md Step 1 and Step 3), confirmed 2026-10-03 when take 2 changed only the eyelines and fixed 1B's eyeline and 1C's end state
- Scope: skill
- Status: active · helpful 1 · harmful 0 · last_confirmed 2026-10-03

### L-002 · 2026-10-03 · Small side-specific marks need a full frame, not the sheet
- Trigger: 2026-10-03, review of the first local H3 renders of the three-shot example: Maren's scar sat above her right eyebrow instead of through the left in both takes; take 1 passed identity at contact-sheet size (300 px frames) and only a full 864x480 frame showed it
- Hypothesis: At sheet size a thin mark is a few pixels, and left and right are easy to flip when reading a face
- Rule: For identity, read one full frame per shot (`ffmpeg -ss <t> -frames:v 1`) and check each side-specific mark against the bible as the character's left or right, not the viewer's
- Evidence: C-20261003-2 (references/qc-loop.md Rules), confirmed 2026-10-03
- Scope: skill
- Status: active · helpful 1 · harmful 0 · last_confirmed 2026-10-03

### L-003 · 2026-10-05 · Generate the rubric before a take exists; never write it by hand
- Trigger: 2026-10-05, S6 T-20261004-1: action-1 (write the QC checklist for card 1B before its first take) failed on Opus 2 of 3: it wrote 1B.checklist.md by hand after a compound shell command was refused, with no qc rubric call
- Hypothesis: Step 1 showed `--clip` as if required, so with no take the model judged the command unusable and fell back to writing the list itself
- Rule: Step 1 says `--clip` is left out before the first take and forbids a hand-written checklist
- Evidence: C-20261005-1 (SKILL.md); confirmed T-20261005-1: no run wrote the checklist by hand; Opus's failing run refused to and asked for the shell (a refused command, harness rev 1)
- Scope: skill
- Status: active · helpful 1 · harmful 0 · last_confirmed 2026-10-05
