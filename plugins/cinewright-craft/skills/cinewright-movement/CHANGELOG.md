# Changelog: cinewright-movement

Every change to [SKILL.md](SKILL.md) and its companions, newest first, each with the reason. Reasons cite findings in [RESEARCH.md](RESEARCH.md) (`R-`), lessons in [LEARNINGS.md](LEARNINGS.md) (`L-`), and test runs in [TESTS.md](TESTS.md) (`T-`). State in `evergreen.json`. Protocol: [MAINTENANCE.md](MAINTENANCE.md).

Entry shape: `### C-YYYYMMDD-n · date · one-line summary`, then `because:`, `files:`, and a sentence on what changed.

### C-20261015-2 · 2026-10-15 · Fight plans: schema, cine_fight.py, entries fight-plan, fight-from-a-book, fight-previs
- because: user request (deeper choreography documents; combat notation, reversal graphs and timeline moments checked; adapt fights from books; 3D for fights), R-20261015-1, L-003
- files: SKILL.md (step 4), references/fight-plan.md, fight-from-a-book.md, fight-previs.md (new), references/fights-and-stunts.md (plan pointer, the double hit, Related), needs.json (cine_fight.py, fight-plan schema), evals/evals.json (action-2)
- A fight longer than one exchange is planned in `fights/<id>.json` before its cards and checked with `cine_fight.py check`, which also holds the cards to it; `sheet` writes the grid and a CSV for a chart of who is ahead. Codes, per-second spreadsheets and coloured graphs were left out (research note).

### C-20261015-1 · 2026-10-15 · Flight mode per character
- because: reviewer note 2026-10-15 (flying characters stepped on the air as if on ground)
- files: references/flying-and-levitation.md, shared vocab failures-motion (`air-steps`)
- Each card names flying or air-walking per character; a flyer's walking steps are a fault with its own code.

### C-20261014-1 · 2026-10-14 · wounds-and-healing and flying-and-levitation entries; fights-and-stunts on contact and blood
- because: user request (impalement, a wound that heals, real fights, flying people), R-20261014-1
- files: references/wounds-and-healing.md (new), references/flying-and-levitation.md (new), references/fights-and-stunts.md (Rules, Pitfalls, sources, Related)
- Contact can be rendered on local models with a pinned still; one fight LoRA at its trained steps; long weapons morph; healing is a two-frame change with the forced-end-frame warning; floating figures are held up by nothing, never by a simile about wires.

### C-20261013-1 · 2026-10-13 · crowd-blockout entry; battle-scenes ranks the ways to make an army wide
- because: user request (battle and crowd scenes from separate generations, Blender offloading), R-20261013-1
- files: references/crowd-blockout.md (new), references/battle-scenes.md (scale rule, core plus extension, takes budget), SKILL.md step on battles
- New entry stages crowds in 3D with polywright's `pw.py crowd`; battle-scenes now lists sound and cutting, a 3D blockout and tiling, cheapest first.

### C-20261004-3 · 2026-10-04 · battle-scenes links the post half
- because: user request (S5)
- files: references/battle-scenes.md
- The scale rule now names cinewright-finish crowd-multiplication, cinewright-sound battle-sound and cinewright-edit cutting-a-battle instead of 'planned in S5'.

### C-20261004-2 · 2026-10-04 · Added battle-scenes (map, sides, phases, scale without a rendered crowd)
- because: user request (Mark, S4 session: a component for designing and shooting large battle scenes and fight scenes)
- files: references/battle-scenes.md, SKILL.md (step 4 and description)
- New entry built on hard-subjects and fights-and-stunts; the compositing half (tiling crowds) is planned for cinewright-finish in S5.

### C-20261004-1 · 2026-10-04 · Created as an evergreen unit (cinewright S3)
- because: user request, R-20261004-1, L-001, L-002
- files: SKILL.md, references/, needs.json, RESEARCH.md, LEARNINGS.md, TESTS.md, evals/evals.json, evergreen.json, MAINTENANCE.md
- Initial version. Tier `slow`, interval 120d. Lessons L-001 to L-002 recorded at creation. First test run is logged in TESTS.md.
