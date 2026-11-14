# Changelog: cinewright-edit

Every change to [SKILL.md](SKILL.md) and its companions, newest first, each with the reason. Reasons cite findings in [RESEARCH.md](RESEARCH.md) (`R-`), lessons in [LEARNINGS.md](LEARNINGS.md) (`L-`), and test runs in [TESTS.md](TESTS.md) (`T-`). State in `evergreen.json`. Protocol: [MAINTENANCE.md](MAINTENANCE.md).

Entry shape: `### C-YYYYMMDD-n · date · one-line summary`, then `because:`, `files:`, and a sentence on what changed.

### C-20261114-1 · 2026-11-14 · Time-pressure tags (Sculpting in Time)
- because: book distillation (technique-harvest), R-20261114-1
- files: references/time-pressure.md (new)
- New entry: still/flowing/rushing tag per shot, flag fast cuts of still frames, regenerate a shot that will not cut. Long takes marked partly applicable to 5-15 s clips. Motion-measure script skipped. Book rules, unverified.

### C-20261113-2 · 2026-11-13 · Early pick-up of a move as a tension beside cut-on-action (Murch)
- because: book distillation (Walter Murch, Suddenly Something Clicked, 2025, leftovers after C-20261106-1), R-20261113-2
- files: references/cutting-on-action.md
- One line: an early pick-up from a new angle can jar, to be judged by watching, not a rule. Book view, unverified.

### C-20261113-1 · 2026-11-13 · Draft cut review: structure map and draft-cut failures (Documentary Storytelling)
- because: book distillation (technique-harvest), R-20261113-1
- files: references/draft-cut-review.md (new); SKILL.md
- New entry draft-cut-review: a structure map (section times, loudness peaks, cut times, train start) and the draft-cut failure list. The map was tried on one 148 s local cut and flagged real faults (transit as loud as the crash, even cut rhythm, train at 30 percent); failure list is book rule, unverified.

### C-20261109-2 · 2026-11-09 · Reaction timing, cut to the one acted on, splits lean to the POV, from Rabiger
- because: book notes round5 (books/plugin-learnings, track 21)
- files: references/reaction-timing.md (new), cut-points.md, j-and-l-cuts.md; vocab cut-terms (counterpoint, dissonance)
- Reply gaps clipped, natural or weighted, with starting numbers marked as guesses.

### C-20261109-1 · 2026-11-09 · Cutting after the move, first-frame motion (Arijon)
- because: book distillation (round 5, books/plugin-learnings/round5), pre-approved
- files: references/cutting-on-action.md
- Cut 2-3 frames after a move for forward cuts on one lens line; match the dominant move; every card starts on some motion; rising stays in frame. Book rules, unverified.

### C-20261106-1 · 2026-11-06 · Fine cut placement (Murch)
- because: book distillation (Murch, *Suddenly Something Clicked*, 2025), pre-approved
- files: references/cut-points.md
- Fricative, weight shift, exit pressure, identical return, opening frames. Book rules, unverified on generated clips.

### C-20261101-1 · 2026-11-01 · Hits generated in two halves (MS1)
- because: book distillation (Kenworthy, *Master Shots* Vol. 1, 2009), pre-approved
- files: references/cutting-on-action.md
- Strike on card A, recoil on card B, cut on the next impact. Book rule, unverified.

### C-20261022-4 · 2026-10-22 · Animatic without ffmpeg
- because: books track 7 (Brito, *Blender for Video Production*); polywright recipe encode-mp4, run on Blender 5.2.1
- files: references/animatic.md (Pitfalls)
- One line: with no ffmpeg, Blender's sequencer encodes image sequences to an MP4 at an exact frame count.

### C-20261022-3 · 2026-10-22 · Animatic stills at the moment before the peak (books track 4)
- because: books track 4 (Mateu-Mestre, *Framed Ink* 1 and 2; Mascelli, *The Five C's*; Katz, *Shot by Shot*; Block, *The Visual Story*; Brown, *Cinematography*; Gurney), decision 2026-10-22-books-track4
- files: references/animatic.md
- Pick each action card's still just before the peak or at a key pose (after Gurney, *Imaginative Realism*).

### C-20261022-2 · 2026-10-22 · Attention continuum, Block's editorial rhythm, frame repairs (books track 3)
- because: books track 3 (Block, *The Visual Story*; Brown, *Cinematography*; *FilmCraft: Cinematography*; Phillips on Resolve), decision 2026-10-22-books-track3
- files: SKILL.md (Steps 3 and 4), references/attention-continuum.md (new), references/pacing.md, references/cutting-around-bad-frames.md; shared/lib/cine.py (ATTENTION warning); shared/lib/cine_post.py (`grade measure --plan`)
- Calm cuts keep the eye in one cell and peaks may jump; a cut's beat follows the contrast between its shots; one broken frame is replaced from its neighbours; the cut is measured against the visual plan.

### C-20261022-1 · 2026-10-22 · Cut points, seam-hiding joins, a planned action overlap, the audience pass (books track 2)
- because: books track 2 (Katz, *Shot by Shot*; Mascelli, *The Five C's*; Murch, *In the Blink of an Eye*), decision 2026-10-22-books-track2
- files: SKILL.md (Step 3 item 2, Step 5 item 3), references/cut-points.md (new), references/cutting-on-action.md, references/pacing.md, references/assembly-to-delivery.md, shared vocab cut-terms (clearing the frame, foreground wipe, soft cut), evals action-2
- Cut where an idea ends, on a look or a reaction before an action; the two branches of a dialogue line; card B repeats the last 0.5-1 s of card A's action; a picture-only first assembly and an audience pass by a fresh context before lock; notes traced to their cause upstream.

### C-20261009-1 · 2026-10-09 · Animatic before any render (cine_post.py)
- because: user request (2026-10-09: research what AI film makers build to raise quality, and add the gaps: prop sheets, LoRAs, animatic, blockout control, identity scoring, one shared grade)
- files: SKILL.md (description, CINE_POST line, new section "Before any render: animatic"), references/animatic.md (new), needs.json (cine_post.py)
- The edit starts before rendering: stills timed to the cards over scratch audio, with a timing sheet, so story and length lock before video is paid for.

### C-20261005-2 · 2026-10-05 · L-003 retired: the rerun did not move its case (S6)
- because: T-20261005-1, L-003
- files: LEARNINGS.md, LEARNINGS-ARCHIVE.md
- L-003 moved to the archive; the description is unchanged

### C-20261005-1 · 2026-10-05 · Step 2 covers a mid-shot fault and states the rule (S6)
- because: T-20261004-2, L-004
- files: SKILL.md
- Step 2 gains the mid-shot cover (a cutaway or reaction of at least 1 s, or a cut on action) and the edit-or-re-render rule

### C-20261004-2 · 2026-10-04 · Description tuned (S6)
- because: T-20261004-2, L-003
- files: SKILL.md
- Description tuned for triggering: the Use clause ends "not vlogs or live footage"

### C-20261004-1 · 2026-10-04 · Created as an evergreen unit (cinewright S5)
- because: user request, R-20261004-1, L-001, L-002
- files: SKILL.md, references/, needs.json, RESEARCH.md, LEARNINGS.md, TESTS.md, evals/evals.json, evergreen.json, MAINTENANCE.md
- Initial version. Tier `slow`, interval 120d. Lessons L-001 and L-002 recorded at creation from the S5 exit check. First test run is logged in TESTS.md.
