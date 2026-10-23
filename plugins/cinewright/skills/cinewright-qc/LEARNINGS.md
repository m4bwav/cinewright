# Learnings: cinewright-qc

Procedural lessons for [SKILL.md](SKILL.md). What it needs installed (ffmpeg): [SETUP.md](SETUP.md). Research findings live in [RESEARCH.md](RESEARCH.md); every change is logged in [CHANGELOG.md](CHANGELOG.md); test runs in [TESTS.md](TESTS.md); state in `evergreen.json`. Format: [MAINTENANCE.md](MAINTENANCE.md) (LEARNINGS-FORMAT in the evergreen protocol). Retired entries go to LEARNINGS-ARCHIVE.md with a reason.

Write an entry the moment a real signal happens: a user correction, the same error twice, a workaround, an environment fact, a failed test. Check existing entries first: add, update, retire or none. Trigger and Hypothesis are required.

## Active

### L-008 · 2026-10-22 · `eye-trace-needs-faces`: a measured eye trace at a cut needs a face detector and finds faces on few cuts
- Trigger: books track 4 (Mascelli's eye scan, Murch's eye trace) asked for `qc cutcheck`, the measured version of the `attention` cells
- Hypothesis: the stdlib runtime has no face or subject detector, and wides, backs and profiles carry no face anyway
- Rule: no `qc cutcheck` here: the rubric `attention` row and the ATTENTION warning stay the check; a detector-based eye trace (largest face either side of each planned cut, warn over 0.35 of the width) runs outside the runtime and points a reviewer at a cut, never gates
- Evidence: on 236 planned cuts in 118 reviewed local takes, 219 were found within 0.6 s of the plan (median 0.10 s) but only 85 had a face on both sides; the jump passed 0.35 on 19 % of them, keeps and rejects alike, since nobody reviewed eye trace
- Scope: skill (references/look-pass, rubric attention row)
- Status: active · helpful 0 · harmful 0 · last_confirmed 2026-10-22

### L-007 · 2026-10-22 · `motion-proxies-miss-settle-and-strobe`: frame difference and column-shift pan speed cannot judge camera settle or strobing
- Trigger: books track 3 proposed two `qc measure` checks from Brown, *Cinematography*: `move-no-settle` (the last 0.5 s of motion under 30 % of its peak) and `pan-strobe` (a pan over a third of the frame a second)
- Hypothesis: whole-frame motion mixes the camera with the subject and the model's own shimmer, so neither measure isolates the camera
- Rule: both stay review items in the look pass, never `qc measure` checks. Try again only with a measure of the camera alone (global motion with the subject masked) and labelled settle or judder faults
- Evidence: 354 planned shots of 118 reviewed takes from local multi-shot films: static shots ended with a tail-to-peak motion ratio of median 0.47 against 0.63 for moving ones, and the 30 % line fired on 78 of 103 moving shots; the pan speed line fired on 17 of 354, its top hits kept tracking shots beside a moving car, and no review in the set names judder
- Scope: skill (cinewright-qc look-pass; shared vocab failures-motion)
- Status: active · helpful 0 · harmful 0 · last_confirmed 2026-10-22

### L-006 · 2026-10-22 · `flicker-not-flash`: a flicker check counts jumps a second, so one explosion flash never trips it
- Trigger: book-learnings build, 2026-10-22: a frame's mean brightness against the average of its two neighbours, on 152 reviewed takes of four local multi-shot films. At a 1.5-level jump and 2 a second, 4 of 58 keepers warned, all in an explosion comedy where flashes are the story; the two highest takes (17.9 and 12.5 a second) pulsed up and down every two or three frames for seconds
- Hypothesis: real flicker alternates for a long stretch; a flash or a fast move is one or two jumps
- Rule: `qc measure` warns on `flicker` at a 2.0-level jump, more than 3 a second inside a shot (no keeper reached it); it never fails a take until `qc agree` has scored it on reviewer labels with flicker named
- Evidence: luma series at 160 px (`frame_motion(clip, False)`), cut-guarded shot windows; the reviewer never named flicker, so precision is unmeasured
- Scope: tool (shared/lib/cine.py)
- Status: active · helpful 0 · harmful 0 · last_confirmed 2026-10-22

### L-004 · 2026-10-15 · `judge-grid-black-tile`: the judge's last tile fell past the end of a one-card clip
- Trigger: set field test, 2026-10-15: `qc judge --twice` failed the action on all three takes of one 5.2 s card, saying the sequence ends on a black frame; the clips play to the end
- Hypothesis: the 2x2 grid starts an eighth into the window but asked for the window's full length, so fps placed the fourth frame after the clip's last frame
- Rule: fixed in `judge_grid` (a 7/8 window with fps fitted to it: four frames, tested on the full clip and on a mid-clip window); before the fix, read any "black frame" or "ends early" verdict on a one-card clip as the judge's fault
- Evidence: ffmpeg showinfo, 3 frames before and 4 after; a rapier duel from a novel, takes s1a-s1c
- Scope: tool (shared/lib/cine.py)
- Status: active · helpful 1 · harmful 0 · last_confirmed 2026-10-15

### L-005 · 2026-10-15 · `rubric-checks-the-set`: the rubric had no set item; it now asks for the faced wall
- Trigger: set field test, 2026-10-15: the card rubric checked light, style and camera but nothing about the room, and the take that lost the room (an invented stair) had no item to fail
- Hypothesis: the rubric builds from the card's fields, and `camera.faces` is not one of its checks
- Rule: `qc rubric` now adds a `set` item from the card's `camera.faces` and that wall's string (code `set-drift`); add sharper claims from the set plan and its blockout class render in `qc/standing.json` under the card id ("Is the background free of any staircase?"), never from the prompt
- Evidence: five set claims judged twice per take: 4 yes and 1 split on the two takes that kept the room, a no on the stair in the one that lost it
- Scope: skill
- Status: active · helpful 1 · harmful 0 · last_confirmed 2026-10-15

### L-001 · 2026-10-03 · A multi-shot generation is one take: measure it whole, change one thing across its cards
- Trigger: 2026-10-03, first local render (cards 1A, 1B, 1C in one 14 s H3 generation): `qc spec --card 1A` judged the 14.4 s clip against a 6 s card, and the three rubrics each proposed a different next change
- Hypothesis: Rubrics are per card but a reroll re-renders the whole generation, so per-card changes stack into several changes at once
- Rule: Pass the generation label to `qc spec` (`--card 1A+1B+1C`); pick the single cheapest fix across all the generation's rubrics for the next take
- Evidence: C-20261003-2 (shared/lib/cine.py qc spec, SKILL.md Step 1 and Step 3), confirmed 2026-10-03 when take 2 changed only the eyelines and fixed 1B's eyeline and 1C's end state
- Scope: skill
- Status: active · helpful 1 · harmful 0 · last_confirmed 2026-10-03

### L-002 · 2026-10-03 · Small side-specific marks need a full frame, not the sheet
- Trigger: 2026-10-03, review of the first local H3 renders of the three-shot example: Maren's scar sat above her right eyebrow instead of through the left in both takes; take 1 passed identity at contact-sheet size (300 px frames) and only a full 864x480 frame showed it
- Hypothesis: At sheet size a thin mark is a few pixels, and left and right are easy to flip when reading a face
- Rule: For identity, read one full frame per shot (`ffmpeg -ss <t> -frames:v 1`) and check each side-specific mark against the bible as the character's left or right, not the viewer's
- Evidence: C-20261003-2 (references/qc-loop.md Rules), confirmed 2026-10-03
- Scope: skill
- Status: active · helpful 1 · harmful 0 · last_confirmed 2026-10-03

### L-003 · 2026-10-05 · Generate the rubric before a take exists; never write it by hand
- Trigger: 2026-10-05, S6 T-20261004-1: action-1 (write the QC checklist for card 1B before its first take) failed on Opus 2 of 3: it wrote 1B.checklist.md by hand after a compound shell command was refused, with no qc rubric call
- Hypothesis: Step 1 showed `--clip` as if required, so with no take the model judged the command unusable and fell back to writing the list itself
- Rule: Step 1 says `--clip` is left out before the first take and forbids a hand-written checklist
- Evidence: C-20261005-1 (SKILL.md); confirmed T-20261005-1: no run wrote the checklist by hand; Opus's failing run refused to and asked for the shell (a refused command, harness rev 1)
- Scope: skill
- Status: active · helpful 1 · harmful 0 · last_confirmed 2026-10-05
