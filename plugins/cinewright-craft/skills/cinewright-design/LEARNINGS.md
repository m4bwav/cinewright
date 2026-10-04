# Learnings: cinewright-design

Procedural lessons for [SKILL.md](SKILL.md). Research findings live in [RESEARCH.md](RESEARCH.md); every change is logged in [CHANGELOG.md](CHANGELOG.md); test runs in [TESTS.md](TESTS.md); state in `evergreen.json`. Format: [MAINTENANCE.md](MAINTENANCE.md) (LEARNINGS-FORMAT in the evergreen protocol). Retired entries go to LEARNINGS-ARCHIVE.md with a reason.

Write an entry the moment a real signal happens: a user correction, the same error twice, a workaround, an environment fact, a failed test. Check existing entries first: add, update, retire or none. Trigger and Hypothesis are required.

## Active

### L-001 · 2026-10-04 · Make each character one turnaround sheet; crop the views into separate references
- Trigger: Field lesson 017 of the maintainer's local renders, 2026-09-29, 'Turnaround sheets hold one identity across views; costume sheets invent symbols'
- Hypothesis: An image model keeps identity inside one image far better than across separate generations, and a whole sheet passed as one reference leaves each view few pixels
- Rule: Generate one three-view sheet per character and costume on flat light and grey, crop each view, and check every sheet for symbols the text did not ask for
- Evidence: C-20261004-1 (references/turnaround-sheets.md), confirmed 2026-10-04
- Scope: skill
- Status: active · helpful 1 · harmful 0 · last_confirmed 2026-10-04

### L-002 · 2026-10-04 · Clean every reference before use; it outranks the prompt
- Trigger: Field lesson 019 of the maintainer's local renders, 2026-09-29, 'A video model copies a reference picture's small emblems onto the character, so clean every reference first'
- Hypothesis: A reference image conditions what it shows more strongly than any text, including exclusion lines
- Rule: Paint out every unwanted mark before the reference goes into a shot, keep the original as `_orig`, and inspect at full size
- Evidence: C-20261004-1 (references/clean-references.md), confirmed 2026-10-04
- Scope: skill
- Status: active · helpful 1 · harmful 0 · last_confirmed 2026-10-04

### L-003 · 2026-10-04 · A prop named by one word changes look between shots; give it a fixed description
- Trigger: 2026-10-03, first local render of the three-shot example: the qc rubric failed 1A on prop-drift (a cardboard box where the story meant a tin matchbox)
- Hypothesis: The model invents a prop's look from its name each generation, as it does identity
- Rule: Describe every held or close-up prop once in bibles/props.json; the compiler pastes it verbatim and the diff warns when one is missing
- Evidence: C-20261004-1 (references/prop-constants.md, shared/lib/cine.py prop_words), confirmed 2026-10-04
- Scope: skill
- Status: active · helpful 1 · harmful 0 · last_confirmed 2026-10-04
