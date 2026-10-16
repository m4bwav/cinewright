# Learnings: cinewright-movement

Procedural lessons for [SKILL.md](SKILL.md). Research findings live in [RESEARCH.md](RESEARCH.md); every change is logged in [CHANGELOG.md](CHANGELOG.md); test runs in [TESTS.md](TESTS.md); state in `evergreen.json`. Format: [MAINTENANCE.md](MAINTENANCE.md) (LEARNINGS-FORMAT in the evergreen protocol). Retired entries go to LEARNINGS-ARCHIVE.md with a reason.

Write an entry the moment a real signal happens: a user correction, the same error twice, a workaround, an environment fact, a failed test. Check existing entries first: add, update, retire or none. Trigger and Hypothesis are required.

## Active

### L-001 · 2026-10-04 · Draw an animal-drawn vehicle from the side; from behind, the order comes out wrong
- Trigger: Field lesson 020 of the maintainer's local renders, 2026-09-30, 'Draw a horse team and wagon from the side; from behind, the image model puts the horses behind the wagon'
- Hypothesis: From behind, 'in front of the vehicle' and 'nearest the camera' conflict in the model's layout; a side view has no such ambiguity
- Rule: Make guide stills and last beats side views with the direction in frame words, and check every still for the order before using it
- Evidence: C-20261004-1 (references/hard-subjects.md), confirmed 2026-10-04
- Scope: skill
- Status: active · helpful 1 · harmful 0 · last_confirmed 2026-10-04

### L-002 · 2026-10-04 · Few animals, large in frame; a far column of animals cannot be drawn
- Trigger: Field lesson 021 of the maintainer's local renders, 2026-09-30, 'Few animals, large in frame, fix the legs; a far column of animals cannot be drawn'
- Hypothesis: Leg detail scales with the animal's size in pixels; a far animal gets about one token of the model's grid
- Rule: Frame 1-5 animals at a third of the frame height or more, side-on, each named differently, the mass as one background line; spend compute on resolution, not steps
- Evidence: C-20261004-1 (references/hard-subjects.md, shared/lib/cine.py HARD-SUBJECT check), confirmed 2026-10-04
- Scope: skill
- Status: active · helpful 1 · harmful 0 · last_confirmed 2026-10-04

### L-003 · 2026-10-15 · An eval allow list written for one script silently blocks its companions
- Trigger: action-2 (fight plan) failed 2 of 2 on Sonnet: the skill wrote the plan and ran `cine_fight.py check` five times, every call refused, because the harness allowed `*cine.py*` only. The first fix then passed on `cine_fight.py check --help`.
- Hypothesis: allow-list patterns and evidence patterns name the file that existed when they were written; a new script needs both widened, and a pattern that matches the command name alone also matches its help
- Rule: when a skill ships a new script, add it to the harness allow list in the same change, and make the evidence pattern require the real argument (here a `.json` path), not the command name
- Evidence: evals/run_evals.py BASH_ALLOW (cine_*.py), evals.json action-2 input_match, T-20261015-1
- Scope: skill
- Status: active · helpful 1 · harmful 0 · last_confirmed 2026-10-15

### L-004 · 2026-10-15 · A fighter with a blade in each hand has one `holding`; an exchange covered by two shots links one card
- Trigger: phrase 2 of a rapier duel from a novel (rapier and dagger against rapier and stiletto): card `holding`/`holding_end` take one prop each, and continuity requires a card's `holding` to equal the previous card's `holding_end`, so cards had to pick one blade per hand-off (stiletto in, rapier out) though both stay in hand; exchange 3 was shot as two singles plus an insert, and `exchanges[].card` takes one id, so the second single and the insert cover the exchange without being linked.
- Hypothesis: the card and fight schemas assume one weapon per fighter and one card per exchange.
- Rule: until the schema has a second hand, put the blade the shot features in `holding`, chain `holding_end` to the next card's featured blade, and name both blades in the action text; link the exchange to the card that shows its operator's move and list the extra coverage cards in the project README. Proposed change: `holding_left` (or `holding` as a list) and `exchanges[].cards`.
- Evidence: the duel project's cards 1F-1K and fights/duel.json (exchanges 3-6), `cine_fight.py check --project` 0 errors, `continuity diff` 0 errors.
- Scope: skill (fight-plan) and shared schema
- Status: active · helpful 2 · harmful 0 · last_confirmed 2026-10-15

### L-005 · 2026-10-15 · A prop's floor mark decides which hand throws it and where it falls in each camera
- Trigger: the third phrase of a rapier duel from a novel ends with the antagonist flinging off his cloak; the set plan had already put the cloak's mark east of him and half a metre behind, and the first card draft had him throw it with his dagger hand, across his body, "away to frame left".
- Hypothesis: a mark written while blocking the room is a fact about the fighter's own side; a card written from the camera's view reads it as screen space and picks the hand that looks natural, which can be the wrong one.
- Rule: before writing a throw, a drop or a disarm, take the prop's mark relative to the fighter's mark and facing (here facing north, the mark to the east: his own right), give the throw to that side's hand, and then say where it lands in each card's frame from that card's camera (over the opponent's shoulder, the fighter facing the lens, his right is frame left; in the low insert aimed at him, the prop lands just beyond his boots, left of centre).
- Evidence: the duel project's cards 1Q and 1R (the throw with the rapier arm, the landing insert) and its set plan's mark for the cloak at the P3 pause.
- Scope: skill (fight-plan, blocking marks)
- Status: active · helpful 1 · harmful 0 · last_confirmed 2026-10-15

### L-006 · 2026-10-15 · Singles on a close pair turn too little to cut; move them in, not out
- Trigger: the duel's pauses cut between two side-on MCU singles of fighters standing about 2 m apart; from 4 m the camera turned only 29 degrees about the pair between the singles and the set check refused the cut, where the same singles 2.8 m apart had turned 39.
- Hypothesis: a side-on single square to the line, looking at its own fighter, turns about the pair's midpoint by 2·atan(half the gap / distance), so the turn falls as the fighters close in or the camera backs off.
- Rule: for singles on a close pair, keep the camera close (3.5 m for a 2 m gap gives 33 degrees) and lengthen the lens if the framing needs it; backing off with a longer lens makes the cut worse. When the gap is under about 1.5 m, cut singles with a two-shot or an over-the-shoulder between them instead.
- Evidence: the duel project's set plan (coverage beats for the P2 and P3 pauses, cards 1L, 1M, 1O, 1P) and its set check (2 errors at 4 m, 0 at 3.5 m).
- Scope: skill (coverage, blocking marks)
- Status: active · helpful 1 · harmful 0 · last_confirmed 2026-10-15
