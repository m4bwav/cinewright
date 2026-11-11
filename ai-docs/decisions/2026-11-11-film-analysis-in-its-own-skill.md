# Film analysis lives in its own skill and script (2026-11-11)

- Context: the video analysis track needs commands to take existing video apart. shared/lib is at 193 of 200 KB and is copied into 16 skills.
- Decision: new skill cinewright-analyze (core plugin) owning `scripts/cine_analyze.py` directly, not through shared/lib; it imports the skill's copy of cine.py for validation. Notation lengths are in character heights (H), never engine units.
- Why: keeps the runtime budget, and only this skill needs the commands. H lets each engine convert with its own character height, which is the unit the failed level never had.
- Revisit: if another skill needs `scale` or `shots`, move the module to shared/lib after a trim.
