---
title: Prop sheets
slug: prop-sheets
summary: A hero prop gets its own reference sheet (alone, grey backdrop, three angles and a detail), one sheet per state; the compiler sends it with every shot that holds or features the prop.
tags: [design, props, references, bible, consistency]
last_checked: 2026-10-09
sources: ["Houbre, How to keep AI-generated props consistent shot to shot, HackerNoon, 2026-09-21", "invideo FAQ, props reference sheets, 2026-07-27", "Pippit, in-hand scale test, 2026-09-02", "Runware, MiniMax H3 reference-driven consistency guide, 2026"]
---

# Prop sheets

## Rules

- Sheet a prop the story turns on, or one seen in more than one shot: three-quarter (the hero view, first in `refs`), front, side, and a detail close-up of its most characteristic surface. Add top or back only if a shot sees them.
- The prop stands alone: seamless mid-grey, flat even light, nothing else in frame. Never sheet it in a hand or with a character; the model copies the hand and guesses the grip. Character and prop sheets meet only in the shot prompt.
- Make every view by editing one locked hero image, never by re-prompting from text.
- One sheet per state. A prop that breaks, opens, burns or empties gets a `states` entry in `bibles/props.json` with its own full description and refs; a card picks it with `holding_state` (held) or `props[].state` (featured). Stretching one sheet across a change gives a different amount of change each shot.
- A prop nobody holds but the shot features (a tank, a cart, a parked car) goes in the card's `props` list with an optional `where`; the compiler pastes its description and sends its sheet.
- The compiler sends refs in order: characters, props, the set plate, the card's refs. Over the model's limit (a compile warning), drop the detail view first.
- Scale and grip go in the prompt: one familiar size comparison ("about the length of a forearm"), fingers visible at contact, under about 20 degrees of turn when only one view exists.
- When a prop drifts, fix the sheet, not the shot: every later shot inherits the fix.

## Numbers

- 3 to 4 views per state; 4 candidates per view; reflective or transparent props need close, evenly lit views.
- Budget about 3 takes per usable shot where a prop touches a character.

## Vocabulary

- prop sheet, hero view, state, featured prop, packshot.

## Pitfalls

- Small text and logos on a moving prop: no open model holds them in 2026. Keep text off the prop, or composite it in finish.
- A camera push-in read as the object growing: say the camera moves, not the prop.
- Two similar props in one shot merge; label each reference by index in the prompt.

## Verify

- `continuity diff` shows no PROP warning; each compiled prompt with the prop contains its description, and its params list the sheet's images.
