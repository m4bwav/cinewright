# Changelog: cinewright-design

Every change to [SKILL.md](SKILL.md) and its companions, newest first, each with the reason. Reasons cite findings in [RESEARCH.md](RESEARCH.md) (`R-`), lessons in [LEARNINGS.md](LEARNINGS.md) (`L-`), and test runs in [TESTS.md](TESTS.md) (`T-`). State in `evergreen.json`. Protocol: [MAINTENANCE.md](MAINTENANCE.md).

Entry shape: `### C-YYYYMMDD-n · date · one-line summary`, then `because:`, `files:`, and a sentence on what changed.

### C-20261016-1 · 2026-10-16 · Character refs keyed by stage (scene id or a named stage such as a wound)
- because: L-005, owner's go-ahead for the compiler change (2026-10-16)
- files: references/costume-arc.md, references/turnaround-sheets.md, LEARNINGS.md (L-005 resolved); shared/lib/cine.py, shared/schemas/character-bible.schema.json, shared/schemas/shot-card.schema.json, tests/test_cine.py
- `refs` may be keyed like wardrobe and a card's cast entry names its stage with `refs_stage`; the compiler sends one stage per card, continuity checks the stage names and their order.

### C-20261015-3 · 2026-10-15 · L-005 confirmed: the refs swap reaches earlier cards; wound stages need a cast-level stage
- because: L-005 (the first scene-1b card), comfyui-gen L-124
- files: LEARNINGS.md (Active: L-005)
- The swap the rule asks for re-sent the new sheets with every earlier card's compile; the workaround and the wider proposed change (a stage named on the cast entry) are recorded for a later code PR.

### C-20261015-2 · 2026-10-15 · Lessons: refs cannot follow a costume or wound stage; museum photo for a period weapon
- because: L-005, L-006 (owner's question on wound stages, 2026-10-15)
- files: LEARNINGS.md (Active: L-005, L-006)
- Two lessons from a duel's reference sheets; the proposed `refs`-by-stage change is for a later code PR.

### C-20261015-1 · 2026-10-15 · No set LoRA for one film
- because: user request (2026-10-15), research note ai-docs/research/2026-10-15-sets-and-loras.md
- files: references/lora-or-references.md
- A Civitai census found no location LoRAs on video models, the one single-room LoRA report failed on layout; the rule gives the break-even and the measured A/B that would justify one.

### C-20261009-1 · 2026-10-09 · Prop sheets, prop states and featured props; LoRA or references
- because: user request (2026-10-09: research what AI film makers build to raise quality, and add the gaps: prop sheets, LoRAs, animatic, blockout control, identity scoring, one shared grade)
- files: SKILL.md (Step 3, Step 4), references/prop-sheets.md (new), references/lora-or-references.md (new), references/prop-constants.md (Rules)
- Props get a sheet per state, sent as refs by the compiler; cards can feature props nobody holds; a new entry says when a trained LoRA beats reference images and how to test one.

### C-20261004-1 · 2026-10-04 · Created as an evergreen unit (cinewright S3)
- because: user request, R-20261004-1, L-001, L-002, L-003
- files: SKILL.md, references/, needs.json, RESEARCH.md, LEARNINGS.md, TESTS.md, evals/evals.json, evergreen.json, MAINTENANCE.md
- Initial version. Tier `slow`, interval 120d. Lessons L-001 to L-003 recorded at creation. First test run is logged in TESTS.md.
