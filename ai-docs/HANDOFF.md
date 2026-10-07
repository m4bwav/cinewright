# Handoff

## Current state
- S7 (PR #9) and the library film test (PR #10) are merged. The repo is still private: https://github.com/m4bwav/cinewright.
- 2026-10-07: Mark watched the best-of film. A rival's off-screen line came out of the hero's mouth, and the hero's name was said less well than in his audiobook. He asked for no new render. Both are fixed in the compiler and docs on `s7b/release`, PR #11 (https://github.com/m4bwav/cinewright/pull/11): an off-screen speaker becomes an H3 voiceover with the visible lips closed; `pronounce` respellings; OFFSCREEN, SPEAKERS, TONE and PRONOUNCE warnings. Record: the "Owner's review" section of [notes/2026-10-07-library-film-test.md](notes/2026-10-07-library-film-test.md) and the proposed decision [decisions/2026-10-07-off-screen-lines-compile-as-voiceovers-or-leave-the-prompt.md](decisions/2026-10-07-off-screen-lines-compile-as-voiceovers-or-leave-the-prompt.md).
- Checks on s7b/release: 80 tests (3.14 and 3.9), kb lint 0 errors, budget GREEN, scrub 0 hits, evergreen lint OK.

## Waiting on Mark
- Review PR #11 (code; it waits for him).
- How his audiobook says the hero's name, if he wants it in the film's `pronounce`. Untested on H3: one 4 s render would show whether H3 follows the voiceover phrase and the respelling. That render needs his go.
- Standing yes from 2026-10-06, now that he has seen the film: claude.ai skill Upload, claude.ai Add marketplace, VS Code Copilot route; D5 public; 0.1.0 tag and release. Release after PR #11 merges, so 0.1.0 carries the fix. Registrations and directory or awesome-copilot submissions each need their own go.

## Open from the test (see the note)
- Sequence header puts every cast member in every shot; no per-scene constants; the 300-word guide for multi-shot H3.

## Next single action
- Once PR #11 is merged, run [next-session-prompt.md](next-session-prompt.md) (S7b: remaining routes, public, release).
