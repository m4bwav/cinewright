# Learnings: cinewright-continuity

Procedural lessons for [SKILL.md](SKILL.md). Research findings live in [RESEARCH.md](RESEARCH.md); every change is logged in [CHANGELOG.md](CHANGELOG.md); test runs in [TESTS.md](TESTS.md); state in `evergreen.json`. Format: [MAINTENANCE.md](MAINTENANCE.md) (LEARNINGS-FORMAT in the evergreen protocol). Retired entries go to LEARNINGS-ARCHIVE.md with a reason.

Write an entry the moment a real signal happens: a user correction, the same error twice, a workaround, an environment fact, a failed test. Check existing entries first: add, update, retire or none. Trigger and Hypothesis are required.

## Active

### L-009 · 2026-10-24 · `offscreen-look-plays-to-lens`: a single with the looked-at person off frame turns to the camera
- Trigger: siege news film, generation 1E+1F (a reporter asks a soldier a question, then the soldier answers and nods up at a siege tower), eight takes over d1-d3 and r2: in every one the reporter faces the lens in 1E and the soldier faces the lens with his eyes rolled up in 1F. Mark (2026-10-24): "the classic problem of the person facing towards the camera instead of the thing they're looking at. Cinewright should have helped you avoid this." Both cards were `framing: single` with `looks_at` someone not in the frame; 1F also had `looks_at: reporter` with `eyeline: up`, which compiled to "Walter is looking up, at Hugh Barrington", a target that is not up.
- Hypothesis: with nothing in the frame to look at, the video model falls back on the most common picture of a person talking, which is to the lens; a newsreader identity pulls harder still. "Looking toward frame left, at X" does not turn the body when X is absent.
- Rule: when someone must look at a person or thing, put it in the frame: an over-the-shoulder with the other person's back at the frame edge, or the object in shot. Otherwise turn the body in words ("side-on to the camera, his body and face turned to frame left toward the wall") and add "never into the lens". Give `looks_at` the thing the `eyeline` points at, never a person in another direction. A diff check should warn on a single whose `looks_at` target is out of the frame and is not `camera`, and on `eyeline: up/down` with a person as `looks_at`.
- Evidence: siege_news d1-d3 and r2 G04 sheets; Mark's note in `review/answers.json` q18; the repair (over-the-shoulder in 1E, side-on in 1F, `make_pass.py` FIXES "1E+1F"), pass siege_r5 G04 t12-t14: all three turned both men off the lens (README Session 6). The scorer's identity check then rejects every take, because it counts the shoulder in the foreground as a stranger.
- Scope: skill and tool (shared/lib/cine.py continuity_diff: a proposed OFFSCREEN-LOOK warning)
- Status: active · helpful 1 · harmful 0 · last_confirmed 2026-10-24

### L-008 · 2026-10-22 · `straight-in-is-for-cut-ins`: a straight-in check on any size change fires on cuts back out
- Trigger: books track 4 added STRAIGHT-IN (two or more size steps, under 10 degrees of azimuth, someone off centre); on 163 cards of seven local multi-shot films it fired on 7, two of them cuts from a medium to a wide
- Hypothesis: Mascelli's rule is about moving in: a cut straight back out on the axis re-establishes, and nobody reads it as a jump
- Rule: STRAIGHT-IN warns only when the cut goes tighter; a planned punch-in at the turn keeps the warning, with the reason in `notes`
- Evidence: after the change 4 of 163 cards (2.5 %), all cut-ins on two fighters across the frame on one axis; tests/test_cine.py TestFraming, mutation run
- Scope: tool (shared/lib/cine.py continuity_diff) and vocab (thirty-degree-rule)
- Status: active · helpful 0 · harmful 0 · last_confirmed 2026-10-22

### L-001 · 2026-10-03 · Chained clips lose identity and prop shape; restate both in every continuation
- Trigger: Field lesson 005 of the maintainer's local renders, 2026-09-06, 'Chained clips lose character identity and prop continuity, and the splice reads as a pause'
- Hypothesis: A first frame conditions composition; nothing in it tells the model who a person is or what shape a prop has
- Rule: Restate the identity string and prop constants verbatim in every continued clip; start it 'already moving, no pause' and trim the eased-in head frames
- Evidence: C-20261003-1 (references/ai-continuity.md, references/identity-strings.md), confirmed 2026-10-03
- Scope: skill
- Status: active · helpful 1 · harmful 0 · last_confirmed 2026-10-03

### L-002 · 2026-10-03 · Separate generations cut together read as the scene restarting
- Trigger: Field lesson 011 of the maintainer's local renders, 2026-09-28, 'Independent shots cut together read as the scene restarting; write the cuts inside long renders'
- Hypothesis: Every generation starts picture and sound from nothing, so each seam looks like a new start
- Rule: Prefer one generation holding several shots; put seams only at real changes of place or side, with one sound named on both sides
- Evidence: C-20261003-1 (references/ai-continuity.md), confirmed 2026-10-03
- Scope: skill
- Status: active · helpful 1 · harmful 0 · last_confirmed 2026-10-03

### L-003 · 2026-10-03 · Story directions give random facing; use one fixed frame-relative phrase
- Trigger: Field lesson 012 of the maintainer's local renders, 2026-09-28, 'Crowds face random ways; give a fixed screen direction, not toward the enemy'
- Hypothesis: The model has no map of the scene, so directions defined by the story have no meaning to it
- Rule: Write direction with the fixed screen-direction phrases in every prompt of the film; never a goal the shot cannot show
- Evidence: C-20261003-1 (references/axis-and-screen-direction.md, shared vocab screen-direction), confirmed 2026-10-03
- Scope: skill
- Status: active · helpful 1 · harmful 0 · last_confirmed 2026-10-03

### L-004 · 2026-10-03 · Negative lines lose; describe what is there with absences inside it
- Trigger: Field lesson 013 of the maintainer's local renders, 2026-09-29, 'Describe what IS in a shot; Avoid entries lose against strong associations'
- Hypothesis: Exclusion text is weak conditioning next to strong scene associations
- Rule: Describe positively and put absences inside the description; add a contrast sentence when two groups share a shot
- Evidence: C-20261003-1 (references/identity-strings.md, references/ai-continuity.md), confirmed 2026-10-03
- Scope: skill
- Status: active · helpful 1 · harmful 0 · last_confirmed 2026-10-03

### L-005 · 2026-10-05 · Report the diff's errors, not every doubt
- Trigger: 2026-10-05, S6 continuity outcome-1 (two one-word plants: the scar side in 1B, a grey sweater in 1A): Opus ran the diff and named both, then listed a correct key-light flip on 1C, take faults from takes.md and optional fields as further errors; judged "no invented errors" 0 of 3 in 2 of 3 runs
- Hypothesis: The Output section asked for "any call the rules could not make" with no rank, so a thorough model adds every by-eye doubt beside the diff's real errors
- Rule: Report as errors only what the diff or a named rule finds; put one by-eye doubt last as a question
- Evidence: C-20261005-1 (SKILL.md Output); confirmed T-20261005-1: outcome-1 Sonnet and Opus 3 of 3 after the edit
- Scope: skill
- Status: active · helpful 1 · harmful 0 · last_confirmed 2026-10-05

### L-006 · 2026-10-07 · claude.ai plugin skills cannot find their own folder from "the folder holding this file"
- Trigger: 2026-10-07, S7c account routes: claude.ai Add marketplace m4bwav/cinewright, Opus 5.5 loaded `cinewright-continuity (cinewright)` and ran `cd /mnt/skills/plugins/cinewright:cinewright-continuity`, which does not exist; every `cine.py` call failed and it answered from general knowledge. The uploaded ZIP of the same skill ran Step 0 fine
- Hypothesis: On the claude.ai plugin route the skill name is namespaced with the plugin and the folder path is not shown to the model, so it builds a path from the name
- Rule: Open. A skill that runs its own script must say how to find its folder when the path is unknown (search for its `scripts/cine.py` next to this SKILL.md) instead of assuming the working folder; retest the claude.ai plugin route after the change
- Evidence: notes/2026-10-06-s7-install-proof.md, "Account routes"
- Scope: all 13 public skills (same CINE line)
- Status: active · helpful 0 · harmful 0 · last_confirmed 2026-10-07

### L-007 · 2026-10-22 · A cut-in check per scene flags people the film already showed (`establish-people-film-wide`)
- Trigger: 2026-10-22, books track 2: the first ESTABLISH check (subject of a cut-in or insert seen in no earlier card of its scene) fired on 2 of 163 cards in seven local multi-shot films, both inserts of people who had been on screen in earlier scenes
- Hypothesis: the rule (after Mascelli) is about the viewer not knowing what the detail belongs to; a person met earlier in the film is known, a prop in a new scene may not be
- Rule: people count as established film-wide, props per scene; after the change the check fired on 0 of the 163 real cards and still fires on the planted test
- Evidence: tests/test_cine.py test_pov_role_protection_and_establish; the decision 2026-10-22-books-track2
- Scope: continuity diff ESTABLISH
- Status: active · helpful 1 · harmful 0 · last_confirmed 2026-10-22
