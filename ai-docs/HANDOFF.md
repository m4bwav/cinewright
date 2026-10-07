# Handoff

## Current state
- S7 is merged (PR #9). The repo is still private: https://github.com/m4bwav/cinewright.
- 2026-10-06/07 night: first end-to-end film test (a 120 s novel-chapter adaptation, 25 cards, 8 H3 sequences, five render passes). Record: [notes/2026-10-07-library-film-test.md](notes/2026-10-07-library-film-test.md). Branch `test/library-film` holds the compiler fixes it found (H3 15 s = 362 frames, card-only travel, no double article, `cards export --film-json --sequence --model`), the budget answers, design L-004 and genvideo L-006 to L-008; its PR waits for Mark.
- Checks on that branch: tests 73 (3.14 and 3.9), kb lint 0 errors, budget GREEN, scrub 0 hits.

## Mark's answers (2026-10-06 21:00: "yes or as you recommend", but test before submitting anywhere)
- Applied: runtime budget row counted once (decision accepted), description budget trimmed to 3,994 of 4,000.
- Yes, after he has seen the test film: claude.ai skill Upload, claude.ai Add marketplace, VS Code Copilot route; D5 public; 0.1.0 tag and release. Registrations and directory or awesome-copilot submissions still need their own go.

## Open from the test (see the note)
- Sequence header puts every cast member in every shot; no per-scene constants; dialogue tone wording; the 300-word guide for multi-shot H3.

## Next single action
- Mark watches the best-of film and reviews the test/library-film PR; then run [next-session-prompt.md](next-session-prompt.md) (S7b: remaining routes, public, release).
