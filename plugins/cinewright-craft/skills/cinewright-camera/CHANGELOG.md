# Changelog: cinewright-camera

Every change to [SKILL.md](SKILL.md) and its companions, newest first, each with the reason. Reasons cite findings in [RESEARCH.md](RESEARCH.md) (`R-`), lessons in [LEARNINGS.md](LEARNINGS.md) (`L-`), and test runs in [TESTS.md](TESTS.md) (`T-`). State in `evergreen.json`. Protocol: [MAINTENANCE.md](MAINTENANCE.md).

Entry shape: `### C-20261022-1 · 2026-10-22 · Upstage key, back-cross, light sources, atmosphere (books track 3)
- because: books track 3 (Block, *The Visual Story*; Brown, *Cinematography*; *FilmCraft: Cinematography*; Phillips on Resolve), decision 2026-10-22-books-track3; L-005
- files: SKILL.md (Step 3), references/lighting-setups.md, references/light-sources.md (new), evals/evals.json (outcome-2), evals/check_lamp.py; shared schema shot card (`light.tone`, `light.atmosphere`); shared/lib/cine.py (KEY-SIDE warning, far-side, backlit and firelight words)
- The key comes from the side the face turns to and the diff warns on a broad key; practicals are carried onto the face; airborne matter is a field compiled as backlit.

### C-YYYYMMDD-n · date · one-line summary`, then `because:`, `files:`, and a sentence on what changed.

### C-20261016-2 · 2026-10-16 · Lesson: an overhead on a fighter pinned under another sees only the top one's back; shoot the pinned face from the floor in profile
- because: L-004
- files: LEARNINGS.md (Active: L-004)
- From the cards for a duel's last phrases.

### C-20261016-1 · 2026-10-16 · Lesson: lay a lying figure across an overhead frame
- because: L-003
- files: LEARNINGS.md (Active: L-003)
- From a duel's overhead close-up: point an overhead's frame top square to a lying body and keep the pair's screen order, instead of along the body, which turns the face upside down.

### C-20261005-1 · 2026-10-05 · "lighting a shot", not "a scene" (S6)
- because: T-20261004-2, L-002
- files: SKILL.md
- After C-20261004-2, "lighting a scene" drew the three.js lights decoy (decoy-3, Sonnet 1 of 3); "a shot" keeps the film sense

### C-20261004-2 · 2026-10-04 · Description tuned (S6)
- because: T-20261004-2, L-002
- files: SKILL.md
- Description tuned for triggering: the Use clause says "when lighting a scene" and ends "period looks: cinewright-history"

### C-20261004-1 · 2026-10-04 · Created as an evergreen unit (cinewright S4)
- because: user request, R-20261004-1, L-001
- files: SKILL.md, references/, needs.json, shared/vocab (aspect-ratios, lens-terms, lighting-terms), RESEARCH.md, LEARNINGS.md, TESTS.md, evals/evals.json, evergreen.json, MAINTENANCE.md
- Initial version. Tier `slow`, interval 120d. Lesson L-001 recorded at creation. First test run is logged in TESTS.md.
