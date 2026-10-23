# Changelog: cinewright-sets

Every change to [SKILL.md](SKILL.md) and its companions, newest first, each with the reason. Reasons cite findings in [RESEARCH.md](RESEARCH.md) (`R-`), lessons in [LEARNINGS.md](LEARNINGS.md) (`L-`), and test runs in [TESTS.md](TESTS.md) (`T-`). State in `evergreen.json`. Protocol: [MAINTENANCE.md](MAINTENANCE.md).

Entry shape: `### C-YYYYMMDD-n · date · one-line summary`, then `because:`, `files:`, and a sentence on what changed.

### C-20261023-1 · 2026-10-23 · Mist against inverse depth, tested once on H3
- because: L-007
- files: references/blender-passes.md (summary; Rules)
- The Mist line said a video model's response to Mist was untested. One blind test on H3 picked Mist over inverse depth on two seeds; the rule now says to render both and keep the better take.

### C-20261022-2 · 2026-10-22 · Entry blender-passes; master-plates tracking line; description names control passes
- because: books track 7 (van Gumster, *Blender All-in-One For Dummies*, passes and motion tracking; polywright recipes run on Blender 5.2.1); T-20261022-1; L-003
- files: references/blender-passes.md (new), references/master-plates.md (Pitfalls), references/blockout-control.md (Related), SKILL.md (description; the blockout paragraph), evals/evals.json (action-blender)
- How to render a blockout's control passes in Blender: inverse depth over one range per shot, Mist only with care (it is plain distance), masks from the same render, no depth of field or motion blur, Line Art as an untested edge option, baked set pieces. The description now names blockout control passes: without it the eval's three runs never loaded the skill.

### C-20261022-1 · 2026-10-22 · Controls carry no light: light the guide still (books track 4)
- because: books track 4 (Mateu-Mestre, *Framed Ink* 1 and 2; Mascelli, *The Five C's*; Katz, *Shot by Shot*; Block, *The Visual Story*; Brown, *Cinematography*; Gurney), decision 2026-10-22-books-track4
- files: references/blockout-control.md
- Gurney's lit maquette, corrected for this pipeline: depth, edge and pose passes carry no light, so a blockout that is also the first frame gets the planned light, and otherwise the words carry it.

### C-20261017-2 · 2026-10-17 · 3D models for film and AI video, the director's side
- because: user request: each plugin carries 3D modelling knowledge for its topic and points to polywright; R-20261017-1
- files: references/3d-models.md (new), SKILL.md (end of Step 3), RESEARCH.md
- What the 3D is for (previs, techvis, postvis, control), model only what the cards' cameras see, detail by shot size, plates for far scenery, grey controls, real scale and lens, and what to ask polywright for, with links to its contract and its film page.

### C-20261017-1 · 2026-10-17 · 3D models, sets and blockouts come from polywright's asset folder
- because: user request (polywright HANDOFF owed item 6: siblings call polywright through the folder contract)
- files: SKILL.md (end of Step 3)
- One sentence: when polywright is installed, ask it for 3D models, sets, crowd blockouts or figure references through its asset folder with the `video-blockout` target and read `out/` from `manifest.json`.

### C-20261015-2 · 2026-10-15 · First card against the set: control from the card's camera; the scene's sun names no wall
- because: L-005, L-006
- files: LEARNINGS.md
- The grid reference alone lost the room on the first card; Canny control from the card's own blockout camera kept it. The scene bible's sun line reaches every card, so it names no window.

### C-20261015-1 · 2026-10-15 · Blocking marks; light, plates and checks from a one-room field test
- because: user request (2026-10-15: sets, set references, blocking continuity, set LoRAs), L-003, L-004, research note ai-docs/research/2026-10-15-sets-and-loras.md
- files: references/blocking-marks.md (new), references/set-light.md, references/master-plates.md, references/set-check.md, SKILL.md (Step 1)
- Marks in metres per beat and cameras placed from them, with the derived checks; name a window wall's light only in its own plates; blockout plus Canny at a strength that keeps the hero's size, one grid reference; plate claims from a class render, asked twice.

### C-20261009-1 · 2026-10-09 · Blockout control
- because: user request (2026-10-09: research what AI film makers build to raise quality, and add the gaps: prop sheets, LoRAs, animatic, blockout control, identity scoring, one shared grade)
- files: SKILL.md (end of Step 3), references/blockout-control.md (new)
- A blockout or phone footage turned into a depth, pose or layout video drives motion through a model's control input; the entry covers sources, strengths and checks.

### C-20261007-1 · 2026-10-07 · Created as an evergreen unit
- because: user request, R-20261007-1, R-20261007-2, L-001, L-002
- files: SKILL.md, references/ (set-plan, wall-strings, master-plates, coverage-angles, set-light, set-check), needs.json, RESEARCH.md, LEARNINGS.md, TESTS.md, evals/evals.json, evals/check_walls.py, evergreen.json, MAINTENANCE.md; shared: location bible `walls`, shot card `camera.faces`, compile adds the faced wall, WALL check, validator `propertyNames`
- Initial version. Tier `moderate`, interval 30d, because the AI tooling for sets (3D worlds, angle-edit models, reference slots) changes monthly.
