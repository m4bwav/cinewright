---
title: Screenplay format
slug: screenplay-format
summary: Slugline, action, character cue, parenthetical and dialogue layout in plain text, how the slugline maps to the scene bible, and the timing rule of a page.
tags: [script, screenplay, slugline, format]
last_checked: 2026-10-04
sources: ["Christopher Riley, The Hollywood Standard, 3rd ed., 2021", "https://fountain.io/syntax"]
---

# Screenplay format

## Rules

- Write `script.md` in Fountain-style plain text: it reads as a screenplay and needs no software.
- Slugline: `INT.` or `EXT.` (or `INT./EXT.`), the place, a hyphen, the time: `INT. LIGHTHOUSE LAMP ROOM - NIGHT`. The scene bible's `heading` is this line, character for character, and its `time_of_day` matches.
- Action lines: present tense, what the camera sees and hears, three lines or fewer per paragraph. A new paragraph suggests a new shot.
- Character cue: the name in capitals on its own line, then the dialogue under it. A parenthetical under the cue holds a short delivery note: `(quietly)`. The card's dialogue `tone` is that note.
- Introduce a character in capitals the first time, with age and one telling detail; the identity string in the character bible is that detail expanded.
- Sound that matters goes in the action in capitals once: `RAIN hammers the glass`. It becomes the card's `sound`.
- Never write camera directions in the script; they belong on the cards.

## Numbers

- One page in standard format (12-point Courier, about 55 lines) runs about one minute of screen time.
- A 30-60 s film: half a page to one page.

## Vocabulary

- slugline (scene heading), action (description), character cue, parenthetical, dialogue, transition (`CUT TO:`), V.O. (voice over), O.S. (off screen), CONT'D.

## Verify

- Every slugline in `script.md` equals a `heading` in `bibles/scenes.json`.
- Every spoken line in the script is on exactly one card's `dialogue`, with the same words.
