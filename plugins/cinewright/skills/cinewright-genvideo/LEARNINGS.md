# Learnings: cinewright-genvideo

Procedural lessons for [SKILL.md](SKILL.md). Research findings live in [RESEARCH.md](RESEARCH.md); every change is logged in [CHANGELOG.md](CHANGELOG.md); test runs in [TESTS.md](TESTS.md); state in `evergreen.json`. Format: [MAINTENANCE.md](MAINTENANCE.md) (LEARNINGS-FORMAT in the evergreen protocol). Retired entries go to LEARNINGS-ARCHIVE.md with a reason.

Write an entry the moment a real signal happens: a user correction, the same error twice, a workaround, an environment fact, a failed test. Check existing entries first: add, update, retire or none. Trigger and Hypothesis are required.

## Active

### L-001 · 2026-10-03 · Keep the verbatim identity guard in the compiler
- Trigger: 2026-10-03, first run of `compile --sequence` on the example: the header described only the first card's cast, and the guard stopped with 'identity of tomas not verbatim in 1C'
- Hypothesis: Multi-card output paths are easy to get wrong silently; the guard turns a silent drift into a stop
- Rule: Never weaken the guard; any new output mode must pass it on the example before it ships
- Evidence: C-20261003-1 (shared/lib/cine.py compile_cards, tests/test_cine.py), confirmed 2026-10-03
- Scope: skill
- Status: active · helpful 1 · harmful 0 · last_confirmed 2026-10-03

### L-002 · 2026-10-03 · Never present a cinewright default as a vendor number
- Trigger: 2026-10-03: the first Veo card carried a 150-word guide; the re-check found Google gives only a 1,024-token cap
- Hypothesis: A plausible number written next to vendor facts reads as a vendor fact
- Rule: Label every cinewright default in a model card as 'its own default, unverified'
- Evidence: C-20261003-1 (references/veo-3-1.md Numbers), confirmed 2026-10-03
- Scope: skill
- Status: active · helpful 1 · harmful 0 · last_confirmed 2026-10-03

### L-003 · 2026-10-03 · Take a model's syntax from the vendor's guide, not from notes or briefs
- Trigger: 2026-10-03 re-verification: three syntax claims in the research brief and local field notes differed from vendor guides (Seedance `@Image1` vs `@Image 1`; H3 bracket moves vs amplitude sentences; H3 Timeline beats vs labelled fields)
- Hypothesis: Second-hand prompt syntax drifts as vendors revise guides; local notes record what worked once, not the documented form
- Rule: Write a card's Compile block from the vendor's own example and test it with a regex that must match that example too
- Evidence: C-20261003-2 (tests/test_cine.py TestModelCards), confirmed 2026-10-03
- Scope: skill
- Status: active · helpful 1 · harmful 0 · last_confirmed 2026-10-03

### L-004 · 2026-10-03 · Shots in one generation must restate where each person stands
- Trigger: 2026-10-03, first local H3 compile of the three-shot example with `--sequence`: card 1A's frame positions and props in hand were missing, because people are described once in the shared header
- Hypothesis: The header carries who people are; where they stand changes per shot and has to travel with the shot
- Rule: Every sequence block includes the staging part (position and prop in hand); a new layout must keep it
- Evidence: C-20261003-2 (shared/lib/cine.py card_parts staging), confirmed 2026-10-03
- Scope: skill
- Status: active · helpful 1 · harmful 0 · last_confirmed 2026-10-03

### L-005 · 2026-10-03 · An eyeline needs a target, not only a frame direction
- Trigger: 2026-10-03, first local H3 render of the three-shot example (one 14 s generation, seed 101): card 1B said 'Maren is looking toward frame right' and she looked almost into the lens; take 2, same seed, with 'looking toward frame right, at Tomas' fixed it
- Hypothesis: A bare direction is weak conditioning next to a close-up's pull toward the lens; a named person or object gives the gaze somewhere to land
- Rule: The compiler writes every eyeline as direction plus the card's looks_at (a character by name, an object as written); cards should always fill looks_at
- Evidence: C-20261003-2 (shared/lib/cine.py card_parts, failures-picture eyeline-wrong row), confirmed 2026-10-03 by a same-seed re-render
- Scope: skill
- Status: active · helpful 1 · harmful 0 · last_confirmed 2026-10-03

