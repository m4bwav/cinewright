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
