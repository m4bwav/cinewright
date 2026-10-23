# Changelog: cinewright-finish

Every change to [SKILL.md](SKILL.md) and its companions, newest first, each with the reason. Reasons cite findings in [RESEARCH.md](RESEARCH.md) (`R-`), lessons in [LEARNINGS.md](LEARNINGS.md) (`L-`), and test runs in [TESTS.md](TESTS.md) (`T-`). State in `evergreen.json`. Protocol: [MAINTENANCE.md](MAINTENANCE.md).

Entry shape: `### C-20261022-1 · 2026-10-22 · grade stabilize, saturation and warmth targets, repair order (books track 3)
- because: books track 3 (Block, *The Visual Story*; Brown, *Cinematography*; *FilmCraft: Cinematography*; Phillips on Resolve), decision 2026-10-22-books-track3; L-004, L-005
- files: SKILL.md (Step 3), references/shot-matching.md, references/grade-order.md, evals/evals.json (action-2); shared/lib/cine_post.py (`grade stabilize`, `grade match --sat --warm`, `grade measure --plan`)
- Drift inside a shot is held to its middle frame before the match; a scene's colour-script chroma and warmth survive the match; colour management is set first and repairs go whole-image, local, single frame.

### C-YYYYMMDD-n · date · one-line summary`, then `because:`, `files:`, and a sentence on what changed.

### C-20261013-1 · 2026-10-13 · crowd-multiplication: alpha plates, tracked masks, whole-frame unify
- because: user request (battle and crowd scenes from separate generations, Blender offloading), R-20261013-1
- files: references/crowd-multiplication.md, SKILL.md step 2
- Adds the empty first-frame plate, Wan-Alpha, SAM 3.1 Multiplex and MatAnyone 2 for cut-outs, hero layer first, and relighting the merged frame.

### C-20261009-1 · 2026-10-09 · Shot matching with cine_post.py grade
- because: user request (2026-10-09: research what AI film makers build to raise quality, and add the gaps: prop sheets, LoRAs, animatic, blockout control, identity scoring, one shared grade)
- files: SKILL.md (CINE_POST line, Step 3), references/shot-matching.md (new), needs.json (cine_post.py)
- Per-shot match to a hero frame as a .cube (stdlib Reinhard fit, pooled over the shot so it cannot flicker), luma targets per scene, then one look LUT and grain.

### C-20261004-2 · 2026-10-04 · Description tuned (S6)
- because: T-20261004-2, L-003
- files: SKILL.md
- Description tuned for triggering: the Use clause ends "not restoring home video"

### C-20261004-1 · 2026-10-04 · Created as an evergreen unit (cinewright S5)
- because: user request, R-20261004-1, L-001, L-002
- files: SKILL.md, references/, needs.json, RESEARCH.md, LEARNINGS.md, TESTS.md, evals/evals.json, evergreen.json, MAINTENANCE.md
- Initial version. Tier `moderate`, interval 30d. Lessons L-001 and L-002 recorded at creation from the S5 exit check. First test run is logged in TESTS.md.
