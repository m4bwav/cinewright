# Changelog: cinewright-genvideo

Every change to [SKILL.md](SKILL.md) and its companions, newest first, each with the reason. Reasons cite findings in [RESEARCH.md](RESEARCH.md) (`R-`), lessons in [LEARNINGS.md](LEARNINGS.md) (`L-`), and test runs in [TESTS.md](TESTS.md) (`T-`). State in `evergreen.json`. Protocol: [MAINTENANCE.md](MAINTENANCE.md).

Entry shape: `### C-YYYYMMDD-n · date · one-line summary`, then `because:`, `files:`, and a sentence on what changed.

### C-20261026-1 · 2026-10-26 · crowd-prompting: blockout depth at 0.6, refs only for a lifelike side
- because: the owner's review of the 2026-10-25 takes and a follow-up test (ai-docs/research/2026-10-25-layered-character-passes.md, Update 2026-10-26)
- files: references/crowd-prompting.md (Rules, Numbers, last_checked); shared/lib/cine.py CAST-COUNT message
- At 0.8 the render paints the blockout's dummies as mannequins; the route is now 0.6/0.4 with sheets only for a side that looks like real people, the other side in words, and a start frame approved before a batch because the look varies by seed.
### C-20261025-1 · 2026-10-25 · crowd-prompting: blockout plus per-side refs over 5 people; layered passes ruled out
- because: user request (layered character passes); test in ai-docs/research/2026-10-25-layered-character-passes.md
- files: references/crowd-prompting.md (Rules, Numbers, last_checked)
- The limit drops from about 8 to about 5 acting people; above it, one render from a 3D blockout's depth at 0.8 with one or two sheets per side; adding people a few per pass was tested and does worse; the CAST-COUNT check and the ask-or-run rule.

### C-20261023-1 · 2026-10-23 · --sequence keeps a card's featured props and says a shared soundscape once
- because: a film's G08 (field lesson; two cards, the second with an arrow as a featured prop) stopped with "compiler bug: prop 'arrow' not verbatim": featured props were only in the single-card subject, which a sequence block does not carry
- files: shared/lib/cine.py (card_parts staging, compile_cards sound), tests/test_cine.py (test_sequence_keeps_featured_props)
- A sequence shot block now states each featured prop and where it is (a prop a cast member holds is said once, in the holding words), and cards of one place that share a soundscape no longer repeat it.

### C-20261022-4 · 2026-10-22 · Compile writes horizon, dutch side, view and the new moves (books track 4)
- because: books track 4 (Mateu-Mestre, *Framed Ink* 1 and 2; Mascelli, *The Five C's*; Katz, *Shot by Shot*; Block, *The Visual Story*; Brown, *Cinematography*; Gurney), decision 2026-10-22-books-track4
- files: SKILL.md (failure code pointer), needs.json (failures-framing), shared/lib/cine.py (card_parts: HORIZON_WORDS, dutch side, VIEW_WORDS)
- Set fields compile to words ("the horizon on the lower third of the frame", "the frame tilted down to the right", "seen from behind at a three-quarter rear angle, only the cheek line showing"); unset fields change nothing, so no committed prompt changed.

### C-20261022-3 · 2026-10-22 · Compile writes space, line, attention and light words (books track 3)
- because: books track 3 (Block, *The Visual Story*; Brown, *Cinematography*; *FilmCraft: Cinematography*; Phillips on Resolve), decision 2026-10-22-books-track3
- files: references/compile-rule.md; shared/lib/cine.py `card_parts`
- The scene's space goes into the context, the card's line and attention cell after the camera words, and the light gets the far-side key, backlit atmosphere, firelight flicker and a hidden face.

### C-20261022-2 · 2026-10-22 · Compile says entrances, exits, end positions, head turns and held moves (books track 2)
- because: books track 2 (Katz, *Shot by Shot*; Mascelli, *The Five C's*; Murch, *In the Blink of an Eye*), decision 2026-10-22-books-track2
- files: references/compile-rule.md, shared/lib/cine.py (card_parts), shared vocab camera-moves (settle and move meanings), shared schema shot-card (`camera.settle`)
- `enters`, `exits`, `position_end` and `eyeline_end` become sentences in the action; `camera.settle` compiles to a move that starts and ends on held frames.

### C-20261022-1 · 2026-10-22 · LTX-2: judge stage 1 before paying for stage 2
- because: user request (book-learnings track 1: Enochs, *Video Generation with AI*, on the LTX-2.3 two-stage pipeline); checked on the LTX-2.5 model page 2026-10-22 (base stage, 2x spatial upsampler, distilled refine)
- files: references/ltx-2.md (a Rules line, a volatile claim dated 2026-10-22; last_checked stays with the last full card refresh); shared vocab failures-motion copy (`flicker`, `lip-lag`)
- Blocking, cuts, motion and sound timing are fixed in stage 1, so `qc measure` and the sheet run on the decoded stage-1 latent and rerolls happen there; look and faces are judged on the final.

### C-20261016-2 · 2026-10-16 · minimax-h3: card beats compile to a Timeline
- because: L-016
- files: references/minimax-h3.md (`beat_stamp`, `beats_lead`, a Rules line); shared schemas and lib (card `beats`)
- A card's `beats` compile to `Timeline: [t0s-t1s] ...` in place of its action on models whose card has `beat_stamp`; others get the action.

### C-20261016-1 · 2026-10-16 · Lesson: a fight card's hits land when each hit has its own timecode
- because: L-016
- files: LEARNINGS.md (Active: L-016)
- Open test 2 of the fight-planning research note, answered on one card at two step counts.

### C-20261014-1 · 2026-10-14 · minimax-h3: violence, fight LoRAs, forced end frame
- because: user request (impalement, fights, healing, flying), R-20261014-1
- files: references/minimax-h3.md (Rules, sources, last_checked)
- Three rules: nothing is refused locally and a pinned contact still lands a stab; the fight LoRA conflict and the one-LoRA rule; first/last frame overshoots and snaps to the end frame.

### C-20261013-1 · 2026-10-13 · crowd-prompting entry
- because: user request (battle and crowd scenes from separate generations, Blender offloading), R-20261013-1
- files: references/crowd-prompting.md (new), SKILL.md step 2
- New entry: tiers, lanes, one reference per subject, clone ban, priority line, stress ladder and subject limits per model.

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
