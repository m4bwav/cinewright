---
title: Off-screen lines compile as voiceovers or leave the prompt; names are respelled inside spoken lines only
kind: decision
status: proposed
date: 2026-10-07
verified: 2026-10-07
stale_after: 2027-04-07
tags: [compile, dialogue, voice, minimax-h3, continuity]
summary: "Read before changing how `compile` writes dialogue, or adding a model card with speech: what happens to a line whose speaker is not in the shot, the silent clause for listeners, and `pronounce`"
---

# Off-screen lines compile as voiceovers or leave the prompt

## Context

In the library film (2026-10-07), Mark found a rival sorcerer's line in the hero's mouth. On card 6D the hero was alone in the shot and the rival shouted from the dark. The compiler wrote the line as a plain `<name> says: <d>...</d>`, and H3 lip-synced it to the only visible face. Mark has seen the same swap in other generated videos. He also heard the hero's name said less well than in his audiobook.

The H3 prompt guide has an exact phrase for this case: `says in an off-screen voiceover`, followed by a statement that the on-screen character's lips remain closed. It asks for each speaker to be identified, including whether they are on screen. It says nothing on pronunciation.

## Decision

- A dialogue speaker who is not in the card's cast counts as off screen. When the model card has a `dialogue_offscreen` template (H3 does), the line is written with it. When it has none, the line is left out of the prompt, and `compile` warns that it should be recorded and laid in the mix. A visible face would otherwise get the line.
- `dialogue_silent` (H3: `while the lips of {names} remain completely closed`) is added to every line, on or off screen, for the other people in the shot.
- `continuity diff` now warns OFFSCREEN, SPEAKERS (two speakers in one card), TONE (a tone that begins with a speech verb) and PRONOUNCE (a character's name in a line with no `pronounce` entry).
- `pronounce` in characters.json maps a word to a respelling. It is applied inside spoken lines only, as whole words. Identity strings, captions and the QC rubric keep the real spelling.
- The QC rubric marks off-screen lines "no visible mouth". The new failure code is `name-misread`.

## Reasons

- The vendor's own phrase beats an invented one (genvideo L-003: take a model's syntax from the vendor's guide).
- Leaving a line out is safer than letting a model guess its mouth: a missing line is cheap to fix in the mix, and a wrong mouth means a re-render.
- The rule existed only in prose, and an agent writing 25 cards missed it. A check catches it on every card.

## Rejected

- Moving off-screen lines into `sound` automatically. That loses the speaker's voice string and S-ID, and H3 has a documented form for the case.
- Erroring on an off-screen speaker. Voiceover and off-screen lines are a real film device, so a warning fits better.
- A `say_as` field on each character. It would not cover names that are spoken but have no character entry, such as an absent person.

## Not yet verified

No new render was made: Mark asked for none this pass. Two questions stay open and need short H3 tests: whether H3 obeys the voiceover phrase, and whether it reads a respelling as intended. Either way, a line in the wrong mouth can still be fixed in the mix.

Related: [../notes/2026-10-07-library-film-test.md](../notes/2026-10-07-library-film-test.md) (where it was found)
