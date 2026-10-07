---
title: First end-to-end film test (a 120 s fantasy-novel adaptation, 2026-10-06 night)
kind: note
date: 2026-10-07
verified: 2026-10-07
stale_after: 2026-11-07
tags: [test, minimax-h3, compile, continuity, design]
summary: "Read before the release or any compiler change: what a real 25-card, 8-generation film found in cinewright, what was fixed on test/library-film, and what is still open"
---

# First end-to-end film test (2026-10-06 night)

Mark asked for a test before cinewright goes anywhere public: a 2-minute adaptation of one chapter of a fantasy novel (a sorcerer alone in an ancient library dozes over his finds and wakes inside a trap set by seven rival sorcerers, who burn the library down around him), planned with cinewright and rendered all night on the maintainer's local MiniMax H3 pipeline. The film folder, the night log and the source passage stay outside the repository (path in the vault sidecar).

## What ran

- `brief.md`, `script.md`, `design.md`, five bibles, 25 cards in 8 scenes, written by a builder script; `cards validate` 0 errors.
- `continuity diff` found 6 real errors on the first draft (two prop hand-offs, three 30-degree jump cuts, a wardrobe slip); 0 after fixes.
- `compile --model minimax-h3 --sequence`: 8 generations of 15.08 s (362 frames), 3-4 shots each.
- Five passes of 8 generations (40 renders, about 17 min each) between 21:17 and about 08:35; references and guide stills on a second machine. Best-of cut at 120.000 s.

## Defects found and fixed (branch test/library-film)

1. **15 s planned 345 frames (14.4 s).** The H3 card said 4-15 s; 362 frames is 15.08 s, the model's maximum. Card now `[4, 15.1]`; `plan_length(15)` gives 362. Eight 14.4 s sections could not fill 120 s.
2. **A scene's travel was stated on every card**, so a close-up of a man lighting a candle said he was "walking away from the camera". `card_parts` now states only the card's own travel; the scene's travel stays the continuity check's reference.
3. **"at the the dragon"** when `looks_at` began with an article. Fixed.
4. **`cards export --film-json` could not express a `--sequence` render** (one shot per card, lengths off the frame grid). New `--sequence --model <card>`: one shot per generation, named like the compiled prompt, frames from the model's grid, refs from the compile.
5. **Budgets** (Mark's answers on 2026-10-06): runtime row counted once, skill folder without shared/lib copies; three descriptions trimmed (3,994 of 4,000). All rows green.

Tests: 73 on Python 3.14 and 3.9 (3 new: export sequence, 362 frames, card-only travel and no double article).

## Open findings (not fixed; for S8 or the next compiler pass)

- **The sequence header introduces every cast member at the top, so everyone appears in every shot.** A 3 s wake-up close-up of the sleeper at the end of his own dream put him in the dream beside the dreamer; a dreamer standing in shot 1 and kneeling in shot 2 became two people. Workaround: keep a scene's cast to people physically present for its whole length, and name the same person in each action. Fix idea: per-shot cast lines in the sequence block, or warn when a cast member is in fewer than all shots of a sequence.
- **No per-scene constants.** The style bible's `lighting` is the only verbatim film-wide slot; a film-wide line about a magic shield invited an unscripted shield into a calm reading scene, and "exactly one <hero>" named him in a dream he is not in. Workaround: one style bible per scene group and `compile --style` per group. Fix idea: a `constants` field on scenes.json, compiled into the sequence head.
- **Dialogue `tone` is pasted after "says"**, so it must be an adverbial ("with a smirk"); "mutters under his breath" gave "says mutters...". Fix idea: document in the schema description, or lint tones that start with a verb.
- **Word count**: every sequence was 344-623 words against the 300-word guide (three identity strings repeated). H3 followed all of them; the guide may be too low for multi-shot H3, or identities should be shortened for crowd scenes.
- `compile` without `--out` prints and writes nothing; fine, but the first run looked like a failure.

## Lessons recorded

- cinewright-design L-004 `effect-substance`: name what an invented effect is made of and what it lacks ("dragon heads of fire" drew winged lizards; the source's spell is a bodiless head and neck of fire and light).
- cinewright-genvideo L-006 to L-008 (this note): simile taken literally, numbers in identity strings rendered literally, reference stills carry composition.

## What the owner corrected during the night (all applied)

Spell dragons are bodiless constructs, a real dragon in the dream stays a beast; the shield is a sphere around the sorcerer; never two of the hero; the fight is inside the library and burns it down; the levitating sorcerers have no wires (the book's "as though from wires" is a simile); keep the dream intact.

Related: builds on [2026-10-06-s7-install-proof.md](2026-10-06-s7-install-proof.md); see also [../plans/PLAN.md](../plans/PLAN.md)
