# Changelog: cinewright-genvideo

Every change to [SKILL.md](SKILL.md) and its companions, newest first, each with the reason. Reasons cite findings in [RESEARCH.md](RESEARCH.md) (`R-`), lessons in [LEARNINGS.md](LEARNINGS.md) (`L-`), and test runs in [TESTS.md](TESTS.md) (`T-`). State in `evergreen.json`. Protocol: [MAINTENANCE.md](MAINTENANCE.md).

Entry shape: `### C-YYYYMMDD-n · date · one-line summary`, then `because:`, `files:`, and a sentence on what changed.

### C-20261007-2 · 2026-10-07 · compile --join and the music field
- because: field test on a 60 s four-section comedy: an exterior establishing shot in the same generation as two interior shots came out with the interior's sofas and rug on the lawn, since the sequence header named only one place; user request (improve the audio)
- files: SKILL.md (Step 2 item 4), shared/lib/cine.py (compile_cards join, location change in sequence blocks, music), shared/schemas/shot-card.schema.json (music), references/minimax-h3.md (layout {music})
- `--join` keeps cards of different scenes in one generation and describes the new place in the block where it changes; a card's `music` fills H3's non_diegetic_music, or follows the sound on other audio models.

### C-20261007-1 · 2026-10-07 · Off-screen lines as H3 voiceovers, listeners silent, names respelled; lessons renumbered
- because: L-012 (owner's review of the library film), L-009 to L-011
- files: references/minimax-h3.md, LEARNINGS.md
- The H3 card gains `dialogue_offscreen` (the guide's "says in an off-screen voiceover") and `dialogue_silent`; models without a voiceover template leave an off-screen line out of the prompt with a warning. The library-test lessons were filed from number 6, which the archive already holds; they are now L-009 to L-011

### C-20261005-1 · 2026-10-05 · L-006 retired: the rerun did not move its case (S6)
- because: T-20261005-1, L-006
- files: LEARNINGS.md, LEARNINGS-ARCHIVE.md
- L-006 moved to the archive; the description is unchanged

### C-20261004-2 · 2026-10-04 · Description tuned (S6)
- because: T-20261004-1, L-006
- files: SKILL.md
- Description tuned for triggering: open with "Writes AI video prompts" and say "Use when asked for a prompt for one of these models or to turn shots into video-model prompts"

### C-20261004-1 · 2026-10-04 · Held props compile as the prop bible's description, with a verbatim guard
- because: first local render's prop drift (cinewright-design L-003)
- files: references/compile-rule.md, scripts/cine.py (copy), scripts/schemas/prop-bible.schema.json (copy), needs.json
- When `bibles/props.json` describes a held prop, subject and staging parts paste its description, and compile stops if it is missing from the prompt, like the identity guard. The staging part in sequences is kept (L-004).

### C-20261003-2 · 2026-10-03 · Every model card and compiler; failure codes; staging in sequences (cinewright S2)
- because: user request, R-20261003-2, L-003, L-004
- files: references/ (8 new model cards, veo-3-1 re-checked, compile-rule), SKILL.md, needs.json (failure codes), shared/lib/cine.py, shared/schemas/model-card.schema.json
- The Compile block gains vendor parameter names, ref tags, sentence moves, frame and size grids, layouts, multi-shot markers and cost. Sequence blocks now restate positions and props in hand.

### C-20261003-1 · 2026-10-03 · Created as an evergreen unit (cinewright S1)
- because: user request, R-20261003-1
- files: SKILL.md, references/, needs.json, RESEARCH.md, LEARNINGS.md, TESTS.md, evals/evals.json, evergreen.json, MAINTENANCE.md
- Initial version. Tier `fast`, interval 14d. Lessons L-001 to L-002 recorded at creation. First test run is logged in TESTS.md.
