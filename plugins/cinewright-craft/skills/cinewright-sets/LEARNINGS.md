# Learnings: cinewright-sets

Procedural lessons for [SKILL.md](SKILL.md). Research findings live in [RESEARCH.md](RESEARCH.md); every change is logged in [CHANGELOG.md](CHANGELOG.md); test runs in [TESTS.md](TESTS.md); state in `evergreen.json`. Format: [MAINTENANCE.md](MAINTENANCE.md) (LEARNINGS-FORMAT in the evergreen protocol). Retired entries go to LEARNINGS-ARCHIVE.md with a reason.

Write an entry the moment a real signal happens: a user correction, the same error twice, a workaround, an environment fact, a failed test. Check existing entries first: add, update, retire or none. Trigger and Hypothesis are required.

## Active

### L-001 · 2026-10-07 · `whole-room-string-pulls-to-hero-wall`: describe each wall on its own
- Trigger: set field test, 2026-10-07: a reverse to the fireplace wall and an east-door shot, both written as framing words after the room's full description, came back as the establishing desk-and-windows view (2 of 2)
- Hypothesis: the image model composes from the nouns in the prompt; framing words like "reverse shot looking north" carry little weight against named hero objects
- Rule: keep one-wall features out of the location description; give each wall its own string in `walls` and point the card at it with `camera.faces`; say what is not in view on a reverse
- Evidence: C-20261007-1 (references/wall-strings.md, compile and WALL check); re-render with the north wall's own string, same seed: fireplace, portrait over the mantel and sofas, no desk or windows (confirmed 2026-10-07)
- Scope: skill
- Status: active · helpful 1 · harmful 0 · last_confirmed 2026-10-07

### L-002 · 2026-10-07 · `stop-the-batch-when-the-words-change`: a running render keeps the old prompts
- Trigger: set field test, 2026-10-07: the batch script had loaded the shot list before the wall strings were written, so its later reverses would have rendered with the old words
- Hypothesis: a batch reads its prompts once at start
- Rule: after changing a set's words mid-batch, stop the batch, move the plates made with the old words to `_rejected/`, and restart; skip plates already made with the right words
- Evidence: field test log 2026-10-07
- Scope: skill
- Status: active · helpful 1 · harmful 0 · last_confirmed 2026-10-07
