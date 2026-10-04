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
