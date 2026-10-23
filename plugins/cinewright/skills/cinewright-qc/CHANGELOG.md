# Changelog: cinewright-qc

Every change to [SKILL.md](SKILL.md) and its companions, newest first, each with the reason. Reasons cite findings in [RESEARCH.md](RESEARCH.md) (`R-`), lessons in [LEARNINGS.md](LEARNINGS.md) (`L-`), and test runs in [TESTS.md](TESTS.md) (`T-`). State in `evergreen.json`. Protocol: [MAINTENANCE.md](MAINTENANCE.md).

Entry shape: `### C-YYYYMMDD-n · date · one-line summary`, then `because:`, `files:`, and a sentence on what changed.

### C-20261022-4 · 2026-10-22 · Framing failure codes and a framing rubric row (books track 4)
- because: books track 4 (Mateu-Mestre, *Framed Ink* 1 and 2; Mascelli, *The Five C's*; Katz, *Shot by Shot*; Block, *The Visual Story*; Brown, *Cinematography*; Gurney), decision 2026-10-22-books-track4; L-008
- files: shared/vocab/failures-framing.md (new), needs.json; shared/lib/cine.py (RUBRIC `framing`)
- Eight codes (`edge-tangent`, `bg-tangent`, `focal-competitor`, `horizon-split`, `horizon-head`, `floating-feet`, `flat-depth`, `ots-wrong`) and one sheet question for edges, heads and feet. A measured eye trace was left out of the runtime (L-008).

### C-20261022-3 · 2026-10-22 · Look pass and nine light and structure codes (books track 3)
- because: books track 3 (Block, *The Visual Story*; Brown, *Cinematography*; *FilmCraft: Cinematography*; Phillips on Resolve), decision 2026-10-22-books-track3; L-007
- files: SKILL.md (Step 2), references/look-pass.md (new), references/review-passes.md; shared vocab failures-picture (`flat-light`, `source-mismatch`, `atmos-unlit`, `tone-hides-subject`, `space-break`, `attention-jump`) and failures-motion (`move-no-settle`, `pan-strobe`); shared/lib/cine.py RUBRIC rows `space` and `attention`, identity `na` under `light.tone: hide`
- Reviewers judge light and visual structure in one pass with its own codes; settle and pan speed stay by eye because the measures failed on real takes.

### C-20261022-2 · 2026-10-22 · Rank blind to cost, a decisive-frame board, notes as symptoms (books track 2)
- because: books track 2 (Katz, *Shot by Shot*; Mascelli, *The Five C's*; Murch, *In the Blink of an Eye*), decision 2026-10-22-books-track2
- files: references/take-selection.md, references/review-passes.md, references/qc-loop.md, shared vocab failures-motion (`insert-too-fast`)
- Takes are ranked without reroll counts in view; one frame per kept take goes on a board in cut order to catch drift between shots that are not adjacent; a note on the whole cut is traced upstream before a re-render.

### C-20261022-1 · 2026-10-22 · Flicker measure; random sides for reviews; rejected takes in the label queue; drift inside a take
- because: user request (book-learnings track 1: Huyen, *AI Engineering*; Enochs, *Video Generation with AI*); L-006
- files: shared/lib/cine.py (`frame_motion(clip, diff)`, `measure_take` flicker per shot, MEASURE_FLICKER, MEASURE_FLICKER_RATE; `scene_cuts` and `frame_motion` through `run_tool` to stay inside the runtime budget), shared vocab failures-motion (`flicker`, `lip-lag`, two Rules lines), SKILL.md (Step 1, flicker warns), references/take-selection.md (random sides, a side-bias Verify line), references/judge-calibration.md (gate-rejected takes in the label queue), references/identity-score.md (a face against its own first face), tests/test_cine.py (a flickering clip warns, a clean one does not)
- `qc measure` reports flicker a second per shot and warns past the threshold; reviewers see two takes in random order with the sides recorded; every film's label queue carries a few takes the gates removed; identity checks a face against itself across the take.

### C-20261015-2 · 2026-10-15 · Judge grid's black last tile fixed; the rubric checks the faced wall
- because: L-004, L-005
- files: shared/lib/cine.py (`judge_grid`; RUBRIC row `set`, filled from `camera.faces`), shared vocab failures-picture (`set-drift`), tests/test_cine.py, LEARNINGS.md
- The judge's 2x2 grid now holds four frames of a one-card clip; a card that faces a wall gets a `set` item from that wall's string, with the new code `set-drift`.

### C-20261015-1 · 2026-10-15 · Critic research: review passes, a vision judge, calibration, take selection
- because: R-20261015-1 (five research tracks and a 600-claim field test), user request
- files: SKILL.md (Steps 1-2), references/review-passes.md, references/vision-judge.md, references/judge-calibration.md, references/take-selection.md, references/qc-loop.md (note), shared/lib/cine.py (`qc judge`, `qc agree`, standing claims from `qc/standing.json` in `qc rubric`), shared vocab failures-motion (`air-steps`)
- A local vision model gives a second opinion per rubric item without seeing the card text, in both claim orders; the agent's verdict decides; the judge is scored against the agent with kappa and Wilson bounds; competing takes are ranked pairwise.

### C-20261009-1 · 2026-10-09 · Identity score entry
- because: user request (2026-10-09: add the gaps AI film makers fill, face-similarity scoring among them); field test against a reviewer's verdicts on two films
- files: SKILL.md (Step 2, one line before the rubric read), references/identity-score.md (new)
- How to score faces and props against the bible's refs, the verdicts, tuned thresholds, and where it cannot be trusted (faces under about 60 px).

### C-20261007-1 · 2026-10-07 · Step 1: qc measure, machine checks of a take
- because: user request (improve how a run and a shot are judged); field test on a 60 s four-section comedy and 24 reviewed takes of an eight-section film
- files: SKILL.md (Step 1 item 3), shared/lib/cine.py (qc measure)
- Planned cuts are matched 1.0 s early to 0.6 s late, because the model put stamped cuts 0.1-0.8 s early in 24 reviewed takes; a cut within 2 s outside that window is reported early or late (a long line holds a shot); still pictures and silence on static-camera cards that ask for them warn instead of failing.

### C-20261005-1 · 2026-10-05 · Step 1: rubric without a clip, never by hand (S6)
- because: T-20261004-1, L-003
- files: SKILL.md
- Step 1 says `--clip` is left out before the first take and that the checklist is never written by hand

### C-20261004-3 · 2026-10-04 · Description tuned (S6)
- because: T-20261004-1
- files: SKILL.md
- Description trimmed by 42 characters (take logs and last frames left the list) to make room for the S6 trigger fixes in other skills; the body still covers both

### C-20261004-2 · 2026-10-04 · Loudness presets and the loudness-targets vocab
- because: user request (S5) and the S5 loudness re-check recorded in cinewright-sound RESEARCH.md
- files: SKILL.md, references/qc-loop.md, needs.json, references/loudness-targets.md (copy), shared/lib/cine.py
- `qc loud --preset web|ebu-r128|atsc-a85|netflix|music-streaming`; the default moved from -16 ± 1 LUFS, -1 dBTP to the web preset (-18 ± 2, -2 dBTP) after the S5 re-check found the brief's R128 tolerance wrong and EBU's streaming range in R128 s2.

### C-20261004-1 · 2026-10-04 · Prop rubric item shows the prop's description
- because: first local render: 1A failed prop-drift (a cardboard box for a tin one) with nothing on the rubric to say what tin looks like
- files: scripts/cine.py (copy), scripts/schemas/prop-bible.schema.json (copy), needs.json
- `qc rubric` writes the props check as `holds the <name> (<description>)` when the prop bible describes it.

### C-20261003-2 · 2026-10-03 · Lessons from the first real render
- because: L-001, L-002
- files: SKILL.md (Step 1, Step 3), references/qc-loop.md, shared/lib/cine.py (qc spec takes a generation label)
- Multi-shot generations are measured whole and changed one thing at a time; identity is read on a full frame per shot.

### C-20261003-1 · 2026-10-03 · Created as an evergreen unit (cinewright S2)
- because: user request, R-20261003-1
- files: SKILL.md, references/qc-loop.md, needs.json, SETUP.md, RESEARCH.md, LEARNINGS.md, TESTS.md, evals/evals.json, evergreen.json, MAINTENANCE.md
- Initial version. Tier `moderate`, interval 30d. Commands `qc sheet|spec|loud|rubric` and `takes log|lastframe` in the shared runtime; failure codes shared with cinewright-genvideo.
