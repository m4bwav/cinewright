# Changelog: cinewright-design

Every change to [SKILL.md](SKILL.md) and its companions, newest first, each with the reason. Reasons cite findings in [RESEARCH.md](RESEARCH.md) (`R-`), lessons in [LEARNINGS.md](LEARNINGS.md) (`L-`), and test runs in [TESTS.md](TESTS.md) (`T-`). State in `evergreen.json`. Protocol: [MAINTENANCE.md](MAINTENANCE.md).

### C-20261114-1 · 2026-11-14 · Artwork props, changing artworks, palette break (Felleman)
- because: book distillation (technique-harvest), R-20261114-1
- files: references/prop-constants.md, prop-sheets.md, color-script.md
- Artwork prop fields and verbatim identity string for portraits; one state per stage for a changing artwork; a named palette-break reveal. Book rules, unverified. Lines trimmed to hold size.

### C-20261113-1 · 2026-11-13 · Dated source per period prop; visual concept and cliche check (Art Direction Handbook)
- because: book distillation (technique-harvest), R-20261113-1
- files: references/prop-constants.md, visual-structure.md
- prop-constants: each period prop names a dated source and year, no guessed details; visual-structure: one-line visual concept and a cliche check. Book rules, unverified.

### C-20261113-1 · 2026-11-13 · Colour associations and colour motifs
- because: R-20261113-1 (Bellantoni 2005, book rule, unverified, culture-bound); RESERVED check measured on one local film, 12 of 12 hits right by eye
- files: references/color-associations.md, references/color-motifs.md (new), references/color-script.md (Related line), SKILL.md Step 1 item 2, shared schema `visual_structure.motifs`, `cards graph` MOTIF and RESERVED flags
- Default hue readings written as questions to check a plan against, and motif devices with two script checks.

### C-20261110-2 · 2026-11-10 · RefMod prompt builder; dataset repeat rule
- because: technique harvest 2026-11-10 (posts 1wtu82e unmeasured, 1x0imbp single maker)
- files: references/lora-or-references.md (RefMod Text Encode for several characters; anything in over a third of the set becomes identity, check proportions; trims for budget)

### C-20261110-1 · 2026-11-10 · Install-test numbers
- because: install tests 2026-11-10 in the technique harvest
- files: references/lora-or-references.md (RefMods line)

Entry shape: `### C-YYYYMMDD-n · date · one-line summary`, then `because:`, `files:`, and a sentence on what changed.

### C-20261109-1 · 2026-11-09 · lora-or-references: candid-light refs, judge checkpoints in the shot workflow
- because: technique harvest 2026-11 (community posts reviewed in a separate harvest workspace), each item single-source and untested here
- files: references/lora-or-references.md (Rules, Pitfalls; trims to stay under the token budget; the H3 LoRA data point went to genvideo h3-long-takes)

### C-20261104-1 · 2026-11-04 · On-screen text and interfaces reference
- because: Addey, *Typeset in the Future* (Summary and interviews); no entry covered designing screens and signs
- files: references/on-screen-text.md (new), references/INDEX.md, SKILL.md (Step 3)
- Sorts text into must-read and must-not-read, keeps plates blank, and gives ways to keep background text unread.

### C-20261022-1 · 2026-10-22 · Visual structure plan, story graph, colour rows (books track 3)
- because: books track 3 (Block, *The Visual Story*; Brown, *Cinematography*; *FilmCraft: Cinematography*; Phillips on Resolve), decision 2026-10-22-books-track3
- files: SKILL.md (Step 1), references/visual-structure.md (new), references/color-script.md, evals/evals.json (action-2); shared schemas style (`visual_structure`) and scenes (`intensity`, `space`, `color`); shared/lib/cine.py `cards graph`
- Design draws the story intensity per scene, picks constants and two or three changing components, and checks the curve with `cards graph`; the colour script becomes a measurable row per scene and names its scheme.

### C-20261016-3 · 2026-10-16 · Lesson: a fighter out of frame takes his new wound stage at his first card in frame; a back wound stays text; a sheathed weapon the story took away is a second weapon in the refs
- because: L-007
- files: LEARNINGS.md (Active: L-007)
- From the cards for a duel's last phrases.

### C-20261016-2 · 2026-10-16 · L-005 confirmed after the staged-refs merge
- because: L-005
- files: LEARNINGS.md (L-005 status)
- A project converted to staged refs compiled exactly as its swap snapshots did, and its next wound stage was one new key.

### C-20261016-1 · 2026-10-16 · Character refs keyed by stage (scene id or a named stage such as a wound)
- because: L-005, owner's go-ahead for the compiler change (2026-10-16)
- files: references/costume-arc.md, references/turnaround-sheets.md, LEARNINGS.md (L-005 resolved); shared/lib/cine.py, shared/schemas/character-bible.schema.json, shared/schemas/shot-card.schema.json, tests/test_cine.py
- `refs` may be keyed like wardrobe and a card's cast entry names its stage with `refs_stage`; the compiler sends one stage per card, continuity checks the stage names and their order.

### C-20261015-3 · 2026-10-15 · L-005 confirmed: the refs swap reaches earlier cards; wound stages need a cast-level stage
- because: L-005 (the first scene-1b card), field lesson 124
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
