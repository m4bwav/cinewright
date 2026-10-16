# Learnings: cinewright-camera

Procedural lessons for [SKILL.md](SKILL.md). Research findings live in [RESEARCH.md](RESEARCH.md); every change is logged in [CHANGELOG.md](CHANGELOG.md); test runs in [TESTS.md](TESTS.md); state in `evergreen.json`. Format: [MAINTENANCE.md](MAINTENANCE.md) (LEARNINGS-FORMAT in the evergreen protocol). Retired entries go to LEARNINGS-ARCHIVE.md with a reason.

Write an entry the moment a real signal happens: a user correction, the same error twice, a workaround, an environment fact, a failed test. Check existing entries first: add, update, retire or none. Trigger and Hypothesis are required.

## Active

### L-001 · 2026-10-04 · A model renders only its own sizes; compose for the film's frame and crop later
- Trigger: 2026-10-04, S4 exit check: "shoot it like 1970s New Hollywood, 2.39" could not set aspect_ratio to 2.39 because compile stops on a size the model card does not offer
- Hypothesis: Video models render a fixed set of aspects (mostly 16:9 and 9:16), so a scope frame has to be asked for as composition inside the render and made in finishing
- Rule: Keep aspect_ratio a size the model offers, set frame_aspect, let the compiler add the composition sentence, and crop in finishing; never ask for letterbox bars
- Evidence: C-20261004-1 (references/aspect-and-framing.md, shared/lib/cine.py frame_words), confirmed 2026-10-04
- Scope: skill
- Status: active · helpful 1 · harmful 0 · last_confirmed 2026-10-04

### L-002 · 2026-10-04 · Say "lighting a scene" and hand period looks to history
- Trigger: 2026-10-04, S6 matrix T-20261004-2: trigger-1 (clips look flat; how to light a night scene in a cabin) invoked the skill Haiku 1 of 3, the rest answered with no tool; history's trigger-1 (1970s New Hollywood, 2.39) came here Haiku 2 of 3
- Hypothesis: "choosing lenses, light or format" does not match a how-to-light question, and "aspect ratio" pulls period-style requests that name a frame
- Rule: The Use clause says "when lighting a shot" (not "a scene": Sonnet then took the three.js lights decoy 1 of 3) and ends "period looks: cinewright-history"
- Evidence: C-20261004-2 (description); confirmed T-20261005-1: trigger-1 Haiku 3 of 3 (was 1 of 3); decoy-3 Sonnet and Opus 0 of 3 (Sonnet took it 1 of 3 with "a scene")
- Scope: skill
- Status: active · helpful 1 · harmful 0 · last_confirmed 2026-10-05

### L-003 · 2026-10-16 · An overhead whose frame top points along a lying body turns the face upside down; lay the body across the frame
- Trigger: the pause after a rapier duel's fifth phrase: an overhead close-up of the hero on his back, head west. The set plan's overhead camera had frame top east, chosen to keep the pair's screen order as seen from side A; with his feet to the east that put his crown at the bottom of the frame and his face upside down, and the set check read the overhead as side B because its centre stood almost on the line through the pair.
- Hypothesis: an overhead camera's frame-top bearing sets both the screen order and which way a lying face reads, and a 16:9 frame holds a lying figure best when the body runs across it.
- Rule: for an overhead on someone lying down, point frame top square to the body, so it lies across the frame with the head to one side; of the two such bearings, take the one that keeps the pair's screen order (here frame top north keeps west frame-left, so the hero still sits left of the antagonist). Centre the camera on the chest, off the line on the side the coverage uses. Never point frame top at the feet.
- Evidence: the duel project's set plan cameras `floor` (frame top east) and `floor-p5` (frame top north, on side A), card 1AG; set check 36 beats, 0 errors.
- Scope: skill (overhead framing, screen direction)
- Status: active · helpful 1 · harmful 0 · last_confirmed 2026-10-16
