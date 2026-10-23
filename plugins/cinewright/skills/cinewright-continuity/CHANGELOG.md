# Changelog: cinewright-continuity

Every change to [SKILL.md](SKILL.md) and its companions, newest first, each with the reason. Reasons cite findings in [RESEARCH.md](RESEARCH.md) (`R-`), lessons in [LEARNINGS.md](LEARNINGS.md) (`L-`), and test runs in [TESTS.md](TESTS.md) (`T-`). State in `evergreen.json`. Protocol: [MAINTENANCE.md](MAINTENANCE.md).

Entry shape: `### C-YYYYMMDD-n · date · one-line summary`, then `because:`, `files:`, and a sentence on what changed.

### C-20261022-3 · 2026-10-22 · STRAIGHT-IN, HORIZON and DUTCH in the diff; camera angle meanings (books track 4)
- because: books track 4 (Mateu-Mestre, *Framed Ink* 1 and 2; Mascelli, *The Five C's*; Katz, *Shot by Shot*; Block, *The Visual Story*; Brown, *Cinematography*; Gurney), decision 2026-10-22-books-track4; L-008
- files: shared/lib/cine.py (continuity_diff), shared/vocab/camera-angles.md, shared/vocab/thirty-degree-rule.md, references/shot-checklist.md (HARD-SUBJECT fix), evals/evals.json (outcome-2), evals/check_cutin.py
- A cut-in straight down the axis on people off centre warns (4 of 163 real cards); a low angle with a high horizon or the reverse warns, and so do two opposing dutch tilts the same way. The angle vocab says what each angle reads as and where its horizon sits.

### C-20261022-2 · 2026-10-22 · SPACE, KEY-SIDE and ATTENTION in the diff (books track 3)
- because: books track 3 (Block, *The Visual Story*; Brown, *Cinematography*; *FilmCraft: Cinematography*; Phillips on Resolve), decision 2026-10-22-books-track3
- files: shared/lib/cine.py `continuity_diff`
- Warnings for a depth move or wide lens in a flat scene, a deep scene of static frames, a broad key on a single face, and an eye jump across the frame at a calm cut. On 163 real cards KEY-SIDE fired 13 times (8 %); the other two read fields no real card has yet.

### C-20261022-1 · 2026-10-22 · Diff checks end positions, exits and entrances, head turns, the middle person, cut-ins and POV (books track 2)
- because: books track 2 (Katz, *Shot by Shot*; Mascelli, *The Five C's*; Murch, *In the Blink of an Eye*), decision 2026-10-22-books-track2
- files: SKILL.md (Step 2 pointer to vehicles), references/vehicles.md (new), references/ai-continuity.md, references/axis-and-screen-direction.md (cross_reason tokens), references/eyelines.md, references/shot-checklist.md, shared/lib/cine.py (continuity_diff), tests/test_cine.py, evals action-2
- The diff checks each card against the block as it stands after the card before (moved by `position_end`), and adds EXIT-ENTRY, LOOK-TRACK, MIDDLE-SWAP, ESTABLISH, POV and ROLE, plus an AXIS warning for a cross_reason that names no legal method. A `role: protection` card is checked but never becomes the next card's starting state.

### C-20261005-1 · 2026-10-05 · Output ranks the diff's errors above by-eye doubts (S6)
- because: T-20261004-1, L-005
- files: SKILL.md
- The Output section reports as errors only what the diff or a named rule finds, and puts one by-eye doubt last as a question

### C-20261004-1 · 2026-10-04 · Thirty-degree rule shared with cinewright-shots; prop bible and two new diff codes
- because: user request (cinewright S3); first local render's prop drift (cinewright-design L-003)
- files: references/thirty-degree-rule.md (now a copy of shared/vocab), references/shot-checklist.md, SKILL.md, needs.json
- The thirty-degree entry moved to shared vocab so shots and continuity read one source. Step 1 lists `bibles/props.json`. The checklist adds DIALOGUE and HARD-SUBJECT warnings and the PROP warning for a held prop with no description.

### C-20261003-1 · 2026-10-03 · Created as an evergreen unit (cinewright S1)
- because: user request, R-20261003-1
- files: SKILL.md, references/, needs.json, RESEARCH.md, LEARNINGS.md, TESTS.md, evals/evals.json, evergreen.json, MAINTENANCE.md
- Initial version. Tier `slow`, interval 120d. Lessons L-001 to L-004 recorded at creation. First test run is logged in TESTS.md.
